from django.core.cache import cache

from blogs.models import Blog
from config.settings import CACHE_ENABLED


def get_articles_from_cache():

    if not CACHE_ENABLED:
        return Blog.objects.all()
    else:
        key = 'blog'
        cache_data = cache.get(key)
        if cache_data is not None:
            return cache_data
        else:
            cache_data = Blog.objects.all()
            cache.set(key, cache_data)
            return cache_data