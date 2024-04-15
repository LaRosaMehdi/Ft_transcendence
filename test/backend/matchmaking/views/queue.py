import logging
from django.http import JsonResponse
from matchmaking.models import MatchmakingQueue
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from users.models import User
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)


# Queue Middleware
# ----------------

# class QueueRemoveFromDefaultAutoMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         if request.user.is_authenticated and not request.path.startswith('/matchmaking/') and not request.path.startswith('/games/play'):
#             logger.debug(f"Removing {request.user} from default queue")
#             queue_remove_from_default(request)
#         return response

# Queue management
# ----------------

@jwt_login_required
def queue_add_to_default(request, player=None):
    user = request.user if player is None else player
    default_queue, created = MatchmakingQueue.objects.get_or_create(name="default queue")
    if user not in default_queue.players.all():
        default_queue.players.add(user)
    return JsonResponse({'message': 'Vous êtes maintenant en file d\'attente pour un match.'})

@jwt_login_required
def queue_remove_from_default(request, player=None):
    user = request.user if player is None else player
    try: default_queue = MatchmakingQueue.objects.get(name="default queue")
    except ObjectDoesNotExist: return
    if player in default_queue.players.all():
        default_queue.players.remove(player)
        logger.debug(f"Removed {player} from default queue")
    # print all players in queue
    players = default_queue.players.all()
    for player in players:
        print(player.username)
    if players.count() == 0:
        logger.debug(f"Queue is empty")
    return JsonResponse({'message': 'Vous avez quitté la file d\'attente.'})
