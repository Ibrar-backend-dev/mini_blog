from django.urls import path 
from .views import CommentCreateView , CommentDeleteView

urlpatterns =[
    path("posts/<int:id>/comments/", CommentCreateView.as_view(),name = "create-comment"),
    path("comments/<int:id>/delete/", CommentDeleteView.as_view(), name = "delete-comment")
]
