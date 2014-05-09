from django.db import models

from core.models import Student
from tag.models import Tag

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=300)

    creator = models.ForeignKey(Student)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(blank=False)

    tag_set = models.ManyToManyField(Tag, blank=True, null=True)
    board = models.ForeignKey(Board, blank=True, null=True)

    creator = models.ForeignKey(Student)
    created_at  = models.DateTimeField(auto_now_add=True)

    viewed_student = models.ManyToManyField(Student, blank=True, null=True, related_name='viewed_student')

    def __unicode__(self):
        return self.name

class Comment(models.Model):
    content = models.TextField(blank=False)

    post = models.ForeignKey(Post, blank=True, null=True)

    creator = models.ForeignKey(Student)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content
