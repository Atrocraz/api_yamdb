from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOrReadOnly(BasePermission):
    '''Пермишен, проверяющий, есть ли у пользователя права модератора или выше.
    '''
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_moderator
                or request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdminOrReadOnly(BasePermission):
    '''Пермишен, проверяющий, есть ли у пользователя права админа или выше.

    Разрешает 'GET', 'HEAD', 'OPTIONS' методы.
    '''

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_admin)


class IsAdmin(BasePermission):
    "Пермишен, проверяющий, есть ли у пользователя права админа или выше."

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
