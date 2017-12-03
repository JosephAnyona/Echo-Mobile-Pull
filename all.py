import requests
import schedule
import time
from time import gmtime, strftime
from datetime import datetime, timedelta
from multiprocessing import Process
import sys


def report_1():
	ARGS = {'_base': 'https://m-swali-hrd.appspot.com',
		'_eid': "XXXXXX", #  replace this with eid from organization settings
		'_pw': 'XXXXXXX'}  # replace this with password from organization settings

	PATH = "/api/cms/report/generate?"
	# Generates a report.

	data = {"eid": ARGS['_eid'],
			"password": ARGS['_pw'], 
			"auth": "XXXXXXXXX",
			"source": X,
			"additionalSpecs": "status",
			"ftype": X,
			"pid": XXXXXXXXXXXXXX,  # replace this with your product id
			"std_field": "field_1,field_2,field_3", # fields you want to include in the report
			"cp_extra": "field_4,field_5,field_6",  # (in CAPS) comma-separated string of serial extra fields
			"field": "XXXXXXXXX",  # comma-separated string of field keys 
			"type": X
			}
	r = requests.post(ARGS['_base'] + PATH,
					 params=data,
					 stream=True,
					 allow_redirects=True)

	if r.status_code == 200:
		body = r.json()
		rkey_ = body.get('rkey')
		print ("Success! Now Fetch your report : %s"  % rkey_)
		print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	else:
		print ("Oops! Something bad happened. Status :%s"% r.status_code)


	ARGS = {'_base': 'https://m-swali-hrd.appspot.com',
		'_eid': 'XXXXXX', #  replace this with eid from organization settings
		'_pw': 'XXXXXXX'}  # replace this with password from organization settings

	PATH = "/api/cms/report/serve?"

	# Fetches a report

	data = {"eid": ARGS['_eid'], 
			"password": ARGS['_pw'], 
			"auth": "XXXXXXXXX",
			"source": X,
			"rkey": rkey_, # Report Key
			}


	r = requests.get(ARGS['_base'] + PATH,
					 params=data,
					 stream=True,
					 allow_redirects=True)
	local_filename = "report1.csv"

	if r.status_code == 200:
		# fetch
		r = requests.get(ARGS['_base'] + PATH,
						 params=data,
						 stream=True,
						 allow_redirects=True)

		# check if complete then write file
		while r.text == "Unauthorized":
			time.sleep(600) # wait 10 minutes
			# Fetch
			r = requests.get(ARGS['_base'] + PATH,
					 params=data,
					 stream=True,
					 allow_redirects=True)

 		# if complete, write file
		if r.text != "Unauthorized":
			with open(local_filename, 'wb') as f:
				for chunk in r:
					f.write(chunk)
			print ("Success! Wrote file %s" % local_filename)
			print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	else:
		print ("Oops! Something bad happened. Status :%s" % r.status_code)


# -------------------------------------------------------------------------------------------------------------------

# Scheduler
def tasks():
	report_1()

# Run every 1 hour
schedule.every(1).hours.do(tasks) 
while True:
	schedule.run_pending()
