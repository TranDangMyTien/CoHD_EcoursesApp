from django.shortcuts import render
from django.http import HttpResponse
# parsers : Để úp ảnh lên Cloud
from rest_framework import viewsets, generics, permissions, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, User, Comment
# import cả serializers.py rồi nên không cần làm kiểu này nữa
# form .serializers import CourseSerializer, LessonSerializer
from courses import serializers, paginators
from django.views import View


# Create your views here.


# def index(request):
#     # e-courses app là view trả ra cho user
#     return render(request, 'index.html')


# Làm việc với GenericViewSet
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
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
    # queryset: trả về các đối tượng từ view => Ý nghĩa dòng code dưới đây là trả về các item có trường active=true
    queryset = Course.objects.filter(active=True)
    # Tạo phân trang, ghi đè cái phân trang chung bên settings.py
    pagination_class = paginators.CoursePaginator
    serializer_class = serializers.CourseSerializer
    # Từ đây nó tạo ra 5 endpoints tương ứng với 5 method
#   list (GET) : chỉ đọc = xem danh sách, trả về danh sách dicts
#   retrieve (GET) : chỉ dọc = xem chi tiết, trả về một dict (xem chi tiết)
#   create (POST) : tạo mới 1 resource
#   update/partial_update (PUT/PATCH) : chỉnh sửa một resource
#   destroy (DELETE) : xóa 1 resource

#      permission_classes -> Muốn thực thi API thì phải ở trạng thái đã đăng nhập
#     permission_classes = [permissions.IsAuthenticated]


#     PHÂN QUYỀN
#     Ví dụ: Ràng buộc, xem danh sách thì ai cũng xem được, các thao tác còn lại thì phải đăng nhập
#  => Phải ghi đè lại permission_classes = [permissions.IsAuthenticated]
#     def get_permissions(self):
#         # Ai cũng có thể xem danh sách
#         if self.action == 'list':
#             return [permissions.AllowAny()]
#
#         # Các quyền còn lại đăng nhập mới được thực hiện
#         return [permissions.IsAuthenticated()]



    # Phần lọc dữ liệu
    def get_queryset(self):
        queries = self.queryset
        # Dòng mã if self.action.__eq__('list'): trong Django REST Framework (DRF)
        # đang kiểm tra xem hành động (action) hiện tại của view có phải là list hay không.
        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            # Nếu q khác null có nghĩa là truy vấn
            if q:
                # /course/?q=
                queries = queries.filter(subject__icontains=q)
            cate_id = self.request.query_params.get('category_id')
            if cate_id:
            # Dùng category__id: thì nó join 2 bảng lại với nhau
            # Ví dụ tìm 10 lần tìm thì nó join lại 10 lần => Tốn chi phí và thời gian
            # Nên dùng category_id vì nó được chương trình sinh ra sẵn cho khóa ngoại của mỗi bảng
            # Ở class Course có trường khóa ngoại category => Django sinh ra 1 trường mới là category_id
            # /course/?category_id=
                queries = queries.filter(category_id=cate_id)
        return queries


#     Phần truy vấn lấy bài học của khóa học (Cha là Course - con là Lesson)
#     Thêm 1 api mới như này  /courses/{course_id}/lessons/?q=
#     /course/ là cái xuất danh mục mình đã làm rồi
#     Tạo api mới cần có 3 tham số như bên dưới, pk là details
#     pk là khóa chính của Course được truyền vào
#     Nếu đường dẫn không có {course_id} thì đừng đưa pk vào cho phức tạp
#     details=False thì không có pk
#     Đổi tên như yêu cầu dùng url_path='lessons'
    @action(methods=['get'], detail=True, name='Get-lessons',
            url_path='get-lessons', url_name='get-lessons')
    # Sau khi đặt url_name='get-lessons' => Đường dẫn bây giờ là /courses/{course_id}/get-lesson/?q=
    def get_lessons(self, request, pk ):
        # Django tự động tạo ra một thuộc tính có tên là {tên_model}_set
        # để cho phép truy xuất các đối tượng liên quan từ một mối quan hệ một-nhiều.
        # Mối qh 1 Course - nhiều bài học => ta có lesson_set
        l = self.get_object().lesson_set.filter(active=True).all()

        q = request.query_params.get('q')
        if q:
            l = l.filter(subject__icontains=q)

        # Bật many=True vì đây là mối quan hệ 1 - nhiều => Muốn xuất ra nhiều bài học
        # context={'request':request} => Ảnh hiện có đường dẫn đầy đủ, cho đây là api mình tự tạo nên phải gắn như vậy
        return Response(serializers.LessonSerializer(l, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)







class LessonViewSet(viewsets.ModelViewSet):
    # queryset = Lesson.objects.filter(active=True)
    # prefetch_related('tags'): Phương thức prefetch_related() được sử dụng để tải trước các đối tượng liên kết (foreign key)
    # hoặc đối tượng liên kết nhiều-nhiều (many-to-many) từ cơ sở dữ liệu.
    # Trong trường hợp này, 'tags' là tên của trường mà Lesson liên kết đến.
    # 'tags' khóa ngoại của Lesson
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    # Dùng upload ảnh lên Cloud
    # LỖI PHẦN SWAGGER
    # parser_classes = [parsers.MultiPartParser, ]

#     Tạo API mới cho người dùng ẩn bài học đi
#     Tất cả biến action đều phải có biến request (được gửi từ client lên)
    @action(methods=['post'], detail=True, name='Hide this lesson',
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
#       context={'request':request} => Ảnh hiện có đường dẫn đầy đủ, cho đây là api mình tự tạo nên phải gắn như vậy
#         return Response(data=serializers.LessonSerializer(l, context={'request' : request}).data,
        return Response(data=serializers.LessonSerializer(l).data,
                    status=status.HTTP_200_OK)
#     Thêm api mới  /lessons/{lesson_id}/comments/
    @action(methods=['get'], url_path='comments', detail=True, name='Get comment')
    def get_comments(self, request, pk):
        # Truy vấn ngược từ Lesson qua Comment (1 Lesson - Nhiều Comment)
        # comment_set do Django tạo ra -> để truy vấn ngược
        # Phương thức select_related() được sử dụng để tải trước (prefetch) các đối tượng liên kết theo một cách thông minh.
        # Sử dụng select_related('user') giúp tải trước tất cả các đối tượng User liên kết với các bản ghi Comment,
        # giúp tăng hiệu suất khi truy cập các trường của User sau này.
        # Phương thức order_by() được sử dụng để sắp xếp các kết quả của truy vấn theo một hoặc nhiều trường dữ liệu.
        # -id : comment mới nhất sẽ xuất hiện đầu tiên.
        comments = self.get_object().comment_set.select_related('user').order_by("-id")

        return Response(serializers.CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)


     

#   Làm việc với GenericViewSet vì UserViewSet không cần tạo ra các default
#   Liên đến User thì tất cả nên dùng Post để bảo mật, crate=post
# class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    # Dùng upload ảnh lên Cloud
    parser_classes = [parsers.MultiPartParser,]

class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    # permission_classes = [perms.CommentOwner]



#     queryset = Post.objects.all().order_by('-date')
# order_by() là một phương thức của queryset trong Django được sử dụng để sắp xếp kết quả truy vấn.
# Khi sử dụng '-date' trong Django, nó có nghĩa là sắp xếp từ mới đến cũ

# DEMO
# class TestView(View):
#     def get(self, request):
#         pass
#     def post(self, request):
#         pass