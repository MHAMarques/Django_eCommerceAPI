from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class UserPermission(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "POST":
            return True

        return req.user.is_superuser


class DetailedPermission(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: User):
        return req.user.is_authenticated and req.user.is_superuser or req.user == obj
