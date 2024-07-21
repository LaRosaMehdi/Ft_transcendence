from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User

class MatchmakingQueue(models.Model):
    name = models.CharField(max_length=255)
    players = models.ManyToManyField(User, related_name="players", blank=True)

    def __str__(self):
        return f"{self.name} - {self.players.count()}"