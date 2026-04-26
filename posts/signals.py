from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .cache_keys import BLOG_LIST_CACHE_KEY, post_detail_cache_key
from .models import Post


@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def invalidate_post_caches(sender, instance, **kwargs):
    cache.delete(BLOG_LIST_CACHE_KEY)
    cache.delete(post_detail_cache_key(instance.pk))
