# region Map / Zone names
MAPS = [
    'World Map', '_unknown_0', '_unknown_1', 'Central Village Map', 'Lost Shrine Area Map', 'Lost Shrine Map',
    'The Aerie Map', 'Seafront Map', 'Desert Map', 'Facade Map', 'Barren Temple Map', 'Junk Heap Area Map',
    'Junk Heap Map', 'Manor Map', 'Forest of Myth Map', 'Underground Facility Map', '_unknown_2',
    'Shadowlord\'s Castle Map', '_unknown_3', 'Northern Plains Map', 'Southern Plains Map', 'Eastern Road Map',
    'Beneath the Forest of Myth Map', 'Toyko Map',
]

MAP_ZONES = [
    'NO_IMAGE_AREA_00',
    'B_CASTLE_FIELD_01', 'B_CASTLE_FIELD_011_D', 'B_CASTLE_FIELD_02', 'B_CASTLE_FIELD_021_D', 'B_CASTLE_FIELD_03',
    'B_CASTLE_FIELD_04', 'B_CASTLE_FIELD_041_D', 'B_CASTLE_FIELD_10',
    'B_CENTER_LIBRARY_01', 'B_CENTER_LIBRARY_011_D',
    'A_CENTER_VILLAGE_01', 'B_CENTER_VILLAGE_01', 'A_CENTER_VILLAGE_21',
    'A_CLIFF_VILLAGE_01', 'B_CLIFF_VILLAGE_01', 'E_CLIFF_VILLAGE_01', 'B_CLIFF_VILLAGE_02', 'B_CLIFF_VILLAGE_21',
    'A_DESERT_FIELD_01', 'B_DESERT_FIELD_01', 'A_DESERT_FIELD_02', 'B_DESERT_FIELD_02',
    'A_DESERT_TEMPLE_01', 'B_DESERT_TEMPLE_01', 'B_DESERT_TEMPLE_011_D', 'B_DESERT_TEMPLE_012_D',
    'B_DESERT_TEMPLE_013_D', 'B_DESERT_TEMPLE_014_D',
    'A_DESERT_TEMPLE_02', 'B_DESERT_TEMPLE_02',
    'A_DESERT_TOWN_01', 'B_DESERT_TOWN_01', 'B_DESERT_TOWN_011_D',
    'A_EAST_FIELD_01', 'B_EAST_FIELD_01',
    'A_FOREST_FIELD_01', 'B_FOREST_FIELD_01', 'C_FOREST_FIELD_01', 'D_FOREST_FIELD_01',
    'E_FOREST_FIELD_01', 'E_FOREST_FIELD_02', 'E_FOREST_FIELD_03', 'E_FOREST_FIELD_04',
    'B_MERMAID_FIELD_01', 'B_MERMAID_FIELD_02', 'B_MERMAID_FIELD_03',
    'A_MOUNT_FIELD_01', 'B_MOUNT_FIELD_01',
    'A_MOUNT_ROBOT_01', 'B_MOUNT_ROBOT_01', 'A_MOUNT_ROBOT_01_1', 'A_MOUNT_ROBOT_01_2',
    'A_MOUNT_ROBOT_02', 'B_MOUNT_ROBOT_02',
    'A_MOUNT_ROBOT_03', 'B_MOUNT_ROBOT_03',
    'A_MOUNT_ROBOT_04', 'B_MOUNT_ROBOT_04', 'B_MOUNT_ROBOT_041_D',
    'A_MOUNT_ROBOT_10', 'B_MOUNT_ROBOT_10', 'B_MOUNT_ROBOT_101_D', 'A_MOUNT_ROBOT_10_1', 'A_MOUNT_ROBOT_10_2',
    'A_MOUNT_ROBOT_10_3',
    'A_NORTH_FIELD_01', 'B_NORTH_FIELD_01', 'E_NORTH_FIELD_01', 'A_NORTH_FIELD_21',
    'A_SEASIDE_TOWN_01', 'B_SEASIDE_TOWN_01', 'B_SEASIDE_TOWN_011_D',
    'A_SOUTH_FIELD_01', 'B_SOUTH_FIELD_01', 'B_SOUTH_FIELD_011_D', 'A_SOUTH_FIELD_21',
    'A_SOUTH_MANSION_01', 'B_SOUTH_MANSION_01', 'A_SOUTH_MANSION_02', 'B_SOUTH_MANSION_02', 'B_SOUTH_MANSION_021_D',
    'B_SOUTH_UNDERGROUND_01', 'B_SOUTH_UNDERGROUND_01_1', 'B_SOUTH_UNDERGROUND_01_2', 'B_SOUTH_UNDERGROUND_01_3',
    'B_SOUTH_UNDERGROUND_02', 'B_SOUTH_UNDERGROUND_021_D',
    'A_STONE_FIELD_01', 'B_STONE_FIELD_01', 'A_STONE_FIELD_01_1', 'A_STONE_FIELD_01_2', 'A_STONE_FIELD_02',
    'B_STONE_FIELD_02', 'B_STONE_FIELD_021_D',
    'A_STONE_TEMPLE_01', 'B_STONE_TEMPLE_01', 'A_STONE_TEMPLE_01_1', 'A_STONE_TEMPLE_01_2', 'A_STONE_TEMPLE_01_3',
    'C_TOKYO_FIELD_01',
]

MAP_ZONE_MAP = {
    'CENTER_VILLAGE': 'NieR\'s Village',
    'CENTER_LIBRARY': 'Library',
    'CLIFF_VILLAGE': 'The Aerie',
    'STONE_TEMPLE': 'Lost Shrine',
    'STONE_FIELD': 'Lost Shrine: Roof',
    'SEASIDE_TOWN': 'Seafront',
    'DESERT_FIELD': 'Desert',
    'DESERT_TOWN': 'Facade',
    'DESERT_TEMPLE': 'Barren Temple',
    'MOUNT_ROBOT': 'Junk Heap',
    'MOUNT_FIELD': 'Junk Heap: Outside',
    'SOUTH_MANSION': 'Manor',
    'FOREST_FIELD': 'Forest of Myth',
    'SOUTH_UNDERGROUND': 'Underground Facility',
    'CASTLE_FIELD': 'Shadowlord\'s Castle',
    'NORTH_FIELD': 'Northern Plains',
    'SOUTH_FIELD': 'Southern Plains',
    'EAST_FIELD': 'Eastern Road',
    'TOKYO_FIELD': 'Tokyo',
    'MERMAID_FIELD': 'Wrecked Ship Interior',
}

# endregion

# region Abilities, Weapons, and Words

ABILITIES = [
    'None',
    'Defend',
    'Evade',
    'Dark Blast',
    'Dark Phantasm',
    'Dark Hand',
    'Dark Lance',
    'Dark Whirlwind',
    'Dark Gluttony',
    'Dark Wall',
    'Dark Execution',
]

SWORDS_1H = [
    'Nameless Blade',
    'Phoenix Dagger',
    'Beastbain',
    "Labyrinth's Whisper",
    "Fool's Embrace",
    'Ancient Overlord',
    'Rebirth',
    'Earth Wyrms Claw',
    'Nirvana Dagger',
    'Moonrise',
    'Blade of Treachery',
    'Lily Leaf Sword',
    'Faith',
    'Iron Pipe',
    "Kainé's Sword",
    'Virtuous Contract',
    'Cruel Oath',
]

SWORDS_2H = [
    'Kusanagi',
    'Phoenix Sword',
    'Beastlord',
    "Labyrinth's Song",
    "Fool's Lament",
    'Fang of the Twins',
    'Axe of Beheading',
    'Vile Axe',
    'Iron Will',
    'Virtuous Treaty',
]

SPEARS = [
    'Transience',
    'Phoenix Spear',
    'Beastcurse',
    "Labyrinth's Shout",
    "Fool's Accord",
    'The Devil Queen',
    'Sunrise',
    'Spear of the Usurper',
    'Dragoon Lance',
    "Captain's Holy Spear",
    'Virtuous Dignity',
]

WORDS = [
    'Pah', 'Paha', 'Pahi', 'Paho', 'Pahu', 'Pahal', 'Pahil', 'Pahol', 'Pahul', 'Pahuloth',
    'Var', 'Vara', 'Vari', 'Varo', 'Varu', 'Varal', 'Varil', 'Varol', 'Varul', 'Varuloth',
    'Geb', 'Geba', 'Gebi', 'Gebo', 'Gebu', 'Gebal', 'Gebil', 'Gebol', 'Gebul', 'Gebuloth',
    'Ul', 'Ula', 'Uli', 'Ulo', 'Ulu', 'Ulal', 'Ulil', 'Ulol', 'Ulul', 'Ululoth',
    'Hod', 'Hoda', 'Hodi', 'Hodo', 'Hodu', 'Hodal', 'Hodil', 'Hodol', 'Hodul', 'Hoduloth',
    'Bes', 'Besa', 'Besi', 'Beso', 'Besu', 'Besal', 'Besil', 'Besol', 'Besul', 'Besuloth',
    '', '', '', '',
    'Lug', 'Lugir', 'Luges', 'Lugka', 'Lugza', 'Lugira', 'Lugesra', 'Lugkarr', 'Lugzarr', 'Lugzarken',
    'Ot', 'Otir', 'Otes', 'Otka', 'Otza', 'Otira', 'Otesra', 'Otkarr', 'Otzarr', 'Otzarken',
    'Mah', 'Mahir', 'Mahes', 'Mahka', 'Mahza', 'Mahira', 'Mahesra', 'Mahkarr', 'Mahzarr', 'Mahzarken',
    'Ashur', 'Ashurir', 'Ashures', 'Ashurka', 'Ashurza', 'Ashurira', 'Ashuresra', 'Ashurkarr', 'Ashurzarr', 'Ashurzarken',
    'Kon', 'Konir', 'Kones', 'Konka', 'Konza', 'Konira', 'Konesra', 'Konkarr', 'Konzarr', 'Konzarken',
    'Sol', 'Solir', 'Soles', 'Solka', 'Solza', 'Solira', 'Solesra', 'Solkarr', 'Solzarr', 'Solzarken',
    'Ashurfarra',
    '', '', '',
]

# endregion

# region Tutorials

TUTORIALS = [
    'Controls',
    'Combos',
    'Dark Blast', 'Dark Phantasm', 'Dark Hand', 'Dark Lance',
    'Dark Whirlwind', 'Dark Gluttony', 'Dark Wall', 'Dark Execution',
    'Maps',
    'Interactions',
    'Attack Gauges',
    'Saving',
    'Quests',
    'Weapon Types',
    'Cultivating Plants',
    'Forging Weapons',
    'Shops',
    'Mine Carts',
    'Switching Magic and Abilities',
    'Fishing',
    'Viewing Letters',
    'Changing Weapons',
    'Moving Boxes',
    '',
    'Charging',
    '',
    'Skull Cracker',
    'Deflecting',
    '', '', '',
    'Sidestepping', 'Sidestep Attacks', 'Combo and Magic Charging', 'Magic Resistance', 'Cancels',
    '', '',
    'Guard Breaks', 'Heavy Attack Guard Breaks',
    'Earning Money',
    'Fishing Tip', 'Fishing Tip 2', 'Fishing Tip 3', 'Fishing Tip 4', 'Fishing Tip 5',
    'Armored Enemies',
    'Controlling Boars',
    'Bombs', 'Breakable Boxes', 'Breakable Barriers',
    'Gathering Items', 'Hidden Items',
    'Words',
    'Ordering Allies', 'Ordering Animals',
    'Item and Equipment Shortcuts',
    'Wall Kicks',
    'Combo Basics', 'Deflecting Enemy Magic', 'Fighting Magic Resistant Enemies', 'Fighting Wolves',
    'Stronger Dark Blasts',
    'Harvests', 'Rare Items',
    '',
    'Collecting Materials', 'Absorbing Blood', 'Magical Collisions',
    'Ending B', 'Ending C', 'Ending D',
    'Evading', 'Double Jump',
    '',
    'Weapon Quick Switching', 'Finishing Blow', 'Magic or Ability Quick Switching', 'Lock On',
    '',
    '',
    'Poison',
    '', '', '', '', '', '', '', '', '', '', '', '',
]

# endregion

# region Documents & Key Items

DOCUMENTS = [
    'Look at the Sky', "Don't try so hard", 'My Birthday!', 'Love Letter 2/12/3340', 'Love Letter 3/28/3340',
    'Love Letter 5/1/3340', 'Letter from the Mayor', "The Postman's Request", "The Postman's Thanks",
    'Invitation from a Stranger', 'Grand Re-Opening Notice', 'Wedding Invitation', 'Letter from the King',
    'Underground Research Record 1', 'Underground Research Record 2', 'Underground Research Record 3',
    'Underground Research Record 4', 'Letter to the Chief', 'Letter to two Brothers Weaponry', 'Letter to Popola',
    'Letter to a Faraway Lover', 'Letter from Emil', 'Weapon Upgrade Notice', 'Letter from the Chief of The Aerie'
]
KEY_ITEMS = [
    'Moon Key', 'Star Key', 'Light Key', 'Darkness Key', 'Fine Flour', 'Coarse Flour', 'Perfume Bottle',
    "Postman's Parcel", "Lover's Letter", 'Water Filter', 'Royal Compass', 'Vapor Moss', 'Valley Spider Silk',
    'Animal Guidebook', 'Ore Guidebook', 'Plant Guidebook', 'Red Book', 'Blue Book', "Old Lady's Elixir",
    "Old Lady's Elixir+", 'Parcel for The Aerie', 'Parcel for Seafront', 'Cookbook', 'Parcel for Facade', "Max's Herbs",
    'Drifting Cargo', 'Drifting Cargo 2', 'Drifting Cargo 3', 'Drifting Cargo 4', 'Old Package', 'Mermaid Tear',
    'Mandrake Leaf', 'Energizer', 'Toad Oil', 'Sleep-B-Gone', 'Antidote', 'Gold Bracelet', 'Elite Kitchen Knife',
    'Elevator Parts', 'Dirty Treasure Map', 'Restored Treasure Map', 'Jade Hair Ornament', 'Employee List',
    'Small Safe', 'Safe Key', 'Great Tree Root', 'Eye of Power', 'Ribbon', "Yonah's Ribbon", 'Bronze Key', 'Brass Key',
    'Boar Tusk', 'Pressed Freesia', 'Potted Freesia', 'Freesia (Delivery)', 'Pile of Junk', 'Old Gold Coin',
    'Marked Map', 'AA Keycard', 'KA Keycard', 'SA Keycard', 'TA Keycard', 'NA Keycard', 'HA Keycard', 'MA Keycard',
    'YA Keycard', 'RA Keycard', 'WA Keycard', "Cultivator's Handbook", 'Red Bag', 'Lantern', 'Empty Lantern',
    'Hold Key', 'Passageway Key', 'Goat Key', 'Lizard Key', 'Unlocking Procedure Memo', 'Red Jewel?', 'Red Flowers',
    'Apples'
]

# endregion

# region Garden

# Enum for seed planted in a given garden plot.  255 = empty.  Order differs from inventory order for Cultivation items.
PLANTS = [
    'Tomato Seed',              # 0
    'Eggplant Seed',            # 1 (unconfirmed)
    'Bell Pepper Seed',         # 2 (unconfirmed)
    'Bean Seed',                # 3
    'Pumpkin Seed',             # 4 (unconfirmed)
    'Watermelon Seed',          # 5
    'Melon Seed',               # 6
    'Gourd Seed',               # 7
    'Wheat Seedling',           # 8
    'Rice Plant Seedling',      # 9
    'Dahlia Bulb',              # 10 (unconfirmed)
    'Tulip Bulb',               # 11 (unconfirmed)
    'Freesia Bulb',             # 12 (unconfirmed)
    'Red Moonflower Seed',      # 13
    'Gold Moonflower Seed',     # 14
    'Peach Moonflower Seed',    # 15
    'Pink Moonflower Seed',     # 16 (unconfirmed)
    'Blue Moonflower Seed',     # 17
    'Indigo Moonflower Seed',   # 18
    'White Moonflower Seed',    # 19 (unconfirmed)
]
FERTILIZER = ['None', 'Speed Fertilizer', 'Flowering Fertilizer', 'Bounty Fertilizer']
FERTILIZER_ALIASES = {f.split(maxsplit=1)[0]: f for f in FERTILIZER}

# endregion

# region Inventory

# Cultivation items in inventory - order is different from garden plot plant enum.
FERTILIZERS = ['Speed Fertilizer', 'Flowering Fertilizer', 'Bounty Fertilizer']
SEEDS = [
    'Pumpkin Seed', 'Watermelon Seed', 'Melon Seed', 'Gourd Seed', 'Tomato Seed', 'Eggplant Seed', 'Bell Pepper Seed',
    'Bean Seed', 'Wheat Seedling', 'Rice Plant Seedling',
    'Dahlia Bulb', 'Tulip Bulb', 'Freesia Bulb',
    'Red Moonflower Seed', 'Gold Moonflower Seed', 'Peach Moonflower Seed',
    'Pink Moonflower Seed', 'Blue Moonflower Seed', 'Indigo Moonflower Seed',
    'White Moonflower Seed',
]
CULTIVATED = [
    'Pumpkin', 'Watermelon', 'Melon', 'Gourd', 'Tomato', 'Eggplant', 'Bell Pepper',
    'Beans', 'Wheat', 'Rice',
    'Dahlia', 'Tulip', 'Freesia',
    'Red Moonflower', 'Gold Moonflower', 'Peach Moonflower',
    'Pink Moonflower', 'Blue Moonflower', 'Indigo Moonflower',
    'White Moonflower',
]
SEED_RESULT_MAP = dict(zip(SEEDS, CULTIVATED))

RECOVERY = {
    'health': ['Medicinal Herb', 'Health Salve', 'Recovery Potion'],
    'stats': [
        'Strength Drop', 'Strength Capsule', 'Magic Drop', 'Magic Capsule', 'Defense Drop', 'Defense Capsule',
        'Spirit Drop', 'Spirit Capsule',
    ],
    'status': ['Antidotal Weed'],
    'misc': ['Smelling Salts'],
}

BAIT = ['Lugworm', 'Earthworm', 'Lure']
FISH = [
    'Sardine', 'Carp', 'Blowfish', 'Bream', 'Shark', 'Blue Marlin', 'Dunkleosteus', 'Rainbow Trout', 'Black Bass',
    'Giant Catfish', 'Royal Fish', 'Hyneria', 'Sandfish', 'Rhizodont', 'Shaman Fish'
]
FISH_RECORDS = [
    'Sardine', 'Blowfish', 'Bream', 'Shark', 'Blue Marlin', 'Dunkleosteus', 'Carp', 'Rainbow Trout', 'Black Bass',
    'Giant Catfish', 'Royal Fish', 'Hyneria', 'Sandfish', 'Rhizodont', 'Shaman Fish'
]

RAW_MATERIALS = {
    'fished': ['Aquatic Plant', 'Deadwood', 'Rusty Bucket', 'Empty Can'],
    'minerals': [
        'Gold Ore', 'Silver Ore', 'Copper Ore', 'Iron Ore',
        'Crystal', 'Pyrite', 'Moldavite', 'Meteorite', 'Amber', 'Fluorite', 'Clay'
    ],
    'plants': ['Berries', 'Royal Fern', 'Tree Branch', 'Log', 'Natural Rubber', 'Ivy', 'Lichen', 'Mushroom', 'Sap'],
    'scavenged': [
        'Mutton', 'Boar Meat', 'Wool', 'Boar Hide', 'Wolf Hide', 'Wolf Fang', 'Giant Spider Silk', 'Bat Fang',
        'Bat Wing', 'Goat Meat', 'Goat Hide', 'Venison', 'Rainbow Spider Silk', 'Boar Liver', 'Scorpion Claw',
        'Scorpion Tail', 'Dented Metal Board', 'Stripped Bolt', 'Broken Lens', 'Severed Cable', 'Broken Arm',
        'Broken Antenna', 'Broken Motor', 'Broken Battery', 'Mysterious Switch', 'Large Gear', 'Titanium Alloy',
        'Memory Alloy', 'Rusted Clump', 'Machine Oil',
    ],
    'shades': [
        'Forlorn Necklace', 'Twisted Ring', 'Broken Earring', 'Pretty Choker', 'Metal Piercing', 'Subdued Bracelet',
        'Technical Guide', 'Grubby Book', 'Thick Dictionary', 'Closed Book', 'Used Coloring Book', 'Old Schoolbook',
        'Dirty Bag', 'Flashy Hat', 'Leather Gloves', 'Silk Handkerchief', 'Leather Boots', 'Complex Machine',
        'Elaborate Machine', 'Simple Machine', 'Stopped Clock', 'Broken Wristwatch', 'Rusty Kitchen Knife',
        'Broken Saw', 'Dented Metal Bat',
    ],
    'seafront': [
        'Shell', 'Gastropod', 'Bivalve', 'Seaweed', 'Empty Bottle', 'Driftwood', 'Pearl', 'Black Pearl', 'Crab',
        'Starfish',
    ],
    'misc': [
        'Sea Turtle Egg', 'Broken Pottery', 'Desert Rose', 'Giant Egg', 'Damascus Steel', 'Eagle Egg', 'Chicken Egg'
    ],
    'tails': ['Mouse Tail', 'Lizard Tail'],
    'antlers': ['Deer Antler'],
}

# endregion

# region Character & Level

CHARACTERS = ['NieR (Young)', 'NieR (Prologue)', 'NieR (Old)', 'NieR (Gestalt)', 'Kainé']

LEVEL_TO_EXP = [
    0, 30, 240, 850, 2060, 4070, 7080, 11290, 16900, 24110,
    33120, 44130, 57340, 72950, 91160, 112170, 136180, 163390, 194000, 228210,
    266220, 308230, 354440, 405050, 460260, 520270, 585280, 655490, 731100, 812310,
    899320, 987380, 1076525, 1166790, 1258210, 1350820, 1444655, 1539750, 1636140, 1733860,
    1832945, 1933430, 2035350, 2138740, 2243635, 2350070, 2458080, 2567700, 2678965, 2791910,
    2906570, 3022980, 3141175, 3261190, 3383060, 3506820, 3632505, 3760150, 3889790, 4021460,
    4155195, 4289596, 4424674, 4560440, 4696906, 4834082, 4971979, 5110609, 5249983, 5390112,
    5531006, 5672677, 5815137, 5958395, 6102464, 6247355, 6393078, 6539644, 6687065, 6835352,
    6984516, 7134568, 7285518, 7437380, 7590162, 7743877, 7898535, 8054148, 8210726, 8368281,
    8526824, 8686367, 8846919, 9008492, 9171098, 9334747, 9499451, 9665220, 9832066,
]

# endregion

# region Quests

# Max diff = 13, and there are no overlapping start/end values (except Thieves in Training...)
# Assumption would be unaccounted-for bits are for quest stages/choices, and failure / multiple outcomes?

# Mapping of {name: (start, end)} bits
QUESTS = {
    'Herbal Remedies': (28, 29),  # 30 = failed?
    "The Gatekeeper's Errand": (31, 33),  # 34 = failed?
    'The Lost Eggs': (35, 39),
    'Old-Fashioned Home Cooking': (41, 43),
    'Shopping List': (45, 47),
    'Book Smarts': (49, 53),
    "The Tavern Keeper's Grandmother": (55, 58),
    'A Return to Shopping': (60, 62),
    "Yonah's Cooking": (64, 65),
    'Boar Hunt!': (67, 70),
    'On the Wings of Eagles': (72, 76),
    'Fragile Delivery': (78, 82),
    'Fragile Delivery 2': (84, 88),
    "The Fisherman's Gambit": (90, 91),
    "The Fisherman's Gambit, Part 2": (93, 94),
    "The Fisherman's Gambit, Part 3": (96, 97),
    "The Fisherman's Gambit, Part 4": (99, 100),
    "The Fisherman's Gambit, Part 5": (102, 103),
    'The Ballad of the Twins': (105, 110),
    'A Dog Astray': (112, 115),
    'The New Merchant in Town': (117, 121),
    "Yonah's Gift": (132, 139),
    'Letter to a Lover': (141, 144),
    'A Signature Dish': (146, 148),
    'Bon Appetit!': (150, 154),
    'Fragile Delivery 3': (156, 160),
    'The Tangled Message': (162, 167),
    'Item Unknown': (172, 174),
    'The Runaway Son': (176, 186),
    'Apology from a Fool': (188, 192),
    'The Pride of a Lover': (198, 200),
    'The Littlest Hero': (202, 205),
    'The Missing Girl': (207, 211),  # 2 bit gap to next... assuming it accounts for multiple outcomes?
    'A Shade Entombed': (214, 217),
    'The Masterless Lighthouse': (219, 220),
    'The Scattered Cargo': (222, 233),
    'The Strange Fate of the Jewel': (236, 244),  # 16 bit gap to next...
    # 'Thieves in Training': (260, 505),  # In theory, 268 should be the end for this, with 269=fail...
    'Thieves in Training (1)': (260, 269),
    'Learning a Trade': (270, 278),
    'A Bridge in Peril': (281, 284),
    'Master of the Southern Plains': (286, 289),
    "The Fisherman's Gambit, Part 6": (291, 292),
    "The Fisherman's Gambit, Part 7": (294, 295),
    "The Fisherman's Gambit, Part 8": (297, 298),
    "The Fisherman's Final Gambit": (300, 301),
    'Staying Afloat': (303, 305),
    'Contract for a Contractor': (307, 309),
    'The Creaky Waterwheel': (311, 315),
    'The Faded Fountain': (317, 321),
    'Bon Appetit! 2': (323, 325),
    'Life in the Sands': (327, 329),
    "The King's Mask": (331, 333),
    "A Child's Final Chance": (334, 343),
    'The Damaged Map': (345, 358),
    'Research Project': (360, 365),
    'A Tale of the Study': (367, 370),
    'The Great Tree': (372, 375),
    'The Despicable Man': (377, 383),
    'A Memorable Knife': (385, 388),
    'The Shade Army': (391, 397),
    'A City Reborn': (399, 400),
    'Nightmares and Dust': (402, 405),
    'Disturbing the Sleep of Kings': (407, 410),
    'Shadows of the Desert': (412, 416),
    'Search for the Shade': (418, 427),
    'Freesia': (429, 433),
    'The Magical': (436, 441),
    "The Postman's Request": (473, 474),
    "The Lighthouse Lady's Wrath": (477, 487),
    'Closure': (489, 490),
    'Thieves in Training (2)': (504, 505),
}

QUESTS_NEW_1 = {'The Promised Gift': (3, 9)}  # Quests added to the 1.22474487139 version that did not exist in original

QUEST_NEW_MARKERS = [
    'The Lost Eggs',
    'The Gatekeeper\'s Errand',
    'Herbal Remedies',
    '_quest_3',
    '_quest_4',
    '_quest_5',
    '_quest_6',
    '_quest_7',
    '_quest_8',
    'Yonah\'s Cooking',
    '_quest_10',
    '_quest_11',
    '_quest_12',
    'Book Smarts',
    'Shopping List',
    'Old-Fashioned Home Cooking',
    '_quest_16',
    '_quest_17',
    'The Fisherman\'s Gambit, Part 2',
    'The Fisherman\'s Gambit',
    '_quest_20',
    '_quest_21',
    '_quest_22',
    '_quest_23',
    '_quest_24',
    'Closure',
    '_quest_26',
    'The Postman\'s Request',
    '_quest_28',
    '_quest_29',
    '_quest_30',
    '_quest_31',
    'Item Unknown',
    'The Tangled Message',
    '_quest_34',
    '_quest_35',
    'A Signature Dish',
    '_quest_37',
    'Yonah\'s Gift',
    '_quest_39',
    '_quest_40',
    '_quest_41',
    '_quest_42',
    'The Missing Girl',
    '_quest_44',
    '_quest_45',
    'Apology from a Fool',
    '_quest_47',
    '_quest_48',
    '_quest_49',
    'The Fisherman\'s Gambit, Part 6',
    '_quest_51',
    '_quest_52',
    '_quest_53',
    'Thieves in Training',
    '_quest_55',
    'The King\'s Mask',
    '_quest_57',
    'Bon Appetit! 2',
    '_quest_59',
    '_quest_60',
    '_quest_61',
    '_quest_62',
    'The Fisherman\'s Final Gambit',
    '_quest_64',
    '_quest_65',
    '_quest_66',
    'A Tale of the Study',
    'Research Project',
    '_quest_69',
    '_quest_70',
    '_quest_71',
    '_quest_72',
    '_quest_73',
    '_quest_74',
    '_quest_75',
    'Disturbing the Sleep of Kings',
    '_quest_77',
    '_quest_78',
    '_quest_79',
    '_quest_80',
    '_quest_81',
    '_quest_82',
    '_quest_83',
    '_quest_84',
    'The Promised Gift',
    '_quest_86',
    '_quest_87'
]

# endregion
