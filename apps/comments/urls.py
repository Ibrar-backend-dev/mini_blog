from django.urls import path 
from .views import CommentDeleteView, CommentLikeView, PostCommentListCreateView

urlpatterns =[
    path("posts/<int:id>/comments/", PostCommentListCreateView.as_view() , name = "post-comment"),
    path("comments/<int:id>/", CommentDeleteView.as_view(), name = "delete-comment"),
    path("comments/<int:comment_id>/like/", CommentLikeView.as_view(), name="like-comment"),
]