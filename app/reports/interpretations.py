"""
interpretations.py -- Static Text Databases for Kundli Report
=============================================================
All interpretation texts for a Parashara's Light style Kundli PDF report.
Concise but meaningful -- compact pages, not verbose padding.

Sections:
  1. LAGNA_NATURE          - Nature & temperament per ascendant sign
  2. NAKSHATRA_INTERPRETATIONS - Per-nakshatra classical + modern
  3. PLANET_IN_HOUSE       - 9 planets x 12 houses (auspicious / inauspicious)
  4. BHAVESH_INTERPRETATIONS - Lord of Nth house in Mth house (144 combos)
  5. GEMSTONE_DATA          - Gemstone recommendations per planet
  6. DASHA_INTERPRETATIONS  - Mahadasha general effects
  7. ANTARDASHA_INTERPRETATIONS - 81 MD-AD combinations
  8. MANGALA_DOSHA_TEXT     - Classical shloka references + remedies
  9. GRAHA_AVASTHAS         - Planetary states & calculation rules
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# 1. LAGNA_NATURE -- Nature & Temperament per Ascendant Sign
# ============================================================

LAGNA_NATURE: Dict[str, Dict[str, Any]] = {
    "Aries": {
        "nature": [
            "Courageous and pioneering spirit",
            "Quick decision-maker, natural leader",
            "Competitive and ambitious in all pursuits",
            "Impulsive but honest and direct",
            "Fiery temperament with strong will-power",
        ],
        "main_sentence": "I am",
        "biggest_talent": "Courage and initiative",
        "biggest_weakness": "Hurried behaviour and impatience",
        "ambition": "Leadership and independence",
        "lucky_day": "Tuesday",
        "lucky_color": "Red, Coral",
        "lucky_number": "9",
        "lucky_stone": "Red Coral (Moonga)",
        "lucky_upratna": "Carnelian",
        "inauspicious_month": "October (Ashwin-Kartik)",
        "auspicious_rashi": "Leo, Sagittarius",
        "physical": [
            "Medium to tall stature with athletic build",
            "Sharp features, prominent forehead",
            "Quick, energetic gait",
            "Often has a scar or mark on head/face",
        ],
    },
    "Taurus": {
        "nature": [
            "Patient, steady and reliable",
            "Strong attachment to material comforts",
            "Artistic sensibility and love of beauty",
            "Stubborn but deeply loyal",
            "Practical and grounded approach to life",
        ],
        "main_sentence": "I have",
        "biggest_talent": "Persistence and stability",
        "biggest_weakness": "Stubbornness and possessiveness",
        "ambition": "Wealth and material security",
        "lucky_day": "Friday",
        "lucky_color": "White, Cream",
        "lucky_number": "6",
        "lucky_stone": "Diamond (Heera)",
        "lucky_upratna": "White Zircon",
        "inauspicious_month": "November (Kartik-Margashirsha)",
        "auspicious_rashi": "Virgo, Capricorn",
        "physical": [
            "Strong, stocky build with broad shoulders",
            "Pleasant face with large expressive eyes",
            "Thick neck, melodious voice",
            "Tends toward weight gain in middle age",
        ],
    },
    "Gemini": {
        "nature": [
            "Intellectual, curious and communicative",
            "Versatile with many interests and skills",
            "Witty, charming conversationalist",
            "Restless mind, easily bored",
            "Adaptable to changing circumstances",
        ],
        "main_sentence": "I think",
        "biggest_talent": "Communication and versatility",
        "biggest_weakness": "Inconsistency and superficiality",
        "ambition": "Knowledge and social connections",
        "lucky_day": "Wednesday",
        "lucky_color": "Green, Light Yellow",
        "lucky_number": "5",
        "lucky_stone": "Emerald (Panna)",
        "lucky_upratna": "Peridot",
        "inauspicious_month": "December (Margashirsha-Paush)",
        "auspicious_rashi": "Libra, Aquarius",
        "physical": [
            "Slim, tall build with long limbs",
            "Youthful appearance, expressive hands",
            "Quick darting eyes, alert expression",
            "Often appears younger than actual age",
        ],
    },
    "Cancer": {
        "nature": [
            "Deeply emotional and nurturing",
            "Strong attachment to home and family",
            "Intuitive and empathetic nature",
            "Moody but fiercely protective",
            "Excellent memory, especially emotional",
        ],
        "main_sentence": "I feel",
        "biggest_talent": "Nurturing and emotional intelligence",
        "biggest_weakness": "Over-sensitivity and mood swings",
        "ambition": "Emotional security and family harmony",
        "lucky_day": "Monday",
        "lucky_color": "White, Silver",
        "lucky_number": "2",
        "lucky_stone": "Pearl (Moti)",
        "lucky_upratna": "Moonstone",
        "inauspicious_month": "January (Paush-Magh)",
        "auspicious_rashi": "Scorpio, Pisces",
        "physical": [
            "Medium height with round face",
            "Soft features, pale complexion",
            "Tendency toward water retention",
            "Expressive eyes with gentle demeanour",
        ],
    },
    "Leo": {
        "nature": [
            "Royal bearing and natural authority",
            "Generous, warm-hearted and dramatic",
            "Strong sense of dignity and self-respect",
            "Creative with a flair for the theatrical",
            "Proud and loyal to those they love",
        ],
        "main_sentence": "I will",
        "biggest_talent": "Leadership and creative expression",
        "biggest_weakness": "Arrogance and need for attention",
        "ambition": "Recognition and authority",
        "lucky_day": "Sunday",
        "lucky_color": "Gold, Orange",
        "lucky_number": "1",
        "lucky_stone": "Ruby (Manik)",
        "lucky_upratna": "Garnet",
        "inauspicious_month": "February (Magh-Phalgun)",
        "auspicious_rashi": "Aries, Sagittarius",
        "physical": [
            "Broad chest, impressive stature",
            "Thick mane-like hair, dignified walk",
            "Strong bone structure, commanding presence",
            "Warm complexion with bright eyes",
        ],
    },
    "Virgo": {
        "nature": [
            "Analytical, detail-oriented and methodical",
            "Health-conscious and service-minded",
            "Critical thinker with high standards",
            "Modest and hardworking",
            "Practical problem-solver",
        ],
        "main_sentence": "I analyze",
        "biggest_talent": "Analysis and attention to detail",
        "biggest_weakness": "Over-criticism and worry",
        "ambition": "Perfection and useful service",
        "lucky_day": "Wednesday",
        "lucky_color": "Green, Grey",
        "lucky_number": "5",
        "lucky_stone": "Emerald (Panna)",
        "lucky_upratna": "Green Tourmaline",
        "inauspicious_month": "March (Phalgun-Chaitra)",
        "auspicious_rashi": "Taurus, Capricorn",
        "physical": [
            "Slim, well-proportioned body",
            "Youthful, clean appearance",
            "Delicate features, bright forehead",
            "Often has a nervous disposition",
        ],
    },
    "Libra": {
        "nature": [
            "Diplomatic, fair-minded and harmonious",
            "Strong aesthetic sense and love of balance",
            "Charming and sociable personality",
            "Indecisive when faced with choices",
            "Partnership-oriented, dislikes being alone",
        ],
        "main_sentence": "I balance",
        "biggest_talent": "Diplomacy and creating harmony",
        "biggest_weakness": "Indecisiveness and people-pleasing",
        "ambition": "Partnership and social harmony",
        "lucky_day": "Friday",
        "lucky_color": "White, Pastel shades",
        "lucky_number": "6",
        "lucky_stone": "Diamond (Heera)",
        "lucky_upratna": "White Sapphire",
        "inauspicious_month": "April (Chaitra-Vaishakh)",
        "auspicious_rashi": "Gemini, Aquarius",
        "physical": [
            "Well-proportioned, attractive appearance",
            "Symmetrical features, pleasant smile",
            "Graceful movements, soft-spoken",
            "Dimples or beauty marks common",
        ],
    },
    "Scorpio": {
        "nature": [
            "Intense, passionate and deeply perceptive",
            "Magnetic personality with hidden depths",
            "Fiercely loyal but unforgiving when betrayed",
            "Excellent at research and investigation",
            "Transformative — rises from setbacks stronger",
        ],
        "main_sentence": "I desire",
        "biggest_talent": "Depth of perception and resilience",
        "biggest_weakness": "Jealousy and vindictiveness",
        "ambition": "Power and transformation",
        "lucky_day": "Tuesday",
        "lucky_color": "Red, Maroon",
        "lucky_number": "9",
        "lucky_stone": "Red Coral (Moonga)",
        "lucky_upratna": "Bloodstone",
        "inauspicious_month": "May (Vaishakh-Jyeshtha)",
        "auspicious_rashi": "Cancer, Pisces",
        "physical": [
            "Medium build with intense eyes",
            "Strong jawline, penetrating gaze",
            "Magnetic presence, sharp features",
            "Often has a mark near the reproductive area",
        ],
    },
    "Sagittarius": {
        "nature": [
            "Optimistic, philosophical and freedom-loving",
            "Natural teacher with broad vision",
            "Adventurous spirit, loves travel",
            "Honest to the point of bluntness",
            "Jovial with strong moral convictions",
        ],
        "main_sentence": "I see",
        "biggest_talent": "Wisdom and expansive vision",
        "biggest_weakness": "Over-optimism and tactlessness",
        "ambition": "Higher knowledge and exploration",
        "lucky_day": "Thursday",
        "lucky_color": "Yellow, Saffron",
        "lucky_number": "3",
        "lucky_stone": "Yellow Sapphire (Pukhraj)",
        "lucky_upratna": "Citrine",
        "inauspicious_month": "June (Jyeshtha-Ashadh)",
        "auspicious_rashi": "Aries, Leo",
        "physical": [
            "Tall, well-built with large forehead",
            "Long face, prominent nose",
            "Athletic body, graceful movements",
            "Often develops a paunch in later years",
        ],
    },
    "Capricorn": {
        "nature": [
            "Disciplined, ambitious and practical",
            "Patient climb toward long-term goals",
            "Reserved exterior hiding dry wit",
            "Strong sense of duty and responsibility",
            "Ages in reverse — becomes lighter with time",
        ],
        "main_sentence": "I use",
        "biggest_talent": "Discipline and perseverance",
        "biggest_weakness": "Pessimism and emotional coldness",
        "ambition": "Status and lasting achievement",
        "lucky_day": "Saturday",
        "lucky_color": "Black, Dark Blue",
        "lucky_number": "8",
        "lucky_stone": "Blue Sapphire (Neelam)",
        "lucky_upratna": "Amethyst",
        "inauspicious_month": "July (Ashadh-Shravan)",
        "auspicious_rashi": "Taurus, Virgo",
        "physical": [
            "Lean, bony frame with prominent cheekbones",
            "Serious expression, dark hair",
            "Slow but steady gait",
            "Weak knees and joints common",
        ],
    },
    "Aquarius": {
        "nature": [
            "Humanitarian, progressive and unconventional",
            "Independent thinker with original ideas",
            "Friendly but emotionally detached",
            "Strong commitment to social causes",
            "Eccentric and ahead of their time",
        ],
        "main_sentence": "I know",
        "biggest_talent": "Innovation and humanitarian vision",
        "biggest_weakness": "Emotional detachment and rebelliousness",
        "ambition": "Social reform and intellectual freedom",
        "lucky_day": "Saturday",
        "lucky_color": "Dark Blue, Electric Blue",
        "lucky_number": "8",
        "lucky_stone": "Blue Sapphire (Neelam)",
        "lucky_upratna": "Lapis Lazuli",
        "inauspicious_month": "August (Shravan-Bhadrapad)",
        "auspicious_rashi": "Gemini, Libra",
        "physical": [
            "Tall, well-formed body",
            "Handsome/beautiful features, bright eyes",
            "Often has distinctive or unusual appearance",
            "Strong calves and ankles",
        ],
    },
    "Pisces": {
        "nature": [
            "Compassionate, intuitive and dreamy",
            "Highly imaginative and artistic",
            "Deeply spiritual with psychic sensitivity",
            "Self-sacrificing, sometimes to own detriment",
            "Adaptable like water, absorbs surroundings",
        ],
        "main_sentence": "I believe",
        "biggest_talent": "Compassion and spiritual insight",
        "biggest_weakness": "Escapism and lack of boundaries",
        "ambition": "Spiritual fulfilment and creative expression",
        "lucky_day": "Thursday",
        "lucky_color": "Yellow, Sea Green",
        "lucky_number": "3",
        "lucky_stone": "Yellow Sapphire (Pukhraj)",
        "lucky_upratna": "Yellow Topaz",
        "inauspicious_month": "September (Bhadrapad-Ashwin)",
        "auspicious_rashi": "Cancer, Scorpio",
        "physical": [
            "Short to medium height, fleshy build",
            "Soft, dreamy eyes with gentle expression",
            "Small hands and feet",
            "Tendency toward fluid retention",
        ],
    },
}


# ============================================================
# 2. NAKSHATRA_INTERPRETATIONS -- Per Nakshatra (27)
# ============================================================

NAKSHATRA_INTERPRETATIONS: Dict[str, Dict[str, Any]] = {
    "Ashwini": {
        "shastras": (
            "Ruled by the Ashwini Kumaras, celestial physicians. "
            "The native is handsome, fond of ornaments, skilled and intelligent. "
            "Bestows quickness in action and healing ability."
        ),
        "modern": (
            "Pioneer energy with natural healing talent. Quick to start new ventures. "
            "Independent spirit that dislikes restrictions. "
            "Excellent in medicine, sports, and emergency services."
        ),
        "health": "Head, cerebral hemispheres, upper jaw",
        "remedy": "Worship Ashwini Kumaras. Chant 'Om Ashwibhyam Namah'. Offer honey and ghee.",
        "compatible_nakshatras": ["Ashwini", "Bharani", "Pushya", "Punarvasu", "Hasta"],
    },
    "Bharani": {
        "shastras": (
            "Ruled by Yama, lord of dharma and death. "
            "The native is determined, truthful and healthy. "
            "Carries the burden of transformation and moral duty."
        ),
        "modern": (
            "Intense creative force and strong sense of duty. "
            "Excellent endurance and ability to bear hardship. "
            "Talented in arts, judiciary, and finance."
        ),
        "health": "Head, lower jaw, face, cerebellum",
        "remedy": "Worship Lord Yama. Chant 'Om Yamaya Namah'. Offer black sesame seeds.",
        "compatible_nakshatras": ["Bharani", "Ashwini", "Pushya", "Rohini", "Uttara Phalguni"],
    },
    "Krittika": {
        "shastras": (
            "Ruled by Agni, the fire god. "
            "The native is sharp, brilliant and famous. "
            "Possesses cutting intellect and purifying nature."
        ),
        "modern": (
            "Strong willpower with ability to cut through illusion. "
            "Natural authority figure, often in leadership roles. "
            "Excels in cooking, military, and editorial work."
        ),
        "health": "Face, neck, tonsils, lower jaw",
        "remedy": "Worship Agni Dev. Chant 'Om Agnaye Namah'. Perform havan with ghee.",
        "compatible_nakshatras": ["Krittika", "Rohini", "Uttara Phalguni", "Uttara Ashadha", "Uttara Bhadrapada"],
    },
    "Rohini": {
        "shastras": (
            "Ruled by Brahma, the creator. Moon is exalted here. "
            "The native is attractive, prosperous and artistic. "
            "Bestows fertility, beauty and material abundance."
        ),
        "modern": (
            "Magnetic charm with strong aesthetic sensibility. "
            "Business acumen and love of luxury. "
            "Success in fashion, agriculture, real estate, and arts."
        ),
        "health": "Throat, neck, cervical vertebrae, tonsils",
        "remedy": "Worship Lord Brahma. Chant 'Om Brahmane Namah'. Offer white flowers and milk.",
        "compatible_nakshatras": ["Rohini", "Krittika", "Mrigashira", "Hasta", "Shravana"],
    },
    "Mrigashira": {
        "shastras": (
            "Ruled by Soma (Moon). Symbol is a deer's head. "
            "The native is gentle, searching and scholarly. "
            "Bestows a seeking nature and love of exploration."
        ),
        "modern": (
            "Curious intellect always searching for truth. "
            "Gentle yet restless, with a love of travel. "
            "Excels in research, writing, textiles, and music."
        ),
        "health": "Chin, cheeks, larynx, palate, throat",
        "remedy": "Worship Soma/Chandra. Chant 'Om Somaaya Namah'. Offer white rice.",
        "compatible_nakshatras": ["Mrigashira", "Rohini", "Ardra", "Chitra", "Dhanishta"],
    },
    "Ardra": {
        "shastras": (
            "Ruled by Rudra, the storm god. Symbol is a teardrop. "
            "The native is mentally sharp, ungrateful yet truthful. "
            "Bestows transformation through suffering and renewal."
        ),
        "modern": (
            "Brilliant analytical mind with capacity for deep research. "
            "Emotional intensity that leads to breakthroughs. "
            "Success in technology, science, pharmacy, and writing."
        ),
        "health": "Throat, arms, shoulders, upper respiratory tract",
        "remedy": "Worship Lord Rudra/Shiva. Chant 'Om Namah Shivaya'. Offer bilva leaves.",
        "compatible_nakshatras": ["Ardra", "Mrigashira", "Punarvasu", "Swati", "Shatabhisha"],
    },
    "Punarvasu": {
        "shastras": (
            "Ruled by Aditi, mother of the gods. Symbol is a quiver of arrows. "
            "The native is contented, virtuous, and returns to goodness. "
            "Bestows renewal, restoration and spiritual wisdom."
        ),
        "modern": (
            "Optimistic nature with ability to bounce back from setbacks. "
            "Philosophical outlook, good teacher and counsellor. "
            "Success in travel, publishing, religion, and philosophy."
        ),
        "health": "Nose, ears, throat, lungs, chest",
        "remedy": "Worship Aditi Devi. Chant 'Om Aditaye Namah'. Offer yellow flowers.",
        "compatible_nakshatras": ["Punarvasu", "Pushya", "Ashwini", "Hasta", "Swati"],
    },
    "Pushya": {
        "shastras": (
            "Ruled by Brihaspati (Jupiter). Most auspicious nakshatra. "
            "The native is calm, religious and wealthy. "
            "Bestows nourishment, protection and spiritual growth."
        ),
        "modern": (
            "Natural caretaker with strong spiritual inclinations. "
            "Conservative approach yields steady growth. "
            "Success in counselling, agriculture, dairy, and government."
        ),
        "health": "Lungs, stomach, ribs, upper digestive system",
        "remedy": "Worship Lord Brihaspati. Chant 'Om Brim Brihaspataye Namah'. Offer yellow sweets.",
        "compatible_nakshatras": ["Pushya", "Punarvasu", "Ashwini", "Ashlesha", "Anuradha"],
    },
    "Ashlesha": {
        "shastras": (
            "Ruled by Sarpas (Nagas), the serpent deities. "
            "The native is shrewd, crafty and prone to deception. "
            "Bestows mystical power, kundalini energy and deep insight."
        ),
        "modern": (
            "Penetrating intelligence with psychic sensitivity. "
            "Hypnotic personality, good at persuasion. "
            "Success in psychology, occult, medicine, and politics."
        ),
        "health": "Stomach, diaphragm, pancreas, upper abdomen",
        "remedy": "Worship Naga Devtas. Chant 'Om Namo Nagarajaya Namah'. Offer milk at snake shrine.",
        "compatible_nakshatras": ["Ashlesha", "Pushya", "Magha", "Jyeshtha", "Revati"],
    },
    "Magha": {
        "shastras": (
            "Ruled by Pitris (ancestors). Symbol is a royal throne. "
            "The native is noble, wealthy and devoted to ancestors. "
            "Bestows authority, legacy consciousness and royal bearing."
        ),
        "modern": (
            "Strong leadership with respect for tradition and lineage. "
            "Regal bearing, expects and receives respect. "
            "Success in government, management, history, and archaeology."
        ),
        "health": "Heart, back, spinal cord, aorta",
        "remedy": "Worship Pitris. Chant 'Om Pitribhyah Namah'. Perform tarpan and shraddha.",
        "compatible_nakshatras": ["Magha", "Purva Phalguni", "Ashlesha", "Mula", "Uttara Bhadrapada"],
    },
    "Purva Phalguni": {
        "shastras": (
            "Ruled by Bhaga, god of fortune and marital bliss. "
            "The native is attractive, generous and pleasure-loving. "
            "Bestows creative talent, prosperity and romantic nature."
        ),
        "modern": (
            "Charismatic personality drawn to luxury and the arts. "
            "Natural entertainer with warm social skills. "
            "Success in entertainment, diplomacy, event management."
        ),
        "health": "Heart, spine, diaphragm, upper back",
        "remedy": "Worship Bhaga Dev. Chant 'Om Bhagaya Namah'. Offer sweets and flowers.",
        "compatible_nakshatras": ["Purva Phalguni", "Uttara Phalguni", "Magha", "Purva Ashadha", "Purva Bhadrapada"],
    },
    "Uttara Phalguni": {
        "shastras": (
            "Ruled by Aryaman, god of contracts and patronage. "
            "The native is generous, kind and prosperous. "
            "Bestows lasting friendships, wealth and helpful nature."
        ),
        "modern": (
            "Reliable leadership with strong sense of commitment. "
            "Excellent organizational skills and social consciousness. "
            "Success in HR, social work, management, and philanthropy."
        ),
        "health": "Spine, lower back, intestines",
        "remedy": "Worship Aryaman. Chant 'Om Aryamne Namah'. Offer rice and ghee.",
        "compatible_nakshatras": ["Uttara Phalguni", "Purva Phalguni", "Bharani", "Krittika", "Hasta"],
    },
    "Hasta": {
        "shastras": (
            "Ruled by Savitar (Sun as creator). Symbol is an open hand. "
            "The native is skilful, witty and industrious. "
            "Bestows dexterity, craftsmanship and resourcefulness."
        ),
        "modern": (
            "Highly skilled hands-on worker with quick wit. "
            "Practical intelligence applied to everyday problems. "
            "Success in crafts, healing, comedy, and commerce."
        ),
        "health": "Hands, fingers, bowels, intestines",
        "remedy": "Worship Savitar/Surya. Chant 'Om Savitri Namah'. Offer water at sunrise.",
        "compatible_nakshatras": ["Hasta", "Chitra", "Rohini", "Uttara Phalguni", "Shravana"],
    },
    "Chitra": {
        "shastras": (
            "Ruled by Vishwakarma, divine architect. Symbol is a bright jewel. "
            "The native is attractive, artistic and well-dressed. "
            "Bestows creative brilliance and architectural vision."
        ),
        "modern": (
            "Outstanding visual sense with talent for design. "
            "Attractive personality that draws attention. "
            "Success in architecture, fashion, jewellery, and photography."
        ),
        "health": "Navel, lower abdomen, kidneys, lumbar region",
        "remedy": "Worship Vishwakarma. Chant 'Om Tvashtre Namah'. Offer colourful flowers.",
        "compatible_nakshatras": ["Chitra", "Hasta", "Mrigashira", "Swati", "Vishakha"],
    },
    "Swati": {
        "shastras": (
            "Ruled by Vayu, the wind god. Symbol is a young plant swaying. "
            "The native is independent, soft-spoken and righteous. "
            "Bestows adaptability, trade skills and restless independence."
        ),
        "modern": (
            "Diplomatic nature with strong business instincts. "
            "Self-made success through adaptability and charm. "
            "Success in trade, law, travel agencies, and diplomacy."
        ),
        "health": "Skin, kidneys, urinary tract, lower abdomen",
        "remedy": "Worship Vayu Dev. Chant 'Om Vayave Namah'. Offer green gram and incense.",
        "compatible_nakshatras": ["Swati", "Vishakha", "Ardra", "Punarvasu", "Chitra"],
    },
    "Vishakha": {
        "shastras": (
            "Ruled by Indra-Agni. Symbol is a triumphal archway. "
            "The native is ambitious, determined and single-minded. "
            "Bestows goal-oriented drive and eventual success."
        ),
        "modern": (
            "Powerful determination that overcomes all obstacles. "
            "Focused ambition, sometimes at cost of relationships. "
            "Success in politics, research, activism, and corporate leadership."
        ),
        "health": "Lower abdomen, kidneys, bladder, pancreas",
        "remedy": "Worship Indra-Agni. Chant 'Om Indragnibhyam Namah'. Perform havan.",
        "compatible_nakshatras": ["Vishakha", "Anuradha", "Swati", "Chitra", "Purva Ashadha"],
    },
    "Anuradha": {
        "shastras": (
            "Ruled by Mitra, god of friendship. "
            "The native is devoted, successful and lives in foreign lands. "
            "Bestows friendship, devotion and organizational power."
        ),
        "modern": (
            "Deep loyalty with talent for building lasting bonds. "
            "Success in group leadership and foreign connections. "
            "Excels in networking, music, astrology, and management."
        ),
        "health": "Bladder, genitals, rectum, nasal bones",
        "remedy": "Worship Mitra Dev. Chant 'Om Mitraya Namah'. Offer lotus flowers.",
        "compatible_nakshatras": ["Anuradha", "Jyeshtha", "Pushya", "Vishakha", "Shravana"],
    },
    "Jyeshtha": {
        "shastras": (
            "Ruled by Indra, king of gods. Symbol is a circular amulet. "
            "The native is valorous, wealthy and of virtuous disposition. "
            "Bestows seniority, protective instinct and occult knowledge."
        ),
        "modern": (
            "Natural protector with strong sense of responsibility. "
            "Leadership through experience, eldest-sibling energy. "
            "Success in military, police, occult, and administration."
        ),
        "health": "Colon, anus, genital organs, ovaries/prostate",
        "remedy": "Worship Lord Indra. Chant 'Om Indraya Namah'. Offer blue flowers.",
        "compatible_nakshatras": ["Jyeshtha", "Anuradha", "Ashlesha", "Revati", "Mula"],
    },
    "Mula": {
        "shastras": (
            "Ruled by Nirriti, goddess of dissolution. Symbol is tied roots. "
            "The native is proud, wealthy yet causes destruction to family. "
            "Bestows power to uproot problems and get to the core truth."
        ),
        "modern": (
            "Deep investigative nature seeking fundamental truths. "
            "Philosophical questioning, sometimes destructive before rebuilding. "
            "Success in research, medicine, herbalism, and philosophy."
        ),
        "health": "Hips, thighs, femur, sciatic nerves",
        "remedy": "Worship Nirrti/Kali. Chant 'Om Nirrtaye Namah'. Offer dark-coloured flowers.",
        "compatible_nakshatras": ["Mula", "Purva Ashadha", "Magha", "Jyeshtha", "Ashwini"],
    },
    "Purva Ashadha": {
        "shastras": (
            "Ruled by Apas (Waters). Symbol is an elephant tusk. "
            "The native is proud, attached to friends and invincible. "
            "Bestows purifying influence, charisma and early victory."
        ),
        "modern": (
            "Charismatic personality with power to influence masses. "
            "Strong debating skills and infectious enthusiasm. "
            "Success in media, law, motivation, and water-related fields."
        ),
        "health": "Thighs, hips, sacral region, sciatic nerve",
        "remedy": "Worship Apas Devta. Chant 'Om Apo Namah'. Offer water and white flowers.",
        "compatible_nakshatras": ["Purva Ashadha", "Uttara Ashadha", "Mula", "Purva Phalguni", "Vishakha"],
    },
    "Uttara Ashadha": {
        "shastras": (
            "Ruled by Vishwadevas (universal gods). Symbol is elephant tusk. "
            "The native is obedient, grateful and ultimately victorious. "
            "Bestows lasting success, deep integrity and universal appeal."
        ),
        "modern": (
            "Unstoppable determination with ethical foundation. "
            "Late bloomer who achieves permanent success. "
            "Success in government, law, social reform, and leadership."
        ),
        "health": "Thighs, knees, skin, bones",
        "remedy": "Worship Vishwadevas. Chant 'Om Vishvedevabhyo Namah'. Offer fruits and ghee.",
        "compatible_nakshatras": ["Uttara Ashadha", "Purva Ashadha", "Krittika", "Uttara Phalguni", "Shravana"],
    },
    "Shravana": {
        "shastras": (
            "Ruled by Vishnu, the preserver. Symbol is three footprints. "
            "The native is scholarly, famous and married to a good spouse. "
            "Bestows learning through listening, organizational skill."
        ),
        "modern": (
            "Excellent listener with talent for connecting knowledge. "
            "Media-savvy, persuasive communicator. "
            "Success in education, media, counselling, and travel."
        ),
        "health": "Knees, joints, skin, lymphatic system",
        "remedy": "Worship Lord Vishnu. Chant 'Om Namo Narayanaya'. Offer tulsi and milk.",
        "compatible_nakshatras": ["Shravana", "Dhanishta", "Rohini", "Hasta", "Anuradha"],
    },
    "Dhanishta": {
        "shastras": (
            "Ruled by the Vasus (eight elemental gods). Symbol is a drum. "
            "The native is wealthy, charitable and fond of music. "
            "Bestows material abundance, rhythm and adaptability."
        ),
        "modern": (
            "Musical talent combined with material ambition. "
            "Generous with resources, enjoys group activities. "
            "Success in music, real estate, sports, and science."
        ),
        "health": "Knees, ankles, limbs, back",
        "remedy": "Worship Vasu Devtas. Chant 'Om Vasubhyo Namah'. Offer sweets and music.",
        "compatible_nakshatras": ["Dhanishta", "Shatabhisha", "Mrigashira", "Chitra", "Shravana"],
    },
    "Shatabhisha": {
        "shastras": (
            "Ruled by Varuna, god of cosmic waters. Symbol is an empty circle. "
            "The native is truthful, sharp-witted and suffers early difficulties. "
            "Bestows healing power, secrecy and philosophical depth."
        ),
        "modern": (
            "Independent healer with scientific temperament. "
            "Secretive but highly knowledgeable, a lone worker. "
            "Success in medicine, astronomy, technology, and research."
        ),
        "health": "Calves, ankles, jaw, right side of body",
        "remedy": "Worship Lord Varuna. Chant 'Om Varunaya Namah'. Offer coconut and water.",
        "compatible_nakshatras": ["Shatabhisha", "Dhanishta", "Ardra", "Purva Bhadrapada", "Ashwini"],
    },
    "Purva Bhadrapada": {
        "shastras": (
            "Ruled by Aja Ekapada (one-footed goat). "
            "The native is wealthy, clever and subject to partner's influence. "
            "Bestows fiery purification, occult abilities and endurance."
        ),
        "modern": (
            "Intense spiritual warrior with reformist tendencies. "
            "Can be extreme in views but ultimately seeks transformation. "
            "Success in mysticism, writing, social work, and healing."
        ),
        "health": "Ankles, feet, toes, ribs",
        "remedy": "Worship Aja Ekapada. Chant 'Om Ajaikapadaya Namah'. Offer fire rituals.",
        "compatible_nakshatras": ["Purva Bhadrapada", "Uttara Bhadrapada", "Magha", "Purva Phalguni", "Shatabhisha"],
    },
    "Uttara Bhadrapada": {
        "shastras": (
            "Ruled by Ahir Budhnya (serpent of the deep). "
            "The native is eloquent, virtuous and happy. "
            "Bestows deep wisdom, spiritual enlightenment and stability."
        ),
        "modern": (
            "Profound thinker with balanced, compassionate outlook. "
            "Excellent counsellor and wise advisor. "
            "Success in philanthropy, spirituality, counselling, and writing."
        ),
        "health": "Feet, soles, toes, ribs, shins",
        "remedy": "Worship Ahir Budhnya. Chant 'Om Ahirbudhnayaya Namah'. Offer milk and flowers.",
        "compatible_nakshatras": ["Uttara Bhadrapada", "Purva Bhadrapada", "Krittika", "Magha", "Revati"],
    },
    "Revati": {
        "shastras": (
            "Ruled by Pushan, the nourisher and protector of travellers. "
            "The native is clean, wealthy and heroic. "
            "Bestows safe passage, prosperity and compassionate nature."
        ),
        "modern": (
            "Gentle, caring soul with love for all creatures. "
            "Creative dreamer with psychic sensitivity. "
            "Success in travel, creative arts, animal care, and spirituality."
        ),
        "health": "Feet, ankles, lymphatic system",
        "remedy": "Worship Pushan. Chant 'Om Pushne Namah'. Offer milk and sweets.",
        "compatible_nakshatras": ["Revati", "Uttara Bhadrapada", "Ashlesha", "Jyeshtha", "Ashwini"],
    },
}


# ============================================================
# 3. PLANET_IN_HOUSE -- 9 Planets x 12 Houses
# ============================================================

PLANET_IN_HOUSE: Dict[str, Dict[int, Dict[str, str]]] = {
    "Sun": {
        1: {
            "auspicious": "Strong personality, leadership qualities, good health and vitality. Respected in society, natural authority figure. Self-made success.",
            "inauspicious": "Ego conflicts, headstrong nature. May suffer from bile disorders. Strained relations with father if afflicted.",
        },
        2: {
            "auspicious": "Wealth through government or authority. Impressive speech that commands attention. Strong family values.",
            "inauspicious": "Harsh speech, eye problems. Family disputes over inheritance. Earnings through struggle rather than ease.",
        },
        3: {
            "auspicious": "Courageous and adventurous. Good relations with siblings. Success in communications, writing, or media.",
            "inauspicious": "Conflicts with siblings or neighbours. Short temper leading to strained relations. Chest or shoulder problems.",
        },
        4: {
            "auspicious": "Government property or land ownership. Inner strength and emotional clarity. Parental support in early life.",
            "inauspicious": "Troubled domestic peace. Heart problems possible. Strained relationship with mother. Frequent changes of residence.",
        },
        5: {
            "auspicious": "Intelligent and creative. Good advisory skills. Children bring pride. Success in speculation and politics.",
            "inauspicious": "Delayed children or difficulties with firstborn. Stomach ailments. Ego clashes in romantic relationships.",
        },
        6: {
            "auspicious": "Victory over enemies and competitors. Good in service and administration. Strong immune system.",
            "inauspicious": "Conflicts with subordinates. Father's health may suffer. Prone to acidity and digestive issues.",
        },
        7: {
            "auspicious": "Spouse from respected family. Good business partnerships. Foreign travel for work.",
            "inauspicious": "Dominating nature strains marriage. Late marriage likely. Partner may be headstrong. Ego battles with partners.",
        },
        8: {
            "auspicious": "Interest in occult and research. Government benefits. Longevity of father if well-placed.",
            "inauspicious": "Eye disease, weak constitution. Loss through government penalties. Father may face chronic health issues.",
        },
        9: {
            "auspicious": "Blessed by fortune and divine grace. Pilgrimage to sacred places. Father is influential and supportive.",
            "inauspicious": "Conflicts with father or guru. Self-righteous attitude. Late luck in life. Religious dogmatism.",
        },
        10: {
            "auspicious": "High position in career, government favour. Natural authority in profession. Fame and public recognition.",
            "inauspicious": "Excessive ambition creates enemies. Work-life imbalance. Authoritarian management style.",
        },
        11: {
            "auspicious": "Excellent gains, wealthy friends. Fulfilment of desires. Influential social circle. Elder sibling is supportive.",
            "inauspicious": "Selfish friendships based on status. Ear problems. Gains come with strings attached.",
        },
        12: {
            "auspicious": "Spiritual inclination, interest in moksha. Government posting abroad. Charitable disposition.",
            "inauspicious": "Low vitality, eye problems. Loss of position. Strained relationship with father. Expenses exceed income.",
        },
    },
    "Moon": {
        1: {
            "auspicious": "Attractive personality, emotional sensitivity. Popular and well-liked. Good intuition and nurturing nature.",
            "inauspicious": "Over-emotional, indecisive. Health fluctuates with Moon phases. Restlessness and anxiety.",
        },
        2: {
            "auspicious": "Sweet speech, family-oriented. Good wealth accumulation. Beautiful eyes and face. Poetic talent.",
            "inauspicious": "Fluctuating finances. Overly sensitive to criticism. Eye ailments if afflicted.",
        },
        3: {
            "auspicious": "Good communication skills, creative writing ability. Helpful siblings, especially sisters. Short pleasant journeys.",
            "inauspicious": "Mental restlessness, inability to focus. Strained sibling relations. Chest congestion.",
        },
        4: {
            "auspicious": "Happy domestic life, close to mother. Property and vehicle ownership. Inner contentment and mental peace.",
            "inauspicious": "Emotional dependency on mother. Frequent changes of residence. Water-related property damage.",
        },
        5: {
            "auspicious": "Sharp intellect, romantic nature. Creative and artistic talents. Good relationship with children.",
            "inauspicious": "Emotional instability in romance. Mood-dependent decision-making. Stomach ailments.",
        },
        6: {
            "auspicious": "Service-oriented, good in healing professions. Overcomes enemies through tact. Strong maternal instincts.",
            "inauspicious": "Emotional enemies, anxiety disorders. Digestive issues, especially dairy intolerance. Mental stress from work.",
        },
        7: {
            "auspicious": "Attractive, caring spouse. Happy married life. Good business partnerships. Social popularity.",
            "inauspicious": "Emotional dependency on partner. Spouse may be moody. Multiple relationships if afflicted.",
        },
        8: {
            "auspicious": "Psychic sensitivity, inheritance from mother's side. Long life with interest in occult sciences.",
            "inauspicious": "Emotional turmoil, depression tendency. Chronic health issues. Mother's health may suffer.",
        },
        9: {
            "auspicious": "Devotional nature, love of pilgrimage. Fortunate mother. Success in foreign lands. Spiritual inclination.",
            "inauspicious": "Wavering faith, restless spiritual seeking. Mother may travel far. Emotional approach to religion.",
        },
        10: {
            "auspicious": "Public popularity, career in public-facing roles. Fame and recognition. Success in liquids, dairy, or hospitality.",
            "inauspicious": "Unstable career, frequent job changes. Public mood affects success. Emotional decision-making at work.",
        },
        11: {
            "auspicious": "Many friends, especially female. Gains through mother and women. Fulfilment of desires. Social networking skill.",
            "inauspicious": "Emotional attachment to gains. Fluctuating income. Over-dependence on social approval.",
        },
        12: {
            "auspicious": "Spiritual dreams, intuitive insight. Charity and compassion. Success in foreign lands or hospitals.",
            "inauspicious": "Sleep disorders, excessive imagination. Eye weakness. Emotional isolation. Expenditure on mother's health.",
        },
    },
    "Mars": {
        1: {
            "auspicious": "Courageous, energetic and physically strong. Leadership in competitive fields. Quick decision-making ability.",
            "inauspicious": "Aggressive temperament, prone to accidents. Scar on head or face. Mangala Dosha affects marriage.",
        },
        2: {
            "auspicious": "Bold speech, wealth through property or military. Strong family protector. Good at debate.",
            "inauspicious": "Harsh speech causes family conflicts. Dental problems. Loss of wealth through arguments or litigation.",
        },
        3: {
            "auspicious": "Brave, adventurous with strong siblings. Success in sports, military, or surgery. Strong willpower.",
            "inauspicious": "Conflicts with siblings. Injury to arms or shoulders. Reckless courage leads to danger.",
        },
        4: {
            "auspicious": "Property and land ownership. Strong domestic foundation. Determined and self-reliant.",
            "inauspicious": "Domestic unrest, conflict with mother. Property disputes. Heart or blood pressure issues.",
        },
        5: {
            "auspicious": "Sharp intelligence, success in competition. Athletic children. Good strategic thinking.",
            "inauspicious": "Impulsive decisions in speculation. Stomach ulcers. Difficulties with first child. Hot temper in romance.",
        },
        6: {
            "auspicious": "Excellent position -- victory over enemies, debts and disease. Good in military, surgery, law enforcement.",
            "inauspicious": "Aggressive with subordinates. Blood disorders. Injury from sharp objects. Cousin conflicts.",
        },
        7: {
            "auspicious": "Passionate marriage, energetic spouse. Success in business partnerships. Foreign connections.",
            "inauspicious": "Mangala Dosha -- marriage conflicts, possible separation. Spouse is dominating. Blood pressure issues.",
        },
        8: {
            "auspicious": "Long life, interest in tantra and research. Sudden gains through inheritance. Strong survival instinct.",
            "inauspicious": "Accidents, surgery, chronic blood disorders. Sudden crises. Piles or fistula. Marital discord.",
        },
        9: {
            "auspicious": "Dharmic warrior, fights for justice. Pilgrimage to sacred places. Father is brave and influential.",
            "inauspicious": "Conflicts with father and guru. Aggressive religious views. Legal troubles. Accident during travel.",
        },
        10: {
            "auspicious": "Excellent career drive, leadership in profession. Success in engineering, military, police, or surgery.",
            "inauspicious": "Ruthless ambition, workplace conflicts. Authority clashes with superiors. Blood pressure at work.",
        },
        11: {
            "auspicious": "High gains, influential friends. Desires fulfilled through effort. Success in property dealing.",
            "inauspicious": "Conflicts with elder siblings. Friends become rivals. Ear infections.",
        },
        12: {
            "auspicious": "Expenses on good causes, interest in spirituality. Success in foreign lands. Bed pleasures.",
            "inauspicious": "Hidden enemies, hospitalization. Eye problems. Disturbed sleep. Excessive expenditure.",
        },
    },
    "Mercury": {
        1: {
            "auspicious": "Intelligent, witty and youthful appearance. Excellent communication skills. Success in business and trade.",
            "inauspicious": "Nervous disposition, overthinking. Skin allergies. Inconsistency in efforts.",
        },
        2: {
            "auspicious": "Eloquent speech, wealth through intellect. Good education. Family of scholars. Financial acumen.",
            "inauspicious": "Speech defects if afflicted. Lying tendency. Wealth fluctuates with business cycles.",
        },
        3: {
            "auspicious": "Excellent writer, communicator, media professional. Good relations with siblings. Short travel brings gains.",
            "inauspicious": "Mental restlessness, nervous exhaustion. Sibling rivalry over intellect. Shoulder/arm nerve issues.",
        },
        4: {
            "auspicious": "Good education, intelligent mother. Multiple properties. Academic success and mental peace.",
            "inauspicious": "Frequent change of residence. Anxiety at home. Mother may be overly critical.",
        },
        5: {
            "auspicious": "Brilliant intellect, success in education and speculation. Intelligent children. Good in mantras.",
            "inauspicious": "Over-analysis paralyzes decisions. Stomach gas issues. Children may be too intellectual, lacking emotion.",
        },
        6: {
            "auspicious": "Victory over enemies through intelligence. Good in service, accounting, law. Analytical problem-solving.",
            "inauspicious": "Mental stress from overwork. Nervous disorders. Skin diseases. Conflicts with maternal relatives.",
        },
        7: {
            "auspicious": "Intelligent, youthful spouse. Good business partnerships. Success in trade and communication.",
            "inauspicious": "Multiple relationships if afflicted. Spouse is overly critical. Business disputes.",
        },
        8: {
            "auspicious": "Research ability, occult study. Longevity. Success in insurance, investigation, or psychology.",
            "inauspicious": "Nervous disorders, speech problems. Inheritance disputes. Anxiety and phobias.",
        },
        9: {
            "auspicious": "Higher education, philosophical mind. Good fortune through knowledge. Foreign education or work.",
            "inauspicious": "Intellectual arrogance about beliefs. Father may be distant. Indecisiveness about faith.",
        },
        10: {
            "auspicious": "Success in business, trade, writing, or IT. Quick career advancement through intellect. Multiple income sources.",
            "inauspicious": "Unstable career path, too many options. Workplace gossip. Ethical compromises for success.",
        },
        11: {
            "auspicious": "Intelligent friends, gains through networking. Multiple income streams. Desires fulfilled through cleverness.",
            "inauspicious": "Unreliable friends. Gains through dubious means if afflicted. Hearing issues.",
        },
        12: {
            "auspicious": "Success in foreign lands. Spiritual intelligence. Good imagination for creative writing.",
            "inauspicious": "Excessive worry, insomnia. Speech problems. Expenditure on education. Secret enemies.",
        },
    },
    "Jupiter": {
        1: {
            "auspicious": "Wise, optimistic and fortunate. Large-hearted and respected. Good health, natural teacher and advisor.",
            "inauspicious": "Overweight, overconfident. May be preachy. Liver issues if afflicted.",
        },
        2: {
            "auspicious": "Wealthy, eloquent and well-educated. Large family. Truthful speech brings respect. Excellent financial sense.",
            "inauspicious": "Extravagant spending. Over-indulgence in food. Speech may be long-winded.",
        },
        3: {
            "auspicious": "Wise siblings, good communication about higher topics. Success in publishing and teaching. Courageous beliefs.",
            "inauspicious": "Lazy about daily effort. Over-promises. Conflicts with siblings over philosophy.",
        },
        4: {
            "auspicious": "Excellent -- happy home, good mother, property, vehicles. Inner wisdom and contentment. Academic foundation.",
            "inauspicious": "Too comfortable, resists change. Excessive attachment to home. Liver or weight issues.",
        },
        5: {
            "auspicious": "Highly intelligent, wise children. Success in education, advisory roles, and speculation. Spiritual merit (Purva Punya).",
            "inauspicious": "Over-confidence in speculation. Spoils children with excessive generosity. Liver troubles.",
        },
        6: {
            "auspicious": "Overcomes enemies and disease through wisdom. Good in medical or legal advisory. Service brings spiritual growth.",
            "inauspicious": "Debts from over-generosity. Liver/sugar disorders. Conflicts with in-laws.",
        },
        7: {
            "auspicious": "Wise, virtuous spouse. Happy marriage and partnerships. Foreign business success. Social standing through marriage.",
            "inauspicious": "Spouse may be overweight or overbearing. Partner's beliefs clash. Delayed marriage.",
        },
        8: {
            "auspicious": "Long life, interest in mysticism and scriptures. Inheritance. Protection from sudden calamities.",
            "inauspicious": "Financial ups and downs. Liver and digestive issues. Difficulty with in-laws' finances.",
        },
        9: {
            "auspicious": "Extremely fortunate -- best house for Jupiter. Religious, father is wise, long pilgrimages. Guru's blessings throughout life.",
            "inauspicious": "Religious dogmatism. Over-reliance on luck. Conflict between different gurus.",
        },
        10: {
            "auspicious": "High position, respected career. Success in law, education, banking, or religion. Famous and influential.",
            "inauspicious": "Career overshadows family. Ethical dilemmas at work. Liver problems from stress.",
        },
        11: {
            "auspicious": "Excellent gains, wealthy and influential friends. All desires fulfilled. Elder sibling is helpful and wise.",
            "inauspicious": "Gains breed complacency. Friendship with self-righteous people. Ear or hearing issues.",
        },
        12: {
            "auspicious": "Spiritual liberation, charity, foreign residence. Peaceful end of life. Bed comforts and divine protection.",
            "inauspicious": "Excessive spending on charity. Isolation from society. Liver ailments. Secret extra-marital affairs if afflicted.",
        },
    },
    "Venus": {
        1: {
            "auspicious": "Attractive, charming and artistic. Love of beauty and luxury. Happy disposition. Success in arts and fashion.",
            "inauspicious": "Vanity and self-indulgence. Over-emphasis on appearance. Reproductive health issues.",
        },
        2: {
            "auspicious": "Wealthy, sweet-spoken. Beautiful face and eyes. Family prosperity. Success in finance and luxury goods.",
            "inauspicious": "Overspending on luxuries. Indulgent eating habits. Eye problems related to cosmetics.",
        },
        3: {
            "auspicious": "Artistic siblings. Success in performing arts, media, and communication. Pleasant short travels.",
            "inauspicious": "Superficial relationships with siblings. Over-indulgence in social media. Throat issues.",
        },
        4: {
            "auspicious": "Luxurious home, fine vehicles. Happy mother. Domestic bliss with beautiful furnishings. Land and property gains.",
            "inauspicious": "Excessive attachment to comforts. Mother may be overly materialistic. Heart related to emotions.",
        },
        5: {
            "auspicious": "Romantic, creative and artistic. Beautiful children. Success in entertainment, fashion, and speculation.",
            "inauspicious": "Multiple love affairs. Over-indulgence in pleasures. Complications in pregnancy if afflicted.",
        },
        6: {
            "auspicious": "Overcomes enemies through charm and diplomacy. Success in service industries. Health through balanced living.",
            "inauspicious": "Urinary and reproductive health issues. Conflicts in relationships. Debts from luxury spending.",
        },
        7: {
            "auspicious": "Beautiful, loving spouse. Happy marriage. Success in partnerships and business. Social charm.",
            "inauspicious": "Excessive attachment to partner. Multiple relationships if afflicted. Partner may be materialistic.",
        },
        8: {
            "auspicious": "Long life, sudden financial gains. Interest in tantra and occult arts. Inheritance of luxury items.",
            "inauspicious": "Reproductive health problems. Secret affairs. Marital discord over finances. Venereal diseases if badly afflicted.",
        },
        9: {
            "auspicious": "Fortunate in love, wealthy father. Pilgrimage to beautiful places. Artistic religious expression.",
            "inauspicious": "Father may be pleasure-loving. Wavering between material and spiritual. Conflicts with guru.",
        },
        10: {
            "auspicious": "Successful career in arts, luxury, fashion, or diplomacy. Public adoration. Glamorous profession.",
            "inauspicious": "Workplace romances create scandal. Career dependent on appearance. Ethical compromises for success.",
        },
        11: {
            "auspicious": "Wealthy friends, gains through women. Fulfilment of desires for luxury. Influential social circle.",
            "inauspicious": "Friendships based on material benefit. Excessive desire. Ear or kidney issues.",
        },
        12: {
            "auspicious": "Bed pleasures, foreign luxury. Spiritual devotion through beauty. Success in foreign lands.",
            "inauspicious": "Excessive expenditure on pleasures. Secret affairs. Eye problems. Loss of wealth through indulgence.",
        },
    },
    "Saturn": {
        1: {
            "auspicious": "Disciplined, hardworking and enduring. Success through persistent effort. Long life. Lean physique.",
            "inauspicious": "Chronic health issues, depression tendency. Difficult childhood. Delays in all matters. Pessimistic outlook.",
        },
        2: {
            "auspicious": "Wealth through hard work and savings. Disciplined speech. Family wealth accumulates slowly.",
            "inauspicious": "Harsh or limited speech. Dental problems. Family poverty or restrictions. Late wealth.",
        },
        3: {
            "auspicious": "Courageous through discipline. Younger siblings are hardworking. Success in writing and communication after struggle.",
            "inauspicious": "Hearing problems, shoulder pain. Estranged siblings. Short journeys are difficult.",
        },
        4: {
            "auspicious": "Property through sustained effort. Old or inherited home. Discipline in domestic matters.",
            "inauspicious": "Lack of domestic peace, cold home environment. Mother's health suffers. Heart or chest problems. Depression.",
        },
        5: {
            "auspicious": "Deep thinker, mature intelligence. Disciplined children. Success in structured speculation.",
            "inauspicious": "Delayed children, stomach ailments. Pessimistic outlook on life. Romance lacks warmth.",
        },
        6: {
            "auspicious": "Excellent -- victory over enemies and disease through endurance. Good for service, law, and labour management.",
            "inauspicious": "Chronic diseases if afflicted. Conflicts with servants. Maternal uncle's troubles.",
        },
        7: {
            "auspicious": "Mature, reliable spouse. Late but stable marriage. Business success with older partners.",
            "inauspicious": "Delayed marriage, cold spouse. Marital dissatisfaction. Partner is older or chronically ill.",
        },
        8: {
            "auspicious": "Long life, interest in mysticism. Success in mining, oil, or underground resources. Research ability.",
            "inauspicious": "Chronic ailments, accidents. Inheritance delayed or denied. Piles, joint pain. Life-threatening events.",
        },
        9: {
            "auspicious": "Disciplined spiritual practice. Father is hardworking. Success through traditional religion and duty.",
            "inauspicious": "Father faces hardship. Conflict with guru. Luck comes very late. Rigid religious views.",
        },
        10: {
            "auspicious": "Excellent career position through hard work. Success in government, mining, law, or administration. Late but lasting fame.",
            "inauspicious": "Career setbacks and delays. Conflict with authority. Knee and joint problems.",
        },
        11: {
            "auspicious": "Steady gains over time. Older or mature friends. Long-term financial goals are met. Elder sibling is disciplined.",
            "inauspicious": "Delayed fulfilment of desires. Hearing problems. Friends are restrictive or burdensome.",
        },
        12: {
            "auspicious": "Spiritual detachment, foreign residence. Interest in meditation and isolation. Charitable work.",
            "inauspicious": "Hospitalization, imprisonment if badly afflicted. Chronic insomnia. Excessive expenditure. Foot and leg problems.",
        },
    },
    "Rahu": {
        1: {
            "auspicious": "Worldly ambition, magnetic personality. Success in foreign lands or unconventional fields. Innovative thinking.",
            "inauspicious": "Identity confusion, deceptive appearance. Mental anxiety. Unconventional or controversial reputation.",
        },
        2: {
            "auspicious": "Wealth through unconventional means. Multilingual ability. Foreign food or cuisine expertise.",
            "inauspicious": "Harsh or deceptive speech. Family conflicts. Dental issues. Wealth through dubious means.",
        },
        3: {
            "auspicious": "Bold communicator, success in media and technology. Adventurous short travels. Courageous and daring.",
            "inauspicious": "Troubled relations with siblings. Reckless risk-taking. Hearing or throat problems.",
        },
        4: {
            "auspicious": "Foreign property, modern home. Success away from birthplace. Unconventional domestic setup.",
            "inauspicious": "No peace at home, mother's health suffers. Haunted or disputed property. Heart anxiety.",
        },
        5: {
            "auspicious": "Genius-level intelligence in technical fields. Success in speculation and stock market. Unconventional creativity.",
            "inauspicious": "Difficult children, stomach ailments. Risky speculation. Deceptive romantic affairs.",
        },
        6: {
            "auspicious": "Victory over enemies through cunning. Success in medicine, litigation, and competition. Strong immune response.",
            "inauspicious": "Mysterious illnesses, misdiagnosis. Conflicts with maternal relatives. Obsessive-compulsive tendencies.",
        },
        7: {
            "auspicious": "Foreign spouse or unconventional marriage. Success in international business. Magnetic attraction to others.",
            "inauspicious": "Marriage instability, deception in partnership. Spouse from different background causes adjustment issues.",
        },
        8: {
            "auspicious": "Sudden transformation and gains. Interest in occult, tantric practices. Inheritance from unexpected sources.",
            "inauspicious": "Sudden accidents, poisoning risk. Chronic mysterious ailments. Scandal and disgrace if badly afflicted.",
        },
        9: {
            "auspicious": "Unorthodox spiritual path, foreign guru. Luck through unconventional means. Pilgrimage to foreign lands.",
            "inauspicious": "Conflicts with father and teachers. Misguided spiritual pursuits. Legal troubles abroad.",
        },
        10: {
            "auspicious": "Powerful career in politics, technology, or foreign companies. Sudden rise to fame. Unconventional profession.",
            "inauspicious": "Sudden career downfall. Public scandal. Unethical means for success. Knee problems.",
        },
        11: {
            "auspicious": "Massive gains through networking and technology. Influential foreign friends. Desires fulfilled in unusual ways.",
            "inauspicious": "Deceptive friends. Gains that don't satisfy. Elder sibling faces foreign troubles.",
        },
        12: {
            "auspicious": "Spiritual awakening, foreign residence. Success in research, isolation work, or spiritual retreat.",
            "inauspicious": "Hidden enemies, hospitalization abroad. Insomnia, nightmares. Expenditure on foreign travel. Feet problems.",
        },
    },
    "Ketu": {
        1: {
            "auspicious": "Spiritual personality, psychic ability. Detachment from material world. Past-life skills manifest naturally.",
            "inauspicious": "Identity crisis, mysterious health issues. Socially awkward. Scars or marks on body.",
        },
        2: {
            "auspicious": "Spiritual wealth, detached from materialism. Family has spiritual or occult background. Mystical speech.",
            "inauspicious": "Speech defects, family estrangement. Financial losses. Eye problems, especially left eye.",
        },
        3: {
            "auspicious": "Courageous in spiritual pursuits. Mystical writing ability. Siblings on spiritual path.",
            "inauspicious": "Troubled relations with siblings. Communication breakdown. Shoulder or arm injuries.",
        },
        4: {
            "auspicious": "Detached from material comforts. Spiritual home environment. Interest in ancient or demolished properties.",
            "inauspicious": "No domestic peace, separation from mother. Property disputes. Heart or chest ailments.",
        },
        5: {
            "auspicious": "Highly intuitive intelligence. Past-life spiritual merit (Purva Punya). Interest in mantra and meditation.",
            "inauspicious": "Difficulties with children. Stomach ailments. Poor results in speculation. Confused romantic life.",
        },
        6: {
            "auspicious": "Victory over hidden enemies. Interest in alternative healing. Overcomes diseases through spiritual remedies.",
            "inauspicious": "Mysterious chronic diseases. Maternal uncle faces troubles. Injury from animals or insects.",
        },
        7: {
            "auspicious": "Spiritual partnership, karmic marriage. Spouse has past-life connection. Detachment leads to better relationships.",
            "inauspicious": "Marriage dissatisfaction, spouse is secretive. Delayed or denied marriage. Separation or partner's ill health.",
        },
        8: {
            "auspicious": "Deep occult knowledge, moksha yoga possibility. Past-life spiritual attainments. Interest in meditation and tantra.",
            "inauspicious": "Sudden losses, accidents. Chronic mysterious ailments. Disgrace through past actions.",
        },
        9: {
            "auspicious": "Deep spiritual wisdom from past lives. Natural philosopher. Pilgrimage to ancient sacred sites.",
            "inauspicious": "Father faces spiritual crisis. Conflict with established religion. Luck is inconsistent.",
        },
        10: {
            "auspicious": "Career in spiritual, healing, or research fields. Detachment from ambition brings unexpected success.",
            "inauspicious": "Career instability, disinterest in worldly achievement. Sudden loss of position. Knee or skin problems.",
        },
        11: {
            "auspicious": "Gains through spiritual pursuits. Fulfilled through non-material desires. Unusual but loyal friends.",
            "inauspicious": "Unfulfilled material desires. Elder sibling faces difficulties. Hearing or ear problems.",
        },
        12: {
            "auspicious": "Excellent for moksha and spiritual liberation. Deep meditation ability. Past-life spiritual completion.",
            "inauspicious": "Excessive isolation, hospitalization. Eye problems. Expenditure on spiritual frauds. Foot ailments.",
        },
    },
}


# ============================================================
# 4. BHAVESH_INTERPRETATIONS -- Lord of Nth House in Mth House
#    Key: (lord_house, placed_house) -> text
#    144 combinations (12 x 12)
# ============================================================

BHAVESH_INTERPRETATIONS: Dict[Tuple[int, int], str] = {
    # --- Lord of 1st house ---
    (1, 1): "Lagnesh in lagna: Strong personality, self-made success, good health. The native is confident and takes initiative in life.",
    (1, 2): "Lagnesh in 2nd: Wealth through own efforts. Good speech and family relations. Self-worth tied to financial security.",
    (1, 3): "Lagnesh in 3rd: Courageous, self-reliant with good communication skills. Success through personal initiative and short travels.",
    (1, 4): "Lagnesh in 4th: Happy domestic life, attached to mother. Gains property and vehicles. Inner contentment.",
    (1, 5): "Lagnesh in 5th: Intelligent, creative, blessed with good children. Success in education and speculation. Purva Punya yoga.",
    (1, 6): "Lagnesh in 6th: Struggles with health and enemies. Success through service but life requires constant effort to overcome obstacles.",
    (1, 7): "Lagnesh in 7th: Marriage defines life direction. Success through partnerships. May live away from birthplace after marriage.",
    (1, 8): "Lagnesh in 8th: Difficult placement -- health issues, obstacles in life. Interest in occult. Life marked by transformation.",
    (1, 9): "Lagnesh in 9th: Very fortunate. Religious, father is helpful. Luck favours the native. Success in higher education.",
    (1, 10): "Lagnesh in 10th: Excellent career success. Public recognition. Life focused on professional achievement. Self-made leader.",
    (1, 11): "Lagnesh in 11th: Gains and fulfilment of desires. Wealthy friends help. Ambitions are realized. Good income.",
    (1, 12): "Lagnesh in 12th: Expenses on self, foreign travel or residence. Spiritual inclination. May face health setbacks.",

    # --- Lord of 2nd house ---
    (2, 1): "2nd lord in 1st: Self-earned wealth. Good speaker. Personality reflects family values. Financial independence.",
    (2, 2): "2nd lord in 2nd: Stable finances, good family life. Truthful speech. Accumulates wealth steadily.",
    (2, 3): "2nd lord in 3rd: Earnings through communication, writing, or siblings. Short travels for income. Courageous speaker.",
    (2, 4): "2nd lord in 4th: Wealth through property, vehicles, or mother. Comfortable home. Education brings income.",
    (2, 5): "2nd lord in 5th: Wealth through intellect, speculation, or children. Good financial planning. Investments prosper.",
    (2, 6): "2nd lord in 6th: Financial struggles, debts. Wealth through service or medical field. Expenditure on health.",
    (2, 7): "2nd lord in 7th: Wealth through marriage or business partnership. Spouse brings financial stability.",
    (2, 8): "2nd lord in 8th: Financial ups and downs. Inheritance possible. Joint finances with spouse. Insurance gains.",
    (2, 9): "2nd lord in 9th: Fortunate for wealth. Father is wealthy. Earnings through religion, law, or foreign connections.",
    (2, 10): "2nd lord in 10th: Career brings wealth. Good income from profession. Financial status depends on career position.",
    (2, 11): "2nd lord in 11th: Excellent wealth combination. Multiple income sources. Friends help in financial growth.",
    (2, 12): "2nd lord in 12th: Expenditure exceeds income. Loss of family wealth. Money spent on foreign travel or charity.",

    # --- Lord of 3rd house ---
    (3, 1): "3rd lord in 1st: Courageous personality. Success through own initiative. Good relationship with siblings influences character.",
    (3, 2): "3rd lord in 2nd: Earnings through communication, writing, or media. Siblings contribute to family wealth.",
    (3, 3): "3rd lord in 3rd: Strong-willed, brave, and self-reliant. Good siblings. Success in media and communication.",
    (3, 4): "3rd lord in 4th: Siblings connected to property. Courage through emotional security. Writing from home.",
    (3, 5): "3rd lord in 5th: Creative communication, artistic talent. Siblings connected to children. Success in performing arts.",
    (3, 6): "3rd lord in 6th: Conflicts with siblings. Courage in overcoming enemies. Success in competitive communication.",
    (3, 7): "3rd lord in 7th: Spouse is brave and communicative. Business partnership with siblings. Short travels for marriage.",
    (3, 8): "3rd lord in 8th: Sibling faces difficulties. Courage through transformation. Interest in occult writing.",
    (3, 9): "3rd lord in 9th: Fortunate siblings. Courage in religious pursuits. Pilgrimage through short travels.",
    (3, 10): "3rd lord in 10th: Career in communication, media, or writing. Professional courage. Siblings help in career.",
    (3, 11): "3rd lord in 11th: Gains through siblings and communication. Brave friends. Desires fulfilled through initiative.",
    (3, 12): "3rd lord in 12th: Loss of courage, estranged siblings. Expenses through short travels. Left hand/arm weakness.",

    # --- Lord of 4th house ---
    (4, 1): "4th lord in 1st: Happy personality rooted in domestic bliss. Mother's influence shapes character. Property owner.",
    (4, 2): "4th lord in 2nd: Wealth through property and mother. Family home is prosperous. Good education leads to wealth.",
    (4, 3): "4th lord in 3rd: Short travels from home. Siblings connected to property. Courage through emotional security.",
    (4, 4): "4th lord in 4th: Excellent domestic happiness. Strong mother. Multiple properties and vehicles. Academic success.",
    (4, 5): "4th lord in 5th: Intelligent, good education. Children bring domestic happiness. Creative home environment.",
    (4, 6): "4th lord in 6th: Domestic troubles, mother's health issues. Property disputes. Lack of mental peace.",
    (4, 7): "4th lord in 7th: Happy marriage brings domestic peace. Spouse provides comfortable home. Property through partnership.",
    (4, 8): "4th lord in 8th: Property disputes, mother's health. Domestic upheaval. Renovation of old properties.",
    (4, 9): "4th lord in 9th: Fortunate home, religious mother. Property through luck. Higher education brings peace.",
    (4, 10): "4th lord in 10th: Career connected to property, education, or agriculture. Professional success brings domestic peace.",
    (4, 11): "4th lord in 11th: Gains through property. Mother's friends are helpful. Domestic desires fulfilled.",
    (4, 12): "4th lord in 12th: Loss of property, distant from mother. Foreign residence. Expenses on home and education.",

    # --- Lord of 5th house ---
    (5, 1): "5th lord in 1st: Intelligent, creative personality. Children influence character. Past-life merit manifests.",
    (5, 2): "5th lord in 2nd: Wealth through intellect and children. Family values education. Good financial planning.",
    (5, 3): "5th lord in 3rd: Creative communication, artistic writing. Siblings connected to children. Performing arts talent.",
    (5, 4): "5th lord in 4th: Education leads to domestic happiness. Creative home. Mother-child relationship is strong.",
    (5, 5): "5th lord in 5th: Excellent intelligence, blessed children. Strong Purva Punya. Success in education and arts.",
    (5, 6): "5th lord in 6th: Difficulties with children, stomach ailments. Intelligence used in service. Competitive exams.",
    (5, 7): "5th lord in 7th: Love marriage likely. Spouse is intelligent. Children connected to partnerships.",
    (5, 8): "5th lord in 8th: Difficulties with children. Intellect used in research and occult. Speculation losses.",
    (5, 9): "5th lord in 9th: Highly fortunate combination. Great intellect, religious children. Luck through education.",
    (5, 10): "5th lord in 10th: Career in education, arts, or advisory. Professional success through intelligence.",
    (5, 11): "5th lord in 11th: Gains through intellect and children. Investment income. Creative desires fulfilled.",
    (5, 12): "5th lord in 12th: Loss of intelligence clarity. Children may settle abroad. Expenses through speculation.",

    # --- Lord of 6th house ---
    (6, 1): "6th lord in 1st: Health challenges shape personality. Success through overcoming obstacles. Service-oriented life.",
    (6, 2): "6th lord in 2nd: Debts affect family wealth. Health expenses. Earning through medical or legal service.",
    (6, 3): "6th lord in 3rd: Courageous in defeating enemies. Conflicts with siblings. Success in competitive fields.",
    (6, 4): "6th lord in 4th: Domestic unrest, mother's health. Property through litigation. No mental peace.",
    (6, 5): "6th lord in 5th: Children face health issues. Intelligence used to overcome enemies. Stomach ailments.",
    (6, 6): "6th lord in 6th: Viparita Raja Yoga -- enemies destroy themselves. Victory in competition. Strong health.",
    (6, 7): "6th lord in 7th: Marital discord, spouse's health issues. Business disputes. Enemies through partnerships.",
    (6, 8): "6th lord in 8th: Chronic health issues. Debts multiply. Enemies create sudden crises.",
    (6, 9): "6th lord in 9th: Father faces health issues. Conflict with religion. Legal troubles with authority.",
    (6, 10): "6th lord in 10th: Career in medicine, law, or service. Professional competition. Enemies at workplace.",
    (6, 11): "6th lord in 11th: Gains through service and competition. Victory over enemies brings wealth.",
    (6, 12): "6th lord in 12th: Viparita Raja Yoga -- enemies are neutralized. Health improves in foreign land. Debts clear.",

    # --- Lord of 7th house ---
    (7, 1): "7th lord in 1st: Spouse influences personality strongly. Marriage-focused life. Partnership defines identity.",
    (7, 2): "7th lord in 2nd: Wealth through marriage or business. Spouse contributes to family finances.",
    (7, 3): "7th lord in 3rd: Spouse is courageous and communicative. Short travels for business. Sibling helps in marriage.",
    (7, 4): "7th lord in 4th: Happy marriage brings domestic bliss. Spouse provides comfortable home. Mother approves of partner.",
    (7, 5): "7th lord in 5th: Love marriage. Spouse is intelligent. Romance leads to children. Creative partnerships.",
    (7, 6): "7th lord in 6th: Marital problems, spouse's health. Divorce possibility if afflicted. Enemies through partnerships.",
    (7, 7): "7th lord in 7th: Strong marriage and partnerships. Spouse is loyal and supportive. Business success.",
    (7, 8): "7th lord in 8th: Spouse faces health challenges. Marriage undergoes transformation. In-law difficulties.",
    (7, 9): "7th lord in 9th: Fortunate marriage, spouse is religious. Father approves of partner. Foreign spouse possible.",
    (7, 10): "7th lord in 10th: Career through partnerships. Spouse helps professionally. Public recognition through marriage.",
    (7, 11): "7th lord in 11th: Gains through marriage and partnerships. Spouse brings financial growth. Desires fulfilled.",
    (7, 12): "7th lord in 12th: Spouse from foreign land. Bed pleasures. Marriage expenses high. Partner may be secretive.",

    # --- Lord of 8th house ---
    (8, 1): "8th lord in 1st: Health challenges, life marked by transformation. Interest in occult. Chronic ailments possible.",
    (8, 2): "8th lord in 2nd: Family wealth disrupted. Speech problems. Financial ups and downs. Inheritance disputes.",
    (8, 3): "8th lord in 3rd: Sibling faces sudden difficulties. Courage through transformation. Interest in occult writing.",
    (8, 4): "8th lord in 4th: Domestic upheaval, property disputes. Mother's health. Renovation of old property.",
    (8, 5): "8th lord in 5th: Children face difficulties. Speculation losses. Stomach ailments. Research-oriented mind.",
    (8, 6): "8th lord in 6th: Viparita Raja Yoga -- sudden transformation defeats enemies. Victory in crisis situations.",
    (8, 7): "8th lord in 7th: Marriage faces crises. Spouse's health. Business partnerships are unstable.",
    (8, 8): "8th lord in 8th: Long life, deep occult knowledge. Inheritance. Life of intense transformation.",
    (8, 9): "8th lord in 9th: Father faces sudden difficulties. Luck disrupted. Spiritual crisis leads to growth.",
    (8, 10): "8th lord in 10th: Career instability, sudden professional changes. Success in research, insurance, or occult.",
    (8, 11): "8th lord in 11th: Sudden gains and losses. Elder sibling faces crises. Inheritance from friends.",
    (8, 12): "8th lord in 12th: Viparita Raja Yoga -- crises resolve through spirituality. Foreign hospitalization. Liberation possible.",

    # --- Lord of 9th house ---
    (9, 1): "9th lord in 1st: Fortunate personality, blessed by destiny. Father's support shapes character. Religious nature.",
    (9, 2): "9th lord in 2nd: Wealth through luck and father. Family has religious values. Truthful and wealthy speech.",
    (9, 3): "9th lord in 3rd: Fortune through communication and initiative. Siblings are lucky. Pilgrimage through short travels.",
    (9, 4): "9th lord in 4th: Fortunate home life, property through luck. Mother is religious. Academic excellence.",
    (9, 5): "9th lord in 5th: Excellent Dharma-Karma combination. Highly intelligent, lucky children. Past-life merit manifests fully.",
    (9, 6): "9th lord in 6th: Luck through service and competition. Father faces health issues. Fortune requires effort.",
    (9, 7): "9th lord in 7th: Fortunate marriage, lucky spouse. Business prospers with divine grace. Foreign partner possible.",
    (9, 8): "9th lord in 8th: Father faces difficulties. Luck hidden or delayed. Fortune through inheritance or occult.",
    (9, 9): "9th lord in 9th: Extremely fortunate. Strong father, religious family. Guru's blessings. Higher education abroad.",
    (9, 10): "9th lord in 10th: Raj Yoga -- career blessed by fortune. High position through merit and luck combined.",
    (9, 11): "9th lord in 11th: Excellent gains through luck. All desires fulfilled. Wealthy, fortunate friends. Father prospers.",
    (9, 12): "9th lord in 12th: Fortune in foreign lands. Spiritual liberation. Father may live abroad. Expenses on pilgrimage.",

    # --- Lord of 10th house ---
    (10, 1): "10th lord in 1st: Career defines personality. Self-employed or self-directed professional. Public figure.",
    (10, 2): "10th lord in 2nd: Career brings wealth. Family business. Professional speech (teacher, lawyer, speaker).",
    (10, 3): "10th lord in 3rd: Career in communication, media, or writing. Professional courage. Siblings help in career.",
    (10, 4): "10th lord in 4th: Career from home, property business. Mother connected to profession. Works in education.",
    (10, 5): "10th lord in 5th: Career in education, entertainment, or advisory. Creative profession. Success through intellect.",
    (10, 6): "10th lord in 6th: Career in service, medicine, or law. Professional competition. Workplace health matters.",
    (10, 7): "10th lord in 7th: Career through partnerships. Spouse connected to profession. Business success.",
    (10, 8): "10th lord in 8th: Career instability. Profession in research, insurance, or occult fields. Hidden sources of income.",
    (10, 9): "10th lord in 9th: Raj Yoga -- fortunate career. Profession in law, religion, or higher education. Father helps career.",
    (10, 10): "10th lord in 10th: Excellent professional success. Strong career, public recognition. Powerful in chosen field.",
    (10, 11): "10th lord in 11th: Career brings massive gains. Professional network is strong. Income exceeds expectations.",
    (10, 12): "10th lord in 12th: Career abroad or in isolation (hospital, ashram, prison). Foreign professional success.",

    # --- Lord of 11th house ---
    (11, 1): "11th lord in 1st: Personal effort brings gains. Desires shape personality. Wealthy through own initiative.",
    (11, 2): "11th lord in 2nd: Excellent wealth combination. Income exceeds expenses. Family benefits from gains.",
    (11, 3): "11th lord in 3rd: Gains through communication, siblings, and short travels. Courageous pursuit of desires.",
    (11, 4): "11th lord in 4th: Gains through property, mother, and education. Comfortable domestic gains.",
    (11, 5): "11th lord in 5th: Gains through intellect and children. Investment income strong. Creative gains.",
    (11, 6): "11th lord in 6th: Gains through service and competition. Income from medical or legal work. Debts reduce gains.",
    (11, 7): "11th lord in 7th: Gains through marriage and partnerships. Spouse brings financial growth.",
    (11, 8): "11th lord in 8th: Sudden gains and losses. Inheritance. Income through insurance or occult work.",
    (11, 9): "11th lord in 9th: Fortunate gains, luck brings income. Father is wealthy. Foreign income sources.",
    (11, 10): "11th lord in 10th: Career brings excellent gains. Professional income is strong. Public recognition brings wealth.",
    (11, 11): "11th lord in 11th: Excellent -- all desires fulfilled. Massive gains. Wealthy and influential circle.",
    (11, 12): "11th lord in 12th: Gains spent quickly. Income through foreign sources. Expenses consume profit.",

    # --- Lord of 12th house ---
    (12, 1): "12th lord in 1st: Foreign travel or residence likely. Expenditure on self. Spiritual personality. Health expenses.",
    (12, 2): "12th lord in 2nd: Family wealth spent. Loss through speech or food. Expenses deplete savings.",
    (12, 3): "12th lord in 3rd: Expenses through siblings or travels. Loss of courage. Writing about foreign or spiritual topics.",
    (12, 4): "12th lord in 4th: Expenses on home and property. Mother's health expenses. Loss of domestic peace.",
    (12, 5): "12th lord in 5th: Expenses through children. Loss in speculation. Intelligence applied to spiritual matters.",
    (12, 6): "12th lord in 6th: Viparita Raja Yoga -- expenses defeat enemies. Losses turn to gains. Health improves after struggle.",
    (12, 7): "12th lord in 7th: Spouse connected to foreign lands. Marriage expenses. Business losses possible.",
    (12, 8): "12th lord in 8th: Hidden expenses, chronic health costs. Occult expenditure. Transformation through loss.",
    (12, 9): "12th lord in 9th: Expenses on pilgrimage and charity. Father lives abroad. Spiritual expenditure is beneficial.",
    (12, 10): "12th lord in 10th: Career abroad. Professional expenses. Loss of position if afflicted. Foreign career success.",
    (12, 11): "12th lord in 11th: Gains from foreign sources. Expenses reduced by income. Friends in foreign lands.",
    (12, 12): "12th lord in 12th: Spiritual liberation, charity. Foreign residence. Complete detachment possible. Bed pleasures.",
}


# ============================================================
# 5. GEMSTONE_DATA -- Gemstone Recommendations per Planet
# ============================================================

GEMSTONE_DATA: Dict[str, Dict[str, str]] = {
    "Sun": {
        "stone": "Ruby (Manik)",
        "upratna": "Garnet (Tamra)",
        "metal": "Gold",
        "finger": "Ring finger",
        "day": "Sunday morning during Shukla Paksha",
        "mantra": "Om Hraam Hreem Hraum Sah Suryaya Namah (7000 times)",
        "description": "Ruby strengthens self-confidence, authority and vitality. Recommended when Sun is yogakaraka or lagna lord.",
    },
    "Moon": {
        "stone": "Pearl (Moti)",
        "upratna": "Moonstone (Chandrakanta Mani)",
        "metal": "Silver",
        "finger": "Little finger",
        "day": "Monday evening during Shukla Paksha",
        "mantra": "Om Shraam Shreem Shraum Sah Chandraya Namah (11000 times)",
        "description": "Pearl stabilizes emotions, improves mental peace and memory. Essential when Moon is weak or afflicted in chart.",
    },
    "Mars": {
        "stone": "Red Coral (Moonga)",
        "upratna": "Carnelian (Masur Mani)",
        "metal": "Gold or Copper",
        "finger": "Ring finger",
        "day": "Tuesday morning during Shukla Paksha",
        "mantra": "Om Kraam Kreem Kraum Sah Bhaumaya Namah (7000 times)",
        "description": "Red Coral boosts courage, energy and physical strength. Helps overcome Mangala Dosha and blood-related issues.",
    },
    "Mercury": {
        "stone": "Emerald (Panna)",
        "upratna": "Peridot (Harit Mani)",
        "metal": "Gold",
        "finger": "Little finger",
        "day": "Wednesday morning during Shukla Paksha",
        "mantra": "Om Braam Breem Braum Sah Budhaya Namah (9000 times)",
        "description": "Emerald enhances intellect, communication and business acumen. Beneficial for students and professionals.",
    },
    "Jupiter": {
        "stone": "Yellow Sapphire (Pukhraj)",
        "upratna": "Citrine (Sunela)",
        "metal": "Gold",
        "finger": "Index finger",
        "day": "Thursday morning during Shukla Paksha",
        "mantra": "Om Graam Greem Graum Sah Gurave Namah (19000 times)",
        "description": "Yellow Sapphire brings wisdom, prosperity and marital bliss. Highly recommended for Jupiter mahadasha.",
    },
    "Venus": {
        "stone": "Diamond (Heera)",
        "upratna": "White Sapphire (Safed Pukhraj) / Zircon",
        "metal": "Platinum or Silver",
        "finger": "Middle finger",
        "day": "Friday morning during Shukla Paksha",
        "mantra": "Om Draam Dreem Draum Sah Shukraya Namah (16000 times)",
        "description": "Diamond enhances love, beauty, artistic talent and marital harmony. Strengthens Venus-related significations.",
    },
    "Saturn": {
        "stone": "Blue Sapphire (Neelam)",
        "upratna": "Amethyst (Katela) / Lapis Lazuli",
        "metal": "Silver or Iron (Panch-dhatu)",
        "finger": "Middle finger",
        "day": "Saturday evening during Shukla Paksha",
        "mantra": "Om Praam Preem Praum Sah Shanaischaraya Namah (23000 times)",
        "description": "Blue Sapphire brings discipline, career success and removes delays. Must be tested for 3 days before permanent wear.",
    },
    "Rahu": {
        "stone": "Hessonite Garnet (Gomed)",
        "upratna": "Orange Zircon",
        "metal": "Silver or Panch-dhatu",
        "finger": "Middle finger",
        "day": "Saturday evening during Krishna Paksha",
        "mantra": "Om Bhraam Bhreem Bhraum Sah Rahave Namah (18000 times)",
        "description": "Hessonite neutralizes Rahu's malefic effects and protects from sudden setbacks, confusion and foreign troubles.",
    },
    "Ketu": {
        "stone": "Cat's Eye (Lehsunia / Vaidurya)",
        "upratna": "Tiger's Eye",
        "metal": "Silver or Panch-dhatu",
        "finger": "Little finger",
        "day": "Tuesday or Saturday during Krishna Paksha",
        "mantra": "Om Sraam Sreem Sraum Sah Ketave Namah (17000 times)",
        "description": "Cat's Eye protects from hidden enemies, accidents and spiritual disturbances. Enhances intuition and detachment.",
    },
}


# ============================================================
# 6. DASHA_INTERPRETATIONS -- Mahadasha General Effects
# ============================================================

DASHA_INTERPRETATIONS: Dict[str, Dict[str, Any]] = {
    "Sun": {
        "general": [
            "Rise in authority, government favour and recognition",
            "Improved health and vitality, recovery from chronic ailments",
            "Relations with father become significant (good or strained based on dignity)",
            "Career advancement, especially in leadership and administrative roles",
            "Increased self-confidence and assertiveness",
            "Possible conflicts with authority if Sun is afflicted",
            "Heart and eye health require attention",
        ],
        "specific_good": [
            "Promotion and recognition in government or corporate sectors",
            "Pilgrimage and religious activities bring peace",
            "Children prosper and bring pride",
            "Political connections strengthen social standing",
        ],
        "specific_bad": [
            "Ego conflicts with superiors and father",
            "Eye problems, heart ailments, bone weakness",
            "Government penalties or tax issues if Sun is afflicted",
            "Separation from family or loss of position in extreme cases",
        ],
    },
    "Moon": {
        "general": [
            "Emotional sensitivity heightened, mood fluctuations increase",
            "Mother's influence and well-being become central themes",
            "Travel, especially overseas or to water bodies",
            "Mental peace depends on Moon's dignity -- calm if strong, anxious if weak",
            "Gains through public, women, and liquid-related businesses",
            "Interest in agriculture, hospitality, nursing, or caregiving",
            "Dreams become vivid and psychic sensitivity increases",
        ],
        "specific_good": [
            "Happy domestic life, property and vehicle acquisition",
            "Mother's blessings and support",
            "Popularity with masses, public-facing success",
            "Marriage and romantic fulfilment if of marriageable age",
        ],
        "specific_bad": [
            "Anxiety, depression, insomnia if Moon is weak or afflicted",
            "Cold, cough, water-borne diseases",
            "Mother's health may decline",
            "Emotional instability leading to poor decisions",
        ],
    },
    "Mars": {
        "general": [
            "Energy and courage increase dramatically",
            "Property and land transactions become prominent",
            "Brothers and siblings come into focus (support or conflict)",
            "Career in technical, military, police, surgery, or engineering thrives",
            "Physical activity increases; sports and exercise benefit",
            "Risk of accidents, surgery, and injuries rises",
            "Legal disputes and conflicts with authority possible",
        ],
        "specific_good": [
            "Property purchase, construction, or land deals succeed",
            "Victory over enemies and competitors",
            "Technical and engineering projects produce results",
            "Blood disorders resolve, physical fitness improves",
        ],
        "specific_bad": [
            "Accidents, burns, cuts, or surgery",
            "Marital conflicts and aggression at home",
            "Blood pressure, fevers, and inflammatory conditions",
            "Legal battles, property disputes, or police trouble",
        ],
    },
    "Mercury": {
        "general": [
            "Intellectual pursuits, education and communication highlighted",
            "Business and trade opportunities expand",
            "Writing, media, IT and analytical careers flourish",
            "Nervous system and skin health need attention",
            "Short travels, networking and social interactions increase",
            "Maternal uncle and friends become important",
            "Financial acumen sharpens -- good for investments",
        ],
        "specific_good": [
            "Academic success, degrees, and certifications",
            "New business ventures and trade partnerships",
            "Writing, publishing, or media recognition",
            "Children excel in education",
        ],
        "specific_bad": [
            "Nervous disorders, skin allergies, speech problems",
            "Overthinking leads to anxiety and insomnia",
            "Business fraud or deception from partners",
            "Cousin or friend betrayals",
        ],
    },
    "Jupiter": {
        "general": [
            "Wisdom, spirituality and fortune increase markedly",
            "Marriage, children, and family expansion",
            "Guru or teacher enters life with significant guidance",
            "Wealth accumulation through ethical means",
            "Higher education, law, religion, or philosophy become central",
            "Liver and weight gain need monitoring",
            "Charitable disposition and religious activities increase",
        ],
        "specific_good": [
            "Marriage, birth of children, and family celebrations",
            "Professional promotion and financial prosperity",
            "Spiritual initiation or deepening of religious practice",
            "Foreign travel for education or pilgrimage",
        ],
        "specific_bad": [
            "Over-optimism leads to poor financial decisions",
            "Liver disorders, diabetes, obesity, or cholesterol issues",
            "Conflicts with religious figures or teachers",
            "Legal issues related to education or religious institutions",
        ],
    },
    "Venus": {
        "general": [
            "Love, marriage, and romantic relationships are central themes",
            "Material comforts, luxury, and aesthetic pleasures increase",
            "Artistic and creative talents flourish",
            "Vehicles, jewellery, and fine clothing acquired",
            "Women play significant roles in life events",
            "Reproductive health requires attention",
            "Social life becomes vibrant and enjoyable",
        ],
        "specific_good": [
            "Happy marriage, romantic fulfilment, and partnership harmony",
            "Wealth through arts, fashion, beauty, or luxury goods",
            "Acquisition of vehicles, property, and ornaments",
            "Travel to beautiful destinations",
        ],
        "specific_bad": [
            "Overindulgence in sensual pleasures",
            "Reproductive and urinary health issues",
            "Marital discord if Venus is afflicted or in dusthana",
            "Financial loss through luxury spending or women-related matters",
        ],
    },
    "Saturn": {
        "general": [
            "Hard work, discipline and perseverance define this period",
            "Karma manifests -- rewards for past effort or consequences of neglect",
            "Career in service, manufacturing, mining, agriculture, or law",
            "Chronic health issues surface; joints, bones, and teeth affected",
            "Delays and obstacles test patience and endurance",
            "Separation from family or loved ones possible",
            "Spiritual maturity through suffering and discipline",
            "Democratic or servant-leadership roles emerge",
        ],
        "specific_good": [
            "Lasting career achievements after initial struggle",
            "Property from sustained effort or inheritance",
            "Spiritual depth and philosophical maturity",
            "Service to society brings recognition",
        ],
        "specific_bad": [
            "Chronic ailments: arthritis, knee pain, dental problems",
            "Depression, loneliness, and pessimism",
            "Financial losses through litigation or government penalties",
            "Separation from family, exile, or demotion",
        ],
    },
    "Rahu": {
        "general": [
            "Unconventional path, breaking from tradition",
            "Foreign connections, travel, or residence abroad",
            "Technology, media, and modern industries offer success",
            "Confusion, deception, and illusion test discernment",
            "Obsessive desires and worldly ambitions intensify",
            "Health: mysterious ailments, poisoning risk, mental fog",
            "Sudden rise or fall in status possible",
        ],
        "specific_good": [
            "Breakthrough in technology, media, or foreign business",
            "Political power or public influence through unconventional means",
            "Foreign travel and settlement",
            "Gains through speculation or stock market",
        ],
        "specific_bad": [
            "Deception, fraud, or scandal involving others or self",
            "Mysterious diseases, food poisoning, snake bite",
            "Family estrangement, marital breakdown",
            "Sudden loss of reputation or wealth",
        ],
    },
    "Ketu": {
        "general": [
            "Spiritual awakening and detachment from material world",
            "Past-life karmas manifest -- sudden events without clear cause",
            "Interest in meditation, yoga, moksha, and occult sciences",
            "Health: digestive issues, mysterious fevers, wounds",
            "Loss of worldly comforts pushes toward inner growth",
            "Isolation, introspection, and withdrawal from society",
            "Technical and research skills sharpen",
        ],
        "specific_good": [
            "Spiritual enlightenment and liberation experiences",
            "Success in research, technology, and occult sciences",
            "Past-life skills (healing, languages, arts) reawaken",
            "Detachment resolves long-standing material problems",
        ],
        "specific_bad": [
            "Mysterious chronic ailments, surgery, or accidents",
            "Loss of position, wealth, or family support",
            "Mental confusion, hallucinations if afflicted",
            "Scandal or disgrace from past actions surfacing",
        ],
    },
}


# ============================================================
# 7. ANTARDASHA_INTERPRETATIONS -- 81 MD-AD Combinations
# ============================================================

ANTARDASHA_INTERPRETATIONS: Dict[Tuple[str, str], str] = {
    # --- Sun Mahadasha ---
    ("Sun", "Sun"): "Peak of self-expression and authority. Government favour. Father's role is significant. Health generally good if Sun is strong.",
    ("Sun", "Moon"): "Emotional sensitivity rises. Mother and public relations become important. Travel for work. Mood fluctuations affect authority.",
    ("Sun", "Mars"): "Courage and energy combine with authority. Property gains, technical projects succeed. Risk of conflicts with authority and blood-related health issues.",
    ("Sun", "Mercury"): "Intellectual pursuits shine. Business acumen combines with authority. Good for examinations, writing, and trade. Skin or nervous issues possible.",
    ("Sun", "Jupiter"): "Highly auspicious -- wisdom, wealth and recognition. Guru's blessings. Promotion, children prosper. Spiritual and material growth together.",
    ("Sun", "Venus"): "Luxury, comfort and romantic fulfilment. Creative expression enhanced. Vehicles and ornaments acquired. Reproductive health needs attention.",
    ("Sun", "Saturn"): "Hard work meets authority. Delays in recognition. Father's health may suffer. Bone, joint, or eye ailments possible. Karmic lessons.",
    ("Sun", "Rahu"): "Unconventional rise in authority. Foreign connections benefit career. Risk of ego-driven mistakes and sudden reputation damage.",
    ("Sun", "Ketu"): "Spiritual introspection during authoritative period. Detachment from ego. Father faces challenges. Mysterious health issues possible.",

    # --- Moon Mahadasha ---
    ("Moon", "Moon"): "Peak emotional period. Mother's role is central. Mental peace if Moon is strong; anxiety if weak. Property and public gains.",
    ("Moon", "Mars"): "Emotional energy channelled into action. Property deals and courage. Emotional conflicts at home. Blood pressure and stomach issues.",
    ("Moon", "Mercury"): "Intellectual clarity improves. Good for business, communication and education. Mother-related travel. Mental agility is sharp.",
    ("Moon", "Jupiter"): "Very auspicious -- emotional wisdom, family expansion. Marriage or childbirth likely. Mother is well. Spiritual contentment.",
    ("Moon", "Venus"): "Romantic fulfilment, luxury and aesthetic pleasures. Emotional bond with partner deepens. Women play beneficial roles.",
    ("Moon", "Saturn"): "Emotional heaviness, depression tendency. Mother's health may suffer. Delays in domestic matters. Hard work needed for peace.",
    ("Moon", "Rahu"): "Mental confusion and emotional turbulence. Foreign travel. Mother faces unusual challenges. Nightmares and anxiety increase.",
    ("Moon", "Ketu"): "Emotional detachment, spiritual seeking. Mother faces health issues. Psychic experiences intensify. Stomach and chest ailments.",
    ("Moon", "Sun"): "Authority and emotions intersect. Public recognition. Father and mother both influential. Health and vitality improve.",

    # --- Mars Mahadasha ---
    ("Mars", "Mars"): "Peak energy and courage. Property transactions. Risk of accidents, cuts, burns. Victory over enemies. Physical fitness improves.",
    ("Mars", "Mercury"): "Technical intellect shines. Property deals through negotiation. Business partnerships in engineering or technology.",
    ("Mars", "Jupiter"): "Auspicious -- dharmic courage. Property through fortune. Brothers prosper. Children and education benefit. Legal victory.",
    ("Mars", "Venus"): "Passion and luxury combine. Romantic relationships intensify. Property acquisition. Reproductive health needs attention.",
    ("Mars", "Saturn"): "Conflict between energy and restriction. Accidents or surgery risk. Property disputes. Joint and bone injuries possible.",
    ("Mars", "Rahu"): "Reckless courage and unconventional action. Foreign property dealings. Risk of explosions, accidents, or deception.",
    ("Mars", "Ketu"): "Spiritual warrior energy. Past-life martial skills resurface. Surgery or accident risk. Detachment from material aggression.",
    ("Mars", "Sun"): "Authority and courage combine. Government property. Father and brothers interact. Leadership in competitive fields.",
    ("Mars", "Moon"): "Emotional courage. Mother and property connected. Domestic energy high. Stomach and blood pressure issues possible.",

    # --- Mercury Mahadasha ---
    ("Mercury", "Mercury"): "Peak intellectual period. Business flourishes. Communication and networking at their best. Skin and nervous health need care.",
    ("Mercury", "Jupiter"): "Wisdom and intellect combine beautifully. Education, publishing, legal success. Financial growth through ethical business.",
    ("Mercury", "Venus"): "Creative communication and artistic business. Fashion, media, and design succeed. Romantic correspondence. Social life vibrant.",
    ("Mercury", "Saturn"): "Disciplined intellect. Serious study and long-term business planning. Nervous exhaustion possible. Dental issues.",
    ("Mercury", "Rahu"): "Unconventional business opportunities. Technology and foreign trade. Risk of fraud or deception. Mental confusion if afflicted.",
    ("Mercury", "Ketu"): "Spiritual intellect, interest in astrology and occult study. Communication breakdowns. Skin ailments and nervous disorders.",
    ("Mercury", "Sun"): "Authority through intellect. Government business. Father supports education. Speech commands respect.",
    ("Mercury", "Moon"): "Emotional intelligence sharpens. Public communication roles. Mother supports business. Travel for trade.",
    ("Mercury", "Mars"): "Technical communication and engineering intellect. Property negotiations. Sibling business partnerships. Arguments possible.",

    # --- Jupiter Mahadasha ---
    ("Jupiter", "Jupiter"): "Peak of wisdom, fortune and expansion. Marriage, children, wealth all prosper. Guru's grace is strongest. Spiritual growth.",
    ("Jupiter", "Venus"): "Wealth and luxury through wisdom. Happy marriage. Artistic and creative prosperity. Vehicles and ornaments. Social prestige.",
    ("Jupiter", "Saturn"): "Disciplined wisdom. Long-term investments mature. Health caution needed -- liver and joints. Spiritual lessons through hardship.",
    ("Jupiter", "Rahu"): "Unconventional expansion. Foreign guru or education. Risk of misplaced faith. Technology and modern ventures through wisdom.",
    ("Jupiter", "Ketu"): "Deep spiritual awakening. Detachment from material wealth. Meditation and moksha practices. Health fluctuations.",
    ("Jupiter", "Sun"): "Authority blessed by wisdom. Government recognition and honour. Father prospers. Career promotion through merit.",
    ("Jupiter", "Moon"): "Emotional wisdom and family happiness. Mother is well. Property and domestic expansion. Public favour.",
    ("Jupiter", "Mars"): "Courageous wisdom. Property through fortune. Brothers benefit. Legal and dharmic victories. Technical education.",
    ("Jupiter", "Mercury"): "Intellectual fortune. Business and education prosper simultaneously. Publishing success. Children excel academically.",

    # --- Venus Mahadasha ---
    ("Venus", "Venus"): "Peak of luxury, romance, and artistic expression. Marriage or renewal of vows. Vehicles, property, and wealth. Social prominence.",
    ("Venus", "Saturn"): "Disciplined luxury. Long-term artistic projects. Reproductive and urinary health issues. Delayed romantic fulfilment.",
    ("Venus", "Rahu"): "Unconventional romance and foreign luxury. Technology in arts. Risk of scandalous affairs. Skin and allergy issues.",
    ("Venus", "Ketu"): "Spiritual detachment from pleasures. Past-life artistic talents resurface. Romantic disappointments lead to growth.",
    ("Venus", "Sun"): "Authority in creative fields. Government arts funding. Glamorous public role. Father and spouse dynamics.",
    ("Venus", "Moon"): "Emotional romance and domestic beauty. Mother and spouse connected. Home decoration. Water travel.",
    ("Venus", "Mars"): "Passionate romance, bold artistic expression. Property acquisition. Reproductive health needs care. Energy in creative projects.",
    ("Venus", "Mercury"): "Creative business and artistic communication. Fashion, media, and design prosper. Social networking expands.",
    ("Venus", "Jupiter"): "Wisdom and luxury combined. Happy marriage and family expansion. Wealth through ethical creative enterprise.",

    # --- Saturn Mahadasha ---
    ("Saturn", "Saturn"): "Peak of karma manifestation. Hard work defines life. Chronic health issues surface. Lasting achievements through discipline.",
    ("Saturn", "Rahu"): "Unconventional hardship. Foreign obstacles. Technology and modern challenges. Risk of deception during difficult times.",
    ("Saturn", "Ketu"): "Spiritual suffering and deep karmic clearing. Health crises lead to detachment. Past-life karmas resolve painfully.",
    ("Saturn", "Sun"): "Authority restricted by karma. Government obstacles. Father's health declines. Eye and bone issues. Frustration with hierarchy.",
    ("Saturn", "Moon"): "Emotional heaviness and depression. Mother's suffering. Domestic hardship. Mental health needs serious attention.",
    ("Saturn", "Mars"): "Accidents, surgery, and conflicts during difficult period. Property disputes. Joint and bone injuries. Legal battles.",
    ("Saturn", "Mercury"): "Intellectual discipline and serious study. Business requires patience. Nervous exhaustion. Delayed results.",
    ("Saturn", "Jupiter"): "Wisdom through suffering. Spiritual maturity. Financial stability slowly returns. Guru helps through hardship.",
    ("Saturn", "Venus"): "Artistic discipline bears fruit. Late romantic fulfilment. Chronic reproductive issues. Vehicles and luxury delayed.",

    # --- Rahu Mahadasha ---
    ("Rahu", "Rahu"): "Peak of worldly obsession and unconventional path. Foreign connections strongest. Maximum confusion and ambition. Sudden changes.",
    ("Rahu", "Ketu"): "Spiritual crisis within material obsession. Axis of karma activates. Sudden events without logic. Health disturbances.",
    ("Rahu", "Sun"): "Unconventional authority. Foreign government roles. Father faces unusual challenges. Ego-driven ambition peaks.",
    ("Rahu", "Moon"): "Mental turbulence and emotional confusion. Mother faces foreign challenges. Nightmares and psychic disturbances.",
    ("Rahu", "Mars"): "Reckless action and unconventional courage. Accidents, explosions, surgery risk. Foreign property. Violent disputes.",
    ("Rahu", "Mercury"): "Technology and foreign business flourish. Risk of intellectual fraud. Media and communication breakthroughs.",
    ("Rahu", "Jupiter"): "Unconventional wisdom. Foreign education or guru. Expansion through modern means. Risk of misplaced faith.",
    ("Rahu", "Venus"): "Foreign romance and unconventional luxury. Technology in arts. Scandalous relationships if afflicted. Material obsession.",
    ("Rahu", "Saturn"): "Double malefic period. Extreme hardship and karmic lessons. Foreign exile. Chronic ailments worsen. Perseverance essential.",

    # --- Ketu Mahadasha ---
    ("Ketu", "Ketu"): "Peak of spiritual detachment. Past-life karmas culminate. Mysterious events and health issues. Moksha-oriented period.",
    ("Ketu", "Sun"): "Detachment from authority and ego. Father faces spiritual crisis. Loss of position leads to inner growth.",
    ("Ketu", "Moon"): "Emotional detachment and psychic sensitivity. Mother's health. Mental disturbances. Vivid dreams and visions.",
    ("Ketu", "Mars"): "Spiritual warrior mode. Surgery or accident risk. Past-life martial energy surfaces. Detachment from aggression.",
    ("Ketu", "Mercury"): "Interest in occult study, astrology, and ancient languages. Communication breakdowns. Nervous and skin issues.",
    ("Ketu", "Jupiter"): "Deep spiritual wisdom manifests. Guru appears. Detachment brings unexpected fortune. Meditation bears fruit.",
    ("Ketu", "Venus"): "Detachment from romantic and material pleasures. Artistic spirituality. Past-life creative talents resurface.",
    ("Ketu", "Saturn"): "Extreme karmic clearing. Health crises and isolation. Spiritual suffering has deep purpose. Joint and skin ailments.",
    ("Ketu", "Rahu"): "Karmic axis fully activated. Confusion between spirit and matter. Sudden reversals. Health disturbances. Transformation.",
}


# ============================================================
# 8. MANGALA_DOSHA_TEXT -- Classical References + Remedies
# ============================================================

MANGALA_DOSHA_TEXT: Dict[str, Any] = {
    "classical_shlokas": [
        {
            "source": "Agastya Samhita",
            "text": (
                "If Mars is placed in the 1st, 4th, 7th, 8th, or 12th house from the Lagna, Moon, or Venus, "
                "the native is said to have Mangala Dosha (Kuja Dosha). Such placement causes disturbance "
                "in marital life and discord with the spouse."
            ),
        },
        {
            "source": "Maanasagari",
            "text": (
                "Mars in the 1st house destroys the spouse. In the 4th, it causes loss of domestic happiness. "
                "In the 7th, there is constant strife. In the 8th, the spouse faces chronic illness. "
                "In the 12th, there is loss of marital bliss."
            ),
        },
        {
            "source": "Brihat Jyotishasara",
            "text": (
                "When Mars occupies the said houses from Lagna, Moon or Venus, the native faces "
                "widowhood or widowerhood, separation, or chronic marital suffering. "
                "Matching charts of both partners is essential."
            ),
        },
        {
            "source": "Bhava Deepika",
            "text": (
                "Kuja Dosha is neutralized when both partners have Mars in the specified houses. "
                "Also cancelled if Mars is in its own sign (Aries, Scorpio), exalted (Capricorn), "
                "or aspected by benefics (Jupiter, Venus)."
            ),
        },
        {
            "source": "Brihat Parashara Hora Shastra",
            "text": (
                "The wise should examine Mars from Lagna, Moon, and Venus. "
                "If Kuja Dosha exists from all three, it is of the highest severity. "
                "From two, it is medium. From one alone, it is mild."
            ),
        },
    ],
    "results": (
        "Mangala Dosha indicates challenges in marital life including: "
        "delay in marriage, discord between spouses, separation or divorce, "
        "health issues of the partner, and in severe cases, bereavement. "
        "The severity depends on the house Mars occupies and whether the dosha "
        "is from Lagna, Moon, Venus, or multiple reference points. "
        "Cancellation conditions include: Mars in own sign/exalted, "
        "both partners having equal dosha, Jupiter's aspect on Mars, "
        "and Mars placed in Aries/Scorpio/Capricorn in the respective houses."
    ),
    "remedies": {
        "mantras": [
            "Chant Hanuman Chalisa daily, especially on Tuesdays",
            "Recite 'Om Kraam Kreem Kraum Sah Bhaumaya Namah' 108 times daily",
            "Navagraha Shanti Puja with special focus on Mars",
        ],
        "fasting": [
            "Fast on Tuesdays (Mangalvar Vrat) for 21 consecutive Tuesdays",
            "Consume only single-grain meal on fasting day",
        ],
        "worship": [
            "Worship Lord Hanuman with sindoor and red flowers on Tuesdays",
            "Perform Kumbh Vivah (symbolic marriage to pot/tree) before actual marriage",
            "Visit Mangalnath temple in Ujjain for Mars pacification",
            "Donate red lentils (masoor dal), red cloth, and jaggery on Tuesdays",
        ],
        "gemstone": (
            "Wear Red Coral (Moonga) in gold/copper on the ring finger "
            "after proper energization with Mars mantra on a Tuesday during Shukla Paksha."
        ),
    },
}


# ============================================================
# 9. GRAHA_AVASTHAS -- Planetary States & Calculation Rules
# ============================================================

# --- 9A. Static reference data ---

# Sign lordship for computing avasthas
_SIGN_LORDS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

_EXALTED = {
    "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
    "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces",
    "Saturn": "Libra", "Rahu": "Gemini", "Ketu": "Sagittarius",
}

_DEBILITATED = {
    "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
    "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo",
    "Saturn": "Aries", "Rahu": "Sagittarius", "Ketu": "Gemini",
}

_OWN_SIGNS = {
    "Sun": ["Leo"], "Moon": ["Cancer"],
    "Mars": ["Aries", "Scorpio"], "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"], "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"], "Rahu": ["Aquarius"], "Ketu": ["Scorpio"],
}

_FRIEND_SIGNS = {
    "Sun": ["Aries", "Scorpio", "Sagittarius", "Pisces", "Cancer"],
    "Moon": ["Taurus", "Gemini", "Virgo", "Sagittarius", "Pisces"],
    "Mars": ["Leo", "Sagittarius", "Pisces", "Cancer"],
    "Mercury": ["Taurus", "Leo", "Libra", "Capricorn", "Aquarius"],
    "Jupiter": ["Aries", "Leo", "Scorpio", "Cancer"],
    "Venus": ["Gemini", "Virgo", "Capricorn", "Aquarius", "Pisces"],
    "Saturn": ["Taurus", "Gemini", "Virgo", "Libra"],
    "Rahu": ["Gemini", "Virgo", "Sagittarius", "Pisces"],
    "Ketu": ["Aries", "Sagittarius", "Pisces"],
}

_ENEMY_SIGNS = {
    "Sun": ["Taurus", "Libra", "Capricorn", "Aquarius"],
    "Moon": ["Capricorn", "Aquarius"],
    "Mars": ["Gemini", "Virgo"],
    "Mercury": ["Cancer", "Scorpio"],
    "Jupiter": ["Taurus", "Libra", "Gemini", "Virgo"],
    "Venus": ["Cancer", "Leo"],
    "Saturn": ["Aries", "Leo", "Cancer", "Scorpio"],
    "Rahu": ["Leo", "Cancer"],
    "Ketu": ["Gemini", "Virgo"],
}

# Odd/Even sign classification
_ODD_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}
_EVEN_SIGNS = {"Taurus", "Cancer", "Virgo", "Scorpio", "Capricorn", "Pisces"}

SIGNS_LIST = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# --- 9B. Avastha descriptions ---

JAGRADADI_AVASTHAS = {
    "Jagrad": "Awakened state -- planet in own or exalted sign. Gives full results. Active and powerful.",
    "Swapna": "Dreaming state -- planet in friend's sign. Gives moderate results. Partially effective.",
    "Sushupti": "Sleeping state -- planet in enemy or neutral sign. Gives minimal results. Dormant potential.",
}

BALADI_AVASTHAS = {
    "Bala": "Infant state (0-6 deg in odd sign, 24-30 deg in even sign). Planet gives ~20% results. New energy, incomplete expression.",
    "Kumara": "Adolescent state (6-12 deg odd, 18-24 deg even). Planet gives ~40% results. Growing strength, developing potential.",
    "Yuva": "Youthful state (12-18 deg odd, 12-18 deg even). Planet gives full 100% results. Peak power and expression.",
    "Vriddha": "Old state (18-24 deg odd, 6-12 deg even). Planet gives ~40% results. Declining but experienced energy.",
    "Mrita": "Dead state (24-30 deg odd, 0-6 deg even). Planet gives minimal ~5% results. Exhausted, unable to deliver.",
}

DEEPTADI_AVASTHAS = {
    "Deepta": "Blazing -- exalted planet. Full benefic results. Radiates power and success.",
    "Swastha": "Comfortable -- planet in own sign. Strong positive results. Self-assured expression.",
    "Mudita": "Delighted -- planet in friend's sign. Good results with ease. Supportive environment.",
    "Shanta": "Peaceful -- planet in benefic vargas. Calm, steady positive results.",
    "Shakta": "Powerful -- retrograde planet (except Sun/Moon). Intensified results, inner strength.",
    "Peedita": "Tormented -- planet in malefic conjunction. Results mixed with suffering.",
    "Deena": "Miserable -- planet in enemy sign. Poor results. Uncomfortable placement.",
    "Vikala": "Defective -- combust planet. Results hidden or damaged. Burnt by Sun's proximity.",
    "Khala": "Wicked -- debilitated planet. Worst results. Planet works against its nature.",
}

SHYANADI_AVASTHAS = {
    "Shyana": "Lying down -- planet aspected by Saturn. Lazy results, delayed outcomes.",
    "Upavesha": "Sitting -- planet in enemy sign without benefic aspect. Stagnant, unproductive.",
    "Netrapani": "Eyes and hands -- planet aspected by friends. Protected, supported results.",
    "Prakasha": "Illuminated -- planet aspected by Jupiter. Wisdom-enhanced results.",
    "Gamana": "Moving -- planet in 2 or more benefic vargas. Progressive, improving results.",
    "Agama": "Returning -- retrograde planet in own/exalted sign. Powerful revisiting energy.",
    "Sabha": "Assembly -- planet conjunct benefics. Enhanced social and public results.",
    "Agam": "Approaching -- planet in friend's sign with benefic aspect. Growing strength.",
    "Bhojana": "Eating -- planet in 5th or 9th house. Nourished and productive.",
    "Nrityalipsa": "Dancing -- planet conjunct Moon in good dignity. Joyful expression.",
    "Kautuka": "Curious -- planet in 3rd or 11th house. Active pursuit of desires.",
    "Nidraa": "Deep sleep -- planet combust and in enemy sign. Completely dormant.",
}


# --- 9C. Calculation functions ---

def calculate_jagradadi(planet: str, sign: str) -> str:
    """
    Jagradadi Avastha (3 states):
    - Jagrad (Awake): planet in own sign or exalted sign
    - Swapna (Dreaming): planet in friend's sign
    - Sushupti (Sleeping): planet in enemy or neutral sign
    """
    if sign == _EXALTED.get(planet) or sign in _OWN_SIGNS.get(planet, []):
        return "Jagrad"
    if sign in _FRIEND_SIGNS.get(planet, []):
        return "Swapna"
    return "Sushupti"


def calculate_baladi(planet: str, sign: str, degree_in_sign: float) -> str:
    """
    Baladi Avastha (5 states based on degree within sign):
    Odd signs: Bala(0-6), Kumara(6-12), Yuva(12-18), Vriddha(18-24), Mrita(24-30)
    Even signs: Mrita(0-6), Vriddha(6-12), Yuva(12-18), Kumara(18-24), Bala(24-30)
    """
    deg = degree_in_sign % 30.0
    if sign in _ODD_SIGNS:
        if deg < 6:
            return "Bala"
        elif deg < 12:
            return "Kumara"
        elif deg < 18:
            return "Yuva"
        elif deg < 24:
            return "Vriddha"
        else:
            return "Mrita"
    else:  # even sign
        if deg < 6:
            return "Mrita"
        elif deg < 12:
            return "Vriddha"
        elif deg < 18:
            return "Yuva"
        elif deg < 24:
            return "Kumara"
        else:
            return "Bala"


def calculate_deeptadi(
    planet: str,
    sign: str,
    is_retrograde: bool = False,
    is_combust: bool = False,
    conjunct_malefics: bool = False,
    in_benefic_vargas: bool = False,
) -> str:
    """
    Deeptadi Avastha (9 states based on dignity and condition):
    Priority order: Khala > Vikala > Deepta > Swastha > Shakta > Peedita >
                    Mudita > Shanta > Deena

    Args:
        planet: planet name
        sign: sign the planet occupies
        is_retrograde: True if planet is retrograde
        is_combust: True if planet is combust (too close to Sun)
        conjunct_malefics: True if conjunct Saturn, Mars, Rahu, or Ketu
        in_benefic_vargas: True if planet is in benefic divisional charts
    """
    # Debilitated = Khala (worst)
    if sign == _DEBILITATED.get(planet):
        return "Khala"
    # Combust = Vikala
    if is_combust:
        return "Vikala"
    # Exalted = Deepta (best)
    if sign == _EXALTED.get(planet):
        return "Deepta"
    # Own sign = Swastha
    if sign in _OWN_SIGNS.get(planet, []):
        return "Swastha"
    # Retrograde (not Sun/Moon) = Shakta
    if is_retrograde and planet not in ("Sun", "Moon"):
        return "Shakta"
    # Conjunct malefics = Peedita
    if conjunct_malefics:
        return "Peedita"
    # Friend sign = Mudita
    if sign in _FRIEND_SIGNS.get(planet, []):
        return "Mudita"
    # In benefic vargas = Shanta
    if in_benefic_vargas:
        return "Shanta"
    # Enemy sign = Deena
    if sign in _ENEMY_SIGNS.get(planet, []):
        return "Deena"
    # Default neutral = Shanta (mildly positive)
    return "Shanta"


def calculate_shyanadi(
    planet: str,
    sign: str,
    house: int,
    is_retrograde: bool = False,
    is_combust: bool = False,
    aspected_by_saturn: bool = False,
    aspected_by_jupiter: bool = False,
    aspected_by_friends: bool = False,
    aspected_by_benefics: bool = False,
    conjunct_benefics: bool = False,
    conjunct_moon_good: bool = False,
    num_benefic_vargas: int = 0,
) -> str:
    """
    Shyanadi Avastha (12 states based on complex conditions):
    Returns the most applicable state based on the planet's condition.

    Args:
        planet: planet name
        sign: sign the planet occupies
        house: house number (1-12) the planet is in
        is_retrograde: True if retrograde
        is_combust: True if combust
        aspected_by_saturn: True if Saturn aspects this planet
        aspected_by_jupiter: True if Jupiter aspects this planet
        aspected_by_friends: True if aspected by planetary friends
        aspected_by_benefics: True if aspected by natural benefics
        conjunct_benefics: True if conjunct natural benefics
        conjunct_moon_good: True if conjunct well-dignified Moon
        num_benefic_vargas: number of benefic divisional chart placements
    """
    # Combust + enemy sign = Nidraa (deep sleep -- worst)
    if is_combust and sign in _ENEMY_SIGNS.get(planet, []):
        return "Nidraa"

    # Aspected by Saturn = Shyana (lying down)
    if aspected_by_saturn:
        return "Shyana"

    # Enemy sign without benefic aspect = Upavesha (sitting, stagnant)
    if sign in _ENEMY_SIGNS.get(planet, []) and not aspected_by_benefics:
        return "Upavesha"

    # Retrograde in own/exalted = Agama (returning with power)
    if is_retrograde and (sign == _EXALTED.get(planet) or sign in _OWN_SIGNS.get(planet, [])):
        return "Agama"

    # Aspected by Jupiter = Prakasha (illuminated)
    if aspected_by_jupiter:
        return "Prakasha"

    # Conjunct benefics = Sabha (assembly)
    if conjunct_benefics:
        return "Sabha"

    # Conjunct well-dignified Moon = Nrityalipsa (dancing)
    if conjunct_moon_good:
        return "Nrityalipsa"

    # In 5th or 9th house = Bhojana (nourished)
    if house in (5, 9):
        return "Bhojana"

    # In 3rd or 11th house = Kautuka (curious)
    if house in (3, 11):
        return "Kautuka"

    # Aspected by friends = Netrapani (protected)
    if aspected_by_friends:
        return "Netrapani"

    # In 2+ benefic vargas = Gamana (moving/progressive)
    if num_benefic_vargas >= 2:
        return "Gamana"

    # Friend sign with benefic aspect = Agam (approaching)
    if sign in _FRIEND_SIGNS.get(planet, []) and aspected_by_benefics:
        return "Agam"

    # Default
    return "Gamana"


def get_all_avasthas(
    planet: str,
    sign: str,
    degree_in_sign: float,
    house: int,
    is_retrograde: bool = False,
    is_combust: bool = False,
    conjunct_malefics: bool = False,
    conjunct_benefics: bool = False,
    in_benefic_vargas: bool = False,
    aspected_by_saturn: bool = False,
    aspected_by_jupiter: bool = False,
    aspected_by_friends: bool = False,
    aspected_by_benefics: bool = False,
    conjunct_moon_good: bool = False,
    num_benefic_vargas: int = 0,
) -> Dict[str, str]:
    """
    Compute all four avastha systems for a planet and return a dict.

    Returns:
        {
            "jagradadi": "Jagrad" | "Swapna" | "Sushupti",
            "baladi": "Bala" | "Kumara" | "Yuva" | "Vriddha" | "Mrita",
            "deeptadi": one of 9 states,
            "shyanadi": one of 12 states,
        }
    """
    return {
        "jagradadi": calculate_jagradadi(planet, sign),
        "baladi": calculate_baladi(planet, sign, degree_in_sign),
        "deeptadi": calculate_deeptadi(
            planet, sign, is_retrograde, is_combust, conjunct_malefics, in_benefic_vargas,
        ),
        "shyanadi": calculate_shyanadi(
            planet, sign, house, is_retrograde, is_combust,
            aspected_by_saturn, aspected_by_jupiter, aspected_by_friends,
            aspected_by_benefics, conjunct_benefics, conjunct_moon_good,
            num_benefic_vargas,
        ),
    }
