# Copyright 2019 BlueCat Networks (USA) Inc. and its affiliates
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# By: BlueCat Networks
# Date: 2019-08-28
# Gateway Version: 19.5.1 or greater
# Description: BlueCat Gateway module for Microsoft Office 365 calls

import os
import sys
import requests
import json

base_url = 'https://endpoints.office.com/'

class EndpointsException(Exception): pass

class EndpointsAPI(object):

    def __init__ (self, client_id, debug=False):
        self._client_id = client_id
        self._loaded = False
        self._service_areas = []
        self._endpoints = []
        self._debug = debug

    def validate_client_id(self):
        valid = False
        try:
            params = {'ClientRequestId': self._client_id}
            response = requests.get(base_url + 'version', params=params)
            if response.status_code == 200:
                valid = True
        except requests.exceptions.RequestException as e:
            if self._debug:
                print('DEBUG: Exceptin <%s>' % str(e))
        except requests.exceptions.ConnectionError as e:
            if self._debug:
                print('DEBUG: Exceptin <%s>' % str(e))
        return valid

    def _collect_service_areas(self):
        service_area_dict = {}

        for ep in self._endpoints:
            service_area = ep['serviceArea']
            if service_area not in service_area_dict:
                service_area_dict[service_area] = {
                    'name': service_area,
                    'display_name': ep['serviceAreaDisplayName'],
                    'check': True
                }
        self._service_areas = list(service_area_dict.values())

    def get_versions(self):
        versions = []
        try:
            params = {'ClientRequestId': self._client_id}
            response = requests.get(base_url + 'version', params=params)
            if response.status_code == 200:
                versions = response.json()
        except requests.exceptions.RequestException as e:
            if self._debug:
                print('DEBUG: Exceptin <%s>' % str(e))
        except requests.exceptions.ConnectionError as e:
            if self._debug:
                print('DEBUG: Exceptin <%s>' % str(e))
        return versions

    def get_current_version(self, instance):
        version = None
        try:
            params = {'ClientRequestId': self._client_id}
            response = requests.get(base_url + 'version/' + instance, params=params)
            if response.status_code == 200:
                contents = response.json()
                version = contents.get('latest')
        except requests.exceptions.RequestException as e:
            if self._debug:
                print('DEBUG: Exceptin <%s>' % str(e))
        except requests.exceptions.ConnectionError as e:
            if self._debug:
                print('DEBUG: Exceptin <%s>' % str(e))
        return version

    def _load_endpoints(self, instance):
        valid = False
        try:
            params = {'ClientRequestId': self._client_id}
            response = requests.get(base_url + 'endpoints/' + instance, params=params)
            if response.status_code == 200:
                self._endpoints = response.json()
                self._collect_service_areas()
                self._loaded = True
                valid = True
        except requests.exceptions.RequestException as e:
            if self._debug:
                print('DEBUG: Exceptin <%s>' % str(e))
        except requests.exceptions.ConnectionError as e:
            if self._debug:
                print('DEBUG: Exceptin <%s>' % str(e))
        return valid

    def get_service_areas(self, instance):
        if not self._loaded:
            self._load_endpoints(instance)
        return self._service_areas

    def get_endpoints(self, instance):
        if not self._loaded:
            self._load_endpoints(instance)
        return self._endpoints
        
