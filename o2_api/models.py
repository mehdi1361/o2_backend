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

class Game(models.Model):
    owner = models.ForeignKey('auth.User', related_name='games')
    tournament = models.ForeignKey(Tournament)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    score = models.IntegerField()

    class Meta:
        ordering = ('score', 'owner')
