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

    # Default queue
    # -------------
    path('matchmaking_remote/', view_matchmaking_remote, name='matchmaking_remote'),
    path('matchmaking_remote_make/', matchmaking_remote_make, name='matchmaking_remote_make'),
    path('matchmaking_remote_leave/', matchmaking_remote_leave, name='matchmaking_remote_leave'),
    
    # Remote mode
    # -----------
]