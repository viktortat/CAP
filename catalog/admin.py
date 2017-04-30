# -*- coding: utf-8 -*-
from django.contrib import admin
from catalog.models import CatalogSite

#Фильтры
class CatalogSiteAdmin(admin.ModelAdmin):
	list_filter = ('pub_date',)
	list_display = ('title', 'user', 'pub_date', 'odobren')
	
admin.site.register(CatalogSite, CatalogSiteAdmin)