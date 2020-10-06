from rest_framework import permissions, status
from rest_framework.response import Response


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == request.user.ADMIN


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == request.user.ADMIN


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return not request.user.is_anonymous()

        if request.method in ("PATCH", "DELETE"):
            return (
                request.user == obj.author
                or request.user.role == request.user.ADMIN
                or request.user.role == request.user.MODERATOR
            )

        if request.method in permissions.SAFE_METHODS:
            return True
        return False
