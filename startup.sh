#!/bin/bash

rm -rf ./db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc" -delete

pip install -r requirements.txt
bun i
bunx tailwindcss -i ./static/src/input.css -o ./static/src/output.css

python ./manage.py compress --force

python ./manage.py makemigrations core accounts && python ./manage.py migrate
python ./manage.py collectstatic --noinput

rm -rf .git
git init
git add .
git commit -m "Initial commit"
python ./manage.py createsuperuser --username admin --email admin@localhost
