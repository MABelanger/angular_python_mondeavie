# -*- coding: utf-8 -*-
import datetime

from models import DaySchedule


def day_start_fct(self, obj):
    day_schedules = DaySchedule.objects.filter(schedule=obj.id)
    if day_schedules:
        day_start = day_schedules[0].day_start
        for day_schedule in day_schedules:
            if day_schedule.day_start < day_start:
                day_start = day_schedule.day_start

        return day_start

    return ""

def day_end_fct(self, obj):
    day_schedules = DaySchedule.objects.filter(schedule=obj.id)
    if day_schedules:
        day_end = day_schedules[0].day_end
        for day_schedule in day_schedules:
            if day_schedule.day_end > day_end:
                day_end = day_schedule.day_end

        return day_end

    return ""