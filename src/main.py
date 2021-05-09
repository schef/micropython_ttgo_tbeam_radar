import peripherals
import oled
import gps
import pwm
import stations
from specific import Location

selected_coordinate = 0
test_coordinate = [
    Location(46.3880032, 16.4399232),
    Location(46.3691968, 16.4137257),
    Location(46.3486437, 16.4094653),
    Location(46.3297037, 16.3973263)
]

def on_button_callback(state):
    print("button %s" % (("released", "pressed")[state]))
    if state:
        global selected_coordinate
        selected_coordinate += 1
        if selected_coordinate == len(test_coordinate):
            selected_coordinate = 0
        gps.set_location(test_coordinate[selected_coordinate])


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
