from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Tournament(models.Model):
    tournament_name = models.CharField(max_length=80)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_user = models.IntegerField()

    class Meta:
        ordering = ('end_date',)

    def __str__(self):
        return self.tournament_name


class GameUser(models.Model):
    user = models.OneToOneField('auth.User', related_name='games', null=True)
    uuid = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13, null=True)
    user_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    gem_quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Game(models.Model):
    owner = models.ForeignKey(GameUser)
    tournament = models.ForeignKey(Tournament)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(auto_now=True)
    score = models.IntegerField()

    class Meta:
        ordering = ('score', 'owner')

class UserVerified(models.Model):
    user = models.ForeignKey(GameUser)
    verified_code = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=500,null=True)
    message_status = models.CharField(max_length=5, null=True)
    verified_status = models.BooleanField(default=False)

class Package(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    gem_quantity = models.IntegerField()
    description = models.CharField(max_length=200)

class BuyPackage(models.Model):
    user = models.ForeignKey(GameUser)
    package = models.ForeignKey(Package)
    created_at = models.DateTimeField(auto_now=True)
    operator_validation = models.BooleanField(default=False)



