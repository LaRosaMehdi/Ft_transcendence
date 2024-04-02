import logging
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from users.views.users import user_update_status
from games.views.games import game_init
from matchmaking.views.queue import queue_add_to_default, queue_remove_from_default
from matchmaking.models import MatchmakingQueue
 
logger = logging.getLogger(__name__)

@login_required
def matchmaking_make(request):
    default_queue = MatchmakingQueue.objects.get(name="default queue")
    players = default_queue.players.all()

    while players.count() >= 2:
        player1 = players.first()
        player2 = players.exclude(pk=player1.pk).first()
        logger.debug(f"Matched players: {player1.username} and {player2.username}")
        new_game = game_init(player1, player2)
        queue_remove_from_default(request, player1)
        queue_remove_from_default(request, player2)
        return True
    return False

@login_required
def matchmaking(request):
    if request.user.status == "ingame":
        return redirect('play')
    try:
        default_queue = MatchmakingQueue.objects.get(name="default queue")
    except ObjectDoesNotExist:
        queue_add_to_default(request)
        default_queue = MatchmakingQueue.objects.get(name="default queue")

    if request.user not in default_queue.players.all():
        queue_add_to_default(request)

    if matchmaking_make(request) is True:
        return redirect('play') 
    return render(request, 'matchmaking.html', {'current_user': request.user})