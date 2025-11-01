from django.core.cache import cache
from django.utils.text import slugify
import hashlib

class SimpleCacheManager:
    """
    A generic cache manager for handling caching logic across models.
    """

    @staticmethod
    def generate_key(model_name, **filters):
        """
        Generate a cache key based on model name and filters.
        Example: generate_key('hotel', city='tehran') -> 'hotel:city:tehran'
        """
        key_parts = [model_name]
        for key, value in sorted(filters.items()):
            if value:  # Only include filters with values
                key_parts.append(f"{key}:{slugify(str(value))}")
        return ':'.join(key_parts)

    @staticmethod
    def generate_list_key(model_name, request):
        """
        Generate a unique cache key for list views based on request path.
        Uses MD5 hash of full path to avoid overly long keys.
        """
        full_path = request.get_full_path()
        path_hash = hashlib.md5(full_path.encode()).hexdigest()[:12]
        return f"{model_name}_list:{path_hash}"

    @staticmethod
    def get(key):
        """Retrieve data from cache."""
        return cache.get(key)

    @staticmethod
    def set(key, data, timeout=300):
        """Store data in cache with optional timeout."""
        cache.set(key, data, timeout)

    @staticmethod
    def invalidate_pattern(pattern):
        """
        Delete all cache keys matching a given pattern.
        Useful for bulk invalidation.
        """
        cache.delete_pattern(pattern)

    @staticmethod
    def invalidate_model_list(model_name):
        """
        Delete all list cache entries for a given model.
        """
        cache.delete_pattern(f"{model_name}_list:*")

    @staticmethod
    def invalidate_by_filters(model_name, **filters):
        """
        Smart invalidation based on filters.
        Example: invalidate_by_filters('hotel', city='tehran')
        """
        if filters:
            pattern = SimpleCacheManager.generate_key(model_name, **filters) + "*"
            cache.delete_pattern(pattern)
        else:
            # If no filters provided, invalidate all list caches for the model
            SimpleCacheManager.invalidate_model_list(model_name)