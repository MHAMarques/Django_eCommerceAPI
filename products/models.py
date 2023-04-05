from django.db import models
import uuid


class CategoryChoices(models.TextChoices):
    ELETRONICS = "Eletrodomésticos"
    CLOTHINGS = "Roupas"
    SMARTPHONES = "Celulares"
    HOME = "Casa"
    IT = "Informática"
    DEFAULT = "Não informado"


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        default=CategoryChoices.DEFAULT,
    )
    sold_by = models.ForeignKey(
        "users.User",
        related_name="my_selling_products",
        on_delete=models.PROTECT,
    )
    thumbnail = models.URLField(
        default="https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cindra/imagens/sem.jpg.gif"
    )
