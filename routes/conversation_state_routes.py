from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import controllers.conversation_state_controller as conversation_state_controller

router = APIRouter()

@router.post("/conversation_state/", response_model=schemas.ConversationState)
def create_or_update_conversation_state(from_number: str, state: schemas.ConversationStateUpdate, db: Session = Depends(get_db)):
    return conversation_state_controller.create_or_update_conversation_state(from_number, state, db)

@router.get("/conversation_state/{from_number}", response_model=schemas.ConversationState)
def read_conversation_state(from_number: str, db: Session = Depends(get_db)):
    db_state = conversation_state_controller.get_conversation_state(from_number, db)
    if db_state is None:
        raise HTTPException(status_code=404, detail="Conversation state not found")
    return db_state

@router.delete("/conversation_state/{from_number}", response_model=schemas.ConversationState)
def reset_conversation_state(from_number: str, db: Session = Depends(get_db)):
    return conversation_state_controller.reset_conversation_state(from_number, db)
