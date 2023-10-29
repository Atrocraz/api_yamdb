import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# from creations.models import Title

CHARACTER_LIMIT = 30
User = get_user_model()
CURRENT_YEAR = datetime.datetime.now().year


class Review(models.Model):
    """Модель Отзывов"""
    text = models.TextField(
        "Текст отзыва",
        help_text="Введите текст отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Минимальная оценка - 1"),
            MaxValueValidator(10, "Максимальная оценка - 10"),
        ],
        verbose_name="Оценка произведения",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата отзыва",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    title = models.ForeignKey(
        on_delete=models.CASCADE,  # Добавить Title
        related_name="reviews",
        verbose_name="Произведение с отзывом",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]

    def __str__(self):
        return self.text[:CHARACTER_LIMIT]


class Comment(models.Model):
    """Модель Комментариев"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв с комментарием",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата комментария",
    )
    text = models.TextField("Текст комментария", )

    class Meta:
        default_related_name = 'comments'
        ordering = ("-pub_date",)
        verbose_name_plural = 'Коментарии'
        verbose_name = 'Коментарий'

    def __str__(self):
        return (
            f'{self.text[:CHARACTER_LIMIT]} к {self.review}, {self.author}'
        )


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField('Заголовок', max_length=100)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:CHARACTER_LIMIT]


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField('Заголовок', max_length=100)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:CHARACTER_LIMIT]


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
        return self.title[:CHARACTER_LIMIT]


class TitlesGenres(models.Model):
    """Вспомогательная модель связи жанров и произведений
    многие-ко-многим.
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
