# myapp/views.py

from django.http import JsonResponse
import requests

API_KEY = '27a7a87a-3ed9-4831-a2de-dc7fbb014b9f'

def bazaar_data(request):
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

    return JsonResponse({'error': 'Failed to fetch data from Hypixel API'}, status=500)
