import urllib.request, os, logging
from django.db import models
from django.core.files import File
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
   
    def create_user(self, username, email=None, password=None, image_url=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        if image_url is None:
            image_url = 'http://www.gravatar.com/avatar/?d=identicon'
        result = urllib.request.urlretrieve(image_url)
        user.image.save(
            os.path.basename(image_url),
            File(open(result[0], 'rb'))
        )
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        email = self.normalize_email(email) if email else 'default@student.42nice.fr'
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)  # Call _create_user instead of create_user

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    elo = models.IntegerField(default=1000)
    password = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='', null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Add this line
    is_connected = models.BooleanField(default=True)

    last_login = models.DateTimeField(auto_now=True)

    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    alias = models.CharField(max_length=100, null=True, blank=True)
    match_history = models.ManyToManyField('games.Game', related_name="match_history_user", blank=True) 

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
