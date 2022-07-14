from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import *


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
        validators=(validate_username, )
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
        max_length=35,
        choices=roles,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор жанра',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год выпуска произведения',
        validators=(valid_year, )
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name', )

    def __str__(self):
        return self.name


class GenresTitles(models.Model):
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE)
    titles = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genres} {self.titles}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст обзора'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор обзора',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MinValueValidator(1, message='Оценка не может быть ниже 1'),
            MaxValueValidator(10, message='Оценка не может быть выше 10'),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации обзора',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзор'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:65]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Комментарий',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:65]
