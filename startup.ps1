# Remove database file
Remove-Item -Path ".\db.sqlite3" -Force -ErrorAction SilentlyContinue

# Remove migration files except __init__.py and .pyc files
Get-ChildItem -Path . -Recurse -Include *.py | Where-Object { $_.FullName -match "migrations" -and $_.Name -ne "__init__.py" } | Remove-Item -Force
Get-ChildItem -Path . -Recurse -Include *.pyc | Where-Object { $_.FullName -match "migrations" } | Remove-Item -Force

# Install Python requirements
poetry env use 3.12
poetry install

# Install bun dependencies
bun i

# Build Tailwind CSS
bun x tailwindcss -i .\static\src\input.css -o .\static\src\output.css

# Compress static files
python .\manage.py compress --force

# Make migrations and migrate
python .\manage.py makemigrations core accounts
python .\manage.py migrate

# Create superuser
python .\manage.py createsuperuser --username admin --email admin@localhost

# Collect static files
python .\manage.py collectstatic --noinput

# Reinitialize git repository
Remove-Item -Path ".git" -Recurse -Force -ErrorAction SilentlyContinue
git init
git add .
git commit -m "Initial commit"
