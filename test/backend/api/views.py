import requests, logging
from requests import get
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from matchmaking.views.queue import queue_add_to_default
from matchmaking.views.manager import matchmaking_manager
from users.views import *
from users.models import User  
from smtp.views.forms import TwoFactorForm
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

def view_login(request):
    return render(request, 'login.html', {'form': LoginForm() })

def view_register(request):
    return render(request, 'register.html', {'form': RegistrationForm() })

@login_required
def view_play(request):
    queue_add_to_default(request)
    matchmaking_manager(request)
    return render(request, 'play.html', {'current_user': request.user})

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
    if request.is_ajax():
        html = render_to_string('perso.html', {'current_user': request.user}, request=request)
        return JsonResponse({'html': html})
    else:
        return HttpResponseBadRequest("This endpoint require an AJAX request.")

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
    context = request.GET.get('context', '')
    return render(request, 'twofactor.html', {'form': TwoFactorForm(), 'context': context})