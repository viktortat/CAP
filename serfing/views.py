from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django import forms
from .models import Serf, SerfUsers, Plinks, Contlinks, Pismo, PismoUsers, Perehod, PerehodUsers
from django.contrib.auth.models import User
from .forms import SerfForm, PopolnitSerfForm, CaptchaForm, PlinksForm, PopolnitPlinksForm, ContlinksForm, PopolnitContlinksForm, PismoForm, PopolnitPismoForm, CaptchaPismoForm, PerehodForm, PopolnitPerehodForm
from django.shortcuts import redirect
from django.contrib import messages
from profuser.models import UserInfo, Refery, UserStatic
from balanssite.models import Balans
from statis.models import Statistica
from datetime import datetime, timedelta, date
from django.utils import timezone
import time
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 

#Функция расчта стоимости ссылки
def func_link(price, time_r, perehod, porating, posex):
#Узнаю время для таймера и стоимость доп. %
	if time_r == "5":
		potimer = price - (price * 0.45)	
		p_s = potimer * 0.45 / 2
		p_u = potimer - (potimer * 0.45 / 2)
	elif time_r == "10":
		potimer = price - (price * 0.30)	
		p_s = potimer * 0.30 / 2
		p_u = potimer - (potimer * 0.30 / 2)
	elif time_r == "15":
		potimer = price - (price * 0.15)	
		p_s = potimer * 0.15 / 2
		p_u = potimer - (potimer * 0.15 / 2)
	elif time_r == "20":
		potimer = price
		p_s = 0
		p_u = price	
	elif time_r == "25":
		potimer = price + (price * 0.15)
		p_s = price * 0.15 / 2
		p_u = price + (price * 0.15 / 2)
	elif time_r == "30":
		potimer = price + price * 0.30
		p_s = price * 0.30 / 2
		p_u = price + (price * 0.30 / 2)				
	elif time_r == "35":
		potimer =  price + price * 0.45
		p_s = price * 0.45 / 2
		p_u = price + (price * 0.45 / 2)				
	elif time_r == "40":
		potimer =  price + price * 0.60
		p_s = price * 0.60 / 2
		p_u = price + (price * 0.60 / 2)				
	elif time_r == "45":
		potimer =  price + price * 0.75
		p_s = price * 0.75 / 2
		p_u = price + (price * 0.75 / 2)				
	elif time_r == "50":
		potimer =  price + price * 0.90
		p_s = price * 0.90 / 2
		p_u = price + (price * 0.90 / 2)				
	elif time_r == "55":
		potimer =  price + price * 1.05
		p_s = price * 1.05 / 2
		p_u = price + (price * 1.05 / 2)				
	elif time_r == "60":
		potimer =  price + price * 1.2
		p_s = price * 1.2 / 2
		p_u = price + (price * 1.2 / 2)				
	#Узнаю заказан переход насайт или нет
	if perehod == "NO":
		perehod = 0
	elif perehod == "YES":
		perehod = 0.02 / 2
	#Узнаю заказан рейтинг или нет
	if porating == "VSEPOL":
		porating = 0
	else:
		porating = 0.02 / 2
	#Узанаю заказан половой признак пользоватеей
	if posex == "VSEPOLZ":
		posex = 0
	else:
		posex = 0.01 / 2
	
	#Считаю сумму для вычита из баланса задания
	price_site = potimer + perehod  * 2 + porating * 2 + posex * 2
	#Считаю сумму для сайта	
	price_s = p_s + perehod + porating + posex
	#Считаю сумму для пользователя
	price_u = p_u + perehod + porating + posex
	a = {'price_site': price_site, 'price_s': price_s, 'price_u': price_u}
	return a
	
#Добовление ссылки серфинга
@login_required
def addserf(request):
	user = request.user.id
	CRITICAL = 50
	if request.method == "POST":
		form = SerfForm(request.POST)
		if form.is_valid():
			price = form.cleaned_data['price']
			price = float(price)
			time_r  = form.cleaned_data['time_r']
			perehod  = form.cleaned_data['perehod']
			porating  = form.cleaned_data['porating']
			posex  = form.cleaned_data['posex']
			#Вызов функции обработки стоимости
			a = func_link(price, time_r, perehod, porating, posex)
			#Сахроняю форму
			post = form.save(commit=False)
			post.user = request.user
			post.price_u = a['price_u']
			post.price_s = a['price_s']
			post.price_t = a['price_site']
			post.save()
			messages.success(request, 'Добавленно')
			return redirect('myserf')
	else:
		form = SerfForm()
	return render(request, 'serfing/addserf.html', {'form': form})

#Редактировать ссылки
@login_required
def edit_serf(request, pk):
	post = get_object_or_404(Serf, pk=pk)
	users = request.user.id
	use = str(users)
	if request.method == "POST":
		form = SerfForm(data=request.POST, instance=post)
		if form.is_valid():
			price = form.cleaned_data['price']
			price = float(price)
			time_r  = form.cleaned_data['time_r']
			perehod  = form.cleaned_data['perehod']
			porating  = form.cleaned_data['porating']
			posex  = form.cleaned_data['posex']
			#Вызов функции обработки стоимости
			a = func_link(price, time_r, perehod, porating, posex)
			post = form.save(commit=False)
			post.price_u = a['price_u']
			post.price_s = a['price_s']
			post.price_t = a['price_site']
			post.moder = 0
			post.odobren = 0
			post.save()
			#Высчитываю остаток просмотров
			prosm_ost(pk)
			return redirect('myserf')			
	else:
		#Запрет редактирования чужого задания.
		p = Serf.objects.get(id = pk)
		if  users == p.user_id:
			form = SerfForm(instance=post)
		else:
			return redirect('myserf')
	return render(request, 'serfing/editserf.html', {'form': form})

#Удаление ссылки
@login_required
def delete_serf(request, pk):
	post = get_object_or_404(Serf, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Serf.objects.get(id = pk, user = user)
		money = post.price_serf
		post.delete()
		#Возвращаю деньги на рекламный счет
		pshet = UserInfo.objects.get(user_id = user)
		pshet.schet_reklam += money
		pshet.save(update_fields=['schet_reklam'])
		return redirect('myserf')			
	return render(request, 'serfing/deleteserf.html', {'task': pk})

#Отправка на модерацию ссылку
@login_required
def moder_serf(request, pk):
	post = get_object_or_404(Serf, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Serf.objects.get(id = pk, user = user)
		post.moder = 1
		post.odobren = 0
		post.save(update_fields=['moder', 'odobren'])
		return redirect('myserf')			
	return render(request, 'serfing/moder_serf.html', {'task': pk})

#Пауза ссылки
@login_required
def pausa_serf(request, pk):
	post = get_object_or_404(Serf, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Serf.objects.get(id = pk, user = user)
		post.pausa = 1
		post.save(update_fields=['pausa'])
		return redirect('myserf')			
	return render(request, 'serfing/pausa_serf.html', {'task': pk})

#Старт ссылки
@login_required
def start_serf(request, pk):
	post = get_object_or_404(Serf, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Serf.objects.get(id = pk, user = user)
		post.pausa = 0
		post.save(update_fields=['pausa'])
		return redirect('myserf')			
	return render(request, 'serfing/start_serf.html', {'task': pk})
	
#Все дабавленые ссылки для рекламодателя
@login_required
def myserf(request):
	user = request.user.id
	myserf = Serf.objects.filter(user_id=user)
	return render(request, 'serfing/myserf.html', {'myserf': myserf})

#Функция просмотров осталось
def prosm_ost(pk):
	silka = Serf.objects.get(id=pk)
	silka.prosm_ost = silka.price_serf // silka.price_t
	silka.spis = 0
	silka.save(update_fields=['prosm_ost', 'spis'])
	

#Пополнение баланса ссылки
@login_required	
def popolnit_serf(request, pk):
	serf = get_object_or_404(Serf, pk=pk)
	silka = Serf.objects.get(id=pk)
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_reklam
	if request.method == "POST":	
		sum = PopolnitSerfForm(request.POST)#, instance=post)
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на рекламном счету
			money = sum.cleaned_data['price_serf']
			if money < 11:
				messages.add_message(request, messages.ERROR, 'Минимум 11 рублей.')
				return redirect('myserf')
			else:
				if money <= schet:
					#Добовляю сумму и обнавляю форму
					post = sum.save(commit=False)
					price_serf = silka.price_serf + money
					post.id = silka.id
					post.user = request.user
					post.price_serf = price_serf
					#Сумма для списания с 11 руб.
					post.spis = 0
					sum_spis = money // 11
					post.sum_spis = silka.sum_spis + sum_spis
					post.save(update_fields=['price_serf', 'sum_spis', 'spis'])
					prosm_ost(pk)
					#Вычитаю сумму с рекламного счета
					pshet = UserInfo()
					schet = schet - money
					pshet.schet_reklam = schet
					pshet.user = request.user
					pshet.id = request.user.id
					pshet.save(update_fields=['schet_reklam'])
					messages.add_message(request, messages.ERROR, 'Баланс ссылки пополнен.')
					return redirect('myserf')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на рекламном счету. Пополните счет.')
					return redirect('myserf')
	else:
		form = PopolnitSerfForm()
	return render(request, 'serfing/popolnit.html', {'silka': silka, 'form': form})
	
	
	
#Все ссылки серфинга для пользователей	
@login_required
def serfall(request):
	user = request.user.id
	today = datetime.today()
	#Вывожу ссылки серфинга исключая с нул балансом и посещеные
	#userinfo = Serf.objects.filter(odobren = 1, moder = 1, pausa = 0).exclude(price_serf__lt = 1).exclude(user__serf_user = user, user__pub_date__gte = today.date())
	userinfo = Serf.objects.filter(odobren = 1, moder = 1, pausa = 0).exclude(price_serf__lt = 1)#.exclude(serfusers__user = user, serfusers__pub_date__gte = today.date())
	#Вывожу псевдо ссылки исключая с нул балансом										
	plinks = Plinks.objects.filter(odobren = 1).exclude(price_link = 0)
	return render(request, 'serfing/serf.html', {'userinfo': userinfo, 'plinks': plinks})

#Просмотр страницы серфинга
@login_required
def frame_serf(request, pk):
	serf = get_object_or_404(Serf, pk=pk)
	user = request.user
	today = datetime.today()
	#Исключение если сылка сегодня посещена ридерект
	try:
		SerfUsers.objects.get(user = user, serf_user = serf, pub_date__gte=date.today())
		return redirect('serfall')
	except:
		CRITICAL = 50
	
	#Узнаю время для таймера
	b = int(serf.time_r)
	#Узнаю баланс ссылки
	schet = serf.price_serf
	schet = float(schet)
	#Считаю сумму для вычита из баланса задания
	price_site = float(serf.price_t)
    #Считаю сумму для сайта	
	price_s = float(serf.price_s)
	#Считаю сумму для пользователя
	price= float(serf.price_u)
    #price_r = 0
    #price_r2 = 0
	if request.method == "POST":
		#Проверю хватает ли денег на балансе задания
		if schet < price_site:
			messages.add_message(request, CRITICAL, 'Не достаточно денег на счету ссылки!')
			return redirect('serfall')
		else:
			form = CaptchaForm(request.POST)
			if form.is_valid():
				#Подтсверждение ответа				
				post = form.save(commit=False)
				#исключение если запись о посещении есть обновляю, если нет создаю новую
				try: 
					p = SerfUsers.objects.get(user = user, serf_user = serf)
					post.serf_user = serf
					post.odobren = 1
					post.pub_date = today.date()
					post.user = user	
                    #post.id = p.id
					post.save(update_fields=['pub_date'])
				except:
					post.serf_user = serf
					post.odobren = 1
					post.pub_date = today.date()
					post.user = user	
				#post.id = user.id
					post.save()
				#Прибовляю деньги к личному счету пользователя + рейтинг
				pshet = UserInfo.objects.get(user = user)
				pshet.schet_lich += price
				pshet.rating += 0.01
				pshet.user = user
				pshet.id = user.id
				pshet.save()
				#Вычитаю деньги со счета ссылки
				tshet = Serf.objects.get(id= serf.id)
				#Списание с каждых 11 руб. 1руб.
				pr = 0
				prosm = 0
				if tshet.spis == 0:
					pr = tshet.sum_spis
					prosm = pr // tshet.price_t
					tshet.prosm += prosm
					tshet.prosm_ost -= prosm					
					tshet.price_serf = schet - (price_site + pr)
					tshet.sum_spis = 0
					tshet.spis = 1	
				else:
					schet = schet - price_site
					tshet.price_serf = schet
					tshet.prosm += 1
					tshet.prosm_ost -= 1
				tshet.user = serf.user
				#tshet.id = request.user.id
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
				
				messages.add_message(request, CRITICAL, 'Ответ подтвержден.')
				#Обновляю статистику сайта			
				stat = Statistica.objects.get(id=1)
				stat.id = 1
				stat.click = (stat.click + 1) + prosm
				stat.save(update_fields=['click'])
				#Добовление стаистики пользователя
				stat_u = UserStatic.objects.get(user = user, pub_date = today.date())
				stat_u.serf += 1
				stat_u.save()
				if serf.perehod == "NO":
					return redirect('serfall')
				elif serf.perehod == "YES":
					return redirect(serf.url)
	else:
		form = CaptchaForm()
	return render(request, 'serfing/frame_serf.html', {'form': form, 'serf': serf, 'b': b})

# ###################### Псевдо ссылки ############################ #

#Добавление псевдо ссылки
@login_required
def addplinks(request):
	#Получение id пользователя
	user = request.user
	if request.method == "POST":
		form = PlinksForm(request.POST)
		if form.is_valid():		
			#Сахроняю форму
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('myplinks')
	else:
		form = PlinksForm()
	return render(request, 'serfing/addplinks.html', {'form': form})

#Все дабавленые псевдо ссылки для рекламодателя
@login_required
def myplinks(request):
	user = request.user.id
	mylinks = Plinks.objects.filter(user_id=user)
	return render(request, 'serfing/mylinks.html', {'mylinks': mylinks})

#Пополнение баланса псевдо ссылки
@login_required	
def popolnit_plinks(request, pk):
	serf = get_object_or_404(Plinks, pk=pk)
	silka = Plinks.objects.get(id=pk)
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_reklam
	if request.method == "POST":	
		sum = PopolnitPlinksForm(request.POST)#, instance=post)
		if sum.is_valid():
			#Получаю введеное кол-во дней и проверяю хватает ли на рекламном счету
			days = sum.cleaned_data['days']
			if days <= 0:
				messages.add_message(request, messages.ERROR, 'Введено не вернае количество дней.')
				return redirect('myplinks')
			else:
				money = days * 4
				if money <= schet:
					#Добовляю сумму и обнавляю форму
					post = sum.save(commit=False)
					price_link = silka.price_link + money
					post.id = silka.id
					post.user = request.user
					post.price_link = price_link
					post.save(update_fields=['price_link'])
					#Вычитаю сумму с рекламного счета
					pshet = UserInfo()
					schet = schet - money
					pshet.schet_reklam = schet
					pshet.user = request.user
					pshet.id = request.user.id
					pshet.save(update_fields=['schet_reklam'])
					messages.add_message(request, messages.ERROR, 'Баланс ссылки пополнен.')
					#Обновление баланса сайта
					site_shet = Balans.objects.get(id=1)
					site_shet.schet_site += money
					site_shet.id = 1
					site_shet.save(update_fields=['schet_site'])
					return redirect('myplinks')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на рекламном счету. Пополните счет.')
					return redirect('myplinks')
	else:
		form = PopolnitPlinksForm()
	return render(request, 'serfing/popolnit_plinks.html', {'silka': silka, 'form': form})

'''import time
def vichet_plinks():
	while True:
		time.sleep(10)  # 24 часа в секундах.
		silka = Plinks.objects.all()
		silka.price_link -= 4
		silka.id = 1
		silka.user = 1
		silka.save(update_fields=['price_link'])'''
# ##################### Контекстная реклама ################### #

#Добавление контекстной ссылки
@login_required
def addcontlinks(request):
	#Получение id пользователя
	user = request.user
	if request.method == "POST":
		form = ContlinksForm(request.POST)
		if form.is_valid():		
			#Сахроняю форму
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('mycontlinks')
	else:
		form = ContlinksForm()
	return render(request, 'serfing/addcontlinks.html', {'form': form})
	
#Все дабавленые контекстные ссылки для рекламодателя
@login_required
def mycontlinks(request):
	user = request.user.id
	mylinks = Contlinks.objects.filter(user_id=user)
	return render(request, 'serfing/mycontlinks.html', {'mylinks': mylinks})
	
#Пополнение баланса контекстной ссылки
@login_required	
def popolnit_contlinks(request, pk):
	serf = get_object_or_404(Contlinks, pk=pk)
	silka = Contlinks.objects.get(id=pk)
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_reklam
	if request.method == "POST":	
		sum = PopolnitContlinksForm(request.POST)#, instance=post)
		if sum.is_valid():
			#Получаю введеное кол-во дней и проверяю хватает ли на рекламном счету
			click = sum.cleaned_data['click']
			if click <= 99:
				messages.add_message(request, messages.ERROR, 'Введено не вернае количество кликов. Минимум 100 		кликов')
				return redirect('mycontlinks')
			else:
				money = click * 0.3
				if money <= schet:
					#Добовляю сумму и обнавляю форму
					post = sum.save(commit=False)
					price_link = silka.price_link + money
					post.id = silka.id
					post.user = request.user
					post.price_link = price_link
					post.save(update_fields=['price_link'])
					#Вычитаю сумму с рекламного счета
					pshet = UserInfo()
					schet = schet - money
					pshet.schet_reklam = schet
					pshet.user = request.user
					pshet.id = request.user.id
					pshet.save(update_fields=['schet_reklam'])
					messages.add_message(request, messages.ERROR, 'Баланс ссылки пополнен.')
					#Обновление баланса сайта
					site_shet = Balans.objects.get(id=1)
					site_shet.schet_site += money
					site_shet.id = 1
					site_shet.save(update_fields=['schet_site'])
					return redirect('mycontlinks')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на рекламном счету. Пополните счет.')
					return redirect('mycontlinks')
	else:
		form = PopolnitContlinksForm()
	return render(request, 'serfing/popolnit_contlinks.html', {'silka': silka, 'form': form})
	
#Все контекстные ссылки для пользователей	
'''def cotnlinksall(request):
	#user = request.user.id
	#today = datetime.today()
	#Вывожу  контекстные ссылки исключая с нул балансом и посещеные
	#userinfo = Serf.objects.filter(odobren = 1).exclude(price_serf = 0, 
											#serfusers__user = user, serfusers__pub_date__gte=	today.date())
	#Вывожу псевдо ссылки исключая с нул балансом										
	contlinks = Contlinks.objects.filter(odobren = 1).exclude(price_link = 0)
	return render(request, 'serfing/serf.html', {'contlinks': contlinks})'''
	
	
# ########################### Чтение писем #################################### #

#Функция расчта стоимости письма
def func_pismo(time, tech, vid, perehod, porating, posex):
	#Цена письма
	price = 0.09 
	#Узнаю время для таймера и стоимость доп. %	
	if time == "20":
		potimer = price
		p_s = 0
		p_u = price	
	elif time == "30":
		potimer = price + 0.004
		p_s = 0.004 / 2
		p_u = price + (0.004 / 2)
	elif time == "40":
		potimer = price + 0.008
		p_s = 0.008 / 2
		p_u = price + (0.008 / 2)
	elif time == "50":
		potimer = price + 0.012
		p_s = 0.012 / 2
		p_u = price + (0.012 / 2)
	elif time == "60":
		potimer = price + 0.016
		p_s = 0.016 / 2
		p_u = price + (0.016 / 2)
		
	#Узнаю показ писем
	if tech == "24_h":
		tech = 0
	elif tech == "1_m":
		tech = 0.02 / 2
		
	#Узнаю выделение письма
	if vid == "NO":
		vid = 0
	elif vid == "YES":
		vid = 0.01 / 2
		
	#Узнаю заказан переход насайт или нет
	if perehod == "NO":
		perehod = 0
	elif perehod == "YES":
		perehod = 0.015 / 2
		
	#Узнаю заказан рейтинг или нет
	if porating == "VSEPOL":
		porating = 0
	else:
		porating = 0.02 / 2
		
	#Узанаю заказан половой признак пользоватеей
	if posex == "VSEPOLZ":
		posex = 0
	else:
		posex = 0.01 / 2
	
	#Считаю сумму для вычита из баланса задания
	price_site = potimer + tech * 2 + vid * 2 + perehod  * 2 + porating * 2 + posex * 2
	#Считаю сумму для сайта	
	price_s = p_s + tech + vid + perehod + porating + posex
	#Считаю сумму для пользователя
	price_u = p_u + tech + vid + perehod + porating + posex
	a = {'price_site': price_site, 'price_s': price_s, 'price_u': price_u}
	return a

#Функция просмотров осталось
def prosm_ost_pismo(pk):
	silka = Pismo.objects.get(id=pk)
	silka.prosm_ost = silka.price_pismo // silka.price_t
	silka.spis = 0
	silka.save(update_fields=['prosm_ost', 'spis'])	
	
#Добовление письма
@login_required
def addpismo(request):
	user = request.user.id
	if request.method == "POST":
		form = PismoForm(request.POST)
		if form.is_valid():
			tech = form.cleaned_data['tech']
			time = form.cleaned_data['time']
			vid = form.cleaned_data['vid']
			perehod = form.cleaned_data['perehod']
			porating = form.cleaned_data['porating']
			posex = form.cleaned_data['posex']
			var_one = form.cleaned_data['var_one']
			if var_one < 1 or var_one > 3:
				messages.add_message(request, messages.ERROR, 'Не верен номер ответа.')
				#return redirect('addpismo')
			else:
				#Вызов функции обработки стоимости
				a = func_pismo(time, tech, vid, perehod, porating, posex)
				#Сахроняю форму
				post = form.save(commit=False)
				post.user = request.user
				post.price_u = a['price_u']
				post.price_s = a['price_s']
				post.price_t = a['price_site']
				post.save()
				messages.success(request, 'Добавленно')
				return redirect('mypismo')
	else:
		form = PismoForm()
	return render(request, 'serfing/addpismo.html', {'form': form})

#Редактирование письма
@login_required
def edit_pismo(request, pk):
	post = get_object_or_404(Pismo, pk=pk)
	users = request.user.id
	use = str(users)
	if request.method == "POST":
		form = PismoForm(data=request.POST, instance=post)
		if form.is_valid():
			tech = form.cleaned_data['tech']
			time = form.cleaned_data['time']
			vid = form.cleaned_data['vid']
			perehod  = form.cleaned_data['perehod']
			porating  = form.cleaned_data['porating']
			posex  = form.cleaned_data['posex']
			var_one = form.cleaned_data['var_one']
			if var_one < 1 or var_one > 3:
				messages.add_message(request, messages.ERROR, 'Не верен номер ответа.')
				return redirect('mypismo')
			else:
				#Вызов функции обработки стоимости
				a = func_pismo(time, tech, vid, perehod, porating, posex)
				post = form.save(commit=False)
				post.price_u = a['price_u']
				post.price_s = a['price_s']
				post.price_t = a['price_site']
				post.moder = 0
				post.odobren = 0
				post.save()
				#Высчитываю остаток просмотров
				prosm_ost_pismo(pk)
				return redirect('mypismo')			
	else:
		#Запрет редактирования чужого письма.
		p = Pismo.objects.get(id = pk)
		if  users == p.user_id:
			form = PismoForm(instance=post)
		else:
			return redirect('mypismo')
	return render(request, 'serfing/editpismo.html', {'form': form})

#Удаление письма
@login_required
def delete_pismo(request, pk):
	post = get_object_or_404(Pismo, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Pismo.objects.get(id = pk, user = user)
		money = post.price_pismo
		post.delete()
		#Возвращаю деньги на рекламный счет
		pshet = UserInfo.objects.get(user_id = user)
		pshet.schet_reklam += money
		pshet.save(update_fields=['schet_reklam'])
		return redirect('mypismo')			
	return render(request, 'serfing/deletepismo.html', {'task': pk})

#Отправка на модерацию письмо
@login_required
def moder_pismo(request, pk):
	post = get_object_or_404(Pismo, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Pismo.objects.get(id = pk, user = user)
		post.moder = 1
		post.odobren = 0
		post.save(update_fields=['moder', 'odobren'])
		return redirect('mypismo')			
	return render(request, 'serfing/moder_pismo.html', {'task': pk})

#Пауза паказа письма
@login_required
def pausa_pismo(request, pk):
	post = get_object_or_404(Pismo, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Pismo.objects.get(id = pk, user = user)
		post.pausa = 1
		post.save(update_fields=['pausa'])
		return redirect('mypismo')			
	return render(request, 'serfing/pausa_pismo.html', {'task': pk})

#Старт паказа письма
@login_required
def start_pismo(request, pk):
	post = get_object_or_404(Pismo, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Pismo.objects.get(id = pk, user = user)
		post.pausa = 0
		post.save(update_fields=['pausa'])
		return redirect('mypismo')			
	return render(request, 'serfing/start_pismo.html', {'task': pk})

#Все дабавленые письма для рекламодателя
@login_required
def mypismo(request):
	user = request.user.id
	myserf = Pismo.objects.filter(user_id=user)
	return render(request, 'serfing/mypismo.html', {'myserf': myserf})

#Пополнение баланса письма
@login_required	
def popolnit_pismo(request, pk):
	serf = get_object_or_404(Pismo, pk=pk)
	silka = Pismo.objects.get(id=pk)
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_reklam
	if request.method == "POST":	
		sum = PopolnitPismoForm(request.POST)
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на рекламном счету
			money = sum.cleaned_data['price_pismo']
			if money < 11:
				messages.add_message(request, messages.ERROR, 'Минимум 11 рублей.')
				return redirect('mypismo')
			else:
				if money <= schet:
					#Добовляю сумму и обнавляю форму
					post = sum.save(commit=False)
					price_pismo = silka.price_pismo + money
					post.id = silka.id
					post.user = request.user
					post.price_pismo = price_pismo
					#Сумма для списания с 11 руб.
					post.spis = 0
					sum_spis = money // 11
					post.sum_spis = silka.sum_spis + sum_spis
					post.save(update_fields=['price_pismo', 'sum_spis', 'spis'])
					#Функция просмотров осталось
					prosm_ost_pismo(pk)
					#Вычитаю сумму с рекламного счета
					pshet = UserInfo()
					schet = schet - money
					pshet.schet_reklam = schet
					pshet.user = request.user
					pshet.id = request.user.id
					pshet.save(update_fields=['schet_reklam'])
					messages.add_message(request, messages.ERROR, 'Баланс ссылки пополнен.')
					return redirect('mypismo')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на рекламном счету. Пополните счет.')
					return redirect('mypismo')
	else:
		form = PopolnitPismoForm()
	return render(request, 'serfing/popolnit_pismo.html', {'silka': silka, 'form': form})

#Все письма для пользователей	
@login_required
def pismoall(request):
	user = request.user.id
	today = datetime.today()
	#Вывожу ссылки серфинга исключая с нул балансом и посещеные
	#userinfo = Serf.objects.filter(odobren = 1, moder = 1, pausa = 0).exclude(price_serf__lt = 1).exclude(user__serf_user = user, user__pub_date__gte = today.date())
	userinfo = Pismo.objects.filter(odobren = 1, moder = 1, pausa = 0).exclude(price_pismo__lt = 1)#.exclude(serfusers__user = user, serfusers__pub_date__gte = today.date())
	return render(request, 'serfing/pismo.html', {'userinfo': userinfo})

#Все письма для пользователей	
@login_required
def pismo_otv(request, pk):
	pismo = get_object_or_404(Pismo, pk=pk)
	user = request.user
	today = datetime.today()
	#Исключение если письмо сегодня посещено ридерект
	try:
		PismoUsers.objects.get(user = user, pismo_user = pismo, pub_date__gte=date.today())
		return redirect('pismoall')
	except:
		CRITICAL = 50
	pismo2 = Pismo.objects.get(id = pk)
	if request.POST:
		#Проверяю какой вариант выбран
		if 'one' in request.POST:
			if pismo.var_one == 1:
				return redirect('/serfing/frame_pismo/{}/'.format(pk))
			else:
				messages.add_message(request, CRITICAL, 'Ответ не верен!')
				return redirect('pismoall')
		elif 'two' in request.POST:
			if pismo.var_one == 2:
				return redirect('/serfing/frame_pismo/{}/'.format(pk))
			else:
				messages.add_message(request, CRITICAL, 'Ответ не верен!')
				return redirect('pismoall')
		elif 'three' in request.POST:
			if pismo.var_one == 3:
				return redirect('/serfing/frame_pismo/{}/'.format(pk))
			else:
				messages.add_message(request, CRITICAL, 'Ответ не верен!')
				return redirect('pismoall')
	return render(request, 'serfing/pismo_otv.html', {'pismo': pismo})

#Просмотр страницы письма
@login_required
def frame_pismo(request, pk):
	serf = get_object_or_404(Pismo, pk=pk)
	user = request.user
	today = datetime.today()
	#Исключение если сылка сегодня посещена ридерект
	try:
		PismoUsers.objects.get(user = user, pismo_user = serf, pub_date__gte=date.today())
		messages.add_message(request, CRITICAL, 'Сегодня Вы уже просматривали это письмо!')
		return redirect('pismoall')
	except:
		CRITICAL = 50
	
	#Узнаю время для таймера
	b = int(serf.time)
	#Узнаю баланс ссылки
	schet = serf.price_pismo
	schet = float(schet)
	#Считаю сумму для вычита из баланса задания
	price_site = float(serf.price_t)
    #Считаю сумму для сайта	
	price_s = float(serf.price_s)
	#Считаю сумму для пользователя
	price= float(serf.price_u)
    #price_r = 0
    #price_r2 = 0
	if request.method == "POST":
		#Проверю хватает ли денег на балансе задания
		if schet < price_site:
			messages.add_message(request, CRITICAL, 'Не достаточно денег на счету ссылки!')
			return redirect('pismoall')
		else:
			form = CaptchaPismoForm(request.POST)
			if form.is_valid():
				#Подтсверждение ответа				
				post = form.save(commit=False)
				#исключение если запись о посещении есть обновляю, если нет создаю новую
				try: 
					p = PismoUsers.objects.get(user = user, pismo_user = serf)
					post.pismo_user = serf
					post.odobren = 1
					post.pub_date = today.date()
					post.user = user	
                    #post.id = p.id
					post.save(update_fields=['pub_date'])
				except:
					post.pismo_user = serf
					post.odobren = 1
					post.pub_date = today.date()
					post.user = user	
				#post.id = user.id
					post.save()
				#Прибовляю деньги к личному счету пользователя + рейтинг
				pshet = UserInfo.objects.get(user = user)
				pshet.schet_lich += price
				pshet.rating += 0.01
				pshet.user = user
				pshet.id = user.id
				pshet.save()
				#Вычитаю деньги со счета ссылки
				tshet = Pismo.objects.get(id= serf.id)
				#Списание с каждых 11 руб. 1руб.
				pr = 0
				prosm = 0
				if tshet.spis == 0:
					pr = tshet.sum_spis
					prosm = pr // tshet.price_t
					tshet.prosm += prosm
					tshet.prosm_ost -= prosm					
					tshet.price_pismo = schet - (price_site + pr)
					tshet.sum_spis = 0
					tshet.spis = 1	
				else:
					schet = schet - price_site
					tshet.price_pismo = schet
					tshet.prosm += 1
					tshet.prosm_ost -= 1
				tshet.user = serf.user
				#tshet.id = request.user.id
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
				messages.add_message(request, CRITICAL, 'Ответ подтвержден.')
				return redirect('pismoall')
				#Обновляю статистику сайта			
				stat = Statistica.objects.get(id=1)
				stat.id = 1
				stat.click = (stat.click + 1) + prosm
				stat.save(update_fields=['click'])
				#Добовление стаистики пользователя
				stat_u = UserStatic.objects.get(user = user, pub_date = today.date())
				stat_u.pismo += 1
				stat_u.save()
				if serf.perehod == "NO":
					return redirect('serfall')
				elif serf.perehod == "YES":
					return redirect(serf.url)
	else:
		form = CaptchaPismoForm()
	return render(request, 'serfing/frame_pismo.html', {'form': form, 'serf': serf, 'b': b})

	
# ###############################Переходы на сайты ############################# #

#Добовление ссылки переходов
@login_required
def addperehod(request):
	user = request.user.id
	CRITICAL = 50
	if request.method == "POST":
		form = PerehodForm(request.POST)
		if form.is_valid():
			price = form.cleaned_data['price']
			price = float(price)
			time_r  = form.cleaned_data['time_r']
			perehod  = form.cleaned_data['perehod']
			porating  = form.cleaned_data['porating']
			posex  = form.cleaned_data['posex']
			#Вызов функции обработки стоимости
			a = func_link(price, time_r, perehod, porating, posex)
			#Сахроняю форму
			post = form.save(commit=False)
			post.user = request.user
			post.price_u = a['price_u']
			post.price_s = a['price_s']
			post.price_t = a['price_site']
			post.save()
			messages.success(request, 'Добавленно')
			return redirect('myperehod')
	else:
		form = PerehodForm()
	return render(request, 'serfing/addperehod.html', {'form': form})

#Редактировать ссылки
@login_required
def edit_perehod(request, pk):
	post = get_object_or_404(Perehod, pk=pk)
	users = request.user.id
	use = str(users)
	if request.method == "POST":
		form = PerehodForm(data=request.POST, instance=post)
		if form.is_valid():
			price = form.cleaned_data['price']
			price = float(price)
			time_r  = form.cleaned_data['time_r']
			perehod  = form.cleaned_data['perehod']
			porating  = form.cleaned_data['porating']
			posex  = form.cleaned_data['posex']
			#Вызов функции обработки стоимости
			a = func_link(price, time_r, perehod, porating, posex)
			post = form.save(commit=False)
			post.price_u = a['price_u']
			post.price_s = a['price_s']
			post.price_t = a['price_site']
			post.moder = 0
			post.odobren = 0
			post.save()
			#Высчитываю остаток просмотров
			prosm_ost_perehod(pk)
			return redirect('myperehod')			
	else:
		#Запрет редактирования чужого задания.
		p = Perehod.objects.get(id = pk)
		if  users == p.user_id:
			form = PerehodForm(instance=post)
		else:
			return redirect('myperehod')
	return render(request, 'serfing/editperehod.html', {'form': form})

#Удаление ссылки
@login_required
def delete_perehod(request, pk):
	post = get_object_or_404(Perehod, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Perehod.objects.get(id = pk, user = user)
		money = post.price_serf
		post.delete()
		#Возвращаю деньги на рекламный счет
		pshet = UserInfo.objects.get(user_id = user)
		pshet.schet_reklam += money
		pshet.save(update_fields=['schet_reklam'])
		return redirect('myperehod')			
	return render(request, 'serfing/deleteperehod.html', {'task': pk})

#Отправка на модерацию ссылку
@login_required
def moder_perehod(request, pk):
	post = get_object_or_404(Perehod, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Perehod.objects.get(id = pk, user = user)
		post.moder = 1
		post.odobren = 0
		post.save(update_fields=['moder', 'odobren'])
		return redirect('myperehod')			
	return render(request, 'serfing/moder_perehod.html', {'task': pk})

#Пауза ссылки
@login_required
def pausa_perehod(request, pk):
	post = get_object_or_404(Perehod, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Perehod.objects.get(id = pk, user = user)
		post.pausa = 1
		post.save(update_fields=['pausa'])
		return redirect('myperehod')			
	return render(request, 'serfing/pausa_perehod.html', {'task': pk})

#Старт ссылки
@login_required
def start_perehod(request, pk):
	post = get_object_or_404(Perehod, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Perehod.objects.get(id = pk, user = user)
		post.pausa = 0
		post.save(update_fields=['pausa'])
		return redirect('myperehod')			
	return render(request, 'serfing/start_perehod.html', {'task': pk})
	
#Все дабавленые ссылки для рекламодателя
@login_required
def myperehod(request):
	user = request.user.id
	myserf = Perehod.objects.filter(user_id=user)
	return render(request, 'serfing/myperehod.html', {'myserf': myserf})

#Функция просмотров осталось
def prosm_ost_perehod(pk):
	silka = Perehod.objects.get(id=pk)
	silka.prosm_ost = silka.price_serf // silka.price_t
	silka.spis = 0
	silka.save(update_fields=['prosm_ost', 'spis'])

#Пополнение баланса ссылки
@login_required	
def popolnit_perehod(request, pk):
	serf = get_object_or_404(Perehod, pk=pk)
	silka = Perehod.objects.get(id=pk)
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_reklam
	if request.method == "POST":	
		sum = PopolnitPerehodForm(request.POST)
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на рекламном счету
			money = sum.cleaned_data['price_serf']
			if money < 11:
				messages.add_message(request, messages.ERROR, 'Минимум 11 рублей.')
				return redirect('myperehod')
			else:
				if money <= schet:
					#Добовляю сумму и обнавляю форму
					post = sum.save(commit=False)
					price_serf = silka.price_serf + money
					post.id = silka.id
					post.user = request.user
					post.price_serf = price_serf
					#Сумма для списания с 11 руб.
					post.spis = 0
					sum_spis = money // 11
					post.sum_spis = silka.sum_spis + sum_spis
					post.save(update_fields=['price_serf', 'sum_spis', 'spis'])
					#Функция просмотров осталось
					prosm_ost_perehod(pk)
					#Вычитаю сумму с рекламного счета
					pshet = UserInfo()
					schet = schet - money
					pshet.schet_reklam = schet
					pshet.user = request.user
					pshet.id = request.user.id
					pshet.save(update_fields=['schet_reklam'])
					messages.add_message(request, messages.ERROR, 'Баланс ссылки пополнен.')
					return redirect('myperehod')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на рекламном счету. Пополните счет.')
					return redirect('myperehod')
	else:
		form = PopolnitPerehodForm()
	return render(request, 'serfing/popolnit_perehod.html', {'silka': silka, 'form': form})
	
	
	
#Все ссылки переходов на сайт для пользователей	
@login_required
def perehodall(request):
	user = request.user.id
	today = datetime.today()
	#Вывожу ссылки серфинга исключая с нул балансом и посещеные
	#userinfo = Serf.objects.filter(odobren = 1, moder = 1, pausa = 0).exclude(price_serf__lt = 1).exclude(user__serf_user = user, user__pub_date__gte = today.date())
	userinfo = Perehod.objects.filter(odobren = 1, moder = 1, pausa = 0).exclude(price_serf__lt = 1)#.exclude(serfusers__user = user, serfusers__pub_date__gte = today.date())
	#Вывожу псевдо ссылки исключая с нул балансом										
	plinks = Plinks.objects.filter(odobren = 1).exclude(price_link = 0)
	return render(request, 'serfing/perehod.html', {'userinfo': userinfo, 'plinks': plinks, 'usl': user})


#После завершения таймера переходов на сайт
@csrf_exempt
@login_required
def frame_perehod1(request):
	if request.is_ajax():
		if request.method == "POST":
			pk = request.POST.get('pk')
			pk = int(pk)
			user = request.POST.get('user')
			serf = Perehod.objects.get(id = pk)
			su = serf.id
			#user = request.user
			today = datetime.today()
			#Исключение если сылка сегодня посещена ридерект
			try:
				PerehodUsers.objects.get(user_id = user, perehod_user_id = su, pub_date__gte=date.today())
				price = 'Сегодня посещали'
				return HttpResponse(price)
			except:
				CRITICAL = 50
			
			#Узнаю время для таймера
			b = int(serf.time_r)
			#Узнаю баланс ссылки
			schet = serf.price_serf
			schet = float(schet)
			#Считаю сумму для вычита из баланса задания
			price_site = float(serf.price_t)
			#Считаю сумму для сайта	
			price_s = float(serf.price_s)
			#Считаю сумму для пользователя
			price= float(serf.price_u)

			#Проверю хватает ли денег на балансе задания
			if schet < price_site:
				return HttpResponse('Не достаточно денег на счету ссылки!')
			else:
				#Подтсверждение ответа				
				#исключение если запись о посещении есть обновляю, если нет создаю новую
				
				try: 
					p = PerehodUsers.objects.get(user_id = user, perehod_user_id = su)
					p.perehod_user = serf
					p.odobren = 1
					p.pub_date = today.date()
					p.user_id = user	
                    #post.id = p.id
					p.save(update_fields=['pub_date'])
				except:
					p = PerehodUsers()
					p.perehod_user = serf
					p.odobren = 1
					p.pub_date = today.date()
					p.user_id = user	
				#post.id = user.id
					p.save()
				#Прибовляю деньги к личному счету пользователя + рейтинг
				pshet = UserInfo.objects.get(user = user)
				pshet.schet_lich += price
				pshet.rating += 0.01
				pshet.user_id = user
				#pshet.id = user.id
				pshet.save()
				#Вычитаю деньги со счета ссылки
				tshet = Perehod.objects.get(id= serf.id)
				#Списание с каждых 11 руб. 1руб.
				pr = 0
				prosm = 0
				if tshet.spis == 0:
					pr = tshet.sum_spis
					prosm = pr // tshet.price_t
					tshet.prosm += prosm
					tshet.prosm_ost -= prosm					
					tshet.price_serf = schet - (price_site + pr)
					tshet.sum_spis = 0
					tshet.spis = 1	
				else:
					schet = schet - price_site
					tshet.price_serf = schet
					tshet.prosm += 1
					tshet.prosm_ost -= 1
				tshet.user = serf.user
				#tshet.id = request.user.id
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
				stat.click = (stat.click + 1) + prosm
				stat.save(update_fields=['click'])
				#Добовление стаистики пользователя
				stat_u = UserStatic.objects.get(user = user, pub_date = today.date())
				stat_u.serf += 1
				stat_u.save()
				return HttpResponse(price)
	#return render(request, 'serfing/perehod.html', {'serf': serf, 'b': b})
	
#Ajax запрос на время таймера
@csrf_exempt
@login_required
def frame_perehod(request):
	user = request.user
	today = datetime.today()
	#b = int(serf.time_r)
	#b = '20'
	if request.is_ajax():
		if request.method == "POST":
			if 'pk' in  request.POST:
				pk = request.POST.get('pk')
				pk = int(pk)
				serf = Perehod.objects.get(id = pk)
				b = int(serf.time_r)
				return HttpResponse(b)
			else:
				b = 10
				return HttpResponse(b)
		else:
			#return render(request, 'serfing/perehod.html', {'userinfo': userinfo, 'plinks': plinks, 'b': b})
			serf = pk
			return HttpResponse(b)
	#return render(request, 'serfing/perehod.html', {'b': b})


