"""
URL configuration for ecourses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# Phần dành cho AdminSite
from courses.admin import admin_site


# Phần tích hợp Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Course API",
        default_version='v1',
        description="APIs for CourseApp",
        contact=openapi.Contact(email="mytien.2682003@gmail.com"),
        license=openapi.License(name="Trần Đặng Mỹ Tiên"),
    ),
    public=True,
    # Cấu hình quyền được xem, AllowAny là tất cả mọi người đều được xem
    permission_classes=(permissions.AllowAny,),
)

# Nơi đầu tiên tìm url => Không được thay đổi tên urlpatterns
urlpatterns = [
    # Cộng chuỗi '' và courses.urls -> Đi tìm URL của app courses để chạy
    path('', include('courses.urls')),
    path('admin/', admin.site.urls),
    # Phần AdminSite
    # path('admin/', admin_site.urls),



    # Phần của CKEditor
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    path("__debug__/", include("debug_toolbar.urls")),

    # Phần tích hợp Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc')
]
