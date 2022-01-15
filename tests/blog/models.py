# vim: set fileencoding=utf8:
"""
Mini blog models

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
__VERSION__ = "0.1.0"

from author.decorators import with_author

try:
    from django.urls import reverse
except ImportError:  # Django<2.0
    from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _


# This class decorator (@with_author) is all you need to add `author` and `updated_by` field
# to particular model.
# If you are using Python under 2.4, use the following code insted::
#
#   class Entry(models.Mode):
#       # brabrabra
#   Entry = with_author(Entry)
#
@with_author
class Entry(models.Model):
    """mini blog entry model

    >>> entry = Entry()

    # Attribute test
    >>> assert hasattr(entry, 'title')
    >>> assert hasattr(entry, 'body')
    >>> assert hasattr(entry, 'created_at')
    >>> assert hasattr(entry, 'updated_at')

    # Function test
    >>> assert callable(getattr(entry, '__unicode__'))
    >>> assert callable(getattr(entry, 'get_absolute_url'))
    """
    title = models.CharField(_('title'), max_length=50, unique=True)
    body = models.TextField(_('body'))

    created_at = models.DateTimeField(
        _('date and time created'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('date and time updated'),
        auto_now=True,
    )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-entry-detail', None, (), {'slug': self.title})

    def clean(self):
        """custom validation"""
        from django.core.exceptions import ValidationError
        if self.title in ('create', 'update', 'delete'):
            raise ValidationError(
                """The title cannot be 'create', 'update' or 'delete'""")
