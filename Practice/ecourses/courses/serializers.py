from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from courses.models import Category, Course, Lesson, Tag, User


class TagSerializers(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# Tạo lớp serializers chung cho Course và Lesson cho có 2 thuộc tính giống nhau là 'tag' và 'image'
class BaseSerializers(ModelSerializer):
    tags = TagSerializers(many=True)

    # COURSE VÀ LESSON DÙNG CHUNG
    # Trường image lấy từ model Course
    # image = serializers.SerializerMethodField(source='image')
    # # Xác định giá trị cho trường 'image'
    # def get_image(self, course):
    #     # Nếu trường image của course khác null
    #     if course.image:
    #         request = self.context.get('request')
    #         if request:
    #             # Dòng mã này đang xây dựng một URI tuyệt đối (absolute URI) dựa trên yêu cầu (request)
    #             return request.build_absolute_uri('/static/%s' % course.image.name)
    #         return '/static/%s' % course.image.name



class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(BaseSerializers):
    # Trường image lấy từ model Course
    image = serializers.SerializerMethodField(source='image')
    # tags = TagSerializers(many=True)

    def get_image(self, course):
        # Nếu trường image của course khác null
        if course.image:
            request = self.context.get('request')
            if request:
                # Dòng mã này đang xây dựng một URI tuyệt đối (absolute URI) dựa trên yêu cầu (request)
                return request.build_absolute_uri('/static/%s' % course.image.name)
            return '/static/%s' % course.image.name


    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_date', 'category', 'tags']




class LessonSerializer(BaseSerializers):
    # tags = TagSerializers(many=True)
    class Meta:
        model = Lesson
        # 'tags' bây giờ chứa thông tin 'id' và 'name' do truyền bằng TagSerializer
        fields = ['id', 'subject', 'content', 'image', 'created_date', 'tags', 'image']



class LessonDetailsSerializer(LessonSerializer):
# NOTE: Khi kế thừa thì thuộc tính kế thừa chứ Meta ko kế thừa, cần viết lại
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # Qua models.py -> ctrl + trỏ vào AbstractUser để thấy được các trường củ User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        # Thiết lập mật khẩu chỉ để ghi
        extra_kwargs = {
            'password': {
                'write_only': True
            }

        }

    def create(self, validated_data):
        # dòng mã data = validated_data.copy() được sử dụng để tạo một bản sao của dữ liệu đã được xác thực (validated_data)
        # validated_data là dữ liệu đã được xác thực (validated) từ dữ liệu đầu vào.
        # Trong serializer của Django Rest Framework, trước khi dữ liệu được sử dụng để tạo hoặc cập nhật đối tượng,
        # nó phải được kiểm tra tính hợp lệ. Điều này bao gồm kiểm tra các trường yêu cầu, kiểm tra định dạng, kiểm tra quyền truy cập, vv.

        # .copy() là một phương thức của đối tượng dictionary trong Python, được sử dụng để tạo một bản sao của dictionary.
        # Bản sao này được sử dụng để tránh thay đổi dữ liệu gốc khi thực hiện các thao tác khác nhau.
        # data này là 1 dict (từ điển)

        data = validated_data.copy()
        # Thông thường phải truyền từng trường như này
        # user = User(first_name=data.first_name)
        # Django hỗ trợ viết nhanh hơn
        # key -> Tên tham số; value -> giá trị truyền vào tham số
        user = User(**data)
        # Băm mật khẩu
        # set_password() : mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu để đảm bảo tính bảo mật.
        # user['password'] là cách truy cập vào mật khẩu mới của người dùng từ dữ liệu đầu vào.
        user.set_password(data['password'])
        user.save()
        return user
