from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
# from users.models import User
# from creations.models import Title


User = get_user_model()
CHARACTER_LIMIT = 30


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
        related_name="comments",
        verbose_name="Отзыв с комментарием",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата комментария",
    )
    text = models.TextField("Текст комментария", )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name_plural = 'Коментарии'
        verbose_name = 'Коментарий'

    def __str__(self):
        return (
            f'{self.text[:CHARACTER_LIMIT]} к {self.review}, {self.author}'
        )
