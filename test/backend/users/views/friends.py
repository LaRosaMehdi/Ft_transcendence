import requests, re, logging
from requests import get
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string

from users.views.forms import *
from aouth.views.jwt import jwt_login_required
from django.urls import reverse

logger = logging.getLogger(__name__)

User = get_user_model()

@jwt_login_required
def friend_list(request):
    search_query = request.GET.get('search_query', '').strip()
    friends = request.user.friends.all()
    users = None
    if search_query:
        users = User.objects.filter(username__icontains=search_query).exclude(id__in=friends).exclude(id=request.user.id)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
       html = render_to_string('spa_friend_list.html', {'friends': friends, 'users': users, 'search_query': search_query, 'current_user': request.user, 'context': 'ajax'}, request=request)
       return JsonResponse({'html': html})
    else:
        return render(request, 'friend_list.html', {
            'friends': friends,
            'users': users,
            'search_query': search_query
        })

@jwt_login_required
def add_friend(request, user_id):
    if request.method == "POST":
        friend = get_object_or_404(User, pk=user_id)
        if friend.username == 'root' or friend == request.user:
            return HttpResponseForbidden("You cannot add this user as a friend.")
        if friend not in request.user.friends.all():
            request.user.friends.add(friend)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':        
        return JsonResponse({
            'status': 'success',
            'message': 'success.',
            'redirectUrl': 'friend_list',
        })
    else:
        return redirect('friend_list')