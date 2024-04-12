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

from users.models import User, Friendship
from users.views.forms import *
from aouth.views.twofactor import twofactor_setting_send
from aouth.views.jwt import jwt_login_required
from django.urls import reverse

logger = logging.getLogger(__name__)

User = get_user_model()

@jwt_login_required
def friend_list(request):
    search_query = request.GET.get('search_query', '').strip()
    
    current_friends_ids = Friendship.objects.filter(requester=request.user).values_list('friend__id', flat=True)
    friends = User.objects.filter(id__in=current_friends_ids)

    users = None
    if search_query:
        users = User.objects.filter(username__icontains=search_query).exclude(id__in=current_friends_ids).exclude(id=request.user.id)

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

        if not Friendship.objects.filter(requester=request.user, friend=friend).exists() and friend != request.user:
            Friendship.objects.create(requester=request.user, friend=friend)
    return redirect('friend_list')