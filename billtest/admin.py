from django.contrib import admin
from .models import BillTest

#Фильтры
class BillTestAdmin(admin.ModelAdmin):
	list_filter = ('pub_date',)
	list_display = ('title', 'user', 'pub_date', 'odobren', 'moder')

admin.site.register(BillTest, BillTestAdmin)
