from math import sin, cos, sqrt, atan2, radians
from specific import *

# approximate radius of earth in km
R = 6373.0



stations = [
    StationCoordinate(46.370007, 16.374832, "Nedelisce, Varazdinska ulica", 50),
    StationCoordinate(46.341629, 16.361911, "Puscine, Cakovecka ulica", 60),
    StationCoordinate(46.348843, 16.411857, "Strahoninec, Poleve", 50)
]

def get_distance(coordinate_from, coordinate_to):
    dlon = coordinate_from.rlon - coordinate_to.rlon
    dlat = coordinate_from.rlat - coordinate_to.rlat

    a = sin(dlat / 2)**2 + cos(coordinate_to.rlat) * \
        cos(coordinate_from.rlat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def get_nearest_station(coordinate_from):
    nearest_station = None
    smallest_distance = 1000.0
    for station in stations:
       distance = get_distance(coordinate_from, station) 
       if distance < smallest_distance:
           smallest_distance = distance
           nearest_station = station
    return nearest_station