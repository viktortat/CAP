from django.conf.urls import url

from tasks import views

urlpatterns = [
    url(r'^$', views.tasksall, name='tasksall'),
	url(r'^(?P<pk>[0-9]+)/$', views.taskscat, name='taskscat'),
	url(r'^tasks/(?P<pk>[0-9]+)/$', views.tasks_detail, name='tasks_detail'),
	url(r'^addtasks/$', views.addtasks, name='addtasks'),
	url(r'^edittask/(?P<pk>[0-9]+)/$', views.edit_task, name='edit_task'),
	url(r'^deletetask/(?P<pk>[0-9]+)/$', views.delete_task, name='delete_task'),
	url(r'^modertask/(?P<pk>[0-9]+)/$', views.moder_task, name='moder_task'),
	url(r'^pausatask/(?P<pk>[0-9]+)/$', views.pausa_task, name='pausa_task'),
	url(r'^starttask/(?P<pk>[0-9]+)/$', views.s_task, name='s_task'),
	url(r'^mytasks/$', views.mytasks, name='mytasks'),
	url(r'^otvet_task/(?P<pk>[0-9]+)/$', views.otvet_task, name='otvet_task'),
	url(r'^otvetdelete/(?P<pk>[0-9]+)/$', views.otvet_delete, name='otvet_delete'),
	url(r'^start_task/(?P<pk>[0-9]+)/$', views.start_task, name='start_task'),
	url(r'^otvet_detail/(?P<pk>[0-9]+)/$', views.otvet_detail, name='otvet_detail'),
	url(r'^money/(?P<pk>[0-9]+)/$', views.popolnit_task, name='popolnit_task'),
	url(r'^dor_otvet/(?P<pk>[0-9]+)/$', views.dor_otvet, name='dor_otvet'),
]