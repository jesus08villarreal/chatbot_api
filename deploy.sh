#!/bin/bash

echo "Iniciando el despliegue en Heroku..."

# Autenticarse en Heroku usando el API Key
echo "machine api.heroku.com" > ~/.netrc
echo "  login ${HEROKU_EMAIL}" >> ~/.netrc
echo "  password ${HEROKU_API_KEY}" >> ~/.netrc
echo "machine git.heroku.com" >> ~/.netrc
echo "  login ${HEROKU_EMAIL}" >> ~/.netrc
echo "  password ${HEROKU_API_KEY}" >> ~/.netrc

# Añadir el remoto de Heroku y empujar el código
git remote add heroku https://git.heroku.com/jatechbotapi.git
git push heroku master --force

echo "Despliegue completo."
