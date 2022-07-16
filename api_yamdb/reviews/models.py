from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, valid_year


class User(AbstractUser):
    roles = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Обязательное поле, не более 150 букв/цифр/@/./+/-/_',
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text='Обязательное поле, не более 254 символов',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Укажите имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Укажите фамилию',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        help_text='Расскажите о себе',
    )
    role = models.CharField(
        verbose_name='Тип пользователя',
        help_text='Укажите тип пользователя',
        max_length=35,
        choices=roles,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

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
        help_text='Укажите название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор категории',
        help_text='Укажите идентификатор категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        help_text='Укажите название жанра',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор жанра',
        help_text='Укажите идентификатор жанра',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        help_text='Укажите название произведения',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год выпуска произведения',
        help_text='Укажите год выпуска произведения',
        validators=(valid_year, )
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        help_text='Введите описание произведения',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
        help_text='Укажите жанр произведения',
        trough='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        help_text='Укажите категорию произведения',
        on_delete=models.SET_NULL,
        null=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
        help_text='Рейтинг произведения',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        help_text='Название произведения',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст обзора',
        help_text='Введите текст обзора',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор обзора',
        help_text='Автор обзора',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        help_text='Укажите оценку',
        validators=[
            MinValueValidator(1, message='Оценка не может быть ниже 1'),
            MaxValueValidator(10, message='Оценка не может быть выше 10'),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации обзора',
        help_text='Дата публикации обзора',
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
        help_text='Комментарий к обзору',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        help_text='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        help_text='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:65]
