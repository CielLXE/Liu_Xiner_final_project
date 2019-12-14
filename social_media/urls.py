
from django.urls import path

from social_media.views import BulletinEdit,BulletinDelete
from . import views

urlpatterns = [
    path('homepage/', views.homepage_list, name='homepage_list'),
    path('society/', views.society_list, name='society_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('follows/', views.follows, name='follows'),
    path('followers/', views.followers, name='followers'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/add/', views.add_post, name='add_post'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/add_favorite/', views.add_favorite, name='add_favorite'),
    path('my_favorite/', views.my_favorite, name='my_favorite'),
    path('others_profile/<int:pk>', views.others_profile, name='others_profile'),
    path('add_follows/<int:pk>', views.add_follows, name='add_follows'),
    path('delete_follows/<str:pk>', views.delete_follows, name='delete_follows'),
    path('delete_followers/<str:pk>', views.delete_followers, name='delete_followers'),
    path('bulletin/', views.bulletin_list, name='bulletin_list'),
    path('bulletin/add/', views.bulletin_add, name='bulletin_add'),
    path('bulletin/<int:pk>/edit/', BulletinEdit.as_view(), name='bulletin_edit'),
    path('bulletin/<int:pk>/delete/', BulletinDelete.as_view(), name='bulletin_delete'),
    path('register/', views.register, name='register_urlpattern'),
]

