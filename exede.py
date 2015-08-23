from ghost import Ghost
from bs4 import BeautifulSoup
import json
from pprint import pprint
from datetime import datetime

def load_auth_info():
	#Check for FAIL: loading the file might fail
	with open('auth.json') as data_file:
		data = json.load(data_file)
		return data['username'],data['password']

def get_excede_html():
	result = 'unknown'
	usage_page_html = ''
	username, password = load_auth_info()
	#print "ghost initialized..."
	#ghost = Ghost(wait_timeout=30, '''log_level='INFO',''' download_images=False)
	ghost = Ghost(wait_timeout=50, log_level='INFO', download_images=False)
	
	#Check for FAIL: no internet access
	try:
		page,resources = ghost.open('https://my.exede.net/usage')
		#ghost.wait_for_page_loaded()
	except Exception as e:
		print e.message
		result = e.message
		ghost.exit()
		return usage_page_html, result

	ghost.wait_for_page_loaded()

	if ghost.exists(".form-control.input-lg.required[name=IDToken1]"):
		print "Login found"
		pass
	else:
		print "Login not found"
		result = 'Can\'t find login box on website'
		ghost.exit()
		return usage_page_html, result
	print "Filling in field values"
	ghost.set_field_value(".form-control.input-lg.required[name=IDToken1]",username)
	ghost.set_field_value(".form-control.input-lg.required[name=IDToken2]",password)
	print "Clicking form button"
	ghost.click('.btn.btn-info.btn-lg.pull-right.col-lg-4[name="Login.Submit"]')
	print "Waiting for page to load"
	ghost.wait_for_page_loaded()
	print "Writing resulting page to disk as final_page.html"
	
	#save what we got to disk
	with open('final_page.html', 'w') as data_file:
		data_file.write(ghost.content.encode('ascii', 'ignore'))
		

	try:
		if ghost.wait_for_selector('.amount-used',timeout=60):
			print "Found the amount used..."
		else:
			result =  "did not find the amount used..."
			ghost.exit()
			return usage_page_html, result
	except Exception as e:
		print e.message
		result = e.message
		return usage_page_html, result

	usage_page_html = ghost.content.encode('ascii', 'ignore')
	result = 'OK'
	ghost.exit()
	return usage_page_html, result

def parse_html(exede_html, usage):
	soup = BeautifulSoup(exede_html, 'html.parser')
	
	divs = soup.find_all("div")
	for idex, thisdiv in enumerate(divs):
		if thisdiv.get('class') is None:
			continue
		if "amount-used" in thisdiv.get('class') and 'GB' in thisdiv.text:
			usage['gb_used_string'] = thisdiv.text

	ps = soup.find_all("p")
	for idex,thisp in enumerate(ps):
		if thisp.get('class') is None:
			continue
		if "used of" in thisp.text:
			usage['percent_usage_string'] = thisp.text
		if "remaining in the current"  in thisp.text:
			usage['days_remaining_string'] = thisp.text

	if usage['gb_used_string'] is not 'unknown' and \
	usage['percent_usage_string'] is not 'unknown' and \
	usage['days_remaining_string'] is not 'unknown':
		usage['result'] = 'OK'
	else:
		usage['result'] = 'Problem parsing HTML'
	return usage

def usage():
	
	usage = {}
	usage['gb_used_string'] = 'unknown'
	usage['percent_usage_string'] = 'unknown'
	usage['days_remaining_string'] = 'unknown'
	usage['result'] = 'unknown'
	exede_html,usage['result'] = get_excede_html()
	usage['updatetime'] = datetime.now().strftime("%a %b %d @ %I:%M %p")
	#usage['result'] = 'OK'
	#exede_html = open('final_page.html','r').read()
	
	if usage['result'] is 'OK':
		usage = parse_html(exede_html, usage)

	return usage

	#pprint(usage)
