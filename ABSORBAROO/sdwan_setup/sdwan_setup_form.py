# Copyright 2018 BlueCat Networks. All rights reserved.

import datetime

from wtforms import StringField, PasswordField, FileField
from wtforms import BooleanField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, MacAddress, URL
from bluecat.wtform_extensions import GatewayForm
from bluecat.wtform_fields import Configuration, CustomStringField, IP4Address, CustomSubmitField


class GenericFormTemplate(GatewayForm):
    # When updating the form, remember to make the corresponding changes to the workflow pages
    workflow_name = 'sdwan_setup'
    workflow_permission = 'sdwan_setup_page'

    key = CustomStringField(
        label='SDWAN API Key',
        default='',
	is_disabled_on_start=False,
        required=True
    )

    orgname = CustomStringField(
        label='Meraki Organization Name',
        default='',
	is_disabled_on_start=False,
        required=True
    )

    templatename = CustomStringField(
        label='Meraki Template Name',
        default='',
	is_disabled_on_start=False,
        required=True
    )

    submit = CustomSubmitField(
	label='Save settings',
	is_disabled_on_start=True
    )
