# myapp/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'sell_price', 'buy_price', 'sell_volume', 'buy_volume', 'sell_orders', 'buy_orders')
