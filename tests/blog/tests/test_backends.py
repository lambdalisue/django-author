# vim: set fileencoding=utf8:
"""
Unittest module of models


AUTHOR:
    Petr Dlouhý (petr.dlouhy@email.cz)

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

from author.backends import AuthorSystemUserBackend

from blog import models

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.utils import override_settings

import settings


class AuthorBackendTestCase(TestCase):
    @override_settings(
        MIDDLEWARE=settings.BASE_MIDDLEWARES,
        MIDDLEWARE_CLASSES=settings.BASE_MIDDLEWARES,
    )
    def test_improperly_configured(self):
        """Test, that if author backend is missing, it throws error"""
        entry = models.Entry(title='foo', body='bar')
        with self.assertRaises(ImproperlyConfigured):
            entry.save()


class AuthorSystemUserBackendTestCase(TestCase):
    @override_settings(
        AUTHOR_BACKEND=AuthorSystemUserBackend,
    )
    def test_save(self):
        """Test that AuthorSystemBackend saves with default user"""
        user = User.objects.create(pk=1)
        entry = models.Entry(title='foo', body='bar')
        entry.save()
        self.assertEqual(entry.author, user)
