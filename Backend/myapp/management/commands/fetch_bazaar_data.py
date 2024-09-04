from celery import shared_task
import requests
import logging
from myapp.models import Product

logger = logging.getLogger(__name__)

@shared_task
def fetch_bazaar_data():
    logger.info("Starting fetch_bazaar_data task")
    API_KEY = 'c847389e-00bb-4ff9-9e5f-daf36cff7f61'
    
    # Fetch products data
    products_response = requests.get(f'https://api.hypixel.net/v2/skyblock/bazaar?key={API_KEY}')
    if products_response.status_code != 200:
        logger.error('Failed to fetch products data.')
        return 'Failed to fetch products data.'
    
    products_data = products_response.json().get('products', {})
    
    # Fetch product names
    names_response = requests.get(f'https://api.hypixel.net/v2/resources/skyblock/items?key={API_KEY}')
    if names_response.status_code != 200:
        logger.error('Failed to fetch product names.')
        return 'Failed to fetch product names.'
    
    names_data = names_response.json().get('items', [])
    product_names = {item['id']: item['name'] for item in names_data}

    # Update or create products in the database
    for product_id, product_data in products_data.items():
        if product_id.startswith('ENCHANTMENT') or product_id.startswith('ESSENCE'):
            continue
        logger.info(f"Processing product {product_id}")
        # Add your database update or create logic here
    
    logger.info("Completed fetch_bazaar_data task")
    return "Task completed"