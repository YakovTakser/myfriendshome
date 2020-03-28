from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
from accounts.models import Profile


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    topic = models.CharField(
        max_length=30,
        choices=(
            ('General', 'General'),
            ('Sports & Fitness', 'Sports & Fitness'),
            ('Health', 'Health'),
            ('Entertainment', 'Entertainment'),
            ('Music', 'Music'),
            ('Education', 'Education'),
            ('Science & Tech', 'Science & Tech'),
            ('Humor', 'Humor'),
            ('Food & Drink', 'Food & Drink'),
            ('Family & Parenting', 'Family & Parenting'),
            ('Style', 'Style'),
            ('Arts', 'Arts'),
            ('Travel', 'Travel'),
            ('Animals', 'Animals'),
        ),
        default='choice1',
    )
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(Profile, related_name='likes', blank=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})

    def like_count(self):
        return self.likes.all().count()

    def __str__(self):
         return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text



class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='')

    def __str__(self):
        return self.image.path



