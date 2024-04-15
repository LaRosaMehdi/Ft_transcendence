import logging
from django.shortcuts import render

from users.models import User
from aouth.views import *
from tournaments.models import Tournament
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

@jwt_login_required
def tournament_view(request):
    return render(request, 'tournament.html')

@jwt_login_required
def view_resTournoi(request):
    return render(request, 'resTournoi.html')