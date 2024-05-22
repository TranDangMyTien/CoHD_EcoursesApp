from django.db import models
from django.contrib.auth.models import AbstractUser # Chứng thực
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True, blank=True)

# calss abstract
class BaseModel(models.Model):
    # DateTime : lưu ngày và giờ

    # auto_now_add Lấy thời điểm hiện tại (lúc thêm dữ liệu) gán vào biến created_date
    # Chỉ lấy lần đầu tiên lúc tạo
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    # auto_now Lấy thời gian hiện tại (ngay khi có chỉnh sửa mới)
    updated_date = models.DateTimeField(auto_now=True, null=True )
    # Tạo trường đánh dấu còn tồn tại hay không
    active = models.BooleanField(default=True)
    # Bật lên để cho  BaseModel trở thành class trừu tượng (abstract)
    class Meta:
        abstract = True



# Mặc định các class sẽ tự tạo trường ID khóa chính
# Nếu tự tạo thì sẽ mất cái mặc định trên
# Tên bảng dưới csdl là : tên app_tên bảng (chữ viết thường dính liền)
# => courses_category
# Danh mục
class Category (BaseModel):
    # unique=True : Không cho trùng tên
    # null=False : Không được để trống
    name = models.CharField(max_length=100, null=False, unique=True)
    def __str__(self):
        return self.name

# Khóa học
class Course (BaseModel):
    subject = models.CharField(max_length=100, null=False)
    # description = models.TextField(null=True, blank=True)
    description = RichTextField()

    image = CloudinaryField('image', null=True, blank=True)

    # Khóa ngoại
    # on_delete khi mà cái Class Category xóa thì cái trường category ở class này sẽ ra sao ?
    # models.CASCADE Khi xóa category thì toàn bộ khóa học (course) ở category xóa theo - quan hệ combosition
    # Khi Class Category xóa thì trường category ở đây sẽ null
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag')


    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ('subject', 'category')



class Lesson(BaseModel):
    subject = models.CharField(max_length=100, null=False)
    content = RichTextField(null=True)
    # image = models.ImageField(upload_to='lessons/%Y/%m')
    # Vì chỉ định đường dẫn nên chỉ còn như này
    image = CloudinaryField('image', null=True, blank=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    # blank=True: Được phép rỗng, khi người dùng (client) quên truyền tham số thì nó vẫn cho chạy
    # null=True : Được phép trống, Database ở MySQL được phép null
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    class Meta:
        unique_together = ('subject', 'course')

    def __str__(self):
        return f'{self.id}-{self.subject}'



# Một bài học có nhiều tag, 1 tag có nhiều bài học => Quan hệ Many to Many
class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


# Lớp tương tác
class Interaction(BaseModel):
    # Khóa ngoại, một người sẽ có nhiều tương tác
    # User hủy thì Interaction sẽ mất
    # CASCADE : Bảng chứa khóa chính mất thì bảng chứa khóa ngoại sẽ mất theo
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Một bài học có nhiều người tương tác tương tác
    # CASCADE: Bảng chưa khóa chính mất thì bảng chưa khóa ngoãi sẽ mất theo
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    # user_id và lesson_id phát sinh ra từ trường user và lesson
    # def __str__(self) -> Nối chuỗi
    # VD: user_id là 1 lesson_id là 100 => 1-100
    def __str__(self):
        return f'{self.user_id} - {self.lesson_id}'

    # Mặc dù kế thừa lớp cha BaseModel nhưng, nhưng nó ko kế thừa trừu tượng
    # Bậc trừu tượng cho nó
    class Meta:
        abstract = True

# Cho lớp comment kế thừa lớp Interaction
class Comment(Interaction):
    content = models.CharField(max_length=255)


# Tạo class like như fb (like 2 lần = unlike)
class Like(Interaction):
    class Meta:
        unique_together = ('user', 'lesson')




