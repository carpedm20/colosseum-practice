from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import http
from django.http import HttpResponse
from django.utils import timezone
import json
import datetime

import dateutil.parser
from utils.func import *

from .models import Event
from core.models import StudyGroup


########################
# Calendar
########################

@login_required
def view_calendar(request, study_group_id=None):
    #form = EventForm(data=request.POST or None, user=request.user)
    study_group = StudyGroup.objects.get(unique_id=study_group_id)
    template = 'event/view_calendar.html'

    return render(request, template, {'study_group': study_group, })

########################
# Event
########################

@login_required
def create_event(request, study_group_id=None):
    current_student = get_student_from_user(request.user)
    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    if request.is_ajax() and request.method == "POST":
        title = request.POST.get('title')
        start_timestamp = request.POST.get('start')
        end_timestamp = request.POST.get('end')
        allDay = request.POST.get('allDay')
        assigned_list = request.POST.get('assigned_list')

        assigned_list = assigned_list.split(',')

        if allDay is 'true':
            allDay = True
        else:
            allDay = False

        start = dateutil.parser.parse(start_timestamp)
        end = dateutil.parser.parse(end_timestamp)

        event = Event(name=title, details='', start=start, end=end, creator=current_student, study_group=study_group)
        event.save()

        for email in assigned_list:
            student = Student.objects.get(user__username=email)
            event.assigned_to.add(student)

        event.save()

        study_group.event_set.add(event)

        #movie_json = {}
        #html = t.render(Context(context))

        #movie_json['source'] = html

        #results = []
        #results.append(movie_json)

        #data = json.dumps(results)
        data = "success"
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def create_event_view(request):
    form = EventForm(data=request.POST or None, user=request.user)
    template = 'core/create_event.html'

    return render(request, template, {'form': form,  })

########################
# Finish event
########################

@login_required
def finish_event_as_json(request, study_group_id=None):
    current_student = get_student_from_user(request.user)
    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    if request.is_ajax() and request.method == "POST":
        id = request.POST.get('id')

        event = Event.objects.get(id=id)

        if current_student in event.finished_student.all():
            event.finished_student.add(current_student)
            data = "success"
        else:
            data = "fail: already finished"
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def unfinish_event_as_json(request, study_group_id=None):
    current_student = get_student_from_user(request.user)
    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    if request.is_ajax() and request.method == "POST":
        id = request.POST.get('id')

        event = Event.objects.get(id=id)

        if current_student in event.finished_student.all():
            event.finished_student.add(current_student)
            data = "success"
        else:
            data = "fail: not finished"
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

########################
# Finish event
########################

@login_required
def finish_event(request, study_group_id=None, event_id=None):
    current_student = get_student_from_user(request.user)
    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    event = Event.objects.get(id=event_id)

    if current_student not in event.finished_student.all():
        event.finished_student.add(current_student)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def unfinish_event(request, study_group_id=None, event_id=None):
    current_student = get_student_from_user(request.user)
    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    event = Event.objects.get(id=event_id)

    if current_student in event.finished_student.all():
        event.finished_student.remove(current_student)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


########################
# Edit event
########################

@login_required
def edit_event(request, study_group_id=None):
    current_student = get_student_from_user(request.user)
    #study_group = StudyGroup.objects.get(unique_id=study_group_id)

    if request.is_ajax() and request.method == "POST":
        id = request.POST.get('id')
        dayDelta = int(request.POST.get('dayDelta'))
        minuteDelta = int(request.POST.get('minuteDelta'))

        event = Event.objects.get(id=id)

        event.start = event.start + datetime.timedelta(days=dayDelta) \
                                  + datetime.timedelta(minutes=dayDelta)
        event.end = event.end + datetime.timedelta(days=dayDelta) \
                              + datetime.timedelta(minutes=dayDelta)

        event.save()

        data = "success"
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

########################
# Complete event
########################

@login_required
def complete_event(request, study_group_id=None):
    current_student = get_student_from_user(request.user)
    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    if request.is_ajax() and request.method == "POST":
        id = request.POST.get('id')
        dayDelta = int(request.POST.get('dayDelta'))
        minuteDelta = int(request.POST.get('minuteDelta'))

        event = Event.objects.get(id=id)

        event.start = event.start + datetime.timedelta(days=dayDelta) \
                                  + datetime.timedelta(minutes=dayDelta)
        event.end = event.end + datetime.timedelta(days=dayDelta) \
                              + datetime.timedelta(minutes=dayDelta)

        event.save()

        data = "success"
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

########################
# Delete event
########################

@login_required
def delete_event(request, study_group_id=None):
    current_student = get_student_from_user(request.user)
    #study_group = StudyGroup.objects.get(unique_id=study_group_id)

    if request.is_ajax() and request.method == "POST":
        id = request.POST.get('id')

        event = Event.objects.get(id=id)
        event.delete()

        data = "success"
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

########################
# Calendar
########################

@login_required
def view_calendar(request, study_group_id=None):
    #form = EventForm(data=request.POST or None, user=request.user)
    template = 'core/view_calendar.html'

    return render(request, template, {})

@login_required
def get_event_as_json(request, study_group_id=None): 
    current_student = get_student_from_user(request.user)

    if study_group_id == '0':
        events = current_student.assigned_to.all()
    else:
        study_group = StudyGroup.objects.get(unique_id=study_group_id)
        events = study_group.event_set.all()

    event_list = []

    for event in events: 
        event_start = event.start.astimezone(timezone.get_default_timezone()) 
        event_end = event.end.astimezone(timezone.get_default_timezone())

        if event_start.hour == 0 and event_start.minute == 0: 
            Allday = True 
        else: 
            Allday = False

        student_list = []
        for student in event.assigned_to.all():
            student_list.append(student.user.username)

        student_list = ','.join(student_list)

        if current_student in event.finished_student.all():
            finished = True
        else:
            finished = False

        event_list.append ({ 
            'id':  event.id , 
            'unique_id':  event.study_group.unique_id , 
            'start':  event_start.strftime ( '%Y-%m- %d %H:%M:%S' ), 
            'end':  event_end.strftime ( '%Y-%m- %d %H:%M:%S' ), 
            'title':  event.name, 
            'allDay': Allday,
            'student_list': student_list,
            'finished': finished,
        })

    if len(event_list)  ==  0 : 
        raise http.Http404 
    else : 
        return http.HttpResponse(json.dumps(event_list), content_type = 'application/json' )
