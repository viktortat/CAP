from django.contrib import admin
from statis.models import Statistica

#Фильтры
class StatisticaAdmin(admin.ModelAdmin):
	list_display = ('click', 'task', 'viplat')
	
admin.site.register(Statistica, StatisticaAdmin)
