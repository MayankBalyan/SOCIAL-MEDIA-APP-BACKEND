from datetime import timezone

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from content.models import Post


# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.name}"
class PostComment(models.Model):

    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=now)
    def __str__(self):
        return self.comment[:35]+'by @'+self.user.username



