from fastapi import APIRouter, Form, Depends
from controllers.whatsapp_controller import whatsapp
import sqlite3
from database import get_db

router = APIRouter()

@router.post("/whatsapp")
async def receive_whatsapp(Body: str = Form(...), From: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    print(f"Received message from {From}: {Body}")
    return whatsapp(Body, From, db)
