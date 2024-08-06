from fastapi import Form, Depends, HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from database import get_db
from utils.openai_client import select_client, select_products, extract_date_time
import sqlite3
import json
import os
import datetime
import pandas as pd

# Configuración de Twilio
twilio_client = TwilioClient(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

# Variable global para almacenar el estado de la conversación
conversation_state = {
    "menu_selected": False,
    "operation": None,
    "client_selected": False,
    "selected_client": None,
    "products_selected": False,
    "order_confirmed": False,
    "selected_products": None,
    "delivery_date": None,
    "delivery_time": None
}

def reset_conversation_state():
    conversation_state["menu_selected"] = False
    conversation_state["operation"] = None
    conversation_state["client_selected"] = False
    conversation_state["selected_client"] = None
    conversation_state["products_selected"] = False
    conversation_state["order_confirmed"] = False
    conversation_state["selected_products"] = None
    conversation_state["delivery_date"] = None
    conversation_state["delivery_time"] = None

def whatsapp(Body: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    incoming_msg = Body.lower()
    response = MessagingResponse()
    msg = response.message()

    try:
        with db as conn:
            cursor = conn.cursor()

            # Main Menu
            if not conversation_state["menu_selected"] or incoming_msg == "menu":
                msg.body("Hola! ¿Qué te gustaría hacer hoy?\n1. Crear un pedido\n2. Descargar pedidos del dia\n3. Actualizar información del cliente\nResponde con el número de la opción.")
                conversation_state["menu_selected"] = True
                return Response(content=str(response), media_type="text/xml")

            # Handle Menu Selection
            if conversation_state["menu_selected"] and not conversation_state["operation"]:
                if incoming_msg == "1":
                    conversation_state["operation"] = "crear_pedido"
                    msg.body("Has seleccionado 'Crear un pedido'. Por favor, ingresa el nombre o información del cliente.")
                elif incoming_msg == "2":
                    conversation_state["operation"] = "descargar_pedidos"
                    try:
                        today = datetime.date.today()
                        cursor.execute("SELECT * FROM orders WHERE delivery_date = ?", (today,))
                        orders = cursor.fetchall()
                    except sqlite3.Error:
                        msg.body("Error al acceder a la base de datos de pedidos.")
                        return Response(content=str(response), media_type="text/xml")

                    if not orders:
                        msg.body("No hay pedidos registrados.")
                        conversation_state["operation"] = None
                        return Response(content=str(response), media_type="text/xml")
                    
                    orders_dict = [{"id": order[0], "client_id": order[1], "order_date": order[2], "delivery_date": order[3], "delivery_time": order[4], "location": order[5], "confirmation_status": order[6]} for order in orders]

                    # Hacemos un mensaje estructurado con los pedidos del día
                    orders_message = "\n".join([f"ID: {order['id']}\nCliente: {order['client_id']}\nFecha de entrega: {order['delivery_date']} - {order['delivery_time']}\nEstado: {order['confirmation_status']}\n" for order in orders_dict])
                    msg.body(f"Pedidos del día {today}:\n\n{orders_message}")
                    
                    conversation_state["operation"] = None
                elif incoming_msg == "3":
                    conversation_state["operation"] = "actualizar_cliente"
                    msg.body("Has seleccionado 'Actualizar información del cliente'. Por favor, ingresa el nombre o información del cliente.")
                else:
                    msg.body("Opción no válida. Por favor, responde con el número de la opción deseada.")
                    return Response(content=str(response), media_type="text/xml")
                return Response(content=str(response), media_type="text/xml")
            
            # Descargar pedidos del día flow
        


            # Crear Pedido Flow
            if conversation_state["operation"] == "crear_pedido":
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
                elif conversation_state["client_selected"] and not conversation_state["delivery_date"]:
                    if "sí" in incoming_msg or "si" in incoming_msg:
                        selected_client = conversation_state["selected_client"]
                        client_info = f"Nombre: {selected_client['name']}\nTeléfono: {selected_client['phone']}\nEmail: {selected_client['email']}\nDirección: {selected_client['address']}\nID Externo: {selected_client['foreing_id']}"
                        msg.body(f"Cliente confirmado: {selected_client['name']}\n{client_info}\n¿Cuándo deseas la entrega? Por favor, ingresa la fecha y hora.")
                        conversation_state["delivery_date"] = True
                        return Response(content=str(response), media_type="text/xml")
                    else:
                        msg.body("No se ha confirmado el cliente. Por favor, verifica la información, se reiniciará el proceso.")
                        reset_conversation_state()
                        return Response(content=str(response), media_type="text/xml")

                # Step 3: Extract Date/Time
                elif conversation_state["delivery_date"] and not conversation_state["products_selected"]:
                    try:
                        delivery_info = extract_date_time(incoming_msg)
                        delivery_info = json.loads(delivery_info)

                        conversation_state["delivery_date"] = delivery_info.get("delivery_date", "pronto")
                        conversation_state["delivery_time"] = delivery_info.get("delivery_time", "pronto")

                        msg.body(f"Fecha de entrega: {conversation_state['delivery_date']}\nHora de entrega: {conversation_state['delivery_time']}\nAhora ingresa los productos.")
                        conversation_state["products_selected"] = True
                        return Response(content=str(response), media_type="text/xml")
                    except Exception as e:
                        print(e)
                        msg.body("Error al procesar la fecha y hora de entrega. Intente nuevamente.")
                        return Response(content=str(response), media_type="text/xml")

                # Step 4: Select Products
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

                    conversation_state["selected_products"] = selected_products
                    products_message = "\n".join([f"{product['name']} - Cantidad: {product['quantity']}" for product in selected_products])
                    msg.body(f"Productos seleccionados:\n{products_message}\n\nResumen del pedido:\n\nCliente:\n{selected_client['name']}\nTeléfono: {selected_client['phone']}\nEmail: {selected_client['email']}\nDirección: {selected_client['address']}\nID Externo: {selected_client['foreing_id']}\n\nFecha de entrega: {conversation_state['delivery_date']}\nHora de entrega: {conversation_state['delivery_time']}\n\n¿Deseas confirmar el pedido? Responde con 'sí' o 'no'.")
                    conversation_state["order_confirmed"] = True
                    return Response(content=str(response), media_type="text/xml")

                # Step 5: Confirm Order
                elif conversation_state["order_confirmed"]:
                    if "sí" in incoming_msg or "si" in incoming_msg:
                        selected_client = conversation_state["selected_client"]
                        selected_products = conversation_state["selected_products"]

                        try:
                            cursor.execute("INSERT INTO orders (client_id, order_date, delivery_date, delivery_time, location, confirmation_status) VALUES (?, ?, ?, ?, ?, ?)",
                                           (selected_client['id'], "hoy", conversation_state['delivery_date'], conversation_state['delivery_time'], "dirección", "confirmado"))
                            order_id = cursor.lastrowid
                            for product in selected_products:
                                cursor.execute("INSERT INTO order_details (order_id, product_id, quantity) VALUES (?, ?, ?)",
                                               (order_id, product['id'], product['quantity'])) 
                            conn.commit()
                            # Send confirmation message to the client
                            client_phone = selected_client['phone']
                            products_message = "\n".join([f"{product['name']} - Cantidad: {product['quantity']}" for product in selected_products])
                            confirmation_message = (
                                f"¡Gracias por tu pedido!\n\nResumen del pedido:\n\nCliente:\n{selected_client['name']}\n"
                                f"Teléfono: {selected_client['phone']}\nEmail: {selected_client['email']}\nDirección: {selected_client['address']}\n"
                                f"ID Externo: {selected_client['foreing_id']}\n\nProductos:\n{products_message}\n\n"
                                f"Fecha de entrega: {conversation_state['delivery_date']}\nHora de entrega: {conversation_state['delivery_time']}\n\n"
                                "Hemos recibido tu solicitud y estamos procesándola. Te contactaremos pronto con los detalles de entrega. ¡Que tengas un excelente día!"
                            )
                            message = twilio_client.messages.create(
                                body=confirmation_message,
                                from_="whatsapp:{}".format(os.getenv("TWILIO_PHONE_NUMBER")),
                                to="whatsapp:{}".format(client_phone)
                            )
                            print(message.sid)
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

            # Aquí se pueden añadir más operaciones como consultar pedido, actualizar cliente, etc.

    except sqlite3.Error:
        msg.body("Error en la conexión a la base de datos.")
    
    return Response(content=str(response), media_type="text/xml")
