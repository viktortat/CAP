from django.conf.urls import url
from statis import views

urlpatterns = [
	url(r'^$', views.top, name='top'),
]