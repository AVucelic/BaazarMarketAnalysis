from django.urls import path
from .views import fetch_bazaar_data

urlpatterns = [
    path('api/bazaar-data/', fetch_bazaar_data, name='fetch_bazaar_data'),
]