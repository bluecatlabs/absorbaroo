# Copyright 2018 BlueCat Networks. All rights reserved.

import os
import json
from meraki_api import MerakiAPI

from utils import get_value, set_values, valid_url

def create_single_rule(item):
        # Get comment string
        commentstr = 'Office365 id ' + str(item['id']) + ":"
        commentstr += " " + item['serviceArea'] if 'serviceArea' in item else ""
        commentstr += " " + item['optionalImpact'] if 'optionalImpact' in item else ""

        # Get allowed ports
        allowedPorts = ''
        if 'tcpPorts' in item: allowedPorts += item['tcpPorts']
        elif 'allowTcpPorts' in item: allowedPorts += item['allowTcpPorts']
        elif 'defaultTcpPorts' in item: allowedPorts += item['defaultTcpPorts']
        elif 'optimizeTcpPorts' in item: allowedPorts += item['optimizeTcpPorts']
        else: return 0

        # Get allowed url list and add optmizeUrls as well
        urllist = (item['urls'] if 'urls' in item
            else item['allowUrls'] if 'allowUrls' in item
            else item['defaultUrls'] if 'defaultUrls' in item
            else "")
        allowedCidr = ''
        if urllist:
                urllist += item['optimizeUrls'] if 'optimizeUrls' in item else ""
                for url in urllist:
                        if valid_url(url):
                                allowedCidr += url + ","
                        else: print 'invalid: ' + url

        if not allowedCidr:
                return

        # Create and return the rule object here
        rule = {}
        rule["comment"] = commentstr
        rule["policy"] = "allow"
        rule["protocol"] = "tcp"
        rule["destPort"] = allowedPorts
        rule["destCidr"] = allowedCidr[:-1]
        rule["srcPort"] = "any"
        rule["srcCidr"] = "any"
        rule["syslogEnabled"] = False
        return rule

class MerakiException(Exception): pass
class Sdwan(object):

        def __init__ (self, debug=0):
                self.debug = debug
                self.filename = "meraki.config"

        def set_key(self, apikey):
                self.key = apikey
                self.sdwan = MerakiAPI(self.key)
                self.organization = self.sdwan.organizations()
                self.orgid = 0
                self.templateid = 0
                self.orgname = ""
                self.templatename = ""
                self.rulecount = 0

        def test_key(self, apikey):
                try:
                        MerakiAPI(apikey).organizations().index().json()
                except Exception as e:
                        raise MerakiException(e)

        def test_orgname(self, apikey, orgname):
                found = 0
                try:
                        for org in MerakiAPI(apikey).organizations().index().json():
                                print 'checking with ' + org['name']
                                if orgname == org['name']:
                                        found = 1
                        if not found: raise MerakiException('organization ' + orgname + ' does not exist')
                except Exception as e:
                        raise MerakiException(e)

        def test_template(self, apikey, orgname, templatename):
                try:
                        sdwan = MerakiAPI(apikey)
                        orgs = sdwan.organizations()
                        for org in orgs.index().json():
                                if orgname == org['name']:
                                        orgs.use(org['id'])
                                        templates = orgs.config_templates().index().json()
                                        for t in templates:
                                                print 'checking with template: ' + t['name']
                                                if templatename == t['name']:
                                                        return 0
                        raise MerakiException('organization does not exist')
                except Exception as e:
                        raise MerakiException(e)

        def set_organization(self, orgname):
                for org in self.organization.index().json():
                        if orgname in org['name']:
                                self.organization.use(org['id'])
                                self.orgname = orgname
                                self.orgid = org['id']
                                if self.debug: print 'DEBUG: Accessing Meraki organization' + org['name']
                                self.networks = self.organization.networks()
                                self.templates = self.organization.config_templates()
                if self.orgid == 0:
                        raise MerakiException('SETUP ERROR: Invalid organization name, please provide a valid and existing organization name')

        def set_template(self, templatename):
                for template in self.templates.index().json():
                        if templatename in template['name']:
                                self.templateid = template['id']
                                self.templatename = templatename
                                self.networks.use(template['id'])
                                if self.debug: print 'DEBUG: Accessing Meraki template' + template['name']
                                self.l3fwrules = self.networks.l3_firewall_rules()

                if self.templateid == 0:
                        raise MerakiException('SETUP ERROR: Invalid template name, please provide a valid and existing template name')

                set_values(self.filename, json.dumps({'key': self.key, 'orgname': self.orgname, 'templatename': self.templatename }))

        def update_l3fwrules(self, wl):
                newrules = []
                # Add every old existing rule except the default rule and old Office365 rules
                rules = self.l3fwrules.get().json()

                deny_all_rule = {}
                deny_all_commentstr = "Deny all outbound traffic"
                deny_all_rule['comment'] = deny_all_commentstr
                deny_all_rule["policy"] = "deny"
                deny_all_rule["protocol"] = "any"
                deny_all_rule["destPort"] = "any"
                deny_all_rule["destCidr"] = "any"
                deny_all_rule["srcPort"] = "any"
                deny_all_rule["srcCidr"] = "any"
                deny_all_rule["syslogEnabled"] = False

                for eachrule in rules:
                        commentstr = eachrule['comment']
                        if deny_all_commentstr in commentstr:
                                deny_all_rule = eachrule

                        elif "Default rule" not in eachrule['comment'] and "Office365" not in eachrule['comment']:
                                newrules.append(eachrule)

                # Start adding the new rules here
                for item in wl:
                        self.rulecount += 1
                        rule = create_single_rule(item)
                        if rule: newrules.append(rule)

                # Add deny all rule to the end
                newrules.append(deny_all_rule)

                if self.debug: print 'DEBUG: new rules: ' + str(newrules)

                finalrules = {}
                finalrules['rules'] = newrules
                finalrules['syslogEnabled'] = True

                return self.l3fwrules.update(finalrules)

        def get_rules_processed(self):
                return self.rulecount

        def get_key(self):
                return get_value(self.filename, "key")

        def get_orgname(self):
                return get_value(self.filename, "orgname")

        def get_templatename(self):
                return get_value(self.filename, "templatename")

        def dump(self):
                newjson = {}
                interested = ['organization', 'templates', 'l3fwrules', 'devices']
                for attr, value in vars(self).items():
                        if attr in interested:
                                newjson[attr] = value.get().json()
                return  json.dumps(newjson)

