# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20170121_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogsite',
            name='price',
            field=models.FloatField(default=0, verbose_name='Сумма'),
        ),
    ]
