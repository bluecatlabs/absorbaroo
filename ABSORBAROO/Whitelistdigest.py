# Copyright 2018 BlueCat Networks. All rights reserved.

import os
import requests
import json
import datetime
import hashlib
import re

from utils import get_value, set_values, valid_url
from apscheduler.schedulers.background import BackgroundScheduler
from Edge import Edge
from Sdwan import Sdwan

def absorbaroo_sync():
        wlurl = get_value('wl.config', "url")
        interval = get_value('wl.config', "interval")
        filters = get_value('wl.config', "filters")
        edgeurl = get_value('edge.config', "edgeurl")
        edge_username = get_value('edge.config', "username")
        edge_password = get_value('edge.config', "password")
        edge_domainlist = get_value('edge.config', "domainlist")
        meraki_key = get_value('meraki.config', "key")
        meraki_orgname = get_value('meraki.config', "orgname")
        meraki_templatename = get_value('meraki.config', "templatename")

        wl = Whitelistdigest(debug=1)
        wl.set_whitelisturl(wlurl, interval, filters)

        oldhash = get_value('hash', 'hash')
        newhash = wl.hash_wl()

        if not oldhash == newhash:
                wl.dump_to_csv()
                e = Edge(debug=1)
                e.set_edgeurl(edgeurl, edge_username, edge_password, edge_domainlist)
                edge_result = e.updateDomainList('edgesync.txt')

                sdwan = Sdwan(debug=0)
                sdwan.set_key(meraki_key)
                sdwan.set_organization(meraki_orgname)
                sdwan.set_template(meraki_templatename)
                print json.dumps(str(sdwan.update_l3fwrules(wl.wl)))

                results = {"timestamp": str(datetime.datetime.now()), "edge_urls_processed": edge_result["numOfValidDomains"], "sdwan_rules_processed": sdwan.get_rules_processed()}
                set_values('results.txt', json.dumps(results))
                set_values('hash', json.dumps({'hash': newhash}))

        print 'perform_sync'

class WhitelistdigestException(Exception): pass
class Whitelistdigest(object):

        def __init__ (self, debug=0):
                self.debug = debug
                self.filename = "wl.config"
                self.url = ""
                self.wl = {}
                self.filters = None

        def test_whitelisturl(self, url):
                try:
                        wl = requests.get(url).json()
                        if not type(wl) == list:
                                raise WhitelistdigestException('ERROR: ' + wl)
                except requests.exceptions.ConnectionError, err:
                        raise WhitelistdigestException('ERROR: Failed to connect to white list url')

        def update_interval(self, interval, scheduler):
                scheduler.print_jobs()
                try:
                        scheduler.remove_job('4401')
                except Exception: pass

                scheduler.add_job(absorbaroo_sync, 'interval', seconds=int(self.interval), id='4401')
                scheduler.start()

        def set_whitelisturl(self, url, interval=86400, filters=None):
                self.url = url
                self.interval = interval
                self.filters = filters
                try:
                        self.wl = requests.get(self.url).json()
                        if not type(self.wl) == list:
                                raise WhitelistdigestException('ERROR: ' + self.wl)
                        if self.debug: print "DEBUG: Retreived whitelist from " + url + ": " + str(len(self.wl)) + " items"
                        set_values(self.filename, json.dumps({ "url": self.url, "interval": self.interval, "filters": self.filters }))

                except requests.exceptions.ConnectionError, err:
                        raise WhitelistdigestException('ERROR: Failed to connect to white list url')


        def dump_to_csv (self):
                pattern = re.compile(r'(' + self.filters + ')') if self.filters else ""
                self.urlcount = 0
                file = open ("edgesync.txt", "w")
                for wl in self.wl:
                        if self.filters and 'required' in wl and not wl['required']:
                                if re.findall (pattern, wl['serviceArea']):
                                        print 'Skipping: ' + wl['serviceAreaDisplayName']
                                        continue
                        urllist = wl['allowUrls'] if 'allowUrls' in wl else wl['defaultUrls'] if 'defaultUrls' in wl else wl['urls'] if 'urls' in wl else ''
                        for url in urllist:
                                if valid_url(url):
                                        self.urlcount += 1
                                        file.write(url + "\n")
                file.close()
                if self.debug: print "DEBUG: total urls processed = " + str(self.urlcount)

        def jsonList (self):
                return self.wl

        def hash_wl(self):
                return hashlib.md5(json.dumps(self.wl)).hexdigest()

        def get_whitelisturl(self):
                return get_value(self.filename, "url")

        def get_interval(self):
                return get_value(self.filename, "interval")

        def get_filters(self):
                return get_value(self.filename, "filters")

