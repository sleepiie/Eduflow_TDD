from django.shortcuts import render
import json
from .models import Category , Topic
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

@csrf_exempt
def topic_page(request,category_id):
    category = Category.objects.get(id=category_id)
    topics = Topic.objects.filter(category=category)
    return render(request,"topic.html",{'topics':topics , 'category': category})

@csrf_exempt
def create_topic(request,category_id):
    if request.method == "POST":
        
        data = json.loads(request.body)
        topic_name = data.get('name')
        category = Category.objects.get(id=category_id)
        topic = Topic.objects.create(
            category=category,
            name=topic_name
        )
        
        return JsonResponse({
            'status': 'success',
            'topic_id': topic.id,
            'name': topic.name
        })





