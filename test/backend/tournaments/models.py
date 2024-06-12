# models.py

from django.db import models
from users.models import User

class Tournament(models.Model):
    LEVEL_CHOICES = [
        ('pool', 'Pool'),
        ('quarter_final', 'Quarter Final'),
        ('semi_final', 'Semi Final'),
        ('final', 'Final'),
        ('finished', 'Finished'),
        ('none', 'None')
    ]
    name = models.CharField(max_length=100, unique=True)
    nb_players = models.IntegerField(default=4)
    players = models.ManyToManyField(User, related_name='players_tournament')
    games = models.ManyToManyField('games.Game', related_name='games_tournament', blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='none')

    current_game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='current_game', null=True, blank=True)

    first_place = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_place', null=True, blank=True)
    second_place = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_place', null=True, blank=True)
    third_place = models.ForeignKey(User, on_delete=models.CASCADE, related_name='third_place', null=True, blank=True)
    fourth_place = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fourth_place', null=True, blank=True)
    fifth_place = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fifth_place', null=True, blank=True)
    sixth_place = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sixth_place', null=True, blank=True)
    seventh_place = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seventh_place', null=True, blank=True)
    eighth_place = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eighth_place', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.nb_players} player tournament"


# class TournamentMatchQueue(models.Model):
#     tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
#     player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1_match_tournament')
#     player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2_match_tournament')
#     winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won_match_tournament', null=True, blank=True)
#     status = models.CharField(max_length=20, default='scheduled')
#     date_time = models.DateTimeField(auto_now_add=True)

# class TournamentMatchLoserQueue(models.Model):
#     tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
#     player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournament_loser')
#     next_opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='next_opponent', null=True, blank=True)
#     status = models.CharField(max_length=20, default='active')
