from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django import forms
from .models import Tasksa, TasksUsers
from django.contrib.auth.models import User
from .forms import TasksaForm, TasksUsersForm, OtvetTasksUsersForm, PopolnitForm, TasksSearchForm, SearchCenForm #TaskMailForm
from mail.forms import TaskMailForm
from mail.models import MyMail
from django.shortcuts import redirect
from django.contrib import messages
from profuser.models import UserInfo, Refery, UserStatic
from balanssite.models import Balans
from datetime import datetime, timedelta
from statis.models import Statistica
from django.http import HttpResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

#Добовление задания
@login_required
def addtasks(request):
	user = request.user.id
	CRITICAL = 50
	if request.method == "POST":
		form = TasksaForm(request.POST)#, instance=post)
		if form.is_valid():
			#Цены
			price = form.cleaned_data['price']
			#Проверка на ввод 0 и отрицательного числа
			if price <= 0:
				messages.add_message(request, CRITICAL, 'Введен отрицательный денежный баланс.')
				return redirect('addtasks')
			else:
				#Сахроняю форму
				post = form.save(commit=False)
				post.price = price
				post.user = request.user
				post.save()
				return redirect('mytasks')
	else:
		form = TasksaForm()
	return render(request, 'tasks/addtasks.html', {'form': form})

#Редактировать задание
@login_required
def edit_task(request, pk):
	post = get_object_or_404(Tasksa, pk=pk)
	users = request.user.id
	use = str(users)
	if request.method == "POST":
		form = TasksaForm(data=request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.moder = 0
			post.odobren = 0
			post.save()
			return redirect('mytasks')			
	else:
		#Запрет редактирования чужого задания.
		p = Tasksa.objects.get(id = pk)
		if  users == p.user_id:
			form = TasksaForm(instance=post)
		else:
			return redirect('mytasks')
	return render(request, 'tasks/edittask.html', {'form': form})

#Удаление задания
@login_required
def delete_task(request, pk):
	post = get_object_or_404(Tasksa, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Tasksa.objects.get(id = pk, user = user)
		money = post.price_task
		post.delete()
		#Возвращаю деньги на рекламный счет
		pshet = UserInfo.objects.get(user_id = user)
		pshet.schet_reklam += money
		pshet.save(update_fields=['schet_reklam'])
		return redirect('mytasks')			
	return render(request, 'tasks/deletetask.html', {'task': pk})

#Отправка на модерацию задания
@login_required
def moder_task(request, pk):
	post = get_object_or_404(Tasksa, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Tasksa.objects.get(id = pk, user = user)
		post.moder = 1
		post.odobren = 0
		post.save(update_fields=['moder', 'odobren'])
		return redirect('mytasks')			
	return render(request, 'tasks/moder_task.html', {'task': pk})

#Пауза задания
@login_required
def pausa_task(request, pk):
	post = get_object_or_404(Tasksa, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Tasksa.objects.get(id = pk, user = user)
		post.pausa = 1
		post.save(update_fields=['pausa'])
		return redirect('mytasks')			
	return render(request, 'tasks/p_task.html', {'task': pk})

#Старт задания
@login_required
def s_task(request, pk):
	post = get_object_or_404(Tasksa, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = Tasksa.objects.get(id = pk, user = user)
		post.pausa = 0
		post.save(update_fields=['pausa'])
		return redirect('mytasks')			
	return render(request, 'tasks/s_task.html', {'task': pk})
	
#Все задания
@login_required
def tasksall(request):
	user = request.user.id
	#Вывожу повторяемые задания			
	task_mnogo = Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'mnogo', pausa = 0).exclude(price_task__lt = 1)
	user_task = TasksUsers.objects.filter(otvet_user = user)
	#Вывожу задания с одноразовым выполнением исключая если есть ответ пользователя
	task_one = Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'one', pausa = 0).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
	form = TasksSearchForm()
	cenform = SearchCenForm()
	return render(request, 'tasks/tasks.html', {'task_one': task_one, 'task_mnogo': task_mnogo, 'form': form, 'cenform': cenform})

#Категория задания
@login_required
def taskscat(request, pk):
	user = request.user.id
	today = datetime.now()
	today = today.strftime("%Y-%m-%d")
	user_task = TasksUsers.objects.filter(otvet_user = user)
	if request.method == "POST":
		#Поиск по форме
		form = TasksSearchForm(request.POST)
		if form.is_valid():
			sel = form.cleaned_data['sel']
			char = form.cleaned_data['char']
			if sel == '0':
				task_mnogo = Tasksa.objects.filter(id = char, odobren = 1, moder = 1, tech = 'mnogo', pausa = 0).exclude(price_task__lt = 1)
				task_one = Tasksa.objects.filter(id = char, odobren = 1, moder = 1, tech = 'one', pausa = 0).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
			if sel == '1':
				task_mnogo = Tasksa.objects.filter(title = char, odobren = 1, moder = 1, tech = 'mnogo', pausa = 0).exclude(price_task__lt = 1)
				task_one = Tasksa.objects.filter(title = char, odobren = 1, moder = 1, tech = 'one', pausa = 0).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
			if sel == '2':
				task_mnogo = Tasksa.objects.filter(user__username = char, odobren = 1, moder = 1, tech = 'mnogo', pausa = 0).exclude(price_task__lt = 1)
				task_one = Tasksa.objects.filter(user__username = char, odobren = 1, moder = 1, tech = 'one', pausa = 0).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
			if sel == '3':
				task_mnogo = Tasksa.objects.filter(url_admin = char, odobren = 1, moder = 1, tech = 'mnogo', pausa = 0).exclude(price_task__lt = 1)
				task_one = Tasksa.objects.filter(url_admin = char, odobren = 1, moder = 1, tech = 'one', pausa = 0).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
			form = TasksSearchForm()
			cenform = SearchCenForm()			
			return render(request, 'tasks/tasks.html', {'task_one': task_one, 'task_mnogo': task_mnogo, 'today': today, 'form': form, 'cenform': cenform})	
		#Поиск по форме цены	
		cenform = SearchCenForm(request.POST)
		if cenform.is_valid():
			cen = cenform.cleaned_data['cen']
			cen = float(cen)
			task_mnogo = Tasksa.objects.filter(price__gte = cen, odobren = 1, moder = 1, tech = 'mnogo', pausa = 0).exclude(price_task__lt = 1)
			task_one = Tasksa.objects.filter(price__gte = cen, odobren = 1, moder = 1, tech = 'one', pausa = 0).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
			form = TasksSearchForm()
			cenform = SearchCenForm()			
			return render(request, 'tasks/tasks.html', {'task_one': task_one, 'task_mnogo': task_mnogo, 'today': today, 'form': form, 'cenform': cenform})
	else:
		#Одноразовые и многораовые задания
		if pk == '10':
			task_mnogo = Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'mnogo', pausa = 0).exclude(price_task__lt = 1)
			task_one = ""
		elif pk == '11':
			task_mnogo = ""
			task_one = Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'one', pausa = 0).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
		elif pk == '12':
			#Новые задания
			task_mnogo = Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'mnogo', pub_date__gte = today, pausa = 0).exclude(price_task__lt = 1)
			task_one = Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'one', pub_date__gte = today).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
		elif pk == '13':
			#Новые задания
			task_mnogo =""# Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'mnogo').order_by('price')
			task_one = Tasksa.objects.filter(odobren = 1, moder = 1, pausa = 0).order_by('-price').exclude(price_task__lt = 1)#.exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).order_by('price')
		else:
			#Вывожу задания по категориям
			task_mnogo = Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'mnogo', cat = pk, pausa = 0).exclude(price_task__lt = 1)
			#Вывожу задания с одноразовым выполнением исключая если есть ответ пользователя
			task_one = Tasksa.objects.filter(odobren = 1, moder = 1, tech = 'one', cat = pk, pausa = 0).exclude(tasksusers__otvet_user= user, tasksusers__proverka = 1, tasksusers__odobren = 1).exclude(price_task__lt = 1)
		form = TasksSearchForm()
		cenform = SearchCenForm()
	return render(request, 'tasks/tasks.html', {'task_one': task_one, 'task_mnogo': task_mnogo, 'today': today, 'form': form, 'cenform': cenform})
	
#Подробнее о задании и ответ на него	
@login_required	
def tasks_detail(request, pk):
	task = get_object_or_404(Tasksa, pk=pk)
	user = request.user
	a = datetime.now()
	a = a.strftime('%Y-%m-%d %H:%M:%S')
	#Вибираю текущей ответ на задание
	task_s = TasksUsers.objects.filter(otvet_user = user, taskuser = pk)
	for id_s in task_s:
		id = id_s.id
	#Сохраняю ответ
	if request.method == "POST":
		otvet = TasksUsersForm(request.POST)#, instance=post)
		if otvet.is_valid():
			post = otvet.save(commit=False)
			post.taskuser = Tasksa.objects.get(id=pk)
			post.otvet_user = user
			post.id = id
			post.start_task = datetime.now()
			#Записываю проверку для многократных заданий
			post.proverka = 1
			post.odobren = 0
			post.otvet_task = 2
			post.save(update_fields=['proverka', 'us_opis_vipoln', 'odobren', 'otvet_task'])
			messages.add_message(request, messages.ERROR, 'Ответ отправлен. Ждите проверку.')
			return redirect('tasksall')
	else:	
		otvet = TasksUsersForm()
	return render(request, 'tasks/tasks_detail.html', {'task': task, 'otvet': otvet, 'task_s': task_s, 'a': a})

#Старт задания
@login_required	
def start_task(request, pk):
	task = get_object_or_404(Tasksa, pk=pk)
	#Устанавливаю срок выполнения задания
	a = datetime.now()
	
	if task.srock == "one_h":
		b = timedelta(hours=1)
	elif task.srock == "two_h":
		b = timedelta(hours=2)
	elif task.srock == "six_h":
		b = timedelta(hours=6)
	elif task.srock == "tvel_h":
		b = timedelta(hours=12)
	elif task.srock == "one_d":
		b = timedelta(hours=24)
	elif task.srock == "two_d":
		b = timedelta(hours=48)
	elif task.srock == "three_d":
		b = timedelta(hours=72)
	elif task.srock == "five_d'":
		b = timedelta(days=5)
	task_i = a + b
	
	user = request.user
	#Сохраняю ответ с датой окончания задания
	if request.method == "POST":
		otvet = request.POST
		post = TasksUsers()
		post.taskuser = Tasksa.objects.get(id=pk)
		post.start_task = task_i
		post.otvet_user = user
		post.otvet_task = 1
		post.save()
		messages.add_message(request, messages.ERROR, 'Вы начали задание.')
		return redirect('/tasks/tasks/{}' .format(pk))

	return render(request, 'tasks/tasks_detail.html', {'task_i': task_i})


#Все дабавленые задания для рекламодателя
@csrf_exempt
@login_required
def mytasks(request):
	user = request.user.id
	mytasks = Tasksa.objects.filter(user_id=user)
	otvet = TasksUsers.objects.filter(taskuser__user = user)
			
	return render(request, 'tasks/mytasks.html', {'mytasks': mytasks, 'otvet': otvet})

#Ответы на задания рекламодателя
@login_required	
def otvet_task(request, pk):
	otvet = TasksUsers.objects.filter(taskuser=pk).filter(odobren = 0, otvet_task = 2)
	return render(request, 'tasks/otvet_tasks.html', {'otvet': otvet, 'pk':pk})

#Удаление ответа
@login_required
def otvet_delete(request, pk):
	post = get_object_or_404(TasksUsers, pk=pk)
	user = request.user.id
	if request.method == "POST":
		post = TasksUsers.objects.get(id = pk, taskuser__user=user)
		post.delete()
		return redirect('mytasks')			
	return render(request, 'tasks/delete_otvet.html', {'task': pk})
	
#Подробние ответ на задание и его подтверждение
@login_required	
def otvet_detail(request, pk):
	#task = get_object_or_404(TasksUsers, pk=pk)
	today = datetime.today()
	CRITICAL = 50
	user = request.user
	otvet = get_object_or_404(TasksUsers, pk=pk)
	#Получаю полный ответ
	kto = TasksUsers.objects.get(id=pk)
	#Узнаю баланс задания
	id = kto.taskuser
	s = Tasksa.objects.get(id= kto.taskuser.id)
	schet = s.price_task
	schet = float(schet)
	#Узнаю цену задания 
	price = s.price
	#Считаю процент сайта
	schet_site = price * 0.25
	
	#Считаю процент  вычита со счета задания	
	price_t = price + (price * 0.25)
	if request.method == "POST":
		#Проверю хватает ли денег на балансе задания
		if schet < price_t:
			messages.add_message(request, CRITICAL, 'Не достаточно денег на счету задания! Пополните пожулуйста счет.')
			return redirect('mytasks')
		else:
			form = OtvetTasksUsersForm(request.POST)
			if form.is_valid():
				#Подтсверждение ответа
				post = form.save(commit=False)
				post.otvet_user = kto.otvet_user
				post.taskuser = kto.taskuser
				post.id = kto.id			
				#Проверка сколько раз можно выполнять задание
				if s.tech == 'MNOGO':
					post.proverka = 0
					post.odobren = 1
					post.otvet_task = 3
				else:
					post.proverka = 1
					post.odobren = 1
					post.otvet_task = 3
				post.save(update_fields=['odobren', 'proverka', 'otvet_task'])
				#Прибовляю деньги к личному счету пользователя + рейтинг
				pshet = UserInfo.objects.get(user = kto.otvet_user)
				pshet.schet_lich += price
				pshet.rating += 0.5
				pshet.user = kto.otvet_user
				pshet.id = kto.otvet_user.id
				pshet.save()
				#Вычитаю деньги со счета задания
				tshet = Tasksa.objects.get(id= kto.taskuser.id)
				schet = schet - price_t
				tshet.price_task = schet
				tshet.user = request.user
				#tshet.id = request.user.id
				tshet.save()
				#Обновляю статистику сайта			
				stat = Statistica.objects.get(id=1)
				stat.id = 1
				stat.task = stat.task + 1
				stat.save(update_fields=['task'])
				messages.add_message(request, CRITICAL, 'Ответ подтвержден.')
				#Считаю процент  рефери 1 уровень и вычитаю из баланса сайта
				refery = Refery.objects.get(user = kto.otvet_user)	
				if refery.one_lvl != 0:
					refery_one = UserInfo.objects.get(user = refery.one_lvl)
					if refery_one.rating < 300:
						price_refery = schet_site * 0.05
					elif refery_one.rating >= 300:
						price_refery = schet_site * 0.1
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
						if refery_two.rating < 300:
							price_refery2 = schet_site * 0.05
						elif refery_two.rating >= 300:
							price_refery2 = schet_site * 0.1
						elif refery_two.rating == 0:
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
						perechet = price_r + price_r2
					else:
						price_r2 = 0
				else:
					price_r = 0
					price_r2 = 0
				perechet = price_r + price_r2
				#Обновляю баланс сайта			
				site = Balans.objects.get(id=1)
				site.schet_site += schet_site - perechet
				site.id = 1
				site.save(update_fields=['schet_site'])
				#Добовление стаистики пользователя
				stat_u = UserStatic.objects.get(user = kto.otvet_user, pub_date = today.date())
				stat_u.task += 1
				stat_u.save()
				return redirect('/tasks/otvet_task/{}'.format(s.id))
	else:
		form = OtvetTasksUsersForm()
		com = TaskMailForm()
	return render(request, 'tasks/otvet_detail.html', {'form': form, 'otvet': otvet, 'com': com, 'pk': s.id})
	
#Дорабротка ответа задания	
@login_required	
def dor_otvet(request, pk):
	if request.method == "POST":
		form = TaskMailForm(request.POST)
		if form.is_valid:
			rec = TasksUsers.objects.get(id=pk)
			#Кто будет отпровлять
			user = UserInfo.objects.get(user = rec.taskuser_id)
			#Кому отправляем
			u = UserInfo.objects.get(id = rec.otvet_user_id)
			#Коментарий к доработки задания
			post = form.save(commit=False)
			post.title = "Коментарий к заданию № {}".format(rec.taskuser_id)
			post.sender = user
			post.recipient = u
			post.save()
			#Отправка задания на доработку
			otv = TasksUsers.objects.get(id=pk)
			otv.proverka = 0
			otv.odobren = 0
			otv.otvet_task = 1
			otv.save(update_fields=['odobren', 'proverka', 'otvet_task'])
			return redirect('/tasks/otvet_task/{}'.format(rec.taskuser_id))
			
#Пополнение баланса задания	
@login_required	
def popolnit_task(request, pk):
	task = get_object_or_404(Tasksa, pk=pk)
	zadanie = Tasksa.objects.get(id=pk)
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_reklam
	if request.method == "POST":	
		sum = PopolnitForm(request.POST)#, instance=post)
		if sum.is_valid():
			#Получаю введеную сумму и проверяю хватает ли на рекламном счету
			money = sum.cleaned_data['price_task']
			if money <= 0:
				messages.add_message(request, messages.ERROR, 'Введена не верная сумма.')
				return redirect('mytasks')
			else:
				if money <= schet:
					#Добовляю сумму и обнавляю форму
					post = sum.save(commit=False)
					price_task = zadanie.price_task + money
					post.id = zadanie.id
					post.user = request.user
					post.price_task = price_task
					post.save(update_fields=['price_task'])
					#Вычитаю сумму с рекламного счета
					pshet = UserInfo()
					schet = schet - money
					pshet.schet_reklam = schet
					pshet.user = request.user
					pshet.id = request.user.id
					pshet.save(update_fields=['schet_reklam'])
					messages.add_message(request, messages.ERROR, 'Баланс задания пополнен.')
					return redirect('mytasks')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на рекламном счету. Пополните счет.')
					return redirect('mytasks')
	else:
		form = PopolnitForm()
	return render(request, 'tasks/popolnit.html', {'task': task, 'form': form})