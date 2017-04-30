from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import auth
from django import forms
from .models import CatalogSite
from .forms import CatalogSiteForm, PopolnitCatalogForm
from profuser.models import UserInfo
from django.shortcuts import redirect
from django.contrib import messages
from balanssite.models import Balans

#Добовление сайта в каталог
@login_required
def addsite(request):
	#post = get_object_or_404(Tasksa, pk=pk)
	CRITICAL = 50
	#Получение id пользователя
	user = request.user.id
	
	#Получаю количество денег на рекламном счету
	for s in UserInfo.objects.filter(user_id = user):
		schet = s.schet_reklam
		
	#Узнаю цену
	for p in CatalogSite.objects.values('price'):
		price = p['price']
		
	if request.method == "POST":
		if schet < 20:
			messages.add_message(request, CRITICAL, 'Не достаточно денег на счету! Пополните пожулуйста счет.')#messages.success(request, 'Не достаточно денег на счету!')
			return redirect('addsite')
		else:
			form = CatalogSiteForm(request.POST)
			if form.is_valid():
			
				#Сахроняю форму
				post = form.save(commit=False)
				post.user = request.user
				post.save()
				return redirect('mycatalog')
	else:
		form = CatalogSiteForm()
	return render(request, 'catalog/addsite.html', {'form': form})
	
#Все ссылки в каталоге	
def siteall(request):
	user = request.user.id
	userinfo = CatalogSite.objects.filter(odobren = 1).exclude(price = 0)
	return render(request, 'catalog/site.html', {'userinfo': userinfo})

#Все дабавленые ссылки в каталог для рекламодателя
@login_required
def mycatalog(request):
	user = request.user.id
	mylinks = CatalogSite.objects.filter(user_id=user)
	return render(request, 'catalog/mycatalog.html', {'mylinks': mylinks})
	
#Пополнение баланса ссылки в каталоге
@login_required	
def popolnit_catalog(request, pk):
	serf = get_object_or_404(CatalogSite, pk=pk)
	silka = CatalogSite.objects.get(id=pk)
	#Получение id пользователя
	user = request.user.id
	#Получаю количество денег на рекламном счету
	s = UserInfo.objects.get(user_id = user)
	schet = s.schet_reklam
	#Проверяю выбрано ли выдиление ссылки
	if silka.dop == "NO":
		dop = 0
	elif silka.dop == "YES":
		dop = 5
		
	if request.method == "POST":	
		sum = PopolnitCatalogForm(request.POST)
		if sum.is_valid():
			#Получаю введеную сумму
			price = sum.cleaned_data['price']
			if price < 20:
				messages.add_message(request, messages.ERROR, 'Введено не верная сумма. Минимум 20 руб.')
				return redirect('mycatalog')
			else:
				price_c = price + dop
				if price_c <= schet:
					#Добовляю сумму и обнавляю форму
					post = sum.save(commit=False)
					price_link = silka.price + price_c
					post.id = silka.id
					post.user = request.user
					post.price = price_link
					post.save(update_fields=['price'])
					#Вычитаю сумму с рекламного счета
					pshet = UserInfo()
					schet = schet - price_c
					pshet.schet_reklam = schet
					pshet.user = request.user
					pshet.id = request.user.id
					pshet.save(update_fields=['schet_reklam'])					
					#Обновление баланса сайта
					site_shet = Balans.objects.get(id=1)
					site_shet.schet_site += price_c
					site_shet.id = 1
					site_shet.save(update_fields=['schet_site'])
					messages.add_message(request, messages.ERROR, 'Баланс ссылки пополнен.')
					return redirect('mycatalog')
				else:
					messages.add_message(request, messages.ERROR, 'Не достаточно денег на рекламном счету. Пополните счет.')
					return redirect('mycatalog')
	else:
		form = PopolnitCatalogForm()
	return render(request, 'catalog/popolnit_catalog.html', {'silka': silka, 'form': form})
