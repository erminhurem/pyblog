from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().filter(status=Post.Status.PUBLISHED))

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, unique_for_date='publish')
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    objects = models.Manager()
    published = PublishedManager()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update= models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    tags = TaggableManager()
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        return reverse('djblog:post_detail', args=[
                                                self.publish.year, 
                                                self.publish.month, 
                                                self.publish.day, 
                                                self.slug])

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.post_likes.count()

    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.post_likes.filter(user=user).exists()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'



