from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView
from tournaments.views import *

urlpatterns = [
    path('tournament/', tournament_view, name='tournament'),
    
    path('', tournament_list, name='tournament_list'),  # Page de liste des tournois

    path('createPrivate/', create_private_tournament_view, name='createPrivateTournament'),  # Créer un tournoi privé
    path('createPublic/', create_public_tournament_view, name='createPublicTournament'),  # Créer un tournoi public
    path('join/', TemplateView.as_view(template_name='join_tournament.html'), name='join_tournament'),  # Rejoindre un tournoi

    path('resTournoi/', view_resTournoi, name='resTournoi'),
]