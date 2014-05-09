#-*- coding: utf-8 -*-
import uuid
import base64

from django.db import models
from django.utils.encoding import smart_unicode

from account.models import Student
from board.models import Board
from tag.models import Tag

# Create your models here.
class StudyGroup(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=300)

    student_set = models.ManyToManyField(Student, blank=True, null=True, related_name='study_group_set')
    liked_student_set = models.ManyToManyField(Student, blank=True, null=True, related_name='liked_student_set')

    tag_set = models.ManyToManyField(Tag, blank=True, null=True)
    board_set = models.ManyToManyField(Board, null=True)

    creator = models.ForeignKey(Student, related_name='study_group_creator')
    leader = models.ManyToManyField(Student, related_name='leader')

    is_private = models.BooleanField(default=False)

    unique_id = models.CharField(max_length=100, null=True, blank=True, unique=True)

    start_date = models.DateField()

    def __init__(self):
        board = Board(name="Plan", details="", creator=None)
        self.board_set.add(board)
        board = Board(name="Develop", details="", creator=None)
        self.board_set.add(board)
        board = Board(name="Design", details="", creator=None)
        self.board_set.add(board)

    #def __init__(self, *args, **kwargs):
    #    super(StudyGroup, self).__init__(*args, **kwargs)

    def current_phase(self):
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)

        if self.start_date + week*3 < now:
            return 2 # design
        elif self.start_date + week*2 < now:
            return 1 # dev
        elif self.start_date + week < now:
            return 0 # plan

    def save(self, *args, **kwargs):
        if not self.unique_id:
            while True:
                unique_id = base64.b64encode(str(uuid.uuid4()))[:10]
                group = StudyGroup.objects.filter(unique_id=unique_id)

                if len(group) is 0:
                    self.unique_id = unique_id
                    break
            
        super(StudyGroup, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
