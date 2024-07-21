from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse


def api_data(request):
    data = {'key': 'value'}
    return JsonResponse(data)

def home(request):
    return HttpResponse("Welcome to the home page!")