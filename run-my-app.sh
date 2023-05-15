#!/bin/sh
python /code/manage.py collectstatic
python /code/manage.py makemigrations
while :
do
        if python /code/manage.py migrate; then
                break
        else
                sleep 1
        fi
done
gunicorn --bind 0.0.0.0:8000 config.wsgi:application

exit 0
