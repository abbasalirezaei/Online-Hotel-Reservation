import redis
from django.conf import settings

# Create a single, reusable Redis client instance from the connection URL in the project settings.
# `decode_responses=True` ensures that the client returns strings instead of bytes,
# which is generally more convenient for application logic.
redis_client = redis.from_url(settings.CELERY_BROKER_URL, decode_responses=True)
# The `redis_client` can now be used throughout the application to interact with Redis.