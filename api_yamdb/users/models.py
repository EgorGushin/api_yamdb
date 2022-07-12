from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    roles = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Обязательное поле, не более 150 букв/цифр/@/./+/-/_',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text='Обязательное поле, не более 254 символов',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Тип пользователя',
        max_length=50,
        choices=roles,
        default='user'
    )
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ('email', )