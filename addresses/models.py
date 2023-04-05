from django.db import models
import uuid


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    street = models.CharField(max_length=140)
    number = models.PositiveIntegerField()
    detail = models.CharField(max_length=80, default=None)
    zip_code = models.CharField(max_length=8)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=30)
