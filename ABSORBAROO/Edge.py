# Copyright 2018 BlueCat Networks. All rights reserved.

import os
import requests
import json
#from bluecat_portal.workflows.ABSORBAROO.utils import get_value, set_values, valid_url
from utils import get_value, set_values, valid_url

rest_calls = {
        'login': { 'url' : 'userManagement/authentication/login', 'type' : 'post' },
        'tos': { 'url' : 'userManagement/tos', 'type' : 'get' },
        'getdomainlist': { 'url' : 'list/dns', 'type': 'get' },
        'updatedl': { 'url' : 'list/dns/id/attachfile', 'type': 'postfile' }
}

class EdgeException(Exception): pass

class Edge(object):

        def __init__ (self, debug=0):
                self.debug = debug
		self.filename = "edge.config"

	def test_edgeurl(self, edgeurl):
		try:
                	edge_url = 'https://api-' + edgeurl + '/v1/api/'
                	self.edge_url = edge_url
                	self.header = {'Authorization': 'Bearer '}
			if 'tosTimestamp' in self.rest_call ('tos'):
				return 0
			else: raise EdgeException('not a valid edge url')
		except Exception as e:
			raise EdgeException(e)

	def test_auth(self, edgeurl, username, password):
                self.edge_url = 'https://api-' + edgeurl + '/v1/api/'
                self.logindata = { "username": username, "password": password }
                self.header = {'Authorization': 'Bearer '}
                self.edge_token = self.rest_call('login', self.logindata)['auth_token']
		if not self.edge_token:
			raise EdgeException('Invalid username and/or password')

	def test_dlname(self, edgeurl, username, password, dlname):
                self.edge_url = 'https://api-' + edgeurl + '/v1/api/'
                self.logindata = { "username": username, "password": password }
                self.header = {'Authorization': 'Bearer '}
                self.edge_token = self.rest_call('login', self.logindata)['auth_token']
                self.dlid = 0

		if not self.edge_token:
			raise EdgeException('Invalid username and/or password')
                self.header = {'Authorization': 'Bearer ' + self.edge_token}

                # Raise a SETUP error if the domain list name is not found.
                for dl in self.rest_call ('getdomainlist'):
                        if dlname in dl['name']:
                                self.dlid = dl['id']

                if self.dlid == 0:
                        raise EdgeException('SETUP ERROR: domain list does not exist, please create it and validate again.')
		
	def set_edgeurl(self, edgeurl, username, password, dlname):
                self.edge_url = 'https://api-' + edgeurl + '/v1/api/'
                self.logindata = { "username": username, "password": password }
                self.header = {'Authorization': 'Bearer '}
                self.edge_token = self.rest_call('login', self.logindata)['auth_token']
                self.header = {'Authorization': 'Bearer ' + self.edge_token}
                self.dlid = 0


                # Raise a SETUP error if the domain list name is not found.
                for dl in self.rest_call ('getdomainlist'):
                        if dlname in dl['name']:
                                self.dlid = dl['id']
                if self.dlid == 0:
                        raise EdgeException('SETUP ERROR: domain list does not exist, please create it and validate again.')
		set_values(self.filename, json.dumps({ 'edgeurl': edgeurl, 'username': username, 'password': password, 'domainlist': dlname }))

        def rest_call (self, call, data="", id=0):
                url = rest_calls[call]['url']
                type = rest_calls[call]['type']
                try:
                        if (type == 'post'):
                                jsondata = requests.post(self.edge_url + url, json=data, headers=self.header).json()
                        elif (type == 'get'):
                                content = requests.get(self.edge_url + url + data, headers=self.header)
				jsondata = content.json()
                        elif (type == 'postfile'):
                                url = url.replace("id", id)
                                jsondata = requests.post(self.edge_url + url, files=data, headers=self.header).json()

                        if 'brief' in jsondata:
                                raise EdgeException (jsondata['brief'])
                        else:
                                if self.debug: print 'DEBUG: rest call -- ' + self.edge_url + url + ', result: ' + json.dumps(jsondata)
                                return jsondata
                except requests.exceptions.ConnectionError, err:
			if type == 'get' and '/tos' in url:
				return content
                        else:
				raise EdgeException ('SETUP ERROR: Enter a valid edge url ommitting http://')

        def updateDomainList (self, csvfile):
                Dict = {'file':(csvfile, open(csvfile, 'rb'), 'text/plain')}
                return self.rest_call ('updatedl', Dict, self.dlid)

	def get_edgeurl(self):
		return get_value(self.filename, "edgeurl")

	def get_username(self):
		return get_value(self.filename, "username")

	def get_password(self):
		return get_value(self.filename, "password")

	def get_dlname(self):
		return get_value(self.filename, "domainlist")
