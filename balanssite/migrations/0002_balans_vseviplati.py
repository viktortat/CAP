# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balanssite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='balans',
            name='vseviplati',
            field=models.FloatField(default=0, verbose_name='Сумма всех выплат'),
        ),
    ]
