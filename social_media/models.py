
# Create your models here.
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="post_user")
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s posts "%s"' % (self.author, self.text)


class Comment(models.Model):
    post = models.ForeignKey('social_media.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='users')
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey('social_media.Post', on_delete=models.CASCADE)
    status = models.CharField(max_length=10)

    def __str__(self):
       return '%s likes "%s" : %s' % (self.user, self.post, self.status)


class Follow(models.Model):
    follows = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="follows")
    follower = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return '%s follows %s' % (self.follower, self.follows)


class Bulletin(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
