from fastapi import Form, HTTPException, Depends
from twilio.twiml.messaging_response import MessagingResponse
from database import get_db
from utils.openai_client import select_client, select_products
import sqlite3
import json

def whatsapp(Body: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    incoming_msg = Body.lower()
    response = MessagingResponse()
    msg = response.message()
    
    with db as conn:
        cursor = conn.cursor()

        # Obtener todos los clientes de la base de datos
        cursor.execute("SELECT id, name, phone, email, address, named_has, foreing_id FROM clients")
        clients = cursor.fetchall()
        client_dicts = [{"id": client[0], "name": client[1], "phone": client[2], "email": client[3], "address": client[4], "named_has": client[5], "foreing_id": client[6]} for client in clients]

        # Seleccionar el cliente usando OpenAI
        selected_client = select_client(incoming_msg, client_dicts)
        if not selected_client:
            msg.body("No pude encontrar un cliente correspondiente. Por favor, verifica la información.")
            return str(response)

        msg.body(f"Cliente encontrado: {selected_client['name']}\n¿Es correcto? Responde con 'sí' o 'no'.")
        return str(response)