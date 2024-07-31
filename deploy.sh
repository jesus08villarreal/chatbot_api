#!/bin/bash

# Ejemplo de script de despliegue
# Esto puede ser tan complejo como necesites, dependiendo de tu entorno de despliegue

echo "Desplegando la aplicación..."

# Conéctate a tu servidor y despliega la aplicación
ssh -o StrictHostKeyChecking=no user@your-server-ip << 'ENDSSH'
cd /ruta/a/tu/aplicacion
git pull origin master
pip install -r requirements.txt
# Parar el proceso anterior si es necesario
pkill -f 'uvicorn app:app'
# Iniciar el nuevo proceso
nohup uvicorn app:app --host 0.0.0.0 --port 8000 &
ENDSSH

echo "Despliegue completo."
##