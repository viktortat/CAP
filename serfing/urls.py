from django.conf.urls import url
from serfing import views

urlpatterns = [
	#Серфинг
	url(r'^$', views.serfall, name='serfall'),
	url(r'^addserf/$', views.addserf, name='addserf'),
	url(r'^editserf/(?P<pk>[0-9]+)/$', views.edit_serf, name='edit_serf'),
	url(r'^deleteserf/(?P<pk>[0-9]+)/$', views.delete_serf, name='delete_serf'),
	url(r'^moderserf/(?P<pk>[0-9]+)/$', views.moder_serf, name='moder_serf'),
	url(r'^pausaserf/(?P<pk>[0-9]+)/$', views.pausa_serf, name='pausa_serf'),
	url(r'^startserf/(?P<pk>[0-9]+)/$', views.start_serf, name='start_serf'),
	url(r'^myserf/$', views.myserf, name='myserf'),
	url(r'^money/(?P<pk>[0-9]+)/$', views.popolnit_serf, name='popolnit_serf'),
	url(r'^silka/(?P<pk>[0-9]+)/$', views.frame_serf, name='frame_serf'),
	#Псевдо ссылки
	url(r'^addplinks/$', views.addplinks, name='addplinks'),
	url(r'^myplinks/$', views.myplinks, name='myplinks'),
	url(r'^money_plinks/(?P<pk>[0-9]+)/$', views.popolnit_plinks, name='popolnit_plinks'),
	#Контекстная реклама
	url(r'^addcontlinks/$', views.addcontlinks, name='addcontlinks'),
	url(r'^mycontlinks/$', views.mycontlinks, name='mycontlinks'),
	url(r'^money_contlinks/(?P<pk>[0-9]+)/$', views.popolnit_contlinks, name='popolnit_contlinks'),
	#Письма
	url(r'^pisma$', views.pismoall, name='pismoall'),
	url(r'^addpismo/$', views.addpismo, name='addpismo'),
	url(r'^editpismo/(?P<pk>[0-9]+)/$', views.edit_pismo, name='edit_pismo'),
	url(r'^deletepismo/(?P<pk>[0-9]+)/$', views.delete_pismo, name='delete_pismo'),
	url(r'^moderpismo/(?P<pk>[0-9]+)/$', views.moder_pismo, name='moder_pismo'),
	url(r'^pausapismo/(?P<pk>[0-9]+)/$', views.pausa_pismo, name='pausa_pismo'),
	url(r'^startpismo/(?P<pk>[0-9]+)/$', views.start_pismo, name='start_pismo'),
	url(r'^mypismo/$', views.mypismo, name='mypismo'),
	url(r'^moneypismo/(?P<pk>[0-9]+)/$', views.popolnit_pismo, name='popolnit_pismo'),
	url(r'^pismo_otv/(?P<pk>[0-9]+)/$', views.pismo_otv, name='pismo_otv'),
	url(r'^frame_pismo/(?P<pk>[0-9]+)/$', views.frame_pismo, name='frame_pismo'),
	#Переходы на сайтыы
	url(r'^perehod$', views.perehodall, name='perehodall'),
	url(r'^addperehod/$', views.addperehod, name='addperehod'),
	url(r'^editperehod/(?P<pk>[0-9]+)/$', views.edit_perehod, name='edit_perehod'),
	url(r'^deleteperehod/(?P<pk>[0-9]+)/$', views.delete_perehod, name='delete_perehod'),
	url(r'^moderperehod/(?P<pk>[0-9]+)/$', views.moder_perehod, name='moder_perehod'),
	url(r'^pausaperehod/(?P<pk>[0-9]+)/$', views.pausa_perehod, name='pausa_perehod'),
	url(r'^startperehod/(?P<pk>[0-9]+)/$', views.start_perehod, name='start_perehod'),
	url(r'^myperehod/$', views.myperehod, name='myperehod'),
	url(r'^moneyperehod/(?P<pk>[0-9]+)/$', views.popolnit_perehod, name='popolnit_perehod'),
	url(r'^frame_perehod/$', views.frame_perehod, name='frame_perehod'),
	url(r'^frame_perehod1/$', views.frame_perehod1, name='frame_perehod1'),
]