# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=50, verbose_name='title')),
                ('body', models.TextField(verbose_name='body')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date and time created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date and time updated')),
                ('author', models.ForeignKey(related_name='entry_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
                ('updated_by', models.ForeignKey(related_name='entry_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
