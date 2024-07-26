from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_id', 'name', 'sell_price', 'buy_price', 
        'sell_volume', 'buy_volume', 'sell_orders', 'buy_orders'
    )
    list_filter = ('name',)  # Allows filtering by product name
    search_fields = ('product_id', 'name')  # Enables search by product ID and name
    ordering = ('name',)  # Default ordering by product name
    readonly_fields = ('product_id',)  # Make product_id read-only since it's unique

    def get_queryset(self, request):
        """Override to use select_related for performance optimization if necessary"""
        queryset = super().get_queryset(request)
        # Add any additional query optimizations or annotations here if needed
        return queryset

    def save_model(self, request, obj, form, change):
        """Custom save method if needed"""
        super().save_model(request, obj, form, change)
        # Additional actions on save can be added here

    def delete_model(self, request, obj):
        """Custom delete method if needed"""
        super().delete_model(request, obj)
        # Additional actions on delete can be added here

    def get_readonly_fields(self, request, obj=None):
        """Custom read-only fields"""
        if obj:  # If the object exists, only make product_id read-only
            return self.readonly_fields + ('product_id',)
        return self.readonly_fields
