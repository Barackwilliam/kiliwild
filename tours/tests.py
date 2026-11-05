from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import FAQ, Destination, GalleryPhoto, Package, PriceTier
from .views import elevation_profile


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class SiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_kiliwild", verbosity=0, stdout=open("/dev/null", "w"))

    def test_seed_loads_everything(self):
        self.assertEqual(Package.objects.count(), 12)
        self.assertEqual(GalleryPhoto.objects.count(), 82)
        machame = Package.objects.get(slug="machame-route-7-days")
        self.assertEqual(machame.price_tiers.count(), 5)
        self.assertEqual(machame.itinerary.count(), 7)
        self.assertTrue(machame.image)
        self.assertTrue(machame.overview_paragraphs)
        self.assertEqual(machame.itinerary.first().elevation, 3000)
        self.assertEqual(Destination.objects.count(), 8)
        self.assertGreater(FAQ.objects.count(), 10)
        self.assertEqual(set(machame.destinations.values_list("slug", flat=True)), {"kilimanjaro", "moshi"})

    def test_seed_is_idempotent(self):
        call_command("seed_kiliwild", verbosity=0, stdout=open("/dev/null", "w"))
        self.assertEqual(Package.objects.count(), 12)
        self.assertEqual(GalleryPhoto.objects.count(), 82)

    def test_pages_render(self):
        urls = [reverse("tours:home"), reverse("tours:about"), reverse("tours:gallery"), reverse("tours:contact"),
                reverse("tours:category", args=["kilimanjaro"]), reverse("tours:destinations"),
                "/sitemap.xml", "/robots.txt"]
        urls += [p.get_absolute_url() for p in Package.objects.all()]
        urls += [d.get_absolute_url() for d in Destination.objects.all()]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_detail_shows_prices_and_whatsapp(self):
        resp = self.client.get(Package.objects.get(slug="machame-route-7-days").get_absolute_url())
        self.assertContains(resp, "$1,900")
        self.assertContains(resp, "$2,400")
        self.assertContains(resp, "wa.me/255750910158")
        self.assertContains(resp, "Elevation profile")
        self.assertContains(resp, "Barranco Wall")
        self.assertContains(resp, "Questions & answers")

    def test_elevation_profile(self):
        safari = Package.objects.get(slug="4-days-safari")
        self.assertIsNone(elevation_profile(list(safari.itinerary.all())))
        prof = elevation_profile(list(Package.objects.get(slug="lemosho-route-8-days").itinerary.all()))
        self.assertEqual(prof["peak"]["elev"], 5895)
        self.assertEqual(len(prof["points"]), 8)

    def test_seed_reset_keeps_counts(self):
        call_command("seed_kiliwild", "--reset", "--no-gallery", verbosity=0, stdout=open("/dev/null", "w"))
        self.assertEqual(Package.objects.count(), 12)
        self.assertEqual(Destination.objects.count(), 8)

    def test_empty_or_unknown_category_404(self):
        self.assertEqual(self.client.get(reverse("tours:category", args=["day-trips"])).status_code, 404)
        self.assertEqual(self.client.get("/tours/nothing/").status_code, 404)

    def test_tier_size_range(self):
        self.assertEqual(PriceTier(group_size="1 person (private)").size_range, (1, 1))
        self.assertEqual(PriceTier(group_size="4–6 people").size_range, (4, 6))
        self.assertEqual(PriceTier(group_size="7+ people").size_range, (7, 99))
