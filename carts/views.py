from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Cart
from .serializer import CartSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import CartPermission
from products.models import Product


class CartView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CartPermission]

    serializer_class = CartSerializer

    def perform_update(self, serializer):
        products = self.request.data
        list_product = []

        for product_id in products["products"]:
            new_products = get_object_or_404(Product, pk=product_id["id"])

            list_product.append(new_products)

        serializer.save(user=self.request.user, products=list_product)

    def get_queryset(self):
        # cart = Cart.objects.filter(id=self.request.user.cart_id)
        # return cart
        return Cart.objects.all()
