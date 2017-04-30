from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import Context, Template, RequestContext
from django.http import HttpResponse
from profuser.models import UserInfo
# Create your views here.
#request_context = RequestContext(request)
#request_context.push({"my_name": "Adrian"})
'''def statis(request):
	statis = User.objects.all()
	context = {'statis': statis}
	request_context = RequestContext(request)
    return render(request, 'base.html', context)'''
	
#Страница топа
def top(request):
	topuser = UserInfo.objects.all().order_by('rating')[:101]
	topuser = topuser.reverse()
	return render(request, 'statis/top.html', {'topuser': topuser})