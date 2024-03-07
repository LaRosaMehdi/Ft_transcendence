from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

# @login_required
def accueil(request):
    return render(request, 'accueil.html')

def generate_profile_json(request):
    profile_data = {
        "username": "testdb",
        "elo_tst": 10,
        "ce que tu veux": "test test"
    }
    return JsonResponse(profile_data)


def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # user = User.objects.create_user(username=username, password=password)
        # if request.user.is_authenticated:
        #     return HttpResponseRedirect('/accueil/')  # Redirect to accueil page if already authenticated
        # else:
        #     return HttpResponseRedirect('/accueil/')  # Redirect to index page if not authenticated
    else:
        return render(request, 'index.html')