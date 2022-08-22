# vim: set fileencoding=utf8:
"""
Unittest module of settings


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

from django.test import TestCase

from author.conf import settings


class AuthorSettingsTestCase(TestCase):
    """Test the lazy settings provide defaults and access to django settings"""

    def test_a_django_setting(self):
        """Test the lazy settings fallback to django settings"""
        time_zone = settings.TIME_ZONE
        self.assertEqual(time_zone, "America/Chicago")

    def test_author_created_by_field(self):
        """Test the default author created by field name"""
        field_name = settings.AUTHOR_CREATED_BY_FIELD_NAME
        self.assertEqual(field_name, "author")

    def test_author_updated_by_field(self):
        """Test the default author updated by field name"""
        field_name = settings.AUTHOR_UPDATED_BY_FIELD_NAME
        self.assertEqual(field_name, "updated_by")

    def test_author_not_update(self):
        """Test the default author 'do not updated while user is none' setting"""
        not_update = settings.AUTHOR_DO_NOT_UPDATE_WHILE_USER_IS_NONE
        self.assertTrue(not_update)

    def test_author_models(self):
        """Test the default author models"""
        author_models = settings.AUTHOR_MODELS
        self.assertIsNone(author_models)

    def test_author_ignore_models(self):
        """Test the default ignored models"""
        ignore_models = settings.AUTHOR_IGNORE_MODELS
        expected_ignored = [
            "auth.user",
            "auth.group",
            "auth.permission",
            "contenttypes.contenttype",
        ]
        self.assertEqual(ignore_models, expected_ignored)

    def test_unknown_setting(self):
        """Test an unknown setting"""
        with self.assertRaises(AttributeError):
            _ = settings.UNKNOWN_SETTING
