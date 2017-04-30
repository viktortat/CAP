# -*- coding: utf-8 -*-
from django.db import models

class Balans (models.Model):
	class Meta:
		db_table = 'balans'
		verbose_name = "Баланс сайта"
		verbose_name_plural = "Баланс сайта"
		
	schet_site = models.FloatField("Баланс сайта", default=0)
	reklama = models.FloatField("Зачислено на рекламу", default=0)
	vivod = models.FloatField("Сумма к выводу", default=0)
	vseviplati = models.FloatField("Сумма всех выплат", default=0)