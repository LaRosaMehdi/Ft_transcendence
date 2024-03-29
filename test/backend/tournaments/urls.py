from api.views import *
from users.views import *
from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView
from tournaments import views

urlpatterns = [
    path('', views.tournament_list, name='tournament_list'),  # Page de liste des tournois
     path('create/', TemplateView.as_view(template_name='create_tournament.html'), name='create_tournament'),  # Créer un tournoi
    path('join/', TemplateView.as_view(template_name='join_tournament.html'), name='join_tournament'),  # Rejoindre un tournoi
]
