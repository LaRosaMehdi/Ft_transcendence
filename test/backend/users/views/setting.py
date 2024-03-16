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

from django.http import JsonResponse

def setting_change_username(request):
    try:
        if request.method == 'POST':
            new_username = request.POST.get('new_username')
            logger.debug("->> new_username: " + new_username)
            
            # Get the username from the URL
            username = request.user.username
            
            user = user_get_by_username(username)
            logger.debug("->> user: " + str(user))
            
            # Update the username
            user.username = new_username
            user.save()
            
            return JsonResponse({'success': True})  # Return a success response
        else:
            logger.error("Invalid request method")
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Exception as e:
        logger.exception("An error occurred in change_username")
        return JsonResponse({'error': str(e)}, status=500)