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

from blog import models

from django.contrib.auth.hashers import make_password
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
        with self.assertRaisesRegexp(
            ImproperlyConfigured,
            r'Error "author.middlewares.AuthorDefaultBackendMiddleware" is not found '
            'in MIDDLEWARE_CLASSES nor MIDDLEWARE. It is required to use AuthorDefaultBackend',
        ):
            entry.save()


@override_settings(
    AUTHOR_BACKEND='author.backends.AuthorSystemUserBackend',
)
class AuthorSystemUserBackendTestCase(TestCase):
    def test_save(self):
        """Test that AuthorSystemBackend saves with default user"""
        user = User.objects.create(pk=1)
        entry = models.Entry(title='foo', body='bar')
        entry.save()
        self.assertEqual(entry.author, user)

    def test_with_request(self):
        admin = User.objects.create(pk=1, username='admin', password=make_password('password'))
        try:  # Django >= 1.9
            self.client.force_login(admin)
        except AttributeError:
            assert self.client.login(username='admin', password='password')
        response = self.client.post(
            '/create/',
            {
                'title': 'barbar',
                'body': 'barbar',
            },
        )
        # if post success, redirect occur
        self.assertEqual(response.status_code, 302)

        entry = models.Entry.objects.get(title='barbar')
        self.assertEqual(entry.author, admin)
        self.assertEqual(entry.updated_by, admin)


class AuthorBackendSettingsTestCase(TestCase):
    @override_settings(
        AUTHOR_BACKEND='author.backends.FooBackend',
    )
    def test_unexistent_backend(self):
        entry = models.Entry(title='foo', body='bar')
        with self.assertRaisesRegexp(
            ImproperlyConfigured,
            'Module "author.backends" does not define a "FooBackend" author backend',
        ):
            entry.save()

    @override_settings(
        AUTHOR_BACKEND=1234,
    )
    def test_wrong_class(self):
        entry = models.Entry(title='foo', body='bar')
        with self.assertRaisesRegexp(
            ImproperlyConfigured,
            'Error author backend must have "get_user" method Please define it in 1234',
        ):
            entry.save()

    @override_settings(
        AUTHOR_BACKEND='foo',
    )
    def test_error_importing(self):
        entry = models.Entry(title='foo', body='bar')
        with self.assertRaisesRegexp(
            ImproperlyConfigured,
            r'Error importing author backend foo: "No module named \'?fo\'?',
        ):
            entry.save()

    @override_settings(
        AUTHOR_BACKEND='.',
    )
    def test_value_error(self):
        entry = models.Entry(title='foo', body='bar')
        with self.assertRaisesRegexp(
            ImproperlyConfigured,
            'Error importing author backend. Is AUTHOR_BACKEND a correctly defined?',
        ):
            entry.save()
