from urllib.parse import quote

from django.conf import settings

from .models import Category, Package


def whatsapp_url(message=""):
    url = f"https://wa.me/{settings.WHATSAPP_NUMBER}"
    return f"{url}?text={quote(message)}" if message else url


def site(request):
    used = set(Package.objects.filter(is_active=True).values_list("category", flat=True).distinct())
    nav = [(c.value, c.label) for c in Category if c.value in used]
    return {
        "SITE_NAME": settings.SITE_NAME,
        "CONTACT_PHONE": settings.CONTACT_PHONE,
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "FACEBOOK_URL": settings.FACEBOOK_URL,
        "FOUNDER_NAME": settings.FOUNDER_NAME,
        "LOCATION": settings.LOCATION,
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
        "WHATSAPP_URL": whatsapp_url("Hello Kili Wild Adventure! I'd like to plan a trip."),
        "nav_categories": nav,
    }
