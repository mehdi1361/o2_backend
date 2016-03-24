import random
from o2_api.models import *
from o2_api.serializers import UserSerializer, GameSerializer, GameUserSerializer, UserVerfiedSerializers, \
    LeaderBoardSerializer, TournamentSerializers
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from o2_api.permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from o2_api.infrastructure import send_verification_code
from django.db.models import Max
from datetime import datetime, timezone


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


@api_view(['POST'])
def create_user(request):
    try:
        send_uuid = request.data['uuid']
        username = request.data['username']
        devices = GameUser.objects.filter(uuid=send_uuid)[0]
        if devices:
            user = User.objects.filter(username=username)
            if user:
                return Response({'id': '304', 'Msg': 'UserRegisteredBefore'})
            else:
                new_user = User(username=username, password=123456)
                new_user.save()
                devices.user = new_user
                devices.save()
                return Response({'id': '304', 'Msg': 'user Created'})
        else:
            return Response({'id': '404', 'Msg': 'device not found'})
    except:
            return Response({'id': '500', 'Msg': 'Parameter Error'})
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
            return Response({'id': '404', 'Msg': 'cant find device id'})
    if request.method == 'POST':
        try:
            now = datetime.now(timezone.utc)
            tournament = Tournament.objects.filter(end_date__gte=now).order_by('-id').exclude(id=1)[:1]
            send_uuid = request.data['uuid']
            devices = GameUser.objects.filter(uuid=send_uuid)
            if devices:
                user = None if not devices[0].user else devices[0].user.username
                print(user)
                if tournament:
                    result_dict = {'uuid': devices[0].uuid,
                                   'UserName': user,
                                   'IsVerified': devices[0].user_verified,
                                   'Gem': devices[0].gem_quantity,
                                   'MobileNumber': devices[0].phone_number,
                                   'IsGoldenTimeAvailable': True,
                                   'GoldenTimeStart': (tournament[0].start_date - now).total_seconds(),
                                   'GoldenTimeEnd': (tournament[0].end_date - now).total_seconds(),
                                   'GoldenTimeId': tournament[0].id,
                                   'Msg': 'ok'
                                   }
                    return Response(result_dict)
                else:
                    result_dict = {'uuid': devices[0].uuid,
                                   'username': user,
                                   'is_verified': devices[0].user_verified,
                                   'Gem': devices[0].gem_quantity,
                                   'MobileNumber': devices[0].phone_number,
                                   'IsGoldenTimeAvailable': False,
                                   'GoldenTimeStart': None,
                                   'GoldenTimeEnd': None,
                                   'GoldenTimeId': None,
                                   'msg': 'ok'
                                   }
                    return Response(result_dict)

            if not devices:
                serialized = GameUserSerializer(data=request.data)
                if serialized.is_valid():
                    serialized.save()
                    return Response(serialized.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'id': '500', 'Msg': 'Error patameter'})


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
    try:
        send_uuid = request.data['uuid']
        send_phone_number = request.data['phone']
        device = GameUser.objects.filter(uuid=send_uuid)[0]
        if device:
            if device.user_verified:
                return Response({'id': '200', 'Msg': 'AlreadyVerified'})
            else:
                verify_code = random.randrange(1000, 10000, 2)
                user_verify = UserVerified(user_id=device.id, message='your verification Code 323',
                                           message_status='created',
                                           verified_code=verify_code)
                send_verification_code(phone_number=send_phone_number, verification_code=verify_code)
                user_verify.save()
                device.phone_number = send_phone_number
                device.save()
                return Response({'id': '200', 'Msg': 'MessageSend'})
        else:
            return Response({'id': '400', 'Msg': 'DeviceDoesNotExist'})
    except:
        return Response({'id': '500', 'Msg': 'ErrorParameter'})


@api_view(['POST'])
def confirm_verification(request):
    try:
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
                return Response({'id': '200', 'Msg': 'user verified'})
            else:
                return Response({'id': '400', 'Msg': 'verification code not defined'})
        else:
            return Response({'id': '400', 'Msg': 'device or user Does Not Exist'})
    except:
        return Response({'id': '400', 'Msg': 'device or user Does Not Exist'})


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
            game = Game(owner=owner, tournament=tournament, start_date=start_date, score=score)
            game.save()
            return Response({'id': 200, 'Msg': 'Game saved'})

        except:
            return Response({'id': 404, 'Msg': 'bad request'})


@api_view(['POST'])
def game_leader_board(request):
    try:
        tournament_id = request.data['tournament']
        leader_board = GameUser.objects.filter(game__tournament=tournament_id).annotate(
            gmax=Max('game__score')).order_by('-gmax').values('user__username', 'gmax')
        serializer = LeaderBoardSerializer(leader_board, many=True)
        return Response(serializer.data)
    except:
        return Response({'id': '404', 'Msg': 'tournament not found'})


@api_view(['POST'])
def golden_tournament(request):
    tournament = Tournament.objects.order_by('-id').exclude(id=1)[:1]
    serializer = TournamentSerializers(tournament, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def buy_package(request):
    try:
        send_uuid = request.data['uuid']
        gem = request.data['gem']
        device = GameUser.objects.filter(uuid=send_uuid)[0]
        if device:
            device.gem_quantity += int(gem)
            device.save()
            return Response({'id': '200', 'Msg': 'buy gem succes'})
        else:
            return Response({'id': '404', 'Msg': 'cant find device id'})
    except:
        return Response({'id': '500', 'Msg': 'error in parameter'})


@api_view(['POST'])
def use_gem(request):
    try:
        send_uuid = request.data['uuid']
        gem = request.data['gem']
        device = GameUser.objects.filter(uuid=send_uuid)[0]
        if device:
            if device.gem_quantity > int(gem):
                device.gem_quantity -= int(gem)
                device.save()
                return Response({'id': '200', 'Msg': 'use gem succes'})
            else:
                return Response({'id': '304', 'Msg': 'mor than gem for user'})
        else:
            return Response({'id': '404', 'Msg': 'cant find device id'})
    except:
        return Response({'id': '500', 'Msg': 'error in parameter'})

# @api_view(['POST'])
# def create_auth(request):
#     serialized = RegisterSerializer(data=request.data)
#     if serialized.is_valid():
#         serialized.save()
#         return Response(serialized.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
