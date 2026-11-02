from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryPhoto, Inclusion, ItineraryDay, Package, PriceTier

admin.site.site_header = "Kili Wild Adventure – Admin"
admin.site.site_title = "Kili Wild Adventure"
admin.site.index_title = "Manage packages, prices and photos"


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
    fields = (("day_label", "sort_order"), "title", "description")


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
    inlines = [PriceTierInline, ItineraryDayInline, InclusionInline]
    readonly_fields = ("preview_large",)
    fieldsets = (
        (None, {"fields": ("category", "title", "slug", "subtitle", "badge", "duration_days")}),
        ("Text", {"fields": ("summary", "why", "max_altitude", "accommodation", "best_for")}),
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
