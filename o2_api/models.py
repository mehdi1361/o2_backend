from __future__ import unicode_literals

from django.db import models

class Tournament(models.Model):
    tournament_name = models.CharField(max_length=80)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_user = models.IntegerField(max_length=5)

    class Meta:
        ordering = ('end_date',)

# Create your models here.
class User_Game(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    join_date = models.DateTimeField()

    class Meta:
        ordering = ('join_date',)

class Game(models.Model):
    user = models.ForeignKey(User_Game)
    tournament = models.ForeignKey(Tournament)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    score = models.IntegerField()

    class Meta:
        ordering = ('score',)
