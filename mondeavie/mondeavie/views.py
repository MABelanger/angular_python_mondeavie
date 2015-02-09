# -*- coding: utf-8 -*-

import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def redirect_to_store(request, path):

    print path

    mstring = []
    for key in request.GET.iterkeys():  # "for key in request.GET" works too.
        # Add filtering logic here.
        valuelist = request.GET.getlist(key)
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])
    print '&'.join(mstring)

    response_data = 'document.location.href="https://mondeavie.liki.com/commande/%s?%s"'\
                            %(path, '&'.join(mstring))

    return HttpResponse(response_data)