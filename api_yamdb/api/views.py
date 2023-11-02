"""Представления моделей приложения yatube_api в api."""
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from api.filters import TitleFilter
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleAdminSerializer, TitleReaderSerializer)
from reviews.models import Category, Genre, Review, Title
from users.permissions import IsAdminOrReadOnly, IsStaffOrAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = [IsStaffOrAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = [IsStaffOrAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id'],
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class CategoryGengeMixin(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    """Миксин для представлений жанра и категории."""
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name',]
    lookup_field = 'slug'


class CategoryViewSet(CategoryGengeMixin):
    """Представление модели категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(CategoryGengeMixin):
    """Представление модели жанра."""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Представление модели произведения. """

    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'name'
    )
    # queryset = Title.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReaderSerializer
        return TitleAdminSerializer
