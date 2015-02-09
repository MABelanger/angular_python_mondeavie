from admin_activities.models import Schedule
from admin_activities.models import DaySchedule
for day_schedule in DaySchedule.objects.all():
  day_schedule.day_start = day_schedule.schedule.day_start
  day_schedule.day_end = day_schedule.schedule.day_end
  day_schedule.save()
