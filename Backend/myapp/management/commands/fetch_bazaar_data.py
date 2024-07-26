import requests
from django.core.management.base import BaseCommand
from myapp.models import Product

class Command(BaseCommand):
    help = 'Fetches bazaar data and updates the database'

    def handle(self, *args, **options):
        self.stdout.write('Fetching bazaar data...')

        API_KEY = '2c2b8b5d-4850-4b91-b0d3-6e74679cf12c'
        url = f'https://api.hypixel.net/v2/skyblock/bazaar?key={API_KEY}'
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses

            data = response.json()
            products = data.get('products', {})

            # Check if products data is not empty
            if not products:
                self.stdout.write('No products found in the response.')
                return

            # Update or create products in the database
            updated_count = 0
            for product_id, product_data in products.items():
                quick_status = product_data.get('quick_status', {})

                product, created = Product.objects.update_or_create(
                    product_id=product_id,
                    defaults={
                        'name': product_data.get('name', 'Unnamed Product'),
                        'sell_price': quick_status.get('sellPrice', 0),
                        'buy_price': quick_status.get('buyPrice', 0),
                        'sell_volume': quick_status.get('sellVolume', 0),
                        'buy_volume': quick_status.get('buyVolume', 0),
                        'sell_orders': quick_status.get('sellOrders', 0),
                        'buy_orders': quick_status.get('buyOrders', 0),
                    }
                )
                if created:
                    self.stdout.write(f'Created new product: {product_id}')
                else:
                    updated_count += 1

            self.stdout.write(f'Data fetch complete. {updated_count} products updated.')

        except requests.RequestException as e:
            self.stdout.write(f'Error fetching data: {e}')
        except Exception as e:
            self.stdout.write(f'An unexpected error occurred: {e}')
