from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Названия произведений отображены в админ-панели.
    Можно найти по названию и году. Фильтр по году.
    """

    list_display = ('titles_id', 'name', 'year', 'genre', 'category',)
    search_fields = ('name', 'year',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры отображены в админ-панели.
    Можно найти по названию. Фильтр по названию.
    """

    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
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
