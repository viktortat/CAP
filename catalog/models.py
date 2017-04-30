# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#Модель облака сайтов
class CatalogSite(models.Model):
	class Meta():
		verbose_name = "Каталог"
		verbose_name_plural = "Каталог сайтов"
		
	DOP = (
		('NO', 'Нет'),
		('YES', 'Да (+5.00 руб.)'),
	)
	
   # Эта строка обязательна. Она связывает UserProfile с экземпляром модели User.
	user = models.ForeignKey('auth.User')
	title = models.CharField("Заголовок ссылки", max_length=25)
	website = models.URLField("URL сайта (включая http://)")	
	dop = models.CharField("Выделить ссылку", 
							max_length=30, choices=DOP, default="Выбор")
	price = models.FloatField("Сумма", default=0)
	pub_date = models.DateTimeField("Дата", default=timezone.now)
	odobren = models.BooleanField("Одобраить", default=False)
	pravila = models.BooleanField("Я согласен(на) с правилами размещения рекламы на WMR_LOVE", default=False)
	
	def __str__(self):
		return self.title