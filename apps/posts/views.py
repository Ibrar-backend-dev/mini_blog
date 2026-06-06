from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .models import Post
from.serializers import PostSerializer

class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = Post.objects.all()

    def perform_create(self, serializer):

        serializer.save(author = self.request.user)