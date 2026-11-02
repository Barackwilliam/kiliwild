"""
Kili Wild Adventure settings. Secrets come from the environment (Render -> Environment, or a local .env).
See env.example for the full list.
"""
import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv(path):
    """Local development: KEY=value lines from .env (git-ignored). Real environment variables win."""
    if not path.exists():
        return
    raw = path.read_bytes()
    # Windows editors/PowerShell may save .env as UTF-16 or UTF-8 with a BOM.
    text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8-sig")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.split(" #", 1)[0].strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


_load_dotenv(BASE_DIR / ".env")


def env(name, default=""):
    return os.environ.get(name, default)


def env_bool(name, default=False):
    return env(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    return [x.strip() for x in env(name, default).split(",") if x.strip()]


DEBUG = env_bool("DJANGO_DEBUG", False)
SECRET_KEY = env("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError("DJANGO_SECRET_KEY is not set")
    SECRET_KEY = "dev-only-insecure-key"

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")
if env("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(env("RENDER_EXTERNAL_HOSTNAME"))
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h not in ("localhost", "127.0.0.1")]

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "tours",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "tours.context_processors.site",
            ],
        },
    },
]

# Database: DATABASE_URL from Supabase (Project Settings -> Database -> Connection string, "Session pooler").
# Without it (local development) SQLite is used.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=int(env("DB_CONN_MAX_AGE", "60")),
        conn_health_checks=True,
    )
}
if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    DATABASES["default"].setdefault("OPTIONS", {})["sslmode"] = env("DB_SSLMODE", "require")

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Dar_es_Salaam"
USE_I18N = True
USE_TZ = True

# Static files: WhiteNoise. Photos (packages, gallery): Supabase Storage through its S3-compatible API when
# SUPABASE_S3_* are set (Supabase -> Storage -> Settings -> S3 access keys); local disk otherwise.
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

SUPABASE_PROJECT_REF = env("SUPABASE_PROJECT_REF")      # the "abcd1234" in https://abcd1234.supabase.co
SUPABASE_BUCKET = env("SUPABASE_BUCKET", "kiliwild")    # must be a PUBLIC bucket
USE_SUPABASE_STORAGE = bool(
    SUPABASE_PROJECT_REF and env("SUPABASE_S3_ACCESS_KEY_ID") and env("SUPABASE_S3_SECRET_ACCESS_KEY")
)

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
                    if not DEBUG else "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
if USE_SUPABASE_STORAGE:
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "endpoint_url": f"https://{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/s3",
            "region_name": env("SUPABASE_S3_REGION", "eu-central-1"),
            "access_key": env("SUPABASE_S3_ACCESS_KEY_ID"),
            "secret_key": env("SUPABASE_S3_SECRET_ACCESS_KEY"),
            "bucket_name": SUPABASE_BUCKET,
            # Public bucket: plain links, no expiring signatures.
            "custom_domain": f"{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/object/public/{SUPABASE_BUCKET}",
            "querystring_auth": False,
            "file_overwrite": False,
            "default_acl": None,
            "object_parameters": {"CacheControl": "public, max-age=2592000"},
        },
    }

# Page cache shared by all gunicorn workers on the machine, so an admin edit clears it everywhere.
CACHES = {"default": {"BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
                      "LOCATION": env("CACHE_DIR", "/tmp/kiliwild-cache"), "TIMEOUT": 600}}

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Business details used across the site (override in the environment if they change).
SITE_NAME = "Kili Wild Adventure"
WHATSAPP_NUMBER = env("WHATSAPP_NUMBER", "255678102003")          # digits only, with country code
CONTACT_PHONE = env("CONTACT_PHONE", "+255 678 102 003")
CONTACT_EMAIL = env("CONTACT_EMAIL", "Danielsteven051@gmail.com")
FACEBOOK_URL = env("FACEBOOK_URL", "https://www.facebook.com/share/19tv582m5o/?mibextid=wwXIfr")
FOUNDER_NAME = "Daniel Bwire Steven"
LOCATION = "Moshi & Arusha, Tanzania"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}
