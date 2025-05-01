#!/usr/bin/env fish

if not status is-interactive
    echo.error "This script is not meant to be run in a non-interactive shell."
    echo.error "Please 'source' it instead of executing the script."
    return
end

if not test -f ".venv"
    read -P "No virtual environment found. Do you want to create one? (y/n): " create_venv
    if test "$create_venv" = y
        read -P "Enter your input: " new_venv_name
        vf new $new_venv_name; and vf connect $new_venv_name
    end
else
    echo ".venv found. Please create a new environment for a new project."
    echo "Delete .venv, deactivate the virtualenv, and source the script again."
end

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete; and find . -path "*/migrations/*.pyc" -delete
rm -rf ./db.sqlite3

poetry install
bun i
bunx tailwindcss -i ./static/src/input.css -o ./static/src/output.css

python ./manage.py compress --force

python ./manage.py makemigrations core accounts; and python ./manage.py migrate
python ./manage.py collectstatic --noinput
git init
git add .
git commit -m "Initial commit"
python ./manage.py createsuperuser --username admin --email admin@localhost.home
