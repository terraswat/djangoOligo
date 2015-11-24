"""
urls.py
^^^^^^^^
Register the application URLs with django.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/http/urls/
"""
from django.conf.urls import patterns, url

from django.conf import settings # extra?

from . import views

urlpatterns = patterns('',

    # /app/
    # initial page
    url(r'^$', views.index, name='index'),

    # /app/init/
	# initialize the context
    # returns:
        # total number of oligo rows
        # population totals
        # list of array names
    url(r'^init/$', views.init, name='init'),

    # /app/oligos/
    # returns the filtered oligo list
    url(r'^oligos/$', views.oligos, name='oligos'),

    # /app/populations/
    # returns the oligo's population counts
    url(r'^populations/$', views.populations, name='populations'),

    # /app/comments/
    # returns the oligo's comments
    url(r'^comments/$', views.comments, name='comments'),

    # /app/addComment/
    # adds a comment
    url(r'^addComment/$', views.addComment, name='addComment'),

    # /app/help/
    # help page
    url(r'^help/$', views.help, name='help'),

    # /app/docs/
    # docs page
    url(r'^docs/$', views.help, name='docs'),
)
