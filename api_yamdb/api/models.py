from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


USER_ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    email = models.EmailField('Почта пользователя', unique=True, blank=False)
    bio = models.TextField('О себе', blank=True, max_length=200)
    role = models.CharField(
        'Роль пользователя', max_length=10,
        choices=USER_ROLE, default='user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ('username',)


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, verbose_name='slug')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='slug')

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    year = models.IntegerField(blank=True, verbose_name='Год выпуска')
    description = models.TextField(max_length=200, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        blank=True, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True,
        null=True, verbose_name='Категория'
    )


class Review(models.Model):
    text = models.TextField(blank=False, verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Произведение'
    )

    class Meta:
        ordering = ('-pub_date',)


class Comment(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, null=False,
        related_name="comments", verbose_name='Произведение'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, null=False,
        related_name="comments", verbose_name='Отзыв'
    )
    text = models.TextField(blank=False, verbose_name='Текст комментария')
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
