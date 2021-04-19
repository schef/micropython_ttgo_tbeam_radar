#!/bin/bash

#rshell -p /dev/ttyUSB0 --buffer-size 512 cp led_blink.py /pyboard/main.py
rshell -p /dev/ttyUSB0 --buffer-size 512 repl
