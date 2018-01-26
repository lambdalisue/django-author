# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8:
"""
backends for django-author

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
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured

from .middlewares import get_request


class AuthorDefaultBackend(object):
    """Author default backend

    Get current user from request stored in thread_locals.
    Return None when request.user is not detected include request.user
    is AnonymousUser

    """

    def __init__(self):

        required_middleware = 'author.middlewares.AuthorDefaultBackendMiddleware'

        if hasattr(settings, 'MIDDLEWARE'):
            middlewares = settings.MIDDLEWARE
        else:
            middlewares = settings.MIDDLEWARE_CLASSES

        if (
                required_middleware not in middlewares
        ):
            raise ImproperlyConfigured(
                'Error "%s" is not found in MIDDLEWARE_CLASSES nor MIDDLEWARE. '
                'It is required to use AuthorDefaultBackend' % required_middleware,
            )

    def _get_user_model(self):
        """get user model class"""
        return auth.get_user_model()

    def _get_request(self):
        """get current request"""
        return get_request()

    def get_user(self):
        """get current user"""
        request = self._get_request()
        if request and getattr(request, 'user', None):
            if isinstance(request.user, self._get_user_model()):
                return request.user
        # AnonymousUser
        return None


class AuthorSystemUserBackend(AuthorDefaultBackend):
    """Author System user backend

    Get current user from request stored in thread_locals.
    Return System user when request.user is not detected include request.user
    is AnonymousUser

    System user is detected with ``get_system_user``

    """

    def _get_filter_kwargs(self):
        """get kwargs for filtering user"""
        return {'pk': 1}

    def get_system_user(self):
        """get system user"""
        user_model = self._get_user_model()
        user = user_model._default_manager.get(**self._get_filter_kwargs())
        return user

    def get_user(self):
        """get current user"""
        request = self._get_request()
        if request and getattr(request, 'user', None):
            if isinstance(request.user, self._get_user_model()):
                return request.user
        # AnonymousUser
        return self.get_system_user()
