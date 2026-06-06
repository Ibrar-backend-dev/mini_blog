from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Post

        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'is_private']

        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


# from rest_framework import serializers
# from .models import Post, Comment


# class PostSerializer(serializers.ModelSerializer):
#     author = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Post
#         fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'is_private']

#         read_only_fields = ['id', 'author', 'created_at', 'updated_at']

# class CommentSerializer(serializers.ModelSerializer):
#     commenter = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'commenter', 'comment_text', 'created_at', 'updated_at']

#         read_only_fields = ['id','post', 'commenter', 'created_at', 'updated_at']

#     def    validate_comment_text(self, value):

#         if len(value.strip()) < 2:
#             raise serializers.ValidationError("Comment text is too short.")
        
#         return value