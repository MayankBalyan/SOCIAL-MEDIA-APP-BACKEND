from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from PIL import Image# Import Pillow for image resizing (optional but recommended)

class UserProfile(models.Model):
    username = models.CharField(primary_key=True, max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='C:\\Users\\kumar\\OneDrive\\Desktop\\SOCIAL MEDIA APP BACKEND\\media\\user.png', upload_to='profile_pics')
    bio= models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)