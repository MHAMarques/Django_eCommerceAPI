from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Product


class ProductPermission(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "GET":
            return True
        if req.user.is_authenticated:
            return req.user.is_vendor or req.user.is_superuser

        return False


class DetailedPermission(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: Product):
        if req.method == "PATCH" or req.method == "DELETE":
            return (
                req.user.is_authenticated
                and req.user.is_superuser
                or req.user.id == obj.sold_by.id
            )
        if req.method == "GET":
            return True
        return req.user.is_authenticated and req.user.is_superuser or req.user.is_vendor
