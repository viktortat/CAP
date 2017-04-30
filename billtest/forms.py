# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import BillTest

#Форма добавления теста	
class BillTestForm(forms.ModelForm):
    class Meta:
        model = BillTest
        fields = ('title', 'opisan', 'time_t', 'vid_t', 'url_admin',
				'quest_1', 'quest_1_ans_1', 'quest_1_ans_2', 'quest_1_ans_3',
				'quest_2', 'quest_2_ans_1', 'quest_2_ans_2', 'quest_2_ans_3',
				'quest_3', 'quest_3_ans_1', 'quest_3_ans_2', 'quest_3_ans_3',
				'var_one', 'var_two', 'var_three', 'pravila')
				
#Форма пополнения теста				
class PopolnitTestForm(forms.ModelForm):
	class Meta:
		model = BillTest
		fields = ('price_test',)
		
#Форма ответа на тестаclass UserInfoForm(forms.ModelForm):
class OtvetTestForm(forms.ModelForm):
    class Meta:
        model = BillTest
        fields = ('var_one', 'var_two', 'var_three')