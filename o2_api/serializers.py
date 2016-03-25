__author__ = 'mousavi'
from django.contrib.auth import get_user_model
from rest_framework import serializers
from o2_api.models import *
# from django.contrib.auth.models import User

owner = serializers.ReadOnlyField(source='owner.username')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = get_user_model()


class GameSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'tournament', 'start_date', 'end_date', 'score', 'owner')


class TournamentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('tournament_name', 'start_date', 'end_date', 'max_user')


class GameUserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GameUser
        fields = ('uuid', 'phone_number', 'user_verified', 'created_at', 'gem_quantity', 'user')

class UserVerfiedSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserVerified
        fields = ('user', 'verified_code', 'created_at', 'message','message_status', 'verified_status')

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ("id", "name", "price", "gem_quantity", "description")

class LeaderBoardSerializer(serializers.Serializer):
    user__username = serializers.CharField(max_length=500)
    gmax = serializers.IntegerField()
    current_user = serializers.CharField(max_length=200)
