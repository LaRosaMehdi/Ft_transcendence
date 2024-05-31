from django.db import models
from users.models import User

class Game(models.Model):
    player1 = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='player1_game')
    player2 = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='player2_game')
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    winner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='won_game', null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    draw = models.IntegerField(default=0)
    # tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='games', null=True, blank=True)

    def __str__(self):
        return f"{self.player1.username} vs {self.player2.username} : {self.player1_score} - {self.player2_score}"