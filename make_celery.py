from server import create_app
from decouple import config

flask_app = create_app(as_celery=True)
# flask_app.config.from_mapping(
#     CELERY=dict(
#         BrokenPipeError = config("REDIS_URL"),
#         backend = config("REDIS_URL"),
#     ),
# )
celery_app = flask_app.extensions["celery"]