from utime import sleep_ms
from struct import unpack
from common import create_uart
from oled import display_lines
from math import radians
import stations
from specific import *
import pwm

uart = create_uart(12, 34)

    
selected_coordinate = 0
test_coordinate = [
    GpsCoordinate(46.3880032, 16.4399232, 0, 9, "doma"),
    GpsCoordinate(46.3691968, 16.4137257, 0, 9, "strahoninec"),
    GpsCoordinate(46.3486437, 16.4094653, 0, 9, "poleve"),
    GpsCoordinate(46.3297037, 16.3973263, 0, 9, "kursanec")
]


def configure():
    print("GPS configure start")
    uart.write(bytes([0xB5, 0x62, 0x06, 0x04, 0x04, 0x00,
                      0xFF, 0xB9, 0x00, 0x00, 0xC6, 0x8B]))  # CFG-RST
    sleep_ms(1000)

    #print("Disable NMEA")
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x00,
                      0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x24]))  # GxGGA off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x01,
                      0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x2B]))  # GxGLL off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x02,
                      0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x32]))  # GxGSA off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x03,
                      0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0x39]))  # GxGSV off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x04,
                      0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x04, 0x40]))  # GxRMC off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x05,
                      0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x05, 0x47]))  # GxVTG off

    #print("Enable UBX")
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x07, 0x01, 0x13, 0x51]))  # NAV-PVT on
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00,
                      0x01, 0x02, 0x01, 0x0E, 0x47]))  # NAV-POSLLH on
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x03, 0x01, 0x0F, 0x49]))  # NAV-STATUS on
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x04, 0x01, 0x10, 0x4B]))  # NAV-DOP on
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x06, 0x01, 0x12, 0x4F]))  # NAV-SOL on
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x12, 0x01, 0x1E, 0x67]))  # NAV-VELNED on

    #print("Disable UBX")
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x07, 0x00, 0x12, 0x50]))  # NAV-PVT off
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x02, 0x00, 0x0D, 0x46]))  # NAV-POSLLH off
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x03, 0x00, 0x0E, 0x48]))  # NAV-STATUS off
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x04, 0x00, 0x0F, 0x4A]))  # NAV-DOP off
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x06, 0x00, 0x11, 0x4E]))  # NAV-SOL off
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x12, 0x00, 0x1D, 0x66]))  # NAV-VELNED off

    # print("Rate")
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0x64, 0x00, 0x01, 0x00, 0x01, 0x00, 0x7A, 0x12]))  # (10Hz)
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0x90, 0x01, 0x01, 0x00, 0x01, 0x00, 0xA7, 0x1F]))  # (2.5Hz)
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0xC8, 0x00, 0x01, 0x00, 0x01, 0x00, 0xDE, 0x6A]))  # (5Hz)
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0xE8, 0x03, 0x01, 0x00, 0x01, 0x00, 0x01, 0x39]))  # (1Hz)

    # Tests
    # uart.write(bytes([]))

    uart.read()
    sleep_ms(3000)  # dont remove this
    uart.read()
    print("GPS configure end")


def parse_binary_data(data):
    coordinate = None
    if data:
        print("".join(["%02X" % (d) for d in data]))
        if data[0] == 0xB5 and data[1] == 0x62 and len(data) == 36:
            # 0U4-iTOWmsGPS Millisecond Time of Week
            time = int(unpack("<L", data[6:10])[0] / 1000)

            # 4I41e-7londegLongitude8I
            lat = unpack("<l", data[10:14])[0] * 10 ** -7

            # 41e-7latdegLatitude12
            lon = unpack("<l", data[14:18])[0] * 10 ** -7

            # I4-heightmmHeight above Ellipsoid16
            height = unpack("<l", data[18:22])[0]
            # I4-hMSLmmHeight above mean sea level20

            hMSL = unpack("<l", data[22:26])[0]
            # U4-hAccmmHorizontal Accuracy Estimate24

            hAcc = unpack("<L", data[26:30])[0]
            # U4-vAccmmVertical Accuracy Estimate

            vAcc = unpack("<L", data[30:34])[0]
            # print(data.decode().strip())
            # print(time, lat, lon, height, hMSL, hAcc, vAcc)
            coordinate = GpsCoordinate(lat, lon, time, hAcc)
    return coordinate


def init():
    configure()


def loop():
    #gps_coordinate = parse_binary_data(uart.read())
    gps_coordinate = test_coordinate[selected_coordinate]
    if gps_coordinate:
        lines = []
        if (gps_coordinate.hacc <= 10):
            lines.append("STATUS: GOOD")
        elif (gps_coordinate.hacc <= 100):
            lines.append("STATUS: BAD")
        else:
            lines.append("STATUS: UGLY")
        lines.append("TIME: %d" % (gps_coordinate.time))
        lines.append("LAT: %f" % (gps_coordinate.lat))
        lines.append("LON: %f" % (gps_coordinate.lon))
        lines.append("HACC: %d" % (gps_coordinate.hacc))
        if (gps_coordinate.hacc < 30):
            nearest_station = stations.get_nearest_station(gps_coordinate)
            distance = stations.get_distance(gps_coordinate, nearest_station)
            lines.append("%.2fkm in %s" % (distance, nearest_station.name))
            if (distance < 0.2):
                if not pwm.is_beep():
                    pwm.set_beep(True)
            else:
                if pwm.is_beep():
                    pwm.set_beep(False)
        else:
            if pwm.is_beep():
                pwm.set_beep(False)
        display_lines(lines)
    else:
        if pwm.is_beep():
            pwm.set_beep(False)