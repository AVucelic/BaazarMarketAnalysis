# myapp/models.py
# myapp/models.py

from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    sell_price = models.FloatField()
    sell_volume = models.IntegerField()
    buy_price = models.FloatField()
    buy_volume = models.IntegerField()
    sell_orders = models.IntegerField()
    buy_orders = models.IntegerField()

    def __str__(self):
        return self.name
