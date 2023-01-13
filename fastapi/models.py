from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Identity
from sqlalchemy.orm import relationship, validates, backref

from database import Base


class Device(Base):
    __tablename__ = "devices"

    device_mac = Column(Text, primary_key=True, index=True)
    device_ip = Column(Text, index=True)
    name = Column(Text, default="")


class Rule(Base):
    __tablename__ = "rules"
    rule_id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    card_id = Column(Text, index=True)
    reader_mac = Column(Text, ForeignKey('devices.device_mac',
                                         name='device_relation_reader_mac_fk', ondelete="cascade", onupdate="cascade"),
                        nullable=False)

    reader = relationship("Device", backref=backref("readers"), foreign_keys=[reader_mac])
    door_mac = Column(Text, ForeignKey('devices.device_mac',
                                         name='device_relation_door_mac_fk', ondelete="cascade", onupdate="cascade"),
                      nullable=False)
    door = relationship("Device", backref=backref("doors"), foreign_keys=[door_mac])


class Log(Base):
    __tablename__ = "logs"
    log_id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    timestamp = Column(Integer)
    card_id = Column(Text)
    reader_mac = Column(Text, ForeignKey('devices.device_mac'), nullable=False)
    device_reader = relationship("Device", foreign_keys=[reader_mac])
    is_success = Column(Integer)

    @validates('is_success')
    def validate_success(self, key, value):
        if not 0 <= value < 2:
            raise ValueError(f'Invalid success {value}')
        return value
