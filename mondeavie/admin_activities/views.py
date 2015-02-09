# -*- coding: utf-8 -*-

from rest_framework import status
from .forms import LoginForm
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from models import Teacher, CourseName, Course, Schedule, DaySchedule,\
                    DayName, TestingDay

from models import Speaker, Conference, DayConference
from serializers import TeacherSerializer, CourseNameSerializer,\
                        CourseSerializer,\
                        ScheduleSerializer,\
                        DayNameSerializer,\
                        DayScheduleSerializer,\
                        TestingDaySerializer


from serializers import ConferenceSerializer, SpeakerSerializer, DayConferenceSerializer,\
                        ConferenceNestedSpeakerSerializer

from django.shortcuts import get_object_or_404
from rest_framework import permissions

from rest_framework import generics
from django.views import generic
from django.contrib.auth.decorators import login_required

class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class CourseNameList(generics.ListCreateAPIView):
    queryset = CourseName.objects.all()
    serializer_class = CourseNameSerializer


class CourseNameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseName.objects.all()
    serializer_class = CourseNameSerializer


class CourseList(generics.ListCreateAPIView):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Course.objects.all()
        teacher_id = self.request.QUERY_PARAMS.get('teacher', None)
        course_name_id = self.request.QUERY_PARAMS.get('course_name', None)
        if teacher_id is not None and\
                    course_name_id is not None:
            # Check if the object exist.
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            course_name = get_object_or_404(CourseName, pk=course_name_id)

            # Filter the queryset
            queryset = queryset.filter(teacher_id=teacher.id)
            queryset = queryset.filter(course_name_id=course_name.id)
        return queryset


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class ScheduleList(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Schedule.objects.all()
        course_id = self.request.QUERY_PARAMS.get('course', None)
        if course_id is not None:
            # Check if the object exist.
            course = get_object_or_404(Course, pk=course_id)

            # Filter the queryset
            queryset = queryset.filter(course_id=course.id)
        return queryset


class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class DayNameList(generics.ListCreateAPIView):
    queryset = DayName.objects.all()
    serializer_class = DayNameSerializer


class DayNameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayName.objects.all()
    serializer_class = DayNameSerializer


class DayScheduleList(generics.ListCreateAPIView):
    serializer_class = DayScheduleSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned DaySchedules to a given schedule,
        by filtering against a `schedule` query parameter in the URL.
        """
        queryset = DaySchedule.objects.all()
        schedule_id = self.request.QUERY_PARAMS.get('schedule', None)
        if schedule_id is not None:
            # Check if the object exist.
            schedule = get_object_or_404(Schedule, pk=schedule_id)
            # Filter the queryset
            queryset = queryset.filter(schedule_id=schedule.id)
        return queryset


class DayScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DaySchedule.objects.all()
    serializer_class = DayScheduleSerializer

'''
Testing Days
'''
class TestingDayList(generics.ListCreateAPIView):
    serializer_class = TestingDaySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned TestingDays to a given schedule,
        by filtering against a `schedule` query parameter in the URL.
        """
        queryset = TestingDay.objects.all()
        day_schedule_id = self.request.QUERY_PARAMS.get('day_schedule', None)
        if day_schedule_id is not None:
            # Check if the object exist.
            day_schedule = get_object_or_404(DaySchedule, pk=day_schedule_id)
            # Filter the queryset
            queryset = queryset.filter(day_schedule_id=day_schedule.id)
        return queryset


class TestingDayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestingDay.objects.all()
    serializer_class = TestingDaySerializer


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'admin_activities/account_login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        self._next = form.cleaned_data['next']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


    def get_success_url(self):
        return '/admin_activities/'




class SpeakerList(generics.ListCreateAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer


class SpeakerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer






class ConferenceNestedSpeakerList(generics.ListCreateAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceNestedSpeakerSerializer


class ConferenceList(generics.ListCreateAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class ConferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class DayConferenceList(generics.ListCreateAPIView):
    serializer_class = DayConferenceSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = DayConference.objects.all()
        conference_id = self.request.QUERY_PARAMS.get('conference', None)
        if conference_id is not None:
            # Check if the object exist.
            conference = get_object_or_404(Conference, pk=conference_id)
            # Filter the queryset
            queryset = queryset.filter(conference_id=conference.id)
        return queryset


class DayConferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayConference.objects.all()
    serializer_class = DayConferenceSerializer