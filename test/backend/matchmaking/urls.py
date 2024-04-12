from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView
from django.urls import path

from matchmaking.views import *

# websocket_urlpatterns = [
#     # URL WebSocket pour la logique de matchmaking
#     path('ws/matchmaking/', MatchmakingConsumer.as_asgi()),
# ]

urlpatterns = [
    path('matchmaking/', view_matchmaking, name='matchmaking'),
    path('matchmaking_make/', matchmaking_make, name='matchmaking_make'),
    path('queue_add_to_default/', queue_add_to_default, name='queue_add_to_default'),
    # Ajoutez d'autres vues et leurs URL ici
]