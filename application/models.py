from application import db



class Device(db.Model):
    __tablename__ = "devices"

    device_mac = db.Column(db.Text, primary_key=True, index=True)
    device_ip = db.Column(db.Text, index=True)
    name = db.Column(db.Text,  default="")



class Rule(db.Model):
    __tablename__ = "rules"
    rule_id = db.Column(db.Integer, db.Identity(start=1, cycle=True), primary_key=True)
    card_id = db.Column(db.Text, index=True)
    reader_mac = db.Column(db.Text, db.ForeignKey('devices.device_mac',
                                         name='device_relation_reader_mac_fk', ondelete="cascade", onupdate="cascade"),
                        nullable=False)

    reader = db.relationship("Device", backref=db.backref("readers"), foreign_keys=[reader_mac])
    door_mac = db.Column(db.Text, db.ForeignKey('devices.device_mac',
                                         name='device_relation_door_mac_fk', ondelete="cascade", onupdate="cascade"),
                      nullable=False)
    door = db.relationship("Device", backref=db.backref("doors"), foreign_keys=[door_mac])
    def __repr__(self):
        return format(self.reader_mac)


class Log(db.Model):
    __tablename__ = "logs"
    log_id = db.Column(db.Integer, db.Identity(start=1, cycle=True), primary_key=True)
    timestamp = db.Column(db.Integer)
    card_id = db.Column(db.Text)
    reader_mac = db.Column(db.Text, db.ForeignKey('devices.device_mac'), nullable=False)
    device_reader = db.relationship("Device", foreign_keys=[reader_mac])
    is_success = db.Column(db.Integer)

    @db.validates('is_success')
    def validate_success(self, key, value):
        if not 0 <= value < 2:
            raise ValueError(f'Invalid success {value}')
        return value