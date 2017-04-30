"""wmr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
#from django.contrib.auth.views import login, logout	
#from statis.views import statis
urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'blog/', include('blog.urls')),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^profuser/', include('profuser.urls')),
	url(r'^tasks/', include('tasks.urls')),
	url(r'^catalog/', include('catalog.urls')),
	url(r'^serfing/', include('serfing.urls')),
	url(r'^billtest/', include('billtest.urls')),
	url(r'top/', include('statis.urls')),
	url(r'^captcha/', include('captcha.urls')),
	url(r'^mail/', include('mail.urls')),
	url(r'^(?P<url>.*/)$', views.flatpage),
	#url(r'^ckeditor/', include('ckeditor.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)