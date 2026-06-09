from django.db import models
from django.conf import settings


class Comment(models.Model):

    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    commenter= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.post.title}"
    
