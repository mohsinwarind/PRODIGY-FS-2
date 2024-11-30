from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.ImageField(upload_to = "profile_image", blank=True,null=True)

class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField( upload_to="post_images/'",blank= True , null = True)
    image_url = models.URLField(blank=True , null= True)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now_add = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True , related_name="likes")

    def __str__(self):
        return f"{self.user} - {self.post[:20]} - {self.timestamp}"
    

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"