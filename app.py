from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from database import init_db, save_order, get_orders
from openai_client import generate_response
import uvicorn
import re
import json

app = FastAPI()


async def startup():
    init_db()

app.add_event_handler("startup", startup)

@app.post('/whatsapp')
async def whatsapp(Body: str = Form(...)):
    incoming_msg = Body.lower()
    response = MessagingResponse()
    msg = response.message()
    gpt_response = generate_response(f"Extract the items and quantities from this order: {incoming_msg}")

    # Hacemos un json con el texto de la respuesta
    try:
        gpt_response = json.loads(gpt_response)
    except:
        msg.body("No pude entender tu pedido. Por favor, inténtalo nuevamente1.")
        return Response(content=str(response), media_type="text/xml")
    # Si es un json y tiene la estructura correcta, procesamos el pedido
    if type(gpt_response) == dict and "item" in gpt_response:
        processed_order = process_order(gpt_response)
        if processed_order:
            msg.body(f"Pedido registrado: {processed_order}")
        else:
            msg.body("No pude entender tu pedido. Por favor, inténtalo nuevamente2.")
        return Response(content=str(response), media_type="text/xml")

    processed_order = process_order(gpt_response)

    if processed_order:
        msg.body(f"Pedido registrado: {processed_order}")
    else:
        msg.body("No pude entender tu pedido. Por favor, inténtalo nuevamente3.")
    return Response(content=str(response), media_type="text/xml")

@app.get('/orders')
async def orders():
    orders = get_orders()
    return orders

def process_order(orders):
    # Guardamos el pedido en la base de datos
    for order in orders["items"]:
        print(order)
        save_order(order)
        

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)