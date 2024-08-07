from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.conversation_state import ConversationState as ConversationStateModel
import schemas

def create_or_update_conversation_state(from_number: str, state: schemas.ConversationStateUpdate, db: Session):
    with db as db:
        db_state = db.query(ConversationStateModel).filter(ConversationStateModel.from_number == from_number).first()
        if db_state:
            for key, value in state.model_dump().items():
                setattr(db_state, key, value)
            db.commit()
            db.refresh(db_state)
        else:
            db_state = ConversationStateModel(**state.model_dump())
            db.add(db_state)
            db.commit()
            db.refresh(db_state)
        return db_state

def get_conversation_state(from_number: str, db: Session):
    with db as db:
        return db.query(ConversationStateModel).filter(ConversationStateModel.from_number == from_number).first()

def reset_conversation_state(from_number: str, db: Session):
    with db as db:
        db_state = db.query(ConversationStateModel).filter(ConversationStateModel.from_number == from_number).first()
        if db_state:
            db_state.menu_selected = False
            db_state.operation = None
            db_state.client_selected = False
            db_state.selected_client = None
            db_state.products_selected = False
            db_state.order_confirmed = False
            db_state.selected_products = None
            db_state.delivery_date = None
            db_state.delivery_time = None
            db.commit()
            db.refresh(db_state)
        return db_state
