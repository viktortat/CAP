# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 17:17
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20170113_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksa',
            name='opisan',
            field=ckeditor.fields.RichTextField(max_length=2000, verbose_name='Описание оплачиваемого задания'),
        ),
    ]
