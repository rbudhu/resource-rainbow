from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.auth.models import Group, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=140, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']
