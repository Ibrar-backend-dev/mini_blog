from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser , JSONParser ,MultiPartParser
from rest_framework import status


from apps.comments.tasks import send_comment_notification_email, send_reply_notification_email
from apps.posts.models import Post

from.models import Comment
from .serializers import CommentReadSerializer, CommentWriteSerializer



def get_visible_post(post_id , user):
    
    post = get_object_or_404(Post , id = post_id)

    if post.is_private and (not user.is_authenticated or user != post.author):
        raise PermissionDenied("Comments are only allowed on public posts.")
    
    return post


def get_visible_comment(comment_id, user):
    comment = get_object_or_404(
        Comment.objects.select_related("post", "commenter"),
        id = comment_id ,
    )

    if comment.post.is_private and (not user.is_aithenticated or user != comment.post.author):
        raise PermissionDenied("You do not have permission to access this comment.")
    
    return comment


class PostCommentListCreateView(APIView):
    parser_classes= [MultiPartParser , FormParser , JSONParser]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]
    

    def get(self, request, post_id):
        post = get_visible_post(post_id, request.user)

        reply_queryset = (
            Comment.objects.filter(parent__isnull=False)
            .select_related("commenter")
            .prefetch_related("likes" , "media")
            .oreder_by("created_at")
        )

        comments = (
            Comment.objects.filter(post=post, parent__isnull= True)
            .select_related("commenter")
            .prefetch_related("likes","media" , Prefetch("replies" , queryset= reply_queryset, to_attr = "prefetch_replies"),
        )
        .order_by("created_at")
        )

        serializer = CommentReadSerializer(
            comments,
            many = True,
            context = {"request": request},
        )
        return Response(serializer.data, status= status.HTTP_200_OK)
    

def post(self, request, post_id):
    post = get_visible_post(post_id)

    serializer = CommentWriteSerializer(
        data = request.data,
        context={"request":request , "post":post},
    )

    serializer.is_valid(raise_exception=True)
    comment =serializer.save()

    if comment.parent_id is None:
        if post.author != request.user:
            send_comment_notification_email(
                post_title=post.title,
                commenter_name=request.user.username,
                comment_text=comment.comment_text,
                author_email=post.author.email,
            )
    else:
        if comment.parent.commenter != request.user:
            send_reply_notification_email.delay(
                post_title=post.title,
                parent_commenter_email = comment.parent.commenter.email,
                replier_name = request.user.username,
                reply_text = comment.comment_text,
            )

    return Response(
        CommentReadSerializer(comment , content = {"request": request}).data,
        status = status.HTTP_201_CREATED,
        )


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_visible_comment(comment_id, request.user)

        if comment.commenter != request.user:
            raise PermissionDenied("Only the commenter can delete the comment.")
        
        comment.delete()

        return Response(
            {"message":"Your message is deleted."},
            status=status.HTTP_200_OK,
        )
    
class CommentLikeView(APIView):

    def post(self, request, comment_id):
        comment = get_visible_comment(comment_id, request.user)
        comment.likes.add(request.user)

        return Response(
            {
                "likes_count": comment.likes.count(),
                "is_liked": comment.likes.filter(id =request.user.id).exists(),
            },
            status=status.HTTP_200_OK,
        )
    
    def delete(self, request, comment_id):
        comment = get_visible_comment(comment_id, request.user)
        comment.likes.remove(request.user)

        return Response(
            {
                "likes_count":comment.likes.count(),
                "is_liked": comment.likes.filter(id =request.user.id).exists(),
            },
            status = status.HTTP_200_OK,
        )

# class CommentCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post( self, request, id ):

#         post =get_object_or_404(Post, id=id)

#         if post.is_private:
#             raise PermissionDenied(" Comments are only allowed on public posts.")
        
#         serializer = CommentReadSerializer(data=request.data)
#         serializer.is_valid(raise_exception = True)
        
#         comment=serializer.save(
#             post=post,
#             commenter=request.user
#         )

#         send_comment_notification_email.delay(
#             post_title=post.title,
#             commenter_name=request.user.username,
#             comment_text=comment.comment_text,
#             author_email=post.author.email,
#         )

        

#         return Response(
#             CommentReadSerializer(comment).data,
#             status=status.HTTP_201_CREATED
#         )
    

# class CommentDeleteView(APIView):

#     permission_classes = [IsAuthenticated]

#     def delete(self, request, id):
#         comment=get_object_or_404(Comment, id=id)

#         if comment.commenter != request.user:
#             raise PermissionDenied("Only the commenter can delete the comment.")
        
#         comment.delete()

#         return Response(
#             {"message": "your message is deleted"},
#             status=status.HTTP_200_OK,
#         )
    
