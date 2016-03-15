import random
from o2_api.models import *
from o2_api.serializers import UserSerializer, GameSerializer, GameUserSerializer, UserVerfiedSerializers
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from o2_api.permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from o2_api.infrastructure import send_verification_code

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameUserLIst(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Game.objects.filter()


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    model = get_user_model()
    permissin_classes = [
        permissions.AllowAny
        # Or anon users can't register
    ]
    serializer_class = UserSerializer


# noinspection PyBroadException
@api_view(['POST'])
def device_validation(request):
    if request.method == 'GET':
        try:
            send_uuid = request.data['uuid']
            devices = GameUser.objects.filter(uuid=send_uuid)[:1]
            serializer = GameUserSerializer(devices, many=True)
            return Response(serializer.data)
        except:
            return Response({'id': '404', 'message': 'cant find device id'})
    if request.method == 'POST':
            send_uuid = request.data['uuid']
            devices = GameUser.objects.filter(uuid=send_uuid)[:1]
            if devices:
                serializer = GameUserSerializer(devices, many=True)
                return Response(serializer.data)
            if not devices:
                serialized = GameUserSerializer(data=request.data)
                if serialized.is_valid():
                    serialized.save()
                    return Response(serialized.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def send_device_verified(request):
    if request.method == 'GET':
        uuid = request.GET.get('uuid')
        user_verified = UserVerified.objects.filter(user=uuid).order_by('-id')[:1]
        serializer = UserVerfiedSerializers(user_verified, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = UserVerfiedSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_verify(request):
    send_uuid = request.data['uuid']
    send_phone_number = request.data['phone']
    device = GameUser.objects.filter(uuid=send_uuid)[0]
    if device:
        verify_code = random.randrange(1000, 10000, 2)
        user_verify = UserVerified(user_id=device.id, message='your verification Code 323', message_status='created',
                                   verified_code=verify_code)
        send_verification_code(phone_number=send_phone_number, verification_code=verify_code)
        user_verify.save()
        device.phone_number = send_phone_number
        device.save()
        return Response({'id': '200', 'value': 'Message Send'})
    else:
        return Response({'id': '400', 'value': 'device Does Not Exist'})


@api_view(['POST'])
def confirm_verification(request):
    send_uuid = request.data['uuid']
    user_name = request.data['username']
    verification_code = request.data['code']
    device = GameUser.objects.filter(uuid=send_uuid)[0]
    user = User.objects.filter(username=user_name)[0]
    if device and user:
        verification = UserVerified.objects.filter(user=device.id).order_by('-id')[0]
        if verification.verified_code == verification_code:
            device.user = user
            device.user_verified = True
            device.save()
            verification.message_status = 'delivered'
            verification.verified_status = 'success'
            verification.save()
            return Response({'id': '200', 'value': 'user verified'})
        else:
            return Response({'id': '400', 'value': 'verification code not defined'})
    else:
        return Response({'id': '400', 'value': 'device or user Does Not Exist'})

@api_view(['POST'])
def game_score_register(request):
    if request.method == 'POST':
        try:
            send_uuid = request.data['uuid']
            tournament_id = request.data['tournament']
            start_date = request.data['start_date']
            score = request.data['score']
            owner = GameUser.objects.get(uuid=send_uuid)
            tournament = Tournament.objects.get(pk=tournament_id)
            print(type(owner))
            game = Game(owner=owner, tournament=tournament, start_date=start_date,score=score)
            game.save()
            return Response({'id': 200, 'message': 'Game saved'})

        except:
            return Response({'id': 404, 'message': 'bad request'})

@api_view(['POST'])
def game_leader_board(request):
    tournament_id = request.data['tournament']


# @api_view(['POST'])
# def create_auth(request):
#     serialized = RegisterSerializer(data=request.data)
#     if serialized.is_valid():
#         serialized.save()
#         return Response(serialized.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
