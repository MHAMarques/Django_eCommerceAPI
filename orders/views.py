from rest_framework import generics
from .models import Order
from .serializer import OrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import OrderPermission, DetailedPermission
from carts.models import Cart
from carts.serializer import CartSerializer
from products.models import Product
from rest_framework.response import Response
from rest_framework import status


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OrderPermission]

    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        vendors = {}
        cart = Cart.objects.get(pk=request.user.cart_id)

        cart_list_product = CartSerializer(cart).data["products"]

        if len(cart_list_product) == 0:
            return Response(
                {"message": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        for product_dict in cart_list_product:
            product = get_object_or_404(Product, pk=product_dict["id"])
            if not product.is_available:
                return Response(
                    {"message": "This product is not available!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                product.amount = product.amount - 1

                if product.amount == 0:
                    product.is_available = False

                product.save()

            vendor_id = product.sold_by.id
            if vendor_id not in vendors:
                vendors[vendor_id] = []

            vendors[vendor_id].append(vars(product))

        objects = []
        for key, value in vendors.items():
            objects.append({"products": value, "user": request.user.id, "sold_by": key})

        serializer = OrderSerializer(data=objects, many=True)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        cart.products.set([])
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(price=0)

    def get_queryset(self):
        return Order.objects.all()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, DetailedPermission]

    serializer_class = OrderSerializer

    def get_queryset(self):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        return Order.objects.filter(pk=order.id)
