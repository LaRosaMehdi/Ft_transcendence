from django.db import models
from users.models import User

class Game(models.Model):
    LEVEL_CHOICES = [
        ('pool', 'Pool'),
        ('quarter_final', 'Quarter Final'),
        ('semi_final', 'Semi Final'),
        ('final', 'Final'),
        ('final', 'Final'),
        ('none', 'None')
    ]

    player1 = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='player1_game', null=True, blank=True)
    player2 = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='player2_game', null=True, blank=True)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    winner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='won_game', null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    tournament = models.ForeignKey('tournaments.Tournament', on_delete=models.CASCADE, related_name='tournament_game', null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='none')
    draw = models.IntegerField(default=0)
    def __str__(self):
        return f"[{self.tournament.name if  self.tournament is not None else 'DEFAULT GAME'}] {'Undefined' if self.player1 is None else self.player1.username} vs {'Undefined' if self.player2 is None else self.player2.username} : {self.player1_score} - {self.player2_score}"