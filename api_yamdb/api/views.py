"""Представления моделей приложения yatube_api в api."""
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from creations.models import Category, Genre, Title


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели жанра."""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Представление модели произведения. """

    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
