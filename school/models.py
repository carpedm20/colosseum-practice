from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200, unique= True)
    logo_url = models.URLField(max_length=200, blank=True)
    course_set = models.ManyToManyField('Course', blank=True)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    course_id = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.name
