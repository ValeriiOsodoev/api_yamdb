from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAdminOrReadOnly(BasePermission):
    """Разрешение для пользователей с правами администратора или на чтение."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_admin


class AdminRules(BasePermission):
    """
    Разрешение для администраторов.

    Пользователь должен быть аутентифицирован и иметь права администратора
    или суперпользователя.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class ReadOnly(BasePermission):
    """
    Разрешение только для чтения.

    Разрешает только запросы методов GET, HEAD и OPTIONS.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AccessOrReadOnly(BasePermission):
    """
    Разрешение на доступ или только для чтения.

    Пользователь должен быть аутентифицирован для запросов методом POST.
    Разрешает доступ для запросов методов GET, HEAD и OPTIONS.
    Для остальных методов требуется аутентификация пользователя и одно из
    следующих условий:
    - Пользователь является автором объекта (если такое условие применимо).
    - Пользователь является модератором.
    - Пользователь является администратором.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.is_authenticated

        return request.user.is_authenticated and (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class UserAccess(BasePermission):
    """
    Разрешение для обычных пользователей.

    Пользователь должен быть аутентифицирован и не иметь прав администратора
    или суперпользователя.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and not (
            request.user.is_admin or request.user.is_superuser
        )
