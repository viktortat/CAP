from django.conf.urls import url

from billtest import views

urlpatterns = [
	url(r'^$', views.billtestall, name='billtestall'),
	url(r'^test/(?P<pk>[0-9]+)/$', views.test_detail, name='test_detail'),
	url(r'^addtest/$', views.addtest, name='addtest'),
	url(r'^edittest/(?P<pk>[0-9]+)/$', views.edit_test, name='edit_test'),
	url(r'^deletetest/(?P<pk>[0-9]+)/$', views.delete_test, name='delete_test'),
	url(r'^modertest/(?P<pk>[0-9]+)/$', views.moder_test, name='moder_test'),
	url(r'^pausatest/(?P<pk>[0-9]+)/$', views.pausa_test, name='pausa_test'),
	url(r'^starttest/(?P<pk>[0-9]+)/$', views.start_test, name='start_test'),
	url(r'^mytest/$', views.mytest, name='mytest'),
	url(r'^money/(?P<pk>[0-9]+)/$', views.popolnit_test, name='popolnit_test'),
]