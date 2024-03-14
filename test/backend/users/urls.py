from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView
from api.views import *
from users.views import *
from django.contrib import admin
from django.http import HttpResponseNotAllowed
from . import views

urlpatterns = [
	#path('accueil/', views.oauth_callback, name='accueil'),
    path('accueil2/<str:username>/', accueil, name='accueil2'),
	path('aouth_register_form/', aouth_register_form, name='aouth_register_form'),
	path('aouth_login_form/', aouth_login_form, name='aouth_login_form'),
]
