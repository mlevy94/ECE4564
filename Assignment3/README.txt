HOW TO:
	icu.py - uses data input from user in form of satellite and zip code and displays information
		 correlated to those values. Those values include satellite information, latitude and
		 longitude of zip, ehpermis data of the satellite, next five viewings, and alerts 
		 within fifteen minutes of viewing.
ARGUMENTS:
	file [-z zipcode] [-s satellite Nomad ID]
	DEFAULTS:
		-z 24060
		-s 25397
DEPENDENCIES:
	icu.py:
		Python Modules:
				argparse
				requests
				ephem
				datetime
				math
				zipcode
				geocoder
				json
				pygame
				sched
				twilio.rest TwilioRestClient
				Thread
				
				
