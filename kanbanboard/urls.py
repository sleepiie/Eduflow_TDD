from django.urls import path
from . import views

app_name = "kanbanboard"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('create-category/', views.create_category, name='create_category'),
    path('category/<int:category_id>/' , views.topic_page , name='topic_page'),
    path('category/<int:category_id>/create-topic/', views.create_topic, name='create_topic'),
    path('topic/<int:topic_id>/', views.board_page, name='board_page'),
    path('api/topics/<int:topic_id>/tasks/', views.task_list, name='task_list'),
    path('api/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
]
