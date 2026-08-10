#!/bin/sh

set -e

echo "=========================================="
echo " Updating Django translations"
echo "=========================================="

LANGUAGES="ur ja ar"

for LANGUAGE in $LANGUAGES
do
    echo "Updating $LANGUAGE translations..."
    uv run python manage.py makemessages -l "$LANGUAGE"
done

echo "Compiling translations..."

uv run python manage.py compilemessages

echo "=========================================="
echo " Translation update completed successfully"
echo "=========================================="