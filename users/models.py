import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=127,
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )
    username = models.CharField(
        max_length=127,
        unique=True,
        error_messages={"unique": "A user with that username already exists."},
    )
    is_vendor = models.BooleanField(default=False)

    address = models.OneToOneField(
        "addresses.Address",
        related_name="user",
        on_delete=models.CASCADE,
    )

    cart = models.OneToOneField(
        "carts.Cart",
        related_name="user",
        on_delete=models.CASCADE,
    )
