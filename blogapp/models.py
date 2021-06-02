from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100000)
    liked = models.ManyToManyField(User,blank=True,default=None,related_name='liked')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    comments = models.ManyToManyField(User,blank=True,default=None,related_name='commented')
    class Meta:
        verbose_name_plural="Post"
    
    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all.count()

    @property
    def num_comments(self):
        return self.commented.all.count()

LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,default='Like',max_length=10)

    class Meta:
        verbose_name_plural="Like"

    def __str__(self):
        return str(self.post.title + " liked by " + self.user.username)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.post.title + " commented by " + self.user.username)
# Create your models here.
