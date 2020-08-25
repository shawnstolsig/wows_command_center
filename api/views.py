from django.shortcuts import render



# for testing below
from django.http import JsonResponse

def test_json(request):
    return JsonResponse({'message': 'You have reached the backend!'})