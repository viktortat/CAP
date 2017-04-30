# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

#модель ссылки серфинга
class Serf(models.Model):
	class Meta():
		db_table = 'serf'
		verbose_name = "Серфинг сайта"
		verbose_name_plural = "Серфинг сайтов"
		
	TIME_R = (
		('5', '5 секунд (-45%)'),
		('10', '10 секунд  (-30%)'),
		('15', '15 секунд  (-15%)'),
		('20', '20 секунд'),
		('25', '25 секунд (+15%)'),
		('30', '30 секунд (+30%)'),
		('35', '35 секунд (+45%)'),
		('40', '40 секунд (+60%)'),
		('45', '45 секунд (+75%)'),
		('50', '50 секунд (+90%)'),
		('55', '55 секунд (+105%)'),
		('60', '60 секунд (+120%)'),
	)
	PRICE = (
		('0.026', '0.026'),
		('0.029', '0.029'),
		('0.032', '0.032'),
		('0.035', '0.035'),
		('0.038', '0.038'),
		('0.041', '0.041'),
		('0.044', '0.044'),
		('0.047', '0.047'),
		('0.05', '0.05'),
		('0.053', '0.053'),
		('0.056', '0.056'),
		('0.059', '0.059'),
		('0.062', '0.062'),
		('0.065', '0.065'),
		('0.068', '0.068'),
		('0.071', '0.071'),
		('0.074', '0.074'),
		('0.077', '0.077'),
		('0.08', '0.08'),
		('0.083', '0.083'),
		('0.086', '0.086'),
		('0.089', '0.089'),
		('0.092', '0.092'),
		('0.095', '0.095'),
		('0.098', '0.098'),
		('0.101', '0.101'),
		('0.104', '0.104'),
		('0.107', '0.107'),
		('0.11', '0.11'),
	)
	
	SILKA_VID = (
		('NO', 'Нет'),
		('YES', 'Да (+ 0,01 руб.)'),
	)

	PEREHOD = (
		('NO', 'Нет'),
		('YES', 'Да (+ 0,02 руб.)'),	
	)
	
	AIDIT = (
		('VSE', 'Все пользователи'),
		('ONE_TWO', '1/2 польователей'),
		('ONE_THREE', '1/3 польователей'),
		('ONE_FOUR', '1/4 польователей'),
		('MEDL', 'Очень медленный серфинг'),
		('SUPM', 'Супер медленный серфинг'),
		('CHEREP', 'Черепаший серфинг'),
	)
	
	PO_REFER = (
		('VSEP', 'Все пользователи'),
		('BEZREFER', 'Только пользователи без реферала'),
		('MOIREFER', 'Только мой рефералы'),
	)
	
	PO_RATING = (
		('VSEPOL', 'Все пользователи'),
		('FIVE_R', 'От 5 баллов и выше (+ 0,02 руб.)'),
		('TEN_R', 'От 10 баллов и выше (+ 0,02 руб.)'),
		('TWENTY_R', 'От 20 баллов и выше (+ 0,02 руб.)'),
		('FIVETY_R', 'От 50 баллов и выше (+ 0,02 руб.)'),
		('ONEH_R', 'От 100 баллов и выше (+ 0,02 руб.)'),
		('THREEH_R', 'От 300 баллов и выше (+ 0,02 руб.)'),
		('FIVEH_R', 'От 500 баллов и выше (+ 0,02 руб.)'),
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
		('VSEPOLZ', 'Все пользователи'),
		('MEN_SEX', 'Мужчина (+ 0,01 руб.)'),
		('WOOMEN_SEX', 'Женщина (+ 0,01 руб.)'),
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
	
	user = models.ForeignKey('auth.User')	
	title = models.CharField("Загаловок ссылки", max_length=40)
	opisan = models.CharField("Краткое описание ссылки",max_length=60)
	url = models.URLField("URL сайта (включая http://)",blank = True)
	pub_date = models.DateTimeField("Дата", default=timezone.now)
	price = models.CharField("Цена за клик:", 
							max_length=30, choices=PRICE, default="Выбор")
	price_serf = models.FloatField("Укажите сумму баланса ссылки", default=0)
	#price_serf_ps = models.FloatField("Псевдо сумма баланса ссылки", default=0)
	time_r = models.CharField("Время просмотра ссылки", 
							max_length=30, choices=TIME_R, default="Выбор")
	price_u = models.FloatField("Вознограждение пользователю", default=0)
	price_s = models.FloatField("Вознограждение сайту", default=0)
	price_t = models.FloatField("Списание с баланса", default=0)
	'''silka_vid = models.CharField("Выделить ссылку", 
							max_length=10, choices=SILKA_VID, default="Выбор")'''
	perehod = models.CharField("Последующий переход на сайт",
							max_length=10, choices=PEREHOD, default="Выбор")
	'''audit = models.CharField("Аудитория смотрящих",
							max_length=10, choices=AIDIT, default="Выбор")'''
	'''porefer = models.CharField("По наличию реферера",
							max_length=10, choices=PO_REFER, default="Выбор")'''
	porating = models.CharField("По рейтингу серфера",
							max_length=10, choices=PO_RATING, default="Выбор")
	'''porep = models.CharField("По репутации исполнителя заданий",
							max_length=10, choices=PO_REP, default="Выбор")'''
	'''pomet = models.CharField("По репутации исполнителя заданий",
							max_length=10, choices=PO_MET, default="Выбор")'''
	'''pofamaly = models.CharField("По семейному положению",
							max_length=10, choices=PO_FAMALY, default="Выбор")'''
	posex = models.CharField("По половому признаку",
							max_length=10, choices=PO_SEX, default="Выбор")
	'''poage = models.CharField("По возрасту",
							max_length=10, choices=PO_AGE, default="Выбор")'''
	pravila = models.BooleanField("Я согласен(на) с правилами размещения рекламы на WMR_LOVE", default=True)
	prosm = models.IntegerField("Количество просмотров", default=0 )
	prosm_ost = models.IntegerField("Количество просмотров осталось", default=0 )
	spis = models.BooleanField("Списание с 11р.", default=False)
	sum_spis = models.IntegerField("Сумма для списания", default=0 )
	com = models.CharField("Коментарий модерации", max_length=300, default="", blank=True)
	moder = models.BooleanField("Модерация", default=False)
	odobren = models.BooleanField("Одобраить", default=False)
	pausa = models.BooleanField("Пауза", default=False)
	
	def __str__(self):
		return self.title

#Ответов на вопрос при серфинге		
class SerfUsers(models.Model):
	class Meta():
		db_table = 'serf_users'
		
	serf_user = models.ForeignKey(Serf)
	user = models.ForeignKey(User)
	#otvet = models.CharField("Ответ", max_length=5)
	odobren = models.BooleanField("Одобрить", default=False)
	pub_date = models.DateTimeField("Дата выполнения", default=0)
	
	def __str__(self):
		return self.serf_user.title
		
#Псевдо ссылки	
class Plinks(models.Model):
	class Meta():
		db_table = 'pseudo_links'
		verbose_name = "Псевдо ссылка"
		verbose_name_plural = "Псевдо ссылки"
		
	user = models.ForeignKey(User)
	url = models.URLField("URL сайта (включая http://)")
	title = models.CharField("Загаловок ссылки", max_length=50)
	opis = models.CharField("Описание ссылки", max_length=50)
	days = models.IntegerField("Количество дней", default=1)
	price_link = models.IntegerField("Укажите сумму баланса ссылки", default=0)
	pub_date = models.DateTimeField("Дата", default=timezone.now)
	pravila = models.BooleanField("Я согласен(на) с правилами размещения рекламы на WMR_LOVE", default=True)
	com = models.CharField("Коментарий модерации", max_length=300, default="", blank=True)
	moder = models.BooleanField("Модерация", default=False)
	odobren = models.BooleanField("Одобраить", default=False)
	pausa = models.BooleanField("Пауза", default=False)
	
	def __str__(self):
		return self.title
		
#Контекстная реклама
class Contlinks(models.Model):
	class Meta():
		db_table = 'context_links'
		verbose_name = "Контекстная реклама"
		verbose_name_plural = "Контекстная реклама"
		
	user = models.ForeignKey(User)
	url = models.URLField("URL сайта (включая http://)")
	title = models.CharField("Загаловок ссылки", max_length=28)
	opis = models.CharField("Описание ссылки", max_length=50)
	click = models.IntegerField("Количество кликов", default=100)
	price_link = models.IntegerField("Укажите сумму баланса ссылки", default=0)
	pub_date = models.DateTimeField("Дата", default=timezone.now)
	pravila = models.BooleanField("Я согласен(на) с правилами размещения рекламы на WMR_LOVE", default=True)
	com = models.CharField("Коментарий модерации", max_length=300, default="", blank=True)
	moder = models.BooleanField("Модерация", default=False)
	odobren = models.BooleanField("Одобраить", default=False)
	pausa = models.BooleanField("Пауза", default=False)
	
	def __str__(self):
		return self.title
		
#Серфинг "Письма"
class Pismo(models.Model):
	class Meta():
		db_table = 'pisma'
		verbose_name = "Чтение писем"
		verbose_name_plural = "Чтение писем"
		
	TECH = (
		('24_h', 'Доставляется всеи каждые 24 часа'),
		('1_m', 'Доставляется всеи 1 раз в месяц (+ 0,02 руб.)'),
	)
	
	TIME = (
		('20', '20 секунд'),
		('30', '30 секунд ( + 0.004 руб.)'),
		('40', '40 секунд ( + 0.008 руб.)'),
		('50', '50 секунд ( + 0.012 руб.)'),
		('60', '60 секунд ( + 0.016 руб.)'),
	)
	
	VID = (
		('NO', 'Нет'),
		('YES', 'Да (+ 0,01 руб.)'),	
	)
	
	PEREHOD = (
		('NO', 'Нет'),
		('YES', 'Да (+ 0,015 руб.)'),	
	)
	
	PO_RATING = (
		('VSEPOL', 'Все пользователи'),
		('FIVE_R', 'От 5 баллов и выше (+ 0,02 руб.)'),
		('TEN_R', 'От 10 баллов и выше (+ 0,02 руб.)'),
		('TWENTY_R', 'От 20 баллов и выше (+ 0,02 руб.)'),
		('FIVETY_R', 'От 50 баллов и выше (+ 0,02 руб.)'),
		('ONEH_R', 'От 100 баллов и выше (+ 0,02 руб.)'),
		('THREEH_R', 'От 300 баллов и выше (+ 0,02 руб.)'),
		('FIVEH_R', 'От 500 баллов и выше (+ 0,02 руб.)'),
	)
	
	PO_SEX = (
		('VSEPOLZ', 'Все пользователи'),
		('MEN_SEX', 'Мужчина (+ 0,01 руб.)'),
		('WOOMEN_SEX', 'Женщина (+ 0,01 руб.)'),
	)
	
	user = models.ForeignKey(User)
	title = models.CharField("Заголовок письма", max_length=55)
	opis = models.TextField("Содержание письма", max_length=3000)
	pub_date = models.DateTimeField("Дата", default=timezone.now)
	quest_1 = models.CharField("Контрольный вопрос к письму", max_length=300)
	quest_1_ans_1 = models.CharField("Вариант ответа №1", max_length=30)
	quest_1_ans_2 = models.CharField("Вариант ответа №2", max_length=30)
	quest_1_ans_3 = models.CharField("Вариант ответа №3", max_length=30)
	var_one = models.IntegerField("Укажите номер правильного ответа на вопрос", default=1)
	url = models.URLField("URL сайта (включая http://)")
	tech = models.CharField("Технология доставки письма:", max_length=30, choices=TECH, default="Выбор")
	time = models.CharField("Время просмотра ссылки", max_length=30, choices=TIME, default="Выбор")
	vid = models.CharField("Выделить письмо", max_length=10, choices=VID, default="Выбор")
	perehod = models.CharField("Последующий переход на сайт", max_length=10, choices=PEREHOD, default="Выбор")
	porating = models.CharField("По рейтингу серфера", max_length=10, choices=PO_RATING, default="Выбор")
	posex = models.CharField("По половому признаку", max_length=10, choices=PO_SEX, default="Выбор")
	price = models.FloatField("Цена просмотра:", max_length=30, default=0.09)
	price_pismo = models.FloatField("Сумму баланса письма", default=0)
	price_u = models.FloatField("Вознограждение пользователю", default=0)
	price_s = models.FloatField("Вознограждение сайту", default=0)
	price_t = models.FloatField("Списание с баланса", default=0)
	pravila = models.BooleanField("Я согласен(на) с правилами размещения рекламы на WMR_LOVE", default=True)
	prosm = models.IntegerField("Количество просмотров", default=0 )
	prosm_ost = models.IntegerField("Количество просмотров осталось", default=0 )
	spis = models.BooleanField("Списание с 11р.", default=False)
	sum_spis = models.IntegerField("Сумма для списания", default=0 )
	com = models.CharField("Коментарий модерации", max_length=300, default="", blank=True)
	moder = models.BooleanField("Модерация", default=False)
	odobren = models.BooleanField("Одобраить", default=False)
	pausa = models.BooleanField("Пауза", default=False)
	
	def __str__(self):
		return self.title
		
#Выполнение писем пользователеми		
class PismoUsers(models.Model):
	class Meta():
		db_table = 'pismo_users'
		
	pismo_user = models.ForeignKey(Pismo)
	user = models.ForeignKey(User)
	otvet = models.CharField("Ответ", max_length=5)
	odobren = models.BooleanField("Одобрить", default=False)
	pub_date = models.DateTimeField("Дата выполнения", default=0)
	
	def __str__(self):
		return self.pismo_user.title
		
#модель ссылки серфинга
class Perehod(models.Model):
	class Meta():
		db_table = 'perehod'
		verbose_name = "Переход на сайт"
		verbose_name_plural = "Переходы на сайты"
		
	TIME_R = (
		('5', '5 секунд (-45%)'),
		('10', '10 секунд  (-30%)'),
		('15', '15 секунд  (-15%)'),
		('20', '20 секунд'),
		('25', '25 секунд (+15%)'),
		('30', '30 секунд (+30%)'),
		('35', '35 секунд (+45%)'),
		('40', '40 секунд (+60%)'),
		('45', '45 секунд (+75%)'),
		('50', '50 секунд (+90%)'),
		('55', '55 секунд (+105%)'),
		('60', '60 секунд (+120%)'),
	)
	PRICE = (
		('0.026', '0.026'),
		('0.029', '0.029'),
		('0.032', '0.032'),
		('0.035', '0.035'),
		('0.038', '0.038'),
		('0.041', '0.041'),
		('0.044', '0.044'),
		('0.047', '0.047'),
		('0.05', '0.05'),
		('0.053', '0.053'),
		('0.056', '0.056'),
		('0.059', '0.059'),
		('0.062', '0.062'),
		('0.065', '0.065'),
		('0.068', '0.068'),
		('0.071', '0.071'),
		('0.074', '0.074'),
		('0.077', '0.077'),
		('0.08', '0.08'),
		('0.083', '0.083'),
		('0.086', '0.086'),
		('0.089', '0.089'),
		('0.092', '0.092'),
		('0.095', '0.095'),
		('0.098', '0.098'),
		('0.101', '0.101'),
		('0.104', '0.104'),
		('0.107', '0.107'),
		('0.11', '0.11'),
	)
	
	PEREHOD = (
		('NO', 'Нет'),
		('YES', 'Да (+ 0,02 руб.)'),	
	)
	
	PO_RATING = (
		('VSEPOL', 'Все пользователи'),
		('FIVE_R', 'От 5 баллов и выше (+ 0,02 руб.)'),
		('TEN_R', 'От 10 баллов и выше (+ 0,02 руб.)'),
		('TWENTY_R', 'От 20 баллов и выше (+ 0,02 руб.)'),
		('FIVETY_R', 'От 50 баллов и выше (+ 0,02 руб.)'),
		('ONEH_R', 'От 100 баллов и выше (+ 0,02 руб.)'),
		('THREEH_R', 'От 300 баллов и выше (+ 0,02 руб.)'),
		('FIVEH_R', 'От 500 баллов и выше (+ 0,02 руб.)'),
	)
	
	PO_SEX = (
		('VSEPOLZ', 'Все пользователи'),
		('MEN_SEX', 'Мужчина (+ 0,01 руб.)'),
		('WOOMEN_SEX', 'Женщина (+ 0,01 руб.)'),
	)
	
	user = models.ForeignKey('auth.User')	
	title = models.CharField("Загаловок ссылки", max_length=40)
	opisan = models.CharField("Краткое описание ссылки",max_length=60)
	url = models.URLField("URL сайта (включая http://)",blank = True)
	pub_date = models.DateTimeField("Дата", default=timezone.now)
	price = models.CharField("Цена за клик:", 
							max_length=30, choices=PRICE, default="Выбор")
	price_serf = models.FloatField("Укажите сумму баланса ссылки", default=0)
	time_r = models.CharField("Время просмотра ссылки", 
							max_length=30, choices=TIME_R, default="Выбор")
	price_u = models.FloatField("Вознограждение пользователю", default=0)
	price_s = models.FloatField("Вознограждение сайту", default=0)
	price_t = models.FloatField("Списание с баланса", default=0)
	perehod = models.CharField("Последующий переход на сайт",
							max_length=10, choices=PEREHOD, default="Выбор")
	porating = models.CharField("По рейтингу серфера",
							max_length=10, choices=PO_RATING, default="Выбор")
	posex = models.CharField("По половому признаку",
							max_length=10, choices=PO_SEX, default="Выбор")
	pravila = models.BooleanField("Я согласен(на) с правилами размещения рекламы на WMR_LOVE", default=True)
	prosm = models.IntegerField("Количество просмотров", default=0 )
	prosm_ost = models.IntegerField("Количество просмотров осталось", default=0 )
	spis = models.BooleanField("Списание с 11р.", default=False)
	sum_spis = models.IntegerField("Сумма для списания", default=0 )
	com = models.CharField("Коментарий модерации", max_length=300, default="", blank=True)
	moder = models.BooleanField("Модерация", default=False)
	odobren = models.BooleanField("Одобраить", default=False)
	pausa = models.BooleanField("Пауза", default=False)
	
	def __str__(self):
		return self.title

#Ответов на вопрос при серфинге		
class PerehodUsers(models.Model):
	class Meta():
		db_table = 'perehod_users'
		
	perehod_user = models.ForeignKey(Perehod)
	user = models.ForeignKey(User)
	#otvet = models.CharField("Ответ", max_length=5)
	odobren = models.BooleanField("Одобрить", default=False)
	pub_date = models.DateTimeField("Дата выполнения", default=0)
	
	def __str__(self):
		return self.perehod_user.title
	