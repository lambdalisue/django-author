# -*- coding: utf-8 -*-
#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
decorators for django-author


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
from django.conf import settings
from django.db import models
from django.utils.text import ugettext_lazy as _

from . import get_backend


def with_author(cls):
    """Decorator to add created_by/updated_by field to particular model"""
    def _get_user_model():
        from django.contrib.auth.models import User
        backend = get_backend()
        return backend._get_user_model() if hasattr(backend, '_get_user_model') else User

    user_model = _get_user_model()
    verbose_name_plural = cls._meta.object_name
    created_by = models.ForeignKey(user_model, verbose_name=_('author'), related_name='%s_create' % verbose_name_plural.lower(), null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(user_model, verbose_name=_('last updated by'), related_name='%s_update' % verbose_name_plural.lower(), null=True, blank=True, on_delete=models.SET_NULL)

    if not hasattr(cls, settings.AUTHOR_CREATED_BY_FIELD_NAME):
        cls.add_to_class(settings.AUTHOR_CREATED_BY_FIELD_NAME, created_by)
    if not hasattr(cls, settings.AUTHOR_UPDATED_BY_FIELD_NAME):
        cls.add_to_class(settings.AUTHOR_UPDATED_BY_FIELD_NAME, updated_by)

    return cls
