# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import UserInfo, Viplati

#Форма профиля
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('phone', 'nick', 'work', 'family', 'sex', 'birth', 
						'wmr', 'yandex', 'qiwi', 'payeer', 'perfect_money', 'website', 'picture')
		
#Форма заказа выплаты
class ViplatiForm(forms.ModelForm):
    class Meta:
        model = Viplati
        fields = ('sum',)
		
#Форма заказа выплаты WMR
class ViplatiWmrForm(forms.ModelForm):
    class Meta:
        model = Viplati
        fields = ('sum',)
		
#Форма заказа выплаты Yandex		
class ViplatiYandexForm(forms.ModelForm):
    class Meta:
        model = Viplati
        fields = ('sum',)
		
#Форма заказа выплаты QIWI		
class ViplatiQiwiForm(forms.ModelForm):
    class Meta:
        model = Viplati
        fields = ('sum',)

#Форма заказа выплаты Perfet money		
class ViplatiPerfectForm(forms.ModelForm):
    class Meta:
        model = Viplati
        fields = ('sum',)
		
#Форма заказа выплаты Payeer		
class ViplatiPayeerForm(forms.ModelForm):
    class Meta:
        model = Viplati
        fields = ('sum',)
		
#Форма перевода с основного баланса на рекламный
class PerevodForm(forms.Form):
    sum = forms.IntegerField(label = "Сумма")
	
#Форма пополнения Webmoney
class Popoln_webForm(forms.Form):
    sum = forms.FloatField(label = "Сумма")
    
#Форма пополнения QIWI
class Popoln_qiwiForm(forms.Form):
	tel = forms.IntegerField(label = "Телефон")
	sum = forms.FloatField(label = "Сумма")
	
#Форма стать рефералом
class IRefForm(forms.Form):
	referer = forms.CharField(label = "Стать рефералом")
	
#Форма поиска пользователя по id
class UserSearchForm(forms.Form):
	search = forms.IntegerField(label = "Поиск по id пользователя", help_text="")