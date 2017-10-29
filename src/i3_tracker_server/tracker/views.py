import datetime
import hashlib
import json
from collections import defaultdict
from django.shortcuts import render
from django.http import HttpResponse
from i3_tracker_server.tracker.svg import printsvg
from tracker.models import Event, Group


def register(request):
    print(request.body)
    event_json = json.loads(request.body)
    if event_json['type'] == 'window::focus':
        event = Event(name=event_json['name'], window_class=event_json['window_class'])
        event.datetime_point = datetime.datetime.now()
        event.save()
    return HttpResponse('OK', content_type="text/plain")


def inactive(request):
    print(request.body)
    event_json = json.loads(request.body)
    if event_json['type'] == 'window::focus':
        event = Event(name=event_json['name'], window_class=event_json['window_class'])
        event.datetime_point = datetime.datetime.now()
        event.save()
    return HttpResponse('OK', content_type="text/plain")


def panel(request):
    today = datetime.datetime.now()
    return panel_day(request, today.year, today.month, today.day)


def panel_day(request, year, month, day):
    events = Event.objects.filter(datetime_point__year=year,
                                  datetime_point__month=month,
                                  datetime_point__day=day)
    event_list = sorted(events, key=lambda event: event.datetime_point)
    group_time = defaultdict(datetime.timedelta)
    duration_event_list = []
    for i,event in enumerate(event_list[0:len(events)-1]):
        event.duration = events[i+1].datetime_point - event.datetime_point
        group_time[event.window_class] += event.duration
        event.id_hash = hashlib.sha1(str(event.__hash__()).encode()).hexdigest()
        duration_event_list.append(event)

    class_list = [k for k in group_time]

    svg, colors = printsvg(duration_event_list, class_list)

    group_sorted = sorted([Group(group_time[k],k,colors[k]) for k in group_time], key=lambda g: g.time, reverse=True)

    return render(request, 'static/index.html', {
        'event_list': duration_event_list,
        'group_sorted': group_sorted,
        'svg': svg
    })


