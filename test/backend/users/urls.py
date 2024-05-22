from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import TemplateView

from users.views import *

urlpatterns = [

    # Base views
    path('home/', view_accueil, name='home'),
    path('perso/', view_perso, name='perso'),
    path('perso-content/', view_perso, name='perso-content'),
    path('viewProfile/', view_profile, name='viewProfile'),
    path('friends/', TemplateView.as_view(template_name='friends.html'), name='friends'),

    
    # Settings
    path('settings/', view_setting, name='settings'),
    path('setting_change_username/', setting_change_username, name='setting_change_username'),
    path('setting_change_image/', setting_change_image, name='setting_change_image'),
    path('setting_change_password/', setting_change_password, name='setting_change_password'),
    path('setting_change_2fa/', setting_change_2fa, name='setting_change_2fa'),

    # Other 
    path('generate_profile_json/', generate_profile_json, name='generate_profile_json'),

    # Tools
    path('get_last_game/', user_get_last_game, name='tools'),
    path('get_current_game/', user_get_current_game, name='tools'),
    path('user_get/', user_get, name='user_get'),

    # Friend list
    path('friend/', friend_list, name='friend_list'),
    path('add_friend/<int:user_id>/', add_friend, name='add_friend'),
    path('friend-profile/<str:friend_user>/', view_profile_friend, name='viewProfileFriend'),
]
