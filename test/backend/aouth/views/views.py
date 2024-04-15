import logging
from django.shortcuts import render

from aouth.views.forms import *

logger = logging.getLogger(__name__)

# Aouth views
# -----------

def view_login(request):
    return render(request, 'login.html', {'form': LoginForm() })

def view_register(request):
    return render(request, 'register.html', {'form': RegistrationForm() })

def view_twofactor(request):
    context = request.GET.get('context', '')
    return render(request, 'twofactor.html', {'form': TwoFactorForm(), 'context': context})
