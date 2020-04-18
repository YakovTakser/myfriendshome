from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
# Profile of user model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(max_length=300, upload_to='', null=True, blank=True)
    theme_image = models.ImageField(max_length=300, upload_to='', null=True, blank=True)
    profession = models.CharField(max_length=255, blank=True)
    about = models.CharField(max_length=1000, blank=True)
    friends = models.ManyToManyField('Profile', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            # If image's height or width more than 300 then resize the image
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return str(self.user.username)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    time_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    text = models.TextField()
    time_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "From {}, to {}, time sent {}".format(self.sender.username, self.receiver.username, self.time_sent)

class Conversation(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    messages = models.ManyToManyField('Message', blank=True)