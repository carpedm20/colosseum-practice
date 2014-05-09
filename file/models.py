from django.db import models
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from core.models import Student
from board.models import Board, Post

fs = FileSystemStorage(location='media')
upload_to='media'

# Create your models here.
class File(models.Model):
    file_field = models.FileField(upload_to=upload_to, default = None, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    post = models.ForeignKey(Post, blank=True, null=True)
    uploader = models.ForeignKey(Student, blank=True, null=True)

    def __unicode__(self):
        return self.file_field.name.replace(upload_to+'/','')

    def get_full_path(self):
        return 'media/' + self.file_field.name

