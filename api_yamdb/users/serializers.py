import math
import random

from django.conf import settings
from django.http import Http404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import CustomUser

ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
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
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=settings.USERNAME_MAX_LEN,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(),
                            message='This username is already registered!'),])
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LEN,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(),
                            message='This email is already registered!'),])
    role = serializers.HiddenField(default='user')
    confirmation_code = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'confirmation_code', 'role')
        read_only_fields = ('id', 'password', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined',
                            'first_name', 'last_name', 'bio', 'role')

    def get_confirmation_code(self):
        "Функция генерации кода подтверждения."
        string = ('0123456789abcdefghijklmnopqrstuvwxyz'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        OTP = ""
        length = len(string)
        for i in range(settings.CONFIRMATION_CODE_LENGHT):
            OTP += string[math.floor(random.random() * length)]

        return OTP

    def validate(self, data):
        confirmation_code = self.get_confirmation_code()
        validated_data = super(UserCodeSerializer, self).validate(data)
        validated_data['confirmation_code'] = confirmation_code
        return validated_data

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
    "Класс-сериализатор для отправки пользователю JWT-токена"

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
        read_only_fields = ('id', 'password', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined',
                            'first_name', 'last_name', 'bio', 'role', 'email')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = CustomUser.objects.filter(username=username).first()

        if user:
            if user.confirmation_code == confirmation_code:
                return data

            raise serializers.ValidationError(
                {"confirmation_code": "Confirmation code is wrong."})

        raise Http404("User does not exist.")


class UserSerializer(serializers.ModelSerializer):
    "Класс-сериализатор для модели CustomUser"

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=settings.USERNAME_MAX_LEN,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(),
                            message='This username is already registered!'),])
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LEN,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(),
                            message='This email is already registered!'),])
    role = serializers.ChoiceField(default='user', choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        read_only_fields = ('id', 'password', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined',
                            'confirmation_code')

    def validate(self, data):
        # Запрет на изменение роли, если обрабатывается
        # эндпоинт users/me/
        if self.context.get('action', None) == 'patchme':
            if 'role' in data:
                data.pop('role')

        return data

    def validate_username(self, value):
        'Валидатор поля username.'

        if value == 'me':
            raise serializers.ValidationError("This username is forbidden!")
        return value