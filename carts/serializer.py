from rest_framework import serializers
from .models import Cart
from products.models import Product
from products.serializer import ProductSerializer


class CartSerializer(serializers.ModelSerializer):

    products = ProductSerializer(many= True)
    

    def update(self, instance, validated_data):

        instance.products.set([])
        for prod in validated_data["products"]:
            instance.products.add(prod)
        # setattr(instance, "products", validated_data["products"])

        instance.save()
        return instance

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products']
