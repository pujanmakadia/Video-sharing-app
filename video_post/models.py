from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class VideoPost(models.Model):

    title = models.CharField(max_length=100)
    content = models.FileField(upload_to='uploads')
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    likes = models.ManyToManyField(get_user_model(), related_name="video_posts")
    dislikes = models.ManyToManyField(get_user_model(), related_name="video_posts_dislikes")

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})