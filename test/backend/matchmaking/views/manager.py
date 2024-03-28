import logging
from matchmaking.models import MatchmakingQueue
from games.views.games import game_init
# 
logger = logging.getLogger(__name__)

def matchmaking_manager(self):
    try:
        default_queue = MatchmakingQueue.objects.get(name="default queue")
        players = default_queue.players.all()

        while players.count() >= 2:
            player1 = players.first()
            player2 = players.exclude(pk=player1.pk).first()

            logger.debug(f"Matched players: {player1.username} and {player2.username}")
            new_game = game_init(player1, player2)

            default_queue.players.remove(player1)
            default_queue.players.remove(player2)

    except ObjectDoesNotExist:
        logger.error("Default matchmaking queue does not exist.")