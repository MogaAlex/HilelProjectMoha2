import functools
import logging
from django.core.cache import caches

logger = logging.getLogger(__name__)

L2 = caches['default']
L3 = caches['page_cache']