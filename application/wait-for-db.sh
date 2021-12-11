#!/bin/bash
# wait-for-grid.sh

set -e

cmd="$@"

echo "Waiting for postgres..."
SQL_HOST="database"
SQL_PORT=5432
while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.5
done

echo "PostgreSQL started"

echo "App started succesfully"
exec $cmd