# blockchain/urls.py
from django.urls import path
from .views import tournament_list_view

urlpatterns = [
    path('tournaments/', tournament_list_view, name='tournament_list'),
]
