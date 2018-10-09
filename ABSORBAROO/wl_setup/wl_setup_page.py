# Copyright 2018 BlueCat Networks. All rights reserved.

# Various Flask framework items.
import os
import sys
import codecs

from flask import url_for, redirect, render_template, flash, g, request, jsonify

from bluecat import route, util
import config.default_config as config
from main_app import app
from .wl_setup_form import GenericFormTemplate
from bluecat_portal.workflows.ABSORBAROO.Whitelistdigest import Whitelistdigest, WhitelistdigestException
from bluecat_portal.workflows.ABSORBAROO.utils import get_value

def module_path():
    encoding = sys.getfilesystemencoding()
    return os.path.dirname(os.path.abspath(unicode(__file__, encoding)))


# The workflow name must be the first part of any endpoints defined in this file.
# If you break this rule, you will trip up on other people's endpoint names and
# chaos will ensue.
@route(app, '/wl_setup/wl_setup_endpoint')
@util.workflow_permission_required('wl_setup_page')
@util.exception_catcher
def wl_setup_wl_setup_page():
    form = GenericFormTemplate()
    form.whitelisturl.data = get_value('wl.config', 'url')
    form.interval.data = get_value('wl.config', 'interval')
    form.filters.data = get_value('wl.config', 'filters')

    return render_template(
        'wl_setup_page.html',
        form=form,
        text=util.get_text(module_path(), config.language),
        options=g.user.get_options(),
    )

@route(app, '/wl_setup/form', methods=['POST'])
@util.workflow_permission_required('wl_setup_page')
@util.exception_catcher
def wl_setup_wl_setup_page_form():
    form = GenericFormTemplate()

    # Put form processing code here
    try:
                wl = Whitelistdigest(debug=1)
                wl.set_whitelisturl(form.whitelisturl.data, form.interval.data, form.filters.data)
                flash('success', 'succeed')
    except Exception as err:
                flash(str(err), 'failure')

    return redirect(url_for('wl_setupwl_setup_wl_setup_page'))

@route(app, '/wl_setup/validateurl', methods=['GET', 'POST'])
@util.workflow_permission_required('wl_setup_page')
@util.exception_catcher
def wl_setup_wl_setup_validateurl():
    testurl = str(request.get_json()['url'])
    try:
	wl = Whitelistdigest()
	wl.test_whitelisturl(testurl)
	return jsonify( status='success' )
    except Exception as e:
	print e
	return jsonify( status='failure' )
