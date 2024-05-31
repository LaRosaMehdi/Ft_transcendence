import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from users.models import User
from games.models import Game 
from aouth.views.jwt import jwt_login_required
from users.views.users import *

logger = logging.getLogger(__name__)

# Middleware
# ----------

@jwt_login_required
def game_init(request, player1_id, player2_id):
    try:
        player1 = User.objects.get(pk=player1_id.id)
        player2 = User.objects.get(pk=player2_id.id)
        new_game = Game.objects.create(
            player1=player1,
            player2=player2,
            player1_score=0,
            player2_score=0,
            winner_id=None
        )
        new_game.save()
        user_update_status(request, player1, "ingame")
        user_add_to_match_history(request, player1, new_game)
        user_update_status(request, player2, "ingame")
        user_add_to_match_history(request, player2, new_game)
        user_add_current_game(request, player1, new_game)
        user_add_current_game(request, player2, new_game)
        return new_game
    except Exception as e:
        logger.error(f"game_init error: {e}")
        return None

@jwt_login_required
def game_update(request, game, player1_score, player2_score):
    try:
        game.player1_score = player1_score
        game.player2_score = player2_score
        if player1_score > player2_score:
            game.winner = game.player1
        elif player1_score < player2_score:
            game.winner = game.player2
        elif player1_score == player2_score:
            game.draw = 1
        game.save()
        # ELO
        user_update_status(request, game.player1, "online")
        user_update_status(request, game.player2, "online")
        user_remove_current_game(request, game.player1)
        user_remove_current_game(request, game.player2)
        return game
    except Exception as e:
        logger.error(f"game_update error: {e}")
        return None

@jwt_login_required
def check_status_user(request):
    logger.info(f"request: {request.user.status}")
    context = request.user.status
    return JsonResponse({'context': context})