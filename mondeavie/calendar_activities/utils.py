
# -*- coding: utf-8 -*-

import json
import datetime
import locale
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponseBadRequest
from django.forms.models import model_to_dict
import collections
from mondeavie import settings


def send_my_mail(email_body, email_from):
    # Send email with activation key
    email_subject = 'Demande de Réservation de mondeavie.ca'
    reply_to = email_from
    email = EmailMessage(email_subject, email_body, 'info@mondeavie.mtrema.com',
        [settings.RESERVATION_SEND_TO],
        headers = {'Reply-To':reply_to})
    email.content_subtype = "html"  # Main content is now text/html
    email.send()

    '''
    send_mail(email_subject, email_body, email_from,\
    		[settings.RESERVATION_SEND_TO], fail_silently=False, html_message=email_body)
    '''

    #print "__send_mail", send_mail('Subject here', 'Here is the message.', 'from@example.com',
        #['michel.alexandre.belanger@gmail.com'], fail_silently=False)


def send_reserve_day_mail(body, reservation_header):
    client_dict = json.loads(body)
    errors = {}

    current_menu = client_dict.get('currentMenu')
    if not current_menu:
        errors['currentMenu'] = "Choisir une selections dans le menu"

    # If is a day selection
    is_selections = client_dict.get('isSelections')
    # The list of selected day
    selections = client_dict.get('selections')
    if not selections and is_selections:
        errors['selections'] = "Sélectionner une ou plusieurs journée(s)"

    name = client_dict.get('name')
    if not name:
        errors['name'] = "Ce champ est obligatoire."

    tel = client_dict.get('tel')
    if not tel:
        errors['tel'] = "Ce champ est obligatoire."

    email_from = client_dict.get('email')
    if not email_from:
        errors['email'] = "Ce champ est obligatoire."

    note = client_dict.get('note')

    if errors:
        return errors

    email_body = reservation_header + "<br>"
    email_body += client_dict.get('currentMenu') + "<br>"

    selections = client_dict.get('selections')
    for selection in selections:
        email_body += unicode(selection) + "<br>"

    email_body += "nom: " + name + "<br>"
    email_body += "tel: " + tel + "<br>"
    email_body += "email: " + email_from + "<br>"
    if note :
        email_body += "note: " + note + "<br>"

    send_my_mail(email_body, email_from)

    return None

def get_duration(hour_start, hour_end):
    hour_start_date = datetime.datetime.combine(datetime.date(2011, 01, 01), hour_start)
    hour_end_date = datetime.datetime.combine(datetime.date(2011, 01, 01), hour_end)
    duration = hour_end_date - hour_start_date
    return ":".join(str(duration).split(":")[0:2])

def get_day(my_date):
    locale.setlocale(locale.LC_ALL, "fr_CA.UTF-8")
    # str(2014-12-01) -> str(Lundi, 1 decembre 2014)
    date_time = datetime.datetime.strptime(str(my_date), '%Y-%m-%d')
    #return date_time.strftime('%A, ').title() + date_time.strftime('%d %B %Y')
    return date_time.strftime('%d %B %Y')


def get_day_month(my_date):
    locale.setlocale(locale.LC_ALL, "fr_CA.UTF-8")
    # str(2014-12-01) -> str(Lundi, 1 decembre 2014)
    date_time = datetime.datetime.strptime(str(my_date), '%Y-%m-%d')
    return date_time.strftime('%d %B %Y')


def _get_weekday(dayname):
    weekday = dayname.lower()

    if weekday == "lundi":
        return 0
    elif weekday == "mardi":
        return 1
    elif weekday == "mercredi":
        return 2
    elif weekday == "jeudi":
        return 3
    elif weekday == "vendredi":
        return 4
    elif weekday == "samedi":
        return 5
    elif weekday == "dimanche":
        return 6


def _get_day_range(day_start, day_end, dayname):
    # http://stackoverflow.com/questions/2381786/
    # how-to-get-the-python-date-object-for-last-wednesday
    from datetime import date
    from datetime import timedelta

    if date.today() > day_end:
        # if the range is passed.
        return []

    if date.today() > day_start :
        day_start = date.today()
    else :
        pass

    delta = day_end - day_start
    day_range_lst = []
    for x in range(delta.days + 1):
        my_date = day_start + timedelta(days=x)
        offset = (_get_weekday(dayname) - my_date.weekday()) % 7
        next_weekday = my_date + timedelta(days=offset)
        if next_weekday not in day_range_lst:
            day_range_lst.append(next_weekday)

    return day_range_lst


#Le mercredi du 30 au 15 janvier 2015

def _get_day_interval_str(days, dayname):

    if len(days) > 0:
        day_start = days[0]
        day_end = days[-1]
    else:
        return ""

    locale.setlocale(locale.LC_ALL, "fr_CA.UTF-8")
    day_start_str = datetime.datetime.strptime(str(day_start), '%Y-%m-%d')
    day_end_str = datetime.datetime.strptime(str(day_end), '%Y-%m-%d')

    str_day_start = '%d'
    if day_start.month != day_end.month:
        str_day_start += ' %B'

    if day_start.year != day_end.year:
        str_day_start += ' %Y'

    return "%s, du %s au %s (%s cours)" %(dayname.encode('utf-8'),
                        day_start_str.strftime(str_day_start),
                        day_end_str.strftime('%d %B %Y'),
                        len(days))

def get_months_dict(days):
    locale.setlocale(locale.LC_ALL, "fr_CA.UTF-8")
    months_dict = {}
    for day in days:
        month_name = day.strftime('%B %Y').capitalize()
        if not day.month in months_dict.keys():
            months_dict[day.month] = {}
            months_dict[day.month]['monthName'] = month_name
            months_dict[day.month]['list'] = []
        months_dict[day.month]['list'].append(get_day(day))

    return months_dict


def get_day_range_dict(day_start, day_end, dayname):
    day_range_dict = {}
    days = _get_day_range( day_start, day_end, dayname)
    print "__days", days
    day_range_dict['list'] = get_months_dict(days)
    day_range_dict['dayInterval'] = \
            _get_day_interval_str(days, dayname)

    return day_range_dict


def get_testing_days(q_testing_days):

    days = []
    for testing_day in q_testing_days:
        days.append(testing_day.day)
    testing_day_dict = {}
    testing_day_dict['list'] = get_months_dict(days)
    
    if get_months_dict(days) :
        return testing_day_dict

def get_hour(my_hour):
    return ":".join(str(my_hour).split(":")[0:2])