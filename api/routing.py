from queue import Queue
import re
import threading
import time

import heapq
import sqlite3
from django.db import connection
import math

lock = threading.Lock()

def get_system_id(system_name):
    conn = get_dd_connection()
    c = conn.cursor()

    for row in c.execute('SELECT `solarSystemID` FROM `mapSolarSystems` WHERE `solarSystemName` = ? COLLATE NOCASE', (system_name,)):
        system_id = row[0]
    close_connection(c, conn)
    return system_id

def get_distance(origin, destination):
    system1 = find_system_info(origin)
    system2 = find_system_info(destination)
    distance = math.sqrt((system1[2] - system2[2])**2 + (system1[3] - system2[3])**2 + (system1[4] - system2[4])**2)/9.461e+15
    print(distance)
    return distance


def find_system_info(system_id):
    conn = get_dd_connection()
    c = conn.cursor()

    for row in c.execute('SELECT `solarSystemID`, `solarSystemName`, `x`, `y`, `z` '
                         'FROM `mapSolarSystems` '
                         'WHERE `solarSystemID`=? COLLATE NOCASE', (system_id,)):
        system_info = row
    close_connection(c, conn)
    return system_info


def dijkstra_search(origin, destination):
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
    return get_path(origin, destination, source, [])


def breadth_first_search(origin, destination, systems):
    nodes = Queue()
    nodes.put(origin)
    source = {}
    source[origin] = None

    while not nodes.empty():
        current = nodes.get()
        if current == destination:
            break
        for neighbor in find_neighbors(current, systems):
            if neighbor not in source:
                source.put(neighbor)
                nodes[neighbor] = current
    return get_path(origin, destination, source, [])


def find_neighbors(origin, systems):
    neighbors = []
    for row in systems:
        if int(origin) == row[0]:
            neighbors.append(row[1])
    return neighbors


def get_path(origin, destination, jumps, path):
    if origin == destination:
        path.append(origin)
        path.reverse()
        return path

    path.append(destination)
    return get_path(origin, jumps[destination], jumps, path)


def find_systems():
    conn = get_dd_connection()
    c = conn.cursor()

    systems = []
    for row in c.execute('SELECT `fromSolarSystemID`, `toSolarSystemID` FROM `mapSolarSystemJumps`'):
        systems.append(row)
    close_connection(c, conn)
    return systems


def find_kspace_systems():
    conn = get_dd_connection()
    c = conn.cursor()
    systems = []
    query = 'SELECT solarSystemID, solarSystemName FROM mapSolarSystems ORDER BY solarSystemID ASC'
    for row in c.execute(query):
        system_name = str(row[1])
        if re.match('[J][0-9]{6}', system_name):
            print('Ignoring %s' % system_name)
        else:
            print('Adding %s' % system_name)
            systems.append(int(row[0]))

    close_connection(c, conn)
    return systems



def get_dd_connection():
    conn = sqlite3.connect('universeDataDx.db')
    return conn


def get_pg_connection():
    return connection.cursor().connection


def close_connection(cursor, connection):
    cursor.close()
    del cursor
    connection.close()


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]