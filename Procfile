web: gunicorn plants_app.wsgi --log-file -
celery: celery worker -A plants_app -l info -c 4
