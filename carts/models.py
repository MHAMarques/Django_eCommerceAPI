import uuid
from django.db import models


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    products = models.ManyToManyField("products.Product", related_name="added_cart")
