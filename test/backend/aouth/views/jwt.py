from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


from functools import wraps
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect

# JWT Decorators
# --------------

def jwt_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = jwt_decode(request)
        if user:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Authentication required', extra_tags='aouth_login_tag')
            return redirect('login')  # Redirect to your login page
    return _wrapped_view

# JWT Tokens
# ----------

def jwt_create(request, user):
    try:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Store tokens in session with expiration time
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        request.session.set_expiry(refresh.access_token.payload['exp'])
    except TokenError as e:
        # Handle token generation errors
        raise SuspiciousOperation(f"Error generating tokens: {e}")
    except Exception as e:
        # Handle other unexpected errors
        raise SuspiciousOperation(f"Unexpected error: {e}")

# def jwt_destroy(request):
#     # Clear JWT tokens from the client side (e.g., remove cookies or clear local storage)
#     if 'access_token' in request.session:
#         del request.session['access_token']
#     if 'refresh_token' in request.session:
#         del request.session['refresh_token']
#     response.delete_cookie('access_token')
#     response.delete_cookie('refresh_token')
    

def jwt_invalidate(request):
    invalidated_tokens = request.session.get('invalidated_tokens', [])
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')
    if access_token:
        invalidated_tokens.append(access_token)
    if refresh_token:
        invalidated_tokens.append(refresh_token)
    request.session['invalidated_tokens'] = invalidated_tokens


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
            # Handle token decoding errors
            raise SuspiciousOperation(f"Error decoding tokens: {e}")
        except User.DoesNotExist:
            # Handle user not found
            raise SuspiciousOperation("User not found")
        except Exception as e:
            # Handle other unexpected errors
            raise SuspiciousOperation(f"Unexpected error: {e}")
    else:
        # No tokens found in session
        return None
