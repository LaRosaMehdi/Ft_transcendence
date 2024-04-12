import requests
from matchmaking.views.matchmaking import matchmaking
from aouth.views.jwt import jwt_login_required

@jwt_login_required
def view_matchmaking(request):
    return matchmaking(request)