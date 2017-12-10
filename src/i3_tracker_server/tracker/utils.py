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


def chop_microseconds(delta):
    return delta - timedelta(microseconds=delta.microseconds)


def sanitize_year_month_day(year, month, day):
    return int(year), int(month), int(day)


def is_today(year, month, day):
    return date(year, month, day) == date.today()

