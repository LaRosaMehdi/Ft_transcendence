from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
import requests
from requests import get
import logging

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def accueil(request, username):
    return render(request, 'accueil.html', {'username': username})

def settings(request, username):
    # Your view logic goes here
    return render(request, 'settings.html', {'username': username})

def perso(request, username):
    return render(request, 'perso.html', {'username': username})

def generate_profile_json(request):
    profile_data = {
        "username": "testdb",
        "elo_tst": 10,
        "ce que tu veux": "test test"
    }
    return JsonResponse(profile_data)

