from django.contrib import admin
from tasks.models import Tasksa, TasksUsers

#Фильтры
class TasksaInLine(admin.StackedInline):
	model = TasksUsers

class TasksaAdmin(admin.ModelAdmin):
	list_filter = ('pub_date',)
	list_display = ('title', 'user', 'pub_date', 'odobren',  'moder')
	
class TasksUsersAdmin(admin.ModelAdmin):
	list_filter = ('taskuser',)
	list_display = ('taskuser', 'otvet_user', 'odobren')
	
admin.site.register(Tasksa, TasksaAdmin)
admin.site.register(TasksUsers, TasksUsersAdmin)
