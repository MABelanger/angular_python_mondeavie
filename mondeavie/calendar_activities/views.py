# -*- coding: utf-8 -*-

import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics

from admin_activities.models import Course, DaySchedule, CourseName,\
                                DayConference, Conference, TestingDay
from serializers import DayScheduleNestedParentsSerializer,\
                        CourseNestedChildsSerializer,\
                        CourseNameNestedCourseSerializer,\
                        ConferenceNestedChildsSerializer


from calendar_activities.calendar_builder.day_schedule_cal import DayScheduleCal
from calendar_activities.calendar_builder.day_cal import DayCal

from calendar_activities.calendar_builder import utils as cal_utils
from calendar_activities.calendar_builder import display as cal_display
import utils


class CourseNestedChilds(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseNestedChildsSerializer


class DayScheduleNestedParentsList(generics.ListCreateAPIView):
    queryset = DaySchedule.objects.all()
    serializer_class = DayScheduleNestedParentsSerializer

class CourseNameNestedCourseList(generics.ListCreateAPIView):
    queryset = CourseName.objects.all()
    serializer_class = CourseNameNestedCourseSerializer

class ConferenceNestedChilds(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceNestedChildsSerializer

def get_data(day_schedule):
    if day_schedule.schedule.course.course_name.icon:
        data = '<img src="%s">' %(day_schedule.schedule.course.course_name.icon.url) + "<br>"
    else :
        data = ''
    #":".join("10:22:00".split(":")[0:2])
    data += "&nbsp;" + ":".join(str(day_schedule.hour_start).split(":")[0:2]) + "-<br>"
    data += ":".join(str(day_schedule.hour_end).split(":")[0:2]) + "<br>"
    data += str(day_schedule.schedule.course.teacher)
    day_schedule.day_name.id -1

    return data


def calandar_builder(request):
    context = {}

    day_cal_lst = []

    for day_number in range(1,8):
        # Add 7 day to the list
        day_cal_lst.append(DayCal("lundi", day_number))


    day_schedules = DaySchedule.objects.all()

    for day_schedule in day_schedules:
        # Add all schedule to day_cal_lst with the data
        if day_schedule.schedule.course.is_visible == True:
            min_start = cal_utils.get_minute(day_schedule.hour_start)
            min_end = cal_utils.get_minute(day_schedule.hour_end)
            row_start = cal_utils.get_row_number(min_start)
            row_end = cal_utils.get_row_number(min_end)
            # crosse, always colspan of 2
            row_end = row_start + 2

            url = "/calendar_activities/#/courses/" + str(day_schedule.schedule.course.id)
            ds = DayScheduleCal(row_start, row_end, get_data(day_schedule), url)
            day_id = day_schedule.day_name.id
            day_cal_lst[day_id - 1].add_day_schedule(ds)
        

    # Transform list of day with list of row of
    row_lst = cal_utils.get_row_lst(day_cal_lst)
    
    #cal_utils.add_col_hour(row_lst)

    context['table'] = cal_display.print_table(row_lst)

    context_instance = RequestContext(request)
    return render_to_response("calendar_activities/calendar_builder.html",\
                    context, context_instance)

def conferences(request):
    context = {}

    context['day_conferences'] = DayConference.objects.filter(conference__is_visible=True).\
                            order_by('day', 'hour_start')

    context_instance = RequestContext(request)
    return render_to_response("calendar_activities/conferences.html",\
                    context, context_instance)


def _get_day_conference_html_content(day_conference):
    from django.template.loader import get_template
    from django.template import Context

    from calendar_activities.serializers import ConferenceNestedChildsSerializer

    
    ser = ConferenceNestedChildsSerializer()
    speakers_str = ser.get_speakers_str(day_conference.conference)

    template_data = {}
    template_data['reserveFor'] = 'attelier/conférence'
    template_data['peoples'] = speakers_str
    template_data['day'] = utils.get_day(day_conference.day)
    template_data['hourStart'] = utils.get_hour(day_conference.hour_start)
    template_data['hourEnd'] = utils.get_hour(day_conference.hour_end)
    template_data['title'] = day_conference.conference.title

    htmly = get_template('calendar_activities/reserve_day_html_msg.html')
    d = Context(template_data)
    html_content = htmly.render(d)

    return unicode(html_content)

@csrf_exempt
def json_msg_reserve_day_conference(request, pk):
    day_conference = get_object_or_404(DayConference, pk=pk)
    reserve_obj_dict = {}
    html_content = _get_day_conference_html_content(day_conference)

    if request.method == 'GET':

        reserve_obj_dict['reserveFor'] = 'conference'
        reserve_obj_dict['parentPath'] = '#/conferences/' + str(day_conference.conference.id)

        # Create the client Object
        reserve_obj_dict['client'] = {}
        reserve_obj_dict['client']['selections'] = []
        reserve_obj_dict['client']['reservationHeader'] = html_content


    elif request.method == 'POST':
        errors = utils.send_reserve_day_mail(request.body, html_content)

        if errors : 
            errors_obj = {"errors" : errors}
            return HttpResponse(json.dumps(errors_obj),\
                    content_type="application/json")

            #return HttpResponseBadRequest(json.dumps(errors),\
                    #content_type="application/json")

    return HttpResponse(json.dumps(reserve_obj_dict),\
                content_type="application/json")

@csrf_exempt
def json_msg_reserve_day_schedule(request, pk):
    day_schedule = get_object_or_404(DaySchedule, pk=pk)

    reserve_obj_dict = {}
    reserve_obj_dict['reserveFor'] = 'cours'
    reserve_obj_dict['day'] = day_schedule.day_name.name
    reserve_obj_dict['parentPath'] = '#/courses/' + str(day_schedule.schedule.course.id)
    reserve_obj_dict['hourStart'] = utils.get_hour(day_schedule.hour_start)
    reserve_obj_dict['hourEnd'] = utils.get_hour(day_schedule.hour_end)
    reserve_obj_dict['peoples'] = unicode(day_schedule.schedule.course.teacher)
    reserve_obj_dict['title'] = unicode(day_schedule.schedule.course.course_name) +\
     ', ' + unicode(day_schedule.schedule.name)

    reservation_header = "Demande de r&eacute;servation pour %s"\
                                    %(reserve_obj_dict['reserveFor'])
    reservation_header += " <strong>%s</strong>" %(reserve_obj_dict['title'])
    reservation_header += " avec %s" %(reserve_obj_dict['peoples'])
    reservation_header += " le %s" %(reserve_obj_dict['day'])
    reservation_header += " de %s" %(reserve_obj_dict['hourStart'])
    reservation_header += " &agrave; %s." %(reserve_obj_dict['hourEnd'])

    # Create the client Object
    reserve_obj_dict['client'] = {}
    reserve_obj_dict['client']['selections'] = []
    reserve_obj_dict['client']['reservationHeader'] = reservation_header


    if request.method == 'GET':


        reserve_obj_dict['dayStart'] = utils.get_day(day_schedule.day_start)
        reserve_obj_dict['dayEnd'] = utils.get_day(day_schedule.day_end)
        reserve_obj_dict['dayRange'] = utils.get_day_range_dict(
                                            day_schedule.day_start,
                                            day_schedule.day_end,
                                            day_schedule.day_name.name)

        q_testing_days = TestingDay.objects.filter(day_schedule=day_schedule)
        reserve_obj_dict['testingDays'] = utils.get_testing_days(q_testing_days)

    elif request.method == 'POST':
        errors = utils.send_reserve_day_mail(request.body, reservation_header)

        if errors : 
            errors_obj = {"errors" : errors}
            return HttpResponse(json.dumps(errors_obj),\
                    content_type="application/json")
            #return HttpResponseBadRequest(json.dumps(errors),\
                    #content_type="application/json")

        reserve_obj_dict = {}
    return HttpResponse(json.dumps(reserve_obj_dict),\
                content_type="application/json")