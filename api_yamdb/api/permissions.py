"""Разрешения для взаимодействия пользователей с эндпойнтами."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AllowAnyOrAdmin(BasePermission):
    """Просмотр списков объектов и объектов доступен всем пользователям,
    добавление, редактирование и удаление объектов доступно только админам.
    """

    def has_object_permission(self, request, view, obj):
        pass
