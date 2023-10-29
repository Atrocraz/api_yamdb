"""Представления моделей приложения yatube_api в api."""
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import AllowAnyOrAdmin
from api.serializers import (CategorySerializer, CommentSerializer, GenreSerializer,
                             ReviewSerializer, TitleSerializer)
from reviews.models import Category, Genre, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(pk=title_id)  # Добавить Title

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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AllowAnyOrAdmin]
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели жанра."""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [AllowAnyOrAdmin]
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Представление модели произведения. """

    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes = [AllowAnyOrAdmin]
    pagination_class = LimitOffsetPagination
