from server import create_app
from decouple import config

flask_app = create_app()
flask_app.config.from_mapping(
    CELERY=dict(
        broker_url = config("REDIS_URL"),
        result_backend = config("REDIS_URL"),
    ),
)
celery_app = flask_app.extensions["celery"]