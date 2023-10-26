from rest_framework import serializers

from users.models import CustomUser

EMAIL_MAX_LEN = 254
USERNAME_MAX_LEN = 150


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
                                      required=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'confirmation_code')
        read_only_fields = ('id', 'password', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined')

    def validate_username(self, value):
        'Валидатор поля username.'
        if len(value) > USERNAME_MAX_LEN:
            raise serializers.ValidationError()

        if value == 'me':
            raise serializers.ValidationError("This username is forbidden!")
        return value

    def validate_email(self, value):
        'Валидатор поля email.'
        if len(value) > EMAIL_MAX_LEN:
            raise serializers.ValidationError()

        if CustomUser.objects.filter(email__exact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered!")
        return value
