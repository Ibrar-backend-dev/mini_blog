from rest_framework import serializers
from django.db import transaction
from .models import Post, PostMedia


class PostMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostMedia
        fields = ["id", "file", "media_type", "created_at"]
        read_only_fields = ["id", "media_type", "created_at"]


class PostSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)
    media = PostMediaSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "is_private",
            "media",
            "uploaded_files",
            "likes_count",
            "is_liked",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_at",
            "updated_at",
            "media",
            "likes_count",
            "is_liked",
        ]

    def validate_uploaded_files(self, files):
        max_files = 3
        max_size = 10 * 1024 * 1024

        allowed_image_types = {"image/jpeg", "image/png", "image/webp"}
        allowed_video_types = {"video/mp4", "video/webm"}
        allowed_types = allowed_image_types | allowed_video_types

        if len(files) > max_files:
            raise serializers.ValidationError("You can only uploads 3 files.")

        for file in files:
            if file.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "only  jpeg , webp , png , mp4 , webm are allowed to uploads. "
                )

            if file.size > max_size:
                raise serializers.ValidationError(
                    "Each file must be less than or equal to 10 MB."
                )
        return files

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(id=request.user.id).exists()

    def _detect_media_type(self, file):
        if file.content_type.startswith("image/"):
            return PostMedia.IMAGE
        return PostMedia.VIDEO

    def _save_media_files(self, post, files):
        for file in files:
            PostMedia.objects.create(
                post=post,
                file=file,
                media_type=self._detect_media_type(file),
            )

    def create(self, validated_data):
        uploaded_files = validated_data.pop("uploaded_files", [])

        with transaction.atomic():
            post = Post.objects.create(**validated_data)
            self._save_media_files(post, uploaded_files)
        return post

    def update(self, instance, validated_data):

        if "uploaded_files" in validated_data:
            raise serializers.ValidationError({
                "uploaded_files": "Updating media is not allowed."
            })
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
