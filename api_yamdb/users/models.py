from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )


class CustomUser(AbstractUser):
    username = models.CharField(
        'Никнейм пользователя',
        unique=True,
        max_length=settings.USERNAME_MAX_LEN)
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=settings.CONFIRMATION_CODE_LENGHT)
    email = models.CharField(
        'Электронная почта',
        unique=True,
        max_length=settings.EMAIL_MAX_LEN)
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    role = models.CharField(
        'Права доступа',
        max_length=10,
        blank=False,
        choices=ROLE_CHOICES
    )
