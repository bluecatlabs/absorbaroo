# Copyright 2018 BlueCat Networks. All rights reserved.

# Various Flask framework items.
import os
import sys
import codecs

from flask import url_for, redirect, render_template, flash, g, request, jsonify

from bluecat import route, util
import config.default_config as config
from main_app import app
from .sdwan_setup_form import GenericFormTemplate
from bluecat_portal.workflows.ABSORBAROO.Sdwan import Sdwan
from bluecat_portal.workflows.ABSORBAROO.utils import get_value

def module_path():
    encoding = sys.getfilesystemencoding()
    return os.path.dirname(os.path.abspath(unicode(__file__, encoding)))


# The workflow name must be the first part of any endpoints defined in this file.
# If you break this rule, you will trip up on other people's endpoint names and
# chaos will ensue.
@route(app, '/sdwan_setup/sdwan_setup_endpoint')
@util.workflow_permission_required('sdwan_setup_page')
@util.exception_catcher
def sdwan_setup_sdwan_setup_page():
    form = GenericFormTemplate()

    form.key.data = get_value('meraki.config', 'key')
    form.orgname.data = get_value('meraki.config', 'orgname')
    form.templatename.data = get_value('meraki.config', 'templatename')

    return render_template(
        'sdwan_setup_page.html',
        form=form,
        text=util.get_text(module_path(), config.language),
        options=g.user.get_options(),
    )

@route(app, '/sdwan_setup/form', methods=['POST'])
@util.workflow_permission_required('sdwan_setup_page')
@util.exception_catcher
def sdwan_setup_sdwan_setup_page_form():
    form = GenericFormTemplate()
    if form.validate_on_submit():
        print(form.key.data)
        print(form.orgname.data)
        print(form.templatename.data)
        print(form.submit.data)

        sdwan = Sdwan(debug=1)
	sdwan.set_key(form.key.data)
	sdwan.set_organization(form.orgname.data)
	sdwan.set_template(form.templatename.data)

        # Put form processing code here
        g.user.logger.info('SUCCESS')
        flash('success', 'succeed')
        return redirect(url_for('sdwan_setupsdwan_setup_sdwan_setup_page'))
    else:
        g.user.logger.info('Form data was not valid.')
        return render_template(
            'sdwan_setup_page.html',
            form=form,
            text=util.get_text(module_path(), config.language),
            options=g.user.get_options(),
        )

@route(app, '/sdwan_setup/validatekey', methods=['GET', 'POST'])
@util.workflow_permission_required('sdwan_setup_page')
@util.exception_catcher
def sdwan_setup_sdwan_setup_validatekey():
    form = GenericFormTemplate()
    testkey = str(request.get_json()['key'])
    try:
        sdwan = Sdwan()
	sdwan.test_key(testkey)
        return jsonify( status='success' )
    except Exception as e:
	print e
        return jsonify( status='failure' )

@route(app, '/sdwan_setup/validateorgname', methods=['GET', 'POST'])
@util.workflow_permission_required('sdwan_setup_page')
@util.exception_catcher
def sdwan_setup_sdwan_setup_validateorgname():
    form = GenericFormTemplate()
    testkey = str(request.get_json()['key'])
    testorgname = str(request.get_json()['orgname'])
    try:
        sdwan = Sdwan()
	sdwan.test_orgname(testkey, testorgname)
        return jsonify( status='success' )
    except Exception as e:
	print e
        return jsonify( status='failure' )

@route(app, '/sdwan_setup/validatetemplate', methods=['GET', 'POST'])
@util.workflow_permission_required('sdwan_setup_page')
@util.exception_catcher
def sdwan_setup_sdwan_setup_validatetemplate():
    form = GenericFormTemplate()
    testkey = str(request.get_json()['key'])
    testorgname = str(request.get_json()['orgname'])
    testtemplate = str(request.get_json()['template'])
    try:
        sdwan = Sdwan()
	sdwan.test_template(testkey, testorgname, testtemplate)
        return jsonify( status='success' )
    except Exception as e:
	print e
        return jsonify( status='failure' )
