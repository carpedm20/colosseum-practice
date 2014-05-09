from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django import http
import json, random

from .forms import StudyGroupForm, EventForm
from account.forms import StudentCreateForm
from account.models import Student
from core.models import StudyGroup
from board.models import Post
from board.forms import CommentForm

from utils.func import *
from utils.say import *

########################
# Index
########################

def index(request, auth_form=None, user_form=None):
    form = StudentCreateForm(request.POST or None)
    context = RequestContext(request)

    if request.user.is_authenticated():
        current_student = get_student_from_user(request.user)

        if current_student is None:
            logout(request)
            redirect('/')
        else:
            print current_student

        # Study group for current User
        #study_group_list = current_student.study_group_set.all()

        study_group_list = StudyGroup.objects.all()
        student_list = Student.objects.all()

        total_event_count = 0.0
        finished_event_count = 0.0

        for event in current_student.assigned_to.all():
            total_event_count += 1

            if current_student in event.finished_student.all():
                finished_event_count += 1

        try:
            event_finished_percent = finished_event_count / total_event_count * 100.0
        except:
            event_finished_percent = -1

        for student in student_list:
            if student in current_student.friends.all():
                student.isFriend = True
            else:
                student.isFriend = False

        return render(request,
                      'core/home.html',
                      {'auth_form': auth_form,
                       'user_form': user_form,
                       'total_event_count': total_event_count,
                       'finished_event_count': finished_event_count,
                       'event_finished_percent' : event_finished_percent,
                       'student_list': student_list,
                       'study_group_list' : study_group_list})

    return render_to_response('core/index.html', locals(), context_instance=context)

########################
# Calendar
########################

@login_required
def view_calendar(request, study_group_id=None):
    #form = EventForm(data=request.POST or None, user=request.user)
    template = 'event/view_calendar_without_subnav.html'

    return render(request, template, {'total_calendar': True})

########################
# View help
########################

@login_required
def view_help(request):
    #form = EventForm(data=request.POST or None, user=request.user)
    template = 'core/view_help.html'

    post = Post.objects.get(id=1)
    form = CommentForm(data=request.POST or None, user=request.user, post_id=1)

    return render(request, template, {'post': post, 'form': form})


########################
# Search group
########################

@login_required
def search_study_group(request): #, search_query=""):
    #form = EventForm(data=request.POST or None, user=request.user)
    template = 'core/search_study_group.html'
    search_query = request.GET.get('search_query', '')

    study_group_list = StudyGroup.objects.filter(name__contains=search_query)

    s = random.choice(say.keys())

    return render(request,
                  template,
                  {'study_group_list' : study_group_list,
                   'say': say[s] + " : " + s,
                   'search_query': search_query })

########################
# Search group with tag
########################

@login_required
def search_study_group_with_tag(request): #, search_query=""):
    #form = EventForm(data=request.POST or None, user=request.user)
    template = 'core/search_study_group.html'
    search_tag = request.GET.get('search_tag', '')

    study_group_list = StudyGroup.objects.filter(tag_set__name__contains=search_tag)

    s = random.choice(say.keys())

    return render(request,
                  template,
                  {'study_group_list' : study_group_list,
                   'say': say[s] + " : " + s,
                   'search_tag': search_tag })

########################
# Do not display calendar guide
########################

@login_required
def no_calendar_guide(request):
    current_student = get_student_from_user(request.user) 

    current_student.display_calendar_guide = not current_student.display_calendar_guide
    current_student.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


########################
# Join study group
########################

@login_required
def join_study_group(request):
    if request.method == 'POST':
        group_unique_id = request.POST.get("group_unique_id", "")
        group = StudyGroup.objects.get(unique_id=group_unique_id)

        current_student = get_student_from_user(request.user) 

        if group in current_student.study_group_set.all():
          current_student.study_group_set.remove(group)
        else:
          current_student.study_group_set.add(group)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

########################
# Like study group
########################

@login_required
def like_study_group(request):
    if request.method == 'POST':
        group_unique_id = request.POST.get("group_unique_id", "")
        group = StudyGroup.objects.get(unique_id=group_unique_id)

        current_student = get_student_from_user(request.user) 

        if current_student in group.liked_student_set.all():
          group.liked_student_set.remove(current_student)
        else:
          group.liked_student_set.add(current_student)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

########################
# View study group
########################

@login_required
def view_study_group(request, study_group_id=None):
    study_group = StudyGroup.objects.get(unique_id=study_group_id)
    template = 'event/view_calendar.html'

    return render(request, template, {'study_group': study_group,  })

########################
# Create Study Group
########################

@login_required
def create_study_group(request):
    form = StudyGroupForm(data=request.POST, user=request.user)
    context = RequestContext(request)
    template = 'core/create_study_group.html'

    if request.method == "POST":
        if form.is_valid():
            group = form.save(commit=False)
            group.save()

            return redirect('/')
        else:
            return create_study_group_view(request)

    return create_study_group_view(request)

########################
# Delete Study Group
########################

@login_required
def delete_study_group(request, study_group_id=None):
    group = StudyGroup.objects.get(unique_id=study_group_id)
    group.delete()

    return redirect('/')

@login_required
def create_study_group_view(request):
    form = StudyGroupForm(data=request.POST or None, user=request.user)
    template = 'core/create_study_group.html'

    return render(request, template, {'form': form,  })

# Create your views here.
"""
class CreateStudyGroup(JSONResponseMixin, LoginRequiredMixin, CreateView):
    template_name = None  # JavaScript-only view
    model = Group
    form_class = StudyGroupForm

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect(reverse('core:recent-pins'))
        return super(CreateImage, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        image = form.save()

        return self.render_json_response({
            'success': {
                'id': StudyGroup.id
            }
        })

    def form_invalid(self, form):
        return self.render_json_response({'error': form.errors})
"""
