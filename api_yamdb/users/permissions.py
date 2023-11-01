from rest_framework.permissions import SAFE_METHODS, BasePermission


class AtLeastModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.role == 'moderator' or
                request.user.role == 'admin' or
                request.user.is_superuser == 1)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.role == 'admin' or
                request.user.is_superuser == 1)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'admin' or
                request.user.is_superuser == 1)
