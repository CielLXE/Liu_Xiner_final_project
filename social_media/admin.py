from django.contrib import admin
from .models import Post, Comment,Favorite,Follow,Bulletin
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Bulletin)