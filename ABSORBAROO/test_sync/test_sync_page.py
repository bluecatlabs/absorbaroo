# Copyright 2018 BlueCat Networks. All rights reserved.

# Various Flask framework items.
import os
import sys
import codecs
import datetime

from flask import url_for, redirect, render_template, flash, g, json

from bluecat import route, util
import config.default_config as config
from main_app import app
from .test_sync_form import GenericFormTemplate
from bluecat_portal.workflows.ABSORBAROO.utils import get_value, set_values
from bluecat_portal.workflows.ABSORBAROO.Edge import Edge
from bluecat_portal.workflows.ABSORBAROO.Whitelistdigest import Whitelistdigest
from bluecat_portal.workflows.ABSORBAROO.Sdwan import Sdwan

def module_path():
    encoding = sys.getfilesystemencoding()
    return os.path.dirname(os.path.abspath(unicode(__file__, encoding)))


# The workflow name must be the first part of any endpoints defined in this file.
# If you break this rule, you will trip up on other people's endpoint names and
# chaos will ensue.
@route(app, '/test_sync/test_sync_endpoint')
@util.workflow_permission_required('test_sync_page')
@util.exception_catcher
def test_sync_test_sync_page():
    form = GenericFormTemplate()
    form.interval.data = get_value('results.txt', 'timestamp')
    form.edge_result.data = get_value('results.txt', 'edge_urls_processed')
    form.sdwan_result.data = get_value('results.txt', 'sdwan_rules_processed')
    return render_template(
        'test_sync_page.html',
        form=form,
        text=util.get_text(module_path(), config.language),
        options=g.user.get_options(),
    )

@route(app, '/test_sync/form', methods=['POST'])
@util.workflow_permission_required('test_sync_page')
@util.exception_catcher
def test_sync_test_sync_page_form():
    form = GenericFormTemplate()
    wlurl = get_value('wl.config', "url")
    interval = get_value('wl.config', "interval")
    edgeurl = get_value('edge.config', "edgeurl")
    edge_username = get_value('edge.config', "username")
    edge_password = get_value('edge.config', "password")
    edge_domainlist = get_value('edge.config', "domainlist")
    meraki_key = get_value('meraki.config', "key")
    meraki_orgname = get_value('meraki.config', "orgname")
    meraki_templatename = get_value('meraki.config', "templatename")

    wl = Whitelistdigest(debug=1)
    wl.set_whitelisturl(wlurl, interval)

    oldhash = get_value('hash', 'hash')
    newhash = wl.hash_wl()

    if not oldhash == newhash:
    	wl.dump_to_csv()
    	e = Edge(debug=1)
    	e.set_edgeurl(edgeurl, edge_username, edge_password, edge_domainlist)
    	edge_result = e.updateDomainList('edgesync.txt')

    	sdwan = Sdwan(debug=1)
    	sdwan.set_key(meraki_key)
    	sdwan.set_organization(meraki_orgname)
    	sdwan.set_template(meraki_templatename)
    	print json.dumps(str(sdwan.update_l3fwrules(wl.wl)))

    	results = {"timestamp": str(datetime.datetime.now()), "edge_urls_processed": edge_result["numOfValidDomains"], "sdwan_rules_processed": sdwan.get_rules_processed()}
    	set_values('results.txt', json.dumps(results))
    	set_values('hash', json.dumps({'hash': newhash}))

    form.interval.data = get_value('results.txt', 'timestamp')
    form.edge_result.data = get_value('results.txt', 'edge_urls_processed')
    form.sdwan_result.data = get_value('results.txt', 'sdwan_rules_processed')
    return render_template(
        'test_sync_page.html',
        form=form,
        text=util.get_text(module_path(), config.language),
        options=g.user.get_options(),
    )

    print 'perform_sync'


