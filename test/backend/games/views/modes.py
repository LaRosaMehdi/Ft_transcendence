import logging
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from users.models import User
from games.models import Game 
from games.views.games import game_update
from aouth.views.jwt import jwt_login_required
from users.views.users import user_update_status, user_add_to_match_history, user_add_current_game, user_remove_current_game
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from users.views.users import user_update_status, user_remove_current_game
from games.views.games import game_update
from aouth.views.jwt import jwt_login_required
from games.models import Game
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
    return JsonResponse({'status': 'success'})

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


@jwt_login_required
@require_POST
def finishAndquit(request):
    logger.info("DEBUG VIEW finish and quit")
    try:
        data = json.loads(request.body)
        player1_score = data.get('player1_score')
        player2_score = data.get('player2_score')

        current_game = request.user.current_game

        # Validation des scores
        if not isinstance(player1_score, int) or not isinstance(player2_score, int):
            raise ValueError("Les scores des joueurs doivent être des entiers.")

        # Mettre à jour le jeu
        updated_game = game_update(request, current_game, player1_score, player2_score)
        if updated_game:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'}, status=500)
    except Exception as e:
        logger.error(f"Erreur lors de la fin du jeu : {e}")
        return JsonResponse({'status': 'error', 'message': 'Une erreur est survenue'}, status=500)

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