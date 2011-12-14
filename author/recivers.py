#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
signal recivers for django-author


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
import logging

from django.conf import settings
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)

def pre_save_callback(sender, instance, **kwargs):
    from . import get_backend

    if "%s.%s" % (instance._meta.app_label, str(instance.__class__).lower()) in settings.AUTHOR_IGNORE_MODELS:
        return
    if not hasattr(instance, settings.AUTHOR_CREATED_BY_FIELD_NAME):
        return
    # get current user via author backend
    user = get_backend().get_user()
    if settings.AUTHOR_DO_NOT_UPDATE_WHILE_USER_IS_NONE and user is None:
        return
    if getattr(instance, settings.AUTHOR_CREATED_BY_FIELD_NAME) is None:
        setattr(instance, settings.AUTHOR_CREATED_BY_FIELD_NAME, user)
    if hasattr(instance, settings.AUTHOR_UPDATED_BY_FIELD_NAME):
        setattr(instance, settings.AUTHOR_UPDATED_BY_FIELD_NAME, user)

def register():
    if settings.AUTHOR_MODELS:
        for model in settings.AUTHOR_MODELS:
            app_label, model = model.split('.', 1)
            ct = ContentType.objects.get_by_natural_key(app_label, model)
            pre_save.connect(pre_save_callback, sender=ct.model_class())
    else:
        pre_save.connect(pre_save_callback)
