# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Tasksa, TasksUsers

class TasksaForm(forms.ModelForm):
    class Meta:
        model = Tasksa
        fields = ('title', 'cat', 'opisan', 'opis_vipoln', 'url_admin', 'price',
				 'tech', 'srock', 'interval', 'porating', 'posex', 'pravila')
				
class TasksUsersForm(forms.ModelForm):
	class Meta:
		model = TasksUsers
		fields = ('us_opis_vipoln',)
		
class OtvetTasksUsersForm(forms.ModelForm):
	class Meta:
		model = TasksUsers
		fields = ('odobren',)
		
class PopolnitForm(forms.ModelForm):
	class Meta:
		model = Tasksa
		fields = ('price_task',)
	#sum = forms.FloatField()
	
#Форма поиска задания
class TasksSearchForm(forms.Form):
	SELECT = (
    ('0', 'ID задания'),
    ('1', 'Название задания'),
    ('2', 'Логин рекламодателя'),
	('3', 'Домен'),
	)
	sel = forms.ChoiceField(label = "Поиск заданий", choices=SELECT, error_messages={'required': ''})
	char = forms.CharField(label = "", error_messages={'required': ''})

#Форма поиска задания по цене
class SearchCenForm(forms.Form):
	cen = forms.CharField(label = "", error_messages={'required': ''})
	
#Форма коментария доработки задания
class TaskMailForm(forms.Form):
	comm = forms.CharField(label = "Комментарий", error_messages={'required': ''})
	