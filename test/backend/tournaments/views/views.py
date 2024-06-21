import logging
from django.shortcuts import render

from users.models import User
from aouth.views import *
from tournaments.models import Tournament
from aouth.views.jwt import jwt_login_required
from tournaments.views.tournaments import *
from tournaments.views.forms import *

logger = logging.getLogger(__name__)

@jwt_login_required
def view_resTournoi(request):
    return render(request, 'resTournoi.html')


@jwt_login_required
def view_tournament(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_tournament.html', request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'tournament.html')

@jwt_login_required
def view_tournament_generate(request):
    logger.info("DEBUG_view_tournament_generate")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_createTournament.html', {'current_user': request.user, 'form': generateTournamentForm()}, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'createTournament.html', {'current_user': request.user, 'form': generateTournamentForm()})

@jwt_login_required
def view_tournament_join(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('joinTournament.html', {'current_user': request.user, 'form': ConnectTournamentForm()}, request=request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'joinTournament.html', {'current_user': request.user, 'form': ConnectTournamentForm()})

# @jwt_login_required
# def view_tournament_dashboard(request, tournament_name):
#     logger.info("DEBUG_dashborad")
#     tournament = Tournament.objects.get(name=tournament_name)
#     if tournament and tournament.players.filter(username=request.user.username).exists() is False:
#         messages.error(request, 'Please join the tournament before accessing the dashboard', extra_tags='tournament_join')
#         return render(request, 'joinTournament.html', {'current_user': request.user, 'form': ConnectTournamentForm()})
#     return render(request, 'dashboardTournament.html', {'tournament_name': tournament_name})

@jwt_login_required
def view_tournament_dashboard(request, tournament_name):
    tournament = Tournament.objects.get(name=tournament_name)
    if tournament and not tournament.players.filter(username=request.user.username).exists():
        messages.error(request, 'Please join the tournament before accessing the dashboard', extra_tags='tournament_join')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('joinTournament.html', {'current_user': request.user, 'form': ConnectTournamentForm()}, request)
            return JsonResponse({'html': html, 'redirect': 'joinTournament'})
        else:
            return render(request, 'joinTournament.html', {'current_user': request.user, 'form': ConnectTournamentForm()})
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboardTournament.html', {'tournament_name': tournament_name}, request)
        return JsonResponse({'html': html, 'redirect': 'dashboardTournament'})
    else:
        return render(request, 'dashboardTournament.html', {'tournament_name': tournament_name})

@jwt_login_required
def view_tournament_play(request, tournament_name, game_id):
    game = Game.objects.get(id=game_id)
    players = {
        'player1': game.player1,
        'player2': game.player2
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('playTournament.html', {'tournament_name': tournament_name, 'game_id': game_id, 'game': players}, request)
        return JsonResponse({'html': html})
    else:
        return render(request, 'playTournament.html', {'tournament_name': tournament_name, 'game_id': game_id, 'game': players})

@jwt_login_required
def view_tournament_in_progress(request):
    tournament_name = request.GET.get('tournament_name', '')
    context = {'tournament_name': tournament_name}

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('tournament_in_progress.html', context=context, request=request)
        return JsonResponse({'html': html})
    else:
        logger.info("View tournament progress call")
        return render(request, 'tournament_in_progress.html', context)
