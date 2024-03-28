from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from courses.models import Category, Course, Lesson
from courses import serializers, paginators
from django.views import View

# Create your views here.


# def index(request):
#     # e-courses app là view trả ra cho user
#     return render(request, 'index.html')


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePaginator

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(subject__icontains=q)
        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            # Dùng category__id: thì nó join 2 bảng lại với nhau
            # Ví dụ tìm 10 lần tìm thì nó join lại 10 lần => Tốn chi phí và thời gian
            # Nên dùng category_id vì nó được chương trình sinh ra sẵn cho khóa ngoại của mỗi bảng
            queryset = queryset.filter(category_id=cate_id)

        return queryset

    # @action(methods=[])



def login(request):
    return render(request, 'index.html')


# DEMO
# class TestView(View):
#     def get(self, request):
#         pass
#     def post(self, request):
#         pass