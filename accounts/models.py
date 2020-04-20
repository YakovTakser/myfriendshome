from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Profile(models.Model):
    """Profile of a user object"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(max_length=300, upload_to='', null=True, blank=True)
    theme_image = models.ImageField(max_length=300, upload_to='', null=True, blank=True)
    profession = models.CharField(max_length=255, blank=True)
    about = models.CharField(max_length=1000, blank=True)
    friends = models.ManyToManyField('Profile', blank=True)

    def save(self, *args, **kwargs):
        """Save a profile and checks if image sizes more than 300px"""
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        """Represent a user object"""
        return self.user.username


class FriendRequest(models.Model):
    """Friend request object"""
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    time_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Represent a friend request object"""
        return f"From {self.from_user.username}, to {self.to_user.username}"



