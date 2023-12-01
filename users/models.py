from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class User(AbstractUser):
    username = None

    tg_id = models.BigIntegerField(
        verbose_name='Telegram_id',
        null=True,
        blank=True
    )
    tg_username = models.CharField(
        unique=True,
        max_length=60,
        verbose_name='Ник в тг',
        default='some_username'
    )

    USERNAME_FIELD = "tg_username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.tg_username)
