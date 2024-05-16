from courses.models import Category, Course, Lesson
from django.db.models import Count
# .models đại diện cho thư mục hiện tại hoặc gói mà đoạn mã đang thực thi

# Hàm truy vấn dữ liệu khóa học (Course)
# def get_courses(params={}):
def get_courses(**params):
    q = Course.objects.filter(active=True)

    kw = params.get('kw')
    if kw:
        q = q.filter(subjects__icontains=kw)
    cate_id = params.get('cate_id')
    if cate_id:
        # Trong bảng Course ta có khóa ngoại course, thì khi build tên của nó là category_id
        q = q.filter(category_id=cate_id)
    # Muốn kết quả cuối giảm theo id
    return q.order_by('-id')

# *args: Lấy giá trị
# **kwargs: Lấy mảng, từ điển (truyền vào bao nhiêu cũng được hết)
# Truy vấn

# Truy vấn ngược
# def count_courses_by_cate():
#     return Category.objects.annotate(counter=Count('course_id')).values('id', 'subject').all()

# Đếm số lượng khóa học mỗi danh mục theo các giá trị chỉ định, sắp xếp tăng dần theo số lượng
def count_courses_by_cate():
    return Category.objects.annotate(count=Count('course__id')).values('id', 'name', 'count').order_by('count')

