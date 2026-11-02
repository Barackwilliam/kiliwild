from django.contrib import admin
from django.utils.html import format_html

from .models import FAQ, Destination, GalleryPhoto, Inclusion, ItineraryDay, Package, PriceTier

admin.site.site_header = "Kili Wild Adventure – Admin"
admin.site.site_title = "Kili Wild Adventure"
admin.site.index_title = "Manage packages, prices, destinations and photos"


def thumb(image, size=60):
    if not image:
        return "—"
    return format_html('<img src="{}" style="height:{}px;border-radius:6px;object-fit:cover">', image.url, size)


class PriceTierInline(admin.TabularInline):
    model = PriceTier
    extra = 0
    fields = ("group_size", "price", "is_best", "sort_order")


class ItineraryDayInline(admin.StackedInline):
    model = ItineraryDay
    extra = 0
    fields = (("day_label", "sort_order"), "title", "description", ("elevation", "distance", "hike_time", "habitat"))


class InclusionInline(admin.TabularInline):
    model = Inclusion
    extra = 0
    fields = ("kind", "text", "sort_order")


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("preview", "title", "category", "duration_days", "price_from", "is_featured", "is_active",
                    "sort_order")
    list_display_links = ("preview", "title")
    list_editable = ("price_from", "is_featured", "is_active", "sort_order")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("title", "subtitle", "summary")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("destinations",)
    inlines = [PriceTierInline, ItineraryDayInline, InclusionInline]
    readonly_fields = ("preview_large",)
    fieldsets = (
        (None, {"fields": ("category", "title", "slug", "subtitle", "badge", "duration_days")}),
        ("Short text", {"fields": ("summary", "why")}),
        ("Full description", {"fields": ("overview", "highlights")}),
        ("Key facts", {"fields": ("difficulty", "max_altitude", "accommodation", "best_for", "best_time",
                                  "destinations")}),
        ("Price", {"fields": ("price_from", "price_note", "tips_note", "extra_notes")}),
        ("Photo", {"fields": ("image", "preview_large")}),
        ("Display", {"fields": ("is_featured", "is_active", "sort_order")}),
    )

    @admin.display(description="")
    def preview(self, obj):
        return thumb(obj.image, 44)

    @admin.display(description="Current photo")
    def preview_large(self, obj):
        return thumb(obj.image, 160)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("preview", "name", "kind", "size", "is_active", "sort_order")
    list_display_links = ("preview", "name")
    list_editable = ("is_active", "sort_order")
    list_filter = ("kind",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_large",)
    fieldsets = (
        (None, {"fields": ("name", "slug", "swahili", "kind", "tagline")}),
        ("Text", {"fields": ("intro", "body", "highlights", "wildlife")}),
        ("Facts", {"fields": ("size", "known_for", "best_time", "map_key")}),
        ("Photo", {"fields": ("image", "preview_large")}),
        ("Display", {"fields": ("is_active", "sort_order")}),
    )

    @admin.display(description="")
    def preview(self, obj):
        return thumb(obj.image, 44)

    @admin.display(description="Current photo")
    def preview_large(self, obj):
        return thumb(obj.image, 160)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "sort_order")
    list_editable = ("sort_order",)
    list_filter = ("category",)
    search_fields = ("question", "answer")


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ("preview", "caption", "kind", "is_active", "sort_order")
    list_display_links = ("preview",)
    list_editable = ("caption", "kind", "is_active", "sort_order")
    list_filter = ("kind", "is_active")
    search_fields = ("caption",)
    list_per_page = 50

    @admin.display(description="")
    def preview(self, obj):
        return thumb(obj.image)
