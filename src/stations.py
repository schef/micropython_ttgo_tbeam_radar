from specific import *
import pwm
import leds
import oled
from gps import get_location
from common import get_millis, millis_passed

beep_off_if_no_location_timestamp = 0

stations = [
    Station(45.417183, 15.606904, 70, "Cerovac Vukmanicki, D1 1186-1166, 47241, 144700"),
    Station(45.428204, 15.604838, 50, "Cerovac Vukmanicki, D6 51, 47241, 105784"),
    Station(45.459061, 16.371681, 50, "Sisak, D37, 44000, 134104"),
    Station(45.460556, 15.570008, 40, "Karlovac, Turanj, 47106, 126235"),
    Station(45.465965, 15.585986, 50, "Karlovac, Ulica Brace Gojak, 47000, 134133"),
    Station(45.485275, 16.780869, 50, "Kutina, D45, 44320, 134090"),
    Station(45.487125, 16.441463, 60, "Novo Selo Palanjecko, D36, 44202, 134102"),
    Station(45.510532, 16.787907, 50, "Kutinska Slatina, D45, 44320, 134073"),
    Station(45.522076, 16.690308, 70, "Gornja Gracenica, 3124, 44318, 134094"),
    Station(45.544685, 16.235092, 50, "Duzica, D30, 44272, 134105"),
    Station(45.551800, 16.988195, 50, "Hrastovac, D26, 43280, 134065"),
    Station(45.591160, 16.938618, 50, "Garesnica, D26, 43280, 134068"),
    Station(45.601143, 15.598508, 50, "Draganic, D1, 47201, 108281"),
    Station(45.625118, 15.603773, 40, "Ceglje, Ceglje, 10450, 101083"),
    Station(45.700073, 15.767168, 50, "Pavucnjak, Pavucnjak, 10450, 101084"),
    Station(45.722187, 16.050133, 0, "Velika Gorica, Zagrebacka Ulica, 10410, 155963"),
    Station(45.753944, 16.076435, 130, "Mala Kosnica, A3, 10410, 104687"),
    Station(45.754280, 16.623947, 60, "Cazma, D43, 43240, 134097"),
    Station(45.760178, 16.236916, 130, "Rugvica, A3, 10370, 133209"),
    Station(45.794060, 15.962664, 70, "Zagreb, Zagrebacka avenija, 10000, 101087"),
    Station(45.795300, 15.990710, 70, "Zagreb, Kruge, 10000, 154206"),
    Station(45.795471, 15.991341, 60, "Zagreb, Slavonska avenija, 10000, 101752"),
    Station(45.796242, 16.008673, 70, "Zagreb, Slavonska Avenija, 10000, 25776"),
    Station(45.796806, 15.998549, 60, "Zagreb, Avenija Marina Drzica, 10000, 101088"),
    Station(45.805443, 15.983846, 0, "Zagreb, Draskoviceva ulica, 10000, 153924"),
    Station(45.805492, 15.984318, 0, "Zagreb, Draskoviceva ulica, 10000, 153923"),
    Station(45.807446, 15.967205, 40, "Zagreb, Rooseveltov trg, 10000, 118255"),
    Station(45.807777, 15.974801, 50, "Zagreb, Preradoviceva ulica, 10000, 118256"),
    Station(45.808929, 15.968900, 50, "Zagreb, Trg Republike Hrvatske, 10000, 105823"),
    Station(45.810429, 15.966402, 0, "Zagreb, prilaz Gjure Dezelica, 10000, 104693"),
    Station(45.811543, 15.913096, 60, "Zagreb, Ilica 446, 10000, 144726"),
    Station(45.811752, 15.941805, 50, "Zagreb, prilaz baruna Filipovica, 10000, 105822"),
    Station(45.813908, 15.870767, 60, "Zagreb, Aleja Bologne, 10000, 101086"),
    Station(45.815456, 15.841931, 60, "Zagreb, Aleja Bologne, 10000, 105802"),
    Station(45.828506, 16.071411, 50, "Zagreb, Druge Poljanice, 10000, 101089"),
    Station(45.835842, 16.176283, 50, "Sesvete, Budenecka, 10361, 145893"),
    Station(45.844357, 15.815011, 60, "Zapresic, Ulica Marsala Tita, 10290, 105781"),
    Station(45.847794, 15.833766, 50, "Ivanec Bistranski, Stubicka ulica, 10290, 105778"),
    Station(45.850056, 15.834281, 50, "Ivanec Bistranski, Stubicka ulica, 10290, 118257"),
    Station(45.852859, 16.930811, 60, "Patkovac, Patkovac, 43000, 136773"),
    Station(45.855103, 16.927656, 60, "Patkovac, Patkovac, 43000, 136772"),
    Station(45.867447, 15.802278, 50, "Zapresic, ulica bana Josipa Jelacica, 10290, 105782"),
    Station(45.869892, 15.789914, 50, "Zapresic, Ulica Mirka Ozegovica, 10290, 105780"),
    Station(45.870281, 16.901300, 70, "Prespa, D28, 43000, 134069"),
    Station(45.872025, 16.161564, 50, "Zerjavinec, Omladinska ulica, 10360, 101090"),
    Station(45.872276, 15.794520, 50, "Zapresic, Ulica Dragutina Tadijanovica, 10290, 105787"),
    Station(45.874027, 16.814806, 70, "Bjelovar, D43, 43000, 134071"),
    Station(45.887051, 16.862711, 50, "Novoseljani, Slavonska cesta, 43000, 133187"),
    Station(45.893471, 15.585706, 130, "Brezice, A2, 8250, 18974"),
    Station(45.905331, 16.163479, 80, "Adamovec, Ulica Dragutina Domjanica, 10363, 133266"),
    Station(45.933758, 15.819754, 60, "Jakovlje, D1 2, 10297, 145894"),
    Station(45.934757, 16.781414, 50, "Predavac, Ulica Stjepana Radica, 43211, 126990"),
    Station(45.935905, 16.778387, 50, "Predavac, Ulica Stjepana Radica, 43211, 126989"),
    Station(45.940334, 16.752008, 70, "Zabjak, D28, 43212, 134091"),
    Station(45.944405, 16.732416, 50, "Rovisce, Bjelovarska ulica, 43212, 133264"),
    Station(45.949604, 16.675217, 70, "Kendelovec, D28, 48213, 134095"),
    Station(45.981277, 15.961692, 40, "Donja Stubica, Toplicka cesta, 49240, 134115"),
    Station(45.992451, 15.844545, 50, "Veliko Trgovisce, Ulica Stjepana Radica, 49214, 134126"),
    Station(45.992489, 15.915045, 50, "Oroslavje, D307, 49243, 134117"),
    Station(46.005264, 16.550905, 50, "Krizevci, Bjelovarska ulica, 48260, 145892"),
    Station(46.005268, 16.552279, 50, "Krizevci, Bjelovarska ulica, 48260, 145891"),
    Station(46.015690, 16.952150, 50, "Hampovica, D43, 48350, 134066"),
    Station(46.022442, 15.897406, 50, "Zabok, 2195, 49210, 134120"),
    Station(46.030239, 16.594103, 60, "Majurec, D41, 48260, 134100"),
    Station(46.039680, 16.534525, 50, "Grad Krizevci, Kalnicka, 48260, 153925"),
    Station(46.044937, 16.004704, 50, "Bedekovcina, Ulica Matije Gupca, 49221, 133268"),
    Station(46.050365, 16.117228, 50, "Veleskovec, Veleskovec, 49247, 151804"),
    Station(46.081608, 16.079988, 50, "Zlatar, D29, 49250, 134110"),
    Station(46.087715, 16.946867, 60, "Novigrad Podravski, D2, 48325, 134067"),
    Station(46.120628, 16.879156, 60, "Glogovac, D2, 48324, 134070"),
    Station(46.136345, 16.782339, 70, "Reka, D41, 48305, 134074"),
    Station(46.152489, 15.878474, 50, "Mihaljekov Jarek, Ulica Mihaljekov jarek, 49000, 134123"),
    Station(46.167652, 15.862772, 40, "Krapina, Celjska cesta, 49000, 134125"),
    Station(46.176033, 16.803446, 60, "Koprivnica, D2, 48000, 134072"),
    Station(46.244896, 16.354408, 70, "Tomasevec Biskupecki, D3 Zagrebacka ulica, 42204, 116656"),
    Station(46.249599, 16.118114, 60, "Horvatsko, Horvatsko 36, 42244, 151795"),
    Station(46.267334, 16.346016, 80, "Warasdin, D2, 42204, 151830"),
    Station(46.272366, 16.362000, 90, "Varazdin, D3, 42000, 105816"),
    Station(46.280685, 16.350180, 50, "Varazdin, Zagrebacka ulica, 42000, 105815"),
    Station(46.281631, 15.424274, 100, "Celje, A1, 3000, 16266"),
    Station(46.282784, 16.217197, 50, "Jurketinec, Jurketinec, 42243, 150492"),
    Station(46.285980, 16.243996, 60, "Vidovec, Ulica Stjepana Radica, 42205, 144049"),
    Station(46.285980, 16.270180, 60, "Cargovec, Varazdinska ulica, 42205, 144048"),
    Station(46.296268, 16.177984, 50, "Opcina Marusevec, 2029, 42243, 153927"),
    Station(46.298538, 16.315510, 50, "Varazdin, Ulica Brace Radic, 42000, 105814"),
    Station(46.299252, 16.400129, 70, "Trnovec Bartolovecki, Ludbreska ulica, 42202, 105818"),
    Station(46.314625, 16.347761, 50, "Varazdin, Koprivnicka ulica, 42000, 133208"),
    Station(46.314899, 16.351303, 50, "Warasdin, Medimurska ulica, 42 00, 145901"),
    Station(46.323444, 16.297770, 60, "Hrascica, Ulica kralja Tomislava, 42000, 105813"),
    Station(46.329296, 16.615372, 50, "Prelog, Ulica Zrinskih, 40323, 155961"),
    Station(46.335144, 16.263157, 50, "Opcina Sracinec, Varazdinska ulica, 42209, 151831"),
    Station(46.340054, 16.604033, 50, "Prelog, D20, 40323, 134099"),
    Station(46.341629, 16.361912, 50, "Puscine, Cakovecka ulica 97, 40305, 155949"),
    Station(46.348843, 16.411858, 50, "Strahoninec, Poleve, 40000, 155994"),
    Station(46.370007, 16.374832, 50, "Nedelisce, Varazdinska ulica, 40305, 133205"),
    Station(46.373135, 16.452183, 80, "Cakovec, D3, 40000, 133201"),
    Station(46.377728, 16.338926, 50, "Opcina Nedelisce, Cakovecka ulica, 40 30, 155962"),
    Station(46.380558, 16.542446, 50, "Mala Subotica, D3, 40321, 134101"),
    Station(46.387215, 16.422808, 50, "Cakovec, Ulica Zrinsko Frankopanska, 40000, 134103"),
    Station(46.396564, 15.600115, 130, "Spodnja Nova Vas, A1, 2310, 136746"),
    Station(46.409904, 16.422495, 50, "Senkovec, Ulica Marsala Tita, 40000, 133203"),
    Station(46.420979, 16.395676, 60, "Brezje, Brezje, 40311, 133204"),
    Station(46.428223, 15.634000, 130, "Slovenska Bistrica, A1, 2310, 17564"),
    Station(46.441971, 16.811235, 130, "Becsehely, M7, 8866, 109390"),
    Station(46.461823, 15.656901, 130, "Maribor, A1, 2000, 18975"),
    Station(46.506844, 16.432089, 50, "Mursko Sredisce, Ulica Josipa Broza Tita, 40315, 133202"),
    Station(46.510990, 16.552956, 110, "Tornyiszentmikls, M70, 8877, 114084"),
    Station(46.545547, 15.685744, 50, "Zrkovci, Zrkovci, 2000, 84130"),
    Station(46.545681, 15.684872, 50, "Zrkovci, Zrkovci, 2000, 84129"),
    Station(46.549191, 16.321749, 70, "Crensovci, 3, 9232, 50719"),
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
        timestamp = get_millis()
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
                if (distance <= 1.0 and not leds.is_on()):
                    leds.set(True)
                if (distance > 1.0 and leds.is_on()):
                    leds.set(False)
                if (distance <= 0.3 and not pwm.is_beep()):
                    pwm.set_beep(True)
                    leds.set_sleep_timeout(400)
                if (distance > 0.3 and pwm.is_beep()):
                    pwm.set_beep(False)
                    leds.set_sleep_timeout()
            else:
                print("ERROR: no nearest station?")
            print("duration %d" % (millis_passed(timestamp)))
        else:
            if pwm.is_beep():
                pwm.set_beep(False)
            if leds.is_on():
                leds.set(False)
        oled.display_lines(lines)
        
    if beep_off_if_no_location_timestamp != 0 and millis_passed(beep_off_if_no_location_timestamp) > 10000:
        beep_off_if_no_location_timestamp = 0
        print("No location in 10 seconds, turning off")
        if pwm.is_beep():
            pwm.set_beep(False)
        if leds.is_on():
            leds.set(False)
