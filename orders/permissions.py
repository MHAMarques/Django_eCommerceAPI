from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Order


class OrderPermission(permissions.BasePermission):
    def has_permission(self, req: Request, view: View):
        if req.method == "POST":
            return req.user.is_authenticated

        return req.user.is_superuser


class DetailedPermission(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: Order):
        if req.method == "PATCH":
            if not "status" in req.data:
                return False
            return (
                req.user.is_authenticated
                and req.user.is_superuser
                or obj.sold_by == req.user.id
            )

        if req.method == "DELETE":
            return (
                req.user.is_authenticated
                and req.user.is_superuser
                or obj.sold_by == req.user.id
            )
        return (
            req.user.is_authenticated
            and req.user.is_superuser
            or req.user.id == obj.user.id
            or obj.sold_by == req.user.id
        )
