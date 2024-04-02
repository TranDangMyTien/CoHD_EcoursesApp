from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson
# import cả serializers.py rồi nên không cần làm kiểu này nữa
# form .serializers import CourseSerializer, LessonSerializer
from courses import serializers, paginators
from django.views import View


# Create your views here.


# def index(request):
#     # e-courses app là view trả ra cho user
#     return render(request, 'index.html')


# Làm việc với GenericViewSet
# class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategorySerializer
#
#
# class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
#     queryset = Course.objects.filter(active=True)
#     serializer_class = serializers.CourseSerializer
#     pagination_class = paginators.CoursePaginator
#
#     def get_queryset(self):
#         queryset = self.queryset
#         q = self.request.query_params.get('q')
#         if q:
#             queryset = queryset.filter(subject__icontains=q)
#         cate_id = self.request.query_params.get('category_id')
#         if cate_id:
#             # Dùng category__id: thì nó join 2 bảng lại với nhau
#             # Ví dụ tìm 10 lần tìm thì nó join lại 10 lần => Tốn chi phí và thời gian
#             # Nên dùng category_id vì nó được chương trình sinh ra sẵn cho khóa ngoại của mỗi bảng
#             queryset = queryset.filter(category_id=cate_id)
#
#         return queryset




def login(request):
    return render(request, 'index.html')

# Làm việc với ModelViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    # Tạo phân trang, ghi đè cái phân trang chung bên settings.py
    pagination_class = paginators.CoursePaginator
    serializer_class = serializers.CourseSerializer
    # Từ đây nó tạo ra 5 endpoints tương ứng với 5 method
#   list (GET) : chỉ đọc, trả về danh sách dicts
#   retrieve (GET) : chỉ dọc, trả về một dict
#   create (POST) : tạo mới 1 resource
#   update/partial_update (PUT/PATCH) : chỉnh sửa một resource
#   destroy (DELETE) : xóa 1 resource

#      permission_classes -> Muốn thực thi API thì phải ở trạng thái đã đăng nhập
#     permission_classes = [permissions.IsAuthenticated]

#     Ví dụ: Ràng buộc, xem danh sách thì ai cũng xem được, các thao tác còn lại thì phải đăng nhập
#  => Phải ghi đè lại permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        # Ai cũng có thể xem danh sách
        if self.action == 'list':
            return [permissions.AllowAny()]

        # Các quyền còn lại đăng nhập mới được thực hiện
        return [permissions.IsAuthenticated()]

    # Phần lọc dữ liệu
    def get_queryset(self):
        queries = self.queryset
        q = self.request.query_params.get('q')
        # Nếu q khác null có nghĩa là truy vấn
        if q:
            queries = queries.filter(subject__icontains=q)

        return queries



class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = serializers.LessonSerializer

#     Tạo API mới cho người dùng ẩn bài học đi
#     Tất cả biến action đều phải có biến request (được gửi từ client lên)
    @action(methods=['post'], detail=True,
            url_path='hide-lesson', url_name='hide-lesson')
    # Ngoài 5 api đã có giờ mình sẽ có thêm 1 api mới như sau
    # /lessons/{pk}/hide_lesson
    # mặc định là hide_lesson trên đường dẫn
    # Nếu muốn chỉnh sử thì thêm url_path
    def hide_lesson(self, request, pk):
        # Để tránh người dùng gửi pk trống thì mình dùng try except
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#       Khi thành công
        return Response(data= serializers.LessonSerializer(l, context={'request':request}).data,
                        status=status.HTTP_200_OK)



# DEMO
# class TestView(View):
#     def get(self, request):
#         pass
#     def post(self, request):
#         pass