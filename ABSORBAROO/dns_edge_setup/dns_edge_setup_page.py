# Copyright 2018 BlueCat Networks. All rights reserved.

# Various Flask framework items.
import os
import sys
import codecs

from flask import url_for, redirect, render_template, flash, g, request, jsonify
from bluecat import route, util
import config.default_config as config
from main_app import app
from .dns_edge_setup_form import GenericFormTemplate
from bluecat_portal.workflows.ABSORBAROO.Edge import Edge
from bluecat_portal.workflows.ABSORBAROO.utils import get_value

def module_path():
    encoding = sys.getfilesystemencoding()
    return os.path.dirname(os.path.abspath(unicode(__file__, encoding)))


# The workflow name must be the first part of any endpoints defined in this file.
# If you break this rule, you will trip up on other people's endpoint names and
# chaos will ensue.
@route(app, '/dns_edge_setup/dns_edge_setup_endpoint')
@util.workflow_permission_required('dns_edge_setup_page')
@util.exception_catcher
def dns_edge_setup_dns_edge_setup_page():
    form = GenericFormTemplate()

    form.edgeurl.data = get_value('edge.config', 'edgeurl')
    form.edgeusername.data = get_value('edge.config', 'username')
    form.edgepassword.data = get_value('edge.config', 'password')
    form.dlname.data = get_value('edge.config', 'domainlist')

    return render_template(
        'dns_edge_setup_page.html',
        form=form,
        text=util.get_text(module_path(), config.language),
        options=g.user.get_options(),
    )

@route(app, '/dns_edge_setup/form', methods=['POST'])
@util.workflow_permission_required('dns_edge_setup_page')
@util.exception_catcher
def dns_edge_setup_dns_edge_setup_page_form():
    form = GenericFormTemplate()
    print(form.edgeurl.data)
    print(form.edgeusername.data)
    print(form.edgepassword.data)
    print(form.dlname.data)
    print(form.submit.data)

    # Put form processing code here
    try:
	edge = Edge(debug=1)
	edge.set_edgeurl(form.edgeurl.data, form.edgeusername.data, form.edgepassword.data, form.dlname.data)
       	flash('success', 'succeed')
    except Exception as err:
       	flash(str(err), 'succeed')
        return redirect(url_for('dns_edge_setupdns_edge_setup_dns_edge_setup_page'))
    else:
        g.user.logger.info('Form data was not valid.')
        return render_template(
            'dns_edge_setup_page.html',
            form=form,
            text=util.get_text(module_path(), config.language),
            options=g.user.get_options(),
        )

@route(app, '/dns_edge_setup/validateurl', methods=['POST'])
@util.workflow_permission_required('dns_edge_setup_page')
@util.exception_catcher
def dns_edge_setup_dns_edge_setup_page_validateurl():
    testurl = str(request.get_json()['url'])
    try:
        edge = Edge()
        edge.test_edgeurl(testurl)
        return jsonify( status='success' )
    except Exception as e:
	print e
        return jsonify( status='failure' )

@route(app, '/dns_edge_setup/validateauth', methods=['POST'])
@util.workflow_permission_required('dns_edge_setup_page')
@util.exception_catcher
def dns_edge_setup_dns_edge_setup_page_validateauth():
    testurl = str(request.get_json()['url'])
    testusername = str(request.get_json()['username'])
    testpassword = str(request.get_json()['password'])
    try:
        edge = Edge()
        edge.test_auth(testurl, testusername, testpassword)
        return jsonify( status='success' )
    except Exception as e:
	print e
        return jsonify( status='failure' )

@route(app, '/dns_edge_setup/validatedlname', methods=['POST'])
@util.workflow_permission_required('dns_edge_setup_page')
@util.exception_catcher
def dns_edge_setup_dns_edge_setup_page_validatedlname():
    testurl = str(request.get_json()['url'])
    testusername = str(request.get_json()['username'])
    testpassword = str(request.get_json()['password'])
    dlname = str(request.get_json()['dlname'])
    try:
        edge = Edge()
        edge.test_dlname(testurl, testusername, testpassword, dlname)
        return jsonify( status='success' )
    except Exception as e:
	print e
        return jsonify( status='failure' )
