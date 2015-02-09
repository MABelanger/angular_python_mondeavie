from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    #url(r'^(?P<path_relative>.+)', views.get_resize_image),
    url(r'^(?P<path_relative>.+)_(?P<width>\d{1,4})(?P<extention>[.]\w{3,4})$', views.get_resize_image),
    
)