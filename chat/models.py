from django.db import models

from account.models import Student

# Create your models here.
class Comments(models.Model):
    user = models.ForeignKey(Student)
    text = models.CharField(max_length=255)

    def __unicode__(self):
        return "[%s] %s" % (user, text)
