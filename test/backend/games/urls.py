from users.views import *
from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView
from games.views.views import *

urlpatterns = [
    
    # Base
    path('play/', view_play, name='play'),
    path('mode/', view_mode, name='mode'),

    # Modes
    path('vscomputer/', view_vscomputer, name='vscomputer'),
    path('remote/', view_remote, name='remote'),
    path('hard/', TemplateView.as_view(template_name='hard.html'), name='hard'),
    
    # Others ??
    path('main_chat/', view_main_chat, name='main_chat'),
]
