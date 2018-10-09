# Copyright 2018 BlueCat Networks. All rights reserved.

import datetime

from wtforms import StringField, PasswordField, FileField
from wtforms import BooleanField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, MacAddress, URL
from bluecat.wtform_extensions import GatewayForm
from bluecat.wtform_fields import Configuration, CustomStringField, IP4Address, CustomSubmitField


class GenericFormTemplate(GatewayForm):
    # When updating the form, remember to make the corresponding changes to the workflow pages
    workflow_name = 'wl_setup'
    workflow_permission = 'wl_setup_page'
    whitelisturl = CustomStringField(
        label='Whitelist url',
        #default='https://endpoints.office.com/endpoints/o365worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7',
        default='',
        required=True,
        is_disabled_on_start=False,
        validators=[URL()]
    )

    interval = CustomStringField(
        label='Interval in seconds (defaults to 86400, 1 day)',
        default='',
        required=True,
        is_disabled_on_start=False
    )

    filters = CustomStringField(
        label='Filter domains using regex (optional)',
        default='',
        is_disabled_on_start=False
    )

    submit = CustomSubmitField(
        label='Save settings',
        is_disabled_on_start=True
    )

