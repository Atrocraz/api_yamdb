from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )


class CustomUser(AbstractUser):
    "Кастомная модель пользователя."

    username = models.CharField(
        'Никнейм пользователя',
        unique=True,
        help_text=('Обязательное. 150 знаков или менее. Допустимы буквы, '
                   'цифры и @/./+/-/_.'),
        max_length=settings.USERNAME_MAX_LEN)
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=settings.CONFIRMATION_CODE_LENGHT)
    email = models.EmailField('Электронная почта',
                              unique=True,
                              max_length=settings.EMAIL_MAX_LEN)
    first_name = models.CharField(('Имя'), max_length=150, blank=True)
    last_name = models.CharField(('Фамилия'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        ('Статус сотрудника'),
        default=False,
        help_text=('Определяет, может ли пользователь войти в админ-панель.'),
    )
    is_active = models.BooleanField(
        ('Активен'),
        default=True,
        help_text=('Определяет, считать ли пользователя активным. '
                   'Отключите вместо удаления пользователя.'),
    )
    date_joined = models.DateTimeField(('Дата регистрации'),
                                       default=timezone.now)
    bio = models.TextField('О себе', blank=True)
    role = models.CharField('Права доступа',
                            max_length=10,
                            blank=False,
                            choices=ROLE_CHOICES)

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True
        return False

    @property
    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False
