from django.urls import path
from . import views

app_name = "kanbanboard"

urlpatterns = [
    path("", views.homepage, name="homepage"),  # Menu page
]
