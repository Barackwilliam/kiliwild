from django.urls import path

from . import views

app_name = "tours"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
    path("tours/<slug:category>/", views.category, name="category"),
    path("tours/<slug:category>/<slug:slug>/", views.package_detail, name="package"),
]
