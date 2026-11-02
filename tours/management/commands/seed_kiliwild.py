"""
Load the client's packages and photos.

    python manage.py seed_kiliwild              # packages + gallery (skips what already exists)
    python manage.py seed_kiliwild --reset      # rewrite packages from seed_data.py (prices, itinerary, lists)
    python manage.py seed_kiliwild --no-gallery

Photos are saved through Django's default storage, so with SUPABASE_S3_* set they go straight into
the Supabase bucket.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from tours import seed_data
from tours.models import GalleryPhoto, Inclusion, ItineraryDay, Package, PriceTier

PHOTOS = Path(settings.BASE_DIR) / "seed_photos"
CHILD_KEYS = ("price_tiers", "itinerary", "inclusions", "exclusions", "photo")


class Command(BaseCommand):
    help = "Load Kili Wild Adventure packages and gallery photos."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Overwrite existing packages (and their prices/itinerary) with seed_data.py")
        parser.add_argument("--no-gallery", action="store_true")

    def handle(self, *args, reset=False, no_gallery=False, **opts):
        where = f"Supabase bucket '{settings.SUPABASE_BUCKET}'" if settings.USE_SUPABASE_STORAGE else "local media/"
        self.stdout.write(f"Photos will be stored in: {where}")
        for data in seed_data.PACKAGES:
            self._package(data, reset)
        if not no_gallery:
            self._gallery()
        self.stdout.write(self.style.SUCCESS("Done."))

    @transaction.atomic
    def _package(self, data, reset):
        fields = {k: v for k, v in data.items() if k not in CHILD_KEYS and k != "slug"}
        pkg = Package.objects.filter(slug=data["slug"]).first()
        if pkg and not reset:
            self.stdout.write(f"  = {pkg.title} (exists, skipped)")
            return
        if pkg:
            for k, v in fields.items():
                setattr(pkg, k, v)
            pkg.save()
        else:
            pkg = Package.objects.create(slug=data["slug"], **fields)

        pkg.price_tiers.all().delete()
        PriceTier.objects.bulk_create(
            PriceTier(package=pkg, sort_order=i, **t) for i, t in enumerate(data.get("price_tiers", [])))
        pkg.itinerary.all().delete()
        ItineraryDay.objects.bulk_create(
            ItineraryDay(package=pkg, sort_order=i, **d) for i, d in enumerate(data.get("itinerary", [])))
        pkg.inclusions.all().delete()
        Inclusion.objects.bulk_create(
            [Inclusion(package=pkg, kind=Inclusion.INCLUDED, text=t, sort_order=i)
             for i, t in enumerate(data.get("inclusions", []))]
            + [Inclusion(package=pkg, kind=Inclusion.EXCLUDED, text=t, sort_order=i)
               for i, t in enumerate(data.get("exclusions", []))])

        photo = PHOTOS / data.get("photo", "")
        if not pkg.image and data.get("photo") and photo.exists():
            with photo.open("rb") as fh:
                pkg.image.save(f"{pkg.slug}.jpg", File(fh), save=True)
        self.stdout.write(f"  + {pkg.title}")

    def _gallery(self):
        files = sorted(PHOTOS.glob("*.jpg"))
        have = set(GalleryPhoto.objects.values_list("source_name", flat=True))
        added = 0
        for i, path in enumerate(files):
            if path.name in have:
                continue
            num, _, suffix = path.stem.partition("-")
            photo = GalleryPhoto(
                caption=seed_data.GALLERY_CAPTIONS.get(num, ""),
                kind=seed_data.GALLERY_KIND_BY_SUFFIX.get(suffix, "kilimanjaro"),
                sort_order=i, source_name=path.name)
            with path.open("rb") as fh:
                photo.image.save(f"kiliwild-{path.name}", File(fh), save=True)
            added += 1
        self.stdout.write(f"  gallery: {added} new photos ({len(files) - added} already there)")
