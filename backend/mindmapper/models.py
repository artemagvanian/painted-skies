from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Mindmap(models.Model):
    title = models.CharField(max_length=100)
    mindmap = models.TextField()
    owner = models.ForeignKey(User, related_name='mindmaps', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    edited_at = models.DateTimeField()
    shared = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Classroom(models.Model):
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classrooms = models.ManyToManyField(Classroom, related_name='students')


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
