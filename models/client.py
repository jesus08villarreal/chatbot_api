from pydantic import BaseModel

class Client(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    address: str
    named_has: str
    foreing_id: int

    class Config:
        from_attributes = True
