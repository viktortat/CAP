# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billtest', '0003_auto_20170123_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billtest',
            name='opisan',
            field=models.TextField(max_length=1000, verbose_name='Инструкции для тестирования'),
        ),
    ]
