from django.contrib.auth.models import User
from django.db import models


class Mindmap(models.Model):
    title = models.CharField('назва', max_length=100)
    mindmap = models.TextField('ментальна карта')
    owner = models.ForeignKey(User, related_name='mindmaps', on_delete=models.CASCADE, verbose_name='власник')
    created_at = models.DateTimeField('створено о')
    edited_at = models.DateTimeField('змінено о')
    shared = models.BooleanField('спільне користування', default=False)

    class Meta:
        verbose_name = 'ментальна карта'
        verbose_name_plural = 'ментальні карти'

    def __str__(self):
        return self.title


class Classroom(models.Model):
    title = models.CharField('назва', max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='вчитель')
    students = models.ManyToManyField(User, related_name='classrooms', verbose_name='учні')

    class Meta:
        verbose_name = 'клас'
        verbose_name_plural = 'класи'

    def __str__(self):
        return self.title
