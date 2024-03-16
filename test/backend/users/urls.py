from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView
from api.views import *
from users.views import *
from django.contrib import admin
from django.http import HttpResponseNotAllowed
from . import views
from api.views import *
from users.views import *

urlpatterns = [
    path('home/', accueil, name='home'),
    path('perso/', perso, name='perso'),
    path('ettings/', settings, name='settings'),
	
	path('aouth_register_form/', aouth_register_form, name='aouth_register_form'),
	path('aouth_login_form/', aouth_login_form, name='aouth_login_form'),

    path('setting_change_username/', setting_change_username, name='setting_change_username'),
]
