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
    return render(request, 'tournament.html')

@jwt_login_required
def view_tournament_generate(request):
    return render(request, 'createTournament.html', {'current_user': request.user, 'form': generateTournamentForm()})

@jwt_login_required
def view_tournament_join(request):
    return render(request, 'joinTournament.html', {'current_user': request.user, 'form': ConnectTournamentForm()})

@jwt_login_required
def view_tournament_dashboard(request, tournament_name):
    tournament = Tournament.objects.get(name=tournament_name)
    if tournament and tournament.players.filter(username=request.user.username).exists() is False:
        messages.error(request, 'Please join the tournament before accessing the dashboard', extra_tags='tournament_join')
        return render(request, 'joinTournament.html', {'current_user': request.user, 'form': ConnectTournamentForm()})
    return render(request, 'dashboardTournament.html', {'tournament_name': tournament_name})

@jwt_login_required
def view_tournament_play(request, tournament_name, game_id):
    game = Game.objects.get(id=game_id)
    players = {
        'player1': game.player1,
        'player2': game.player2
    }
    return render(request, 'playTournament.html', {'tournament_name': tournament_name, 'game_id': game_id, 'game': players})