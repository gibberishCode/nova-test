from django.urls import path

from .views import create_file_view

urlpatterns = [
    path("create-file/", create_file_view, name="create-file"),
]
