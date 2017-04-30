# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Serf, SerfUsers, Plinks, Contlinks, Pismo, PismoUsers, Perehod, PerehodUsers
from captcha.fields import CaptchaField

#Форма добовления ссылки
class SerfForm(forms.ModelForm):
    class Meta:
        model = Serf
        fields = ('title', 'opisan', 'url', 'price', 'time_r',
				'perehod', 'porating', 'posex', 'pravila')
				
#Форма пополнения ссылки				
class PopolnitSerfForm(forms.ModelForm):
	class Meta:
		model = Serf
		fields = ('price_serf',)

#Форма ответа в серфинге		
class CaptchaForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = SerfUsers
        fields = ('captcha',)

#Форма добовления псевдо ссылки
class PlinksForm(forms.ModelForm):
    class Meta:
        model = Plinks
        fields = ('url', 'title', 'opis', 'pravila')

#Форма пополнения псевдо ссылки				
class PopolnitPlinksForm(forms.ModelForm):
	class Meta:
		model = Plinks
		fields = ('days',)
		
#Форма добовления контекстной ссылки
class ContlinksForm(forms.ModelForm):
    class Meta:
        model = Contlinks
        fields = ('url', 'title', 'opis', 'click', 'pravila')
		
#Форма пополнения контекстной ссылки				
class PopolnitContlinksForm(forms.ModelForm):
	class Meta:
		model = Contlinks
		fields = ('click',)

#Форма добовления письма
class PismoForm(forms.ModelForm):
    class Meta:
        model = Pismo
        fields = ('title', 'opis', 'quest_1', 'quest_1_ans_1', 'quest_1_ans_2', 'quest_1_ans_3', 'var_one', 
					'url', 'tech', 'time', 'vid', 'perehod', 'porating', 'posex', 'pravila')
					
#Форма пополнения письма			
class PopolnitPismoForm(forms.ModelForm):
	class Meta:
		model = Pismo
		fields = ('price_pismo',)
		
#Форма ответа в письма		
class CaptchaPismoForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = PismoUsers
        fields = ('captcha',)
		
#Форма добовления ссылки
class PerehodForm(forms.ModelForm):
    class Meta:
        model = Perehod
        fields = ('title', 'opisan', 'url', 'price', 'time_r',
				'perehod', 'porating', 'posex', 'pravila')
				
#Форма пополнения ссылки				
class PopolnitPerehodForm(forms.ModelForm):
	class Meta:
		model = Perehod
		fields = ('price_serf',)
		