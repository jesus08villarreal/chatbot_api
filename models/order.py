from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    order_date = Column(String)
    delivery_date = Column(String)
    delivery_time = Column(String)
    location = Column(String)
    confirmation_status = Column(String)
