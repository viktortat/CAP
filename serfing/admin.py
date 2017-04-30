from django.contrib import admin
from serfing.models import Serf, Plinks, Contlinks, Pismo, Perehod

#Фильтры
class SerfAdmin(admin.ModelAdmin):
	list_filter = ('pub_date',)
	list_display = ('title', 'user', 'pub_date', 'odobren', 'moder')

class PismoAdmin(admin.ModelAdmin):
	list_filter = ('pub_date',)
	list_display = ('title', 'user', 'pub_date', 'odobren', 'moder')
	
class PlinksAdmin(admin.ModelAdmin):
	list_filter = ('pub_date',)
	list_display = ('title', 'user', 'pub_date', 'odobren')
	
class ContlinksAdmin(admin.ModelAdmin):
	list_filter = ('pub_date',)
	list_display = ('title', 'user', 'pub_date', 'odobren')
	
class PerehodAdmin(admin.ModelAdmin):
	list_filter = ('pub_date',)
	list_display = ('title', 'user', 'pub_date', 'odobren', 'moder')
	
admin.site.register(Serf, SerfAdmin)
admin.site.register(Pismo, PismoAdmin)
admin.site.register(Plinks, PlinksAdmin)
admin.site.register(Contlinks, ContlinksAdmin)
admin.site.register(Perehod, PerehodAdmin)

