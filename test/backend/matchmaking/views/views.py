import requests, logging
from matchmaking.views.matchmaking import matchmaking_remote
from aouth.views.jwt import jwt_login_required, jwt_decode

logger = logging.getLogger(__name__)

@jwt_login_required
def view_matchmaking_remote(request):
    return matchmaking_remote(request)