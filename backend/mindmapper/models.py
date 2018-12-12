from django.contrib.auth.models import User
from django.db import models


class Mindmap(models.Model):
    title = models.CharField(max_length=100)
    mindmap = models.TextField()
    owner = models.ForeignKey(User, related_name='mindmaps', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
