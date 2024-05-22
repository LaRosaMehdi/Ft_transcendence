import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

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


@jwt_login_required
def game_end_quit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            score_player1 = data.get('scorePlayer1')
            score_player2 = data.get('scorePlayer2')

            current_game = request.user.current_game
            if current_game.player1 == request.user:
                game_update(request, current_game, score_player1, score_player2)
            else:
                game_update(request, current_game, score_player1, score_player2)
            
            return JsonResponse({'status': 'success', 'message': 'Match done', 'redirectUrl': 'results'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


""" def game_end_quit(request):
    logger.info("DEBUG_00")
    current_game = request.user.current_game
    data = json.loads(request.body)
    score_player1 = data.get('scorePlayer1')
    score_player2 = data.get('scorePlayer2')
    if current_game.player1 == request.user:
        game_update(request, current_game, score_player1, score_player2)
    else:
        game_update(request, current_game, score_player1, score_player2)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Match done',
            'redirectUrl': 'results',
        })
    else:
        return redirect('results') """