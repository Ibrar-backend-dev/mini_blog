from rest_framework import serializers

from .models import Comment, CommentMedia


class CommentMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentMedia
        fields = ["id", "file", "media_type", "created_at"]
        read_only_fields = ["id", "media_type", "created_at"]


class CommentReadSerializer(serializers.ModelSerializer):
    commenter = serializers.ReadOnlyField(source="commenter.username")
    media = CommentMediaSerializer(many=True, read_only=True)
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "parent",
            "commenter",
            "comment_text",
            "created_at",
            "updated_at",
            "likes_count",
            "is_liked",
            "media",
            "replies",
        ]
        read_only_fields = fields

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(id=request.user.id).exists()

    def get_replies(self, obj):
        if obj.parent_id is not None:
            return []

        replies = getattr(obj, "prefetched_replies", None)
        if replies is None:
            replies = obj.replies.all().order_by("created_at")

        serializer = CommentReadSerializer(replies, many=True, context=self.context)
        return serializer.data


class CommentWriteSerializer(serializers.ModelSerializer):
    uploaded_file = serializers.FileField(required=False, write_only=True)

    class Meta:
        model = Comment
        fields = ["id", "parent", "comment_text", "uploaded_file"]
        read_only_fields = ["id"]

    def validate_uploaded_file(self, file):
        max_size = 3 * 1024 * 1024
        allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}

        if file.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG, PNG, WEBP, and GIF files are allowed.")

        if file.size > max_size:
            raise serializers.ValidationError("Each file must be less than or equal to 3 MB.")

        return file

    def validate(self, attrs):
        parent = attrs.get("parent")
        uploaded_file = attrs.get("uploaded_file")
        comment_text = attrs.get("comment_text", "").strip()
        post = self.context.get("post")

        if parent:
            if parent.post_id != post.id:
                raise serializers.ValidationError(
                    {"parent": "Parent comment must belong to the same post."}
                )

            if parent.parent_id is not None:
                raise serializers.ValidationError(
                    {"parent": "Only one level of replies is allowed."}
                )

        if not parent and uploaded_file:
            raise serializers.ValidationError(
                {"uploaded_file": "Attachments are only allowed on replies."}
            )

        if not comment_text and not uploaded_file:
            raise serializers.ValidationError(
                {"comment_text": "Empty comments are not allowed."}
            )

        attrs["comment_text"] = comment_text
        return attrs

    def _detect_media_type(self, file):
        if file.content_type == "image/gif":
            return CommentMedia.GIF
        return CommentMedia.IMAGE

    def _save_media_file(self, comment, file):
        CommentMedia.objects.create(
            comment=comment,
            file=file,
            media_type=self._detect_media_type(file),
        )

    def create(self, validated_data):
        uploaded_file = validated_data.pop("uploaded_file", None)
        post = self.context["post"]
        commenter = self.context["request"].user

        comment = Comment.objects.create(
            post=post,
            commenter=commenter,
            **validated_data,
        )

        if uploaded_file:
            self._save_media_file(comment, uploaded_file)

        return comment
