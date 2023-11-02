from rest_framework.permissions import SAFE_METHODS, BasePermission


class AtLeastModeratorOrReadOnly(BasePermission):
    '''Пермишен, проверяющий, есть ли у пользователя права модератора или выше.
    '''

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_moderator or
                request.user.is_admin or
                request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    '''Пермишен, проверяющий, есть ли у пользователя права админа или выше.

    Разрешает 'GET', 'HEAD', 'OPTIONS' методы.
    '''

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_admin or
                request.user.is_superuser)


class IsAdmin(BasePermission):
    "Пермишен, проверяющий, есть ли у пользователя права админа или выше."

    def has_permission(self, request, view):
        return (request.user.is_admin or request.user.is_superuser)


class IsStaffOrAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_moderator
            or request.user.is_admin
            or request.user == obj.author
        )
