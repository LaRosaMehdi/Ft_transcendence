from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView
from tournaments.views import *
from tournaments.views.tournaments import tournament_get

urlpatterns = [
    # Tournament
    path('tournament/', view_tournament, name='tournament'),


    # Public
    path('create/', view_tournament_generate, name='createTournament'),  # Créer un tournoi public
    path('join/', view_tournament_join, name='joinTournament'),  # Rejoindre un tournoi public
    path('generateTournament/', tournament_generate, name='generateTournament'),  # Générer un tournoi public
    path('connectTournament/', tournament_join, name='connectTournament'),  # Rejoindre un tournoi public
    path('tournament_in_progress/', view_tournament_in_progress, name='tournament_in_progress'),
    
    # path
    path('<str:tournament_name>/', view_tournament_dashboard, name='dashboardTournament'),  # Page de tournoi
    path('<str:tournament_name>/get/', tournament_get, name='detailsTournament'),  # Détails d'un tournoi
    path('<str:tournament_name>/launch/', tournament_launch, name= 'launchTournament'),  # Rejoindre un tournoi
    path('<str:tournament_name>/play/<int:game_id>/', view_tournament_play, name='playTournament'),  # Rejoindre un tournoi
    # path('<str:tournament_name>/play/<int:game_id>/quit/', tournament_play_quit, name='playQuitTournament'),  # Quitter un tournoi
    path('<str:tournament_name>/play/<int:game_id>/end/', tournament_play_end, name='playEndTournament'),  # Terminer un tournoi
    # Other
    path('', tournament_list, name='tournament_list'),  # Page de liste des tournois
    path('resTournoi/', view_resTournoi, name='resTournoi'),
]