from celery_app import app
import requests
from myapp.models import Product

API_KEY = '2c2b8b5d-4850-4b91-b0d3-6e74679cf12c'

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

        quick_status = product.get('quick_status', {})
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
