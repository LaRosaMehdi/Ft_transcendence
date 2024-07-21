from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView

from aouth.views.twofactor import twofactor_oauth

urlpatterns = [
    path('twofactor_oauth/', twofactor_oauth, name='twofactor_oauth'),
]
