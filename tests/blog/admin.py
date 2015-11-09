# -*- coding: utf-8 -*-
# admin.py

from django.contrib import admin
from .models import *

admin.site.register(Entry, admin.ModelAdmin)
