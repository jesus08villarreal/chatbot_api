# Guaxuco Chatbot API

## Descripción

Guaxuco Chatbot API es una solución automatizada diseñada para gestionar pedidos de productos a través de WhatsApp. Utiliza tecnologías avanzadas de procesamiento de lenguaje natural y servicios de mensajería para facilitar y mejorar la experiencia del cliente.

## Problema Identificado

El proceso manual de toma de pedidos a través de WhatsApp puede ser lento y propenso a errores. Además, la falta de una integración eficiente con sistemas de gestión y bases de datos complica el seguimiento y la organización de los pedidos.

## Solución

Guaxuco Chatbot API automatiza el proceso de toma de pedidos, permitiendo a los clientes realizar sus pedidos a través de WhatsApp de manera rápida y eficiente. La API está integrada con una base de datos para gestionar clientes y productos, y utiliza OpenAI para interpretar y procesar los mensajes de los clientes.

## Arquitectura

- **Frontend**: WhatsApp (interfaz de usuario)
- **Backend**: FastAPI
- **Base de Datos**: SQLite
- **Mensajería**: Twilio API
- **Procesamiento de Lenguaje Natural**: OpenAI

## Tabla de Contenidos

1. [Requerimientos](#requerimientos)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso](#uso)
5. [Contribución](#contribución)
6. [Roadmap](#roadmap)

## Requerimientos

### Servidores

- **Servidor de Aplicación**: Heroku
- **Base de Datos**: SQLite

### Paquetes Adicionales

- `fastapi`
- `uvicorn`
- `twilio`
- `spacy`
- `pandas`
- `python-dotenv`
- `openai`
- `boto3`
- `botocore`

### Versiones

- **Python**: 3.8 o superior

## Instalación

### ¿Cómo instalar el ambiente de desarrollo?
Clona el repositorio:
  
   `git clone https://github.com/jesus08villarreal/guaxuco_chatbot_api.git`
   `cd guaxuco_chatbot_api`
Crea y activa un entorno virtual:

```sh
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```
Instala las dependencias:

```sh
pip install -r requirements.txt
```
¿Cómo ejecutar pruebas manualmente?
Inicia el servidor local:

```sh
uvicorn main:app --reload
```
Usa herramientas como curl o Postman para enviar solicitudes a la API.

¿Cómo implementar la solución en producción en un ambiente local o en la nube como Heroku?
Instala Heroku CLI y autentícate:

```sh
heroku login
```
Crea una aplicación en Heroku:

```sh
heroku create nombre-de-tu-aplicacion
```
Despliega la aplicación:

```sh
git push heroku master
```
Configura las variables de entorno en Heroku:

```sh
heroku config:set TWILIO_ACCOUNT_SID=tu_account_sid
heroku config:set TWILIO_AUTH_TOKEN=tu_auth_token
heroku config:set TWILIO_PHONE_NUMBER=tu_phone_number
heroku config:set OPENAI_API_KEY=tu_openai_api_key
heroku config:set HEROKU_APP_URL=https://tu-aplicacion.herokuapp.com
```

## Configuración
Configuración del Producto
Archivo .env: contiene las claves y tokens necesarios para la integración con Twilio y OpenAI.
Configuración de los Requerimientos
Twilio: Configura la cuenta de Twilio y el número de WhatsApp.
OpenAI: Configura la API Key de OpenAI en el archivo .env.

## Uso
Sección de Referencia para Usuario Final
Los usuarios pueden interactuar con el chatbot enviando mensajes a través de WhatsApp. El chatbot guiará al usuario a través del proceso de toma de pedidos.

Sección de Referencia para Usuario Administrador
Los administradores pueden gestionar los clientes y productos a través de la base de datos y realizar consultas sobre el estado de los pedidos.

## Contribución
Guía de Contribución para Usuarios
Clona el repositorio:

```sh
git clone https://github.com/jesus08villarreal/guaxuco_chatbot_api.git
```
Crea un nuevo branch:

```sh
git checkout -b nombre-del-branch
```
Realiza tus cambios y haz commit:

```sh
git commit -am "Descripción de los cambios"
```
Envía el branch a GitHub:

```sh
git push origin nombre-del-branch
```
