# -*- coding: utf-8 -*-
from django import forms
from .models import MyMail

#Форма лс
class MyMailForm(forms.ModelForm):
    class Meta:
        model = MyMail
        fields = ('title', 'text', 'recipient')

#Форма лс доработки задания
class TaskMailForm(forms.ModelForm):
    class Meta:
        model = MyMail
        fields = ('text',)