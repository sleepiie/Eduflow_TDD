from django.shortcuts import render
import json
from .models import Category , Topic , Task
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


@csrf_exempt
def board_page(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    category = topic.category
    return render(request, "board.html", {'topic': topic, 'category': category})



@csrf_exempt
def task_list(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    
    if request.method == 'GET':
        tasks = Task.objects.filter(topic=topic)
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'title': task.title,
                'due_date': task.due_date,
                'status': task.status
            })
        return JsonResponse(task_list, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        due_date = data.get('due_date', '')
        status = data.get('status', 'todo')
        
        task = Task.objects.create(
            topic=topic,
            title=title,
            due_date=due_date,
            status=status
        )
        
        return JsonResponse({
            'status': 'success',
            'task_id': task.id,
            'title': task.title,
            'due_date': task.due_date,
            'status': task.status
        })

@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'due_date': task.due_date,
            'status': task.status,
            'topic_id': task.topic.id
        })
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        title = data.get('title')
        due_date = data.get('due_date')
        status = data.get('status')
        
        if title:
            task.title = title
        
        if due_date is not None:
            task.due_date = due_date
        
        if status:
            task.status = status
        
        task.save()
        
        return JsonResponse({
            'status': 'success',
            'id': task.id,
            'title': task.title,
            'due_date': task.due_date,
            'status': task.status
        })
    
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'status': 'success'})