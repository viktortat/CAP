from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

#Модель профиля пользователя
class UserInfo(models.Model):
	class Meta():
		db_table = 'user_info'
		verbose_name = "Профиль"
		verbose_name_plural = "Профили пользователей"
		
	WORK = (
		('NOS', 'Нет основного места работы'),
		('SCHOOL', 'Учусь в школе'),
		(u'STUDENT', 'Студент'),
		('PRED', 'Предприниматель'),
		('WORKSPRED', 'Работник на предприятии'),
		('SLUG', 'Служащий на предприятии'),
	)
	
	FAMALY = (
		('MARRIED', 'Женат\замужем, есть дети'),
		('MARRIEDS', 'Женат\замужем, нет детей'),
		('NOMARRIED', 'Не женат\Не замужем, есть дети'),
		('NOMARRIEDS', 'Не женат\Не замужем, нет детей'),
		('DIVORCED', 'Разведен\разведена, есть дети'),
		('DIVORCEDS', 'Разведен\разведена, нет детей'),
	)
	
	SEX = (
		('MEN', 'Мужчина'),
		('WOOMEN', 'Женщина'),
	)
	
	user = models.OneToOneField(User)
	phone = models.IntegerField("Телефон", default=0) #, validators=([MinValueValidator(0),
                                       #MaxValueValidator(999999999999)]))
	nick = models.CharField("Имя", max_length=20)
	work = models.CharField("Род деятельности", blank = True, max_length=30, choices=WORK, 
							default="Выбор")
	family = models.CharField("Семейное положение", blank = True, max_length=30, choices=FAMALY, 
							default="Выбор")
	sex = models.CharField("Пол", blank = True, max_length=30, choices=SEX, 
							default="Выбор")
	birth = models.DateField("Дата рождения", default='1970-01-01')
	wmr = models.CharField("Номер счёта WMR (Вместе с латинской R)", default = 0, blank = True, 					max_length=20)
	yandex = models.CharField("Yandex кошелек", default = 0, blank = True, max_length=20)
	qiwi = models.CharField("QIWI кошелек", default = 0, blank = True, max_length=20)
	payeer = models.CharField("Payeer (Вместе с латинской P)", default = 0, blank = True, max_length=20)
	perfect_money = models.CharField("Perfect Money (Вместе с латинской U)", default = 0, 
											blank = True, max_length=20)
	schet_lich = models.FloatField(default = 0, blank = True )
	schet_reklam = models.FloatField(default = 0, blank = True )
	refery = models.IntegerField("Рефери", default = 0, blank = True)
	rating = models.FloatField("Рейтинг", default = 0, blank = True)
	status = models.CharField("Статус", default="Новичок", max_length=20)
	website = models.URLField("Мой сайт", blank=True)
	picture = models.ImageField("Фотография", upload_to='profile_images', blank=True)
	
	def __str__(self):
		return self.user.username
	
#Модель рефералов	
class Refery(models.Model):
	class Meta():
		db_table = 'referal'
		verbose_name = "Реферал"
		verbose_name_plural = "Рефералы"
		
	user = models.OneToOneField(User)
	one_lvl = models.IntegerField("Первый уровень", default=0)
	two_lvl = models.IntegerField("Второй уровень", default=0)
	three_lvl = models.IntegerField("Третий уровень", default=0)
	
	def __str__(self):
		return self.user.username
	
#Модель выплат	
class Viplati(models.Model):
	class Meta():
		db_table = 'viplati_user'
		verbose_name = "Выплата"
		verbose_name_plural = "Заказы выплат"
		
	user = models.ForeignKey(User)
	sum = models.IntegerField("Сумма", default = 0)
	sys_viplat = models.CharField("Система для выплаты", max_length=20)
	ub_date = models.DateTimeField("Дата", default=timezone.now)
	odobren = models.BooleanField("Одобрин", default=False)
	
	def __str__(self):
		return self.user.username
		
#Модель пополнения	
class UserPopoln(models.Model):
	class Meta():
		db_table = 'popoln_user'
		verbose_name = "Пополнение"
		verbose_name_plural = "Пополнения"
		
	user = models.ForeignKey(User)
	sum = models.FloatField("Сумма", default = 0)
	sys = models.CharField("Кошелек", max_length=20)
	date = models.DateTimeField("Дата", default=timezone.now)
	odobren = models.BooleanField("Успех пополнения", default=False)
	
	def __str__(self):
		return self.user.username
		
#Статистика пользователя
class UserStatic(models.Model):
	class Meta():
		db_table = 'user_static'
		verbose_name = "Ститистика пользователя"
		verbose_name_plural = "Ститистика пользователей"
	#Текущая дата
	today = datetime.today()
	
	user = models.ForeignKey(User)
	pub_date = models.DateTimeField("Дата последнего входа", default=today.date())
	serf = models.IntegerField("Серфинг", default = 0, blank=True)
	task = models.IntegerField("Задания", default = 0, blank=True)
	test = models.IntegerField("Тесты", default = 0, blank=True)
	pismo = models.IntegerField("Письма", default = 0, blank=True)
	viplat = models.FloatField("Всего выплат", default = 0, blank=True)
	ref_one = models.FloatField("Заработано с рефералов 1 ур.", default = 0, blank=True)
	ref_two = models.FloatField("Заработано с рефералов 2 ур.", default = 0, blank=True)