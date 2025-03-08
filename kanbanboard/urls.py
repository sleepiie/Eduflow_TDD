from django.urls import path
from . import views

app_name = "kanbanboard"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('create-category/', views.create_category, name='create_category'),
    path('category/<int:category_id>/' , views.topic_page , name='topic_page'),
    path('category/<int:category_id>/create-topic/', views.create_topic, name='create_topic'),

]
