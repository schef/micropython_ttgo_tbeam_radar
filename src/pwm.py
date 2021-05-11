import machine
from utime import sleep_ms
from common import dump_func, get_millis, millis_passed
from specific import TESTING

current_status = False
pwm_pin = None
timestamp = 0
FREQ = 800
DUTY = 512
#DUTY = 2


@dump_func()
def init():
    global pwm_pin
    pwm_pin = machine.PWM(machine.Pin(2))
    pwm_pin.freq(FREQ)
    pwm_pin.duty(0)


def set_beep(status):
    global current_status, timestamp
    current_status = status
    if (status):
        timestamp = get_millis()
        pwm_pin.duty(DUTY)
    else:
        pwm_pin.duty(0)
        
def is_beep():
    return current_status


def loop():
    global timestamp
    if current_status:
        if pwm_pin.duty() and millis_passed(timestamp) > 100:
            timestamp = get_millis()
            pwm_pin.duty(0)
        elif not pwm_pin.duty() and millis_passed(timestamp) >= 900:
            timestamp = get_millis()
            pwm_pin.duty(DUTY)
    else:
        if pwm_pin.duty():
            pwm_pin.duty(0)
