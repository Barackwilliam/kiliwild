from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Destination, Package


class PackageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Package.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class StaticSitemap(Sitemap):
    priority = 0.6

    def items(self):
        return ["tours:home", "tours:destinations", "tours:about", "tours:gallery", "tours:contact"]

    def location(self, item):
        return reverse(item)


class DestinationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Destination.objects.filter(is_active=True)
