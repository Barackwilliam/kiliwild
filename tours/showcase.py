"""Home-page showcase content: hero slides and the talking map of northern Tanzania."""

# Hero slideshow: (static image, Swahili word, English caption)
SLIDES = [
    ("img/slides/kilimanjaro.jpg", "Kilimanjaro", "Sunset camp below the Roof of Africa"),
    ("img/slides/lions.jpg", "Simba", "Lions resting in the Serengeti shade"),
    ("img/slides/elephants.jpg", "Tembo", "Elephants at the waterhole"),
    ("img/slides/crater.jpg", "Ngorongoro", "The great crater, home of the Big Five"),
    ("img/slides/migration.jpg", "Uhamaji", "The Great Migration crossing the river"),
    ("img/slides/maasai.jpg", "Utamaduni", "Meeting the Maasai, keepers of the plains"),
]

# Talking map. x/y are positions in the 960x720 map drawing (roughly longitude 33.6–37.9 E, latitude 1.2–4.5 S).
MAP_PLACES = [
    {
        "key": "kilimanjaro", "label": "Kilimanjaro", "lx": 0, "ly": -44, "anchor": "middle", "name": "Mount Kilimanjaro", "sw": "Mlima Kilimanjaro", "kind": "mountain",
        "x": 825, "y": 405, "photo": "img/map/kilimanjaro.jpg", "fact": "5,895m · Uhuru Peak",
        "say": "Jambo! I am Kilimanjaro, the Roof of Africa. At five thousand eight hundred and ninety five metres, "
               "I am the highest free-standing mountain in the world. Choose Machame, Lemosho, Marangu or Rongai, "
               "and our local crew will walk with you all the way to Uhuru Peak.",
        "link": ("tours:category", "kilimanjaro"), "cta": "See Kilimanjaro climbs",
    },
    {
        "key": "moshi", "label": "Moshi", "lx": 16, "ly": -10, "anchor": "start", "name": "Moshi", "sw": "Mji wa Moshi", "kind": "town",
        "x": 830, "y": 478, "photo": "img/map/moshi.jpg", "fact": "Our base at the foot of Kili",
        "say": "Karibu Moshi! This small, friendly town sits at the foot of Kilimanjaro. It is one of our two bases, "
               "and the start of every climb – the gate is less than an hour away.",
        "link": ("tours:about", None), "cta": "About our team",
    },
    {
        "key": "meru", "label": "Mt Meru", "lx": -16, "ly": -30, "anchor": "end", "name": "Mount Meru", "sw": "Mlima Meru", "kind": "mountain",
        "x": 688, "y": 440, "photo": "img/map/meru.jpg", "fact": "4,566m · Socialist Peak",
        "say": "I am Mount Meru, Kilimanjaro's little sister and Tanzania's second highest peak. Giraffes and buffalo "
               "walk my lower slopes, and I am the perfect warm-up before you climb Kili.",
        "link": ("tours:category", "mount-meru"), "cta": "See Mount Meru treks",
    },
    {
        "key": "arusha", "label": "Arusha", "lx": -16, "ly": -6, "anchor": "end", "name": "Arusha", "sw": "Mji wa Arusha", "kind": "town",
        "x": 668, "y": 486, "photo": "img/map/arusha.jpg", "fact": "Safari capital of Tanzania",
        "say": "Welcome to Arusha, the safari capital of Tanzania and our second base. Every safari starts here: "
               "we pick you up, load the jeep and head out to the parks.",
        "link": ("tours:category", "safari"), "cta": "See safaris",
    },
    {
        "key": "tarangire", "label": "Tarangire", "lx": 16, "ly": -16, "anchor": "start", "name": "Tarangire", "sw": "Hifadhi ya Tarangire", "kind": "park",
        "x": 540, "y": 618, "photo": "img/map/tarangire.jpg", "fact": "Land of giant baobabs",
        "say": "This is Tarangire, land of ancient baobab trees and some of the biggest elephant herds in Africa. "
               "It is the first stop on most of our safaris.",
        "link": ("tours:category", "safari"), "cta": "See safaris",
    },
    {
        "key": "manyara", "label": "Lake Manyara", "lx": 16, "ly": -14, "anchor": "start", "name": "Lake Manyara", "sw": "Ziwa Manyara", "kind": "park",
        "x": 492, "y": 520, "photo": "img/map/manyara.jpg", "fact": "Tree-climbing lions & flamingos",
        "say": "Lake Manyara! Pink flamingos crowd the shore, and if you are lucky you will find our famous "
               "tree-climbing lions resting in the branches.",
        "link": ("tours:category", "safari"), "cta": "See safaris",
    },
    {
        "key": "ngorongoro", "label": "Ngorongoro", "lx": -30, "ly": -6, "anchor": "end", "name": "Ngorongoro Crater", "sw": "Kreta ya Ngorongoro", "kind": "park",
        "x": 420, "y": 440, "photo": "img/map/ngorongoro.jpg", "fact": "The Big Five in one crater",
        "say": "Look down into the Ngorongoro Crater, a giant volcanic bowl twenty kilometres across. Lions, "
               "elephants, buffalo, leopards and the rare black rhino all live on its floor.",
        "link": ("tours:category", "safari"), "cta": "See safaris",
    },
    {
        "key": "serengeti", "label": "Serengeti", "lx": 16, "ly": -16, "anchor": "start", "name": "Serengeti", "sw": "Serengeti – Siringet", "kind": "park",
        "x": 262, "y": 250, "photo": "img/map/serengeti.jpg", "fact": "Endless plains & the Migration",
        "say": "Serengeti comes from the Maasai word Siringet – the place where the land runs on forever. "
               "Millions of wildebeest and zebra cross these plains every year in the Great Migration.",
        "link": ("tours:category", "safari"), "cta": "See safaris",
    },
]

TOUR_ORDER = ["kilimanjaro", "moshi", "meru", "arusha", "tarangire", "manyara", "ngorongoro", "serengeti"]

# "Journey to the summit" scroll story on the home page: Kilimanjaro's climate zones, bottom to top.
ZONES = [
    {"sw": "Msitu wa mvua", "name": "Rainforest", "range": "1,800 – 2,800m", "low": 1800, "high": 2800,
     "day": "Day 1", "color": "#0f2a1c", "photo": "img/zones/rainforest.jpg",
     "text": "Moss-draped trees, misty trails and the call of black-and-white colobus monkeys. "
             "Every climb begins in the green heart of the mountain."},
    {"sw": "Nyika", "name": "Heath & moorland", "range": "2,800 – 4,000m", "low": 2800, "high": 4000,
     "day": "Day 2 – 3", "color": "#28301a", "photo": "img/zones/moorland.jpg",
     "text": "The forest opens up into giant heather, groundsels and lobelias – plants found almost nowhere "
             "else on Earth – with Kibo glowing ahead."},
    {"sw": "Jangwa la juu", "name": "Alpine desert", "range": "4,000 – 5,000m", "low": 4000, "high": 5000,
     "day": "Day 3 – 5", "color": "#3a2a1c", "photo": "img/zones/alpine.jpg",
     "text": "A silent, lunar landscape of rock and scree. Hot sun by day, frost by night – "
             "and Lava Tower, Barranco Wall and Barafu Camp."},
    {"sw": "Barafu", "name": "Arctic summit zone", "range": "5,000 – 5,756m", "low": 5000, "high": 5756,
     "day": "Day 6 · midnight", "color": "#18283a", "photo": "img/zones/arctic.jpg",
     "text": "Glaciers, ice and thin air – about half the oxygen of sea level. You climb by headlamp, "
             "pole pole, towards the crater rim."},
    {"sw": "Paa la Afrika", "name": "Uhuru Peak", "range": "5,895m", "low": 5756, "high": 5895,
     "day": "Day 6 · sunrise", "color": "#3b2412", "photo": "img/zones/summit.jpg",
     "text": "The sun rises over the clouds and the whole continent lies below you. "
             "You are standing on the Roof of Africa."},
]

# Horizontal wildlife gallery on the home page.
WILDLIFE = [
    {"sw": "Simba", "name": "Lion", "where": "Serengeti", "photo": "img/wild/simba.jpg",
     "fact": "The Serengeti is home to one of Africa's largest lion populations."},
    {"sw": "Tembo", "name": "Elephant", "where": "Tarangire", "photo": "img/wild/tembo.jpg",
     "fact": "In the dry season, Tarangire's herds can number in the hundreds."},
    {"sw": "Chui", "name": "Leopard", "where": "Seronera, Serengeti", "photo": "img/wild/chui.jpg",
     "fact": "The master of stealth. Look up – leopards love resting in the trees."},
    {"sw": "Faru", "name": "Black rhino", "where": "Ngorongoro Crater", "photo": "img/wild/faru.jpg",
     "fact": "Ngorongoro Crater is one of the best places on Earth to see this rare giant."},
    {"sw": "Twiga", "name": "Giraffe", "where": "Everywhere we go", "photo": "img/wild/twiga.jpg",
     "fact": "Tanzania's national animal, and the tallest animal on the planet."},
    {"sw": "Duma", "name": "Cheetah", "where": "Serengeti plains", "photo": "img/wild/duma.jpg",
     "fact": "The fastest land animal, hunting across the open grass of the Serengeti."},
    {"sw": "Nyumbu", "name": "Wildebeest", "where": "The Great Migration", "photo": "img/wild/nyumbu.jpg",
     "fact": "Over a million of them move around the Serengeti every year."},
]
