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
    # path('createPrivate/', TemplateView.as_view(template_name='createPrivateTournament.html'), name='createPrivateTournament'),  # Créer un tournoi
    # path('createPublic/', TemplateView.as_view(template_name='createOpenTournament.html'), name='createPublicTournament'),  # Créer un tournoi
    path('createPrivate/', views.create_private_tournament_view, name='createPrivateTournament'),  # Créer un tournoi privé
    path('createPublic/', views.create_public_tournament_view, name='createPublicTournament'),  # Créer un tournoi public
    path('join/', TemplateView.as_view(template_name='join_tournament.html'), name='join_tournament'),  # Rejoindre un tournoi
]
