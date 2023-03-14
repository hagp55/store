from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(
        _('Имя'), max_length=150
    )
    email = models.EmailField(
        _('Электронная почта'), unique=True
    )
    phone = models.CharField(
        _('Телефон'), max_length=12, unique=True
    )
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone',]

    class Meta:
        verbose_name = _('Пользователя')
        verbose_name_plural = _('Пользователи')
