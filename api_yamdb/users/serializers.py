import math
import random

from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


class UserCodeSerializer(serializers.ModelSerializer):
    '''Класс-сериализатор для модели CustomUser

    Поле username проходит валидацию как регулярное выражение,
    ограничено в длине переменной USERNAME_MAX_LEN и не может
    быть равно значению 'me'.
    Поле confirmation_code доступно только для записи и не
    отправляет пользователю в ответе на запрос.
    Поле email проверяется на уникальность и ограничено в длине
    переменной EMAIL_MAX_LEN.
    '''
    username = serializers.RegexField(
        regex='^[\w.@+-]+\Z',
        required=True,
        max_length=settings.USERNAME_MAX_LEN,
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='This username is already registered!'),])
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LEN,
        allow_blank=False,
        required=True,
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='This email is already registered!'),])
    role = serializers.HiddenField(
        default='user')
    confirmation_code = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'confirmation_code', 'role')
        read_only_fields = ('id', 'password', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined',
                            'first_name', 'last_name', 'bio', 'role',
                            'confirmation_code')

    def get_confirmation_code(self, value):
        "Функция генерации кода подтверждения."
        string = ('0123456789abcdefghijklmnopqrstuvwxyz'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        OTP = ""
        length = len(string)
        for i in range(settings.CONFIRMATION_CODE_LENGHT):
            OTP += string[math.floor(random.random() * length)]

        return OTP

    def to_representation(self, obj):
        ret = super(UserCodeSerializer, self).to_representation(obj)
        ret.pop('confirmation_code')
        return ret

    def validate_username(self, value):
        'Валидатор поля username.'

        if value == 'me':
            raise serializers.ValidationError("This username is forbidden!")
        return value


class UserJWTSerializer(serializers.ModelSerializer):
    '''Класс-сериализатор для модели CustomUser
    '''
    username = serializers.RegexField(
        regex='^[\w.@+-]+\Z',
        required=True,
        max_length=settings.USERNAME_MAX_LEN)
    confirmation_code = serializers.CharField(
        write_only=True,
        required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
        read_only_fields = ('id', 'password', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined',
                            'first_name', 'last_name', 'bio', 'role', 'email')

    def validate_username(self, value):
        'Валидатор поля username.'

        if value == 'me':
            raise serializers.ValidationError("This username is forbidden!")
        return value


class UserSerializer(serializers.ModelSerializer):
    '''Класс-сериализатор для модели CustomUser

    Поле username проходит валидацию как регулярное выражение,
    ограничено в длине переменной USERNAME_MAX_LEN и не может
    быть равно значению 'me'.
    Поле confirmation_code доступно только для записи и не
    отправляет пользователю в ответе на запрос.
    Поле email проверяется на уникальность и ограничено в длине
    переменной EMAIL_MAX_LEN.
    '''
    username = serializers.RegexField(
        regex='^[\w.@+-]+\Z',
        required=True,
        max_length=settings.USERNAME_MAX_LEN,
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='This username is already registered!'),])
    email = serializers.CharField(
        max_length=settings.EMAIL_MAX_LEN,
        required=True,
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='This email is already registered!'),])
    role = serializers.CharField(
        max_length=10,
        default='user')

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('id', 'password', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined',
                            'confirmation_code')

    def to_representation(self, obj):
        ret = super(UserSerializer, self).to_representation(obj)

        return ret

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

    def validate_username(self, value):
        'Валидатор поля username.'

        if value == 'me':
            raise serializers.ValidationError("This username is forbidden!")
        return value
