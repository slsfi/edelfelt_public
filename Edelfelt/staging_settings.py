#Import these settings from local_settings.py
from settings import MIDDLEWARE_CLASSES

ALLOWED_HOSTS = ['', '', '', '']


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:xxxxx',
    }
}

# Cache the whole site. UpdateCacheMiddleWare needs to be first in list and
# FetchFromCacheMiddleware needs to be last.
MIDDLEWARE_CLASSES.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
MIDDLEWARE_CLASSES.append('django.middleware.cache.FetchFromCacheMiddleware')

CACHE_MIDDLEWARE_SECONDS = 2505600  # 29 days
CACHE_MIDDLEWARE_KEY_PREFIX = 'edelfelt'