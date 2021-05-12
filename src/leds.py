import machine
from common import dump_func, get_millis, millis_passed
from peripherals import create_led

current_status = False
led_pin = None
timestamp = 0
sleep_timeout = 900


@dump_func()
def init():
    global led_pin
    led_pin = create_led(4)


def set(status):
    global current_status, timestamp
    current_status = status
    if (status):
        timestamp = get_millis()
        led_pin.on()
    else:
        led_pin.off()
        set_sleep_timeout()


def set_sleep_timeout(timeout=900):
    global sleep_timeout
    sleep_timeout = timeout


def is_on():
    return current_status


def loop():
    global timestamp
    if current_status:
        if led_pin.value() and millis_passed(timestamp) > 100:
            timestamp = get_millis()
            led_pin.off()
        elif not led_pin.value() and millis_passed(timestamp) >= sleep_timeout:
            timestamp = get_millis()
            led_pin.on()
    else:
        if led_pin.value():
            led_pin.off()
