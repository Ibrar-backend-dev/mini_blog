from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Comment(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_comments", blank=True)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def clean(self):
        if self.parent:
            if self.parent.post_id != self.post_id:
                raise ValidationError("Parent comment must belong to the same post as current comment.")

            if self.parent.parent_id is not None:
                raise ValidationError("Only one level of replies is allowed.")

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.post.title}"


class CommentMedia(models.Model):
    IMAGE = "image"
    GIF = "gif"

    MEDIA_TYPE_CHOICES = (
        (IMAGE, "image"),
        (GIF, "gif"),
    )

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="comment_media/")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def clean(self):
        if self.comment.parent is None:
            raise ValidationError("Attachments are only allowed on replies.")

    def __str__(self):
        return f"Media for comment {self.comment.id} - {self.media_type}"
