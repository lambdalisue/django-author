# vim: set fileencoding=utf8:
"""
Unittest module of ...


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

from author import recivers

from blog import models

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.test import TestCase
from django.test.utils import override_settings

from mock import patch


class TestPreSaveCallback(TestCase):
    @override_settings(
        AUTHOR_IGNORE_MODELS=['blog.entry'],
    )
    def test_ignore_models(self):
        """blog.Entry: setting author on ignored models doesn't do anything"""
        instance = models.Entry.objects.create()
        recivers.pre_save_callback(None, instance)
        self.assertEqual(instance.author, None)
        self.assertEqual(instance.updated_by, None)

    @override_settings(
        AUTHOR_CREATED_BY_FIELD_NAME='foo',
    )
    def test_ignore_models_created_field(self):
        """blog.Entry: setting author on nonexistent field doesn't do anything"""
        instance = models.Entry.objects.create()
        recivers.pre_save_callback(None, instance)
        self.assertEqual(instance.author, None)
        self.assertEqual(instance.updated_by, None)

    def test_callback_no_user(self):
        """blog.Entry: setting author is ignored"""
        instance = models.Entry.objects.create()
        recivers.pre_save_callback(None, instance)
        self.assertEqual(instance.author, None)
        self.assertEqual(instance.updated_by, None)

    @patch('author.backends.AuthorDefaultBackend.get_user')
    def test_callback(self, get_user):
        """blog.Entry: callbacks runned """
        user = User.objects.create()
        get_user.return_value = user
        instance = models.Entry.objects.create()
        recivers.pre_save_callback(None, instance)
        self.assertEqual(instance.author, user)
        self.assertEqual(instance.updated_by, user)


class TestBlankSettingsTestCase(TestCase):
    @override_settings(
        AUTHOR_MODELS=['auth.user'],
    )
    def test_author_models_settings_blank(self):
        """blog.Entry: callbacks are not created"""
        pre_save.disconnect(recivers.pre_save_callback)
        self.assertEqual(pre_save._live_receivers(models.Entry), [])
        recivers.register()
        self.assertEqual(pre_save._live_receivers(models.Entry), [])


class TestSettingsTestCase(TestCase):
    @override_settings(
        AUTHOR_MODELS=['blog.entry'],
    )
    def test_author_models_settings(self):
        """blog.Entry: callbacks are created"""
        self.assertEqual(pre_save._live_receivers(models.Entry), [])
        recivers.register()
        self.assertEqual(pre_save._live_receivers(models.Entry)[0], recivers.pre_save_callback)
