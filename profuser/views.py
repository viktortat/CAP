# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.models import User
from .forms import UserInfoForm, ViplatiForm, ViplatiWmrForm, ViplatiYandexForm, ViplatiQiwiForm, ViplatiPerfectForm, ViplatiPayeerForm, PerevodForm, Popoln_webForm, IRefForm, UserSearchForm
from .models import UserInfo, Refery, Viplati, UserPopoln, UserStatic
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from balanssite.models import Balans
#import hashlib
import base64
import binascii
from hashlib import sha256
#import requests
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

#Сигнал регистрации создание профиля и рефералов
@receiver(post_save, sender = User)
def addinfo(instance, **kwargs):
	today = datetime.today()
	try:
		#Заходил чегодня пользователь или нет
		stat = UserStatic.objects.get(user = instance, pub_date__gte = today.date())	
	except:	
		#Добовляю запись о входе
		stat = UserStatic()
		stat.user = instance
		stat.pub_date = today.date()
		stat.save()
	#Существует пользователь или нет	
	try:
		p = UserInfo.objects.get(user = instance)
		return redirect('activ')
	except:
		post = instance.id
		form = UserInfoForm()
		post = form.save(commit=False)
		us = instance.id
		post.id = us
		post.user = instance
		post.nick = instance.username
		post.save()
		#Создание в таб. рефералов
		refery = Refery()
		refery.id = instance.id
		refery.one_lvl = 0
		refery.two_lvl = 0
		refery.user = instance
		refery.save()

	
#Редактирование профиля
@login_required
def editinfo(request, pk):
	post = get_object_or_404(UserInfo, pk=pk)
	user = request.user.id
	user = str(user)
	if request.method == "POST":
		form = UserInfoForm(data=request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			if 'picture' in request.FILES:
				post.picture = request.FILES['picture']
			post.save()
			return redirect('info')			
	else:
		'''Запрет редактирования чужого профиля. 
		Проверка юзера и передаваемого пораметра, если не совподает ридерект.'''
		if user in pk:
			form = UserInfoForm(instance=post)
		else:
			return redirect('info')
	return render(request, 'profuser/editinfo.html', {'form': form})
	
#Вывод публичного профиля
@login_required
def pub_info(request, pk):
	post = get_object_or_404(UserInfo, pk=pk)
	user = request.user.id
	error = ""
	userinfo = UserInfo.objects.filter(user = pk)
	refery = Refery.objects.get(user = user)
	referal = Refery.objects.get(user = pk)		
	referyone = refery.one_lvl
	#Исключение есть реферер или нет
	try:
		ref = UserInfo.objects.get(id= referal.one_lvl)
	except:
		ref = 0
				
	if request.method == "POST":
		form = UserSearchForm(request.POST)
		if form.is_valid():
			search = form.cleaned_data['search']
			#Исключение найден пользователь с таким id или нет
			try:
				s_user = UserInfo.objects.get(id = search)
				return redirect('/profuser/{}'.format(s_user.id))
			except:
				error = "Пользователя с таким id не существует!"
	else:
		form = UserSearchForm()		
	return render(request, 'profuser/pub_info.html', {'userinfo': userinfo, 'refery': referyone, 'useri': user, 'referal': referal.one_lvl, 'referal_two': referal.two_lvl, 'ref': ref, 'form': form,  'error': error})
	
#Вывод профиля
@login_required
def info(request):	
	user = request.user.id
	userinfo = UserInfo.objects.filter(user = user)
	referal = Refery.objects.get(user = user)
	#Исключение есть реферер или нет
	try:
		ref = UserInfo.objects.get(id= referal.one_lvl)
	except:
		ref = 0
	error = ""
	#Форма поиска пользователя
	if request.method == "POST":
		form = UserSearchForm(request.POST)
		if form.is_valid():
			search = form.cleaned_data['search']
			try:
				s_user = UserInfo.objects.get(id = search)
				return redirect('/profuser/{}'.format(s_user.id))
			except:
				error = "Пользователя с таким id не существует!"
	else:
		form = UserSearchForm()
	return render(request, 'profuser/userinfo.html', {'userinfo': userinfo, 'form': form,  'ref': ref, 'error': error})

#Вывод статистики пользователя
@login_required
def stat_user(request):
	user = request.user.id
	#Статистика последних 7 дней
	statuser = UserStatic.objects.filter(user = user)[:7]
	#Информация о профиле пользователя
	userinfo = UserInfo.objects.get(user = user)
	referal = Refery.objects.get(user = user)		
	#Исключение есть реферер или нет
	try:
		ref = UserInfo.objects.get(id= referal.one_lvl)
	except:
		ref = 0
	#Подсчет количества просмотров и т.п.
	stat = UserStatic.objects.filter(user = user)
	count = {'s' : 0, 't': 0, 'test': 0, 'p': 0, 'v': 0, 'r1': 0, 'r2': 0, 'ref_c': 0}
	for serf in stat:
		count['s'] += serf.serf
		count['t'] += serf.task
		count['test'] += serf.test
		count['p'] += serf.pismo
		count['v'] += serf.viplat
		count['r1'] += serf.ref_one
		count['r2'] += serf.ref_two
		count['ref_c'] = count['r1'] + count['r2']
	#Рефералы
	r = {}
	r['one_lvl'] = str(Refery.objects.filter(one_lvl = user).count())
	r['two_lvl'] = Refery.objects.filter(two_lvl = user).count()
	return render(request, 'profuser/statuser.html', {'statuser': statuser, 'userinfo': userinfo, 'ref': ref, 'count': count, 'r': r})#'count_s': count_s, 'count_t': count_t, 'count_test': count_test, 'count_p': count_p, 'count_v': count_v, 'r': r})
	
#Стать рефералом
@login_required
def iref(request, pk):
    post = get_object_or_404(Refery, pk=pk)
    user = request.user.id
    if request.method == "POST":
        form= IRefForm(request.POST)
		#Проверка реферералов юзера
        ref = Refery.objects.get(user = user)
        #Рефералы того чей профиль
        referal = Refery.objects.get(user = pk)
        if referal.one_lvl == user:
            messages.add_message(request, messages.ERROR, 'Извините, это Ваш реферер.')
            return redirect("/profuser/iref/{}".format(pk))			
        if ref.one_lvl != 0:
            messages.add_message(request, messages.ERROR, 'Извините, но у Вас есть реферер.')
            return redirect("/profuser/iref/{}".format(pk))
        else:
            if form.is_valid():			
                ref = form.cleaned_data['referer']
                if ref == "ДА":
                    refery = Refery.objects.get(user = user)
                    refery.one_lvl = pk
                    refery.two_lvl = referal.one_lvl
                    refery.user = request.user
                    refery.save()
                    messages.add_message(request, messages.ERROR, 'Поздравляем, Вы стали рефералом.')
                    return redirect("/profuser/iref/{}".format(pk))
                else:
                    messages.add_message(request, messages.ERROR, 'Не верная команда.')
                    return redirect("/profuser/iref/{}".format(pk))
    else:
        form = IRefForm()
    return render(request, 'profuser/iref.html', {'form': form})
	
# ######################### Реферальная система ################ #

#Добовление в рефералы
@login_required
def activ(request):	
	#Добовление в рефералы
	user = request.user.id
	if 'ref' in request.COOKIES:
		wallet = request.COOKIES["ref"]
		refery = Refery.objects.get(user = user)
		if refery.one_lvl == 0:
			refery.one_lvl = wallet
			for two in Refery.objects.filter(id = wallet):
				two_lvl = two.one_lvl
				if two_lvl == 0:
					refery.two_lvl= 0
				else:
					refery.two_lvl = two_lvl
			#Для 3-го уровня рефералов
			'''for three in Refery.objects.filter(one_lvl = two_lvl):
				three_lvl = three.two_lvl
				if three_lvl == '':
					refery.three_lvl = 0
				else:
					refery.three_lvl = three_lvl'''
			refery.id = refery.id
			refery.user = request.user
			refery.save()
	return render(request, 'profuser/activ.html')
	
#Cookie для ревералов
def referal(request, ref):
	if 'ref' in request.COOKIES:
		wallet = request.COOKIES.get('ref')
	else:
		wallet = ref      
	response = render(request, 'profuser/referal.html', {'wallet': wallet})
	response.set_cookie('ref', ref)
	return response

#Мои рефералы
@login_required
def myreferal(request):
	user = request.user.id
	r = {}
	referal = {}
	#referal = Refery.objects.filter(one_lvl = user)
	#name = Refery.objects.filter(user__username = referal)
	referal_one = Refery.objects.filter(one_lvl = user)
	referal_two = Refery.objects.filter(two_lvl = user)
	referal_three = Refery.objects.filter(three_lvl= user)
	r['one_lvl'] = str(Refery.objects.filter(one_lvl = user).count())
	r['two_lvl'] = Refery.objects.filter(two_lvl = user).count()
	r['three_lvl'] = Refery.objects.filter(three_lvl= user).count()
	'''for referal in Refery.objects.filter(one_lvl = user):
		r['user'] = User.objects.filter(id = referal.id)'''
	return render(request, 'profuser/myreferal.html', {'referal_one': referal_one, 'referal_two': referal_two, 'referal_three': referal_three, 'name': r})	

#Рекламные материалы для рефералов
@login_required
def rekmat(request):
	user = request.user.id
	userinfo = UserInfo.objects.get(user = user)
	return render(request, 'profuser/rekmat.html', {'users': user, 'userinfo': userinfo})	
	
# ################## Выплаты ########################## #

#Выбор системы для выплаты
@login_required
def sys_viplat(request):
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	return render(request, 'profuser/sysviplat.html')	

#Заказ вывода денег на WMR
@login_required	
def vivod_wmr(request):
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на личном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_lich
			
	if request.method == "POST":	
		sum = ViplatiWmrForm(request.POST)
		#Проверка рейтинга для выплат
		if s.rating < 1:
			vivod = 2
		elif s.rating < 499:
			vivod = 500
		elif s.rating >= 500:
			vivod = 1000
		#Проверяю казан ли кошелек
		if s.wmr == '0' or 'R' not in s.wmr:
			messages.add_message(request, messages.ERROR, 'Проверьте пожалуйста указан ли номер кошелька.')
			return redirect('sys_viplat')
		#Проверка валидации формы
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на личном счету и рейтингу
			money = sum.cleaned_data['sum']
			if money <= 0 or money > vivod:
				messages.add_message(request, messages.ERROR, 'Введена не верная сумма. Или недопустиммая сумма по рейтингу')
				return redirect('sys_viplat')
			else:
				if money <= schet:
					#Добовляю сумму на вывод
					post = sum.save(commit=False)
					post.user = request.user
					post.sum = money
					post.sys_viplat = s.wmr
					post.save()						
					#Вычитаю сумму с личного счета
					pshet = UserInfo.objects.get(user_id = user)
					schet = schet - money
					pshet.schet_lich = schet
					pshet.user = pshet.user
					pshet.save()
					messages.add_message(request, messages.ERROR, 'Запрос на вывод принят. Пожалуйста ждите')
					return redirect('sys_viplat')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на личном счету.')
					return redirect('sys_viplat')
	else:
		form = ViplatiWmrForm()
	return render(request, 'profuser/wmr.html', {'form': form})		

#Заказ вывода денег на Yandex	
@login_required	
def vivod_yandex(request):
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на личном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_lich
			
	if request.method == "POST":	
		sum = ViplatiYandexForm(request.POST)
		#Проверка рейтинга для выплат
		if s.rating < 1:
			vivod = 2
		elif s.rating < 499:
			vivod = 500
		elif s.rating >= 500:
			vivod = 1000
		#Проверяю казан ли кошелек
		if s.yandex == '0' or ' ' in s.yandex:
			messages.add_message(request, messages.ERROR, 'Проверьте пожалуйста указан ли номер кошелька.')
			return redirect('sys_viplat')
		#Проверка валидации формы
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на личном счету и рейтингу
			money = sum.cleaned_data['sum']
			if money <= 0 or money > vivod:
				messages.add_message(request, messages.ERROR, 'Введена не верная сумма. Или недопустиммая сумма по рейтингу')
				return redirect('sys_viplat')
			else:
				if money <= schet:
					#Добовляю сумму на вывод
					post = sum.save(commit=False)
					post.user = request.user
					post.sum = money
					post.sys_viplat = s.yandex
					post.save()						
					#Вычитаю сумму с личного счета
					pshet = UserInfo.objects.get(user_id = user)
					schet = schet - money
					pshet.schet_lich = schet
					pshet.user = pshet.user
					pshet.save()
					messages.add_message(request, messages.ERROR, 'Запрос на вывод принят. Пожалуйста ждите')
					return redirect('sys_viplat')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на личном счету.')
					return redirect('sys_viplat')
	else:
		form = ViplatiYandexForm()
	return render(request, 'profuser/yandex.html', {'form': form})
	
#Заказ вывода денег на QIWI	
@login_required	
def vivod_qiwi(request):
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на личном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_lich
			
	if request.method == "POST":	
		sum = ViplatiQiwiForm(request.POST)
		#Проверка рейтинга для выплат
		if s.rating < 1:
			vivod = 2
		elif s.rating < 499:
			vivod = 500
		elif s.rating >= 500:
			vivod = 1000
		#Проверяю казан ли кошелек
		if s.qiwi == '0' or '+' not in s.qiwi:
			messages.add_message(request, messages.ERROR, 'Проверьте пожалуйста указан ли номер кошелька.')
			return redirect('sys_viplat')
		#Проверка валидации формы
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на личном счету и рейтингу
			money = sum.cleaned_data['sum']
			if money <= 0 or money > vivod:
				messages.add_message(request, messages.ERROR, 'Введена не верная сумма. Или недопустиммая сумма по рейтингу')
				return redirect('sys_viplat')
			else:
				if money <= schet:
					#Добовляю сумму на вывод
					post = sum.save(commit=False)
					post.user = request.user
					post.sum = money
					post.sys_viplat = s.qiwi
					post.save()						
					#Вычитаю сумму с личного счета
					pshet = UserInfo.objects.get(user_id = user)
					schet = schet - money
					pshet.schet_lich = schet
					pshet.user = pshet.user
					pshet.save()
					messages.add_message(request, messages.ERROR, 'Запрос на вывод принят. Пожалуйста ждите')
					return redirect('sys_viplat')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на личном счету.')
					return redirect('sys_viplat')
	else:
		form = ViplatiQiwiForm()
	return render(request, 'profuser/qiwi.html', {'form': form})

#Заказ вывода денег на Perfect money	
@login_required	
def vivod_perfect(request):
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на личном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_lich
			
	if request.method == "POST":	
		sum = ViplatiPerfectForm(request.POST)
		#Проверка рейтинга для выплат
		if s.rating < 1:
			vivod = 2
		elif s.rating < 499:
			vivod = 500
		elif s.rating >= 500:
			vivod = 1000
		#Проверяю казан ли кошелек
		if s.perfect_money == '0' or 'U' not in s.perfect_money:
			messages.add_message(request, messages.ERROR, 'Проверьте пожалуйста указан ли номер кошелька.')
			return redirect('sys_viplat')
		#Проверка валидации формы
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на личном счету и рейтингу
			money = sum.cleaned_data['sum']
			if money <= 0 or money > vivod:
				messages.add_message(request, messages.ERROR, 'Введена не верная сумма. Или недопустиммая сумма по рейтингу')
				return redirect('sys_viplat')
			else:
				if money <= schet:
					#Добовляю сумму на вывод
					post = sum.save(commit=False)
					post.user = request.user
					post.sum = money
					post.sys_viplat = s.perfect_money
					post.save()						
					#Вычитаю сумму с личного счета
					pshet = UserInfo.objects.get(user_id = user)
					schet = schet - money
					pshet.schet_lich = schet
					pshet.user = pshet.user
					pshet.save()
					messages.add_message(request, messages.ERROR, 'Запрос на вывод принят. Пожалуйста ждите')
					return redirect('sys_viplat')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на личном счету.')
					return redirect('sys_viplat')
	else:
		form = ViplatiPerfectForm()
	return render(request, 'profuser/perfect.html', {'form': form})	

#Заказ вывода денег на Payeer	
@login_required	
def vivod_payeer(request):
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на личном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_lich
			
	if request.method == "POST":	
		sum = ViplatiPayeerForm(request.POST)
		#Проверка рейтинга для выплат
		if s.rating < 1:
			vivod = 2
		elif s.rating < 499:
			vivod = 500
		elif s.rating >= 500:
			vivod = 1000
		#Проверяю казан ли кошелек
		if s.payeer == '0' or 'P' not in s.payeer:
			messages.add_message(request, messages.ERROR, 'Проверьте пожалуйста указан ли номер кошелька.')
			return redirect('sys_viplat')
		#Проверка валидации формы
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на личном счету и рейтингу
			money = sum.cleaned_data['sum']
			if money <= 0 or money > vivod:
				messages.add_message(request, messages.ERROR, 'Введена не верная сумма. Или недопустиммая сумма по рейтингу')
				return redirect('sys_viplat')
			else:
				if money <= schet:
					#Добовляю сумму на вывод
					post = sum.save(commit=False)
					post.user = request.user
					post.sum = money
					post.sys_viplat = s.payeer
					post.save()						
					#Вычитаю сумму с личного счета
					pshet = UserInfo.objects.get(user_id = user)
					schet = schet - money
					pshet.schet_lich = schet
					pshet.user = pshet.user
					pshet.save()
					messages.add_message(request, messages.ERROR, 'Запрос на вывод принят. Пожалуйста ждите')
					return redirect('sys_viplat')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на личном счету.')
					return redirect('sys_viplat')
	else:
		form = ViplatiPayeerForm()
	return render(request, 'profuser/payeer.html', {'form': form})		
	
# ####################### Пополнение ############################ #

#Выбор системы для пополнения
@login_required
def sys_popol(request):
	#Получение id пользователя
	user = request.user.id
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_lich
	return render(request, 'profuser/syspopol.html')	
	
	
# ####################### Статистика пользователя ################### #



