"""Liu_Xiner_final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path('',
         RedirectView.as_view(
             pattern_name='society_list',
             permanent=False
         )),

    path('login/',
         LoginView.as_view(template_name='social_media/login.html'),
         name='login_urlpattern'
         ),

    path('logout/',
         LogoutView.as_view(),
         name='logout_urlpattern'
         ),
    path('admin/', admin.site.urls),
    url(r'', include('social_media.urls')),
]