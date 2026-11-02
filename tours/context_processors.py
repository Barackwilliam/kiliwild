from urllib.parse import quote

from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from .models import Category, Package


NAV_NOTES = {
    "kilimanjaro": "Four routes to Uhuru Peak",
    "mount-meru": "Tanzania's second-highest peak",
    "safari": "Serengeti, Ngorongoro & more",
    "combo": "Two mountains, one trip",
    "day-trips": "Short adventures",
}
NAV_THUMBS = {
    "kilimanjaro": "img/map/kilimanjaro.jpg",
    "mount-meru": "img/map/meru.jpg",
    "safari": "img/slides/elephants.jpg",
    "combo": "img/summit-team.jpg",
    "day-trips": "img/slides/maasai.jpg",
}
EXTRA_PAGES = [
    ("tours:destinations", "Destinations", "Parks, mountains & towns", "compass"),
    ("tours:gallery", "Gallery", "Photos from the trail", "camera"),
    ("tours:about", "About", "Our local team", "team"),
    ("tours:contact", "Contact", "Plan your trip with us", "mail"),
]


def whatsapp_url(message=""):
    url = f"https://wa.me/{settings.WHATSAPP_NUMBER}"
    return f"{url}?text={quote(message)}" if message else url


def site(request):
    used = set(Package.objects.filter(is_active=True).values_list("category", flat=True).distinct())
    nav = [(c.value, c.label) for c in Category if c.value in used]
    path = request.path
    trips = [{"url": reverse("tours:category", args=[slug]), "label": label, "note": NAV_NOTES.get(slug, ""),
              "active": f"/tours/{slug}/" in path, "thumb": static(NAV_THUMBS.get(slug, "img/hero.jpg")),
              "slug": slug}
             for slug, label in nav]
    pages = [{"url": reverse(name), "label": label, "note": note, "icon": icon,
              "active": path.startswith(reverse(name))}
             for name, label, note, icon in EXTRA_PAGES]
    return {
        "SITE_NAME": settings.SITE_NAME,
        "CONTACT_PHONE": settings.CONTACT_PHONE,
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "FACEBOOK_URL": settings.FACEBOOK_URL,
        "INSTAGRAM_URL": settings.INSTAGRAM_URL,
        "FOUNDER_NAME": settings.FOUNDER_NAME,
        "LOCATION": settings.LOCATION,
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
        "WHATSAPP_URL": whatsapp_url("Hello Kili Wild Adventure! I'd like to plan a trip."),
        "nav_categories": nav,
        "nav_trips": trips,
        "nav_pages": pages,
    }
