#!/bin/sh
set -e
if [ -n "$DJANGO_DATA_DIR" ]; then
  mkdir -p "$DJANGO_DATA_DIR/media" "$DJANGO_DATA_DIR/logs"
fi
python manage.py migrate --noinput
exec python manage.py runserver 0.0.0.0:8000