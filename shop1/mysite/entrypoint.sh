#!/bin/sh

set -e

echo "Starting application"

echo "Applaying migrations"
python manage.py migrate --noinput

echo "Collect static"
python manage.py collectstatic --noinput
#docker logs

if [ "$RESTORE_DUMP" = "true" ] || [ "$RESTORE_DUMP" = "1" ]; then
  if [ -f "$DUMP_FILE" ]; then
  echo "found dump file: $DUMP_FILE"
  echo "Restoring data from dump"

  python manage.py loaddata "$DUMP_FILE"

  echo "Dump succesfully loaded"
  else
  echo "Restore_DUMP = true but dump no found"
  fi
else
  echo "Restore dump skipped"
fi

echo "App is ready!"

exec "$@"