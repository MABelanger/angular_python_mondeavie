# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    tel = models.CharField(max_length=15, blank=True)
    school_name = models.CharField(max_length=30, blank=True)
    school_url = models.URLField(max_length=100, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

'''
Course section
'''
class CourseName(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ImageField(upload_to='course_icon', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class Course(models.Model):
    teacher = models.ForeignKey(Teacher)
    is_visible = models.BooleanField(default=True)
    course_name = models.ForeignKey(CourseName, blank=True)
    course_type = models.CharField(max_length=50, blank=True)
    note = models.CharField(max_length=512, blank=True)
    image = models.ImageField(upload_to='course_pic', null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s avec %s' % (self.course_name, self.teacher)

    class Meta:
        unique_together = (("teacher", "course_name"),)


class Schedule(models.Model):
    course = models.ForeignKey(Course)
    # Yoga Doux
    name = models.CharField(max_length=50)
    # 15 Jan au 5 mars

    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        pass
        #unique_together = (("course_category", "course"),)
        #verbose_name = _('schedule')
        #verbose_name_plural = _('schedules')

class DayName(models.Model):
    name = models.CharField(max_length=10)
    def __unicode__(self):
        return u'%s' % (self.name)

class DaySchedule(models.Model):
    is_full = models.BooleanField(default=False)
    schedule = models.ForeignKey(Schedule)
    day_name = models.ForeignKey(DayName)
    # 15 Jan au 5 mars
    day_start = models.DateField()
    day_end = models.DateField()

    hour_start = models.TimeField()
    hour_end = models.TimeField()
    

    def __unicode__(self):
        return u'%s: de %s a %s du %s au %s' % \
        (self.day_name, self.hour_start, self.hour_end,\
            self.day_start, self.day_end)


class TestingDay(models.Model):
    day_schedule = models.ForeignKey(DaySchedule)
    day = models.DateField()
    is_full = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.day)

'''
Conference section
'''

class Speaker(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Conference(models.Model):
    is_visible = models.BooleanField(default=True)
    speakers = models.ManyToManyField(Speaker, related_name='ConferenceSpeaker', blank=False, null=False)
    tel = models.CharField(max_length=15, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    price = models.TextField(blank=True)
    school_name = models.CharField(max_length=30, blank=True)
    school_url = models.URLField(max_length=100, blank=True)
    note = models.CharField(max_length=512, blank=True)
    image = models.ImageField(upload_to='atelier_image', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.title)


# le 5 janvier...
# le 10 janvier...
class DayConference(models.Model):
    is_full = models.BooleanField(default=False)
    conference = models.ForeignKey(Conference)
    day = models.DateField()
    hour_start = models.TimeField()
    hour_end = models.TimeField()

    def __unicode__(self):
        return u'%s: de %s a %s' % (self.day, self.hour_start, self.hour_end)
