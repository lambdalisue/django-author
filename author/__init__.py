#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
initialization django-object-permission

Add this backend to your ``AUTHENTICATION_BACKENDS`` like below::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'object_permission.backends.ObjectPermBackend',
    )

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
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

import backends
import recivers

settings.AUTHOR_BACKEND = getattr(settings, 'AUTHOR_BACKEND', backends.AuthorDefaultBackend)

settings.AUTHOR_CREATED_BY_FIELD_NAME = getattr(settings, 'AUTHOR_CREATED_BY_FIELD_NAME', 'author')
settings.AUTHOR_UPDATED_BY_FIELD_NAME = getattr(settings, 'AUTHOR_UPDATED_BY_FIELD_NAME', 'updated_by')
settings.AUTHOR_DO_NOT_UPDATE_WHILE_USER_IS_NONE = getattr(settings, 'AUTHOR_DO_NOT_UPDATE_WHILE_USER_IS_NONE', True)

settings.AUTHOR_MODELS = getattr(settings, 'AUTHOR_MODELS', None)
settings.AUTHOR_IGNORE_MODELS = getattr(settings, 'AUTHOR_IGNORE_MODELS', [
        'auth.user',
        'auth.group',
        'auth.permission',
        'contenttypes.contenttype',
    ])

def load_backend(path):
    """load author backend from string path"""
    i = path.rfind('.')
    module ,attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing author backend %s: "%s"' % (path, e))
    except ValueError, e:
        raise ImproperlyConfigured('Error importing author backend. Is AUTHOR_BACKEND a correctly defined?')
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" author backend' % (module, attr))
    
    if not hasattr(cls, 'get_user'):
        raise ImproperlyConfigured('Error author backend must have "get_user" method Please define it in %s.' % cls)
    return cls()

def get_backend_class():
    """get author backend"""
    backend = settings.AUTHOR_BACKEND
    if isinstance(backend, basestring):
        return load_backend(backend)
    elif isinstance(backend, object) and hasattr(backend, 'get_user'):
        return backend
    else:
        raise ImproperlyConfigured('Error author backend must have "get_user" method Please define it in %s.' % backend)

def get_backend():
    backend_class = get_backend_class()
    return backend_class()

# Register recivers
recivers.register()
