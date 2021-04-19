
from machine import Pin, SoftI2C, UART
from utime import sleep_ms
from time import ticks_ms
from struct import unpack
import ssd1306

LED_PIN = 27
BUTTON_PIN = 38


def get_millis():
    return ticks_ms()


def millis_passed(timestamp):
    return get_millis() - timestamp


def create_led(pin):
    return Pin(pin, Pin.OUT)


def create_button(pin):
    return Pin(pin, Pin.IN, Pin.PULL_UP)


def create_uart(pin_tx, pin_rx, baud=9600):
    return UART(1, rx=pin_rx, tx=pin_tx, baudrate=baud, bits=8, parity=None, stop=1, rxbuf=2048, txbuf=256)


def create_i2c(pin_sda, pin_scl):
    return SoftI2C(scl=Pin(pin_scl), sda=Pin(pin_sda))


led = create_led(LED_PIN)
button = create_button(BUTTON_PIN)
button_state = 1
uart = create_uart(12, 34)
i2c = create_i2c(21, 22)

oled_width = 128  # 16 chars
oled_height = 64  # 6 lines
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


def draw_string(string):
    oled.fill(0)
    line_count = 0
    line = ""
    for s in string:
        line += s
        if len(line) >= 16:
            oled.text(line, 0, line_count * 10)
            line = ""
            line_count += 1
    if len(line):
        oled.text(line, 0, line_count * 10)
    oled.show()


def draw_gps_data(gps_data):
    oled.fill(0)
    line_count = 0
    for line in gps_data:
        oled.text(str(line), 0, line_count * 10)
        line_count += 1
    oled.show()


def disable_gps_data():
    print("GPS configure start")
    uart.write(bytes([0xB5, 0x62, 0x06, 0x04, 0x04, 0x00, 0xFF, 0xB9, 0x00, 0x00, 0xC6, 0x8B]))  # CFG-RST
    sleep_ms(1000)

    #print("Disable NMEA")
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x24]))  # GxGGA off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x2B]))  # GxGLL off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x32]))  # GxGSA off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x03, 0x39]))  # GxGSV off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x04, 0x40]))  # GxRMC off
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x08, 0x00, 0xF0, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x05, 0x47]))  # GxVTG off

    #print("Enable UBX")
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x07, 0x01, 0x13, 0x51]))  # NAV-PVT on
    uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x02, 0x01, 0x0E, 0x47]))  # NAV-POSLLH on
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x03, 0x01, 0x0F, 0x49]))  # NAV-STATUS on
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x04, 0x01, 0x10, 0x4B]))  # NAV-DOP on
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x06, 0x01, 0x12, 0x4F]))  # NAV-SOL on
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x12, 0x01, 0x1E, 0x67]))  # NAV-VELNED on

    #print("Disable UBX")
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x07, 0x00, 0x12, 0x50]))  # NAV-PVT off
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x02, 0x00, 0x0D, 0x46]))  # NAV-POSLLH off
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x03, 0x00, 0x0E, 0x48]))  # NAV-STATUS off
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x04, 0x00, 0x0F, 0x4A]))  # NAV-DOP off
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x06, 0x00, 0x11, 0x4E]))  # NAV-SOL off
    #uart.write(bytes([0xB5, 0x62, 0x06, 0x01, 0x03, 0x00, 0x01, 0x12, 0x00, 0x1D, 0x66]))  # NAV-VELNED off

    # print("Rate")
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0x64, 0x00, 0x01, 0x00, 0x01, 0x00, 0x7A, 0x12]))  # (10Hz)
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0x90, 0x01, 0x01, 0x00, 0x01, 0x00, 0xA7, 0x1F]))  # (2.5Hz)
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0xC8, 0x00, 0x01, 0x00, 0x01, 0x00, 0xDE, 0x6A]))  # (5Hz)
    # uart.write(bytes([0xB5, 0x62, 0x06, 0x08, 0x06, 0x00, 0xE8, 0x03, 0x01, 0x00, 0x01, 0x00, 0x01, 0x39]))  # (1Hz)

    # Tests
    # uart.write(bytes([]))

    uart.read()
    sleep_ms(3000)
    uart.read()
    print("GPS configure end")


def on_button_callback(state):
    print("button %s" % (("released", "pressed")[state]))
    if state:
        disable_gps_data()


def check_button():
    global button_state
    state = button.value()
    if state != button_state:
        button_state = state
        on_button_callback(not button_state)


def parse_binary_gps_data(data):
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
            print(time, lat, lon, height, hMSL, hAcc, vAcc)
            return (time, lat, lon, hAcc)        
    return []

def display_boot():
    lines = []
    lines.append("BOOT")
    draw_gps_data(lines)

display_boot()
disable_gps_data()

while True:
    check_button()
    gps_data = parse_binary_gps_data(uart.read())
    if gps_data:
        lines = []
        if (gps_data[3] <= 10):
            lines.append("STATUS: GOOD")
        elif (gps_data[3] <= 100):
            lines.append("STATUS: BAD")
        else:
            lines.append("STATUS: UGLY")
        lines.append("")
        lines.append("LAT: %f" % (gps_data[1]))
        lines.append("LON: %f" % (gps_data[2]))
        lines.append("HACC: %d" % (gps_data[3]))
        draw_gps_data(lines)
