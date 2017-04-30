from django.contrib import admin
from balanssite.models import Balans

class BalansAdmin(admin.ModelAdmin):
	list_display = ('schet_site', 'reklama', 'vivod', 'vseviplati')
	
admin.site.register(Balans, BalansAdmin)

