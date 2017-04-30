from django.conf.urls import url
from catalog import views

urlpatterns = [
	url(r'^$', views.siteall, name='siteall'),
	url(r'^addsite/$', views.addsite, name='addsite'),
	url(r'^mycatalog/$', views.mycatalog, name='mycatalog'),
	url(r'^money_catalog/(?P<pk>[0-9]+)/$', views.popolnit_catalog, name='popolnit_catalog'),
]