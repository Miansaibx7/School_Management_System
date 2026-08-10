#!/bin/sh

set -e

echo "=========================================="
echo " Updating Django translations"
echo "=========================================="

LANGUAGES="en ur ja"

for LANGUAGE in $LANGUAGES
do
    echo "Updating translation: $LANGUAGE"
    python manage.py makemessages -l "$LANGUAGE"
done

echo ""
echo "Compiling translation files..."

python manage.py compilemessages

echo ""
echo "=========================================="
echo " Translation update completed"
echo "=========================================="