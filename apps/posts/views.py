from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Q

from .permissions import IsPostAuthorOrReadOnly
from .models import Post
from.serializers import PostSerializer

class PostViewSet(ModelViewSet):
    
    # filter posts by author id
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Post.objects.filter(
                Q(is_private = False)|Q(author=user)
                ).order_by('-created_at')
        
        return Post.objects.filter(
            is_private = False
            ).order_by('-created_at')

    def perform_create(self, serializer):

        serializer.save(author = self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "your message is deleted"},
            status=status.HTTP_200_OK,
        )
    
class PostViewSetv2(APIVIEW):