from account.models import Student
from django.contrib.auth.models import User

def get_student_from_user(user):
    try:
        return Student.objects.get(user=user)
    except:
        return None

def get_student_from_usernme(username):
    try:
        user = User.objects.get(username=username)
        return Student.objects.get(user=user)
    except:
        return None
