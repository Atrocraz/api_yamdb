from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

from creations.models import Category, Genre, Title


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    slug = models.SlugField(
        max_length=50,
        validators=[UniqueValidator(
            queryset=Category.objects.all(),
            message='Отсутствует обязательное поле или оно некорректно'
        ),]
    )

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    slug = models.SlugField(
        max_length=50,
        validators=[UniqueValidator(
            queryset=Genre.objects.all(),
            message='Отсутствует обязательное поле или оно некорректно'
        ),]
    )

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведения."""

    category = SlugRelatedField(
        required=True,
        slug_field='name',
        read_only=True,
        help_text='Выберите категорию'
    )

    genres = SlugRelatedField(
        required=True,
        many=True,
        slug_field='name',
        read_only=True,
        help_text='Выберите хотя бы один жанр'
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_genres(self, value):
        """
        Проверка жанров из существующего списка.
        """
        for genre in value:
            if genre not in Genre.objects.all():
                raise ValidationError(
                    ['Выберите существующий жанр из списка.']
                )
        return value

    def validate_category(self, value):
        """
        Проверка категории из существующего списка.
        """
        if value not in Category.objects.all():
            raise ValidationError(
                ['Выберите существующую категорию из списка.']
            )
        return value
