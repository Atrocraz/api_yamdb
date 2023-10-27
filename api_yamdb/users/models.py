from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=settings.CONFIRMATION_CODE_LENGHT)
    email = models.CharField(
        'Электронная почта',
        unique=True,
        max_length=settings.EMAIL_MAX_LEN)
