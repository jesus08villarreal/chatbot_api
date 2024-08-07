from fastapi import Form, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from database import get_db
from utils.openai_client import select_client, select_products, extract_date_time
import json
import os
import datetime
import pandas as pd
import controllers.client_controller as client_controller
import controllers.order_controller as order_controller
import controllers.product_controller as product_controller
import controllers.conversation_state_controller as conversation_state_controller
import schemas

# Configuración de Twilio
twilio_client = TwilioClient(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

def whatsapp(Body: str = Form(...), From: str = Form(...), db: Session = Depends(get_db)):
    print("Received message from: ", From)
    print(Body)
    print(From)
    incoming_msg = Body.lower()
    response = MessagingResponse()
    msg = response.message()

    conversation_state = conversation_state_controller.get_conversation_state(From, db)
    if not conversation_state:
        conversation_state = conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateCreate(from_number=From), db)

    try:
        # Main Menu
        if not conversation_state.menu_selected or incoming_msg == "menu":
            msg.body("Hola! ¿Qué te gustaría hacer hoy?\n1. Crear un pedido\n2. Descargar pedidos del dia\n3. Actualizar información del cliente\nResponde con el número de la opción.")
            conversation_state.menu_selected = True
            conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
            return Response(content=str(response), media_type="text/xml")

        # Handle Menu Selection
        if conversation_state.menu_selected and not conversation_state.operation:
            if incoming_msg == "1":
                conversation_state.operation = "crear_pedido"
                msg.body("Has seleccionado 'Crear un pedido'. Por favor, ingresa el nombre o información del cliente.")
            elif incoming_msg == "2":
                conversation_state.operation = "descargar_pedidos"
                today = datetime.date.today()
                orders = order_controller.get_orders_by_date(db, today)
                if not orders:
                    msg.body("No hay pedidos registrados para hoy.")
                    conversation_state.operation = None
                    conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
                    return Response(content=str(response), media_type="text/xml")
                
                orders_message = "\n".join([f"ID: {order.id}\nCliente: {order.client_id}\nFecha de entrega: {order.delivery_date} - {order.delivery_time}\nEstado: {order.confirmation_status}\n" for order in orders])
                msg.body(f"Pedidos del día {today}:\n\n{orders_message}")
                conversation_state.operation = None
                conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
                return Response(content=str(response), media_type="text/xml")
            elif incoming_msg == "3":
                conversation_state.operation = "actualizar_cliente"
                msg.body("Has seleccionado 'Actualizar información del cliente'. Por favor, ingresa el nombre o información del cliente.")
            else:
                msg.body("Opción no válida. Por favor, responde con el número de la opción deseada.")
                return Response(content=str(response), media_type="text/xml")
            conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
            return Response(content=str(response), media_type="text/xml")

        # Crear Pedido Flow
        if conversation_state.operation == "crear_pedido":
            # Step 1: Select Client
            if not conversation_state.client_selected:
                clients = client_controller.get_clients(db)
                client_dicts = [{"id": client.id, "name": client.name, "phone": client.phone, "email": client.email, "address": client.address, "named_has": client.named_has, "foreing_id": client.foreing_id} for client in clients]

                try:
                    selected_client = select_client(incoming_msg, client_dicts)
                    selected_client = json.loads(selected_client)  # Asegúrate de que la respuesta es JSON
                except Exception:
                    msg.body("Error al procesar la selección de clientes. Intente nuevamente.")
                    return Response(content=str(response), media_type="text/xml")

                if not selected_client:
                    msg.body("No pude encontrar un cliente correspondiente. Por favor, verifica la información.")
                    return Response(content=str(response), media_type="text/xml")

                conversation_state.selected_client = selected_client['id']
                msg.body(f"Cliente encontrado: {selected_client['name']}\n¿Es correcto? Responde con 'sí' o 'no'.")
                conversation_state.client_selected = True
                conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
                return Response(content=str(response), media_type="text/xml")

            # Step 2: Confirm Client
            elif conversation_state.client_selected and not conversation_state.delivery_date:
                if "sí" in incoming_msg or "si" in incoming_msg:
                    selected_client = conversation_state.selected_client
                    client_info = client_controller.get_client(db, selected_client)
                    client_info_message = f"Nombre: {client_info.name}\nTeléfono: {client_info.phone}\nEmail: {client_info.email}\nDirección: {client_info.address}\nID Externo: {client_info.foreing_id}"
                    msg.body(f"Cliente confirmado: {client_info.name}\n{client_info_message}\n¿Cuándo deseas la entrega? Por favor, ingresa la fecha y hora.")
                    conversation_state.delivery_date = "pronto"
                    conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
                    return Response(content=str(response), media_type="text/xml")
                else:
                    msg.body("No se ha confirmado el cliente. Por favor, verifica la información, se reiniciará el proceso.")
                    conversation_state_controller.reset_conversation_state(From, db)
                    return Response(content=str(response), media_type="text/xml")

            # Step 3: Extract Date/Time
            elif conversation_state.delivery_date and not conversation_state.products_selected:
                try:
                    print(incoming_msg)
                    delivery_info = extract_date_time(incoming_msg)
                    print(delivery_info)
                    delivery_info = json.loads(delivery_info)
                    print(delivery_info)
                    conversation_state.delivery_date = delivery_info.get("delivery_date", "pronto")
                    conversation_state.delivery_time = delivery_info.get("delivery_time", "pronto")

                    if not conversation_state.delivery_date or not conversation_state.delivery_time:
                        raise Exception("Error al procesar la fecha y hora de entrega. Intente nuevamente.")

                    msg.body(f"Fecha de entrega: {conversation_state.delivery_date}\nHora de entrega: {conversation_state.delivery_time}\nAhora ingresa los productos.")
                    conversation_state.products_selected = True
                    conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
                    return Response(content=str(response), media_type="text/xml")
                except Exception as e:
                    print(e)
                    msg.body("Error al procesar la fecha y hora de entrega. Intente nuevamente.")
                    return Response(content=str(response), media_type="text/xml")

            # Step 4: Select Products
            elif conversation_state.products_selected and not conversation_state.order_confirmed:
                selected_client = conversation_state.selected_client

                products = product_controller.get_products(db)
                product_dicts = [{"id": product.id, "name": product.name, "description": product.description, "named_has": product.named_has, "foreing_id": product.foreing_id} for product in products]

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
                client_info = client_controller.get_client(db, selected_client)
                conversation_state.selected_products = json.dumps(selected_products)
                products_message = "\n".join([f"{product['name']} - Cantidad: {product['quantity']}" for product in selected_products])
                msg.body(f"Productos seleccionados:\n{products_message}\n\nResumen del pedido:\n\nCliente:\n{client_info.name}\nTeléfono: {client_info.phone}\nEmail: {client_info.email}\nDirección: {client_info.address}\nID Externo: {client_info.foreing_id}\n\nFecha de entrega: {conversation_state.delivery_date}\nHora de entrega: {conversation_state.delivery_time}\n\n¿Deseas confirmar el pedido? Responde con 'sí' o 'no'.")
                conversation_state.order_confirmed = True
                conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
                return Response(content=str(response), media_type="text/xml")

            # Step 5: Confirm Order
            elif conversation_state.order_confirmed:
                if "sí" in incoming_msg or "si" in incoming_msg:
                    selected_client = conversation_state.selected_client
                    selected_products = json.loads(conversation_state.selected_products)

                    try:
                        order = order_controller.create_order(
                            schemas.OrderCreate(
                                client_id=selected_client,
                                order_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                                delivery_date=conversation_state.delivery_date,
                                delivery_time=conversation_state.delivery_time,
                                location="dirección"
                            ), db)
                        print(order)
                        for product in selected_products:
                            order_detail = order_controller.create_order_detail(
                                schemas.OrderDetailCreate(
                                    order_id=order.id,
                                    product_id=product['id'],
                                    quantity=product['quantity']
                                ), db)
                            print(order_detail.id)
                        # Send confirmation message to the client
                        client_info = client_controller.get_client(db, selected_client)
                        client_phone = client_info.phone
                        products_message = "\n".join([f"{product['name']} - Cantidad: {product['quantity']}" for product in selected_products])
                        confirmation_message = (
                            f"¡Gracias por tu pedido!\n\nResumen del pedido:\n\nCliente:\n{client_info.name}\n"
                            f"Teléfono: {client_info.phone}\nEmail: {client_info.email}\nDirección: {client_info.address}\n"
                            f"ID Externo: {client_info.foreing_id}\n\nProductos:\n{products_message}\n\n"
                            f"Fecha de entrega: {conversation_state.delivery_date}\nHora de entrega: {conversation_state.delivery_time}\n\n"
                            "Hemos recibido tu solicitud y estamos procesándola. Te contactaremos pronto con los detalles de entrega. ¡Que tengas un excelente día!"
                        )
                        print(confirmation_message)
                        # message = twilio_client.messages.create(
                        #     body=confirmation_message,
                        #     from_="whatsapp:{}".format(os.getenv("TWILIO_PHONE_NUMBER")),
                        #     to="whatsapp:{}".format(client_phone)
                        # )
                        # print(message.sid)
                    except Exception as e:
                        print(e)
                        msg.body("Error al registrar el pedido en la base de datos.")
                        return Response(content=str(response), media_type="text/xml")

                    msg.body("Pedido registrado con éxito.")
                    conversation_state_controller.reset_conversation_state(From, db)
                    return Response(content=str(response), media_type="text/xml")
                else:
                    msg.body("No se ha confirmado el pedido. Por favor, verifica la información.")
                    conversation_state.order_confirmed = False
                    conversation_state_controller.create_or_update_conversation_state(From, schemas.ConversationStateUpdate(**conversation_state.__dict__), db)
                    return Response(content=str(response), media_type="text/xml")

    except Exception as e:
        print(e)
        msg.body("Error en la conexión a la base de datos.")
    
    return Response(content=str(response), media_type="text/xml")
