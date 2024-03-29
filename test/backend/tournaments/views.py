from django.shortcuts import render
from .models import Tournament
from users.models import User

from .models import Tournament

def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournaments/tournament_list.html', {'tournaments': tournaments})


def create_tournament_view(request):
    if request.method == 'POST':
        tournament_name = request.POST.get('name')
        # Traitement des données du formulaire et création du tournoi
        # Redirection vers une autre page après la création du tournoi
        return HttpResponse("Tournament created successfully!")  # Exemple de réponse

    # Si la méthode HTTP est GET, afficher simplement la page HTML du formulaire
    return render(request, 'tournaments/create_tournament.html')  # Chemin correct vers le modèle HTML

def join_tournament_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        tournament_id = request.POST.get('tournament_id')
        user, created = User.objects.get_or_create(username=user_name)
        # Enregistrer le joueur dans le tournoi spécifié par l'ID
        # Vous devez implémenter cette logique
        return HttpResponse("You've successfully joined the tournament!")  # Réponse temporaire, vous pouvez rediriger vers une autre page
    return render(request, 'tournaments/join_tournament.html')