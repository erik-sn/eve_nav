import datetime

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from api.routing import dijkstra_search
from api.routing import breadth_first_search
from api.routing import get_distance
from api.routing import get_system_id



def index(request):
    return render(request, 'api/api.html')


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


def get_distance_id(request, origin, destination):
    distance = get_distance(origin, destination)
    return JSONResponse({'distance': distance})


def get_distance_name(request, origin, destination):
    origin_id = get_system_id(origin)
    destination_id = get_system_id(destination)
    distance = get_distance(origin_id, destination_id)
    return JSONResponse({'distance': distance})


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

