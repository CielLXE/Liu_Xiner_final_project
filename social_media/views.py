import django.utils.timezone as timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse

from social_media.forms import CommentForm, PostForm, BulletinForm
from social_media.models import Post, Follow, Comment, Favorite,Bulletin
from django.db import connection


def homepage_list(request):
    uname= request.session['_auth_user_id']
    # posts = Post.objects.all().order_by('date').filter(author=uname)
    cursor = connection.cursor()
    cursor.execute("""Select p.id, u.username,p.text,p.date,u.id
                       From social_media_Post as p,auth_user as u
                       WHERE p.author_id in 
                       (Select f.follows_id
                        From social_media_Follow as f
                        WHERE f.follower_id = %s)
                       and p.author_id = u.id
                       order by p.date desc 
                       """, [uname])
    post = cursor.fetchall()
    label = ['id','author', 'text','date','uid']
    posts = [dict(zip(label, p)) for p in post]
    return render(request, 'social_media/homepage_list.html', {'posts': posts})


def society_list(request):
    cursor = connection.cursor()
    cursor.execute("""Select p.id, u.username,p.text,p.date,u.id
                           From social_media_Post as p,auth_user as u
                           WHERE p.author_id = u.id
                           order by p.date desc 
                           """)
    post = cursor.fetchall()
    label = ['id', 'author', 'text', 'date', 'uid']
    posts = [dict(zip(label, p)) for p in post]
    return render(request, 'social_media/society_list.html', {'posts': posts})


def post_detail(request, pk):
    uname = request.session['_auth_user_id']
    post = get_object_or_404(Post, pk=pk)
    loveinfo = Favorite.objects.filter(post=pk, user=uname)
    if loveinfo and loveinfo[0].status == "True":
        love_flag = 1
    else:
        love_flag = 0
    return render(request, 'social_media/post_detail.html', {'post': post, 'loveflag':love_flag})


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
    return render(request, 'social_media/comment_add.html', {'form': form})


def my_profile(request):
    uname = request.session['_auth_user_id']
    posts = Post.objects.all().order_by('-date').filter(author=uname)
    return render(request, 'social_media/my_profile.html', {'posts': posts})


def follows(request):
    uname = request.session['_auth_user_id']
    follows_users = Follow.objects.filter(follower=uname)
    return render(request, 'social_media/follows.html', {'follows_users': follows_users})


def followers(request):
    uname = request.session['_auth_user_id']
    followers_users = Follow.objects.filter(follows=uname)
    return render(request, 'social_media/followers.html', {'followers_users': followers_users})


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'social_media/post_edit.html', {'form': form})


def delete_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('my_profile')


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'social_media/post_add.html', {'form': form})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def add_favorite(request, pk):
    p_id = pk
    uname = request.session['_auth_user_id']
    love_info = Favorite.objects.filter(post=p_id, user=uname)
    post = Post.objects.get(id=p_id)
    user = User.objects.get(id=uname)
    if love_info:
        if love_info[0].status == "True":
            Favorite.objects.filter(post=p_id, user=uname).update(status="False")
        else:
            Favorite.objects.filter(post=p_id, user=uname).update(status="True")
    else:
        Favorite.objects.create(post=post, user=user, status="True")
    return redirect('post_detail', pk=p_id)


def my_favorite(request):
    uname = request.session['_auth_user_id']
    posts = set()
    for f in Favorite.objects.filter(user=uname, status="True").select_related('post'):
        posts.add(f.post)
    return render(request, 'social_media/my_favorite.html', {'posts': posts})


def others_profile(request, pk):
    posts = Post.objects.filter(author=pk).order_by('-date')
    uname = request.session['_auth_user_id']
    username = User.objects.get(id=pk)
    follows_info = Follow.objects.filter(follows=pk, follower=uname)
    if follows_info:
        flag = 1
    else:
        flag = 0
    return render(request, 'social_media/others_profile.html', {'posts': posts, 'uid': pk, 'username':username,'flag':flag})


def add_follows(request,pk):
    uname = request.session['_auth_user_id']
    uid = pk
    follows_info = Follow.objects.filter(follows=uid, follower=uname)
    target_user = User.objects.get(id=uid)
    user = User.objects.get(id=uname)
    if follows_info:
        Follow.objects.filter(follows=uid, follower=uname).delete()
    else:
        Follow.objects.create(follows=target_user, follower=user)
    return redirect('others_profile', pk=uid)


def delete_follows(request,pk):
    uname = request.session['_auth_user_id']
    uid = User.objects.get(username=pk).id
    Follow.objects.filter(follows=uid, follower=uname).delete()
    return redirect('follows')


def delete_followers(request,pk):
    uname = request.session['_auth_user_id']
    uid = User.objects.get(username=pk).id
    Follow.objects.filter(follows=uname, follower=uid).delete()
    return redirect('followers')


def bulletin_list(request):
    posts = Bulletin.objects.all().order_by('-date')
    return render(request, 'social_media/bulletin_list.html', {'posts': posts})


def bulletin_add(request):
    if request.method == "POST":
        form = BulletinForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('bulletin_list')
    else:
        form = BulletinForm()
    return render(request, 'social_media/bulletin_add.html', {'form': form})


def bulletin_edit(request, pk):
    post = get_object_or_404(Bulletin, pk=pk)
    if request.method == "POST":
        form = BulletinForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('bulletin_list')
    else:
        form = BulletinForm(instance=post)
    return render(request, 'social_media/bulletin_edit.html', {'form': form})


def bulletin_delete(request,pk):
    post = get_object_or_404(Bulletin, pk=pk)
    post.delete()
    return redirect('bulletin_list')