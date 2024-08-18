from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200, null=False)
    title = models.CharField(max_length=200, null=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'url'], name='unique_user_id_url')
        ]

    def __str__(self):
        return self.url

class Tag(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['link_id', 'tag'], name='unique_link_id_tag')
        ]

    def __str__(self):
        return self.tag

class Category(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['link_id', 'category'], name='unique_link_id_category')
        ]

    def __str__(self):
        return self.category