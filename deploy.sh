#!/bin/bash

echo "Iniciando el despliegue en Heroku..."

# Configurar autenticación en Heroku
cat > ~/.netrc <<EOF
machine api.heroku.com
  login $HEROKU_EMAIL
  password $HEROKU_API_KEY
machine git.heroku.com
  login $HEROKU_EMAIL
  password $HEROKU_API_KEY
EOF

# Añadir el remoto de Heroku
heroku git:remote -a jatechbotapi

# Empujar a Heroku
git push heroku master --force

echo "Despliegue completo."
