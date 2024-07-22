# myapp/models.py
from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_volume = models.DecimalField(max_digits=20, decimal_places=2)
    buy_volume = models.DecimalField(max_digits=20, decimal_places=2)
    sell_orders = models.IntegerField()
    buy_orders = models.IntegerField()

    class Meta:
        db_table = 'myapp_product'  # Optional: custom table name

    def __str__(self):
        return self.name
