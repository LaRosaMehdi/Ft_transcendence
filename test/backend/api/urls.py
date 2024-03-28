from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView
from api.views import *
from django.http import HttpResponseNotAllowed
from . import views
from users.views import *
urlpatterns = [
    path('', view_register, name='register'),
	path('register/', view_register, name='register'),
    path('login/', view_login, name='login'),
    path('tournament/', TemplateView.as_view(template_name='tournament.html'), name='tournament'),
    path('mode/', TemplateView.as_view(template_name='mode.html'), name='mode'),
    path('friends/', TemplateView.as_view(template_name='friends.html'), name='friends'),
    path('perso/', TemplateView.as_view(template_name='perso.html'), name='perso'),
    path('main_chat/', TemplateView.as_view(template_name='main_chat.html'), name='main_chat'),
    path('vscomputer/', TemplateView.as_view(template_name='vscomputer.html'), name='vscomputer'),
    path('twofactor/', view_twofactor, name='twofactor'),

	path('generate_profile_json/', generate_profile_json, name='generate_profile_json'),
    path('play/', view_play, name='play'),
]