from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import CATEGORY_INFO, Category, GalleryPhoto, Inclusion, Package

WHY_US = [
    ("team", "100% local team", "Born and raised under Kilimanjaro. Our guides know every trail, camp and crater."),
    ("shield", "Safety first", "Emergency oxygen, first aid kit and pulse oximeter on every climb, with licensed guides."),
    ("tag", "Fair prices", "Clear group prices with park fees included – and fair pay for our crew."),
    ("tree", "A tree for every climb", "We plant a tree for every climber, giving back to the mountain that hosts us."),
]


def active_packages():
    return Package.objects.filter(is_active=True)


def home(request):
    packages = active_packages().filter(is_featured=True)
    return render(request, "tours/home.html", {
        "kili": [p for p in packages if p.category == Category.KILIMANJARO],
        "safaris": [p for p in packages if p.category == Category.SAFARI],
        "meru": [p for p in packages if p.category == Category.MERU][:1],
        "combo": [p for p in packages if p.category == Category.COMBO][:1],
        "photos": GalleryPhoto.objects.filter(is_active=True).order_by("?")[:8],
        "why_us": WHY_US,
    })


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
    })


def package_detail(request, category, slug):
    package = get_object_or_404(
        active_packages().prefetch_related("price_tiers", "itinerary", Prefetch("inclusions")),
        category=category, slug=slug)
    inclusions = list(package.inclusions.all())
    related = active_packages().filter(category=package.category).exclude(pk=package.pk)[:3]
    return render(request, "tours/package_detail.html", {
        "package": package,
        "tiers": list(package.price_tiers.all()),
        "included": [i for i in inclusions if i.kind == Inclusion.INCLUDED],
        "excluded": [i for i in inclusions if i.kind == Inclusion.EXCLUDED],
        "related": related,
    })


def about(request):
    return render(request, "tours/about.html", {
        "why_us": WHY_US,
        "photos": GalleryPhoto.objects.filter(is_active=True, kind=GalleryPhoto.Kind.KILIMANJARO)[:3],
    })


def gallery(request):
    return render(request, "tours/gallery.html", {
        "photos": GalleryPhoto.objects.filter(is_active=True),
        "kinds": GalleryPhoto.Kind.choices,
    })


def contact(request):
    return render(request, "tours/contact.html", {"packages": active_packages().order_by("category", "sort_order")})
