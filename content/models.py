from django.db import models
from django.contrib.auth.models import User # Or your custom user model if you made one
from django.urls import reverse # To get the URL for a post
from django.utils import timezone
from user.models import UserProfile
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts') # The user who created the post
    caption = models.TextField(blank=True, null=True) # Text content of the post
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) # Optional image
    video = models.FileField(upload_to='post_videos/', blank=True, null=True) # Optional video
    created_at = models.DateTimeField(default=timezone.now) # When the post was created
    # When the post was last updated
    hashtags = models.ManyToManyField('interaction.Hashtag', blank=True, related_name='posts')
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()


    # Optional: For future features like hashtags, location tagging, etc.
    # hashtags = models.ManyToManyField('Hashtag', blank=True)
    # location = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"Post by {self.author.username}"
    class Meta:
        ordering = ['-created_at'] # Order posts from newest to oldest

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.caption)
            unique_slug = base_slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)



