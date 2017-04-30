from django.contrib import admin
from .models import Post, Comments

class PostAdmin(admin.ModelAdmin):
	list_filter = ('published_date',)
	list_display = ('title', 'author', 'published_date')

class CommentsAdmin(admin.ModelAdmin):
	list_filter = ('pub_date', 'comment_post',)
	list_display = ('author', 'comment_post', 'pub_date')
	
admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)
