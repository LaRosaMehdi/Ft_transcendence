import requests, logging
from matchmaking.views.matchmaking import matchmaking
from aouth.views.jwt import jwt_login_required, jwt_decode

logger = logging.getLogger(__name__)

@jwt_login_required
def view_matchmaking(request):
    user = jwt_decode(request)
    logger.debug(f"Matchmaking user: {user}")
    return matchmaking(request)