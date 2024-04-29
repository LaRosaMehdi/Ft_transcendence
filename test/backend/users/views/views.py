import logging
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse

from users.views.forms import *
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

# Base views
# ----------

@jwt_login_required
def view_accueil(request):
    logger.debug(f"ACCEUIL JWT tokens: {request.session.get('access_token')} {request.session.get('refresh_token')}")
    logger.debug(f"ACCEUIL User ID: {request.user}")
    return render(request, 'accueil.html', {'current_user': request.user})

@jwt_login_required
def view_perso(request):
    logger.debug(f"PERSO JWT tokens: {request.session.get('access_token')} {request.session.get('refresh_token')}")
    logger.debug(f"PERSO User ID: {request.user}")
    if request.is_ajax():
        html = render_to_string('perso.html', {'current_user': request.user}, request=request)
        return JsonResponse({'html': html})
    else:
        return HttpResponseBadRequest("This endpoint require an AJAX request.")


# Settings
# --------

# @jwt_login_required
# def view_setting(request):
#     if request.user.password is not None:
#         return render(request, 'settings.html', {
#             'change_username_form': ChangeUsernameForm(instance=request.user),
#             'change_image_form': ChangeImageForm(instance=request.user),
#             'change_password_form': PasswordChangeForm(request.user)
#         })
#     return render(request, 'settings.html', {
#         'change_username_form': ChangeUsernameForm(instance=request.user),
#         'change_image_form': ChangeImageForm(instance=request.user),
#     })


@jwt_login_required
def view_setting(request):
    if request.user.password is not None:
        return render(request, 'settings.html', {
            'change_username_form': ChangeUsernameForm(instance=request.user),
            'change_image_form': ChangeImageForm(instance=request.user),
            'change_password_form': ChangePasswordForm(request.user)
        })
    return render(request, 'settings.html', {
        'change_username_form': ChangeUsernameForm(instance=request.user),
        'change_image_form': ChangeImageForm(instance=request.user),
    })