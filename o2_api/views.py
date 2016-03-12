from o2_api.models import *
from o2_api.serializers import UserSerializer, GameSerializer, GameUserSerializer,UserVerfiedSerializers
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from o2_api.permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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


@api_view(['POST', 'GET'])
def device_validation(request):
    if request.method == 'GET':
        devices = GameUser.objects.all()[:10]
        serializer = GameUserSerializer(devices, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
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
        print(uuid)
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
	user_verify = UserVerified(user_id=device.id, message='your verification Code 323', message_status='created', verified_code='323')
#user_verify.save()
	device.phone_number = send_phone_number
	device.save()
	return Response({'id': '200', 'value': 'Message Send'})
    else:
        return Response({'id': '400', 'value': 'device Does Not Exist'})

# @api_view(['POST'])
# def create_auth(request):
#     serialized = RegisterSerializer(data=request.data)
#     if serialized.is_valid():
#         serialized.save()
#         return Response(serialized.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
