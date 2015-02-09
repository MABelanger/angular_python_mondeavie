from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import views

urlpatterns = patterns('',
    ## Course
    url(r'^$', TemplateView.as_view(template_name=\
        "calendar_activities/calendar-2.html")),
    url(r'^calendar_builder/$', views.calandar_builder),

    # Angular Partials
    url(r'^partials/course_detail.html$',\
        TemplateView.as_view(template_name=\
            "calendar_activities/partials/course_detail.html")),
    url(r'^partials/reserve_day_schedule.html$',\
        TemplateView.as_view(template_name=\
            "calendar_activities/partials/reserve_day_schedule.html")),

    # JSON
    url(r'^json/reserve/day_schedules/(?P<pk>[0-9]+)$',\
        views.json_msg_reserve_day_schedule),

    # API REST
    url(r'^api/nested/courses/course_name/$',\
        views.CourseNameNestedCourseList.as_view()),
    url(r'^api/nested/childs/courses/(?P<pk>[0-9]+)$',\
        views.CourseNestedChilds.as_view()),


    ## Conference
    url(r'^conferences/$', views.conferences),

    # Angular Partials
    url(r'^partials/conference_detail.html$',\
        TemplateView.as_view(template_name=\
            "calendar_activities/partials/conference_detail.html")),
    url(r'^partials/reserve_day_conference.html$',\
        TemplateView.as_view(template_name=\
            "calendar_activities/partials/reserve_day_conference.html")),

    url(r'^partials/reserve_table_days.html$',\
        TemplateView.as_view(template_name=\
            "calendar_activities/partials/reserve_table_days.html")),

    # JSON
    url(r'^json/reserve/day_conferences/(?P<pk>[0-9]+)$',\
        views.json_msg_reserve_day_conference),

    # API REST
    url(r'^api/nested/parents/day_schedules/$',\
        views.DayScheduleNestedParentsList.as_view()),
    url(r'^api/nested/childs/conferences/(?P<pk>[0-9]+)$',\
        views.ConferenceNestedChilds.as_view()),
)