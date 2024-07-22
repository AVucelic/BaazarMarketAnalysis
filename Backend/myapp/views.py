from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def fetch_bazaar_data(request):
    api_key = '27a7a87a-3ed9-4831-a2de-dc7fbb014b9f'
    bazaar_url = f'https://api.hypixel.net/v2/skyblock/bazaar?key={api_key}'
    items_url = f'https://api.hypixel.net/v2/resources/skyblock/items?key={api_key}'

    try:
        bazaar_response = requests.get(bazaar_url)
        items_response = requests.get(items_url)
        bazaar_data = bazaar_response.json()
        items_data = items_response.json()

        product_names = {item['id']: item['name'] for item in items_data.get('items', [])}

        return JsonResponse({
            'products': bazaar_data.get('products', {}),
            'productNames': product_names
        })
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
