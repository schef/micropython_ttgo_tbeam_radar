from math import radians


class StationCoordinate():
    def __init__(self, lat, lon, name, speed):
        self.lat = lat
        self.lon = lon
        self.rlat = radians(lat)
        self.rlon = radians(lon)
        self.name = name
        self.speed = speed


class GpsCoordinate():
    def __init__(self, lat, lon, time, hacc, name = ""):
        self.lat = lat
        self.lon = lon
        self.rlat = radians(lat)
        self.rlon = radians(lon)
        self.time = time
        self.hacc = hacc
        self.name = name
