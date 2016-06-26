********
django-author
********
.. image:: https://travis-ci.org/lambdalisue/django-author.svg
    :target: https://travis-ci.org/lambdalisue/django-author
.. image:: https://coveralls.io/repos/github/lambdalisue/django-author/badge.svg?branch=master
    :target: https://coveralls.io/github/lambdalisue/django-author?branch=master
    
Update author and updated_by fields of models automatically

This library is used for updating ``author`` and ``updated_by`` fields automatically
with ``request.user`` when the model has created/changed.

Also if you are too lazy to write ``author = models.ForeignKey(User, _('author'), related_name ...)`` to every model,
just add ``@with_author`` decorator to the top of class makes you happy.


Install
==============
This library is on PyPI so you can install it with::

    pip install django-author

or from github::
    
    pip install git+https://github.com/lambdalisue/django-author.git


Usage
==========

1.  Add 'author' to your ``INSTALLED_APPS`` on settings.py

2.  Add 'author.middlewares.AuthorDefaultBackendMiddleware' to your ``MIDDLEWARE_CLASSES``
    if you use default author backend

3.  Add ``author`` and ``updated_by`` field to models which you want to have ``author`` and ``updated_by`` fields manually
    or use ``@with_author`` decorator like below::

        from django.db import models
        from author.decorators import with_author

        @with_author
        class Entry(models.Model):
            title = models.CharField('title', max_length=50)
            body = models.TextField('body')

4.  Done. Now you have automatically updated ``author`` and ``updated_by`` fields

    If you are in truble, see ``author_test`` directory for usage sample.


Settings
================

AUTHOR_BACKEND
    Class or string path of backend. the backend is used to determine user when object is created/updated.

AUTHOR_CREATED_BY_FIELD_NAME
    A name of field. the setting also interfer the name of field created by ``@with_author`` decorator. default is 'author'

AUTHOR_UPDATED_BY_FIELD_NAME
    A name of field. the setting also interfer the name of field created by ``@with_author`` decorator. default is 'updated_by'

AUTHOR_DO_NOT_UPDATE_WHILE_USER_IS_NONE
    Do not update ``author`` or ``updated_by`` field when detected user is None. default is True

AUTHOR_MODELS
    Check signals for only these models. default is None

AUTHOR_IGNORE_MODELS
    Do not check signals for these models. default is ['auth.user', 'auth.group', 'auth.permission', 'contenttype.contenttype']


Backend
==============
The default backend use ``thread_locals`` storategy to get current request in signal call.

If you want to change the strategy or whatever, create your own backend.

A backend is a class which have ``get_user`` method to determine current user.

AuthorDefaultBackend
    Default backend. This backend return None when no request found or AnonymousUser create/update object.

AuthorSystemUserBackend
    System user backend. This backend return system user when no request found or AnonymousUser create/update object.

    system user is determined with ``get_system_user`` method and default is ``User.objects.get(pk=1)``
