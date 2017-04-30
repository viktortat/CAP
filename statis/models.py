from django.db import models

class Statistica(models.Model):
	class Meta():
		db_table = 'statistica'
		verbose_name = "Статистика"
		verbose_name_plural = "Статистика"
		
	click = models.IntegerField("Клики", default = 0)
	task = models.IntegerField("Задания", default = 0)
	viplat = models.IntegerField("Выплаты", default = 0)
	activ_user = models.IntegerField("Активных пользователей", default = 0)
	
	def __int__(self):
		return self.click