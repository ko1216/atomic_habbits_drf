from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    tg_id = models.BigIntegerField(unique=True, verbose_name='Telegram_id', null=False, default=0)
    tg_username = models.CharField(max_length=30, verbose_name='Ник в тг', blank=True, null=True)

    USERNAME_FIELD = "tg_id"
    REQUIRED_FIELDS = []
