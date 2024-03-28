from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from .admin import admin_site
from .import views

r = routers.DefaultRouter()
r.register('categories', views.CategoryViewSet, 'categories')
r.register('courses', views.CourseViewSet, 'courses')



urlpatterns = [
    # name="index" dùng để phân giải đường dẫn
    # path('', views.index, name="index"),

    # Phần API
    path('', include(r.urls)),


    path('login/', views.login, name="login")

]

