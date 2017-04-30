from django.conf.urls import url

from mail import views

urlpatterns = [
	url(r'^$', views.mymail, name='mymail'),
	url(r'^sendmail/$', views.otmail, name='otmail'),
	url(r'^addmail/$', views.addmail, name='addmail'),
	url(r'^full/(?P<pk>[0-9]+)/$', views.detail_mail, name='detail_mail'),
	url(r'^fulls/(?P<pk>[0-9]+)/$', views.detail_otmail, name='detail_otmail'),
]