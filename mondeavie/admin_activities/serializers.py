# -*- coding: utf-8 -*-

import base64
import json
import datetime

import django.core
from django.forms import widgets
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.forms.models import model_to_dict
from models import Teacher, CourseName, Course, Schedule, DaySchedule,\
        DayName, TestingDay

import utils as admin_utils
from calendar_activities import utils as cal_utils
from models import Speaker, Conference, DayConference


class Base64ImageField(serializers.ImageField):

    # Model Object to JSON
    def to_native(self, obj):
        if obj and hasattr(obj, 'url'):
            return obj.url
        return ""

    # https://gist.github.com/yprez/7704036
    # JSON to Model object
    def from_native(self, data):
        #if is a dictionnary that contain ['name', 'base64']
        #coming from the javascript object.
        if not isinstance(data, basestring):
            file_name = data.pop("name", None)
            # data is now a basestring
            data = data.pop("base64", None)

        if isinstance(data, basestring) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,') # format ~= data:image/X,
            ext = format.split('/')[-1] # guess file extension


            data = ContentFile(base64.b64decode(imgstr), name=file_name)
            return super(Base64ImageField, self).from_native(data)
        return data


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'tel', 'school_name',\
            'school_url')


class CourseNameSerializer(serializers.ModelSerializer):
    icon = Base64ImageField(required=False) # Field optional
    class Meta:
        model = CourseName
        fields = ('id', 'name', 'icon')


class CourseSerializer(serializers.ModelSerializer):
    obj_unicode = serializers.SerializerMethodField('obj_unicode_fct')
    image = Base64ImageField(required=False) # Field optional

    def obj_unicode_fct(self, obj):
        return obj 

    class Meta:
        model = Course
        fields = ('id', 'teacher', 'course_name', 'obj_unicode', 'course_type',\
            'note', 'image', 'description', 'price', 'is_visible')


class ScheduleSerializer(serializers.ModelSerializer):

    day_start = serializers.SerializerMethodField('day_start_fct')
    day_end = serializers.SerializerMethodField('day_end_fct')

    def day_start_fct(self, obj):
        return admin_utils.day_start_fct(self, obj)

    def day_end_fct(self, obj):
        return admin_utils.day_end_fct(self, obj)

    class Meta:
        model = Schedule
        fields = ('id', 'course', 'name', 'day_start', 'day_end', 'description')


class DayNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'name',)


class DayScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DaySchedule
        fields = ('id', 'schedule', 'day_name', 'day_name', 'hour_start',\
            'hour_end', 'day_start', 'day_end', 'is_full')


class TestingDaySerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField('day_name_fct')

    def day_name_fct(self, obj):
        return cal_utils.get_day(obj.day)

    class Meta:
        model = TestingDay
        fields = ('id', 'day', 'day_name', 'day_schedule', 'is_full')


# Conference Section 
class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('id', 'first_name', 'last_name')


class ConferenceSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False) # Field optional
    #speakers = SpeakerSerializer(required=True)

    class Meta:
        model = Conference
        fields = ('id', 'speakers', 'tel', 'title', 'description','abstract', 'price',\
            'image', 'note', 'school_name', 'school_url', 'is_visible')


class ConferenceNestedSpeakerSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False) # Field optional
    speakers = SpeakerSerializer(many=True, blank=False, required=True)


    class Meta:
        model = Conference
        fields = ('id', 'speakers', 'tel', 'title', 'description', 'abstract', 'price',\
            'image', 'note', 'school_name', 'school_url', 'is_visible')
        extra_kwargs = {'speakers': {'allow_empty': False}}


class DayConferenceSerializer(serializers.ModelSerializer):

    day_name = serializers.SerializerMethodField('day_name_fct')

    def day_name_fct(self, obj):
        return cal_utils.get_day(obj.day)


    class Meta:
        model = DayConference
        fields = ('id', 'conference', 'day', 'day_name', 'hour_start', 'hour_end', 'is_full')
