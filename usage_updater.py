#!/usr/bin/python

#Todo:
# Check for bad username/password, and halt detection if it fails twice during two separate checks in a row
# webpage updates - Create system to check for updated files pushed to Git, download them, install them
# username password updates with encryption - create system to download updated auth information from a private box account
# email alerting systems and health checks - Send email about problems detected

from exede import usage
from time import sleep
import json

def write_usage_to_disk(usage):
	with open('usage.json', 'w') as usage_file:
		json.dump(usage,usage_file)
	try:	
		history_data = []
		with open('usage_history.json', 'r+') as usage_history_file:
        		history_data = json.load(usage_history_file)
		history_data.append(usage)	
		with open('usage_history.json', 'w+') as usage_history_file:
			json.dump(history_data,usage_history_file)
	except Exception as e:
		print "usage_updater.py: write_usage_to_disk(): Problem with writing to the history file"	
	return

print "Checking usage"

for i in xrange(0,3):
	theusage = usage()
	if theusage['result'] == 'OK':
		print "Result was OK, done"
		break
	if theusage['result'] == 'bad_password':
		print "Bad password, halting"
		break
			
	print "Problem: {}".format(theusage['result'])
	print "trying again in 200 seconds"
	sleep(200)


print "Writing to file"
write_usage_to_disk(theusage)
