# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.models import User
from .forms import UserInfoForm, PerevodForm, Popoln_webForm, Popoln_qiwiForm
from .models import UserInfo, UserPopoln
from django.dispatch import receiver
from django.http import HttpResponse
from balanssite.models import Balans
from blog.models import Comments
#import hashlib
import base64
import binascii
from hashlib import sha256
#import requests
import json
from django.views.decorators.csrf import csrf_exempt

# Пополнение QIWI
@login_required
def popoln_qiwi(request):
	if request.method == "POST":	
		sum = Popoln_qiwiForm(request.POST)
	else:
		form = Popoln_qiwiForm()
	return render(request, 'profuser/qiwi_popol.html', {'form': form})
		
#QIWI проверка плотежа
@csrf_exempt
def res_qiwi(request):
    if not request.method == 'POST':
        return HttpResponse('error')
        
# Проверка Яндекс деньги
@csrf_exempt
def res_yandex(request):
	if request.method == "POST":
		return HttpResponseBadRequest("NO")
	else:
		return HttpResponseBadRequest("No")
	
# Пополнение Яндекс
@login_required
def popoln_yandex(request):
    if request.method == "POST":	
        sum = Popoln_webForm(request.POST)
    else:
        form = Popoln_webForm()
    return render(request, 'profuser/yandex_popolnpred.html', {'form': form})	

# Пополнение Webmoney
@login_required
def popoln_webm(request):
    if request.method == "POST":	
        sum = Popoln_webForm(request.POST)
    else:
        form = Popoln_webForm()
    return render(request, 'profuser/webmoney_popol.html', {'form': form})		

#Проверка Webmoney
@csrf_exempt
def popoln_webmres(request):
    if not request.method == 'POST':
        return HttpResponse('no')
    return HttpResponseBadRequest("NO")

        
@csrf_exempt	
#Платеж принят webmoney	
def success(request):
    return render(request, 'profuser/webmoney_success.html')
    
@csrf_exempt		
#Платеж не принят webmoney		
def fail(request):
    return render(request, 'profuser/webmoney_fail.html')


# Пополнение Prfect money
@login_required
def popoln_pm(request):
    return render(request, 'profuser/pm.html')	
	
#Проверка Perfect money
@csrf_exempt
def popoln_pmres(request):
    if not request.POST or request.POST.get('LMI_PREREQUEST', None):
        return render(request, 'profuser/pm_popol.html')
        
#Ошибка оплаты Perfect money        
@csrf_exempt
def pmfail(request):
    return render(request, 'profuser/pmfail.html')
	

# Пополнение Payeer
@login_required
def popoln_payeer(request):
	if request.method == "POST":	
		sum = Popoln_webForm(request.POST)
	else:
		form = Popoln_webForm()
		return render(request, 'profuser/payeer_popol.html', {'form': form})

#Проверка и подтверждение оплаты Payeer        
@csrf_exempt
def deposit_result(request):
	if not request.method == 'POST':
		return HttpResponse("error")
    
#Платеж принят payeer
@csrf_exempt
def payeer_success(request):
    return render(request, 'profuser/payeer_success.html')	

#Платеж не принят payeer
@csrf_exempt		
def payeer_fail(request):
    return render(request, 'profuser/payeer_fail.html')	
	
    
#Перевод с личного счета на рекламный
@login_required
def perevod(request):
	if request.method == "POST":	
		sum = PerevodForm(request.POST)
	else:
		form = PerevodForm()
	return render(request, 'profuser/popol.html', {'form': form})			
