"""
Starting content for Kili Wild Adventure, taken from the price sheets the client sent.
`python manage.py seed_kiliwild` loads it; after that everything is edited in the Django admin.

Where the client gave no itinerary (Lemosho, Marangu, Rongai, Meru 3 days) the standard route
camps are used – check them with the client.
"""

# ---------------------------------------------------------------- shared lists

TREK_CAMPING_INCLUDED = [
    "Tent and sleeping mattress (soft mattress)",
    "All meals on the mountain – breakfast, lunch, dinner + snacks",
    "Drinking water (3 litres per day)",
    "All transport – go and return (Arusha/Moshi to the gate and back)",
    "All park fees – entry, camping and rescue fees (KINAPA)",
    "All safety equipment – emergency oxygen, first aid kit, pulse oximeter",
    "Airport pickup – Kilimanjaro Airport (JRO) to Arusha / Moshi",
    "Professional mountain crew – licensed guide, cook, porters",
    "Government taxes",
]

TREK_EXCLUDED = [
    "Chef, guide and porter tips – recommended $350 per climber, shared among the crew",
    "International flights",
    "Tanzania visa ($50–$100)",
    "Travel insurance (highly recommended)",
    "Personal climbing gear – sleeping bag, jacket (available for rent, $80)",
    "Personal expenses (drinks at hotel, laundry)",
    "Hotel before and after the climb (we can arrange, $50 per night)",
]

MARANGU_INCLUDED = [
    "Hut accommodation – Mandara, Horombo and Kibo huts (beds & mattresses)",
    "All meals and drinking water",
    "All transport – go and return",
    "All park fees and safety equipment (oxygen, first aid)",
    "Airport pickup – Arusha / Moshi",
    "Professional guide, cook and porters",
]

MARANGU_EXCLUDED = [
    "Chef, guide and porter tips ($350 total)",
    "International flights",
    "Tanzania visa",
    "Travel insurance",
    "Personal gear",
]

MERU_INCLUDED = [
    "Hut accommodation – Miriakamba & Saddle huts",
    "All meals and drinking water",
    "All transport – go and return (Arusha to the gate)",
    "All park fees (Arusha National Park)",
    "All safety equipment",
    "Airport pickup",
    "Professional guide, cook and porters",
    "Armed ranger (required for wildlife protection)",
]

MERU_EXCLUDED = [
    "Chef, guide and porter tips ($200 total)",
    "International flights",
    "Tanzania visa",
    "Travel insurance",
    "Personal gear",
]

SAFARI_INCLUDED = [
    "4x4 safari jeep with pop-up roof",
    "Professional English-speaking safari guide",
    "All park fees – Serengeti, Ngorongoro, Tarangire, Manyara",
    "Accommodation – lodge / tented camp",
    "All meals – breakfast, lunch, dinner",
    "Bottled water – 1.5L per day",
    "All transport – go and return (Arusha to the parks)",
    "Airport pickup (JRO to Arusha)",
]

SAFARI_EXCLUDED = [
    "Guide tips ($20 per day per group)",
    "Chef tips (camping safari only)",
    "International flights",
    "Tanzania visa",
    "Travel insurance",
    "Alcoholic drinks",
    "Personal expenses",
]

KILI_EXTRAS = (
    "Gear rental (sleeping bag, jacket and more): $80\n"
    "Hotel before / after the climb: we can arrange from $50 per night\n"
    "We plant a tree for every climber"
)


def tiers(*rows, best=None):
    """rows: (group_size, price). `best` is the group_size to highlight."""
    return [{"group_size": g, "price": p, "is_best": g == best} for g, p in rows]


def days(*rows):
    """rows: (day_label, title, description)."""
    return [{"day_label": d, "title": t, "description": desc} for d, t, desc in rows]


# ---------------------------------------------------------------- packages

PACKAGES = [
    # ---------------- Kilimanjaro: the four main routes first
    {
        "slug": "machame-route-7-days",
        "category": "kilimanjaro",
        "title": "7 Days Machame Route",
        "subtitle": "The Whiskey Route – Roof of Africa, 5,895m",
        "badge": "Most popular",
        "duration_days": 7,
        "summary": "Kilimanjaro's most popular route: rainforest, the Shira Plateau, Lava Tower and the famous "
                   "Barranco Wall, with a climb-high-sleep-low profile that helps you acclimatize.",
        "why": "Machame is scenic from the first hour to the last. You climb through thick rainforest, cross the "
               "open Shira Plateau, touch 4,630m at Lava Tower and drop back down to sleep at Barranco – the best "
               "natural acclimatization on the mountain. Day 6 is summit day: Uhuru Peak at sunrise, then down to "
               "Mweka Camp.",
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain tents",
        "best_for": "Fit hikers who want great scenery and a strong summit chance",
        "price_from": 1900,
        "tips_note": "Tips not included – recommended $350 per climber, shared among the crew.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": True,
        "sort_order": 10,
        "photo": "19-kili.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 2400), ("2 people", 2050), ("3 people", 1950),
            ("4–6 people", 1900), ("7+ people", 1800), best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Machame Gate to Machame Camp",
             "Drive from Moshi/Arusha to Machame Gate (1,800m) and hike through the rainforest to Machame Camp (3,000m)."),
            ("Day 2", "Machame Camp to Shira Camp",
             "Leave the forest behind and climb onto the Shira Plateau (3,840m) with wide views of Kibo."),
            ("Day 3", "Shira Camp to Barranco Camp via Lava Tower",
             "Climb high to Lava Tower (4,630m) for acclimatization, then descend to sleep at Barranco Camp (3,960m)."),
            ("Day 4", "Barranco Camp to Karanga Camp",
             "Scramble up the Barranco Wall and traverse to Karanga Camp (4,035m)."),
            ("Day 5", "Karanga Camp to Barafu Camp",
             "A short climb to Barafu base camp (4,670m). Early dinner and rest before the summit push."),
            ("Day 6", "Barafu Camp to SUMMIT Uhuru Peak to Mweka Camp",
             "Start around midnight, reach Stella Point and Uhuru Peak (5,895m) at sunrise, then descend to Mweka Camp (3,100m)."),
            ("Day 7", "Mweka Camp to Mweka Gate – return to Moshi/Arusha",
             "Walk down through the rainforest to Mweka Gate, collect your summit certificate and transfer back."),
        ),
        "inclusions": TREK_CAMPING_INCLUDED,
        "exclusions": TREK_EXCLUDED,
    },
    {
        "slug": "lemosho-route-8-days",
        "category": "kilimanjaro",
        "title": "8 Days Lemosho Route",
        "subtitle": "Premium route – best summit success rate",
        "badge": "Best for success",
        "duration_days": 8,
        "summary": "The most beautiful and remote route on Kilimanjaro, with the best summit success rate. "
                   "A favourite of our American guests.",
        "why": "Lemosho starts on the quiet western side of the mountain and crosses the whole Shira Plateau "
               "before joining the southern circuit. Eight days gives your body the most time to adjust to altitude, "
               "which is why it has the best success rate of all our routes.",
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain tents",
        "best_for": "Anyone who wants the highest chance of reaching the summit",
        "price_from": 2150,
        "tips_note": "Tips not included – $350 per climber, shared among the crew.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": True,
        "sort_order": 20,
        "photo": "36-kili.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 2750), ("2 people", 2350), ("4–6 people", 2150), ("7+ people", 2050),
            best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Londorossi Gate to Mti Mkubwa Camp",
             "Drive to Londorossi Gate (2,360m) and hike through rainforest to Mti Mkubwa – 'Big Tree' Camp (2,650m)."),
            ("Day 2", "Mti Mkubwa to Shira 1 Camp", "Climb out of the forest onto the Shira Ridge (3,500m)."),
            ("Day 3", "Shira 1 to Shira 2 Camp", "An easy acclimatization day across the Shira Plateau (3,850m)."),
            ("Day 4", "Shira 2 to Barranco Camp via Lava Tower",
             "Climb to Lava Tower (4,630m), then descend to sleep at Barranco Camp (3,960m)."),
            ("Day 5", "Barranco Camp to Karanga Camp", "Climb the Barranco Wall and continue to Karanga Camp (4,035m)."),
            ("Day 6", "Karanga Camp to Barafu Camp", "A short climb to Barafu base camp (4,670m) and rest."),
            ("Day 7", "Barafu Camp to SUMMIT Uhuru Peak to Mweka Camp",
             "Midnight start, Uhuru Peak (5,895m) at sunrise, then descend to Mweka Camp (3,100m)."),
            ("Day 8", "Mweka Camp to Mweka Gate – return to Moshi/Arusha",
             "Final walk down, summit certificates and transfer back."),
        ),
        "inclusions": TREK_CAMPING_INCLUDED,
        "exclusions": TREK_EXCLUDED,
    },
    {
        "slug": "marangu-route-6-days",
        "category": "kilimanjaro",
        "title": "6 Days Marangu Route",
        "subtitle": "The Coca-Cola Route – sleep in huts, not tents",
        "badge": "Recommended",
        "duration_days": 6,
        "summary": "The only route with hut accommodation – beds and mattresses instead of tents. Good for "
                   "beginners, and the extra day at Horombo gives you better acclimatization.",
        "why": "Marangu is the classic route and the most affordable way to the top. You sleep in the Mandara, "
               "Horombo and Kibo huts, and the 6-day version adds an acclimatization day at Horombo, which makes a "
               "real difference on summit night.",
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain huts (beds & mattresses)",
        "best_for": "Beginners and anyone who prefers a bed to a tent",
        "price_from": 1750,
        "tips_note": "Tips not included – $350 total.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": True,
        "sort_order": 30,
        "photo": "56-kili.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 2250), ("2 people", 1900), ("4–6 people", 1750), ("7+ people", 1650),
            best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Marangu Gate to Mandara Hut",
             "Short drive to Marangu Gate (1,860m) and a gentle rainforest walk to Mandara Hut (2,720m)."),
            ("Day 2", "Mandara Hut to Horombo Hut", "Through moorland to Horombo Hut (3,720m) with views of Kibo and Mawenzi."),
            ("Day 3", "Acclimatization day at Horombo",
             "A hike towards Zebra Rocks or the Mawenzi saddle, then back to Horombo to sleep."),
            ("Day 4", "Horombo Hut to Kibo Hut", "Across the alpine desert 'saddle' to Kibo Hut (4,700m). Early rest."),
            ("Day 5", "Kibo Hut to SUMMIT Uhuru Peak to Horombo Hut",
             "Midnight start via Gilman's Point to Uhuru Peak (5,895m), then descend to Horombo Hut."),
            ("Day 6", "Horombo Hut to Marangu Gate – return to Moshi/Arusha",
             "Walk down to the gate, collect certificates and transfer back."),
        ),
        "inclusions": MARANGU_INCLUDED,
        "exclusions": MARANGU_EXCLUDED,
    },
    {
        "slug": "rongai-route-7-days",
        "category": "kilimanjaro",
        "title": "7 Days Rongai Route",
        "subtitle": "The quiet northern route",
        "badge": "",
        "duration_days": 7,
        "summary": "The only route that starts from the north, near the Kenyan border. Drier, quieter and less "
                   "crowded, with a steady climb and a descent down the Marangu side.",
        "why": "Rongai is a good choice in the rainy season because the northern slopes get less rain. It sees "
               "fewer climbers than the southern routes, passes the beautiful Mawenzi Tarn and comes down on the "
               "other side of the mountain, so you see Kilimanjaro from two sides.",
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain tents",
        "best_for": "Quiet trails and rainy-season climbs",
        "price_from": None,
        "price_note": "Ask us on WhatsApp for the current price",
        "tips_note": "Tips not included – $350 per climber, shared among the crew.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": True,
        "sort_order": 40,
        "photo": "76-kili.jpg",
        "price_tiers": [],
        "itinerary": days(
            ("Day 1", "Rongai Gate to Simba Camp", "Drive to Rongai Gate (1,950m) and hike to Simba Camp (2,600m)."),
            ("Day 2", "Simba Camp to Second Cave", "Climb steadily through heath to Second Cave (3,450m)."),
            ("Day 3", "Second Cave to Kikelewa Camp", "Towards the jagged peaks of Mawenzi, to Kikelewa Camp (3,600m)."),
            ("Day 4", "Kikelewa Camp to Mawenzi Tarn", "A short, steep climb to Mawenzi Tarn (4,330m) for acclimatization."),
            ("Day 5", "Mawenzi Tarn to Kibo Hut", "Cross the saddle to Kibo Hut (4,700m). Early rest."),
            ("Day 6", "Kibo Hut to SUMMIT Uhuru Peak to Horombo Hut",
             "Midnight start via Gilman's Point to Uhuru Peak (5,895m), then descend to Horombo Hut (3,720m)."),
            ("Day 7", "Horombo Hut to Marangu Gate – return to Moshi/Arusha", "Walk down, certificates and transfer back."),
        ),
        "inclusions": TREK_CAMPING_INCLUDED,
        "exclusions": TREK_EXCLUDED,
    },
    # ---------------- Kilimanjaro: shorter / longer versions
    {
        "slug": "lemosho-route-7-days",
        "category": "kilimanjaro",
        "title": "7 Days Lemosho Route",
        "subtitle": "Premium western route, one day shorter",
        "badge": "",
        "duration_days": 7,
        "summary": "All the beauty of Lemosho – remote western start, the full Shira Plateau, Lava Tower and "
                   "Barranco – in seven days.",
        "why": "The same quiet, scenic route as our 8-day Lemosho, with one less day on the mountain. Choose the "
               "8-day version if you want the very best acclimatization.",
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain tents",
        "best_for": "Fit hikers short on time who still want the scenic route",
        "price_from": 1950,
        "tips_note": "Tips not included – $350 per climber, shared among the crew.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": False,
        "sort_order": 50,
        "photo": "13-kili.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 2550), ("2 people", 2150), ("4–6 people", 1950), ("7+ people", 1850),
            best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Londorossi Gate to Mti Mkubwa Camp", "Rainforest hike to Mti Mkubwa Camp (2,650m)."),
            ("Day 2", "Mti Mkubwa to Shira 1 Camp", "Onto the Shira Ridge (3,500m)."),
            ("Day 3", "Shira 1 to Shira 2 Camp", "Across the Shira Plateau (3,850m)."),
            ("Day 4", "Shira 2 to Barranco Camp via Lava Tower", "Up to Lava Tower (4,630m), down to Barranco (3,960m)."),
            ("Day 5", "Barranco Camp to Barafu Camp via Karanga", "Barranco Wall, Karanga valley and on to Barafu (4,670m)."),
            ("Day 6", "Barafu Camp to SUMMIT Uhuru Peak to Mweka Camp", "Uhuru Peak (5,895m) at sunrise, down to Mweka Camp."),
            ("Day 7", "Mweka Camp to Mweka Gate – return to Moshi/Arusha", "Final descent and transfer back."),
        ),
        "inclusions": TREK_CAMPING_INCLUDED,
        "exclusions": TREK_EXCLUDED,
    },
    {
        "slug": "marangu-route-5-days",
        "category": "kilimanjaro",
        "title": "5 Days Marangu Route",
        "subtitle": "The Coca-Cola Route – fastest and cheapest",
        "badge": "",
        "duration_days": 5,
        "summary": "The quickest hut route to Uhuru Peak. Beds and mattresses every night and the lowest price "
                   "on the mountain.",
        "why": "Good if you are short on time or already acclimatized (for example after Mount Meru). If this is "
               "your first time at altitude we recommend the 6-day version.",
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain huts (beds & mattresses)",
        "best_for": "Travellers short on time or already acclimatized",
        "price_from": 1600,
        "tips_note": "Tips not included – $350 total.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": False,
        "sort_order": 60,
        "photo": "81-kili.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 2100), ("2 people", 1750), ("4–6 people", 1600), ("7+ people", 1500),
            best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Marangu Gate to Mandara Hut", "Rainforest walk to Mandara Hut (2,720m)."),
            ("Day 2", "Mandara Hut to Horombo Hut", "Through moorland to Horombo Hut (3,720m)."),
            ("Day 3", "Horombo Hut to Kibo Hut", "Across the saddle to Kibo Hut (4,700m)."),
            ("Day 4", "Kibo Hut to SUMMIT Uhuru Peak to Horombo Hut", "Uhuru Peak (5,895m) at sunrise, down to Horombo."),
            ("Day 5", "Horombo Hut to Marangu Gate – return to Moshi/Arusha", "Final descent and transfer back."),
        ),
        "inclusions": MARANGU_INCLUDED,
        "exclusions": MARANGU_EXCLUDED,
    },
    # ---------------- Mount Meru
    {
        "slug": "mount-meru-4-days",
        "category": "mount-meru",
        "title": "4 Days Mount Meru",
        "subtitle": "Tanzania's 2nd highest peak – best acclimatization",
        "badge": "Most popular",
        "duration_days": 4,
        "summary": "Socialist Peak (4,566m) in Arusha National Park. Wildlife on the trail, huts every night and "
                   "far fewer people than Kilimanjaro.",
        "why": "Meru is a real mountain in its own right – a sharp crater rim walk to the summit with Kilimanjaro "
               "on the horizon at sunrise. Giraffes and buffalo on the lower slopes mean an armed ranger walks "
               "with you. It's also the perfect acclimatization climb before Kilimanjaro.",
        "max_altitude": "4,566m – Socialist Peak",
        "accommodation": "Mountain huts",
        "best_for": "Acclimatization before Kilimanjaro, wildlife lovers, quieter trails",
        "price_from": 1100,
        "tips_note": "Tips not included – $200 total.",
        "is_featured": True,
        "sort_order": 10,
        "photo": "66-landscape.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 1400), ("2 people", 1200), ("4–6 people", 1100), best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Momella Gate to Miriakamba Hut", "Walk through forest and open grassland with wildlife to Miriakamba Hut (2,500m)."),
            ("Day 2", "Miriakamba Hut to Saddle Hut", "A steep forest climb to Saddle Hut (3,570m). Optional afternoon walk up Little Meru."),
            ("Day 3", "Saddle Hut to SUMMIT Socialist Peak (4,566m) to Miriakamba Hut",
             "Early start along the crater rim to the summit at sunrise, then descend to Miriakamba Hut."),
            ("Day 4", "Miriakamba Hut to Momella Gate – return to Arusha", "Easy walk down and transfer back to Arusha."),
        ),
        "inclusions": MERU_INCLUDED,
        "exclusions": MERU_EXCLUDED,
    },
    {
        "slug": "mount-meru-3-days",
        "category": "mount-meru",
        "title": "3 Days Mount Meru",
        "subtitle": "Fast trek to Socialist Peak",
        "badge": "",
        "duration_days": 3,
        "summary": "A fast climb of Tanzania's 2nd highest peak for fit hikers who are short on time.",
        "why": "The same summit as the 4-day trek, with the descent done in one long day. Choose the 4-day version "
               "if you want better acclimatization.",
        "max_altitude": "4,566m – Socialist Peak",
        "accommodation": "Mountain huts",
        "best_for": "Fit hikers short on time",
        "price_from": 900,
        "tips_note": "Tips not included – $200 total.",
        "is_featured": False,
        "sort_order": 20,
        "photo": "42-landscape.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 1200), ("2 people", 1000), ("4–6 people", 900), best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Momella Gate to Miriakamba Hut", "Forest and grassland walk with wildlife to Miriakamba Hut (2,500m)."),
            ("Day 2", "Miriakamba Hut to Saddle Hut", "Climb to Saddle Hut (3,570m). Optional walk up Little Meru."),
            ("Day 3", "Saddle Hut to SUMMIT Socialist Peak to Momella Gate – return to Arusha",
             "Summit at sunrise, then a long descent all the way to Momella Gate."),
        ),
        "inclusions": MERU_INCLUDED,
        "exclusions": MERU_EXCLUDED,
    },
    # ---------------- Combo
    {
        "slug": "meru-kilimanjaro-combo",
        "category": "combo",
        "title": "Meru + Kilimanjaro Combo",
        "subtitle": "Mount Meru 4 Days + Machame Route 7 Days",
        "badge": "Save $200",
        "duration_days": 11,
        "summary": "Two mountains in one trip. Acclimatize on Meru, then climb Kilimanjaro by the Machame Route "
                   "already adjusted to altitude.",
        "why": "Meru is the best warm-up for Kilimanjaro: you sleep above 3,500m, summit at 4,566m and see wildlife "
               "on the way. When you start Machame a day later, your body is already used to the altitude – a big "
               "boost on summit night.",
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Huts on Meru, tents on Kilimanjaro",
        "best_for": "Climbers who want the best summit chance – and two summits",
        "price_from": 2800,
        "price_note": "per person · save $200",
        "tips_note": "Tips not included – $200 for the Meru crew and $350 for the Kilimanjaro crew.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": True,
        "sort_order": 10,
        "photo": "07-kili.jpg",
        "price_tiers": [],
        "itinerary": days(
            ("Day 1–4", "Mount Meru – Momella Gate to Socialist Peak and back",
             "Miriakamba Hut, Saddle Hut, summit of Socialist Peak (4,566m) and back to Momella Gate."),
            ("Day 5–11", "Kilimanjaro – Machame Route",
             "Machame Camp, Shira, Lava Tower & Barranco, Karanga, Barafu, Uhuru Peak (5,895m) and down via Mweka."),
        ),
        "inclusions": ["Everything included in the Mount Meru 4 Days package",
                       "Everything included in the Machame Route 7 Days package"],
        "exclusions": ["Crew tips – $200 (Meru) and $350 (Kilimanjaro)", "International flights", "Tanzania visa",
                       "Travel insurance", "Personal gear (rental available)"],
    },
    # ---------------- Safaris
    {
        "slug": "3-days-safari",
        "category": "safari",
        "title": "3 Days Safari",
        "subtitle": "Tarangire · Ngorongoro Crater · Lake Manyara",
        "badge": "",
        "duration_days": 3,
        "summary": "Elephants in Tarangire, the Big Five in Ngorongoro Crater and flamingos at Lake Manyara – the "
                   "best of northern Tanzania in three days.",
        "why": "Short on time? This safari packs in Tarangire's huge elephant herds and baobabs, a full game drive "
               "on the floor of Ngorongoro Crater – one of the best places in Africa to see the Big Five – and Lake "
               "Manyara on the way home.",
        "max_altitude": "",
        "accommodation": "Lodge / tented camp",
        "best_for": "Short trips and add-ons after a climb",
        "price_from": 800,
        "tips_note": "Guide tips not included – $20 per day per group.",
        "is_featured": True,
        "sort_order": 10,
        "photo": "54-landscape.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 1200), ("2 people", 900), ("4–6 people", 800), ("7+ people", 750),
            best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Arusha to Tarangire National Park", "Game drive among elephants and giant baobab trees."),
            ("Day 2", "Ngorongoro Crater", "Descend into the crater for a full day looking for the Big Five."),
            ("Day 3", "Lake Manyara – return to Arusha", "Game drive at Lake Manyara, then drive back to Arusha."),
        ),
        "inclusions": SAFARI_INCLUDED,
        "exclusions": SAFARI_EXCLUDED,
    },
    {
        "slug": "4-days-safari",
        "category": "safari",
        "title": "4 Days Safari",
        "subtitle": "Tarangire · Serengeti · Ngorongoro Crater",
        "badge": "Bestseller",
        "duration_days": 4,
        "summary": "Our bestseller. Tarangire, a night in the endless plains of the Serengeti and a full game "
                   "drive in Ngorongoro Crater.",
        "why": "Four days is the sweet spot: enough time to reach the Serengeti and spend a night there, with "
               "Tarangire on the way in and Ngorongoro Crater on the way out.",
        "max_altitude": "",
        "accommodation": "Lodge / tented camp",
        "best_for": "First-time safari travellers",
        "price_from": 1100,
        "tips_note": "Guide tips not included – $20 per day per group.",
        "is_featured": True,
        "sort_order": 20,
        "photo": "34-safari.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 1600), ("2 people", 1250), ("4–6 people", 1100), ("7+ people", 1000),
            best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Arusha to Tarangire National Park", "Game drive among elephants and baobabs."),
            ("Day 2", "Tarangire to Central Serengeti", "Drive into the Serengeti with a game drive on the way to camp."),
            ("Day 3", "Serengeti to Ngorongoro", "Morning game drive in the Serengeti, then on to the Ngorongoro highlands."),
            ("Day 4", "Ngorongoro Crater – return to Arusha", "Game drive on the crater floor, then back to Arusha."),
        ),
        "inclusions": SAFARI_INCLUDED,
        "exclusions": SAFARI_EXCLUDED,
    },
    {
        "slug": "5-days-safari",
        "category": "safari",
        "title": "5 Days Safari",
        "subtitle": "Full experience – 2 full days in the Serengeti",
        "badge": "Full experience",
        "duration_days": 5,
        "summary": "Tarangire, two full days in the Serengeti – with the chance to see the migration – "
                   "Ngorongoro Crater and Lake Manyara.",
        "why": "Two full days in the Serengeti give you time to follow the big herds and the predators that "
               "follow them. Add Tarangire, Ngorongoro Crater and Lake Manyara and you have seen all four of "
               "northern Tanzania's great parks.",
        "max_altitude": "",
        "accommodation": "Lodge / tented camp",
        "best_for": "Wildlife lovers and photographers",
        "price_from": 1400,
        "tips_note": "Guide tips not included – $20 per day per group.",
        "is_featured": True,
        "sort_order": 30,
        "photo": "40-safari.jpg",
        "price_tiers": tiers(
            ("1 person (private)", 2000), ("2 people", 1600), ("4–6 people", 1400), ("7+ people", 1300),
            best="4–6 people"),
        "itinerary": days(
            ("Day 1", "Arusha to Tarangire National Park", "Game drive among elephants and baobabs."),
            ("Day 2–3", "Serengeti – two full days", "Follow the herds across the plains – see the migration in season."),
            ("Day 4", "Ngorongoro Crater", "A full game drive on the crater floor."),
            ("Day 5", "Lake Manyara – return to Arusha", "Game drive at Lake Manyara, then drive back to Arusha."),
        ),
        "inclusions": SAFARI_INCLUDED,
        "exclusions": SAFARI_EXCLUDED,
    },
]


# ---------------------------------------------------------------- gallery captions (file -> caption)

GALLERY_CAPTIONS = {
    "00": "Sunrise at Uhuru Peak", "01": "Uhuru Peak – the Roof of Africa", "02": "Kibo above the clouds",
    "03": "Above the clouds on Kilimanjaro", "04": "On the high slopes of Kibo", "05": "Summit team at Uhuru Peak",
    "06": "Celebrating at the summit", "07": "Uhuru Peak sign at dawn", "08": "Kilimanjaro from the trail",
    "09": "Giant lobelia below Kibo", "10": "Kilimanjaro over the moorland", "11": "Climbers at the rock caves",
    "12": "Giant groundsels on the trail", "13": "Camp below Kibo", "14": "The summit glaciers",
    "15": "Our climbers at the cave", "16": "Rainforest trail", "17": "Giraffe with Kilimanjaro behind",
    "18": "Camp with a view", "19": "Evening at camp", "20": "Baobabs and elephant",
    "21": "Summit night on the snow", "22": "Elephants at the river", "23": "Kibo's rugged slopes",
    "24": "Across the high desert", "25": "Ngorongoro Crater viewpoint", "26": "Sunrise from the crater rim",
    "27": "Kilimanjaro from the plains", "28": "Camp sign on the mountain", "29": "Zebras, wildebeest & flamingos",
    "30": "Zebras and giraffes", "31": "Kibo above the lava fields", "32": "View from the escarpment",
    "33": "Flamingos on the lake", "34": "Game drive with giraffes", "35": "Zebras in the Serengeti",
    "36": "Stars over camp", "37": "Black rhino in the crater", "38": "Kibo above the moorland",
    "39": "Wildebeest river crossing", "40": "The Great Migration", "41": "Balloon safari at sunrise",
    "42": "Crater lake", "43": "The crater floor", "44": "Cheetahs on a kopje", "45": "Acacia at sunset",
    "46": "Wildebeest herds", "47": "Meeting the Maasai", "48": "Lake view from the forest",
    "49": "Sunset camp under Kilimanjaro", "50": "Crater from above", "51": "Coffee tour and waterfall",
    "52": "Lions under an acacia", "53": "Elephants and baobab", "54": "Flamingos at Lake Manyara",
    "55": "Safari jeep at the waterhole", "56": "Mandara Huts, Marangu Route", "57": "Lions in a tree",
    "58": "Kilimanjaro at golden hour", "59": "Giraffes", "60": "Zebras by the crater lake",
    "61": "Treetop walkway", "62": "Lion on the plains", "63": "Lion pride at a kill", "64": "Congratulations!",
    "65": "Lionesses on the hunt", "66": "Savanna below the mountains", "67": "Leopard resting",
    "68": "Made it to Uhuru Peak", "69": "Tree-climbing lions", "70": "Climbers heading up",
    "71": "Zebras and wildebeest", "72": "Serengeti National Park", "73": "Leopard up close",
    "74": "Wildlife on the crater floor", "75": "Fiery sky over the plains", "76": "Kibo from the north",
    "77": "Elephants under Kilimanjaro", "78": "Ngorongoro Crater", "79": "Serengeti gate",
    "80": "Our climbers at the gate", "81": "Kilimanjaro National Park gate",
}

GALLERY_KIND_BY_SUFFIX = {"kili": "kilimanjaro", "safari": "safari", "landscape": "landscape", "culture": "culture"}
