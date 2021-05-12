#!/usr/bin/env python3

import json
import requests
from math import sin, cos, sqrt, atan2, radians


URL = 'https://www.scdb.info/en/karte/'
PARAMS = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.scdb.info',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.scdb.info/en/karte/',
    'Accept-Language': 'en-GB,en;q=0.9,de;q=0.8,en-US;q=0.7',
    'Cookie': 'PHPSESSID=7d2283cf67dafa2b07829db6a33e6b3f; LAN=en',
}

R = 6373.0


def get_clean_name(name):
  name = name.replace("Č", "C")
  name = name.replace("Ć", "C")
  name = name.replace("Ž", "Z")
  name = name.replace("Š", "S")
  name = name.replace("Đ", "D")
  name = name.replace("č", "c")
  name = name.replace("ć", "c")
  name = name.replace("ž", "z")
  name = name.replace("š", "s")
  name = name.replace("đ", "d")
  return name.encode("ascii", errors="ignore").decode()

class Coordinate():
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.rlat = radians(lat)
        self.rlon = radians(lon)


class Station(Coordinate):
    def __init__(self, lat, lon, name, speed):
        super().__init__(lat, lon)
        self.name = name
        self.speed = speed

    def __str__(self):
        return "Station(%f, %f, %i, \"%s\")," % (self.lat, self.lon, self.speed, get_clean_name(self.name))


class Location(Coordinate):
    def __init__(self, lat, lon, time=0, hacc=10):
        super().__init__(lat, lon)
        self.time = time
        self.hacc = hacc
        self.speed = 0.0
        self.timestamp = 0


extra_stations = [
    Station(46.370007, 16.374832, "Nedelisce, Aqua", 50),
    Station(46.341629, 16.361911, "Puscine", 60),
    Station(46.348843, 16.411857, "Poleve", 50),
    Station(46.377726, 16.338927, "Gornji Hrascan", 50),
    Station(46.387215, 16.422808, "Cakovec, Konzum", 70),
    Station(46.373135, 16.452183, "Cakovec, Zaobilaznica", 70),
    Station(46.332015, 16.407159, "Kursanec, Skola", 50),
    Station(46.409904, 16.422495, "Senkovec", 50),
    Station(46.420979, 16.395676, "Brezje", 50),
    Station(46.506844, 16.432089, "Mursko Sredisce", 50),
    Station(46.380558, 16.542446, "Palovec", 50),
    Station(46.340054, 16.604033, "Prelog, Cakovecka", 50),
    Station(46.329298, 16.615371, "Prelog, Zrinskih", 50),
    Station(46.379714, 16.374166, "Nedelisce, Nazora", 50)
]


class WebStation(Coordinate):
    def __init__(self, dictionary):
        super().__init__(float(dictionary["lat"]), float(dictionary["lng"]))
        self.name = "%s, %s, %s, %s" % (dictionary["ort"], dictionary["strasse"], dictionary["plz"], dictionary["id"])
        self.speed = int(dictionary["vmax"])

    def __str__(self):
        return "Station(%f, %f, %i, \"%s\")," % (self.lat, self.lon, self.speed, get_clean_name(self.name))


def get_raw_data(lat1, lon1, lat2, lon2):
    if lat1 > lat2:
        latMin = lat2
        latMax = lat1
    else:
        latMin = lat1
        latMax = lat2
    if lon2 > lon1:
        lonMax = lon2
        lonMin = lon1
    else:
        lonMax = lon1
        lonMin = lon2
    return 'xhr=1&action=all&latMax=%f&lngMax=%f&latMin=%f&lngMin=%f' % (latMax, lonMax, latMin, lonMin)


def get_distance(coordinate_from, coordinate_to):
    dlon = coordinate_from.rlon - coordinate_to.rlon
    dlat = coordinate_from.rlat - coordinate_to.rlat
    a = sin(dlat / 2)**2 + cos(coordinate_to.rlat) * \
        cos(coordinate_from.rlat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


if __name__ == "__main__":
    raw_data = get_raw_data(46.4859993, 16.3086184, 46.1355817, 16.8162473)
    r = requests.post(URL, data=raw_data, headers=PARAMS)
    data = r.json()
    stations = []
    for i in data["result"]:
        stations.append(WebStation(i))

    print("Adding missing stations")
    for extra_station in extra_stations:
        minimal_distance = 999999.0
        for station in stations:
            distance = get_distance(station, extra_station)
            if distance < minimal_distance:
                minimal_distance = distance
        if minimal_distance > 0.3:
          print("    %s" % (extra_station.name))
        stations.append(extra_station)
    
    print("Print station list")
    for station in stations:
      print("    %s" % (station))
