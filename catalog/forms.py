# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import CatalogSite

#Форма добавления ссылки облака сайтов
class CatalogSiteForm(forms.ModelForm):
	class Meta:
		model = CatalogSite
		fields = ('title', 'website', 'dop', 'pravila')
		
#Форма пополнения ссылки облака сайтов			
class PopolnitCatalogForm(forms.ModelForm):
	class Meta:
		model = CatalogSite
		fields = ('price',)