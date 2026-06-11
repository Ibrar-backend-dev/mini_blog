from rest_framework import permissions
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