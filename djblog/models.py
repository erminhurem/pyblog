from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published']),
        ]
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


    def __str__(self):
        return self.title

