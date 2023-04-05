from rest_framework import serializers
from .models import Order, StatusOrderChoices
from django.shortcuts import get_object_or_404
from products.models import Product
from products.serializer import choices_error_message
import smtplib
import email.message


def email_autosend(to_email, nome, status):
    corpo_email = f"""
    <p>Olá, {nome}</p>
    <p>O status do seu pedido foi alterado para {status}</p>
    <p>At.te G19 Commerce</p>
    <small>Este e-mail é enviado automaticamente</small>
    """

    msg = email.message.Message()
    msg["Subject"] = "O status do seu pedido foi alterado"
    msg["From"] = "g19commerceapi@gmail.com"
    msg["To"] = to_email
    password = "ibgpfwtkhxlsimgi"
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(corpo_email)

    s = smtplib.SMTP("smtp.gmail.com: 587")
    s.starttls()

    s.login(msg["From"], password)
    s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))


class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "is_available",
            "thumbnail",
            "amount",
        ]
        extra_kwargs = {"amount": {"write_only": True}}


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    def create(self, validated_data):
        for product in validated_data["products"]:
            validated_data["price"] += product["price"]

        products = validated_data.pop("products")
        print(products)
        order_inst = Order.objects.create(**validated_data)

        for product in products:
            product_inst = get_object_or_404(Product, pk=product["id"])
            order_inst.products.add(product_inst)

        return order_inst

    def update(self, instance, validated_data):
        if validated_data["status"]:
            setattr(instance, "status", validated_data["status"])

            instance.save()

            email_autosend(
                instance.user.email, instance.user.first_name, validated_data["status"]
            )

        return instance

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "bought_at",
            "price",
            "user",
            "sold_by",
            "products",
        ]
        extra_kwargs = {
            "status": {
                "error_messages": {
                    "invalid_choice": choices_error_message(StatusOrderChoices)
                }
            },
            "price": {"read_only": True},
        }
