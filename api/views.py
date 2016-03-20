import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.routing import *

def index(request):
    return render(request, 'api/api.html')

@csrf_exempt
def get_route_name(request, origin, destination):
    origin_id = get_system_id(origin)
    destination_id = get_system_id(destination)
    start = datetime.datetime.now()

    # Run algorithm
    # path = breadth_first_search(int(origin), int(destination), systems, max)
    path = dijkstra_search(int(origin_id), int(destination_id))

    # format path into deliminated string
    pathName = str(path).strip('[]').replace(', ', ';')
    jumps = len(path)
    end = datetime.datetime.now()
    return JSONResponse({'jumps': jumps, 'path': pathName, 'time': (end - start)})


@csrf_exempt
def get_route_id(request, origin, destination):
    start = datetime.datetime.now()

    # Run algorithm
    # path = breadth_first_search(int(origin), int(destination), systems, max)
    path = dijkstra_search(int(origin), int(destination))

    # format path into deliminated string
    pathName = str(path).strip('[]').replace(', ', ';')
    jumps = len(path)
    end = datetime.datetime.now()
    return JSONResponse({'jumps': jumps, 'path': pathName, 'time': (end - start)})


@csrf_exempt
def get_distance_id(request, origin, destination):
    distance = get_distance(origin, destination)
    return JSONResponse({'distance': distance})


@csrf_exempt
def get_distance_name(request, origin, destination):
    origin_id = get_system_id(origin)
    destination_id = get_system_id(destination)
    distance = get_distance(origin_id, destination_id)
    return JSONResponse({'distance': distance})


@csrf_exempt
def get_jump_range(request, origin, jump):
    origins = origin.split(",")
    jumps = jump.split(",")
    if len(origins) == len(jumps):
        systems = systems_in_range(list(map(int, origins)), list(map(int, jumps)))
        return JSONResponse({'systems': systems})
    return JSONResponse({'systems': []})





class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

