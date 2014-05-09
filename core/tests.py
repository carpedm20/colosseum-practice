from django.test import TestCase
from django.contrib.auth.models import User

from core.models import StudyGroup, Tag
from account.models import Student
from school.models import School

class StudnetGroupTestCase(TestCase):
    def setUp(self):
        unist = School(name="UNIST")
        kaist = School(name="KAIST")
        postech = School(name="POSTECH")

        user = User(username="hello@gmail.com", password="123")
        user.save()
        Student.objects.create(user=user, school=unist)

        user = User(username="serious@gmail.com", password="123")
        user.save()
        Student.objects.create(user=user, school=postech)

        user = User(username="kaist@gmail.com", password="123")
        user.save()
        Student.objects.create(user=user, school=kaist)

        user = User(username="unist@gmail.com", password="123")
        user.save()
        Student.objects.create(user=user, school=unist)

        group = StudyGroup(name="TOEIC study", details="over 990")
        group.save()
# Create your tests here.
