from django.shortcuts import render
import json
from .models import Category
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def homepage(request):
    categories = Category.objects.all()
    return render(request,"homepage.html", {'categories': categories})

@csrf_exempt
def create_category(request):
    if request.method == "POST":
        
        data = json.loads(request.body)
        category_name = data.get('name')
        category = Category.objects.create(name=category_name)
        
        return JsonResponse({
            'status': 'success',
            'category_id': category.id,
            'name': category.name
        })