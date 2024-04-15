import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from users.models import User
from aouth.views import *
from tournaments.models import Tournament
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

@jwt_login_required
def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournaments/tournament_list.html', {'tournaments': tournaments})

@jwt_login_required
def create_tournament_view(request):
    if request.method == 'POST':
        tournament_name = request.POST.get('name')
        # Traitement des données du formulaire et création du tournoi
        # Redirection vers une autre page après la création du tournoi
        return HttpResponse("Tournament created successfully!")  # Exemple de réponse

    # Si la méthode HTTP est GET, afficher simplement la page HTML du formulaire
    return render(request, 'tournaments/templates/createPrivateTournament.html', {'current_user': request.user})  # Chemin correct vers le modèle HTML

@jwt_login_required
def join_tournament_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        tournament_id = request.POST.get('tournament_id')
        user, created = User.objects.get_or_create(username=user_name)
        # Enregistrer le joueur dans le tournoi spécifié par l'ID
        # Vous devez implémenter cette logique
        return HttpResponse("You've successfully joined the tournament!")  # Réponse temporaire, vous pouvez rediriger vers une autre page
    return render(request, 'tournaments/join_tournament.html')
