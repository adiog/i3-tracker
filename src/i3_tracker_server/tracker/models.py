from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=128)
    window_class = models.CharField(max_length=128)
    datetime_point = models.DateTimeField()


class Group(object):
    def __init__(self, time, name, color):
        self.time = time
        self.name = name
        self.color = color
