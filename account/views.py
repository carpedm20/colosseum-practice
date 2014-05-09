from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.functional import lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
import random

from .forms import StudentCreateForm, StudentAuthForm
from core.views import index
from utils.func import *
from utils.say import *

reverse_lazy = lambda name=None, *args: lazy(reverse, str)(name, args=args)


########################
# View profile
########################

@login_required
def view_profile(request): #, search_query=""):
    #form = EventForm(data=request.POST or None, user=request.user)
    template = 'account/view_profile.html'

    try:
        user_id = request.GET.get('user_id','')
        student = Student.objects.get(user__username=user_id)
    except:
        student = None
        pass

    s = random.choice(say.keys())

    return render(request,
                  template,
                  {'student' : student,
                   'say' : say[s] + " : " + s,})


########################
# Follow friends
########################

@login_required
def follow(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        student = get_student_from_usernme(username)

        current_student = get_student_from_user(request.user) 

        if student in current_student.friends.all():
          current_student.friends.remove(student)
        else:            
          current_student.friends.add(student)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

########################
# Sign in (Log in)
########################

def sign_in(request):
    form = StudentAuthForm(data=request.POST)
    template = 'account/sign_in.html'

    if request.method == 'POST':
        if form.is_valid():
            # Success
            login(request, form.get_user())
            next_url = request.POST.get("next_url", "/")

            return redirect('/')
        else:
            # Failure
            return sign_in_view(request)

    return sign_in_view(request)

##############################
# Sign in View (Log in View)
##############################

def sign_in_view(request):
    form = StudentAuthForm(request.POST or None)
    template = 'account/sign_in.html'

    s = random.choice(say.keys())

    return render(request, template, {'form': form, 'say' : say[s] + " : " + s})
    

########################
# Sign up (Join)
########################

def sign_up(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            # `commit=False`: before save it to database, just keep it in memory
            username = form.clean_username()
            password = form.clean_password2()
            new_user = form.save()
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect("/")
    else:
        form = StudentCreateForm() 

    return render(request, "core/index.html",  {'form': form,  })

########################
# Sign out (Log out)
########################

@login_required
def sign_out(request):
    logout(request)
    #messages.success(request, 'You have successfully logged out.')
    return redirect('/')
