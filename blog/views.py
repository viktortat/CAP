from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comments
from .forms import CommentsForm
import datetime
from django.contrib.auth.models import User
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	user = request.user
	post_s = Post.objects.get(id = pk)
	comm_s = Comments.objects.filter(comment_post_id = pk)
	if request.method == "POST":
		form = CommentsForm(request.POST)
		if form.is_valid():
			#Сахроняю коментарий
			comm = form.save(commit=False)
			comm.comment_post = post_s
			comm.author = user
			comm.save()
			return redirect('/blog/post/{}'.format(pk))
	else:
		form = CommentsForm()
	return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comm_s': comm_s})
	
def current_datetime(request):
    nowtime = datetime.datetime.now()
    return render(request, 'base.html', {'nowtime': nowtime})