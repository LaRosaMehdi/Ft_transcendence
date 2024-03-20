from django.db import models
from users.models import User

class MatchmakingQueue(models.Model):
    players = models.ManyToManyField("users.User", related_name='matchmaking_queues')

