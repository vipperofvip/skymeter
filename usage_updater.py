#!/usr/bin/python

from exede import usage
from time import sleep
import json

def write_usage_to_disk(usage):
	with open('usage.json', 'w') as usage_file:
		json.dump(usage,usage_file)
	return

print "Checking usage"

for i in xrange(0,3):
	theusage = usage()
	if theusage['result'] == 'OK':
		print "Result was OK, done"
		break
	print "Problem: {}".format(theusage['result'])
	print "trying again in 200 seconds"
	sleep(200)


print "Writing to file"
write_usage_to_disk(theusage)
