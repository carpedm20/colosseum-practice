from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studyplan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='home'),

    url(r'^calendar/$', views.view_calendar, name='view_calendar'),
    url(r'^no-calendar-guide/$', views.no_calendar_guide, name='no_calendar_guide'),

    url(r'^search/tag/', views.search_study_group_with_tag, name='search_study_group_with_tag'),
    url(r'^search/', views.search_study_group, name='search_study_group'),
    url(r'^help/$', views.view_help, name='view_help'),

    url(r'^create/$', views.create_study_group, name='create_study_group'),
    url(r'^(?P<study_group_id>\w+)/delete/$', views.delete_study_group, name='delete_study_group'),
    url(r'^join/$', views.join_study_group, name='join_study_group'),
    url(r'^like/$', views.like_study_group, name='like_study_group'),

    url(r'^(?P<study_group_id>\w+)/$', views.view_study_group, name='view_study_group'),

    url(r'^group/board/edit/$', include('django_summernote.urls')),

    url(r'^articles/comments/', include('django.contrib.comments.urls')),
)
