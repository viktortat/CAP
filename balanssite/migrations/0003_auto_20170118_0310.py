# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 00:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balanssite', '0002_balans_vseviplati'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balans',
            name='reklama',
            field=models.FloatField(default=0, verbose_name='Зачислено на рекламу'),
        ),
        migrations.AlterField(
            model_name='balans',
            name='schet_site',
            field=models.FloatField(default=0, verbose_name='Баланс сайта'),
        ),
        migrations.AlterField(
            model_name='balans',
            name='vivod',
            field=models.FloatField(default=0, verbose_name='Сумма к выводу'),
        ),
    ]
