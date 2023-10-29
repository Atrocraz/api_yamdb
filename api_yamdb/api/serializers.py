from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""

        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    slug = serializers.SlugField(
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

    slug = serializers.SlugField(
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
        read_only=True,
        slug_field='slug',
        help_text='Выберите категорию'
    )

    genres = SlugRelatedField(
        many=True,
        slug_field='slug',
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
