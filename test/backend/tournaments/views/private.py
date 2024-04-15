import logging
from django.shortcuts import render
from django.http import HttpResponse

from users.models import User
from aouth.views import *
from tournaments.models import Tournament
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

@jwt_login_required
def create_private_tournament_view(request):
    if request.method == 'POST':
        tournament_name = request.POST.get('name')
        # Traitement des données du formulaire et création du tournoi
        # Redirection vers une autre page après la création du tournoi
        return HttpResponse("Tournament created successfully!")  # Exemple de réponse

    # Si la méthode HTTP est GET, afficher simplement la page HTML du formulaire
    return render(request, 'createPrivateTournament.html', {'current_user': request.user})  # Chemin correct vers le modèle HTML

