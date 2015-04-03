from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from account import views

urlpatterns = [
    url('^login/?$', login, {'template_name': 'account/login.html'}),
    url('^create/?$', views.UserCreate.as_view()),
    ]
