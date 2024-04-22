import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse

from users.models import User
from games.models import Game 
from games.views.games import game_update
from aouth.views.jwt import jwt_login_required
from users.views.users import user_update_status, user_add_to_match_history, user_add_current_game, user_remove_current_game

logger = logging.getLogger(__name__)


# Remote mode
# -----------

@jwt_login_required
def remote_quit(request):
    current_game = request.user.current_game
    if current_game.player1 == request.user:
        game_update(request, current_game, -1, current_game.player2_score)
    else:
        game_update(request, current_game, current_game.player1_score, -1)
    return redirect('results')