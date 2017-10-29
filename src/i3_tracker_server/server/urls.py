"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import i3_tracker_server.tracker.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', i3_tracker_server.tracker.views.panel),
    url(r'^panel/$', i3_tracker_server.tracker.views.panel),
    url(r'^panel/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', i3_tracker_server.tracker.views.panel_day),
    url(r'^register/$', i3_tracker_server.tracker.views.register),
    url(r'^inactive/$', i3_tracker_server.tracker.views.inactive),
]
