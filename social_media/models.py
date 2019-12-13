
# Create your models here.
from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key= True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('social_media.User', on_delete=models.CASCADE, related_name="post_user")
    text = models.TextField()
    date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return '%s posts "%s"' % (self.author, self.text)


class Comment(models.Model):
    post = models.ForeignKey('social_media.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('social_media.User', on_delete=models.CASCADE, related_name='users')
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class Favorite(models.Model):
    user = models.ForeignKey('social_media.User', on_delete=models.CASCADE)
    post = models.ForeignKey('social_media.Post', on_delete=models.CASCADE)

    def __str__(self):
        return '%s likes "%s"' % (self.user, self.post)


class Follow(models.Model):
    follows = models.ForeignKey('social_media.User', on_delete=models.CASCADE, related_name="follows")
    follower = models.ForeignKey('social_media.User', on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return '%s follows %s' % (self.follower, self.follows)

    class Meta:
        unique_together = (('follows', 'follower'),)
