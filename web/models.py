from django.db import models
from account.models import User


class Status(models.Model):
    name = models.CharField(max_length=140, unique=True)
    active = models.BooleanField(default=True)


class Skill(models.Model):
    name = models.CharField(max_length=140, unique=True)
    active = models.BooleanField(default=True)


class UserStatus(models.Model):
    user = models.ForeignKey(User)
    status = models.ForeignKey(Status)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)


class UserSkill(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
