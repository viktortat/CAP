# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-12 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20170112_0311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasksusers',
            old_name='title',
            new_name='taskuser',
        ),
        migrations.RemoveField(
            model_name='tasksa',
            name='audit',
        ),
        migrations.RemoveField(
            model_name='tasksa',
            name='poage',
        ),
        migrations.RemoveField(
            model_name='tasksa',
            name='pofamaly',
        ),
        migrations.RemoveField(
            model_name='tasksa',
            name='pomet',
        ),
        migrations.RemoveField(
            model_name='tasksa',
            name='porefer',
        ),
        migrations.RemoveField(
            model_name='tasksa',
            name='porep',
        ),
        migrations.AddField(
            model_name='tasksa',
            name='odobren',
            field=models.BooleanField(default=False, verbose_name='Одобраить'),
        ),
        migrations.AlterField(
            model_name='tasksa',
            name='interval',
            field=models.CharField(choices=[('BEZ_INTER', 'Без интервала'), ('ONE_M', '1 минута'), ('TWO_M', '2 минуты'), ('FIVE_M', '5 минут'), ('TEN_M', '10 минут'), ('TWENTY_M', '20 минут'), ('THIRTY_M', '30 минут'), ('ONE_H', '1 час'), ('TWO_H', '2 часа'), ('SIX_H', '6 часов'), ('TVEL_H', '12 часов'), ('TWNTYF_H', '24 часа')], default='Выбор', max_length=10, verbose_name='Минимальный интервал очереди последовательной раздачи заданий'),
        ),
    ]
