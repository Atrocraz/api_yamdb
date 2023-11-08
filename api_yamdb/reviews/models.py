from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser
from api_yamdb.settings import CHARACTER_LIMIT, CURRENT_YEAR, MAX_NAME_LENGTH

User = CustomUser


class ВaseCategoyGenre(models.Model):
    """Общая для жанра и катеогрии."""

    name = models.CharField('Заголовок', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:CHARACTER_LIMIT]


class Genre(ВaseCategoyGenre):
    """Модель жанра произведения."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Category(ВaseCategoyGenre):
    """Модель категории произведения."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Title(models.Model):
    """Модель публикации."""

    name = models.CharField('название', max_length=MAX_NAME_LENGTH)
    year = models.PositiveSmallIntegerField(
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

    def display_genres(self):
        """
        Добавляет возможность просмотра жанров
        произведения в админ панели.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genres.short_description = 'genre'

    def __str__(self):
        return self.name[:CHARACTER_LIMIT]


class GenreTitle(models.Model):
    """Вспомогательная модель, связывает произведения и жанры."""

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
