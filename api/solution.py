import threading
from queue import Queue
from api.routing import *

lock = threading.Lock()

def dijkstra_search_multi(origin, destination):
    # retrieve gate map for eve universe
    systems = find_systems()
    # initialize containers and starting node
    nodes = PriorityQueue()
    nodes.put(origin, 0)
    source = {}
    weights = {}
    source[origin] = None
    weights[origin] = 0

    # iterate until there are no more neighbors to explore
    while not nodes.empty():
        current = nodes.get()
        # if we have a solution, break out of the loop
        if current == destination:
            break

        # find all neighbors of the node and see if they already exist or a shorter path was found
        for neighbor in find_neighbors(current, systems):
            cost = weights[current] + 1
            if neighbor not in weights or cost < weights[neighbor]:
                weights[neighbor] = cost
                priority = cost
                nodes.put(neighbor, priority)
                source[neighbor] = current
    # generate a path from the source map
    path = get_path(origin, destination, source, [])
    pathName = str(path).strip('[]').replace(', ', ';')
    jumps = len(path)
    with lock:
        print(threading.current_thread().name, 'Jumps: %s  Path: %s' % (jumps, pathName))

def worker():
    while True:
        route = routes.get()
        dijkstra_search_multi(route[0], route[1])
        routes.task_done()

routes = Queue()
systems = find_kspace_systems()
iterations = 0
# for origin in systems:
origin = systems[0]
systems.remove(origin)
for system in systems:
    iterations += 1
    route = [origin, system]
    routes.put(route)

for i in range(10):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
