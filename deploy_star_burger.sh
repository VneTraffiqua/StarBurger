#!/bin/bash

set -e


cd /opt/StarBurger

source .env

git pull origin main

source /opt/StarBurger/venv/bin/activate

pip install -r requirements.txt

python manage.py migrate --noinput

npm ci --dev

./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"

python manage.py collectstatic --noinput

systemctl reload nginx

hash=$(git rev-parse HEAD)

curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$ROLLBAR_TOKEN \
  -F environment=$ROLLBAR_ENVIROMENT \
  -F revision=$hash \
  -F local_username=$USER \
  -F comment="Deployed new version" \
  -F status=succeeded

echo 'Deploy succes'
