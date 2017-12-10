import json
from django.http import HttpResponse, JsonResponse
from django.utils.datetime_safe import datetime

from i3_tracker_server.tracker.models import Task, TaskTimeRange
from i3_tracker_server.tracker.utils import sanitize_year_month_day


def create_task(request):
    task_json = json.loads(request.body)

    if 'pk' in task_json:
        pk = task_json['pk']
        task = Task.objects.get(pk=pk)

    if 'start' not in task_json:
        task_json['start'] = datetime.now()

    if 'stop' not in task_json:
        task_json['stop'] = datetime.now()

    if 'duration' not in task_json:
        task_json['duration'] = 0

    task = Task(name=task_json['name'],
                datetime_start=task_json['start'],
                datetime_stop=task_json['stop'],
                duration=task_json['duration'])
    task.save()

    return JsonResponse({'pk': task.pk})

#def datetime_to_milliseconds(some_datetime_object):
#    timetuple = some_datetime_object.timetuple()
#    timestamp = time.mktime(timetuple)
#    return timestamp * 1000.0

class ConvertDate(object):
    @classmethod
    def js_to_python(cls, jsdatetime):
        return datetime.fromtimestamp(int(jsdatetime)/1000)

    @classmethod
    def python_to_js(cls, pydatetime):
        return pydatetime

    @classmethod
    def js_duration(cls, start, stop):
        return (int(stop) - int(start)) / 1000

def create_range(request):
    log_json = json.loads(request.body)

    task = Task.objects.get(pk=log_json['pk'])
    task.datetime_stop = ConvertDate.js_to_python(log_json['stop'])
    task.duration += ConvertDate.js_duration(log_json['start'], log_json['stop'])
    task.save()

    range = TaskTimeRange(task=task,
                          datetime_start=ConvertDate.js_to_python(log_json['start']),
                          datetime_stop=ConvertDate.js_to_python(log_json['stop']))
    range.save()

    return JsonResponse({'pk': log_json['pk']})


def retrieve(request):
    today = datetime.now()
    return retrieve_day(request, today.year, today.month, today.day)


def do_retrieve_day(year, month, day):
    return Task.objects.filter(datetime_start__year=year,
                               datetime_start__month=month,
                               datetime_start__day=day).order_by('datetime_start')


def retrieve_day(request, year, month, day):
    year, month, day = sanitize_year_month_day(year, month, day)
    tasks = do_retrieve_day(year, month, day)
    return JsonResponse({'tasks': [{'name': task.name, 'start': task.datetime_start, 'stop': task.datetime_stop} for task in tasks]})


def delete(request):
    task_json = json.loads(request.body)

    tasks = Task.objects.filter(datetime_start=task_json['datetime_start'], name=task_json['name'])

    for task in tasks:
        task.delete()

    return JsonResponse('OK')
