import requests, re, logging
from requests import get
from users.models import User
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from users.views import *

logger = logging.getLogger(__name__)

# SETTINGS
# --------

# CHANGE AOUHT 42 TO LOGIN WIHT ADDRESS

from django.contrib import messages

def setting_change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Username already taken.', extra_tags='change_username_tag')
            else:
                if request.user.password is None:
                    messages.warning(request, f'As a 42 user, your username will be changed to {new_username}_42', extra_tags='change_username_tag')
                    new_username += "_42"
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'Username changed successfully.', extra_tags='change_username_tag')
                return redirect('settings') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}', extra_tags='change_username_tag')
    return redirect('settings')
