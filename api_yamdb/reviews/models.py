import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

User = get_user_model()

SHOW_SYMBOLS = 30
CURRENT_YEAR = datetime.datetime.now().year


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField('Заголовок', max_length=100)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:SHOW_SYMBOLS]


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField('Заголовок', max_length=100)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:SHOW_SYMBOLS]


class Title(models.Model):
    """Модель публикации."""

    name = models.CharField('название', max_length=256)
    year = models.IntegerField(
        verbose_name='год создания',
        validators=[MaxValueValidator(CURRENT_YEAR)]
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        through='TitlesGenres',
        verbose_name='жанр',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        null=True,
        blank=True
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('year',)

    def __str__(self):
        return self.title[:SHOW_SYMBOLS]


class TitlesGenres(models.Model):
    """Вспомогательная модель связи жанров и произведений
    многие-ко-многим.
    под вопросом.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.SET_NULL

    )
