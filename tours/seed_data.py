"""
Starting content for Kili Wild Adventure, taken from the price sheets the client sent and expanded with
route and park descriptions. `python manage.py seed_kiliwild` loads it; after that everything is edited in
the Django admin.

Prices, inclusions and the Machame / Meru 4-day itineraries come from the client. The other itineraries use
the standard camps, distances and times for each route (approximate) – check them with the client.
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

KILI_BEST_TIME = "January – mid March and June – October (the dry seasons). Climbs run all year."
SAFARI_BEST_TIME = ("All year. June – October for classic dry-season game viewing; January – February for "
                    "the calving season in the southern Serengeti.")


def tiers(*rows, best=None):
    """rows: (group_size, price). `best` is the group_size to highlight."""
    return [{"group_size": g, "price": p, "is_best": g == best} for g, p in rows]


def day(label, title, description, elevation=None, distance="", hike_time="", habitat=""):
    return {"day_label": label, "title": title, "description": description, "elevation": elevation,
            "distance": distance, "hike_time": hike_time, "habitat": habitat}


SUMMIT_NIGHT = (
    "The big one. You wake around midnight, drink something hot and start up by headlamp, slow and steady "
    "– pole pole – with your guide setting the pace. Dawn breaks as you reach the crater rim, and Uhuru Peak, "
    "the highest point in Africa, comes a little later with the whole continent glowing below you. Photos, "
    "hugs, then a long descent to thicker air."
)

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
        "why": "Machame is scenic from the first hour to the last – and its climb-high-sleep-low profile gives "
               "your body the best natural acclimatization on the mountain.",
        "overview": (
            "Machame is called the Whiskey Route because it is a little tougher than the old Marangu 'Coca-Cola' "
            "route – and far more rewarding. In seven days you walk through every climate zone on Kilimanjaro: "
            "thick, mossy rainforest full of colobus monkeys, giant heather and moorland, the open Shira Plateau, "
            "the lunar alpine desert and finally the glaciers and snow of the summit.\n\n"
            "Day three is the secret to Machame's success. You climb to Lava Tower at 4,630m, eat lunch high, "
            "then drop back down to sleep at Barranco Camp. Climbing high and sleeping low is the best thing you "
            "can do for acclimatization, and it shows on summit night.\n\n"
            "The next morning brings the Barranco Wall – a fun, hands-on scramble that looks scary from below and "
            "turns out to be one of the highlights of the trip. From there the route traverses below the southern "
            "glaciers to Barafu base camp, where you rest before the midnight push to Uhuru Peak."
        ),
        "highlights": (
            "Walk through five climate zones, from rainforest to arctic summit\n"
            "Climb-high-sleep-low at Lava Tower (4,630m) for strong acclimatization\n"
            "Scramble the Barranco Wall – the most fun hour on the mountain\n"
            "Sunrise on Uhuru Peak, the Roof of Africa\n"
            "Descend via the quiet Mweka trail through the rainforest"
        ),
        "difficulty": "challenging",
        "best_time": KILI_BEST_TIME,
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain tents",
        "best_for": "Fit hikers who want great scenery and a strong summit chance",
        "price_from": 1900,
        "tips_note": "Tips not included – recommended $350 per climber, shared among the crew.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": True,
        "sort_order": 10,
        "photo": "19-kili.jpg",
        "destinations": ["kilimanjaro", "moshi"],
        "price_tiers": tiers(
            ("1 person (private)", 2400), ("2 people", 2050), ("3 people", 1950),
            ("4–6 people", 1900), ("7+ people", 1800), best="4–6 people"),
        "itinerary": [
            day("Day 1", "Machame Gate to Machame Camp",
                "A morning drive from Moshi/Arusha to Machame Gate (1,800m), where you register with the park and "
                "meet your porters. The trail winds up through tall, misty rainforest – listen for blue monkeys "
                "and look for black-and-white colobus – to Machame Camp at the edge of the forest.",
                3000, "11 km", "5–7 hours", "Rainforest"),
            day("Day 2", "Machame Camp to Shira Camp",
                "You leave the trees behind and climb a steep, rocky ridge through giant heather. The views open "
                "up as you reach the Shira Plateau, with Kibo's glaciers ahead and, on a clear evening, Mount Meru "
                "floating above the clouds to the west.",
                3850, "5 km", "4–6 hours", "Heath & moorland"),
            day("Day 3", "Shira Camp to Barranco Camp via Lava Tower",
                "The key acclimatization day. You climb steadily across the alpine desert to the 90-metre Lava "
                "Tower (4,630m) for lunch, then descend into the Barranco Valley, past forests of giant groundsels, "
                "to sleep at 3,960m. You may feel the altitude today – that is exactly the point.",
                3960, "10 km", "6–8 hours", "Alpine desert"),
            day("Day 4", "Barranco Camp to Karanga Camp",
                "Straight after breakfast you tackle the Barranco Wall: an exciting scramble using your hands, "
                "with no ropes or technical skills needed. At the top the views of the southern ice fields are "
                "spectacular. A shorter afternoon over ridges and valleys brings you to Karanga Camp.",
                4035, "5 km", "4–5 hours", "Alpine desert"),
            day("Day 5", "Karanga Camp to Barafu Camp",
                "A short, steady climb on bare rock and scree to Barafu – 'ice' in Swahili – the base camp for "
                "the summit. You arrive by lunchtime, check your gear, eat an early dinner and try to sleep a few "
                "hours before the big night.",
                4670, "4 km", "4–5 hours", "Alpine desert"),
            day("Day 6", "Barafu Camp to SUMMIT Uhuru Peak to Mweka Camp",
                SUMMIT_NIGHT + " You pass Stella Point (5,756m) on the rim and descend all the way to Mweka Camp.",
                5895, "5 km up · 12 km down", "12–16 hours", "Arctic summit"),
            day("Day 7", "Mweka Camp to Mweka Gate – return to Moshi/Arusha",
                "A relaxed final walk back through the rainforest. The crew usually sings you a farewell song – "
                "Jambo Bwana – before you reach Mweka Gate (1,640m), collect your summit certificate and transfer "
                "back for a hot shower.",
                1640, "10 km", "3–4 hours", "Rainforest"),
        ],
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
        "why": "Eight days gives your body the most time to adjust to altitude – which is why Lemosho has the "
               "best success rate of all our routes.",
        "overview": (
            "Lemosho starts far from the crowds, on the wild western side of Kilimanjaro. The first two days are "
            "spent in pristine rainforest where few climbers ever walk, before you climb onto the Shira Ridge and "
            "see the whole mountain laid out in front of you.\n\n"
            "Instead of rushing, Lemosho crosses the entire Shira Plateau – an ancient collapsed volcano, now a "
            "huge high-altitude meadow – over two easy days. This slow start is what makes the route so "
            "successful: by the time you reach Lava Tower and the southern circuit, your body has had days to "
            "adjust.\n\n"
            "From Barranco the route joins Machame for the Barranco Wall, Karanga and Barafu, and you summit "
            "via Stella Point at sunrise. If you want the best possible chance of standing on Uhuru Peak – and "
            "the most beautiful scenery on the way – this is the route we recommend."
        ),
        "highlights": (
            "Remote western start in untouched rainforest\n"
            "Two full days crossing the Shira Plateau\n"
            "The most gradual acclimatization profile on the mountain\n"
            "Our highest summit success rate\n"
            "Fewer people on the trail for the first half of the climb"
        ),
        "difficulty": "challenging",
        "best_time": KILI_BEST_TIME,
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain tents",
        "best_for": "Anyone who wants the highest chance of reaching the summit",
        "price_from": 2150,
        "tips_note": "Tips not included – $350 per climber, shared among the crew.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": True,
        "sort_order": 20,
        "photo": "36-kili.jpg",
        "destinations": ["kilimanjaro", "moshi"],
        "price_tiers": tiers(
            ("1 person (private)", 2750), ("2 people", 2350), ("4–6 people", 2150), ("7+ people", 2050),
            best="4–6 people"),
        "itinerary": [
            day("Day 1", "Londorossi Gate to Mti Mkubwa Camp",
                "A scenic drive around the western slopes to Londorossi Gate (2,360m). After registration, a "
                "short walk through ancient rainforest brings you to Mti Mkubwa – 'Big Tree' Camp.",
                2650, "6 km", "3–4 hours", "Rainforest"),
            day("Day 2", "Mti Mkubwa to Shira 1 Camp",
                "The forest gives way to giant heather as you climb onto the Shira Ridge. Your first big views of "
                "Kibo appear across the plateau as you reach camp.",
                3500, "8 km", "5–6 hours", "Heath & moorland"),
            day("Day 3", "Shira 1 to Shira 2 Camp",
                "An easy, beautiful day across the flat Shira Plateau – the remains of Kilimanjaro's oldest "
                "volcanic cone. Short day, lots of rest: perfect for acclimatization.",
                3850, "7 km", "4–5 hours", "Heath & moorland"),
            day("Day 4", "Shira 2 to Barranco Camp via Lava Tower",
                "Climb high to Lava Tower (4,630m) for lunch, then descend through giant groundsels into the "
                "Barranco Valley to sleep low at 3,960m.",
                3960, "10 km", "6–8 hours", "Alpine desert"),
            day("Day 5", "Barranco Camp to Karanga Camp",
                "Scramble up the famous Barranco Wall, then follow ridges and valleys below the southern glaciers "
                "to Karanga Camp.",
                4035, "5 km", "4–5 hours", "Alpine desert"),
            day("Day 6", "Karanga Camp to Barafu Camp",
                "A short climb on rock and scree to base camp. Arrive by lunch, rest, prepare your gear and eat an "
                "early dinner.",
                4670, "4 km", "4–5 hours", "Alpine desert"),
            day("Day 7", "Barafu Camp to SUMMIT Uhuru Peak to Mweka Camp",
                SUMMIT_NIGHT + " You descend all the way to Mweka Camp.",
                5895, "5 km up · 12 km down", "12–16 hours", "Arctic summit"),
            day("Day 8", "Mweka Camp to Mweka Gate – return to Moshi/Arusha",
                "A gentle walk down through the rainforest, a farewell song from the crew, summit certificates at "
                "the gate and a transfer back to your hotel.",
                1640, "10 km", "3–4 hours", "Rainforest"),
        ],
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
        "why": "Beds every night, a gentle gradient and an extra acclimatization day at Horombo – the comfortable "
               "way to the top.",
        "overview": (
            "Marangu is Kilimanjaro's classic route and the only one where you sleep in huts. Instead of a tent "
            "you get a bunk bed with a mattress in the wooden A-frame huts at Mandara, Horombo and Kibo – a big "
            "comfort on cold nights, and a great choice if you have never camped before.\n\n"
            "The trail climbs steadily on a well-made path from the south-east, through rainforest and wide "
            "moorland with views of jagged Mawenzi, Kilimanjaro's second peak. The six-day version adds a full "
            "acclimatization day at Horombo, where you hike up towards Zebra Rocks and come back down to sleep. "
            "That one extra day makes a real difference to how you feel on summit night.\n\n"
            "On summit night you climb the steep scree to Gilman's Point on the crater rim, then follow the rim "
            "to Uhuru Peak. You go up and down the same way, so the final descent is quick and familiar."
        ),
        "highlights": (
            "Sleep in mountain huts with beds and mattresses\n"
            "Gentle, steady gradient – good for first-time trekkers\n"
            "Extra acclimatization day at Horombo Hut\n"
            "Close-up views of Mawenzi peak\n"
            "The most affordable way to Uhuru Peak"
        ),
        "difficulty": "challenging",
        "best_time": KILI_BEST_TIME,
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain huts (beds & mattresses)",
        "best_for": "Beginners and anyone who prefers a bed to a tent",
        "price_from": 1750,
        "tips_note": "Tips not included – $350 total.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": True,
        "sort_order": 30,
        "photo": "56-kili.jpg",
        "destinations": ["kilimanjaro", "moshi"],
        "price_tiers": tiers(
            ("1 person (private)", 2250), ("2 people", 1900), ("4–6 people", 1750), ("7+ people", 1650),
            best="4–6 people"),
        "itinerary": [
            day("Day 1", "Marangu Gate to Mandara Hut",
                "A short drive to Marangu Gate (1,860m) and a gentle walk through rainforest to the wooden huts at "
                "Mandara. In the afternoon, a short side trip to the Maundi Crater for views towards Kenya.",
                2720, "8 km", "4–5 hours", "Rainforest"),
            day("Day 2", "Mandara Hut to Horombo Hut",
                "Out of the forest and into open moorland dotted with giant groundsels and lobelias. Kibo and "
                "Mawenzi rise ahead as you reach Horombo Hut.",
                3720, "12 km", "6–8 hours", "Heath & moorland"),
            day("Day 3", "Acclimatization day at Horombo",
                "A day to let your body adjust. Hike up towards Zebra Rocks – striped black-and-white cliffs – or "
                "the Mawenzi saddle, then return to Horombo for lunch and rest.",
                3720, "5 km", "3–4 hours", "Heath & moorland"),
            day("Day 4", "Horombo Hut to Kibo Hut",
                "Across 'the Saddle', a vast, silent alpine desert between Mawenzi and Kibo, to the stone Kibo Hut "
                "at the foot of the summit cone. Early dinner, early bed.",
                4700, "10 km", "6–7 hours", "Alpine desert"),
            day("Day 5", "Kibo Hut to SUMMIT Uhuru Peak to Horombo Hut",
                SUMMIT_NIGHT + " On Marangu you reach the rim at Gilman's Point (5,685m) and descend to Horombo Hut.",
                5895, "6 km up · 15 km down", "12–15 hours", "Arctic summit"),
            day("Day 6", "Horombo Hut to Marangu Gate – return to Moshi/Arusha",
                "A long but easy walk all the way down to Marangu Gate, certificates, celebrations and a transfer "
                "back to Moshi or Arusha.",
                1860, "20 km", "6–7 hours", "Rainforest"),
        ],
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
        "why": "Quiet trails, drier weather and two sides of the mountain in one climb.",
        "overview": (
            "Rongai is the only route that approaches Kilimanjaro from the north, close to the Kenyan border. "
            "The northern slopes get far less rain than the southern side, so Rongai is a smart choice in the "
            "wetter months – and because fewer climbers use it, the trail feels wild and peaceful.\n\n"
            "The climb is gentle and steady, through pine and rainforest and up across open moorland with views "
            "over the Amboseli plains in Kenya. Day four takes you to Mawenzi Tarn, a small lake tucked beneath "
            "the jagged towers of Mawenzi – one of the most beautiful campsites on the mountain.\n\n"
            "From Kibo Hut you summit via Gilman's Point and Uhuru Peak, then come down the Marangu Route on the "
            "south-east side. So you see Kilimanjaro from two completely different sides in one trip."
        ),
        "highlights": (
            "The only route from the north – remote and uncrowded\n"
            "Drier slopes: a good option in the rainy months\n"
            "Camp at beautiful Mawenzi Tarn\n"
            "Views across the Amboseli plains in Kenya\n"
            "Go up one side of the mountain and down the other"
        ),
        "difficulty": "challenging",
        "best_time": "All year – the drier northern slopes make it a good choice in the rainy months too.",
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
        "destinations": ["kilimanjaro", "moshi"],
        "price_tiers": [],
        "itinerary": [
            day("Day 1", "Rongai Gate to Simba Camp",
                "A long, scenic drive around the mountain to Rongai Gate (1,950m) near the Kenyan border, then a "
                "gentle walk through pine plantations and forest to Simba Camp.",
                2600, "7 km", "3–4 hours", "Forest"),
            day("Day 2", "Simba Camp to Second Cave",
                "A steady climb through heath with Kibo ahead and Kenya's plains behind you.",
                3450, "6 km", "3–4 hours", "Heath & moorland"),
            day("Day 3", "Second Cave to Kikelewa Camp",
                "Leave the main trail and head towards the jagged peaks of Mawenzi, to Kikelewa Camp in a sheltered "
                "valley.",
                3600, "6 km", "3–4 hours", "Heath & moorland"),
            day("Day 4", "Kikelewa Camp to Mawenzi Tarn",
                "A short, steep climb to Mawenzi Tarn, a small lake beneath Mawenzi's towers. Afternoon "
                "acclimatization walk.",
                4330, "4 km", "3–4 hours", "Alpine desert"),
            day("Day 5", "Mawenzi Tarn to Kibo Hut",
                "Cross the wide, silent Saddle between Mawenzi and Kibo to Kibo Hut. Early dinner and rest.",
                4700, "9 km", "4–5 hours", "Alpine desert"),
            day("Day 6", "Kibo Hut to SUMMIT Uhuru Peak to Horombo Hut",
                SUMMIT_NIGHT + " You reach the rim at Gilman's Point and descend to Horombo Hut on the Marangu side.",
                5895, "6 km up · 15 km down", "12–15 hours", "Arctic summit"),
            day("Day 7", "Horombo Hut to Marangu Gate – return to Moshi/Arusha",
                "Walk down through moorland and rainforest to Marangu Gate, collect your certificate and transfer "
                "back.",
                1860, "20 km", "6–7 hours", "Rainforest"),
        ],
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
        "why": "The scenic western route for fit hikers who are a little short on time.",
        "overview": (
            "The same quiet, beautiful route as our 8-day Lemosho, with one less day on the mountain. You still "
            "start in the remote western rainforest, cross the Shira Plateau and climb high to Lava Tower before "
            "sleeping low at Barranco.\n\n"
            "The day you save comes on day five, when you go from Barranco straight to Barafu base camp via "
            "Karanga. It is a longer day, so this version suits fit hikers. If you want the very best "
            "acclimatization, choose the 8-day Lemosho."
        ),
        "highlights": (
            "Remote western start in untouched rainforest\n"
            "Cross the Shira Plateau\n"
            "Lava Tower and the Barranco Wall\n"
            "Summit at sunrise via Stella Point"
        ),
        "difficulty": "challenging",
        "best_time": KILI_BEST_TIME,
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain tents",
        "best_for": "Fit hikers short on time who still want the scenic route",
        "price_from": 1950,
        "tips_note": "Tips not included – $350 per climber, shared among the crew.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": False,
        "sort_order": 50,
        "photo": "13-kili.jpg",
        "destinations": ["kilimanjaro", "moshi"],
        "price_tiers": tiers(
            ("1 person (private)", 2550), ("2 people", 2150), ("4–6 people", 1950), ("7+ people", 1850),
            best="4–6 people"),
        "itinerary": [
            day("Day 1", "Londorossi Gate to Mti Mkubwa Camp", "Rainforest walk to 'Big Tree' Camp.",
                2650, "6 km", "3–4 hours", "Rainforest"),
            day("Day 2", "Mti Mkubwa to Shira 1 Camp", "Through giant heather onto the Shira Ridge.",
                3500, "8 km", "5–6 hours", "Heath & moorland"),
            day("Day 3", "Shira 1 to Shira 2 Camp", "An easy crossing of the Shira Plateau.",
                3850, "7 km", "4–5 hours", "Heath & moorland"),
            day("Day 4", "Shira 2 to Barranco Camp via Lava Tower",
                "Up to Lava Tower (4,630m) for lunch, down to Barranco to sleep.",
                3960, "10 km", "6–8 hours", "Alpine desert"),
            day("Day 5", "Barranco Camp to Barafu Camp via Karanga",
                "The Barranco Wall, lunch at Karanga and on to base camp – a long but rewarding day.",
                4670, "9 km", "7–8 hours", "Alpine desert"),
            day("Day 6", "Barafu Camp to SUMMIT Uhuru Peak to Mweka Camp", SUMMIT_NIGHT,
                5895, "5 km up · 12 km down", "12–16 hours", "Arctic summit"),
            day("Day 7", "Mweka Camp to Mweka Gate – return to Moshi/Arusha", "Final descent and transfer back.",
                1640, "10 km", "3–4 hours", "Rainforest"),
        ],
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
        "why": "The fastest, most affordable way to the top – best if you are already acclimatized.",
        "overview": (
            "The classic Marangu hut route without the extra acclimatization day. You sleep in the Mandara, "
            "Horombo and Kibo huts and reach Uhuru Peak on the fourth night.\n\n"
            "Five days is a fast ascent, so this version is best if you are short on time or already used to "
            "altitude – for example after climbing Mount Meru. If this is your first time high up, we recommend "
            "the 6-day Marangu."
        ),
        "highlights": (
            "Huts with beds and mattresses\n"
            "The lowest price on Kilimanjaro\n"
            "Great after a Mount Meru climb"
        ),
        "difficulty": "demanding",
        "best_time": KILI_BEST_TIME,
        "max_altitude": "5,895m – Uhuru Peak",
        "accommodation": "Mountain huts (beds & mattresses)",
        "best_for": "Travellers short on time or already acclimatized",
        "price_from": 1600,
        "tips_note": "Tips not included – $350 total.",
        "extra_notes": KILI_EXTRAS,
        "is_featured": False,
        "sort_order": 60,
        "photo": "81-kili.jpg",
        "destinations": ["kilimanjaro", "moshi"],
        "price_tiers": tiers(
            ("1 person (private)", 2100), ("2 people", 1750), ("4–6 people", 1600), ("7+ people", 1500),
            best="4–6 people"),
        "itinerary": [
            day("Day 1", "Marangu Gate to Mandara Hut", "Rainforest walk to the Mandara huts.",
                2720, "8 km", "4–5 hours", "Rainforest"),
            day("Day 2", "Mandara Hut to Horombo Hut", "Through moorland with views of Kibo and Mawenzi.",
                3720, "12 km", "6–8 hours", "Heath & moorland"),
            day("Day 3", "Horombo Hut to Kibo Hut", "Across the alpine desert Saddle to Kibo Hut.",
                4700, "10 km", "6–7 hours", "Alpine desert"),
            day("Day 4", "Kibo Hut to SUMMIT Uhuru Peak to Horombo Hut", SUMMIT_NIGHT,
                5895, "6 km up · 15 km down", "12–15 hours", "Arctic summit"),
            day("Day 5", "Horombo Hut to Marangu Gate – return to Moshi/Arusha", "Final descent and transfer back.",
                1860, "20 km", "6–7 hours", "Rainforest"),
        ],
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
        "why": "A real mountain adventure with wildlife on the trail – and the perfect warm-up for Kilimanjaro.",
        "overview": (
            "Mount Meru is Kilimanjaro's dramatic little sister – a steep volcanic cone rising out of Arusha "
            "National Park. Because the lower slopes are full of wildlife, an armed park ranger walks with your "
            "group, and it is normal to pass giraffes, buffalo, warthogs and colobus monkeys on the first day.\n\n"
            "You sleep in comfortable mountain huts at Miriakamba and Saddle Hut. On day two there is time for an "
            "afternoon climb of Little Meru (3,820m), with Kilimanjaro on the horizon at sunset.\n\n"
            "Summit night follows a narrow, exciting ridge along the rim of Meru's huge collapsed crater, with the "
            "ash cone far below. You reach Socialist Peak as the sun comes up behind Kilimanjaro – one of the best "
            "sunrise views in Africa. Meru is also the ideal acclimatization climb before Kilimanjaro: see our "
            "Meru + Kilimanjaro combo."
        ),
        "highlights": (
            "Walk among giraffes and buffalo with an armed ranger\n"
            "Sleep in mountain huts\n"
            "Optional sunset climb of Little Meru (3,820m)\n"
            "Dramatic crater-rim ridge on summit night\n"
            "Sunrise over Kilimanjaro from Socialist Peak"
        ),
        "difficulty": "moderate",
        "best_time": "June – October and December – February (dry seasons).",
        "max_altitude": "4,566m – Socialist Peak",
        "accommodation": "Mountain huts",
        "best_for": "Acclimatization before Kilimanjaro, wildlife lovers, quieter trails",
        "price_from": 1100,
        "tips_note": "Tips not included – $200 total.",
        "is_featured": True,
        "sort_order": 10,
        "photo": "66-landscape.jpg",
        "destinations": ["mount-meru", "arusha"],
        "price_tiers": tiers(
            ("1 person (private)", 1400), ("2 people", 1200), ("4–6 people", 1100), best="4–6 people"),
        "itinerary": [
            day("Day 1", "Momella Gate to Miriakamba Hut",
                "From Momella Gate (1,500m) your ranger leads you through open grassland and forest where giraffe, "
                "buffalo and warthog graze, past a giant fig-tree arch and a waterfall, to Miriakamba Hut.",
                2514, "10 km", "4–5 hours", "Forest & grassland"),
            day("Day 2", "Miriakamba Hut to Saddle Hut",
                "A steep morning climb through beautiful forest hung with lichen to Saddle Hut. In the afternoon, "
                "an optional climb of Little Meru (3,820m) for sunset views of Kilimanjaro.",
                3570, "4 km", "3–4 hours", "Heath & moorland"),
            day("Day 3", "Saddle Hut to SUMMIT Socialist Peak (4,566m) to Miriakamba Hut",
                "A 1am start up to Rhino Point and along the narrow crater rim, with the ash cone below you, to "
                "Socialist Peak at sunrise. Then descend all the way to Miriakamba Hut.",
                4566, "12 km", "10–12 hours", "Alpine summit"),
            day("Day 4", "Miriakamba Hut to Momella Gate – return to Arusha",
                "An easy morning walk down to Momella Gate, often with more wildlife, and a short drive back to "
                "Arusha.",
                1500, "10 km", "2–3 hours", "Forest & grassland"),
        ],
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
        "why": "The same summit and sunrise as the 4-day trek, in one day less.",
        "overview": (
            "The 3-day Meru trek follows the same trail to Socialist Peak as the 4-day version, but after the "
            "summit you descend all the way to Momella Gate in one long day.\n\n"
            "It is a big summit day, so this trek suits fit hikers. If you are using Meru to acclimatize for "
            "Kilimanjaro, choose the 4-day version."
        ),
        "highlights": (
            "Wildlife walk with an armed ranger\n"
            "Crater-rim ridge and sunrise over Kilimanjaro\n"
            "Done in three days"
        ),
        "difficulty": "challenging",
        "best_time": "June – October and December – February (dry seasons).",
        "max_altitude": "4,566m – Socialist Peak",
        "accommodation": "Mountain huts",
        "best_for": "Fit hikers short on time",
        "price_from": 900,
        "tips_note": "Tips not included – $200 total.",
        "is_featured": False,
        "sort_order": 20,
        "photo": "42-landscape.jpg",
        "destinations": ["mount-meru", "arusha"],
        "price_tiers": tiers(
            ("1 person (private)", 1200), ("2 people", 1000), ("4–6 people", 900), best="4–6 people"),
        "itinerary": [
            day("Day 1", "Momella Gate to Miriakamba Hut", "Forest and grassland walk with wildlife.",
                2514, "10 km", "4–5 hours", "Forest & grassland"),
            day("Day 2", "Miriakamba Hut to Saddle Hut", "Climb to Saddle Hut. Optional walk up Little Meru.",
                3570, "4 km", "3–4 hours", "Heath & moorland"),
            day("Day 3", "Saddle Hut to SUMMIT Socialist Peak to Momella Gate – return to Arusha",
                "Summit at sunrise along the crater rim, then a long descent all the way to Momella Gate.",
                4566, "22 km", "12–14 hours", "Alpine summit"),
        ],
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
        "why": "The best preparation for Kilimanjaro is another mountain – and you get a second summit.",
        "overview": (
            "This is the combination serious climbers choose. You start on Mount Meru: four days of wildlife, "
            "mountain huts and a summit at 4,566m. By the time you come down, your body has already spent nights "
            "above 3,500m and touched 4,500m.\n\n"
            "Then you start the 7-day Machame Route on Kilimanjaro. Already acclimatized, you feel stronger "
            "every day, and summit night to Uhuru Peak is noticeably easier. Booking both together saves you "
            "$200 per person."
        ),
        "highlights": (
            "Two summits: Socialist Peak (4,566m) and Uhuru Peak (5,895m)\n"
            "The best acclimatization you can get\n"
            "Wildlife walks on Meru, five climate zones on Kilimanjaro\n"
            "Save $200 per person"
        ),
        "difficulty": "demanding",
        "best_time": KILI_BEST_TIME,
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
        "destinations": ["mount-meru", "kilimanjaro", "arusha", "moshi"],
        "price_tiers": [],
        "itinerary": [
            day("Day 1–4", "Mount Meru – Momella Gate to Socialist Peak and back",
                "Miriakamba Hut, Saddle Hut, summit of Socialist Peak (4,566m) at sunrise and back down to Momella "
                "Gate, with wildlife on the lower slopes.",
                4566, "", "4 days", "Mount Meru"),
            day("Day 5–11", "Kilimanjaro – Machame Route",
                "Machame Camp, Shira, Lava Tower & Barranco, the Barranco Wall, Karanga, Barafu, Uhuru Peak "
                "(5,895m) at sunrise and down via Mweka.",
                5895, "", "7 days", "Kilimanjaro"),
        ],
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
        "why": "Three parks, three completely different landscapes, and a real chance of the Big Five.",
        "overview": (
            "Short on time, or looking for the perfect add-on after your climb? This safari packs three of "
            "northern Tanzania's best parks into three days, all within easy reach of Arusha.\n\n"
            "Tarangire is elephant country: huge herds gather along the river beneath ancient baobab trees. "
            "Day two is the highlight – a full game drive on the floor of Ngorongoro Crater, a 600-metre-deep "
            "volcanic bowl where lions, elephants, buffalo, hippos and the rare black rhino all live together. "
            "On the way home you stop at Lake Manyara, famous for flamingos, baboon troops and lions that climb "
            "trees."
        ),
        "highlights": (
            "Big elephant herds and baobabs in Tarangire\n"
            "A full day inside Ngorongoro Crater – chance of the Big Five\n"
            "Flamingos and tree-climbing lions at Lake Manyara\n"
            "Perfect after a Kilimanjaro or Meru climb"
        ),
        "difficulty": "easy",
        "best_time": SAFARI_BEST_TIME,
        "max_altitude": "",
        "accommodation": "Lodge / tented camp",
        "best_for": "Short trips and add-ons after a climb",
        "price_from": 800,
        "tips_note": "Guide tips not included – $20 per day per group.",
        "is_featured": True,
        "sort_order": 10,
        "photo": "54-landscape.jpg",
        "destinations": ["tarangire", "ngorongoro", "lake-manyara", "arusha"],
        "price_tiers": tiers(
            ("1 person (private)", 1200), ("2 people", 900), ("4–6 people", 800), ("7+ people", 750),
            best="4–6 people"),
        "itinerary": [
            day("Day 1", "Arusha to Tarangire National Park",
                "Pickup in Arusha and a drive to Tarangire. Afternoon game drive along the Tarangire River, where "
                "elephants, giraffes, zebras and lions come to drink beneath giant baobabs.",
                None, "~120 km", "2 hours drive", "Game drive"),
            day("Day 2", "Ngorongoro Crater",
                "An early descent 600 metres down into the crater for a full day of game viewing. Lunch by a hippo "
                "pool, then search for the black rhino before climbing back to the rim.",
                None, "~150 km", "Full day", "Game drive"),
            day("Day 3", "Lake Manyara – return to Arusha",
                "Morning game drive at Lake Manyara: groundwater forest, baboons, flamingos on the lake and, with "
                "luck, lions resting in the trees. Drive back to Arusha in the afternoon.",
                None, "~130 km", "Half-day drive", "Game drive"),
        ],
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
        "why": "The sweet spot: enough time to reach the Serengeti and sleep there, with Tarangire and Ngorongoro on "
               "the way.",
        "overview": (
            "Four days is the sweet spot for a first safari. It gives you time to drive deep into the Serengeti "
            "and spend a night in the middle of the endless plains – falling asleep to the sound of lions is "
            "something you never forget.\n\n"
            "You start in Tarangire with its elephants and baobabs, then cross the Ngorongoro highlands to the "
            "Central Serengeti, home to big cats all year round. The final day is spent on the floor of "
            "Ngorongoro Crater, looking for the Big Five, before driving back to Arusha."
        ),
        "highlights": (
            "A night inside the Serengeti\n"
            "Big cats on the Central Serengeti plains\n"
            "Full game drive in Ngorongoro Crater\n"
            "Elephants and baobabs in Tarangire"
        ),
        "difficulty": "easy",
        "best_time": SAFARI_BEST_TIME,
        "max_altitude": "",
        "accommodation": "Lodge / tented camp",
        "best_for": "First-time safari travellers",
        "price_from": 1100,
        "tips_note": "Guide tips not included – $20 per day per group.",
        "is_featured": True,
        "sort_order": 20,
        "photo": "34-safari.jpg",
        "destinations": ["tarangire", "serengeti", "ngorongoro", "arusha"],
        "price_tiers": tiers(
            ("1 person (private)", 1600), ("2 people", 1250), ("4–6 people", 1100), ("7+ people", 1000),
            best="4–6 people"),
        "itinerary": [
            day("Day 1", "Arusha to Tarangire National Park",
                "Drive to Tarangire for an afternoon game drive among elephants and baobabs.",
                None, "~120 km", "2 hours drive", "Game drive"),
            day("Day 2", "Tarangire to Central Serengeti",
                "Climb into the Ngorongoro highlands, stop at the crater viewpoint, then drop down onto the "
                "Serengeti plains with a game drive all the way to camp.",
                None, "~330 km", "Full day", "Game drive"),
            day("Day 3", "Serengeti to Ngorongoro",
                "Sunrise game drive in the Serengeti when the cats are most active, then drive to the crater rim.",
                None, "~150 km", "Full day", "Game drive"),
            day("Day 4", "Ngorongoro Crater – return to Arusha",
                "Descend into the crater for a game drive on its floor, then drive back to Arusha.",
                None, "~190 km", "Full day", "Game drive"),
        ],
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
        "why": "All four great parks of northern Tanzania, with time to really explore the Serengeti.",
        "overview": (
            "This is the full northern Tanzania experience. Two whole days in the Serengeti give you time to "
            "follow the herds and the predators that follow them, instead of passing through.\n\n"
            "The Great Migration – over a million wildebeest with zebras and gazelles – moves around the "
            "Serengeti through the year. Your guide keeps track of where the herds are and plans your game "
            "drives to find them. Add Tarangire's elephants, a day in Ngorongoro Crater and the flamingos of Lake "
            "Manyara, and you have seen all four of the north's great parks."
        ),
        "highlights": (
            "Two full days in the Serengeti\n"
            "Follow the Great Migration (route planned to the season)\n"
            "Ngorongoro Crater game drive\n"
            "Tarangire and Lake Manyara too – all four great parks"
        ),
        "difficulty": "easy",
        "best_time": SAFARI_BEST_TIME,
        "max_altitude": "",
        "accommodation": "Lodge / tented camp",
        "best_for": "Wildlife lovers and photographers",
        "price_from": 1400,
        "tips_note": "Guide tips not included – $20 per day per group.",
        "is_featured": True,
        "sort_order": 30,
        "photo": "40-safari.jpg",
        "destinations": ["tarangire", "serengeti", "ngorongoro", "lake-manyara", "arusha"],
        "price_tiers": tiers(
            ("1 person (private)", 2000), ("2 people", 1600), ("4–6 people", 1400), ("7+ people", 1300),
            best="4–6 people"),
        "itinerary": [
            day("Day 1", "Arusha to Tarangire National Park", "Afternoon game drive among elephants and baobabs.",
                None, "~120 km", "2 hours drive", "Game drive"),
            day("Day 2–3", "Serengeti – two full days",
                "Drive into the Serengeti and spend two days following the herds and big cats across the plains, "
                "with sunrise and sunset game drives.",
                None, "", "2 full days", "Game drive"),
            day("Day 4", "Ngorongoro Crater", "A game drive on the crater floor looking for the Big Five.",
                None, "~150 km", "Full day", "Game drive"),
            day("Day 5", "Lake Manyara – return to Arusha",
                "Morning game drive at Lake Manyara, then drive back to Arusha.",
                None, "~130 km", "Half-day drive", "Game drive"),
        ],
        "inclusions": SAFARI_INCLUDED,
        "exclusions": SAFARI_EXCLUDED,
    },
]


# ---------------------------------------------------------------- destinations

DESTINATIONS = [
    {
        "slug": "kilimanjaro", "name": "Mount Kilimanjaro", "swahili": "Mlima Kilimanjaro", "kind": "mountain",
        "map_key": "kilimanjaro", "photo": "10-kili.jpg", "sort_order": 10,
        "tagline": "The Roof of Africa – the highest free-standing mountain on Earth.",
        "size": "5,895m · Uhuru Peak", "known_for": "Summit at sunrise, five climate zones",
        "best_time": KILI_BEST_TIME,
        "intro": "Kilimanjaro rises alone from the plains of northern Tanzania, a giant snow-capped volcano you can "
                 "see from a hundred kilometres away. Its highest point, Uhuru Peak, is the summit of Africa – and "
                 "you can walk all the way there, with no ropes or technical climbing.",
        "body": "The mountain is made of three volcanic cones: Shira in the west, the jagged towers of Mawenzi in "
                "the east, and Kibo in the middle, with its crater, glaciers and Uhuru Peak. Kilimanjaro National "
                "Park protects 1,688 km² of it and is a UNESCO World Heritage Site.\n\n"
                "Climbing it is like walking from the equator to the Arctic in a week. You start in farmland and "
                "rainforest, cross giant heather and moorland, then an empty alpine desert, and finish among ice "
                "and snow. The key to reaching the top is going slowly – pole pole – and giving your body time to "
                "adjust to the altitude. Our guides have done it many times and set exactly the right pace.",
        "highlights": "Uhuru Peak (5,895m), the highest point in Africa\nFive climate zones in one climb\n"
                      "The Barranco Wall and Lava Tower\nGlaciers and the summit crater\n"
                      "Four routes to choose from: Machame, Lemosho, Marangu and Rongai",
        "wildlife": "Black-and-white colobus monkeys\nBlue monkeys\nGiant groundsels and lobelias\n"
                    "White-necked ravens\nFour-striped grass mice at camp",
    },
    {
        "slug": "mount-meru", "name": "Mount Meru", "swahili": "Mlima Meru", "kind": "mountain",
        "map_key": "meru", "photo": "66-landscape.jpg", "sort_order": 20,
        "tagline": "Tanzania's second-highest peak, in the heart of Arusha National Park.",
        "size": "4,566m · Socialist Peak", "known_for": "Wildlife on the trail, crater-rim summit",
        "best_time": "June – October and December – February (dry seasons).",
        "intro": "Mount Meru is the steep volcano that towers over Arusha town. At 4,566m it is Tanzania's "
                 "second-highest mountain, and it is one of the most beautiful – and least crowded – climbs in East "
                 "Africa.",
        "body": "Meru sits inside Arusha National Park (552 km²), so the lower slopes are full of wildlife and an "
                "armed ranger walks with every group. Giraffes, buffalo, warthogs and colobus monkeys are common on "
                "the first day.\n\n"
                "Long ago the top of the volcano collapsed, leaving a huge horseshoe crater with a young ash cone "
                "inside. The summit trail runs along the narrow rim of that crater, and at sunrise you watch the "
                "sun come up behind Kilimanjaro. Because it is high enough to prepare your body for altitude, many "
                "climbers do Meru first and Kilimanjaro straight after.",
        "highlights": "Socialist Peak (4,566m)\nThe crater rim and ash cone\nSunrise over Kilimanjaro\n"
                      "Comfortable mountain huts\nPerfect acclimatization before Kilimanjaro",
        "wildlife": "Giraffe\nCape buffalo\nWarthog\nBlack-and-white colobus\nBushbuck\nMany forest birds",
    },
    {
        "slug": "serengeti", "name": "Serengeti National Park", "swahili": "Serengeti – Siringet", "kind": "park",
        "map_key": "serengeti", "photo": "39-safari.jpg", "sort_order": 30,
        "tagline": "Endless plains and the greatest wildlife show on Earth.",
        "size": "14,763 km²", "known_for": "The Great Migration and big cats",
        "best_time": "All year. Calving in the south in January – February; river crossings in the north around "
                     "July – September.",
        "intro": "The name comes from the Maasai word Siringet – 'the place where the land runs on forever'. Stand "
                 "on the plains of the Serengeti and you understand why: golden grass stretches to the horizon in "
                 "every direction, broken only by acacia trees and granite kopjes.",
        "body": "Serengeti National Park covers 14,763 km² and is a UNESCO World Heritage Site. It is home to the "
                "Great Migration: more than a million wildebeest, with hundreds of thousands of zebras and "
                "gazelles, moving in a huge circle through the year in search of fresh grass and water.\n\n"
                "Where the herds go, the predators follow. The Serengeti has one of the largest lion populations in "
                "Africa, and cheetahs and leopards are seen regularly, especially in the central Seronera area. "
                "Our guides follow the movements of the herds and plan your game drives to put you in the right "
                "place.",
        "highlights": "The Great Migration\nLions, cheetahs and leopards in Seronera\nGranite kopjes and acacia "
                      "plains\nHot-air balloon safaris at sunrise (optional extra)\nNights in camp under the stars",
        "wildlife": "Lion\nCheetah\nLeopard\nWildebeest\nZebra\nElephant\nGiraffe\nHyena\nThomson's gazelle",
    },
    {
        "slug": "ngorongoro", "name": "Ngorongoro Crater", "swahili": "Kreta ya Ngorongoro", "kind": "park",
        "map_key": "ngorongoro", "photo": "50-landscape.jpg", "sort_order": 40,
        "tagline": "A lost world inside a volcano – home of the Big Five.",
        "size": "~260 km² crater floor", "known_for": "Black rhino and the Big Five",
        "best_time": "All year – wildlife lives in the crater permanently.",
        "intro": "Ngorongoro is the largest unbroken volcanic caldera in the world: a giant bowl about 20 km across "
                 "and 600 metres deep, formed when a huge volcano collapsed millions of years ago. Today its floor is "
                 "one of the richest wildlife areas on the planet.",
        "body": "Around 25,000 large animals live inside the crater, protected by its steep walls. It is one of the "
                "best places in Africa to see the Big Five in a single day, and one of the last refuges of the "
                "endangered black rhino.\n\n"
                "The crater is part of the Ngorongoro Conservation Area, a UNESCO World Heritage Site where Maasai "
                "herders still graze their cattle alongside the wildlife. A day in the crater starts with a dramatic "
                "drive down the wall, includes a picnic by a hippo pool, and ends with the climb back up to the "
                "misty rim.",
        "highlights": "The Big Five in one day\nOne of the best places to see black rhino\nHippo pools and Lake "
                      "Magadi's flamingos\nViews from the crater rim\nMaasai culture in the conservation area",
        "wildlife": "Black rhino\nLion\nElephant\nBuffalo\nHippo\nSpotted hyena\nFlamingo\nGolden jackal",
    },
    {
        "slug": "tarangire", "name": "Tarangire National Park", "swahili": "Hifadhi ya Tarangire", "kind": "park",
        "map_key": "tarangire", "photo": "53-safari.jpg", "sort_order": 50,
        "tagline": "Land of giant baobabs and great elephant herds.",
        "size": "2,850 km²", "known_for": "Elephants and baobab trees",
        "best_time": "June – October, when animals crowd along the river.",
        "intro": "Tarangire is often the first stop on a northern Tanzania safari – and many guests say it was their "
                 "favourite. Its landscape is unlike any other park: rolling hills covered in ancient baobab trees, "
                 "some more than a thousand years old.",
        "body": "In the dry season the Tarangire River is the only water for miles around, and animals pour in from "
                "the surrounding plains. That is when Tarangire has some of the largest elephant herds in Africa, "
                "sometimes hundreds together.\n\n"
                "Lions, leopards and cheetahs follow the zebras and wildebeest that come to drink, and the park is "
                "a paradise for birdwatchers, with over 500 species recorded.",
        "highlights": "Huge elephant herds\nAncient baobab trees\nThe Tarangire River in the dry season\n"
                      "Over 500 bird species",
        "wildlife": "Elephant\nLion\nGiraffe\nZebra\nWildebeest\nLeopard\nPython\nLilac-breasted roller",
    },
    {
        "slug": "lake-manyara", "name": "Lake Manyara National Park", "swahili": "Ziwa Manyara", "kind": "park",
        "map_key": "manyara", "photo": "54-landscape.jpg", "sort_order": 60,
        "tagline": "Flamingos, forests and lions in the trees.",
        "size": "~650 km² (two-thirds is lake)", "known_for": "Tree-climbing lions and flamingos",
        "best_time": "All year. Birding is best November – April.",
        "intro": "Lake Manyara lies at the foot of the steep Rift Valley escarpment. In a small area it packs in "
                 "groundwater forest, grassy floodplains and a shallow soda lake that often turns pink with "
                 "flamingos.",
        "body": "The park is famous for its tree-climbing lions, which like to rest in the branches of acacia "
                "trees. Large troops of olive baboons live in the forest, and elephants, giraffes and hippos are "
                "common.\n\n"
                "Because it is close to Arusha and on the way to Ngorongoro, Lake Manyara is an easy and rewarding "
                "half-day game drive at the start or end of a safari.",
        "highlights": "Tree-climbing lions\nFlamingos on the soda lake\nThe Rift Valley escarpment\n"
                      "Groundwater forest and baboon troops",
        "wildlife": "Lion\nFlamingo\nOlive baboon\nElephant\nHippo\nGiraffe\nBlue monkey",
    },
    {
        "slug": "arusha", "name": "Arusha", "swahili": "Mji wa Arusha", "kind": "town",
        "map_key": "arusha", "photo": "55-safari.jpg", "sort_order": 70,
        "tagline": "The safari capital of Tanzania – and one of our two bases.",
        "size": "Gateway to the northern parks", "known_for": "Safari starts, markets and Mount Meru views",
        "best_time": "All year.",
        "intro": "Arusha is a lively green city at the foot of Mount Meru and the starting point for every safari "
                 "in northern Tanzania. It is one of our two bases.",
        "body": "Most of our safaris start here: we pick you up from your hotel or Kilimanjaro Airport (JRO), load "
                "the jeep and head out to Tarangire, Manyara, Ngorongoro and the Serengeti. Mount Meru treks start "
                "from Arusha National Park, just outside town.\n\n"
                "If you have a free day, Arusha has busy local markets, coffee farms on the slopes of Meru and "
                "craft shops full of Tanzanian art.",
        "highlights": "Start of every northern safari\nMount Meru and Arusha National Park nearby\nLocal markets and "
                      "coffee farms\nAbout an hour from Kilimanjaro Airport (JRO)",
        "wildlife": "",
    },
    {
        "slug": "moshi", "name": "Moshi", "swahili": "Mji wa Moshi", "kind": "town",
        "map_key": "moshi", "photo": "80-kili.jpg", "sort_order": 80,
        "tagline": "The friendly town at the foot of Kilimanjaro.",
        "size": "Gateway to Kilimanjaro", "known_for": "Kilimanjaro views, coffee and waterfalls",
        "best_time": "All year.",
        "intro": "Moshi is a small, relaxed town on the southern slopes of Kilimanjaro, and the base for most climbs. "
                 "On clear mornings the snowy summit fills the sky above the town.",
        "body": "Our team is from here. Before your climb we meet you in Moshi for a briefing and gear check, and the "
                "Machame and Marangu gates are less than an hour away.\n\n"
                "Around Moshi are coffee farms where you can pick, roast and taste your own coffee, the Materuni "
                "waterfalls and the turquoise Chemka hot springs – perfect for a rest day after the climb.",
        "highlights": "Briefing and gear check before your climb\nCoffee farms and Materuni waterfalls\n"
                      "Chemka hot springs\nViews of Kilimanjaro from town",
        "wildlife": "",
    },
]


# ---------------------------------------------------------------- FAQs

FAQS = {
    "kilimanjaro": [
        ("When is the best time to climb Kilimanjaro?",
         "The driest months are January to mid-March and June to October, and those are the most popular times. "
         "We run climbs all year – in the rainy months (April, May and November) the Rongai Route on the drier "
         "northern side is a good choice."),
        ("Do I need climbing experience?",
         "No. None of our routes need ropes or technical climbing – it is a long, high-altitude hike. You do need "
         "good fitness: regular walking, hiking or running in the months before your trip makes a big difference."),
        ("Which route should I choose?",
         "For the best chance of reaching the summit, choose the 8-day Lemosho. For great scenery at a lower price, "
         "the 7-day Machame. If you prefer a bed to a tent, the 6-day Marangu. For quiet trails or a rainy-season "
         "climb, the 7-day Rongai. Message us and we'll help you decide."),
        ("What about altitude sickness?",
         "Altitude affects everyone differently, and the best protection is going slowly and spending more days on "
         "the mountain. Our guides check how you are doing with a pulse oximeter, carry emergency oxygen and a "
         "first-aid kit, and will always put your safety first."),
        ("How much should I tip the crew?",
         "We recommend $350 per climber in total, shared among the guide, cook and porters. It is paid at the end "
         "of the climb and is an important part of the crew's income."),
        ("What gear do I need?",
         "Good broken-in hiking boots, warm layers, a down jacket, a warm sleeping bag, rain gear, gloves, a hat and "
         "a headlamp. If you don't have everything, we can rent you a sleeping bag, jacket and more for $80."),
        ("Do you arrange hotels and airport transfers?",
         "Yes. Airport pickup from Kilimanjaro Airport (JRO) is included, and we can book a hotel in Moshi or Arusha "
         "before and after your climb from $50 per night."),
    ],
    "mount-meru": [
        ("Is Mount Meru harder than Kilimanjaro?",
         "Meru is lower (4,566m vs 5,895m) so the altitude is easier, but the summit ridge is steep and narrow in "
         "places. Most people find it a great challenge and an ideal warm-up for Kilimanjaro."),
        ("Why does a ranger come with us?",
         "Meru is inside Arusha National Park, where buffalo, giraffes and other wild animals live on the lower "
         "slopes. An armed park ranger is required for every group to keep everyone safe."),
        ("Can I climb Meru and Kilimanjaro on the same trip?",
         "Yes – it's the best way to acclimatize. Our Meru + Kilimanjaro combo (Meru 4 days + Machame 7 days) costs "
         "$2,800 per person and saves you $200."),
        ("What tips are expected on Meru?",
         "We recommend $200 in total for the crew, paid at the end of the climb."),
    ],
    "safari": [
        ("When is the best time for a safari?",
         "Safaris are good all year. June to October is the dry season, when animals gather around water and are "
         "easiest to see. January and February are calving season in the southern Serengeti."),
        ("Will I see the Big Five?",
         "Ngorongoro Crater is one of the best places in Africa to see lions, elephants, buffalo, leopards and "
         "black rhino in a single day. Wildlife is wild, so nothing is guaranteed, but our guides know where to "
         "look."),
        ("What kind of vehicle do you use?",
         "A 4x4 safari jeep with a pop-up roof, so everyone has a window seat and can stand up for photos."),
        ("Where do we sleep?",
         "In lodges or tented camps inside or close to the parks, with all meals included. Tell us your budget "
         "and we'll recommend the best options."),
        ("Can I add a safari to my Kilimanjaro climb?",
         "Yes, and many of our guests do. The 3-day safari is perfect after a climb, and we handle the transfers "
         "between the two."),
        ("How much should I tip the safari guide?",
         "We recommend $20 per day per group for your guide."),
    ],
    "combo": [
        ("How does the combo work?",
         "You climb Mount Meru for 4 days, then start the 7-day Machame Route on Kilimanjaro. Meru prepares your "
         "body for altitude, so Kilimanjaro feels easier."),
        ("Is there a rest day between the two mountains?",
         "Tell us when you book – we can add a rest night in Arusha or Moshi between the two climbs."),
    ],
}


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
