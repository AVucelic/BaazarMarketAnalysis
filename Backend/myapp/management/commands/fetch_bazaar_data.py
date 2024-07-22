# myapp/management/commands/fetch_bazaar_data.py
import requests
from django.core.management.base import BaseCommand
from myapp.models import Product

class Command(BaseCommand):
    help = 'Fetches bazaar data and updates the database'

    def handle(self, *args, **options):
        self.stdout.write('Fetching bazaar data...')
        
        API_KEY = '27a7a87a-3ed9-4831-a2de-dc7fbb014b9f'
        response = requests.get(f'https://api.hypixel.net/v2/skyblock/bazaar?key={API_KEY}')
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', {})
            
            for product_id, product_data in products.items():
                quick_status = product_data.get('quick_status', {})
                
                Product.objects.update_or_create(
                    product_id=product_id,
                    defaults={
                        'name': product_data.get('name', ''),
                        'sell_price': quick_status.get('sellPrice', 0),
                        'buy_price': quick_status.get('buyPrice', 0),
                        'sell_volume': quick_status.get('sellVolume', 0),
                        'buy_volume': quick_status.get('buyVolume', 0),
                        'sell_orders': quick_status.get('sellOrders', 0),
                        'buy_orders': quick_status.get('buyOrders', 0),
                    }
                )
                
            self.stdout.write('Data fetch complete.')
        else:
            self.stdout.write('Failed to fetch data.')
