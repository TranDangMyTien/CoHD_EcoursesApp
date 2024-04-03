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
        fields = ['id', 'subject', 'content', 'image', 'created_date', 'tags']