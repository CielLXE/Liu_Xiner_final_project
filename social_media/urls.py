
from django.urls import path

from . import views

urlpatterns = [
    path('homepage/', views.homepage_list, name='homepage_list'),
    path('society/', views.society_list, name='society_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('my_profile/<int:pk>/', views.my_profile, name='my_profile'),
    # path('login/', views.login_view, name='login_urlpattern'),
]

