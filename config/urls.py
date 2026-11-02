from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path

from tours.sitemaps import PackageSitemap, StaticSitemap


def robots(request):
    lines = ["User-agent: *", "Disallow: /admin/", f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"packages": PackageSitemap, "pages": StaticSitemap}},
         name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots),
    path("", include("tours.urls")),
]
if settings.DEBUG and not settings.USE_SUPABASE_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
