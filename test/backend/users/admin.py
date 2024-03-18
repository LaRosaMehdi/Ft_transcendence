from django.contrib import admin
from .models import User
from django.contrib.auth import logout
from django.urls import reverse

admin.site.register(User)