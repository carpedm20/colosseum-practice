from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .forms import BoardForm, PostForm, CommentForm
from .models import Post, Comment
from core.models import StudyGroup

import sys
from utils.func import *

########################
# List board
########################

@login_required
def list_board(request):
    form = BoardForm(data=request.POST or None, user=request.user)

    context = RequestContext(request)
    template = 'core/create_board.html'

    if request.method == "POST":
        if form.is_valid():
            board = form.save(commit=False)
            board.save()

            return HttpResponseRedirect(reverse('core:view_study_group', kwargs={'study_group_id':study_group_id,}))
        else:
            return create_board_view(request)

    return create_board_view(request)

########################
# View post
########################

@login_required
def view_post(request, study_group_id, post_id, board_id=None):
    form = CommentForm(data=request.POST or None, user=request.user, post_id=post_id)

    context = RequestContext(request)
    template = 'board/view_post.html'

    study_group = StudyGroup.objects.get(unique_id=study_group_id)
    current_student = get_student_from_user(request.user)

    try:
        post = Post.objects.get(id=post_id)

        for comment in post.comment_set.all():
            comment.content = comment.content.replace('\r\n','<br />')

        if current_student in study_group.student_set.all():
            if current_student not in post.viewed_student.all():
                post.viewed_student.add(current_student)

        return render(request, template, {'form': form, 'study_group': study_group,'post': post, 'board_id': post.board.id, 'user': request.user})

    except:
        for e in sys.exc_info():
            print e
        return HttpResponseRedirect(reverse('core:view_study_group', kwargs={'study_group_id':study_group_id,}))


########################
# Create comment
########################

@login_required
def create_comment(request, study_group_id, post_id, board_id=None):
    form = CommentForm(data=request.POST or None, user=request.user, post_id=post_id)
    context = RequestContext(request)

    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

########################
# Delete comment
########################

@login_required
def delete_comment(request, study_group_id=None, board_id=None, comment_id=None, post_id=None):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    if study_group_id == '0':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    else:
        return HttpResponseRedirect(reverse('view_post', kwargs={'study_group_id':study_group_id, 'board_id':board_id, 'post_id': post_id, }))


########################
# Create board
########################

@login_required
def create_board(request, study_group_id):
    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    form = BoardForm(data=request.POST or None, user=request.user, study_group=study_group)

    context = RequestContext(request)
    template = 'core/create_board.html'

    if request.method == "POST":
        if form.is_valid():
            board = form.save(commit=False)
            board.save()

            return HttpResponseRedirect(reverse('core:view_study_group', kwargs={'study_group_id':study_group_id,}))
        else:
            return create_board_view(request, study_group)

    return create_board_view(request, study_group)

@login_required
def create_board_view(request, study_group):
    form = BoardForm(data=request.POST or None, user=request.user, study_group=study_group)
    template = 'board/create_board.html'

    return render(request, template, {'form': form, 'study_group': study_group})

########################
# Create post
########################

@login_required
def create_post(request, study_group_id=None, board_id=None):
    form = PostForm(data=request.POST or None, user=request.user, board_id=board_id)

    context = RequestContext(request)
    template = 'core/create_post.html'

    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return HttpResponseRedirect(reverse('core:view_study_group', kwargs={'study_group_id':study_group_id,}))
        else:
            return create_post_view(request, study_group, board_id)

    return create_post_view(request, study_group, board_id)

@login_required
def create_post_view(request, study_group, board_id):
    form = PostForm(data=request.POST or None, user=request.user, board_id=board_id)
    template = 'board/create_post.html'

    return render(request, template, {'form': form, 'study_group': study_group, 'board_id': board_id})

########################
# Edit post
########################

@login_required
def edit_post(request, study_group_id=None, board_id=None, post_id=None):
    instance = Post.objects.get(id=post_id)
    form = PostForm(data=request.POST or None, user=request.user, instance=instance, post_id=post_id)

    context = RequestContext(request)
    template = 'core/create_post.html'

    study_group = StudyGroup.objects.get(unique_id=study_group_id)

    if request.method == "POST":
        print "!@#!@#"
        if form.is_valid():
            print "!@#!@#"
            post = form.save()
            #post.save()

            return HttpResponseRedirect(reverse('core:view_study_group', kwargs={'study_group_id':study_group_id,}))
        else:
            return edit_post_view(request, study_group, board_id, post_id)

    return edit_post_view(request, study_group, board_id, post_id)

########################
# Delete post
########################

@login_required
def delete_post(request, study_group_id=None, board_id=None, post_id=None):
    instance = Post.objects.get(id=post_id)
    instance.delete()

    return HttpResponseRedirect(reverse('core:view_study_group', kwargs={'study_group_id':study_group_id,}))

@login_required
def edit_post_view(request, study_group, board_id, post_id):
    instance = Post.objects.get(id=post_id)
    form = PostForm(data=request.POST or None, user=request.user, instance=instance, post_id=post_id)

    template = 'board/create_post.html'

    return render(request, template, {'form': form, 'study_group': study_group, 'board_id': board_id, 'post_id': post_id})

