# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 17:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок теста')),
                ('opisan', models.CharField(max_length=1000, verbose_name='Инструкции для тестирования')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('time_t', models.CharField(choices=[('ONE_T', 'Доступно всем каждые 24 часа'), ('TWO_T', '30 секунд + 0.004 руб.')], default='Выбор', max_length=30, verbose_name='Технология тестирования')),
                ('vid_t', models.CharField(choices=[('ONE_T', 'Нет'), ('TWO_T', 'Выделить тест среди других + 0.01 руб.')], default='Выбор', max_length=30, verbose_name='Технология тестирования')),
                ('audit', models.CharField(choices=[('VSE', 'Все пользователи'), ('ONE_TWO', '1/2 польователей'), ('ONE_THREE', '1/3 польователей'), ('ONE_FOUR', '1/4 польователей'), ('MEDL', 'Очень медленный серфинг'), ('SUPM', 'Супер медленный серфинг'), ('CHEREP', 'Черепаший серфинг')], default='Выбор', max_length=10, verbose_name='Аудитория смотрящих')),
                ('quest_1', models.CharField(max_length=300, verbose_name='Содержание вопроса №1')),
                ('quest_1_ans_1', models.CharField(max_length=30, verbose_name='Вариант ответа (правильный)')),
                ('quest_1_ans_2', models.CharField(max_length=30, verbose_name='Вариант ответа (ложный)')),
                ('quest_1_ans_3', models.CharField(max_length=30, verbose_name='Вариант ответа (ложный)')),
                ('quest_2', models.CharField(max_length=300, verbose_name='Содержание вопроса №2')),
                ('quest_2_ans_1', models.CharField(max_length=30, verbose_name='Вариант ответа (правильный)')),
                ('quest_2_ans_2', models.CharField(max_length=30, verbose_name='Вариант ответа (ложный)')),
                ('quest_2_ans_3', models.CharField(max_length=30, verbose_name='Вариант ответа (ложный)')),
                ('quest_3', models.CharField(max_length=300, verbose_name='Содержание вопроса №3')),
                ('quest_3_ans_1', models.CharField(max_length=30, verbose_name='Вариант ответа (правильный)')),
                ('quest_3_ans_2', models.CharField(max_length=30, verbose_name='Вариант ответа (ложный)')),
                ('quest_3_ans_3', models.CharField(max_length=30, verbose_name='Вариант ответа (ложный)')),
                ('porod', models.CharField(choices=[('VSEPOLZOV', 'Все пользователи'), ('UCH', 'Учится в школе'), ('STUDENT', 'Студент'), ('PRED', 'Предприниматель'), ('RAB_P', 'Работники на предприятиях'), ('SLUG_P', 'Служащие на предприятиях'), ('BOMR', 'Без основного места работы')], default='Выбор', max_length=10, verbose_name='По роду деятельности')),
                ('pofamaly', models.CharField(choices=[('MARRIED', 'Женат\\замужем, есть дети'), ('MARRIEDS', 'Женат\\замужем, нет детей'), ('NOMARRIED', 'Не женат\\Не замужем, есть дети'), ('NOMARRIEDS', 'Не женат\\Не замужем, нет детей'), ('DIVORCED', 'Разведен\\разведена, есть дети'), ('DIVORCEDS', 'Разведен\\разведена, нет детей')], default='Выбор', max_length=10, verbose_name='По семейному положению')),
                ('posex', models.CharField(choices=[('MEN_SEX', 'Мужчина'), ('WOOMEN_SEX', 'Женщина')], default='Выбор', max_length=10, verbose_name='По половому признаку')),
                ('poage', models.CharField(choices=[('LUB_AGE', 'Любой возраст'), ('SIXT_AGE', 'От 16 до 18'), ('EIGHT_AGE', 'От 18 до 20'), ('TWENT_AGE', 'От 20 до 25'), ('TWENTF_AGE', 'От 25 до 30'), ('THIRT_AGE', 'От 30 до 40'), ('FORTY_AGE', 'От 40 до 50'), ('FIVETY_AGE', 'От 50 до 70')], default='Выбор', max_length=10, verbose_name='По возрасту')),
                ('pravila', models.BooleanField(default=False, verbose_name='Я согласен(на) с правилами размещения рекламы на WMR_LOVE')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'billtest',
            },
        ),
    ]
