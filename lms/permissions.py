from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    """Проверка на модератора, не может удалять и создавать новые курсы/уроки"""
    message = 'Вы не являетесь модератором'

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsOwner(BasePermission):
    """Проверка на владельца"""
    message = 'Вы не являетесь владельцем'

    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
        return False


class IsOwnerOrIsStaff(BasePermission):
    """Проверка на модератора или владельца"""
    message = 'Вы не являетесь владельцем или модератором'

    def has_permission(self, request, view):
        if request.user == view.get_object().owner or request.user.is_staff:
            return True
        return False