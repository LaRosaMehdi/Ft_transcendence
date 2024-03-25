from api.views import *
from users.views import *
from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView
from django.urls import path
from .consumers import MatchmakingConsumer
from . import views

websocket_urlpatterns = [
    # URL WebSocket pour la logique de matchmaking
    path('ws/matchmaking/', MatchmakingConsumer.as_asgi()),
]

urlpatterns = [
    path('add-to-queue/', views.add_to_queue, name='add_to_queue'),
    # Ajoutez d'autres vues et leurs URL ici
]