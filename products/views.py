from .models import Product
from .serializer import ProductSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import ProductPermission, DetailedPermission


class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [ProductPermission]

    def get_queryset(self):
        name = self.request.query_params.get("name")

        if name is not None:
            return self.queryset.filter(name__icontains=name)

        category = self.request.query_params.get("category")

        if category is not None:
            return self.queryset.filter(category__icontains=category)

        return self.queryset

    def perform_create(self, serializer):
        serializer.save(sold_by=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [DetailedPermission]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Create your views here.
