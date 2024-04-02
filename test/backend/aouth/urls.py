from api.views import *
from aouth.views import *
from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView

urlpatterns = [
	path('aouth_register_form/', aouth_register_form, name='aouth_register_form'),
	path('aouth_login_form/', aouth_login_form, name='aouth_login_form'),
    path('aouth_logout/', aouth_logout, name='aouth_logout'),
    path('aouth_callback_register/', aouth_callback_register, name='aouth_callback_register'),
    path('aouth_callback_login/', aouth_callback_login, name='aouth_callback_login'),

    path('twofactor/', view_twofactor, name='twofactor'),
    path('twofactor_oauth/', twofactor_oauth, name='twofactor_oauth'),
    path('twofactor_setting/', twofactor_setting, name='twofactor_setting')
]
