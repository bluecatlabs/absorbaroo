# Copyright 2018 BlueCat Networks. All rights reserved.

import datetime

from wtforms import StringField, PasswordField, FileField
from wtforms import BooleanField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, MacAddress, URL
from bluecat.wtform_extensions import GatewayForm
from bluecat.wtform_fields import Configuration, CustomStringField, IP4Address, CustomSubmitField


class GenericFormTemplate(GatewayForm):
    # When updating the form, remember to make the corresponding changes to the workflow pages
    workflow_name = 'dns_edge_setup'
    workflow_permission = 'dns_edge_setup_page'

    edgeurl = CustomStringField(
        label='Edge URL',
        default='adbcd.blue.ca.t',
        required=True,
        is_disabled_on_start=False
    )

    edgeusername = CustomStringField(
        label='Username',
        default='e@e.com',
        required=True,
        is_disabled_on_start=False
    )

    edgepassword = PasswordField(
        label='Password'
    )

    dlname = CustomStringField(
        label='Domain List name on DNS Edge',
        required=True,
        is_disabled_on_start=False
    )

    submit = CustomSubmitField(
	label='Save',
        is_disabled_on_start=False
    )
