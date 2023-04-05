from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Cart


class CartPermission(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: Cart):
        if req.method == "PATCH":
            if not "products" in req.data:
                return False

        return (
            req.user.is_authenticated and req.user.is_superuser or req.user.cart == obj
        )
