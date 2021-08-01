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
    # Many of these are guesses
    'CENTER_VILLAGE': 'NieR\'s Village',
    'CENTER_LIBRARY': 'Library',
    'CLIFF_VILLAGE': 'The Aerie',
    'STONE_TEMPLE': 'Lost Shrine',
    'SEASIDE_TOWN': 'Seafront',
    'DESERT_FIELD': 'Desert',
    'DESERT_TOWN': 'Facade',
    'DESERT_TEMPLE': 'Barren Temple',
    'MOUNT_ROBOT': 'Junk Heap',
    'SOUTH_MANSION': 'Manor',
    'FOREST_FIELD': 'Forest of Myth',
    'SOUTH_UNDERGROUND': 'Underground Facility',
    'CASTLE_FIELD': 'Shadowlord\'s Castle',
    'NORTH_FIELD': 'Northern Plains',
    'SOUTH_FIELD': 'Southern Plains',
    'EAST_FIELD': 'Eastern Road',
    # '': 'Beneath the Forest of Myth',
    'TOKYO_FIELD': 'Toyko',
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
    'Dark Blast',
    'Dark Phantasm',
    'Dark Hand',
    'Dark Lance',
    'Dark Whirlwind',
    'Dark Gluttony',
    'Dark Wall',
    'Dark Execution',
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
    '',
    'Viewing Letters',
    'Changing Weapons',
    'Moving Boxes',
    '',
    'Charging',
    '',
    'Skull Cracker',
    'Deflecting',
    '',
    '',
    '',
    'Sidestepping',
    'Sidestep Attacks',
    'Combo and Magic Charging',
    'Magic Resistance',
    'Cancels',
    '',
    '',
    'Guard Breaks',
    'Heavy Attack Guard Breaks',
    'Earning Money',
    'Fishing Tip',
    'Fishing Tip 2',
    'Fishing Tip 3',
    'Fishing Tip 4',
    'Fishing Tip 5',
    'Armored Enemies',
    'Controlling Boars',
    'Bombs',
    'Breakable Boxes',
    'Breakable Barriers',
    'Gathering Items',
    'Hidden Items',
    'Words',
    'Ordering Allies',
    'Ordering Animals',
    'Item and Equipment Shortcuts',
    'Wall Kicks',
    'Combo Basics',
    'Deflecting Enemy Magic',
    'Fighting Magic Resistant Enemies',
    'Fighting Wolves',
    'Stronger Dark Blasts',
    'Harvests',
    'Rare Items',
    '',
    'Collecting Materials',
    'Absorbing Blood',
    'Magical Collisions',
    'Ending B',
    'Ending C',
    'Ending D',
    'Evading',
    'Double Jump',
    '',
    'Weapon Quick Switching',
    'Finishing Blow',
    'Magic or Ability Quick Switching',
    'Lock On',
    '',
    '',
    'Poison',
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

QUEST_STARTED_A = {
    28: 'Herbal Remedies',
    31: "The Gatekeeper's Errand",
    35: 'The Lost Eggs',
    41: 'Old-Fashioned Home Cooking',
    45: 'Shopping List',
    49: 'Book Smarts',
    55: "The Tavern Keeper's Grandmother",
    60: 'A Return to Shopping',
    64: "Yonah's Cooking",
    67: 'Boar Hunt!',
    72: 'On the Wings of Eagles',
    78: 'Fragile Delivery',
    84: 'Fragile Delivery 2',
    90: "The Fisherman's Gambit",
    93: "The Fisherman's Gambit, Part 2",
    96: "The Fisherman's Gambit, Part 3",
    99: "The Fisherman's Gambit, Part 4",
    102: "The Fisherman's Gambit, Part 5",
    105: 'The Ballad of the Twins',
    112: 'A Dog Astray',
    117: 'The New Merchant in Town',
    132: "Yonah's Gift",
    141: 'Letter to a Lover',
    146: 'A Signature Dish',
    150: 'Bon Appetit!',
    156: 'Fragile Delivery 3',
    162: 'The Tangled Message',
    172: 'Item Unknown',
    176: 'The Runaway Son',
    188: 'Apology from a Fool',
    198: 'The Pride of a Lover',
    202: 'The Littlest Hero',
    207: 'The Missing Girl',
    214: 'A Shade Entombed',
    219: 'The Masterless Lighthouse',
    222: 'The Scattered Cargo',
    236: 'The Strange Fate of the Jewel',
    260: 'Thieves in Training',
    270: 'Learning a Trade',
    281: 'A Bridge in Peril',
    286: 'Master of the Southern Plains',
    291: "The Fisherman's Gambit, Part 6",
    294: "The Fisherman's Gambit, Part 7",
    297: "The Fisherman's Gambit, Part 8",
    300: "The Fisherman's Final Gambit",
    303: 'Staying Afloat',
    307: 'Contract for a Contractor',
    311: 'The Creaky Waterwheel',
    317: 'The Faded Fountain',
    323: 'Bon Appetit! 2',
    327: 'Life in the Sands',
    331: "The King's Mask",
    334: "A Child's Final Chance",
    345: 'The Damaged Map',
    360: 'Research Project',
    367: 'A Tale of the Study',
    372: 'The Great Tree',
    377: 'The Despicable Man',
    385: 'A Memorable Knife',
    391: 'The Shade Army',
    399: 'A City Reborn',
    402: 'Nightmares and Dust',
    407: 'Disturbing the Sleep of Kings',
    412: 'Shadows of the Desert',
    418: 'Search for the Shade',
    429: 'Freesia',
    436: 'The Magical',
    473: "The Postman's Request",
    477: "The Lighthouse Lady's Wrath",
    489: 'Closure',
}

QUEST_FINISHED_A = {
    29: 'Herbal Remedies',
    33: "The Gatekeeper's Errand",
    39: 'The Lost Eggs',
    43: 'Old-Fashioned Home Cooking',
    47: 'Shopping List',
    53: 'Book Smarts',
    58: "The Tavern Keeper's Grandmother",
    62: 'A Return to Shopping',
    65: "Yonah's Cooking",
    70: 'Boar Hunt!',
    76: 'On the Wings of Eagles',
    82: 'Fragile Delivery',
    88: 'Fragile Delivery 2',
    91: "The Fisherman's Gambit",
    94: "The Fisherman's Gambit, Part 2",
    97: "The Fisherman's Gambit, Part 3",
    100: "The Fisherman's Gambit, Part 4",
    103: "The Fisherman's Gambit, Part 5",
    110: 'The Ballad of the Twins',
    115: 'A Dog Astray',
    121: 'The New Merchant in Town',
    139: "Yonah's Gift",
    144: 'Letter to a Lover',
    148: 'A Signature Dish',
    154: 'Bon Appetit!',
    160: 'Fragile Delivery 3',
    167: 'The Tangled Message',
    174: 'Item Unknown',
    186: 'The Runaway Son',
    192: 'Apology from a Fool',
    200: 'The Pride of a Lover',
    205: 'The Littlest Hero',
    211: 'The Missing Girl',
    217: 'A Shade Entombed',
    220: 'The Masterless Lighthouse',
    233: 'The Scattered Cargo',
    244: 'The Strange Fate of the Jewel',
    505: 'Thieves in Training',
    278: 'Learning a Trade',
    284: 'A Bridge in Peril',
    289: 'Master of the Southern Plains',
    292: "The Fisherman's Gambit, Part 6",
    295: "The Fisherman's Gambit, Part 7",
    298: "The Fisherman's Gambit, Part 8",
    301: "The Fisherman's Final Gambit",
    305: 'Staying Afloat',
    309: 'Contract for a Contractor',
    315: 'The Creaky Waterwheel',
    321: 'The Faded Fountain',
    325: 'Bon Appetit! 2',
    329: 'Life in the Sands',
    333: "The King's Mask",
    343: "A Child's Final Chance",
    358: 'The Damaged Map',
    365: 'Research Project',
    370: 'A Tale of the Study',
    375: 'The Great Tree',
    383: 'The Despicable Man',
    388: 'A Memorable Knife',
    397: 'The Shade Army',
    400: 'A City Reborn',
    405: 'Nightmares and Dust',
    410: 'Disturbing the Sleep of Kings',
    416: 'Shadows of the Desert',
    427: 'Search for the Shade',
    433: 'Freesia',
    441: 'The Magical',
    474: "The Postman's Request",
    487: "The Lighthouse Lady's Wrath",
    490: 'Closure',
}

QUEST_STARTED_B = {3: 'The Promised Gift'}
QUEST_FINISHED_B = {9: 'The Promised Gift'}

QUESTS = set(QUEST_STARTED_A.values()).union(QUEST_STARTED_B.values())

# endregion
