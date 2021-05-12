from math import radians
from math import sin, cos, sqrt, atan2, radians

TESTING = False
# approximate radius of earth in km
R = 6373.0


class Coordinate():
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.rlat = radians(lat)
        self.rlon = radians(lon)


class Station(Coordinate):
    def __init__(self, lat, lon, speed, name):
        super().__init__(lat, lon)
        self.name = name
        self.speed = speed


class Location(Coordinate):
    def __init__(self, lat, lon, time = 0, hacc = 10):
        super().__init__(lat, lon)
        self.time = time
        self.hacc = hacc
        self.speed = 0.0
        self.timestamp = 0


def get_distance(coordinate_from, coordinate_to):
    dlon = coordinate_from.rlon - coordinate_to.rlon
    dlat = coordinate_from.rlat - coordinate_to.rlat

    a = sin(dlat / 2)**2 + cos(coordinate_to.rlat) * \
        cos(coordinate_from.rlat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def get_nearest_station(coordinate_from, stations):
    nearest_station = None
    smallest_distance = 99999.0
    for station in stations:
        distance = get_distance(coordinate_from, station)
        if distance < smallest_distance:
            smallest_distance = distance
            nearest_station = station
    return nearest_station


def get_status(location):
    if (location.hacc <= 10):
        return "GOOD"
    elif (location.hacc <= 100):
        return "BAD"
    else:
        return "UGLY"
