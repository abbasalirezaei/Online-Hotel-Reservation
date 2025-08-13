import redis
from django.conf import settings

# Create a Redis client using the project's settings
redis_client = redis.from_url(settings.CELERY_BROKER_URL, decode_responses=True)

# You can now use `redis_client` anywhere in the app to work with Redis
