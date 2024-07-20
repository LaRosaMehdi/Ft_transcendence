# blockchain/urls.py
from django.urls import path
from .views import blockchain_tournament_list_view

urlpatterns = [
    path('score-tournament/', blockchain_tournament_list_view, name='score_tournament'),
]
