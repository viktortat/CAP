# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MyMailForm
from .models import MyMail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profuser.models import UserInfo
	
#Полученые  лс
@login_required
def mymail(request):
	users = request.user
	user = UserInfo.objects.get(user = users)
	#Выбираю все входящие по убыванию, по дате
	mail = MyMail.objects.filter(recipient = user, delete_two = 0).order_by('-pub_date')
	#mail_count = len(mail)
	return render(request, 'mail/mymail.html', {'mail': mail})

#Отправленые лс
@login_required
def otmail(request):	
	user = request.user.id
	mail = MyMail.objects.filter(sender = user, delete_one = 0).order_by('-pub_date')
	return render(request, 'mail/otmail.html', {'mail': mail})

#Полное полученное лс
@login_required
def detail_mail(request, pk):		
	m = get_object_or_404(MyMail, pk=pk)
	users = request.user
	user = UserInfo.objects.get(user = users)	
	mail = MyMail.objects.get(recipient = user, id = pk, delete_two = 0)
	if mail:
		mm = mail.sender
		user_send = User.objects.get(username = mm)
		if mail.read == 0:
			mail.read = 1
			mail.save(update_fields=['read'])
	#Удаление сообщения
	if request.method == "POST":
		mail_d = MyMail.objects.get(recipient = user, id = pk, delete_two = 0)
		mail_d.delete_two = 1
		mail_d.save(update_fields=['delete_two'])
		return redirect('mymail')	
	return render(request, 'mail/detail-mail.html', {'mail': mail, 'send': user_send})
	
#Полное отправленное лс
@login_required
def detail_otmail(request, pk):		
	m = get_object_or_404(MyMail, pk=pk)
	users = request.user
	user = UserInfo.objects.get(user = users)	
	mail = MyMail.objects.filter(sender= user, id = pk, delete_one = 0)
	if mail:
		for m in mail:
			mm = m.recipient
		user_rec = User.objects.get(username = mm)
	#Удаление сообщения
	if request.method == "POST":
		mail_d = MyMail.objects.get(sender = user, id = pk, delete_one = 0)
		mail_d.delete_one = 1
		mail_d.save(update_fields=['delete_one'])
		return redirect('otmail')	
	return render(request, 'mail/detail-otmail.html', {'mail': mail, 'rec': user_rec})
	
#Отправка лс
@login_required
def addmail(request):
	users = request.user
	user = UserInfo.objects.get(user = users)	
	if request.method == "POST":
		form = MyMailForm(request.POST)
		if form.is_valid():
			#Сахроняю форму
			post = form.save(commit=False)
			post.sender= user
			post.save()
			return redirect('otmail')
	else:
		form = MyMailForm()
	return render(request, 'mail/addmail.html', {'form': form})

#Удаление лс
@login_required
def delete_mail(request, pk):
	m = get_object_or_404(MyMail, pk=pk)
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