from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_id', 'name', 'sell_price', 'buy_price', 
        'sell_volume', 'buy_volume', 'sell_orders', 'buy_orders'
    )
    list_filter = ('name',) 
    search_fields = ('product_id', 'name') 
    ordering = ('name',)
    readonly_fields = ('product_id',)

    def get_queryset(self, request):
        """Override to use select_related for performance optimization if necessary"""
        queryset = super().get_queryset(request)
        return queryset

    def save_model(self, request, obj, form, change):
        """Custom save method if needed"""
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """Custom delete method if needed"""
        super().delete_model(request, obj)

    def get_readonly_fields(self, request, obj=None):
        """Custom read-only fields"""
        if obj:
            return self.readonly_fields + ('product_id',)
        return self.readonly_fields
