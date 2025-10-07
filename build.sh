#!/usr/bin/env bash
# Exit on error
set -o errexit

# Create static files directory if it doesn't exist
mkdir -p staticfiles

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Create superuser (optional - remove in production)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'password') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell