from datetime import timezone

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy

from social_media.forms import CommentForm
from social_media.models import Post, Follow
from django.db import connection


def homepage_list(request):
    uname= request.session['_auth_user_id']
    posts = Post.objects.select_related(User)
    # cursor = connection.cursor()
    # cursor.execute("""Select p.id,p.author_id,p.text,p.date
    #                    From social_media_Post as p,
    #                    WHERE p.author_id= %s or p.author_id in
    #                    (Select f.follows_id
    #                    From social_media_Follow as f
    #                    WHERE f.follower_id = %s)
    #                    """, [uname, uname])
    # post = cursor.fetchall()
    # label = ['id', 'author', 'text','date']
    # posts = [dict(zip(label, p)) for p in post]
    return render(request, 'social_media/homepage_list.html', {'posts': posts})


def society_list(request):
    posts = Post.objects.all().order_by('date')
    return render(request, 'social_media/society_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'social_media/post_detail.html', {'post': post})


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'social_media/add_comment.html', {'form': form})


def my_profile(request, pk):
    posts = Post.objects.all().order_by('date').filter(author=pk)
    return render(request, 'social_media/my_profile.html', {'posts': posts})

