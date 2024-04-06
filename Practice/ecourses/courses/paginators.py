from rest_framework import pagination
# Phân trang chung ở file setting.py
# Còn ở dưới đây là phân trang ghi đè lại

# Tạo phân trang cho Course
class CoursePaginator(pagination.PageNumberPagination):
    page_size = 2

# Tạo phân trang cho Comment
class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2
