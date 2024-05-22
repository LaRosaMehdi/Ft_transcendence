
from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView
from django.urls import path

from aouth.views.aouth import *
from aouth.views.twofactor import *
from aouth.views.views import *

# from django.contrib.auth import views as auth_views

urlpatterns = [

    # Base views (login, register)
    path('', view_register, name='register'),
	path('register/', view_register, name='register'),
    path('login/', view_login, name='login'),

    # OAuthentication (login, register, logout and 42)
	path('aouth_register_form/', aouth_register_form, name='aouth_register_form'),
	path('aouth_login_form/', aouth_login_form, name='aouth_login_form'),
    path('aouth_logout/', aouth_logout, name='aouth_logout'),
    path('aouth_callback_register/', aouth_callback_register, name='aouth_callback_register'),
    path('aouth_callback_login/', aouth_callback_login, name='aouth_callback_login'),

    # Two factor authentication
    path('twofactor/', view_twofactor, name='twofactor'),
    path('twofactor_oauth/', twofactor_oauth, name='twofactor_oauth'),
    path('twofactor_auto_delete/<str:bruteforce>/', twofactor_auto_delete, name='twofactor_auto_delete'),
]
