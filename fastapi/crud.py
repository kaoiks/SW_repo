from sqlalchemy.orm import Session

import models
import schemas


def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()


def get_device(db: Session, device_mac: str):
    return db.query(models.Device).filter(models.Device.device_mac == device_mac).first()


def create_device(db: Session, device: schemas.Device):
    db_device = models.Device(device_mac=device.device_mac, device_ip=device.device_ip, name=device.name)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_rules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rule).offset(skip).limit(limit).all()


def get_rule(db: Session, rule: schemas.Rule):
    return db.query(models.Device).filter(models.Rule.card_id == rule.card_id, models.Rule.reader_mac == rule.reader_mac
                                          , models.Rule.door_mac == rule.door_mac).first()


def create_rule(db: Session, rule: schemas.Rule):
    db_rule = models.Rule(card_id=rule.card_id, reader_mac=rule.reader_mac, door_mac=rule.door_mac)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def create_log(db, log: schemas.Log):
    db_log = models.Log(timestamp=log.timestamp, card_id=log.card_id, reader_mac=log.reader_mac,
                        is_success=log.is_success)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Log).offset(skip).limit(limit).all()
