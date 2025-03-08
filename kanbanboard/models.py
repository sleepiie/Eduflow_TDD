from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=200)

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Todo'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    due_date = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    
    def __str__(self):
        return self.title
