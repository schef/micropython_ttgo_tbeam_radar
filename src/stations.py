from specific import *
import pwm
import oled
from gps import get_location
from common import get_millis, millis_passed

last_location_timestamp = 0

stations = [
    Station(46.370007, 16.374832, "Nedelisce, Var.", 50),
    Station(46.341629, 16.361911, "Puscine", 60),
    Station(46.348843, 16.411857, "Poleve", 50)
]

def loop():
    location = get_location()
    if location:
        last_location_timestamp = get_millis()
        lines = []
        lines.append("%s:%d" % (get_status(location), location.hacc))
        lines.append("TIME: %d" % (location.time))
        lines.append("LAT: %f" % (location.lat))
        lines.append("LON: %f" % (location.lon))
        if (get_status(location) in [LocationStatus.BAD, LocationStatus.GOOD]):
            nearest_station = get_nearest_station(location, stations)
            distance = get_distance(location, nearest_station)
            lines.append("%.1fkm in %s" % (distance, nearest_station.name))
            lines.append("%.1fkm/h" % (location.speed))
            if (distance < 0.2):
                if not pwm.is_beep():
                    pwm.set_beep(True)
            else:
                if pwm.is_beep():
                    pwm.set_beep(False)
        else:
            if pwm.is_beep():
                pwm.set_beep(False)
        oled.display_lines(lines)
    else:
        if millis_passed(last_location_timestamp) > 3000:
            if pwm.is_beep():
                pwm.set_beep(False)