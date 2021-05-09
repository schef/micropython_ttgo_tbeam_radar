import peripherals
import oled
import gps
import pwm
import stations


def on_button_callback(state):
    print("button %s" % (("released", "pressed")[state]))


if __name__ == "__main__":
    peripherals.register_button_callback_function(on_button_callback)
    pwm.init()
    oled.init()
    gps.init()

    while True:
        peripherals.loop()
        gps.loop()
        pwm.loop()
        stations.loop()
