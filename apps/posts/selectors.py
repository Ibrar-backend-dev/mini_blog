# from django.db.models import Q
# from .models import Post

# def get_visible_posts(user):
#     #Public posts + current user's private posts

#     if user.is_authenticated:
#         return Post.objects.filter(  Q(is_private=False) | Q(is_private=True, author=user)  ).select_related('author')
    
#     return Post.objects.filter(is_private=False).select_related('author')