#!/usr/bin/python
import gaugette.ssd1306
import time
import sys
from time import sleep
import json
from gaugette.fonts import arial_16

def load_usage_from_disk():
	with open('usage.json') as usage_file:
		usage = json.load(usage_file)
	return usage

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

while True:
	try:
		usage = load_usage_from_disk()
		led.clear_display()
		led.draw_text2(30,0,usage['gb_used_string'],2,1)
		led.draw_text2(5,20,'used ' + usage['percent_usage_string'].split('used ')[1].replace('allowance','limit'),1,1)
		led.draw_text2(8,30,'with ' + usage['days_remaining_string'].split(' in')[0].replace('remaining','left'),1,1)
		led.draw_text2(0,45,'updated:',1,1)
		led.draw_text2(0,55,usage['updatetime'],1,1)
	except:	
		led.clear_display()
		led.draw_text2(30,0,'??',2,1)
		led.draw_text2(5,20,'problem loading data',1)
		led.draw_text2(5,30,'will try again @3AM',1)
		led.draw_text2(0,45,'updated:',1,1)
		led.draw_text2(0,55,usage['updatetime'],1,1)

	led.display()
	sleep(500)
	
