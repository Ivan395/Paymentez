#!/bin/bash

sleep 10

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Create default superuser
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

# Start server
echo "Starting server"
python manage.py runserver "$HOST":"$PORT"
