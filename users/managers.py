from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, tg_username, password=None, **extra_fields):
        if not tg_username:
            raise ValueError('The tg_username field must be set')
        user = self.model(tg_username=tg_username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tg_username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(tg_username, password, **extra_fields)
