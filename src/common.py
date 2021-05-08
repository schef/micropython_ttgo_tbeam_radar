from machine import Pin, SoftI2C, UART
from time import ticks_ms


def get_millis():
    return ticks_ms()


def millis_passed(timestamp):
    return get_millis() - timestamp


def dump_func(pexit=False, timing=False, showarg=False):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            enter_string = "%s enter" % (f.__name__)
            pexit_local = False
            if showarg:
                enter_string += ", args[%s%s]" % (args, kwargs)
            print(enter_string)
            if timing:
                pexit_local = True
                timestamp = get_millis()
            response = f(*args, **kwargs)
            exit_string = "%s exit" % (f.__name__)
            if timing:
                exit_string += ", time[%d]" % (millis_passed(timestamp))
            if pexit or pexit_local:
                print(exit_string)
            return response
        return wrapped
    return inner_decorator


def print_available_pins():
    print(dir(Pin.board))
    print(dir(Pin.cpu))


def create_led(pin):
    return Pin(pin, Pin.OUT)


def create_button(pin):
    return Pin(pin, Pin.IN, Pin.PULL_DOWN)


def create_uart(pin_tx, pin_rx, baud=9600, instance=1):
    return UART(instance, rx=pin_rx, tx=pin_tx, baudrate=baud, bits=8, parity=None, stop=1, rxbuf=2048, txbuf=256)


def create_i2c(pin_sda, pin_scl):
    return SoftI2C(scl=Pin(pin_scl), sda=Pin(pin_sda))