import os
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse
from django.shortcuts import render

from .models import File
from board.models import Post
from core.models import StudyGroup

from utils.func import *


def view_file_list(request, study_group_id=None):
    template = 'file/view_file_list.html'

    study_group = StudyGroup.objects.get(unique_id=study_group_id)
    file_list = []

    """
    for board in study_group.board_set.all():
        for post in board.post_set.all():
            for f in post.file_set.all():
                file_list.append(f)
    """

    return render(request, template, {'study_group': study_group})#'file_list': file_list})
    

@require_POST
def upload(request, study_group_id=None, post_id=None):
    f = upload_receive(request)

    instance = File(file_field=f)
    instance.save()

    post = Post.objects.get(id=post_id)
    instance.post = post
    instance.uploader = get_student_from_user(request.user)
    instance.save()

    basename = os.path.basename(instance.file_field.path)

    file_dict = {
        'name' : basename,
        'size' : f.size,

        'url': settings.MEDIA_URL + basename,
        'thumbnailUrl': settings.MEDIA_URL + basename,

        'deleteUrl': reverse('jfu_delete', kwargs = { 'study_group_id': study_group_id, 'pk': instance.pk, 'post_id': post_id }),
        'deleteType': 'POST',
    }

    return UploadResponse(request, file_dict)

@require_POST
def upload_delete(request, study_group_id=None, pk=None, post_id=None):
    success = True

    try:
        instance = File.objects.get(pk = pk)
        os.unlink(instance.file_field.path)
        instance.delete()
    except File.DoesNotExist:
        success = False

    return JFUResponse(request, success)
