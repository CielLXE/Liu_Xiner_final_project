
from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post, Bulletin


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['text']


class BulletinForm(forms.ModelForm):

    class Meta:
        model = Bulletin
        fields = ('title', 'text',)