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

class GameUser(models.Model):
    user = models.OneToOneField('auth.User', related_name='games',null=True)
    uuid = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13)
    user_verified = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    gem_quantity = models.IntegerField()

class Game(models.Model):
    owner = models.ForeignKey(GameUser)
    tournament = models.ForeignKey(Tournament)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    score = models.IntegerField()

    class Meta:
        ordering = ('score', 'owner')

class UserVerified(models.Model):
    user = models.ForeignKey(GameUser)
    verified_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)

class SendMessage(models.Model):
    user = models.ForeignKey(GameUser)
    message = models.CharField(max_length=500)
    message_status = models.CharField(max_length=5)

class BuyPackage(models.Model):
    user = models.ForeignKey(GameUser)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    gem_quantity = models.IntegerField()
