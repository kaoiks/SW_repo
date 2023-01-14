from flask_wtf import FlaskForm, Form
from wtforms import StringField, SelectField, SubmitField, IntegerField,validators
from wtforms.validators import DataRequired
from application import db, app
from wtforms_sqlalchemy.fields import QuerySelectField
from application.models import Device


class DeviceDataForm(FlaskForm):
    device_mac = StringField('MAC', [validators.input_required(), validators.MacAddress()])
    device_ip = StringField('IP',[validators.input_required(), validators.IPAddress()])
    name = StringField('Description')
    submit = SubmitField('Submit')


def readers_mac_choices():
    #return db.session.query(Device.device_mac).all()
    return Device.query

def doors_mac_choices():
    #return db.session.query(Device.device_mac).all()
    return Device.query

class RuleDataForm(FlaskForm):
    card_id = StringField('Cart ID', [validators.input_required()])
    reader_mac = QuerySelectField('Reader', query_factory=readers_mac_choices, get_label=lambda s : '%s %s' % (s.device_mac, s.name) if (s.name!="") else s.device_mac)
    # reader_mac = StringField('Reader')
    door_mac = QuerySelectField('Door', query_factory=doors_mac_choices, get_label=lambda s : '%s %s' % (s.device_mac, s.name) if (s.name!="") else s.device_mac)
    submit = SubmitField('Submit')

class DeviceEditForm(FlaskForm):
    edit_name = StringField('Description')
    submit = SubmitField('Submit')
