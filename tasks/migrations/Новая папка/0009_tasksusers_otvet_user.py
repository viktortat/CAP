# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-15 23:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0008_auto_20170115_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksusers',
            name='otvet_user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
