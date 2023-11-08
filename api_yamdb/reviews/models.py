import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser
from api_yamdb.settings import CHARACTER_LIMIT

User = CustomUser

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
        return self.name[:CHARACTER_LIMIT]


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField('Заголовок', max_length=256)
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
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
        blank=True

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('year',)

    def __str__(self):
        return self.title[:CHARACTER_LIMIT]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        verbose_name='жанр',
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        verbose_name='произведениe',
        on_delete=models.CASCADE
    )


class AbstractPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='автор',
    )
    text = models.TextField(verbose_name='текст')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)
        abstract = True

    def __str__(self):
        return self.text[:CHARACTER_LIMIT]


class Review(AbstractPost):
    """Модель Отзывов"""

    text = models.TextField(
        "текст отзыва",
        help_text="введите текст отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "минимальная оценка - 1"),
            MaxValueValidator(10, "максимальная оценка - 10"),
        ],
        verbose_name="оценка произведения",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="автор отзыва",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="произведение с отзывом",
    )

    class Meta:
        default_related_name = "reviews"
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]


class Comment(AbstractPost):
    """Модель Комментариев"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="отзыв с комментарием",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="автор комментария",
    )

    text = models.TextField("текст комментария", )

    class Meta:
        default_related_name = 'comments'
        verbose_name_plural = 'коментарии'
        verbose_name = 'коментарий'
