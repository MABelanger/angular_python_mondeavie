
# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.forms.models import model_to_dict
from admin_activities.models import Course, Schedule, DaySchedule,\
                            CourseName, Conference, DayConference, Speaker, TestingDay
import admin_activities
import utils as cal_utils
from admin_activities import  utils as admin_utils
import datetime

class Base64ImageField(serializers.ImageField):

    # Model Object to JSON
    def to_native(self, obj):
        if obj and hasattr(obj, 'url'):
            return obj.url
        return ""

class CourseNestedParentsSerializer(serializers.ModelSerializer):
    obj_unicode = serializers.SerializerMethodField('obj_unicode_fct')
    image = Base64ImageField(required=False) # Field optional
    # Nested object
    teacher = admin_activities.serializers.TeacherSerializer()
    course_name = admin_activities.serializers.CourseNameSerializer()


    def obj_unicode_fct(self, obj):
        return obj 

    class Meta:
        model = Course
        fields = ('id', 'teacher', 'course_name', 'obj_unicode', 'course_type',\
            'note', 'image', 'description', 'price', 'is_visible')


class CourseNestedChildsSerializer(serializers.ModelSerializer):
    obj_unicode = serializers.SerializerMethodField('obj_unicode_fct')
    image = Base64ImageField(required=False) # Field optional
    schedules = serializers.SerializerMethodField('schedules_fct')
    #daySchedules = serializers.SerializerMethodField('day_schedules_fct')

    teacher = admin_activities.serializers.TeacherSerializer()
    course_name = admin_activities.serializers.CourseNameSerializer()


    def obj_unicode_fct(self, obj):
        return obj

    def schedules_fct(self, obj):
        def get_day_schedule_lst(schedule):
            day_schedule_lst = []

            for day_schedule in DaySchedule.objects.filter(schedule=schedule).\
                                order_by('day_name__id', 'hour_start'):

                #DaySchedule.objects.filter(schedule=schedule):
                day_schedule_dict = model_to_dict(day_schedule)

                # Correct the right values Ex:. Lundi 13:00, 14:00
                day_schedule_dict['day_name'] = day_schedule.day_name.name

                day_schedule_dict['hour_end'] = \
                ":".join(str(day_schedule.hour_end).split(":")[:2])

                day_schedule_dict['hour_start'] = \
                ":".join(str(day_schedule.hour_start).split(":")[:2])

                q_testing_days = TestingDay.objects.filter(day_schedule=day_schedule,\
                                    day__gt=datetime.date.today())

                day_schedule_dict['testingDays'] = cal_utils.get_testing_days(q_testing_days)

                day_schedule_lst.append(day_schedule_dict)

            return day_schedule_lst



        schedule_lst = []
        for schedule in Schedule.objects.filter(course=obj):
            schedule_dict = model_to_dict(schedule)
            schedule_dict['day_start'] = admin_utils.day_start_fct(self, schedule)
            schedule_dict['day_end'] = admin_utils.day_end_fct(self, schedule)
            schedule_dict['daySchedules'] = get_day_schedule_lst(schedule)
            schedule_lst.append(schedule_dict)



        return schedule_lst


    #def day_schedules_fct(self, obj):


    class Meta:
        model = Course
        fields = ('id', 'teacher', 'course_name', 'obj_unicode', 'course_type',\
            'note', 'image', 'description', 'price', 'schedules', 'is_visible')



class ScheduleNestedParentsSerializer(serializers.ModelSerializer):
    course = CourseNestedParentsSerializer()

    day_start = serializers.SerializerMethodField('day_start_fct')
    day_end = serializers.SerializerMethodField('day_end_fct')

    def day_start_fct(self, obj):
        return admin_utils.day_start_fct(self, obj)

    def day_end_fct(self, obj):
        return admin_utils.day_end_fct(self, obj)

    class Meta:
        model = Schedule
        fields = ('id', 'course', 'name', 'day_start', 'day_end', 'description',)



class DayScheduleNestedParentsSerializer(serializers.ModelSerializer):
    schedule = ScheduleNestedParentsSerializer()
    class Meta:
        model = DaySchedule
        fields = ('id', 'schedule', 'day_name', 'day_name', 'hour_start',\
            'hour_end', 'is_full')


class CourseNameNestedCourseSerializer(serializers.ModelSerializer):
    icon = Base64ImageField(required=False) # Field optional
    courses = serializers.SerializerMethodField('courses_fct')

    def courses_fct(self, obj):

        try:
            course_lst = []
            for course in Course.objects.filter(course_name=obj, is_visible=True):
                course_dict = {}
                course_dict['id'] = course.id
                course_dict['teacher'] = course.teacher
                course_lst.append(course_dict)
        except:
            course_lst = None

        return course_lst

    class Meta:
        model = CourseName
        fields = ('id', 'name', 'icon', 'courses')



class ConferenceNestedChildsSerializer(serializers.ModelSerializer):
    speakers = admin_activities.serializers.SpeakerSerializer()
    image = Base64ImageField(required=False) # Field optional
    day_conferences = serializers.SerializerMethodField('day_conferences_fct')
    speakers_str = serializers.SerializerMethodField('get_speakers_str')
    duration = serializers.SerializerMethodField('get_duration')


    def get_speakers_str(self, obj):

        def get_speaker_str(obj, pre):
            if pre:
                return pre + obj.first_name + ' ' + obj.last_name
            else :
                return obj.first_name + ' ' + obj.last_name

        speakers = Speaker.objects.filter(ConferenceSpeaker__id=obj.id)

        speaker_lst = list(speakers)
        speaker_str_lst = []

        if speakers:
            # Alexandre Belanger
            speaker_str_lst.append(get_speaker_str(speaker_lst[0], ""))

            for speaker in speaker_lst[1:-1]:
                # ,Johane frechette, Guillaume Rimbeau
                speaker_str_lst.append(get_speaker_str(speaker, ", "))

            # et Jose Frechette
            if len(speaker_lst) > 1:
                speaker_str_lst.append(get_speaker_str(speaker_lst[-1], " et "))

            return ''.join(speaker_str_lst)

        return ""


    def day_conferences_fct(self, obj):

        day_conference_lst = []

        day_conferences = DayConference.objects.filter(conference=obj)
        for day_conference in day_conferences:
            day_conference_dict = {}
            day_conference_dict['id'] = day_conference.id
            day_conference_dict['day'] = cal_utils.get_day(day_conference.day)
            day_conference_dict['hour_start'] = cal_utils.get_hour(day_conference.hour_start)
            day_conference_dict['hour_end'] = cal_utils.get_hour(day_conference.hour_end)
            day_conference_dict['duration'] = cal_utils.get_duration(day_conference.hour_start, day_conference.hour_end)
            day_conference_dict['is_full'] = day_conference.is_full
            day_conference_lst.append(day_conference_dict)

        return day_conference_lst

    class Meta:
        model = Conference
        fields = ('id', 'speakers', 'image', 'title', 'description',\
            'abstract', 'price', 'day_conferences', 'speakers_str', 'tel', 'note',\
            'school_name', 'school_url', 'is_visible')