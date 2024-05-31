import logging
from django.shortcuts import render
from django.http import JsonResponse
from users.views.users import user_get_last_game
from aouth.views.jwt import jwt_login_required, jwt_decode
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

# Base views
# -----------

@jwt_login_required
def view_play(request, game_id=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_play.html', {'game_id': game_id, 'game': user_get_last_game(request)})
        return JsonResponse({'html': html})
    else:
        return render(request, 'play.html', {'game_id': game_id, 'game': user_get_last_game(request)})

@jwt_login_required
def view_mode(request):
    user = jwt_decode(request)
    logger.debug(f"Mode user: {user}")
    return render(request, 'mode.html')

@jwt_login_required
def view_results(request):
    context = user_get_last_game(request)
    if context.winner == request.user:
        request.user.wins += 1
        request.user.elo += 100
    elif context.draw == 0:
        request.user.losses += 1
        request.user.elo -= 100
    request.user.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('results.html', {'game': user_get_last_game(request)}, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'results.html', {'game': user_get_last_game(request)})

# Modes
# -----

@jwt_login_required
def view_remote(request):
    user = jwt_decode(request)
    logger.debug(f"Remote user: {user}")
    return render(request, 'remote.html')

@jwt_login_required
def view_vscomputer(request):
    user = jwt_decode(request)
    logger.debug(f"Remote user: {user}")
    return render(request, 'vscomputer.html')

# Others ??
# ---------

@jwt_login_required
def view_main_chat(request):
    user = jwt_decode(request)
    logger.debug(f"Remote user: {user}")
    return render(request, 'main_chat.html')

@jwt_login_required
def view_game_in_progress(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_game_progress.html', request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'game_progress.html')