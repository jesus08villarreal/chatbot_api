from sqlalchemy import Column, Integer, String, Text
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    named_has = Column(Text)
    foreing_id = Column(Integer)
