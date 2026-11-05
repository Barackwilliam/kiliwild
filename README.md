# Kili Wild Adventure – website

Django site for Kili Wild Adventure (Moshi & Arusha, Tanzania): Kilimanjaro climbs, Mount Meru, safaris and
combo offers. Bookings go straight to WhatsApp **+255 750 910 158**: the booking form builds a message with
the trip, name, date, group size and a price estimate.

- **Database:** Supabase Postgres (`DATABASE_URL`), SQLite locally
- **Photos:** Supabase Storage public bucket through the S3 API (`SUPABASE_S3_*`), local `media/` otherwise
- **Admin:** `/admin/` – packages (price tiers, day-by-day itinerary with elevation/distance/time, included/not
  included), destinations, FAQs and gallery
- **Pages:** home (slideshow, talking map), Kilimanjaro / Meru / Safari / Combo, package pages (elevation
  profile, FAQ), 8 destination pages, gallery, about, contact
- **Speed:** public pages are cached for 10 minutes in production; any admin edit clears the cache

## Run locally

```bash
git clone https://github.com/Barackwilliam/kiliwild.git
cd kiliwild
pip install -r requirements.txt
cp env.example .env          # set DJANGO_DEBUG=True and leave the Supabase lines empty for local work
                             # (Windows: copy env.example .env)
python manage.py migrate
python manage.py seed_kiliwild
python manage.py createsuperuser
python manage.py runserver
```

## Supabase setup

1. **Database:** Project Settings → Database → Connection string → *Session pooler*. Put it in `DATABASE_URL`.
2. **Storage:** create a **public** bucket called `kiliwild`. Then Storage → Settings → S3 access keys → create
   a key, and set `SUPABASE_PROJECT_REF`, `SUPABASE_S3_ACCESS_KEY_ID` and `SUPABASE_S3_SECRET_ACCESS_KEY`
   (and `SUPABASE_S3_REGION` if your project isn't in `eu-central-1`).
3. Run `python manage.py migrate` and `python manage.py seed_kiliwild` with those variables set. The command
   uploads the package photos and the 82 gallery photos from `seed_photos/` into the bucket.

`seed_kiliwild` can be run again safely: existing packages and photos are skipped. Use
`--reset` to overwrite packages, destinations and FAQs with what's in `tours/seed_data.py` (this resets prices
and text edited in admin). **If you seeded an older version, run `python manage.py seed_kiliwild --reset` once**
to load the new descriptions, destinations and FAQs.

## Deploy (Render)

- Build command: `./build.sh`
- Start command: `gunicorn config.wsgi`
- Environment: everything in `env.example` (`DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL`, `SUPABASE_*`)

## Content

All content lives in the database and is edited in the admin. The starting data is in `tours/seed_data.py`.
To check with the client:

- **Rongai 7 days** has no price yet, so it shows "Price on request". Add price tiers in admin.
- Itineraries for **Lemosho, Marangu, Rongai and Meru 3 days** use the standard route camps, because the
  client only sent day-by-day plans for Machame and Meru 4 days. Distances and hiking times on every route are
  the usual published approximations.
- **Lemosho and Rongai** use the Machame included/not-included list (camping routes).
- **Day Trips:** the category exists but is hidden until a day-trip package is added in admin.

## Tests

```bash
python manage.py test tours
```
