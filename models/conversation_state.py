from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
import datetime

class ConversationState(Base):
    __tablename__ = "conversation_states"

    id = Column(Integer, primary_key=True, index=True)
    from_number = Column(String, unique=True, index=True)
    menu_selected = Column(Boolean, default=False)
    operation = Column(String, nullable=True)
    client_selected = Column(Boolean, default=False)
    selected_client = Column(Integer, nullable=True)
    products_selected = Column(Boolean, default=False)
    order_confirmed = Column(Boolean, default=False)
    selected_products = Column(String, nullable=True)
    delivery_date = Column(String, nullable=True)
    delivery_time = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
