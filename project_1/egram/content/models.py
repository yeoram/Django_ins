from django.db import models

# Create your models here.
class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)

class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()

class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)