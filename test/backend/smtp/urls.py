from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView

from aouth.views.twofactor import twofactor_oauth, twofactor_setting

urlpatterns = [
    path('twofactor_oauth/', twofactor_oauth, name='twofactor_oauth'),
    path('twofactor_setting/', twofactor_setting, name='twofactor_setting')
]
