# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Teacher, CourseName, Course, Schedule,\
    DaySchedule, DayName, TestingDay

from models import Speaker, Conference, DayConference

class CourseNameAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseName, CourseNameAdmin)


class TeacherAdmin(admin.ModelAdmin):
    pass
admin.site.register(Teacher, TeacherAdmin)


class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CourseAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    def day_schedules(self, inst):
        return ','.join([str(b) for b in inst.dayschedule_set.all()])

    list_display = ('name', 'day_schedules')

admin.site.register(Schedule, ScheduleAdmin)

class TestingDayAdmin(admin.ModelAdmin):
    pass
admin.site.register(TestingDay, TestingDayAdmin)


class DayScheduleAdmin(admin.ModelAdmin):
    pass
admin.site.register(DaySchedule, DayScheduleAdmin)


class DayNameAdmin(admin.ModelAdmin):
    pass
admin.site.register(DayName, DayNameAdmin)


'''
Conference Section
'''

class SpeakerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Speaker, SpeakerAdmin)


class ConferenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Conference, ConferenceAdmin)


class DayConferenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(DayConference, DayConferenceAdmin)
