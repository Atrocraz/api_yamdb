from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser


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
    username = serializers.RegexField(regex='^[\w.@+-]+\Z',
                                      required=True,
                                      max_length=settings.USERNAME_MAX_LEN)
    email = serializers.CharField(
        max_length=settings.EMAIL_MAX_LEN,
        required=True,
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='This email is already registered!'),])
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'confirmation_code')
        read_only_fields = ('id', 'password', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined')

    def validate_username(self, value):
        'Валидатор поля username.'

        if value == 'me':
            raise serializers.ValidationError("This username is forbidden!")
        return value
