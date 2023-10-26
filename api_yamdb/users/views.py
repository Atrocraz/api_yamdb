import math
import random

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_confirmation_code(request):
    '''API-view функция регистрации пользователя.

    Ожидает на вход поля username и email.
    В качестве ответа на запрос возвращает поля username и email.
    Отправляет пользователю код подтверждения на почту и
    Сохраняет его в базу данных для последующей сверки.
    '''
    pass_data = request.data
    user = CustomUser.objects.filter(username=pass_data.get('username'),
                                     email=pass_data.get('email'))
    conf_code = get_confirmation_code()
    pass_data['confirmation_code'] = conf_code
    if user.first():
        serializer = UserSerializer(user.first(), data=pass_data)
        resp_status = status.HTTP_200_OK
    else:
        serializer = UserSerializer(data=pass_data)
        resp_status = status.HTTP_201_CREATED

    if serializer.is_valid():
        send_conf_code(pass_data.get('email'), conf_code)
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
        serializer = UserSerializer(user.first(), data=request.data)
        if serializer.is_valid():
            refresh = RefreshToken.for_user(user.first())
            response_data = {'token': str(refresh.access_token)}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response([{'detail': 'User not found'}],
                    status=status.HTTP_404_NOT_FOUND)


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
    for i in range(20):
        OTP += string[math.floor(random.random() * length)]

    return OTP
