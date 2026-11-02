import re

from django.db import models
from django.urls import reverse


class Category(models.TextChoices):
    KILIMANJARO = "kilimanjaro", "Kilimanjaro"
    MERU = "mount-meru", "Mount Meru"
    SAFARI = "safari", "Safari"
    COMBO = "combo", "Combo Offers"
    DAY_TRIP = "day-trips", "Day Trips"


CATEGORY_INFO = {
    Category.KILIMANJARO: {
        "title": "Kilimanjaro Climbs",
        "tagline": "Stand on the Roof of Africa – Uhuru Peak, 5,895m.",
        "intro": "Four routes, one summit. Every climb comes with a licensed guide, cook and porters, "
                 "emergency oxygen and a pulse oximeter – and we plant a tree for every climber.",
    },
    Category.MERU: {
        "title": "Mount Meru",
        "tagline": "Tanzania's 2nd highest peak – 4,566m in Arusha National Park.",
        "intro": "Less crowded, full of wildlife and the perfect acclimatization warm-up before Kilimanjaro.",
    },
    Category.SAFARI: {
        "title": "Tanzania Safaris",
        "tagline": "Serengeti · Ngorongoro Crater · Tarangire · Lake Manyara",
        "intro": "4x4 pop-up roof jeeps, English-speaking guides, lodges or tented camps and every park fee "
                 "included. Choose 3, 4 or 5 days.",
    },
    Category.COMBO: {
        "title": "Combo Offers",
        "tagline": "Two mountains, one trip – and a better price.",
        "intro": "Pair Mount Meru with Kilimanjaro: acclimatize on Meru, then summit Kili stronger.",
    },
    Category.DAY_TRIP: {
        "title": "Day Trips",
        "tagline": "Short adventures around Moshi & Arusha.",
        "intro": "Waterfalls, coffee farms, hot springs and culture – perfect before or after your climb or safari.",
    },
}


def lines(text):
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]


class Destination(models.Model):
    class Kind(models.TextChoices):
        MOUNTAIN = "mountain", "Mountain"
        PARK = "park", "National park"
        TOWN = "town", "Town"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    swahili = models.CharField(max_length=100, blank=True, help_text="Swahili name or meaning")
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.PARK)
    tagline = models.CharField(max_length=180)
    intro = models.TextField(help_text="Opening paragraph.")
    body = models.TextField(blank=True, help_text="More paragraphs, separated by an empty line.")
    highlights = models.TextField(blank=True, help_text="One highlight per line.")
    wildlife = models.TextField(blank=True, help_text="Animals / things to see, one per line.")
    best_time = models.CharField(max_length=200, blank=True)
    size = models.CharField(max_length=100, blank=True, help_text='e.g. "14,763 km²" or "5,895m"')
    known_for = models.CharField(max_length=160, blank=True)
    image = models.ImageField(upload_to="destinations/", blank=True)
    map_key = models.CharField(max_length=40, blank=True, help_text="Key of the pin on the home-page map.")
    sort_order = models.PositiveSmallIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tours:destination", args=[self.slug])

    @property
    def body_paragraphs(self):
        return paragraphs(self.body)

    @property
    def highlights_list(self):
        return lines(self.highlights)

    @property
    def wildlife_list(self):
        return lines(self.wildlife)


class Package(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MODERATE = "moderate", "Moderate"
        CHALLENGING = "challenging", "Challenging"
        DEMANDING = "demanding", "Demanding"

    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    subtitle = models.CharField(max_length=160, blank=True, help_text='e.g. "Whiskey Route"')
    badge = models.CharField(max_length=40, blank=True, help_text='Short label on the card, e.g. "Bestseller"')
    duration_days = models.PositiveSmallIntegerField()
    summary = models.TextField(help_text="One or two sentences shown on cards and at the top of the page.")
    why = models.TextField(blank=True, help_text="Longer 'Why this trip' text on the package page.")
    overview = models.TextField(blank=True, help_text="Full description – paragraphs separated by an empty line.")
    highlights = models.TextField(blank=True, help_text="One highlight per line.")
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, blank=True)
    best_time = models.CharField(max_length=200, blank=True)
    destinations = models.ManyToManyField(Destination, blank=True, related_name="packages")
    max_altitude = models.CharField(max_length=60, blank=True)
    accommodation = models.CharField(max_length=80, blank=True)
    best_for = models.CharField(max_length=160, blank=True)

    price_from = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True,
                                     help_text="Headline price in USD. Leave empty for 'price on request'.")
    price_note = models.CharField(max_length=80, blank=True, default="per person · group of 4–6")
    tips_note = models.CharField(max_length=200, blank=True)
    extra_notes = models.TextField(blank=True, help_text="Good-to-know lines, one per line.")

    image = models.ImageField(upload_to="packages/", blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on the home page.")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=100)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "duration_days", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tours:package", args=[self.category, self.slug])

    @property
    def category_label(self):
        return Category(self.category).label

    @property
    def extra_notes_list(self):
        return lines(self.extra_notes)

    @property
    def overview_paragraphs(self):
        return paragraphs(self.overview)

    @property
    def highlights_list(self):
        return lines(self.highlights)

    @property
    def difficulty_level(self):
        """1–4 for the difficulty meter."""
        return {"easy": 1, "moderate": 2, "challenging": 3, "demanding": 4}.get(self.difficulty, 0)


class PriceTier(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="price_tiers")
    group_size = models.CharField(max_length=60, help_text='e.g. "1 person (private)", "4–6 people"')
    price = models.DecimalField(max_digits=8, decimal_places=0, help_text="USD per person")
    is_best = models.BooleanField(default=False, help_text="Highlight as best price")
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.group_size}: ${self.price}"

    @property
    def size_range(self):
        """(min, max) people this tier covers, read from the label: "4–6 people" -> (4, 6), "7+" -> (7, 99)."""
        nums = [int(n) for n in re.findall(r"\d+", self.group_size)]
        if not nums:
            return (0, 0)
        if "+" in self.group_size:
            return (nums[0], 99)
        return (nums[0], nums[-1])


class ItineraryDay(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="itinerary")
    day_label = models.CharField(max_length=20, help_text='e.g. "Day 1" or "Day 2–3"')
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    elevation = models.PositiveIntegerField(null=True, blank=True, help_text="Metres – where you sleep (or the summit)")
    distance = models.CharField(max_length=40, blank=True, help_text='e.g. "11 km"')
    hike_time = models.CharField(max_length=40, blank=True, help_text='e.g. "5–7 hours"')
    habitat = models.CharField(max_length=60, blank=True, help_text='e.g. "Rainforest" or "Game drive"')
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.day_label}: {self.title}"


class Inclusion(models.Model):
    INCLUDED, EXCLUDED = "in", "out"
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="inclusions")
    kind = models.CharField(max_length=3, choices=[(INCLUDED, "Included"), (EXCLUDED, "Not included")])
    text = models.CharField(max_length=240)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.text


class FAQ(models.Model):
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ["category", "sort_order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class GalleryPhoto(models.Model):
    class Kind(models.TextChoices):
        KILIMANJARO = "kilimanjaro", "Kilimanjaro"
        SAFARI = "safari", "Safari & Wildlife"
        LANDSCAPE = "landscape", "Craters & Lakes"
        CULTURE = "culture", "Culture & Day Trips"

    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=160, blank=True)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.KILIMANJARO)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=100)
    source_name = models.CharField(max_length=120, blank=True, editable=False,
                                   help_text="Original file name, used by the import command.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.caption or self.image.name
