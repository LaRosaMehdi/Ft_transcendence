from .models import *
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth import logout

admin.site.register(User)