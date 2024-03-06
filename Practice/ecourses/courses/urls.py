from django.contrib import admin
from django.urls import path
# from ecourses.courses import views

from .import views

urlpatterns = [
    # name="index" dùng để phân giải đường dẫn
    path('', views.index, name="index"),
]
