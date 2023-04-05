import uuid
from django.db import models


class StatusOrderChoices(models.TextChoices):
    ON_GOING = "EM ANDAMENTO"
    DELIVERED = "ENTREGUE"
    DEFAULT = "PEDIDO REALIZADO"


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.CharField(
        max_length=30,
        choices=StatusOrderChoices.choices,
        default=StatusOrderChoices.DEFAULT,
    )
    bought_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_by = models.UUIDField()

    user = models.ForeignKey(
        "users.User",
        related_name="orders",
        on_delete=models.CASCADE,
    )

    products = models.ManyToManyField(
        "products.Product",
        related_name="sold_products",
    )
