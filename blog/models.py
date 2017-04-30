from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

#Модель новости
class Post(models.Model):
	class Meta():
		db_table = 'news'
		verbose_name = "Новость"
		verbose_name_plural = "Новости"
		
	author = models.ForeignKey('auth.User')
	title = models.CharField("Заголовок", max_length=200)
	text = RichTextField()
	created_date = models.DateTimeField(
            default=timezone.now)
	published_date = models.DateTimeField("Дата", 
            blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

#Модель коментария		
class Comments(models.Model):
	class Meta():
		db_table = 'Comments'
		verbose_name = "Коментарий"
		verbose_name_plural = "Коментарии"
		
	author = models.ForeignKey(User, verbose_name = "Пользователь")
	comment_post = models.ForeignKey(Post, verbose_name = "Новость")
	comment_text = models.TextField("Коментарий")
	pub_date = models.DateTimeField('Дата', default=timezone.now)
	
	def __str__(self):
		return self.comment_post.title