import logging
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse

from aouth.views.forms import *
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

# Aouth views
# -----------

def view_login(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_login.html', {'form': LoginForm()}, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'login.html', {'form': LoginForm()})

def view_register(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_register.html', {'form': RegistrationForm()}, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'register.html', {'form': RegistrationForm()})

def view_twofactor(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_twofactor.html', {'form': TwoFactorForm(), 'context': 'ajax'}, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'twofactor.html', {'form': TwoFactorForm(), 'context': ''})