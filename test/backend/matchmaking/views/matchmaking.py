import logging
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from users.views.users import user_update_status
from games.views.games import game_init
from matchmaking.views.queue import queue_remote_add, queue_remote_remove
from matchmaking.models import MatchmakingQueue
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

# Default queue management
# ------------------------

@jwt_login_required
def matchmaking_remote_leave(request):
    queue_remote_remove(request)
    return redirect('home')

@jwt_login_required
def matchmaking_remote_make(request):
    default_queue = MatchmakingQueue.objects.get(name="remote queue")
    players = default_queue.players.all()

    while players.count() >= 2:
        player1 = players.first()
        player2 = players.exclude(pk=player1.pk).first()
        logger.info(f"player1: {player1}")
        logger.info(f"player2: {player2}")
        new_game = game_init(request, player1, player2)
        queue_remote_remove(request, player1)
        queue_remote_remove(request, player2)
        return True
    return False

@jwt_login_required
def matchmaking_remote(request):
    if request.user.status == "ingame":
        return redirect('play')
    try:
        default_queue = MatchmakingQueue.objects.get(name="remote queue")
    except ObjectDoesNotExist:
        queue_remote_add(request)
        default_queue = MatchmakingQueue.objects.get(name="remote queue")

    if request.user not in default_queue.players.all():
        queue_remote_add(request)

    if matchmaking_remote_make(request) is True:
        return redirect('play') 
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_matchmaking_remote.html', {'current_user': request.user})
        return JsonResponse({'html': html})
    else:    
        return render(request, 'matchmaking_remote.html', {'current_user': request.user})
