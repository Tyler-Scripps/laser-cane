# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.
import time

import board
import busio
import adafruit_ssd1306

import adafruit_vl53l0x


# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)


if i2c.try_lock():
    print("Found i2c addresses:")
    for x in i2c.scan():
        print(hex(x))
    i2c.unlock()

display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
print("clearing display")
display.fill(0)
display.show()
print("cleared")
display.text('Laser cane v0.1',0,0,1)
display.show()


vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

vl53.start_continuous()

# Main loop will read the range and print it every second.
while True:
    tempStr = "Range: " + str(vl53.range) + "mm"
    print(tempStr)
    display.text("                ", 0, 8, 0)
    display.text(tempStr, 0, 8, 1)
    display.show()
    time.sleep(1.0)