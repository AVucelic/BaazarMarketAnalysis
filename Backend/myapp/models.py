from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=255, unique=True, verbose_name="Product ID")
    name = models.CharField(max_length=255, verbose_name="Product Name")
    sell_price = models.FloatField(verbose_name="Sell Price")
    sell_volume = models.IntegerField(verbose_name="Sell Volume")
    buy_price = models.FloatField(verbose_name="Buy Price")
    buy_volume = models.IntegerField(verbose_name="Buy Volume")
    sell_orders = models.IntegerField(verbose_name="Sell Orders")
    buy_orders = models.IntegerField(verbose_name="Buy Orders")

    def __str__(self):
        return f'{self.name} ({self.product_id})'

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']
