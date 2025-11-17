#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Populate demo data
python manage.py populate_demo_data

# Assign sample images to cars and drivers
python manage.py add_sample_images