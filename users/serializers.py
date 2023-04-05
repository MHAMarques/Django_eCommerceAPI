from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User
from addresses.models import Address
from carts.models import Cart
from addresses.serializer import AddressSerializer
from products.serializer import ProductSerializer


class UserCartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "products"]


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    cart = UserCartSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_vendor",
            "is_superuser",
            "address",
            "cart",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user_address = validated_data.pop("address")
        new_address = Address.objects.create(**user_address)
        if "is_superuser" in validated_data:
            validated_data["is_superuser"] = False
        new_cart = Cart.objects.create()
        return User.objects.create_user(
            address=new_address, cart=new_cart, **validated_data
        )

    def update(self, instance: User, validated_data: dict) -> User:
        if "address" in validated_data:
            new_address = validated_data.pop("address")
            user_address = Address.objects.get(id=instance.address.id)
            for key, value in new_address.items():
                setattr(user_address, key, value)

            user_address.save()

        instance.refresh_from_db()
        if "is_superuser" in validated_data:
            validated_data["is_superuser"] = False
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def delete(self, instance):
        instance.address.delete()
        instance.cart.delete()
        instance.delete()
