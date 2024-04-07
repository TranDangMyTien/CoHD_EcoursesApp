from django.shortcuts import render
from django.http import HttpResponse
# parsers : Để úp ảnh lên Cloud
from rest_framework import viewsets, generics, permissions, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, User, Comment
# import cả serializers.py rồi nên không cần làm kiểu này nữa
# form .serializers import CourseSerializer, LessonSerializer
from courses import serializers, paginators, perms
from django.views import View


# Create your views here.


# def index(request):
#     # e-courses app là view trả ra cho user
#     return render(request, 'index.html')


# Làm việc với GenericViewSet
# Một ViewSet có thể add nhiều api
# ListAPIView = GET : Xem danh sách
# RetrieveAPIView = GET : Xem chi tiết
# DestroyAPIView = DELETE : Xóa
# CreateAPIView = POST : Tạo mới
# UpdateAPIView = PUT/PATCH = Cập nhật toàn bộ/ một phần
# ListCreateAPIView = GET + POST : Xem danh sách + tạo mới
# RetrieveUpdateAPIView = GET + PUT + PATCH : Xem chi tiết + cập nhật toàn phần + cập nhật một phần
# RetrieveDestroyAPIView = GET + DELETE : Xem chi tiết + xóa
# RetrieveUpdateDestroyAPIView = GET + PUT + PATCH + DELETE : Xem chi tiết + cập nhật toàn phần + cập nhật một phần + xóa
class CategoryViewSet(viewsets.ViewSet, generics.RetrieveUpdateDestroyAPIView):
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
    permission_classes = [permissions.IsAuthenticated]


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
    # hoặc đối tượng liên kết nhiều-nhiều (many-to-many) từ cơ sở dữ liệu. => DÙNG TRONG MANY TO MANY
    # Trong trường hợp này, 'tags' là tên của trường mà Lesson liên kết đến.
    # 'tags' khóa ngoại của Lesson
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    # Tạo phần chứng thực
    def get_permissions(self):
        # Rơi vào các hoạt động 'add_comment', 'hide_lesson' thì cần chứng thực mới được làm
        if self.action in ['add_comment', 'hide_lesson']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

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
        # giúp tăng hiệu suất khi truy cập các trường của User sau này. => select_related('user') => DÙNG TRONG MANY TO ONE
        # Phương thức order_by() được sử dụng để sắp xếp các kết quả của truy vấn theo một hoặc nhiều trường dữ liệu.
        # -id : comment mới nhất sẽ xuất hiện đầu tiên.
        comments = self.get_object().comment_set.select_related('user').order_by("-id")
        # paginators.CommentPaginator() đang tạo một instance của custom paginator
        paginator = paginators.CommentPaginator()
        # paginate_queryset() là một phương thức của paginator được sử dụng để phân trang một tập hợp dữ liệu
        # Nhận đầu vào là comments
        # Phương thức này thực hiện việc phân trang dữ liệu dựa trên các thông tin trong request,
        # chẳng hạn như số trang hiện tại, kích thước trang, vv., và trả về một trang (page) của dữ liệu đã được phân trang.
        # => Từ những comments cho client tạo thì mình phân trang trên đó
        page = paginator.paginate_queryset(comments, request)
        # if page is not None: đang kiểm tra xem việc phân trang dữ liệu đã thành công hay không => Thành công thì qua bước tiếp theo
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(serializers.CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)


#   Thêm API mới /lessons/{lesson_id}/comments/ => Thêm một bình luận mới vào bài học
    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk ):
        # Thay vì viết Comment.objects.create(content='..', lesson  user,...)
        # Viết ngắn gọn hơn
        # self (từ Lesson)
        # Chỉ lấy user = request.user => Cái đã được chứng thực
        c = self.get_object().comment_set.create(content=request.data.get('content'),
                                             user=request.user)
        # Không có many = True => Mỗi lần chỉ tạo 1 commentSai với nguyên tắc bảo mật
        # Tạo comment mới nên trả về trạng thái 201 OK => Cho người dùng biết đã tao thành công
        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)


     

#   Làm việc với GenericViewSet vì UserViewSet không cần tạo ra các default
#   Liên đến User thì tất cả nên dùng Post để bảo mật, crate=post
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):

    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    # Dùng upload ảnh lên Cloud
    parser_classes = [parsers.MultiPartParser,]

    def get_permissions(self):
    # Kiểm tra xem hành động hiện tại của ViewSet có nằm trong danh sách các hành động được chỉ định hay không
    # self.action : xác định hành động hiện tại
        if self.action in ['get_current_user']:
            #  Đăng nhập mới được thực hiện được các thao tác
            return [permissions.IsAuthenticated()]
        # Ai cũng có thể thao tác được
        return [permissions.AllowAny()]



#   Tạo api mới /users/current-user/
#   Lấy thông tin của current user => Người dùng chỉ được xem thông tin của mình mà thoi
#   detail = False => Không cho gửi id, chỉ khi nào chứng thực mới được vào
#   Cập nhật 1 phần profile => patch
    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
#   Đã được chứng thực rồi thì không cần truy vấn nữa => Xác định đây là người dùng luôn
        user = request.user
        # Khi so sánh thì viết hoa hết
        if request.method.__eq__('PATCH'):
            # user = user hiện đang đăng nhập
            for k, v in request.data.items():
                # Thay vì viết user.first_name = v
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)


# Vừa tạo api delete + update
class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    # Truyền dạng call_back
    permission_classes = [perms.CommentOwner]






#     queryset = Post.objects.all().order_by('-date')
# order_by() là một phương thức của queryset trong Django được sử dụng để sắp xếp kết quả truy vấn.
# Khi sử dụng '-date' trong Django, nó có nghĩa là sắp xếp từ mới đến cũ

# DEMO
# class TestView(View):
#     def get(self, request):
#         pass
#     def post(self, request):
#         pass