# -*- coding: utf-8 -*-
#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
middlewares for django-author


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
from threading import local
import django


__all__ = ['get_request', 'AuthorDefaultBackendMiddleware']
_thread_locals = local()

def get_request():
    """Get request stored in current thread"""
    return getattr(_thread_locals, 'request', None)

class AuthorDefaultBackendMiddleware(object):
    def process_request(self, request):
        _thread_locals.request = request

    def process_response(self, request, response):
        _thread_locals.request = None
        return response

if django.VERSION > (1,10):
    from django.utils import deprecation
    class AuthorDefaultBackendMiddlewareNewStyle(deprecation.MiddlewareMixin, AuthorDefaultBackendMiddleware):
        pass
