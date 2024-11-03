from celery import shared_task
from celery.result import AsyncResult
import requests
import time
import os
from dotenv import load_dotenv
from myapp.models import Product

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('API_KEY')

@shared_task
def fetch_bazaar_data():
    # Fetch products data
    products_response = requests.get(f'https://api.hypixel.net/v2/skyblock/bazaar?key={API_KEY}')
    if products_response.status_code != 200:
        return 'Failed to fetch products data.'
    
    products_data = products_response.json().get('products', {})
    
    # Fetch product names
    names_response = requests.get(f'https://api.hypixel.net/v2/resources/skyblock/items?key={API_KEY}')
    if names_response.status_code != 200:
        return 'Failed to fetch product names.'
    
    names_data = names_response.json().get('items', [])
    product_names = {item['id']: item['name'] for item in names_data}

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
    
    return 'Data fetch complete.'

@shared_task
def test_task():
    print("Test task executed!")
    return "Task completed"

def run_and_monitor_task(task, *args, **kwargs):
    result = task.delay(*args, **kwargs)
    while True:
        result = AsyncResult(result.id)
        print(result.status)
        if result.successful() or result.failed():
            break
        time.sleep(1)
    return result

if __name__ == "__main__":
    run_and_monitor_task(fetch_bazaar_data)
    run_and_monitor_task(test_task)