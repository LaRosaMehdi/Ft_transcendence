import logging
from django.http import JsonResponse
from matchmaking.models import MatchmakingQueue
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from users.models import User
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

# Remote queue
# ------------

@jwt_login_required
def queue_remote_add(request, player=None):
    user = request.user if player is None else player
    default_queue, created = MatchmakingQueue.objects.get_or_create(name="remote queue")
    if user not in default_queue.players.all():
        default_queue.players.add(user)
    return JsonResponse({'message': 'Vous êtes maintenant en file d\'attente pour un match.'})

@jwt_login_required
def queue_remote_remove(request, player=None):
    user = request.user if player is None else player
    try:
        default_queue = MatchmakingQueue.objects.get(name="remote queue")
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'La file d\'attente n\'existe pas.'})

    if user in default_queue.players.all():
        default_queue.players.remove(user)

    return JsonResponse({'message': 'Vous avez quitté la file d\'attente.'})