# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Tasksa(models.Model):
    class Meta():
        db_table = 'task'
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    TECH = (
        ('ONE', 'Один пользователь - одно выполнение'),
        ('MNOGO', 'Задание можно выполнять многократно'),
    )

    SROCK = (
            ('one_h', '1 час'),
            ('two_h', '2 часа'),
            ('six_h', '6 часов'),
            ('tvel_h', '12 часов'),
            ('one_d', '1 день'),
            ('two_d', '2 дня'),
            ('three_d', '3 дня'),
            ('five_d', '5 дней'),
    )

    INTERVAL = (
        ('BEZ_INTER', 'Без интервала'),
        ('ONE_M', '1 минута'),
        ('TWO_M', '2 минуты'),
        ('FIVE_M', '5 минут'),
        ('TEN_M', '10 минут'),
        ('TWENTY_M', '20 минут'),
        ('THIRTY_M', '30 минут'),
        ('ONE_H', '1 час'),
        ('TWO_H', '2 часа'),
        ('SIX_H', '6 часов'),
        ('TVEL_H', '12 часов'),
        ('TWNTYF_H', '24 часа'),
    )

    AIDIT = (
            ('VSE', 'Все пользователи'),
            ('IZBRAN', 'Только исполнители из списка избарнных'),
    )

    PO_REFER = (
        ('VSEP', 'Все пользователи'),
        ('BEZREFER', 'Только пользователи без реферала'),
        ('MOIREFER', 'Только мой рефералы'),
    )

    PO_RATING = (
        ('VSEPOL', 'Все пользователи'),
        ('RAB_R', 'Все с рейтингом "Рабочий" и выше'),
        ('FIVE_R', 'От 5 баллов и выше'),
        ('TEN_R', 'От 10 баллов и выше'),
        ('TWENTY_R', 'От 20 баллов и выше'),
        ('FIVETY_R', 'От 50 баллов и выше'),
        ('ONEH_R', 'От 100 баллов и выше'),
        ('THREEH_R', 'От 300 баллов и выше'),
        ('FIVEH_R', 'От 500 баллов и выше'),
    )

    PO_REP = (
        ('VSEPOLZ', 'Все пользователи'),
        ('ZERO_REP', 'С репутацией от 0 и выше'),
        ('ONE_REP', 'С репутацией от 1 и выше'),
        ('FIVE_REP', 'С репутацией от 5 и выше'),
        ('TEN_REP', 'С репутацией от 10 и выше'),
        ('TWENTY_REP', 'С репутацией от 20 и выше'),
        ('THIRTY_REP', 'С репутацией от 30 и выше'),
        ('FIVETY_REP', 'С репутацией от 50 и выше'),
        ('ONEH_R', 'С репутацией от 100 и выше'),
    )

    PO_MET = (
        ('VSEPOLZOV', 'Все пользователи'),
        ('UCH', 'Учится в школе'),
        ('STUDENT', 'Студент'),
        ('PRED', 'Предприниматель'),
        ('RAB_P', 'Работники на предприятиях'),
        ('SLUG_P', 'Служащие на предприятиях'),
        ('BOMR', 'Без основного места работы'),
    )

    PO_FAMALY = (
        ('MARRIED', 'Женат\замужем, есть дети'),
        ('MARRIEDS', 'Женат\замужем, нет детей'),
        ('NOMARRIED', 'Не женат\Не замужем, есть дети'),
        ('NOMARRIEDS', 'Не женат\Не замужем, нет детей'),
        ('DIVORCED', 'Разведен\разведена, есть дети'),
        ('DIVORCEDS', 'Разведен\разведена, нет детей'),
    )

    PO_SEX = (
        ('VSE', 'Все пользователи'),
        ('MEN_SEX', 'Мужчина'),
        ('WOOMEN_SEX', 'Женщина'),
    )

    PO_AGE = (
        ('LUB_AGE', 'Любой возраст'),
        ('SIXT_AGE', 'От 16 до 18'),
        ('EIGHT_AGE', 'От 18 до 20'),
        ('TWENT_AGE', 'От 20 до 25'),
        ('TWENTF_AGE', 'От 25 до 30'),
        ('THIRT_AGE', 'От 30 до 40'),
        ('FORTY_AGE', 'От 40 до 50'),
        ('FIVETY_AGE', 'От 50 до 70'),
    )

    CAT = (
        ('0', 'Клики'),
        ('1', 'Клики YouTube'),
        ('2', 'Разгадать капчу'),
        ('3', 'Регистрация без активности'),
        ('4', 'Регистрация с активности'),
        ('5', 'Социальные сети'),
        ('6', 'Постинг в форум'),
        ('7', 'Постинг в блоги'),
        ('8', 'Голосование'),
        ('9', 'Загрузка файлов'),
        ('10', 'Прочее'),
    )

    user = models.ForeignKey('auth.User')
    title = models.CharField("Заголовок задания", max_length=50)
    cat = models.CharField("Категория", max_length=30, choices=CAT, default="Выбор")
    opisan = models.TextField("Описание оплачиваемого задания", max_length=2000)
    opis_vipoln = models.TextField(
        "Что должен указать исполнитель для проверки выполнения задания", 						max_length=2000)
    pub_date = models.DateTimeField("Дата", default=timezone.now)
    url_admin = models.URLField("URL сайта (включая http://)")
    #url = models.URLField("URL сайта (включая http://)Не обязательно", blank = True)
    price = models.FloatField("Вознаграждение исполнителю", default=0.1)
    price_task = models.FloatField("Укажите сумму баланса задания", default=0)
    tech = models.CharField("Технология выполнения задания",
                            max_length=30, choices=TECH, default="Выбор")
    srock = models.CharField("Максимальный срок, отведённый на выполнение задания",
                             max_length=10, choices=SROCK, default="Выбор")
    interval = models.CharField("Минимальный интервал очереди последовательной раздачи заданий",
                                max_length=10, choices=INTERVAL, default="Выбор")
    '''audit = models.CharField("Аудитория исполнителей",
							max_length=10, choices=AIDIT, default="Выбор")
	porefer = models.CharField("По наличию реферерала",
							max_length=10, choices=PO_REFER, default="Выбор")'''
    porating = models.CharField("По рейтингу серфера",
                                max_length=10, choices=PO_REFER, default="Выбор")
    '''porep = models.CharField("По репутации исполнителя заданий",
							max_length=10, choices=PO_REP, default="Выбор")
	pomet = models.CharField("По репутации исполнителя заданий",
							max_length=10, choices=PO_MET, default="Выбор")
	pofamaly = models.CharField("По семейному положению",
							max_length=10, choices=PO_FAMALY, default="Выбор")'''
    posex = models.CharField("По половому признаку",
                             max_length=10, choices=PO_SEX, default="Выбор")
    '''poage = models.CharField("По возрасту",
							max_length=10, choices=PO_AGE, default="Выбор")'''
    com = models.CharField("Коментарий модерации", max_length=300, default="", blank=True)
    moder = models.BooleanField("Модерация", default=False)
    odobren = models.BooleanField("Одобрить", default=False)
    pausa = models.BooleanField("Пауза", default=False)
    pravila = models.BooleanField("Я согласен(на) с правилами размещения рекламы на WMR_LOVE",
                                  default=True, blank=False)

    def __str__(self):
        return self.title

    '''def limit_pub_date_choices():
    return {'pub_date__lte': datetime.date.utcnow()}'''


class TasksUsers(models.Model):
    class Meta():
        db_table = 'task_users'
        verbose_name = "Ответ на задания"
        verbose_name_plural = "Ответы на задания"

    taskuser = models.ForeignKey(Tasksa, verbose_name="Задание")
    otvet_user = models.ForeignKey(User, verbose_name="Пользователь")
    us_opis_vipoln = models.TextField("Ответ задания", max_length=1000)
    odobren = models.BooleanField("Одобрить", default=False)
    start_task = models.DateTimeField("Время на выполнение")
    proverka = models.BooleanField("Проверка", default=False)
    otvet_task = models.IntegerField("Выполение задания", default=0)

    def __str__(self):
        return self.taskuser.title

