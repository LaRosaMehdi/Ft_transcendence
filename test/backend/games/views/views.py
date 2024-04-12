from django.shortcuts import render

from aouth.views.jwt import jwt_login_required

@jwt_login_required
def view_play(request):
    return render(request, 'play.html', {'current_user': request.user})

