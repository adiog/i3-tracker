import hashlib
import json
import re
from collections import defaultdict

from datetime import timedelta, date
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datetime_safe import datetime

from i3_tracker_server.server.settings import BLACKLIST_NAME, BLACKLIST_TYPE, OVERRIDE_TIME, DUPLICATE_TIME
from i3_tracker_server.tracker.svg import printsvg, printsvg_legend, svgcolors
from i3_tracker_server.tracker.models import Event, Group


def is_blacklist(event_json):
    return any([re.search(n, event_json['name']) for n in BLACKLIST_NAME]) or any([re.search(n, event_json['window_class']) for n in BLACKLIST_TYPE])


def is_recent(event, delta=OVERRIDE_TIME):
    diff = datetime.now() - event.datetime_point
    return diff.total_seconds() < delta


def is_duplicate(event, event_json):
    return event_json['name'] == event.name and event_json['type'] == event.window_class and is_recent(event, DUPLICATE_TIME)


def create_or_override(event_json):
    last_event = Event.objects.order_by('datetime_point').last()
    if last_event is not None:
        if is_duplicate(last_event, event_json):
            return
        if is_recent(last_event):
            last_event.name = event_json['name']
            last_event.window_class = event_json['window_class']
            last_event.save()
            return
    event = Event(name=event_json['name'], window_class=event_json['window_class'])
    event.datetime_point = datetime.now()
    event.save()


def register(request):
    event_json = json.loads(request.body)
    if event_json['type'] == 'window::focus' or event_json['type'] == 'window::title':
        if not is_blacklist(event_json):
            create_or_override(event_json)
            return HttpResponse('OK', content_type="text/plain")
        else:
            return timeout(request)
    return HttpResponse('OK', content_type="text/plain")


def breakpoint(time=datetime.now()):
    return Event(name='BREAKPOINT', window_class='INACTIVE', datetime_point=time)


def timeout(request):
    event = Event(name='TIMEOUT', window_class='INACTIVE', datetime_point=datetime.now())
    event.save()
    return HttpResponse('OK', content_type="text/plain")


def userlock(request):
    event = breakpoint()
    event.save()
    return HttpResponse('OK', content_type="text/plain")


def panel(request):
    today = datetime.now()
    return panel_day(request, today.year, today.month, today.day)


def chop_microseconds(delta):
    return delta - timedelta(microseconds=delta.microseconds)


def is_today(year, month, day):
    return date(year, month, day) == date.today()


def panel_day(request, year, month, day):
    year=int(year)
    month=int(month)
    day=int(day)
    events_set = Event.objects.filter(datetime_point__year=year,
                                      datetime_point__month=month,
                                      datetime_point__day=day).order_by('datetime_point')

    events = [event for event in events_set]

    group_time = defaultdict(timedelta)
    duration_event_list = []

    dayDuration = timedelta()

    if is_today(year, month, day):
        events.append(breakpoint())
        markNow = datetime.now()
    else:
        markNow = None
        next_date = date(year, month, day) + timedelta(days=1)
        next_datetime = datetime.combine(next_date, datetime.min.time())
        events.append(breakpoint(next_datetime))

    if len(events) > 1:
        for i,event in enumerate(events[0:len(events)-1]):
            event.duration = events[i+1].datetime_point - event.datetime_point

            # correct events followed by timeout
            if events[i+1].window_class == 'INACTIVE' and events[i+1].name == 'TIMEOUT':
                event.duration -= timedelta(minutes=15)

            # correct infinite event (assuming 2h and more to be 15minutes task)
            if event.duration.total_seconds() > 2*60*60:
                event.duration = timedelta(minutes=15)

            event.duration = chop_microseconds(event.duration)

            # add event to display list
            if event.window_class != 'INACTIVE':
                if event.duration > timedelta(seconds=10):
                    group_time[event.window_class] += event.duration
                    event.id_hash = hashlib.sha1(str(event.__hash__()).encode()).hexdigest()
                    event.end = event.datetime_point + event.duration
                    dayDuration += event.duration
                    duration_event_list.append(event)

    dayDuration = chop_microseconds(dayDuration)

    class_list = [k for k in group_time]

    svg_legend = printsvg_legend()
    svgs, colors = printsvg(duration_event_list, class_list, markNow)

    group_sorted = sorted([Group(group_time[k],k,colors[k]) for k in group_time], key=lambda g: g.time, reverse=True)

    for event in duration_event_list:
        event.datetime_point = event.datetime_point.strftime("%X")
        event.end = event.end.strftime("%X")
        event.color = colors[event.window_class]

    select = [''] + sorted([key for key in class_list])

    if duration_event_list:
        dayStart = duration_event_list[0].datetime_point
        dayEnd = duration_event_list[-1].end
    else:
        dayStart = "no data"
        dayEnd = "no data"

    return render(request, 'panel.html', {
        'year': year,
        'month': month,
        'day': day,
        'event_list': duration_event_list,
        'group_sorted': group_sorted,
        'svgs': svgs,
        'svg_legend': svg_legend,
        'dayStart': dayStart,
        'dayEnd': dayEnd,
        'dayDuration': dayDuration,
        'colors': svgcolors,
        'select': select
    })


