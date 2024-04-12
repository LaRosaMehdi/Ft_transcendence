import logging
from users.models import User
from users.views.users import user_update_status
from games.models import Game 
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

@jwt_login_required
def game_init(player1_id, player2_id):
    logger.debug(f"game_init: player1_id={player1_id}, player2_id={player2_id}")
    try: 
        player1 = User.objects.get(pk=player1_id.id)
        player2 = User.objects.get(pk=player2_id.id)
        new_game = Game.objects.create(
            player1=player1,
            player2=player2,
            player1_score=0,
            player2_score=0,
            winner_id=None
        )
        new_game.save()
        user_update_status(player1, "ingame")
        user_update_status(player2, "ingame")
        logger.debug(f"New game created: {new_game}")
        return new_game
    except Exception as e:
        logger.error(f"game_init error: {e}")
        return None
