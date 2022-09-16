from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from autoslug import AutoSlugField


class Guide(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    text = RichTextUploadingField()
    moderated = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="guides", blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = 'Guide'
        verbose_name_plural = 'Guides'

    def __str__(self):
        return self.title


class Comment(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
