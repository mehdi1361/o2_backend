__author__ = 'mousavi'
from rest_framework import serializers
from o2_api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Game
        fields = ('id', 'name', 'password', 'join_date')

class TournamentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('tournament_name', 'start_date', 'end_date', 'max_user')

# class GameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Game
#         fields = ('tournament_name','start_date','end_date','max_user')