from django.contrib import admin

from reviews.models import (Category, Comment, Genre,
                            Review, Title)


class TitleInline(admin.TabularInline):
    model = Title.genres.through


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывов."""

    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    empty_value_display = "-empty-"
    list_filter = ('author', 'score', 'pub_date')
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review'
    )
    empty_value_display = "-empty-"
    list_filter = ('author', 'pub_date')
    search_fields = ('author',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    model = Genre,
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-',
    inlines = [
        TitleInline,
    ]


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Названия произведений отображены в админ-панели.
    Можно найти по названию и году. Фильтр по году.
    """

    list_display = ('id', 'name', 'year', 'category',)
    search_fields = ('name', 'year',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории отображены в админ-панели.
    Можно найти по названию. Фильтр по названию.
    """

    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'