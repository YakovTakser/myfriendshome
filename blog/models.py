from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
from accounts.models import Profile


class Post(models.Model):
    """Post object"""
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    topic_choices = (
        ('Health', 'Health'),
        ('Entertainment', 'Entertainment'),
        ('Arts', 'Arts'),
        ('Travel', 'Travel'),
    )

    topic = models.CharField(max_length=30, choices=topic_choices, default='General')

    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(Profile, related_name='likes', blank=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def like_count(self):
        return self.likes.all().count()

    def __str__(self):
        """Represent post object"""
        return self.title


class Comment(models.Model):
    """Comment object"""
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        """Represent comment object"""
        return self.text


class Image(models.Model):
    """Image object"""
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(max_length=300, upload_to='')

    def __str__(self):
        """Represent Image object"""
        return self.image.path


class TopicOfPost(models.Model):
    """topic of post object"""
    topic = models.CharField(max_length=255)
    count = models.IntegerField(default=0)

    def __str__(self):
        """Represent topic of post object"""
        return self.topic
