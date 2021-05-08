from common import dump_func, create_led, create_button, get_millis, millis_passed

LED_PINS = [27]
BUTTON_PIN = 38

leds = []
current_led = 0
button_callback_function = None

for pin in LED_PINS:
    leds.append(create_led(pin))

button = create_button(BUTTON_PIN)
button_state = 0
button_timestamp = 0


@dump_func()
def toggle_leds():
    global current_led
    leds[current_led].value(not leds[current_led].value())
    current_led += 1
    if current_led >= len(leds):
        current_led = 0


@dump_func(showarg=True)
def on_button_callback(state):
    if button_callback_function:
        button_callback_function(state)
    if state:
        toggle_leds()


@dump_func()
def register_button_callback_function(callback_function):
    global button_callback_function
    button_callback_function = callback_function


def check_button():
    global button_timestamp
    if millis_passed(button_timestamp) < 50:
        return
    button_timestamp = get_millis()
    global button_state
    state = not button.value()
    if state != button_state:
        button_state = state
        on_button_callback(button_state)


def loop():
    check_button()
