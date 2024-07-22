from django.urls import path
from . import views

urlpatterns = [
    path('bazaar-data/', views.bazaar_data, name='bazaar-data'),
]
