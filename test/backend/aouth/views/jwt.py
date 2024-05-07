import logging
from functools import wraps
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()
logger = logging.getLogger(__name__)

# JWT Decorators
# --------------

def jwt_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.exists(request.session.session_key):
            access_token = request.session.get('access_token')
            if access_token:
                return view_func(request, *args, **kwargs)
            else:
                try:
                    jwt_refresh(request)
                    access_token = request.session.get('access_token')
                    if access_token:
                        return view_func(request, *args, **kwargs)
                except SuspiciousOperation as e:
                    messages.error(request, 'Authentication error', extra_tags='aouth_login_tag')
                    return redirect('login')
        else:
            messages.error(request, 'Session does not exist', extra_tags='aouth_login_tag')
            return redirect('login')
    return _wrapped_view

      
# JWT Tokens
# ----------

def jwt_create(request, user):
    try:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        request.session.set_expiry(refresh.access_token.payload['exp'])
    except TokenError as e:
        raise SuspiciousOperation(f"Error generating tokens: {e}")
    except Exception as e:
        raise SuspiciousOperation(f"Unexpected error: {e}")

def jwt_destroy(request, response):
    if 'access_token' in request.session:
        del request.session['access_token']
    if 'refresh_token' in request.session:
        del request.session['refresh_token']
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

def jwt_decode(request):
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')
    
    if access_token and refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh.access_token.payload.get('user_id')
            user = User.objects.get(id=user_id)
            return user
        except TokenError as e:
            raise SuspiciousOperation(f"Error decoding tokens: {e}")
        except User.DoesNotExist:
            raise SuspiciousOperation("User not found")
        except Exception as e:
            raise SuspiciousOperation(f"Unexpected error: {e}")
    else:
        return None
  
def jwt_refresh(request):
    try:
        refresh_token = request.session.get('refresh_token')
        if refresh_token:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            request.session['access_token'] = access_token
            request.session.set_expiry(refresh.access_token.payload['exp'])
            return access_token
        else:
            raise SuspiciousOperation("Refresh token not found")
    except TokenError as e:
        raise SuspiciousOperation(f"Error refreshing token: {e}")
    except Exception as e:
        raise SuspiciousOperation(f"Unexpected error: {e}")
