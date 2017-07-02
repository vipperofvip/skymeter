from ghost import Ghost
from bs4 import BeautifulSoup
from time import sleep
import json
from pprint import pprint
from datetime import datetime

def load_auth_info():
	#Check for FAIL: loading the file might fail
	with open('auth.json') as data_file:
		data = json.load(data_file)
		return data['username'],data['password']

def password_is_ok():
	with open('exede_status.json','r+') as auth_status:
		data = json.load(auth_status)
		return True if data['password_status'] == 'OK' else False	

def set_password_status(status):
	with open('exede_status.json', 'r+') as exede_status_file:
        	json.dump({'password_status':status},exede_status_file)

def get_excede_html():
	result = 'unknown'
	usage_page_html = ''
	username, password = load_auth_info()
	#print "ghost initialized..."
	ghost = Ghost(wait_timeout=50, log_level='DEBUG', download_images=False)
	
	#Check for FAIL: no internet access
	try:
		page,resources = ghost.open('https://my.exede.net/usage')
	except Exception as e:
		print e.message
		result = e.message
		ghost.exit()
		return usage_page_html, result

	ghost.wait_for_page_loaded()

	if ghost.exists(".form-control.input-lg.required[name=IDToken1]"):
		print "Login found"
	else:
		print "Login not found"
		result = 'Can\'t find login box on website'
		ghost.exit()
		return usage_page_html, result

	print "Filling in field values"
	ghost.set_field_value(".form-control.input-lg.required[name=IDToken1]",username)
	ghost.set_field_value(".form-control.input-lg.required[name=IDToken2]",password)
	print "Clicking form button"
	#ghost.click('.btn.btn-info.btn-lg.pull-right.col-lg-4[name="Login.Submit"]')
	ghost.click('.btn.btn-info.btn-lg.btn-block[name="Login.Submit"]')
	print "Waiting for page to load"
	ghost.wait_for_page_loaded()

	try:
		if ghost.wait_for_selector('.amount-used',timeout=60):
			print "Found the amount used..."
			result = 'OK'
		else:
			print "Did not find the amount used"	
			result = 'OK'
			#ghost.exit()
			#return usage_page_html, result

	except Exception as e:
		print e.message
		result = e.message

	
	usage_page_html = ghost.content.encode('ascii', 'ignore')
	
	print "Writing resulting page to disk as final_page.html"
	with open('final_page.html', 'w') as data_file:
		data_file.write(usage_page_html)
	
	ghost.exit()
	return usage_page_html, result

def parse_html(exede_html, usage):
	soup = BeautifulSoup(exede_html, 'html.parser')
	
	divs = soup.find_all("div")
	for idex, thisdiv in enumerate(divs):
		
		print "Checking a div: {}".format(thisdiv.get('class'))
		if thisdiv.get('class') is None:
			continue
		
		#bad password
		if "alert-danger" in thisdiv.get('class') and 'hide' not in thisdiv.get('class') and 'password are incorrect.' in thisdiv.text:
			print "Password on file is incorrect, shutting down"
			usage['result'] = 'bad_password'
			set_password_status('bad_password')
			return {'result':'bad_password'}
		
		if "amount-used" in thisdiv.get('class') and 'GB' in thisdiv.text:
			print "Found the amount used"
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

	#check for bad password before doing anything. 
	# bail if the password is bad
	if not password_is_ok():
		return {'result':'bad_password'}

	usage = {}
	usage['gb_used_string'] = 'unknown'
	usage['percent_usage_string'] = 'unknown'
	usage['days_remaining_string'] = 'unknown'
	usage['result'] = 'unknown'
	
	exede_html,usage['result'] = get_excede_html()
	#for testing against html files on disk...	
	#with open('exede_login_now.html','r+') as html:
	#	exede_html = html.read()
	#	usage['result'] = 'OK'

	usage['updatetime'] = datetime.now().strftime("%b %d %I:%M %p")
	
	if usage['result'] is 'OK':
		usage = parse_html(exede_html, usage)

	return usage

