from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateView.as_view(
        template_name="admin_activities/index.html"),\
        login_url='/admin_activities/login/')),
    url(r'^login/$', views.LoginView.as_view(), name='accounts-login'),

    url(r'^logout/$', 'django.contrib.auth.views.logout',
    {
        'next_page': '/admin_activities/login/',
    }, name='logout'),

    url(r'^api/teachers/$', views.TeacherList.as_view()),
    url(r'^api/teachers/(?P<pk>[0-9]+)$', views.TeacherDetail.as_view()),

    url(r'^api/course_names/$', views.CourseNameList.as_view()),
    url(r'^api/course_names/(?P<pk>[0-9]+)$', views.CourseNameDetail.as_view()),

    url(r'^api/courses/$', views.CourseList.as_view()),
    url(r'^api/courses/(?P<pk>[0-9]+)$', views.CourseDetail.as_view()),

    url(r'^api/schedules/$', views.ScheduleList.as_view()),
    url(r'^api/schedules/(?P<pk>[0-9]+)$', views.ScheduleDetail.as_view()),

    url(r'^api/day_names/$', views.DayNameList.as_view()),
    url(r'^api/day_names/(?P<pk>[0-9]+)$', views.DayNameDetail.as_view()),

    url(r'^api/day_schedules/$', views.DayScheduleList.as_view()),
    url(r'^api/day_schedules/(?P<pk>[0-9]+)$', views.DayScheduleDetail.as_view()),

    url(r'^api/testing_days/$', views.TestingDayList.as_view()),
    url(r'^api/testing_days/(?P<pk>[0-9]+)$', views.TestingDayDetail.as_view()),


    url(r'^api/speakers/$', views.SpeakerList.as_view()),
    url(r'^api/speakers/(?P<pk>[0-9]+)$', views.SpeakerDetail.as_view()),

    url(r'^api/conferences/$', views.ConferenceList.as_view()),
    url(r'^api/conferences/(?P<pk>[0-9]+)$', views.ConferenceDetail.as_view()),
    url(r'^api/nested/speakers/conferences/$', views.ConferenceNestedSpeakerList.as_view()),


    url(r'^api/day_conferences/$', views.DayConferenceList.as_view()),
    url(r'^api/day_conferences/(?P<pk>[0-9]+)$', views.DayConferenceDetail.as_view()),


    url(r'^courses/$', TemplateView.as_view(template_name="admin_activities/admin_courses.html")),
    url(r'^conferences/$', TemplateView.as_view(template_name="admin_activities/admin_conferences.html")),
)