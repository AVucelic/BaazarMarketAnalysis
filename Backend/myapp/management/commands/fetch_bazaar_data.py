import requests
from django.core.management.base import BaseCommand
from myapp.models import Product

class Command(BaseCommand):
    help = 'Fetches bazaar data and updates the database'

    def handle(self, *args, **options):
        self.stdout.write('Fetching bazaar data...')
        
        API_KEY = '08511e18-0f4e-4985-93b5-4ff3ab863010'
        
        try:
            # Fetch products data
            products_response = requests.get(f'https://api.hypixel.net/v2/skyblock/bazaar?key={API_KEY}')
            products_response.raise_for_status()
            products_data = products_response.json().get('products', {})
        except requests.RequestException as e:
            self.stdout.write(f'Error fetching products data: {e}')
            return
        
        try:
            # Fetch product names
            names_response = requests.get(f'https://api.hypixel.net/v2/resources/skyblock/items?key={API_KEY}')
            names_response.raise_for_status()
            names_data = names_response.json().get('items', [])
            product_names = {item['id']: item['name'] for item in names_data}
        except requests.RequestException as e:
            self.stdout.write(f'Error fetching product names: {e}')
            return
        
        # Update or create products in the database
        for product_id, product_data in products_data.items():
            if product_id.startswith('ENCHANTMENT') or product_id.startswith('ESSENCE'):
                continue

            quick_status = product_data.get('quick_status', {})
            product_name = product_names.get(product_id, product_id)

            # Update or create product in the database
            Product.objects.update_or_create(
                product_id=product_id,
                defaults={
                    'name': product_name,
                    'sell_price': quick_status.get('sellPrice', 0),
                    'sell_volume': quick_status.get('sellVolume', 0),
                    'sell_orders': quick_status.get('sellOrders', 0),
                    'buy_price': quick_status.get('buyPrice', 0),
                    'buy_volume': quick_status.get('buyVolume', 0),
                    'buy_orders': quick_status.get('buyOrders', 0)
                }
            )
        
        self.stdout.write('Data fetch complete.')
