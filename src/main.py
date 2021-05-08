import peripherals
import oled
import gps
import pwm


def on_button_callback(state):
    print("button %s" % (("released", "pressed")[state]))
    if state:
        gps.selected_coordinate += 1
        if gps.selected_coordinate == len(gps.test_coordinate):
            gps.selected_coordinate = 0
        print("selected %s" % (gps.test_coordinate[gps.selected_coordinate].name))


if __name__ == "__main__":
    peripherals.register_button_callback_function(on_button_callback)
    pwm.init()
    oled.init()
    gps.init()

    while True:
        peripherals.loop()
        gps.loop()
        pwm.loop()
