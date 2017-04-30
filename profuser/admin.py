from django.contrib import admin
from profuser.models import UserInfo, Refery, Viplati

#Фильтры
class ViplatiAdmin(admin.ModelAdmin):
	list_filter = ('ub_date', 'sum')
	list_display = ('user', 'sum', 'sys_viplat', 'ub_date', 'odobren')

class UserInfoAdmin(admin.ModelAdmin):
	#list_filter = ('nick', 'user')
	list_display = ('user', 'rating', 'schet_lich')
	
admin.site.register(Refery)
admin.site.register(Viplati, ViplatiAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
