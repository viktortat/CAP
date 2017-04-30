# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 00:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20170126_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasksa',
            name='url',
        ),
        migrations.AddField(
            model_name='tasksa',
            name='cat',
            field=models.CharField(choices=[('0', 'Клики'), ('1', 'Клики YouTube'), ('2', 'Разгадать капчу'), ('3', 'Регистрация без активности'), ('4', 'Регистрация с активности'), ('5', 'Социальные сети'), ('6', 'Постинг в форум'), ('7', 'Постинг в блоги'), ('8', 'Голосование'), ('9', 'Загрузка файлов'), ('10', 'Прочее')], default='Выбор', max_length=30, verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='tasksa',
            name='moder',
            field=models.BooleanField(default=False, verbose_name='Модерация'),
        ),
        migrations.AddField(
            model_name='tasksusers',
            name='otvet_task',
            field=models.IntegerField(default=0, verbose_name='Выполение задания'),
        ),
        migrations.AlterField(
            model_name='tasksa',
            name='odobren',
            field=models.BooleanField(default=False, verbose_name='Одобрить'),
        ),
        migrations.AlterField(
            model_name='tasksa',
            name='opisan',
            field=models.TextField(max_length=2000, verbose_name='Описание оплачиваемого задания'),
        ),
        migrations.AlterField(
            model_name='tasksa',
            name='price_task',
            field=models.FloatField(default=0, verbose_name='Укажите сумму баланса задания'),
        ),
        migrations.AlterField(
            model_name='tasksa',
            name='url_admin',
            field=models.URLField(verbose_name='URL сайта (включая http://)'),
        ),
    ]
