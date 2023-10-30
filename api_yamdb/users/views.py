import math
import random

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserCodeSerializer, UserJWTSerializer, UserSerializer
from .permissions import IsAdmin


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_confirmation_code(request):
    '''API-view функция регистрации пользователя.

    Ожидает на вход поля username и email.
    В качестве ответа на запрос возвращает поля username и email.
    Отправляет пользователю код подтверждения на почту и
    Сохраняет его в базу данных для последующей сверки.
    '''
    user = CustomUser.objects.filter(username=request.data.get('username'),
                                     email=request.data.get('email'))
    if user.first():
        serializer = UserCodeSerializer(user.first(), data=request.data)
        resp_status = status.HTTP_200_OK
    else:
        serializer = UserCodeSerializer(data=request.data)
        resp_status = status.HTTP_200_OK

    if serializer.is_valid():
        send_conf_code(request.data.get('email'),
                       request.data.get('confirmation_code'))
        serializer.save()
        return Response(serializer.data, status=resp_status)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    '''API-view функция отправки JWT-кода.

    Ожидает на вход поля username и confirmation_code.
    В качестве ответа на запрос возвращает JWT-токен.
    '''
    user = CustomUser.objects.filter(
        username=request.data.get('username'),
        confirmation_code=request.data.get('confirmation_code'))
    if user.first():
        serializer = UserJWTSerializer(user.first(), data=request.data)
        if serializer.is_valid():
            refresh = RefreshToken.for_user(user.first())
            response_data = {'token': str(refresh.access_token)}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.filter(username=request.data.get('username'))
    if user.first():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if 'username' in request.data:
        return Response([{'detail': 'User not found'}],
                        status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = LimitOffsetPagination


def send_conf_code(email, conf_code):
    "Функция-шорткат для отправки письма."
    send_mail(
        subject='[YaMDB] Код подтверждения',
        message=('Добрый день!\n'
                 f'Ваш код подтверждения - {conf_code}'),
        from_email='from@example.com',
        recipient_list=[email],
        fail_silently=True,
    )


def get_confirmation_code():
    "Функция генерации кода подтверждения."
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(settings.CONFIRMATION_CODE_LENGHT):
        OTP += string[math.floor(random.random() * length)]

    return OTP
