"""Представления моделей приложения yatube_api в api."""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404

from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleReaderSerializer, TitleAdminSerializer
)
from api.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title
from users.permissions import (
    AtLeastModeratorOrReadOnly, IsAdminOrReadOnly
)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = [AtLeastModeratorOrReadOnly]

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
    permission_classes = [AtLeastModeratorOrReadOnly]
    pagination_class = PageNumberPagination

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


class CategoryViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    """Представление модели категории."""

    http_method_names = ['get', 'post', 'delete']
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name',]
    lookup_field = 'slug'


class GenreViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin,
    GenericViewSet
):
    """Представление модели жанра."""

    http_method_names = ['get', 'post', 'delete']
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Представление модели произведения. """

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    serializer_class = TitleAdminSerializer

    # def update(self):
    #     if self.request.method == 'PUT':
    #         raise exceptions.MethodNotAllowed(method=HTTP_STRING['put'])
    #     return super().update

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReaderSerializer
        else:
            return TitleAdminSerializer
