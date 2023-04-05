from rest_framework import serializers
from .models import Product, CategoryChoices
from users.models import User


def choices_error_message(choices_class):
    valid_choices = [choice[0] for choice in choices_class.choices]
    message = ", ".join(valid_choices).rsplit(",", 1)

    return "Choose between " + " and".join(message) + "."


class ProdutSoldBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
        ]


class ProductSerializer(serializers.ModelSerializer):
    sold_by = ProdutSoldBySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "is_available",
            "thumbnail",
            "sold_by",
            "amount",
        ]

        read_only_fields = ["id", "sold_by"]

        extra_kwargs = {
            "amount": {"write_only": True},
            "category": {
                "error_messages": {
                    "invalid_choice": choices_error_message(CategoryChoices)
                }
            },
        }

    def create(self, validated_data):
        if validated_data['amount'] == 0:
            validated_data['is_available'] = False
        return Product.objects.create(**validated_data)
