#!/usr/bin/python
import gaugette.ssd1306
import time
import sys
from time import sleep
import json
from gaugette.fonts import arial_16

ROWS = 32

if gaugette.platform == 'raspberrypi':
  RESET_PIN = 4
  DC_PIN    = 6
else:  # beagebone
  RESET_PIN = "P9_15"
  DC_PIN    = "P9_13"
font = arial_16
print("init")

led = gaugette.ssd1306.SSD1306(reset_pin=RESET_PIN, dc_pin=DC_PIN, rows=64, cols=128, buffer_cols=256)

print("begin")
led.begin()
print("clear")
led.clear_display()
led.display()

led.invert_display()
time.sleep(0.5)
led.normal_display()
time.sleep(0.5)
led.flip_display()
led.set_contrast(0x81)

led.draw_text2(0,0,'Updating usage...',1,1)
led.display()
