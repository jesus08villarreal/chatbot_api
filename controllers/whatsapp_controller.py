from fastapi import Form, Depends, HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from database import get_db
from utils.openai_client import select_client, select_products
import sqlite3
import json

# Variable global para almacenar el estado de la conversación
conversation_state = {
    "client_selected": False,
    "selected_client": None,
    "products_selected": False,
    "order_confirmed": False,
    "selected_products": None
}


def reset_conversation_state():
    conversation_state["client_selected"] = False
    conversation_state["selected_client"] = None
    conversation_state["products_selected"] = False
    conversation_state["order_confirmed"] = False
    conversation_state["selected_products"] = None

def whatsapp(Body: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    incoming_msg = Body.lower()
    response = MessagingResponse()
    msg = response.message()

    try:
        with db as conn:
            cursor = conn.cursor()

            # Step 1: Select Client
            if not conversation_state["client_selected"]:
                try:
                    cursor.execute("SELECT id, name, phone, email, address, named_has, foreing_id FROM clients")
                    clients = cursor.fetchall()
                except sqlite3.Error:
                    msg.body("Error al acceder a la base de datos de clientes.")
                    return Response(content=str(response), media_type="text/xml")

                client_dicts = [{"id": client[0], "name": client[1], "phone": client[2], "email": client[3], "address": client[4], "named_has": client[5], "foreing_id": client[6]} for client in clients]

                try:
                    selected_client = select_client(incoming_msg, client_dicts)
                    selected_client = json.loads(selected_client)  # Asegúrate de que la respuesta es JSON
                except Exception:
                    msg.body("Error al procesar la selección de clientes. Intente nuevamente.")
                    return Response(content=str(response), media_type="text/xml")

                if not selected_client:
                    msg.body("No pude encontrar un cliente correspondiente. Por favor, verifica la información.")
                    return Response(content=str(response), media_type="text/xml")

                conversation_state["selected_client"] = selected_client
                msg.body(f"Cliente encontrado: {selected_client['name']}\n¿Es correcto? Responde con 'sí' o 'no'.")
                conversation_state["client_selected"] = True
                return Response(content=str(response), media_type="text/xml")

            # Step 2: Confirm Client
            elif conversation_state["client_selected"] and not conversation_state["products_selected"]:
                if "sí" in incoming_msg or "si" in incoming_msg:
                    conversation_state["products_selected"] = True
                    selected_client = conversation_state["selected_client"]
                    msg.body(f"Cliente confirmado: {selected_client['name']}\nAhora ingresa los productos.")
                    return Response(content=str(response), media_type="text/xml")
                else:
                    msg.body("No se ha confirmado el cliente. Por favor, verifica la información, se reiniciará el proceso.")
                    reset_conversation_state()
                    return Response(content=str(response), media_type="text/xml")

            # Step 3: Select Products
            elif conversation_state["products_selected"] and not conversation_state["order_confirmed"]:
                selected_client = conversation_state["selected_client"]

                try:
                    cursor.execute("SELECT id, name, description, named_has, foreing_id FROM products")
                    products = cursor.fetchall()
                except sqlite3.Error:
                    msg.body("Error al acceder a la base de datos de productos.")
                    return Response(content=str(response), media_type="text/xml")

                product_dicts = [{"id": product[0], "name": product[1], "description": product[2], "named_has": product[3], "foreing_id": product[4]} for product in products]

                try:
                    selected_products = select_products(incoming_msg, product_dicts)
                    selected_products = json.loads(selected_products)

                    if "selected_products" not in selected_products:
                        raise Exception("Error al procesar la selección de productos. Intente nuevamente.")
                    else:
                        selected_products = selected_products["selected_products"]

                except Exception as e:
                    print(e)
                    msg.body("Error al procesar la selección de productos. Intente nuevamente.")
                    return Response(content=str(response), media_type="text/xml")

                if not selected_products:
                    msg.body("No pude encontrar productos correspondientes. Por favor, verifica la información.")
                    return Response(content=str(response), media_type="text/xml")

                print(selected_products)
                conversation_state["selected_products"] = selected_products
                msg.body(f"Productos seleccionados: {[product['name'] for product in selected_products]}\n¿Deseas confirmar el pedido? Responde con 'sí' o 'no'.")
                conversation_state["order_confirmed"] = True
                return Response(content=str(response), media_type="text/xml")

            # Step 4: Confirm Order
            elif conversation_state["order_confirmed"]:
                if "sí" in incoming_msg or "si" in incoming_msg:
                    selected_client = conversation_state["selected_client"]
                    selected_products = conversation_state["selected_products"]

                    try:
                        cursor.execute("INSERT INTO orders (client_id, order_date, delivery_date, delivery_time, location, confirmation_status) VALUES (?, ?, ?, ?, ?, ?)",
                                       (selected_client['id'], "hoy", "pronto", "pronto", "dirección", "confirmado"))
                        order_id = cursor.lastrowid
                        for product in selected_products:
                            cursor.execute("INSERT INTO order_details (order_id, product_id, quantity) VALUES (?, ?, ?)",
                                           (order_id, product['id'], product['quantity']))  # Ajusta la cantidad según sea necesario
                        conn.commit()
                        # Send confirmation message to the client
                        client_phone = selected_client['phone']
                        confirmation_message = "¡Gracias por tu pedido! Hemos recibido tu solicitud y estamos procesándola. Te contactaremos pronto con los detalles de entrega. ¡Que tengas un excelente día!"
                        msg = client.messages.create(
                            body=confirmation_message,
                            from_="your_twilio_phone_number",
                            to=client_phone
                        )
                    except sqlite3.Error:
                        msg.body("Error al registrar el pedido en la base de datos.")
                        return Response(content=str(response), media_type="text/xml")

                    msg.body("Pedido registrado con éxito.")
                    reset_conversation_state()
                    return Response(content=str(response), media_type="text/xml")
                else:
                    msg.body("No se ha confirmado el pedido. Por favor, verifica la información.")
                    conversation_state["order_confirmed"] = False
                    return Response(content=str(response), media_type="text/xml")

    except sqlite3.Error:
        msg.body("Error en la conexión a la base de datos.")
    
    return Response(content=str(response), media_type="text/xml")
