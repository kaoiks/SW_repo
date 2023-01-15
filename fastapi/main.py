from fastapi import FastAPI
from fastapi import Depends, FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import crud
import models
import schemas
import sqlalchemy.exc
from aws import send_email_alert
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/devices", response_model=schemas.Device)
def create_user(device: schemas.Device, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_mac=device.device_mac)
    if db_device:
        raise HTTPException(status_code=400, detail="Device already exists")
    return crud.create_device(db=db, device=device)


@app.put("/devices")
def update_device(device: schemas.Device, db: Session = Depends(get_db)):
    print(device)
    db_device = crud.get_device(db, device_mac=device.device_mac)
    if db_device:
        db_device.device_ip = device.device_ip
        db.commit()
        return {'message': 'Device updated successfully'}

    raise HTTPException(status_code=404, detail='Device doesn\'t exist')


@app.get("/devices", response_model=list[schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices


@app.post("/rules", response_model=schemas.Rule)
def create_rule(rule: schemas.Rule, db: Session = Depends(get_db)):
    db_rule = crud.get_rule(db, rule=rule)

    if db_rule:
        raise HTTPException(status_code=400, detail="Rule already exists")
    try:
        return crud.create_rule(db=db, rule=rule)
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Reader mac or Door mac doesn't exist")


@app.get("/rules", response_model=list[schemas.Rule])
def read_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rules = crud.get_rules(db, skip=skip, limit=limit)
    return rules


@app.post("/logs", response_model=schemas.Log)
def create_log(log: schemas.Log, db: Session = Depends(get_db)):
    try:
        if log.is_success == 0:
            db_device = crud.get_device(db, device_mac=log.reader_mac)
            send_email_alert(log.reader_mac, db_device.name, log.card_id, datetime.fromtimestamp(log.timestamp).strftime("%d/%m/%Y, %H:%M:%S"))
        return crud.create_log(db=db, log=log)
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail="")


@app.get("/logs", response_model=list[schemas.Log])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = crud.get_logs(db, skip=skip, limit=limit)
    return logs
