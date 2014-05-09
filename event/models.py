#-*- coding: utf-8 -*-
from django.db import models

from core.models import StudyGroup
from account.models import Student
from tag.models import Tag

class Event(models.Model):
    name = models.CharField(max_length=30)
    details = models.CharField(max_length=50, blank=True)

    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)

    allDay = models.BooleanField(default=True)

    creator = models.ForeignKey(Student, related_name='event_creator')
    assigned_to = models.ManyToManyField(Student, related_name='assigned_to')
    finished_student = models.ManyToManyField(Student, related_name='finished_student')

    study_group = models.ForeignKey(StudyGroup, null=True)
    tag_set = models.ManyToManyField(Tag, blank=True, null=True)

    def __unicode__(self):
        #return "%s : %s ~ %s" % (self.name, self.start, self.end)
        return "%s" % (self.name)

    def get_start_as_korean(self):
        if self.start.hour == 12 and self.start.minute == 0:
            return "%s월 %s일" % (self.start.month,
                                  self.start.day)
        else:
            return "%s월 %s일  %s시 %s분" % (self.start.month,
                                             self.start.day,
                                             self.start.hour,
                                             self.start.minute)

    def get_end_as_korean(self):
        if self.end.hour == 12 and self.end.minute == 0:
            return "%s월 %s일" % (self.end.month,
                                  self.end.day)
        else:
            return "%s월 %s일  %s시 %s분" % (self.end.month,
                                             self.end.day,
                                             self.end.hour,
                                             self.end.minute)

    def is_all_day(self):
        return (self.start.month == self.end.month and self.start.day == self.end.day)

    def get_all_day(self):
        return "%s월 %s일" % (self.start.month, self.start.day)
