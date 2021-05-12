from specific import *
import pwm
import oled
from gps import get_location
from common import get_millis, millis_passed

beep_off_if_no_location_timestamp = 0

stations = [
    Station(46.136345, 16.782339, 70, "Reka, D41, 48305, 134074"),
    Station(46.176033, 16.803446, 60, "Koprivnica, D2, 48000, 134072"),
    Station(46.244896, 16.354408, 70, "Tomasevec Biskupecki, D3 Zagrebacka ulica, 42204, 116656"),
    Station(46.267334, 16.346016, 80, "Warasdin, D2, 42204, 151830"),
    Station(46.272366, 16.362000, 90, "Varazdin, D3, 42000, 105816"),
    Station(46.280685, 16.350180, 50, "Varazdin, Zagrebacka ulica, 42000, 105815"),
    Station(46.298538, 16.315510, 50, "Varazdin, Ulica Brace Radic, 42000, 105814"),
    Station(46.299252, 16.400129, 70, "Trnovec Bartolovecki, Ludbreska ulica, 42202, 105818"),
    Station(46.314625, 16.347761, 50, "Varazdin, Koprivnicka ulica, 42000, 133208"),
    Station(46.314899, 16.351303, 50, "Warasdin, Medimurska ulica, 42 00, 145901"),
    Station(46.329296, 16.615372, 50, "Prelog, Ulica Zrinskih, 40323, 155961"),
    Station(46.340054, 16.604033, 50, "Prelog, D20, 40323, 134099"),
    Station(46.341629, 16.361912, 50, "Puscine, Cakovecka ulica 97, 40305, 155949"),
    Station(46.348843, 16.411858, 50, "Strahoninec, Poleve, 40000, 155994"),
    Station(46.370007, 16.374832, 50, "Nedelisce, Varazdinska ulica, 40305, 133205"),
    Station(46.373135, 16.452183, 80, "Cakovec, D3, 40000, 133201"),
    Station(46.377728, 16.338926, 50, "Opcina Nedelisce, Cakovecka ulica, 40 30, 155962"),
    Station(46.380558, 16.542446, 50, "Mala Subotica, D3, 40321, 134101"),
    Station(46.387215, 16.422808, 50, "Cakovec, Ulica Zrinsko Frankopanska, 40000, 134103"),
    Station(46.409904, 16.422495, 50, "Senkovec, Ulica Marsala Tita, 40000, 133203"),
    Station(46.420979, 16.395676, 60, "Brezje, Brezje, 40311, 133204"),
    Station(46.441971, 16.811235, 130, "Becsehely, M7, 8866, 109390"),
    Station(46.370007, 16.374832, 50, "Nedelisce, Aqua"),
    Station(46.341629, 16.361911, 60, "Puscine"),
    Station(46.348843, 16.411857, 50, "Poleve"),
    Station(46.377726, 16.338927, 50, "Gornji Hrascan"),
    Station(46.387215, 16.422808, 70, "Cakovec, Konzum"),
    Station(46.373135, 16.452183, 70, "Cakovec, Zaobilaznica"),
    Station(46.332015, 16.407159, 50, "Kursanec, Skola"),
    Station(46.409904, 16.422495, 50, "Senkovec"),
    Station(46.420979, 16.395676, 50, "Brezje"),
    Station(46.506844, 16.432089, 50, "Mursko Sredisce"),
    Station(46.380558, 16.542446, 50, "Palovec"),
    Station(46.340054, 16.604033, 50, "Prelog, Cakovecka"),
    Station(46.329298, 16.615371, 50, "Prelog, Zrinskih"),
    Station(46.379714, 16.374166, 50, "Nedelisce, Nazora")
]

def loop():
    global beep_off_if_no_location_timestamp
    location = get_location()
    if location:
        lines = []
        lines.append("%s:%d" % (get_status(location), location.hacc))
        lines.append("TIME: %d" % (location.time))
        lines.append("LAT: %f" % (location.lat))
        lines.append("LON: %f" % (location.lon))
        if (location.hacc <= 100):
            beep_off_if_no_location_timestamp = get_millis()
            nearest_station = get_nearest_station(location, stations)
            if nearest_station:
                distance = get_distance(location, nearest_station)
                lines.append("%.1fkm in %s" % (distance, nearest_station.name))
                lines.append("%.1fkm/h" % (location.speed))
                if (distance <= 0.3):
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
        
    if beep_off_if_no_location_timestamp != 0 and millis_passed(beep_off_if_no_location_timestamp) > 10000:
        beep_off_if_no_location_timestamp = 0
        print("No location in 10 seconds, turning off")
        if pwm.is_beep():
            pwm.set_beep(False)
