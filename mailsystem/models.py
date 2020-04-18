from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
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