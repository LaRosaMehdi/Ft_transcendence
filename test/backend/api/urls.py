from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView
from api.views import *
from django.contrib import admin
from django.http import HttpResponseNotAllowed

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path("admin/", admin.site.urls),
    path('accueil/', TemplateView.as_view(template_name='accueil.html'), name='accueil'),
    path('tournament/', TemplateView.as_view(template_name='tournament.html'), name='tournament'),
    path('mode/', TemplateView.as_view(template_name='mode.html'), name='mode'),
    path('friends/', TemplateView.as_view(template_name='friends.html'), name='friends'),
    path('perso/', TemplateView.as_view(template_name='perso.html'), name='perso'),
	path('generate_profile_json/', generate_profile_json, name='generate_profile_json'),
    path('play/', TemplateView.as_view(template_name='play.html'), name='play'),
]
