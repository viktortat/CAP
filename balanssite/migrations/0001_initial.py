# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-15 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schet_site', models.FloatField(verbose_name='Баланс сайта')),
                ('reklama', models.FloatField(verbose_name='Зачислено на рекламу')),
                ('vivod', models.FloatField(verbose_name='Сумма к выводу')),
            ],
            options={
                'db_table': 'balans',
            },
        ),
    ]
