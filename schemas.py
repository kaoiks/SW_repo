from pydantic import BaseModel


class Device(BaseModel):
    device_mac: str
    device_ip: str
    name: str
    class Config:
        orm_mode = True


class ResponseRule(BaseModel):
    rule_id: int
    card_id: str
    reader_mac: str
    door_mac: str

    class Config:
        orm_mode = True


class Rule(BaseModel):
    card_id: str
    reader_mac: str
    door_mac: str

    class Config:
        orm_mode = True


class Log(BaseModel):
    timestamp: int
    card_id: str
    reader_mac: str
    is_success: int

    class Config:
        orm_mode = True
