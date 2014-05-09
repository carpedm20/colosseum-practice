from django.db import models
from account.models import Student

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=200)
    user_set = models.ManyToManyField(Student, null=True)

    tag_set = models.ManyToManyField('Tag', null=True)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
