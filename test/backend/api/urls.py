from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView
from api.views import *
from django.http import HttpResponseNotAllowed
from . import views

from games.views.views import view_play

urlpatterns = [
    path('tournament/', TemplateView.as_view(template_name='tournament.html'), name='tournament'),
    path('mode/', TemplateView.as_view(template_name='mode.html'), name='mode'),
    path('friends/', TemplateView.as_view(template_name='friends.html'), name='friends'),

    
    path('resTournoi/', TemplateView.as_view(template_name='res_tournoi.html'), name='resTournoi'),
    
    path('main_chat/', TemplateView.as_view(template_name='res_tournoi.html'), name='main_chat'),
    path('vscomputer/', TemplateView.as_view(template_name='vscomputer.html'), name='vscomputer'),
    path('hard/', TemplateView.as_view(template_name='hard.html'), name='hard'),
    path('remote/', TemplateView.as_view(template_name='remote.html'), name='remote'),
	path('generate_profile_json/', generate_profile_json, name='generate_profile_json'),
   
    path('play/', view_play, name='play'),
]