# Copyright 2018 BlueCat Networks. All rights reserved.

import os
import json

def set_values(fname, vals):
	try:
		fname = 'bluecat_portal/' + fname
		with open(fname, 'w') as json_data:
			json_data.write(vals)
			json_data.close()
	except Exception as e:
		print e

def get_value(fname, item):
	try:
		fname = 'bluecat_portal/' + fname
		with open(fname) as json_data:
			items = json.load(json_data)
			json_data.close()
			return items[item]
	except Exception as e:
		print e
		return ""

def valid_url(url):
        # If it is of the type *.xxx - valid wildcard
        if '*' in url and '*' in url[0] and '.' in url[1]:
                return True
        elif not '*' in url:
                return True
        else:
                return False
	
