from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Права доступа для владельца"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsModer(permissions.BasePermission):
    """Права доступа для модератора"""

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="moders").exists()
