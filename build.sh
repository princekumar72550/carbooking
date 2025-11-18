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

# Add more cars and drivers
python manage.py add_more_cars_drivers

# Assign sample images to cars and drivers
python manage.py add_sample_images

# Create cache table for database caching (if using database cache)
# python manage.py createcachetable