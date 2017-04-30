from django.conf.urls import url

from profuser import views, sys_money

urlpatterns = [
	url(r'^$', views.info, name='info'),
	url(r'^(?P<pk>[0-9]+)/$', views.pub_info, name='pub_info'),
	url(r'^stat_user/$', views.stat_user, name='stat_user'),
	url(r'^edit/(?P<pk>[0-9]+)/$', views.editinfo, name='editinfo'),
	url(r'^myreferal/$', views.myreferal, name='myreferal'),
	url(r'^iref/(?P<pk>[0-9]+)/$', views.iref, name='iref'),
	url(r'^money/$', views.sys_viplat, name='sys_viplat'),
	url(r'^money/syswmr$', views.vivod_wmr, name='vivod_wmr'),
	url(r'^money/sysandex$', views.vivod_yandex, name='vivod_yandex'),
	url(r'^money/sysqiwi$', views.vivod_qiwi, name='vivod_qiwi'),
	url(r'^money/sysperfect$', views.vivod_perfect, name='vivod_perfect'),
	url(r'^money/syspayeer$', views.vivod_payeer, name='vivod_payeer'),
	url(r'^money/syspopol$', views.sys_popol, name='sys_popol'),
	url(r'^ref/(?P<ref>[0-9]+)/$', views.referal, name='referal'),
	url(r'^activ/$', views.activ, name='activ'),
	url(r'^reflinks/$', views.rekmat, name='rekmat'),
	url(r'^money/perevod$', sys_money.perevod, name='perevod'),
	url(r'^money/yandex/$', sys_money.popoln_yandex, name='popoln_yandex'),
	url(r'^money/resyandex/$', sys_money.res_yandex, name='res_yandex'),
	url(r'^money/webmoney/$', sys_money.popoln_webm, name='popoln_webm'),
	url(r'^money/webmresult/$', sys_money.popoln_webmres, name='popoln_webmres'),
	url(r'^money/success/$', sys_money.success, name='success'),
	url(r'^money/fail/$', sys_money.fail, name='fail'),
	url(r'^money/perfectm/$', sys_money.popoln_pm, name='popoln_pm'),
	url(r'^money/pm/$', sys_money.popoln_pmres, name='popoln_pmres'),
	url(r'^money/pmfail/$', sys_money.pmfail, name='pmfail'),
	url(r'^money/pyaeer/$', sys_money.popoln_payeer, name='popoln_payeer'),
	url(r'^money/payeerres/$', sys_money.deposit_result, name='deposit_result'),
    url(r'^money/payeer/success/$', sys_money.payeer_success, name='payeer_success'),
	url(r'^money/payeer/fail/$', sys_money.payeer_fail, name='payeer_fail'),
	#url(r'^money/payeer/test/$', views.payeer_test, name='payeer_test'),
	url(r'^money/qiwi/$', sys_money.popoln_qiwi, name='popoln_qiwi'),
	url(r'^money/qiwires/$', sys_money.res_qiwi, name='res_qiwi'),
]