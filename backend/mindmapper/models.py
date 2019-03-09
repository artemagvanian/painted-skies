from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Mindmap(models.Model):
    title = models.CharField(max_length=100)
    mindmap = models.TextField()
    owner = models.ForeignKey(User, related_name='mindmaps', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    # shared = models.BooleanField(default=False)


# class Classroom(models.Model):
#     title = models.CharField(max_length=100)
#     head_teacher = models.ForeignKey('Profile', on_delete=models.CASCADE)
#
#
# class Profile(models.Model):
#     ROLES = (
#         ('TR', 'Teacher'),
#         ('ST', 'Student')
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=2, choices=ROLES, default='ST')
#     classrooms = models.ManyToManyField(Classroom, related_name='students')
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance):
#     instance.profile.save()
