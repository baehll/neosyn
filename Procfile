web: gunicorn app:app
worker: celery -A make_celery.celery_app worker --loglevel=info --concurrency 2