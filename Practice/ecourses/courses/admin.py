from django.contrib import admin
from courses.models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.

# Form define cho Lesson
class LessonForm(forms.Form):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        # Ghi đè lại trường content
        # Cho nó sử dụng class Lesson
        model = Lesson
        # Cho nó được sử dụng tất cả các trường của class Lesson
        fields = '__all__'


# Form define cho Course
class CourseForm(forms.Form):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        # Ghi đè lại trường description
        # Cho nó sử dụng class Course
        model = Course
        # Cho nó được sử dụng tất cả các trường của class Course
        fields = '__all__'




class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name', 'created_date']


class CourseAdmin(admin.ModelAdmin):
    # Dùng đề ghi đè
    forms = CourseForm
    list_display = ['id', 'subject', 'created_date', 'category']
    search_fields = ['subject', 'created_date', 'category__name']
    readonly_fields = ['avatar']
    def avatar(self, course):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px/>".format(img_url=course.image.name, alt=course.subject))


class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            # Kiểu tuple thì khi dùng một phần tử thì có dấu "," như bên dưới
            'all': ('/static/css/main.css',)
        }
    # Dùng đề ghi đè
    forms = LessonForm
    list_display = ['id', 'subject', 'created_date', 'active', 'course']
    search_fields = ['subject', 'created_date', 'course__subject']
    # course__subject : tìm theo khóa ngoại
    # Thêm trường chỉ để đọc không chỉnh sửa
    readonly_fields = ['avatar']

    # self là this trong hướng đối tượng
    # obj là đại diện model
    # Đặt vào trong mark_safe : để xử lý các kí tự cho an toàn
    # Dùng 3 dấu ''' để xuống hàng
    # def image(self, obj):
    #     return mark_safe('''
    #         <img src='/static/{img_url}' alt='{alt}' />
    #     '''.format(img_url=obj.image.name), alt = obj.subject)

    # {img_url} sẽ được thay thế bằng đường dẫn đến hình ảnh được cung cấp trong đối tượng 'lesson'.
    def avatar(self, lesson):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px/>".format(img_url=lesson.image.name, alt=lesson.subject))



# Thêm CategoryAdmin ở sau để nó kế thừa cái mình đã tạo
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag)