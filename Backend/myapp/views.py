import logging
import requests
from django.http import JsonResponse

logger = logging.getLogger(__name__)

API_KEY = 'c847389e-00bb-4ff9-9e5f-daf36cff7f61'

def bazaar_data(request):
    try:
        bazaar_response = requests.get(f'https://api.hypixel.net/v2/skyblock/bazaar?key={API_KEY}')
        items_response = requests.get(f'https://api.hypixel.net/v2/resources/skyblock/items?key={API_KEY}')
        
        if bazaar_response.status_code == 200 and items_response.status_code == 200:
            bazaar_data = bazaar_response.json()
            items_data = items_response.json()
            
            # Filter out products that start with "ENCHANTMENT" or "ESSENCE"
            filtered_products = {
                k: v for k, v in bazaar_data['products'].items()
                if not (k.startswith('ENCHANTMENT') or k.startswith('ESSENCE'))
            }
            
            product_names = {
                item['id']: item['name'] for item in items_data['items']
            }
            
            return JsonResponse({
                'products': filtered_products,
                'productNames': product_names
            })
        
        logger.error('Failed to fetch data from Hypixel API: Status Codes %d, %d', bazaar_response.status_code, items_response.status_code)
        return JsonResponse({'error': 'Failed to fetch data from Hypixel API'}, status=500)
    
    except Exception as e:
        logger.exception('An error occurred while fetching bazaar data: %s', str(e))
        return JsonResponse({'error': 'An internal error occurred'}, status=500)
