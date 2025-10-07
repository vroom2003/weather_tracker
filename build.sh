#!/usr/bin/env bash
# Exit on error
set -o errexit

# Create static files directory if it doesn't exist
mkdir -p staticfiles

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Build completed successfully!"