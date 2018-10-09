# Copyright 2018 BlueCat Networks. All rights reserved.

import datetime

from wtforms import StringField, PasswordField, FileField
from wtforms import BooleanField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, MacAddress, URL
from bluecat.wtform_extensions import GatewayForm
from bluecat.wtform_fields import Configuration, CustomStringField, IP4Address, CustomSubmitField


class GenericFormTemplate(GatewayForm):
    # When updating the form, remember to make the corresponding changes to the workflow pages
    workflow_name = 'test_sync'
    workflow_permission = 'test_sync_page'

    interval = CustomStringField(
	label='Last synced at:',
	is_disabled_on_start=True
    )

    edge_result = CustomStringField(
        label='Edge Sync - domains added',
	is_disabled_on_start=True
    )

    sdwan_result = CustomStringField(
        label='Meraki Sync - rules added',
	is_disabled_on_start=True
    )

    sync_now = CustomSubmitField(
	label='Sync Now',
	is_disabled_on_start=False
    )

