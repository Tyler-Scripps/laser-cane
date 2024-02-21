# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.
import time

import board
from digitalio import DigitalInOut
import busio
import adafruit_ssd1306

from adafruit_vl53l0x import VL53L0X


# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

displayDetected = True

display = None

try:
    display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
    display.rotate(False)
except:
    print("No display detected")
    displayDetected = False

if displayDetected:
    print("display detected, clearing display")
    display.fill(0)
    display.show()
    print("cleared")
    display.text('Laser cane v0.1',0,0,1)
    display.show()

shutdownPins = [DigitalInOut(board.IO3), DigitalInOut(board.IO1), DigitalInOut(board.IO2), DigitalInOut(board.IO38), DigitalInOut(board.IO39)]

for pin in shutdownPins:
    pin.switch_to_output(value=False)
    pin.value = False

# time.sleep(30)

vl53List = []

for i, power_pin in enumerate(shutdownPins):
    print("Setting vl53", i, "to address:", hex(i + 0x30))
    # turn on the VL53L0X to allow hardware check
    power_pin.value = True
    vl53List.insert(i, VL53L0X(i2c))
    vl53List[i].set_address(i + 0x30)


print("Multiple VL53L0X sensors' addresses are assigned properly\n")

for vl53 in vl53List:
    vl53.start_continuous()

# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

while True:
    ranges = []
    for vl53 in vl53List:
        ranges.append(min((vl53.range / 1000), 2.0))
    
    printStr = ""
    for range in ranges:
        printStr += "{:.1f}".format(range) + ' '

    if displayDetected:
        display.fill(0)
        display.text(printStr, 0, 8, 1)
        display.show()
        print(printStr)
    else:
        print(printStr)
