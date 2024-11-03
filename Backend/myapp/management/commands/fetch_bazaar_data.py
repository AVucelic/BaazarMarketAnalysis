from celery import shared_task
import requests
import logging
import os
from dotenv import load_dotenv
from myapp.models import Product

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

@shared_task
def fetch_bazaar_data():
    logger.info("Starting fetch_bazaar_data task")
    
    # Get API key from environment variable
    API_KEY = os.getenv('API_KEY')
    
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