# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers

import settings

import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin_activities/', include('admin_activities.urls')),
    url(r'^calendar_activities/', include('calendar_activities.urls')),
    url(r'^getpic/', include('getpic.urls')),
    url(r'^commande/(?P<path>.+)$', views.redirect_to_store),
]

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
            (r'^admin/', include(admin.site.urls)),
         )

urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':False}),
    )