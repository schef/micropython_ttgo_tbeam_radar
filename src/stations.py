from specific import *
import pwm
import oled
from gps import get_location
from common import get_millis, millis_passed

beep_off_if_no_location_timestamp = 0

stations = [
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

def loop():
    global beep_off_if_no_location_timestamp
    location = get_location()
    if location:
        beep_off_if_no_location_timestamp = get_millis()
        lines = []
        lines.append("%s:%d" % (get_status(location), location.hacc))
        lines.append("TIME: %d" % (location.time))
        lines.append("LAT: %f" % (location.lat))
        lines.append("LON: %f" % (location.lon))
        if (location.hacc <= 100):
            nearest_station = get_nearest_station(location, stations)
            if nearest_station:
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
                print("ERROR: no nearest station?")
        else:
            if pwm.is_beep():
                pwm.set_beep(False)
        oled.display_lines(lines)
        
    if millis_passed(beep_off_if_no_location_timestamp) > 3000:
        print("No location in 3 seconds, turning off")
        if pwm.is_beep():
            pwm.set_beep(False)