from django import forms
from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from tournaments.models import *

class generateTournamentForm(forms.Form):
    name = forms.CharField(label='Name', max_length=150, required=True)
    nb_players = forms.ChoiceField(label='Number of players', choices=[(4, '4'), (8, '8')], required=True)
    user_alias = forms.CharField(label='User alias', max_length=150, required=True)

class ConnectTournamentForm(forms.Form):
    user_alias = forms.CharField(label='User alias', max_length=150, required=True)
    tournament_name = forms.CharField(label='Tournament Name', max_length=150, required=True)
