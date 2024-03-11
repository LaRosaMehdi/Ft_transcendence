# Create your models here.

from django.db import models

# @admin.register(user)
class user(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100, null=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.username } - { self.email }"
    