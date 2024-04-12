import logging
from django.shortcuts import render

from aouth.views.forms import *

logger = logging.getLogger(__name__)

# Aouth views
# -----------

def view_login(request):
    logger.debug(f"LOGIN JWT tokens: {request.session.get('access_token')} {request.session.get('refresh_token')}")
    logger.debug(f"LOGIN User ID: {request.user}")
    return render(request, 'login.html', {'form': LoginForm() })

def view_register(request):
    logger.debug(f"REG JWT tokens: {request.session.get('access_token')} {request.session.get('refresh_token')}")
    logger.debug(f"REG User ID: {request.user}")
    return render(request, 'register.html', {'form': RegistrationForm() })

def view_twofactor(request):
    logger.debug(f"TWOFA JWT tokens: {request.session.get('access_token')} {request.session.get('refresh_token')}")
    logger.debug(f"TWOFA User ID: {request.user}")
    context = request.GET.get('context', '')
    return render(request, 'twofactor.html', {'form': TwoFactorForm(), 'context': context})
