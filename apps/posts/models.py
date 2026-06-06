from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title =  models.CharField(max_length= 1000)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    





# from django.db import models
# from django.conf import settings


# class Post(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
#     title = models.CharField(max_length= 1000)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     is_private = models.BooleanField(default=False)
    
#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.title
    

# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
#     commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
#     comment_text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['created_at']

#     def __str__(self):
#         return f"{self.commenter.email} -> {self.post.title}"
