from django.db import models
from django.contrib.auth.models import AbstractUser # Chứng thực

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

# calss abstract
class BaseModel(models.Model):
    # DateTime : lưu ngày và giờ

    # auto_now_add Lấy thời điểm hiện tại (lúc thêm dữ liệu) gán vào biến created_date
    # Chỉ lấy lần đầu tiên lúc tạo

    created_date = models.DateTimeField(auto_now_add=True)
    # auto_now Lấy thời gian hiện tại (ngay khi có chỉnh sửa mới)
    updated_date = models.DateTimeField(auto_now=True)
    # Tạo trường đánh dấu còn tồn tại hay không
    active = models.BooleanField(default=True)

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
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='courses/%Y/%m')

    # Khóa ngoại
    # on_delete khi mà cái Class Category xóa thì cái trường category ở class này sẽ ra sao ?
    # models.CASCADE Khi xóa category thì toàn bộ khóa học (course) ở category xóa theo - quan hệ combosition
    # Khi Class Category xóa thì trường category ở đây sẽ null
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.name