import logging
from django.http import JsonResponse
from matchmaking.models import MatchmakingQueue
from django.contrib.auth.decorators import login_required

from users.models import User

logger = logging.getLogger(__name__)

@login_required
def queue_add_to_default(request):
    user = request.user
    default_queue, created = MatchmakingQueue.objects.get_or_create(name="default queue")
    if user not in default_queue.players.all():
        default_queue.players.add(user)
    # for user in default_queue.players.all():
    #     logger.debug(f"User in default queue: {user.username}")
    return JsonResponse({'message': 'Vous êtes maintenant en file d\'attente pour un match.'})

