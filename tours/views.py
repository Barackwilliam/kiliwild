from functools import wraps

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.cache import cache_page

from .models import CATEGORY_INFO, FAQ, Category, Destination, GalleryPhoto, Inclusion, Package
from .showcase import MAP_PLACES, SLIDES, TOUR_ORDER, WILDLIFE, ZONES

WHY_US = [
    ("team", "100% local team", "Born and raised under Kilimanjaro. Our guides know every trail, camp and crater.",
     "img/why/team.jpg"),
    ("shield", "Safety first", "Emergency oxygen, first aid kit and pulse oximeter on every climb, with licensed guides.",
     "img/why/safety.jpg"),
    ("tag", "Fair prices", "Clear group prices with park fees included – and fair pay for our crew.",
     "img/why/prices.jpg"),
    ("tree", "A tree for every climb", "We plant a tree for every climber, giving back to the mountain that hosts us.",
     "img/why/tree.jpg"),
]

PAGE_CACHE_SECONDS = 600


def public_page(view):
    """Cache public pages for a few minutes in production. tours/signals.py clears the cache on any admin edit."""
    if settings.DEBUG:
        return view
    cached = cache_page(PAGE_CACHE_SECONDS)(view)

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:          # staff see their edits straight away
            return view(request, *args, **kwargs)
        return cached(request, *args, **kwargs)
    return wrapper


def active_packages():
    return Package.objects.filter(is_active=True)


def map_places():
    """Map places with real URLs, for the page and for the map script (json_script)."""
    more = {d.map_key: d.get_absolute_url() for d in Destination.objects.filter(is_active=True).exclude(map_key="")}
    places = []
    for p in MAP_PLACES:
        name, arg = p["link"]
        places.append({**p, "photo": static(p["photo"]), "url": reverse(name, args=[arg] if arg else None),
                       "more": more.get(p["key"], ""), "link": None})
    return places


def elevation_profile(days, width=760, height=230):
    """SVG coordinates for an elevation chart of a climb, or None when there is too little data."""
    pts = [(d.day_label, d.elevation) for d in days if d.elevation]
    if len(pts) < 3:
        return None
    pad_l, pad_r, pad_t, pad_b = 46, 24, 34, 36
    lo, hi = 1000, max(e for _, e in pts) + 400
    hi = (hi // 1000 + 1) * 1000
    w, h = width - pad_l - pad_r, height - pad_t - pad_b
    step = w / (len(pts) - 1)

    def y(e):
        return round(pad_t + h - (e - lo) / (hi - lo) * h, 1)

    points = [{"x": round(pad_l + i * step, 1), "y": y(e), "label": lbl.replace("Day ", "D"), "elev": e}
              for i, (lbl, e) in enumerate(pts)]
    line = " ".join(f"{p['x']},{p['y']}" for p in points)
    area = f"M{points[0]['x']},{pad_t + h} L" + " L".join(f"{p['x']},{p['y']}" for p in points) + \
           f" L{points[-1]['x']},{pad_t + h} Z"
    grid = [{"y": y(e), "label": f"{e:,}m"} for e in range(2000, hi + 1, 1000)]
    peak = max(points, key=lambda p: p["elev"])
    return {"width": width, "height": height, "points": points, "line": line, "area": area, "grid": grid,
            "base": pad_t + h, "peak": peak, "left": pad_l, "right": width - pad_r}


def ticket_package(slug, category):
    """The package shown on a homepage ticket: the usual one, or the first of its kind if it was removed."""
    return (active_packages().filter(slug=slug).first()
            or active_packages().filter(category=category, price_from__isnull=False).first())


@public_page
def home(request):
    packages = active_packages().filter(is_featured=True)
    return render(request, "tours/home.html", {
        "ticket_climb": ticket_package("machame-route-7-days", Category.KILIMANJARO),
        "ticket_safari": ticket_package("4-days-safari", Category.SAFARI),
        "kili": [p for p in packages if p.category == Category.KILIMANJARO],
        "safaris": [p for p in packages if p.category == Category.SAFARI],
        "meru": [p for p in packages if p.category == Category.MERU][:1],
        "combo": [p for p in packages if p.category == Category.COMBO][:1],
        "destinations": Destination.objects.filter(is_active=True, kind=Destination.Kind.PARK)[:4],
        "photos": GalleryPhoto.objects.filter(is_active=True).order_by("?")[:14],
        "why_us": WHY_US,
        "slides": SLIDES,
        "places": map_places(),
        "tour_order": TOUR_ORDER,
        "zones": ZONES,
        "wildlife": WILDLIFE,
    })


@public_page
def category(request, category):
    if category not in Category.values:
        raise Http404
    packages = active_packages().filter(category=category)
    if not packages.exists():
        raise Http404
    return render(request, "tours/category.html", {
        "category": category,
        "category_label": Category(category).label,
        "info": CATEGORY_INFO.get(category, {}),
        "packages": packages,
        "hero_image": next((p.image.url for p in packages if p.image), ""),
        "faqs": FAQ.objects.filter(category=category),
    })


@public_page
def package_detail(request, category, slug):
    package = get_object_or_404(
        active_packages().prefetch_related("price_tiers", "itinerary", "inclusions", "destinations"),
        category=category, slug=slug)
    inclusions = list(package.inclusions.all())
    days = list(package.itinerary.all())
    return render(request, "tours/package_detail.html", {
        "package": package,
        "days": days,
        "profile": elevation_profile(days),
        "tiers": list(package.price_tiers.all()),
        "included": [i for i in inclusions if i.kind == Inclusion.INCLUDED],
        "excluded": [i for i in inclusions if i.kind == Inclusion.EXCLUDED],
        "destinations": [d for d in package.destinations.all() if d.is_active],
        "faqs": FAQ.objects.filter(category=package.category),
        "related": active_packages().filter(category=package.category).exclude(pk=package.pk)[:3],
    })


@public_page
def destinations(request):
    items = Destination.objects.filter(is_active=True)
    return render(request, "tours/destinations.html", {
        "groups": [(label, [d for d in items if d.kind == kind]) for kind, label in
                   [(Destination.Kind.PARK, "National parks"), (Destination.Kind.MOUNTAIN, "Mountains"),
                    (Destination.Kind.TOWN, "Our bases")]],
    })


@public_page
def destination_detail(request, slug):
    dest = get_object_or_404(Destination, slug=slug, is_active=True)
    return render(request, "tours/destination_detail.html", {
        "dest": dest,
        "packages": dest.packages.filter(is_active=True),
        "others": Destination.objects.filter(is_active=True).exclude(pk=dest.pk)[:4],
    })


@public_page
def about(request):
    return render(request, "tours/about.html", {"why_us": WHY_US})


@public_page
def gallery(request):
    live = GalleryPhoto.objects.filter(is_active=True)
    hero_photos = [p for p in (live.filter(kind=k).order_by("?").first() for k in
                               (GalleryPhoto.Kind.KILIMANJARO, GalleryPhoto.Kind.SAFARI, GalleryPhoto.Kind.CULTURE)) if p]
    return render(request, "tours/gallery.html", {
        "hero_photos": hero_photos,
        "photos": live,
        "kinds": GalleryPhoto.Kind.choices,
    })


@public_page
def contact(request):
    return render(request, "tours/contact.html", {"packages": active_packages().order_by("category", "sort_order")})
