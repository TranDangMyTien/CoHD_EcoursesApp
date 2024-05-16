from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.contrib.auth.models import Permission
from courses.models import Category, Course, Lesson, Tag, User, Comment
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
import cloudinary
from django.urls import path


# Register your models here.

# Form define cho Lesson
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        # Ghi đè lại trường content
        # Cho nó sử dụng class Lesson
        model = Lesson
        # Cho nó được sử dụng tất cả các trường của class Lesson
        fields = '__all__'


# Form define cho Course
class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        # Ghi đè lại trường description
        # Cho nó sử dụng class Course
        model = Course
        # Cho nó được sử dụng tất cả các trường của class Course
        fields = '__all__'





class CategoryAdmin(admin.ModelAdmin):
    # Cột mà danh sách hiện ra
    list_display = ['id', 'name']
    # Tìm theo trường
    search_fields = ['name', 'created_date']

# Đang thêm Course thì thêm luôn Lesson nhờ vào khóa ngoại
class LessonInline(admin.StackedInline):
    model = Lesson
    pk_name = 'course'
# Khi thêm Lesson sẽ có luôn phần thêm Tag. Mối quan hệ nhiều nhiều (nhiều bài học và nhiều tag)
class LessonTagInline(admin.TabularInline):
    model = Lesson.tags.through


class CourseAdmin(admin.ModelAdmin):
    # Dùng đề ghi đè
    form = CourseForm
    list_display = ['id', 'subject', 'created_date', 'category']
    search_fields = ['subject', 'created_date', 'category__name']
    readonly_fields = ['avatar']
    inlines = (LessonInline, )
    # Phần này này lưu ảnh ở máy local
    def avatar(self, course):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px/>".format(img_url=course.image.name, alt=course.subject))


class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            # Kiểu tuple thì khi dùng một phần tử thì có dấu "," như bên dưới
            'all': ('/static/css/main.css',)
        }
    # Dùng đề ghi đè
    form = LessonForm
    list_display = ['id', 'subject', 'created_date', 'active', 'course']
    search_fields = ['subject', 'created_date', 'course__subject']
    # course__subject : tìm theo khóa ngoại
    # Thêm trường chỉ để đọc không chỉnh sửa
    readonly_fields = ['image']

    # self là this trong hướng đối tượng
    # obj là đại diện model
    # Đặt vào trong mark_safe : để xử lý các kí tự cho an toàn
    # Dùng 3 dấu ''' để xuống hàng
    # def image(self, obj):
    #     return mark_safe('''
    #         <img src='/static/{img_url}' alt='{alt}' />
    #     '''.format(img_url=obj.image.name), alt = obj.subject)

    # {img_url} sẽ được thay thế bằng đường dẫn đến hình ảnh được cung cấp trong đối tượng 'lesson'.
    # có thể ghi là obj cũng được ở phần def avatar(self, obj)
    def avatar(self, lesson):
        # Trường hợp up ảnh lên couldinary
        if lesson.image:

            if type(lesson.image) is cloudinary.CloudinaryResource:
                # return mark_safe(f"<img width='250' src='{lesson.image.url}' />")
                return mark_safe("<img src='{img_url}' alt='{alt}' width=120px/>".format(img_url=lesson.image.url, alt=lesson.subject))
            return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px/>".format(img_url=lesson.image.name, alt=lesson.subject))

    inlines = [LessonTagInline,]


# Ghi đè lại trang Admin -> AdminSite : tùy chỉnh theo ý của mình
class CourseAppAdminSite(admin.AdminSite):
    # stie_header : Chữ trên tiêu đề trang chủ
    site_header = 'HỆ THỐNG QUẢN LÝ KHÓA HỌC'




    # Ghi đè lại url của nó
    def get_urls(self):
        return [
            # course-stats : tên đường dẫn mình tự đặt
            # course_stats là cái hàm phía dưới
            path('course-stats/', self.course_stats)
        ] + super().get_urls()

    # Đây là view của mình
    def course_stats(self, request):
        # Đếm có bao nhiêu khóa học
        course_count = Course.objects.count()

        # Đếm 1 khóa học có bao nhiêu bài học
        # Truy vấn ngược từ 1 Course -> nhiều Lesson
        # các trường trong value là của Course
        # lessons : tên truy vấn ngược đến Lesson (chưa được related_name)
        stats = Course.objects.annotate(lesson_count=Count('lessons')).values("id", "subject", "lesson_count" )


        # Tạo một TemplateResponse để trả về một trang web.
        # Đối tượng truyền vào hàm request: cái người ta gửi lên,
        # cái thứ 2 là template mình muốn render hiển thị trang web
        # cái thứ 3 là dữ liệu mà mình muốn đưa ra trang web
        # {'course_count': course_count}: là một dictionary chứa dữ liệu mà bạn muốn truyền vào template.
        # 'course_count' : Tên mình đặt
        # course_count: là thứ mình đổ ra
        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': course_count,
            'stats': stats
        })



# Tạo đối tượng
admin_site = CourseAppAdminSite('mycourse')


# Thêm CategoryAdmin ở sau để nó kế thừa cái mình đã tạo
# admin_site.register(Category, CategoryAdmin)
# admin_site.register(Course, CourseAdmin)
# admin_site.register(Lesson, LessonAdmin)
# admin_site.register(Tag)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Comment)