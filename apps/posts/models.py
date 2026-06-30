from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title =  models.CharField(max_length= 1000)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL , related_name = "liked_posts" , blank = True)

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.title
    

class PostMedia(models.Model):
    VIDEO ="video"
    IMAGE = "image"

    MEDIA_TYPE_CHOICES = (
        (IMAGE , "image"),
        (VIDEO , "video"),
    )
    
    post = models.ForeignKey( Post , on_delete= models.CASCADE ,related_name="media")
    file = models.FileField(upload_to ="posts_media/")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
