'''
urls.py
^^^^^^^
Register the application root URL and admin URL with django.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/http/urls/
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^app/', include('app.urls', namespace="app")),
    url(r'^admin/', include(admin.site.urls)),
)
