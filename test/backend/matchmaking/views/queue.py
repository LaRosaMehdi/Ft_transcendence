import logging
from django.http import JsonResponse
from matchmaking.models import MatchmakingQueue
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from users.models import User

logger = logging.getLogger(__name__)

@login_required
def queue_add_to_default(request, player=None):
    user = request.user if player is None else player
    default_queue, created = MatchmakingQueue.objects.get_or_create(name="default queue")
    if user not in default_queue.players.all():
        default_queue.players.add(user)
    return JsonResponse({'message': 'Vous êtes maintenant en file d\'attente pour un match.'})

@login_required
def queue_remove_from_default(request, player=None):
    user = request.user if player is None else player
    try: default_queue = MatchmakingQueue.objects.get(name="default queue")
    except ObjectDoesNotExist: return
    if player in default_queue.players.all():
        default_queue.players.remove(player)
    return JsonResponse({'message': 'Vous avez quitté la file d\'attente.'})
    