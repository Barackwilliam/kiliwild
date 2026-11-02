"""Clear the page cache whenever site content changes in the admin, so visitors never see stale prices."""
from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .models import FAQ, Destination, GalleryPhoto, Inclusion, ItineraryDay, Package, PriceTier

CONTENT_MODELS = (Package, PriceTier, ItineraryDay, Inclusion, Destination, FAQ, GalleryPhoto)


@receiver(post_save)
@receiver(post_delete)
def clear_page_cache(sender, **kwargs):
    if sender in CONTENT_MODELS:
        cache.clear()


@receiver(m2m_changed, sender=Package.destinations.through)
def clear_on_m2m(sender, **kwargs):
    cache.clear()
