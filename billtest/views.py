from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django import forms
from .models import BillTest
from django.contrib.auth.models import User
from .forms import BillTestForm, PopolnitTestForm, OtvetTestForm
from django.contrib import messages
from profuser.models import UserInfo, Refery, UserStatic
from balanssite.models import Balans
from datetime import datetime, timedelta
from statis.models import Statistica
from datetime import datetime


#Функция расчта стоимости теста
def func_link(time_t, vid_t):
	price = 0.4
	#Узнаю время для таймера и стоимость
	if time_t == "ONE_T":
		potimer = 0	
	elif time_t == "TWO_T":
		potimer = 0.15 / 2	
	#Узанаю заказано ли выделение теста
	if vid_t == "TWO_T":
		vid_t = 0.02 / 2
	else:
		vid_t = 0
	
	#Считаю сумму для вычита из баланса задания
	price_site = potimer * 2 + vid_t * 2 + price
	#Считаю сумму для сайта	
	price_s = potimer + vid_t 
	#Считаю сумму для пользователя
	price_u = potimer + vid_t + price
	a = {'price_site': price_site, 'price_s': price_s, 'price_u': price_u}
	return a

#Функция просмотров осталось
def prosm_ost(pk):
	silka = BillTest.objects.get(id=pk)
	silka.prosm_ost = silka.price_test // silka.price_t
	silka.spis = 0
	silka.save(update_fields=['prosm_ost', 'spis'])
	
#Добавление теста
@login_required
def addtest(request):
	if request.method == "POST":
		form = BillTestForm(request.POST)
		if form.is_valid():
			time_t = form.cleaned_data['time_t']
			vid_t = form.cleaned_data['vid_t']
			var_one = form.cleaned_data['var_one']
			var_two = form.cleaned_data['var_two']
			var_three = form.cleaned_data['var_three']
			if var_one <=0 or var_one >= 4:
				messages.success(request, 'Не верно указан вариант ответа')
				return redirect('addtest')
			if var_two <=0 or var_two >= 4:
				messages.success(request, 'Не верно указан вариант ответа')
				return redirect('addtest')	
			if var_three <=0 or var_three >= 4:
				messages.success(request, 'Не верно указан вариант ответа')
				return redirect('addtest')
			#Вызов функции обработки стоимости
			a = func_link(time_t, vid_t)
			post = form.save(commit=False)
			post.user = request.user
			post.price_u = a['price_u']
			post.price_s = a['price_s']
			post.price_t = a['price_site']
			post.save()
			messages.success(request, 'Тест добавлен.')
			return redirect('mytest')
	else:
		form = BillTestForm()
	return render(request, 'billtest/addtest.html', {'form': form})
	
#Редактировать тест
@login_required
def edit_test(request, pk):
	post = get_object_or_404(BillTest, pk=pk)
	users = request.user.id
	use = str(users)
	if request.method == "POST":
		form = BillTestForm(data=request.POST, instance=post)
		if form.is_valid():
			time_t = form.cleaned_data['time_t']
			vid_t = form.cleaned_data['vid_t']
			var_one = form.cleaned_data['var_one']
			var_two = form.cleaned_data['var_two']
			var_three = form.cleaned_data['var_three']
			if var_one <=0 or var_one >= 4:
				messages.success(request, 'Не верно указан вариант ответа')
				return redirect('addtest')
			if var_two <=0 or var_two >= 4:
				messages.success(request, 'Не верно указан вариант ответа')
				return redirect('addtest')	
			if var_three <=0 or var_three >= 4:
				messages.success(request, 'Не верно указан вариант ответа')
				return redirect('addtest')
			#Вызов функции обработки стоимости
			a = func_link(time_t, vid_t)
			post = form.save(commit=False)
			post.price_u = a['price_u']
			post.price_s = a['price_s']
			post.price_t = a['price_site']
			post.moder = 0
			post.odobren = 0
			post.save()
			#Высчитываю остаток просмотров
			prosm_ost(pk)
			return redirect('mytest')			
	else:
		#Запрет редактирования чужого задания.
		p = BillTest.objects.get(id = pk)
		if  users == p.user_id:
			form = BillTestForm(instance=post)
		else:
			return redirect('mytest')
	return render(request, 'billtest/edittest.html', {'form': form})

#Удаление теста
@login_required
def delete_test(request, pk):
	post = get_object_or_404(BillTest, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = BillTest.objects.get(id = pk, user = user)
		money = post.price_test
		post.delete()
		#Возвращаю деньги на рекламный счет
		pshet = UserInfo.objects.get(user_id = user)
		pshet.schet_reklam += money
		pshet.save(update_fields=['schet_reklam'])
		return redirect('mytest')			
	return render(request, 'billtest/deletetest.html', {'task': pk})
	
#Отправка на модерацию тест
@login_required
def moder_test(request, pk):
	post = get_object_or_404(BillTest, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = BillTest.objects.get(id = pk, user = user)
		post.moder = 1
		post.odobren = 0
		post.save(update_fields=['moder', 'odobren'])
		return redirect('mytest')			
	return render(request, 'billtest/moder_test.html', {'task': pk})

#Пауза теста
@login_required
def pausa_test(request, pk):
	post = get_object_or_404(BillTest, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = BillTest.objects.get(id = pk, user = user)
		post.pausa = 1
		post.save(update_fields=['pausa'])
		return redirect('mytest')			
	return render(request, 'billtest/pausa_test.html', {'task': pk})
	
#Старт теста
@login_required
def start_test(request, pk):
	post = get_object_or_404(BillTest, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = BillTest.objects.get(id = pk, user = user)
		post.pausa = 0
		post.save(update_fields=['pausa'])
		return redirect('mytest')			
	return render(request, 'billtest/start_test.html', {'task': pk})
	
#Все дабавленые тесты для рекламодателя
@login_required
def mytest(request):
	user = request.user.id
	mytest = BillTest.objects.filter(user_id=user)
	return render(request, 'billtest/mytest.html', {'mytest': mytest})

#Все тесты для пользователей	
@login_required
def billtestall(request):
	user = request.user.id
	userinfo = BillTest.objects.filter(odobren = 1)
	return render(request, 'billtest/billtest.html', {'userinfo': userinfo})
	
#Подробнее о тесте и ответ на него	
@login_required	
def test_detail(request, pk):
	task = get_object_or_404(BillTest, pk=pk)
	today = datetime.today()
	user = request.user
	a = datetime.now()
	a = a.strftime('%Y-%m-%d %H:%M:%S')
	task_ss = BillTest.objects.filter(id = pk)
	#Вибираю текущей ответ на задание
	task_s = BillTest.objects.get(id = pk)
	#Узнаю баланс теста
	schet = task_s.price_test
	schet = float(schet)
	#Узнаю цену на ссылку 
	#price = task_s.price
	#Считаю сумму для вычита из баланса задания
	price_site = float(task_s.price_t)
    #Считаю сумму для сайта	
	price_s = float(task_s.price_s)
	#Считаю сумму для пользователя
	price= float(task_s.price_u)
	#Сохраняю ответ
	if request.method == "POST":
		#Проверю хватает ли денег на балансе задания
		if schet < price_site:
			messages.add_message(request, CRITICAL, 'Не достаточно денег на счету теста')
			return redirect('billtestall')
		else:
			form = OtvetTestForm(request.POST)
			if form.is_valid():
				var_one = form.cleaned_data['var_one']
				var_two = form.cleaned_data['var_two']
				var_three = form.cleaned_data['var_three']
				if var_one <=0 or var_one >= 4:
					messages.success(request, 'Не верно указан вариант ответа')
					return redirect('/billtest/test/{}'.format(pk))
				if var_two <=0 or var_two >= 4:
					messages.success(request, 'Не верно указан вариант ответа')
					return redirect('/billtest/test/{}'.format(pk))
				if var_three <=0 or var_three >= 4:
					messages.success(request, 'Не верно указан вариант ответа')
					return redirect('/billtest/test/{}'.format(pk))
				if var_one == task_s.var_one and var_two == task_s.var_two and var_three == task_s.var_three:
					#Обновляю баланс пользователя и рейтинг
					pshet = UserInfo.objects.get(user = user)
					pshet.schet_lich += price
					pshet.rating += 0.5
					pshet.user = user
					pshet.id = user.id
					pshet.save()
					#Вычитаю деньги со счета теста
					tshet = BillTest.objects.get(id= task_s.id)
					pr = 0
					prosm = 0
					if tshet.spis == 0:
						pr = tshet.sum_spis
						prosm = pr // tshet.price_t + 1
						tshet.prosm += prosm
						tshet.prosm_ost -= prosm					
						tshet.price_test = schet - (price_site + pr)
						tshet.sum_spis = 0
						tshet.spis = 1	
					else:
						schet = schet - price_site
						tshet.price_test = schet
						tshet.prosm += 1
						tshet.prosm_ost -= 1
					tshet.user = task_s.user
					tshet.save()
					#Обновляю баланс сайта			
					#Считаю процент  рефери 1 уровень и вычитаю из баланса сайта
					refery = Refery.objects.get(user = user)	
					if refery.one_lvl != 0:
						refery_one = UserInfo.objects.get(user = refery.one_lvl)
						if refery_one.rating < 20:
							price_refery = price_s * 0.1
						elif refery_one.rating >= 20 and refery_one.rating < 50:
							price_refery = price_s * 0.2
						elif refery_one.rating >= 50 and refery_one.rating < 100:
							price_refery = price_s * 0.2
						elif refery_one.rating >= 100 and refery_one.rating < 300:
							price_refery = price_s * 0.3			
						elif refery_one.rating >= 300 and refery_one.rating < 500:
							price_refery = price_s * 0.35
						elif refery_one.rating >= 500:
							price_refery = price_s * 0.40								
						elif refery_one.rating == 0:
							price_refery = 0
						price_r = price_refery
						#Прибовляю деньги к личному счету пользователя
						refery_one.schet_lich += price_r
						refery_one.save(update_fields=['schet_lich'])
						#Прибовляю к статистики заработка с рефералов 1 ур.
						stat_u_r1 = UserStatic.objects.get(user = refery.one_lvl, pub_date = today.date())
						stat_u_r1.ref_one += price_r
						stat_u_r1.save()
						#Считаю процент  рефери 2 уровень и вычитаю из баланса сайта
						if refery.two_lvl != 0:
							refery_two = UserInfo.objects.get(user = refery.two_lvl)
							if refery_two.rating >= 100 and refery_two.rating < 300:
								price_refery2 = price_s * 0.3			
							elif refery_two.rating >= 300 and refery_two.rating < 500:
								price_refery2 = price_s * 0.35
							elif refery_two.rating >= 500:
								price_refery2 = price_s * 0.40								
							else:
								price_refery2 = 0
							price_r2 = price_refery2
						#Прибовляю деньги к личному счету пользователя
							refery_two.schet_lich += price_r2
							refery_two.save(update_fields=['schet_lich'])
							#Прибовляю к статистики заработка с рефералов 2 ур.
							stat_u_r2 = UserStatic.objects.get(user = refery.two_lvl, pub_date = today.date())
							stat_u_r2.ref_two += price_r2
							stat_u_r2.save()
						#Сумма процентов рефереров
						else:
							price_r2 = 0			
					else:
						price_r  = 0
						price_r2 = 0	
					perechet = price_r + price_r2
					#Обновляю баланс сайта			
					site = Balans.objects.get(id=1)
					site.schet_site += (price_s - perechet) + pr
					site.id = 1
					site.save(update_fields=['schet_site'])
					#Обновляю статистику сайта			
					stat = Statistica.objects.get(id=1)
					stat.id = 1
					stat.task = stat.task + 1
					stat.save(update_fields=['task'])
					#Добовление стаистики пользователя
					stat_u = UserStatic.objects.get(user = user, pub_date = today.date())
					stat_u.test += 1
					stat_u.save()
					messages.add_message(request, messages.ERROR, 'Ответ отправлен.')
					return redirect('billtestall')
				else:
					messages.add_message(request, messages.ERROR, 'Тест не пройден')
					return redirect('billtestall')
	else:	
		form = OtvetTestForm()
	return render(request, 'billtest/test_detail.html', {'task': task, 'form': form, 'task_s': task_ss, 'a': a})
	
#Пополнение баланса теста	
@login_required	
def popolnit_test(request, pk):
	task = get_object_or_404(BillTest, pk=pk)
	zadanie = BillTest.objects.get(id=pk)
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_reklam
	if request.method == "POST":	
		sum = PopolnitTestForm(request.POST)
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на рекламном счету
			money = sum.cleaned_data['price_test']
			if money < 11:
				messages.add_message(request, messages.ERROR, 'Введена не верная сумма.')
				return redirect('mytest')
			else:
				if money <= schet:
					#Добовляю сумму и обнавляю форму
					post = sum.save(commit=False)
					price_test = zadanie.price_test + money
					post.id = zadanie.id
					post.user = request.user
					post.price_test = price_test
					#Сумма для списания с 11 руб.
					post.spis = 0
					sum_spis = money // 11
					post.sum_spis = zadanie.sum_spis + sum_spis
					post.save(update_fields=['price_test', 'sum_spis', 'spis'])
					prosm_ost(pk)
					#Вычитаю сумму с рекламного счета
					pshet = UserInfo()
					schet = schet - money
					pshet.schet_reklam = schet
					pshet.user = request.user
					pshet.id = request.user.id
					pshet.save(update_fields=['schet_reklam'])
					
					messages.add_message(request, messages.ERROR, 'Баланс теста пополнен.')
					return redirect('mytest')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на рекламном счету. Пополните счет.')
					return redirect('mytest')
	else:
		form = PopolnitTestForm()
	return render(request, 'billtest/popolnit.html', {'task': task, 'form': form})