# from rest_framework.permissions import BasePermission

# class IsOwnerOrReadOnly(BasePermission):

#     def has_object_permission(self, request, view, obj):
        
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return True
#         return obj.auther == request.user
    

# class IsCommentOwner(BasePermission):

#     def has_object_permission(self, request, view, obj):
        
#         return obj.commenter == request.user
    
