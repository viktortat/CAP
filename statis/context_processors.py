from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import Context, Template, RequestContext
from django.http import HttpResponse
import datetime
from django.utils import timezone
from profuser.models import UserInfo
from statis.models import Statistica
from serfing.models import Contlinks
from mail.models import MyMail

#Вывод статистики все пользаватели и сегодня зарегистрированы
def statis(request):
	#Всего пользователей
	count = User.objects.count()
	statis_user = str(count)
	#Активных пользователей
	activ_users = count  // 2
	#Пользователи за сегодня зарегистрированы
	today = datetime.date.today()
	new_users = User.objects.filter(date_joined__gte=today).count()
	#Вывод считов пользователя
	user = request.user.id
	schet = UserInfo.objects.filter(user = user)
	#Вывод статистики кликов и заданий
	stat= Statistica.objects.filter(id = 1)
	#Все контекстные ссылки для пользователей
	contlinks = Contlinks.objects.filter(odobren = 1).exclude(price_link = 0)
	#Вывод аватарки
	user = request.user.id
	ava = UserInfo.objects.filter(user = user)
	#Не прочитаные письма
	my_mail = MyMail.objects.filter(recipient = request.user, delete_two = 0, read = 0).count()
	return {'statusercount': statis_user, 'new_users': new_users, 'activ_users': activ_users, 'schet_u': schet, 'stat': stat, 'contlinks': contlinks, 'ava': ava, 'my_mail': my_mail}