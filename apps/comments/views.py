from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from apps.comments.tasks import send_comment_notification_email
from apps.posts.models import Post

from.models import Comment
from .serializers import CommentSerializer


class CommentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post( self, request, id ):

        post =get_object_or_404(Post, id=id)

        if post.is_private:
            raise PermissionDenied(" Comments are only allowed on public posts.")
        
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        
        comment=serializer.save(
            post=post,
            commenter=request.user
        )

        send_comment_notification_email.delay(
            post_title=post.title,
            commenter_name=request.user.username,
            comment_text=comment.comment_text,
            author_email=post.author.email,
        )

        

        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )
    

class CommentDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        comment=get_object_or_404(Comment, id=id)

        if comment.commenter != request.user:
            raise PermissionDenied("Only the commenter can delete the comment.")
        
        comment.delete()

        return Response(
            {"message": "your message is deleted"},
            status=status.HTTP_200_OK,
        )
    
