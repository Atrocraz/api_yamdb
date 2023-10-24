from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    confirmation_code = models.TextField('Код подтверждения', blank=True)
