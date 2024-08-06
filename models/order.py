from pydantic import BaseModel

class Order(BaseModel):
    id: int
    client_id: int
    order_date: str
    delivery_date: str
    delivery_time: str
    location: str
    confirmation_status: str

    class Config:
        from_attributes = True
