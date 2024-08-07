from sqlalchemy import Column, Integer, String, Text
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String)
    named_has = Column(Text)
    foreing_id = Column(Integer)

