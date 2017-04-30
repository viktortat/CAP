# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from profuser.models import UserInfo

#Модель личного сообщения
class MyMail(models.Model):
	class Meta():
		db_table = 'my_mail'
		verbose_name = "Личное сообщение"
		verbose_name_plural = "Личные сообщения"
			
	title = models.CharField("Тема", max_length=40)
	text = models.TextField("Текст", max_length=500)
	sender = models.ForeignKey(UserInfo,  verbose_name = "От кого")
	recipient = models.CharField("Кому", max_length=50)
	read = models.BooleanField("Прочитан", default=False)
	pub_date = models.DateTimeField("Дата", default=timezone.now)
	delete_one = models.BooleanField("Удален отправителем", default=False)
	delete_two = models.BooleanField("Удален получателем", default=False)