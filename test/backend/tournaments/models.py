from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField("users.User", related_name='players_tournament')
    games = models.ManyToManyField("games.Game", related_name='games_tournament', blank=True)