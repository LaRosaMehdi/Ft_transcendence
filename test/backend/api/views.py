import requests, logging
from requests import get
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from users.views import *
from users.models import User  

logger = logging.getLogger(__name__)

def view_login(request):
    return render(request, 'login.html', {'form': LoginForm() })

def view_register(request):
    return render(request, 'register.html', {'form': RegistrationForm() })

@login_required
def view_accueil(request):
    return render(request, 'accueil.html', {'current_user': request.user})

@login_required
def view_setting(request):
    if request.user.password is not None:
        return render(request, 'settings.html', {
            'change_username_form': ChangeUsernameForm(instance=request.user),
            'change_image_form': ChangeImageForm(instance=request.user),
            'change_password_form': ChangePasswordForm()
        })
    return render(request, 'settings.html', {
        'change_username_form': ChangeUsernameForm(instance=request.user),
        'change_image_form': ChangeImageForm(instance=request.user),
    })

@login_required
def view_perso(request):
    return render(request, 'perso.html')

@login_required
def generate_profile_json(request):
    profile_instance = get_object_or_404(User, username=request.user.username)
    profile_data = {
        'username': profile_instance.username,
        'email': profile_instance.email,
        'elo': profile_instance.elo,
        'image': profile_instance.image.url
    }
    return JsonResponse(profile_data)

def view_twofactor(request):
    return render(request, 'twofactor.html', {'form': TwoFactorForm(), 'current_user': request.user })
