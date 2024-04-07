from rest_framework import permissions

# Tạo quyền:cập nhật comment và người dùng chỉ cập nhật comment của mình đã thêm
# Đầu tiên là phải được chứng thực trước
class CommentOwner(permissions.IsAuthenticated):
    # def has_object_permission(self, request, view, obj):
    # Ghi như bên dưới cho tường minh, vì cái này đem cho bên kia chạy thì nó chính là Model Comment\
    def has_object_permission(self, request, view, comment):
        # request.user là người đã được chứng thực
        # comment.user là người tạo ra comment
        return super().has_permission(request, view) and request.user == comment.user


