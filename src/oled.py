
import ssd1306
from common import create_i2c


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


def display_lines(lines):
    oled.fill(0)
    line_count = 0
    for line in lines:
        oled.text(str(line), 0, line_count * 10)
        line_count += 1
    oled.show()


def display_boot():
    display_lines(["BOOT", "v0.1.0"])

def init():
    display_boot()