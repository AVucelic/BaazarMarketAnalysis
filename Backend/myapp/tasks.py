from celery_app import app
import requests
from myapp.models import Product

API_KEY = '27a7a87a-3ed9-4831-a2de-dc7fbb014b9f'

@app.task
def fetch_bazaar_data():
    # Fetch products data
    products_response = requests.get(f'https://api.hypixel.net/v2/skyblock/bazaar?key={API_KEY}')
    if products_response.status_code != 200:
        raise Exception('Failed to fetch products data')

    products_data = products_response.json().get('products', {})

    # Fetch product names
    names_response = requests.get(f'https://api.hypixel.net/v2/resources/skyblock/items?key={API_KEY}')
    if names_response.status_code != 200:
        raise Exception('Failed to fetch product names')

    names_data = names_response.json().get('items', [])
    product_names = {item['id']: item['name'] for item in names_data}

    for product_id, product in products_data.items():
        if product_id.startswith('ENCHANTMENT') or product_id.startswith('ESSENCE'):
            continue

        quick_status = product['quick_status']
        product_name = product_names.get(product_id, product_id)

        # Update or create product in the database
        Product.objects.update_or_create(
            product_id=product_id,
            defaults={
                'name': product_name,
                'sell_price': quick_status['sellPrice'],
                'sell_volume': quick_status['sellVolume'],
                'sell_orders': quick_status['sellOrders'],
                'buy_price': quick_status['buyPrice'],
                'buy_volume': quick_status['buyVolume'],
                'buy_orders': quick_status['buyOrders']
            }
        )
