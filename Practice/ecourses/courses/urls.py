from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

# from rest_framework import routers
from .admin import admin_site
from .import views

# Phần GenericViewSet
# r = routers.DefaultRouter()
# r.register('categories', views.CategoryViewSet, 'categories')
# r.register('courses', views.CourseViewSet, 'courses')


# Phần của ModelViewSet
# Tạo đối tượng
router = DefaultRouter()
# Phần đầu tiên là prefix, tiếp đầu ngữ -> Phần đầu mà URL nó tạo ra cho mình
# Phần thứ 2 là viewsest
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('courses', views.CourseViewSet, basename='courses')
router.register('lessons', views.LessonViewSet, basename='lessons')
router.register('users', views.UserViewSet, basename='users')
router.register('comments', views.CommentViewSet, basename='comments')




urlpatterns = [
    # name="index" dùng để phân giải đường dẫn
    # path('', views.index, name="index"),

    # Phần API
    # path('', include(r.urls)),
    # Tạo ra các endpoints tương ứng như sau:
    # /courses/ - GET : Lấy danh sách
    # /courses/ - POST : Thêm một khóa học mới
    # /courses/{courses_id}/ - GET : Xem chi tiết danh sách khóa học
    # /courses/{courses_id}/ - PUT : Để cập nhật
    # /courses/{courses_id}/ - DELETE : Xóa
    path('', include(router.urls)),
    # Tương tự cũng sẽ có 5 api cho lessons


    # Phần OAuth2
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),


    path('login/', views.login, name="login")

]

