from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    """Message object"""
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    text = models.TextField()
    time_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Represent message object"""
        return f"From {self.sender.username}, to {self.receiver.username}, time sent {self.time_sent}"


class Conversation(models.Model):
    """Conversation object"""
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    messages = models.ManyToManyField('Message', blank=True)

    def __str__(self):
        """Represent conversation object"""
        return f"user 1 {self.user1.username}, user 2 {self.user2.username}"