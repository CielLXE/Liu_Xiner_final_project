from django.contrib import admin
from .models import Post, Comment,Favorite,Follow, User
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Follow)