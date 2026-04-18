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
  10. LIFE_PREDICTIONS      - 8 life areas based on house-sign analysis
  11. NAKSHATRA_PHAL        - 27 nakshatras x 4 padas detailed predictions
  12. ASCENDANT_PERSONALITY - Extended personality profiles per ascendant
  13. MAHADASHA_DETAILED    - Mahadasha effects by planet's house placement
"""
from __future__ import annotations

from typing import Any, Dict, Tuple

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
            "Transformative  -  rises from setbacks stronger",
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
            "Ages in reverse  -  becomes lighter with time",
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


# ============================================================
# 10. LIFE_PREDICTIONS -- 8 Life Areas by House Sign
# ============================================================

LIFE_PREDICTIONS: Dict[str, Dict[str, str]] = {
    "career": {
        "Aries": (
            "Strong leadership drives your professional life. You excel in competitive environments "
            "where initiative and courage are rewarded -- military, sports, surgery, engineering, or entrepreneurship. "
            "Mars energy makes you a self-starter who prefers to lead rather than follow. "
            "Career breakthroughs often come through bold, independent action rather than patient waiting."
        ),
        "Taurus": (
            "Steady career growth through persistence and reliability defines your professional journey. "
            "You thrive in banking, agriculture, real estate, luxury goods, hospitality, and fine arts. "
            "Venus-ruled Taurus on the 10th gives an eye for aesthetics that can translate into profitable ventures. "
            "Financial security matters more to you than fame, and your patience eventually builds lasting wealth."
        ),
        "Gemini": (
            "Communication is the cornerstone of your career success. You shine in writing, journalism, "
            "teaching, marketing, trading, and information technology. Mercury's influence gives versatility -- "
            "you may hold multiple roles or change fields more than once. Your networking ability and quick wit "
            "open doors that remain closed to others, but focus is essential to avoid scattered energies."
        ),
        "Cancer": (
            "Your career flourishes in nurturing, caregiving, and emotionally resonant professions. "
            "Hospitality, food industry, nursing, counselling, interior design, and public welfare suit you well. "
            "The Moon's rulership makes your professional life subject to emotional tides -- periods of intense "
            "productivity alternate with withdrawal. Working close to home or in family businesses is highly favourable."
        ),
        "Leo": (
            "The stage is your natural workplace. Politics, entertainment, senior management, government, "
            "and creative direction are fields where your Sun-ruled 10th house sign shines brightest. "
            "You need recognition and authority in your role; subordinate positions breed discontent. "
            "Your generosity and personal magnetism attract loyal teams, making you a natural CEO or director."
        ),
        "Virgo": (
            "Analytical precision and service orientation define your professional path. Healthcare, "
            "accounting, editing, quality control, data science, and pharmaceutical work suit you perfectly. "
            "Mercury's rulership gives meticulous attention to detail that others find extraordinary. "
            "Promotions may come slowly but your work speaks for itself and builds an impeccable reputation over time."
        ),
        "Libra": (
            "Partnership and diplomacy are central to your career success. Law, judiciary, diplomacy, "
            "fashion design, mediation, and luxury retail are ideal fields. Venus-ruled Libra on the 10th "
            "gives an elegant public image and skill in managing relationships. Joint ventures and collaborations "
            "bring greater success than solo efforts, and fairness in dealings earns lasting professional respect."
        ),
        "Scorpio": (
            "Intensity and transformation mark your professional journey. Research, investigation, surgery, "
            "psychology, insurance, occult sciences, and crisis management are your forte. Mars and Ketu's "
            "combined influence gives unmatched focus and willingness to probe hidden truths. Your career often "
            "involves dramatic shifts that ultimately lead to positions of deep influence behind the scenes."
        ),
        "Sagittarius": (
            "Wisdom and expansion drive your career. Higher education, law, publishing, foreign trade, "
            "philosophy, religious leadership, and long-distance travel industries suit you. Jupiter's rulership "
            "bestows optimism and ethical conduct that earns trust in positions of authority. International "
            "connections play a significant role, and your career often takes you far from your birthplace."
        ),
        "Capricorn": (
            "Ambition and structure are the pillars of your professional life. Government administration, "
            "mining, construction, corporate management, and traditional industries reward your disciplined nature. "
            "Saturn's rulership demands patience -- career heights are reached in the 30s and 40s rather than early. "
            "Your capacity for hard work and organisational skill eventually places you in positions of lasting authority."
        ),
        "Aquarius": (
            "Innovation and social reform characterise your career path. Technology, aviation, social work, "
            "NGO leadership, scientific research, and network-based businesses are ideal. Saturn and Rahu's "
            "combined influence gives both discipline and unconventional thinking. Your greatest professional "
            "success comes through serving collective goals rather than purely personal ambition."
        ),
        "Pisces": (
            "Intuition and compassion guide your professional life. Spiritual teaching, music, cinema, "
            "marine industries, hospital administration, charitable work, and the healing arts suit you. "
            "Jupiter's rulership bestows wisdom and selflessness that earns deep respect. Your career may "
            "lack conventional structure but its impact on others' lives is profound and your reputation endures."
        ),
    },
    "health": {
        "Aries": (
            "With Aries influencing your health house, you are prone to acute conditions -- fevers, "
            "inflammation, headaches, and blood-related disorders. Your body runs hot and responds quickly "
            "to both illness and recovery. Regular physical activity is essential to channel excess Mars energy. "
            "Guard especially against head injuries, migraines, and skin eruptions caused by pitta imbalance."
        ),
        "Taurus": (
            "Taurus on the 6th house gives a generally robust constitution but vulnerability in the throat, "
            "thyroid, and cervical spine. Overindulgence in rich foods leads to weight gain and metabolic issues. "
            "Your recovery from illness is slow but thorough once you commit to treatment. "
            "Diabetes, tonsillitis, and neck stiffness are conditions to monitor throughout life."
        ),
        "Gemini": (
            "Gemini influencing health brings nervous system sensitivity and respiratory vulnerability. "
            "Anxiety, insomnia, bronchial issues, and shoulder-arm complaints are common patterns. "
            "Your mental health is deeply tied to physical well-being -- stress manifests as bodily symptoms quickly. "
            "Regular pranayama, moderate exercise, and digital detoxes protect your delicate nervous constitution."
        ),
        "Cancer": (
            "The Moon's influence on your health house makes you susceptible to digestive and emotional ailments. "
            "Acidity, water retention, chest congestion, and hormonal fluctuations follow lunar cycles. "
            "Emotional eating and comfort-seeking behaviour can lead to stomach disorders. "
            "A calm domestic environment and regular meal timing are your best preventive medicines."
        ),
        "Leo": (
            "Leo on the 6th house gives vitality but vulnerability in the heart, spine, and eyes. "
            "Blood pressure, cardiac rhythm issues, and spinal problems require monitoring after age 35. "
            "Your constitution is strong when the Sun is well-placed but weakens dramatically under stress. "
            "Regular cardiovascular exercise, avoiding excessive anger, and sun salutations keep you robust."
        ),
        "Virgo": (
            "Mercury-ruled Virgo on the health house creates sensitivity in the intestines and nervous digestion. "
            "IBS, food allergies, skin issues from internal toxins, and anxiety-driven ailments are common. "
            "Your tendency to worry amplifies minor symptoms into major concerns. "
            "A clean diet, herbal supplements, and routine health check-ups serve you far better than overthinking."
        ),
        "Libra": (
            "Libra influencing health brings kidney, lower back, and urinary tract vulnerabilities. "
            "Sugar imbalances, skin conditions related to blood impurity, and reproductive health issues arise. "
            "Your health improves dramatically when emotional relationships are harmonious. "
            "Adequate water intake, avoiding processed foods, and maintaining work-life balance are essential."
        ),
        "Scorpio": (
            "Scorpio on the 6th house indicates intense health crises that ultimately lead to transformation. "
            "Reproductive organs, excretory system, and hidden infections are vulnerable areas. "
            "Surgical interventions may be necessary at some point in life but lead to complete recovery. "
            "Detoxification routines, sexual health awareness, and regular screening prevent serious complications."
        ),
        "Sagittarius": (
            "Jupiter's influence on health gives a generally optimistic constitution but excess in liver, "
            "hips, and thighs. Fatty liver, sciatica, and weight gain from overindulgence are common patterns. "
            "Your faith and positive outlook aid recovery remarkably well. "
            "Moderation in diet, hip-strengthening exercises, and periodic fasting maintain your natural vitality."
        ),
        "Capricorn": (
            "Saturn-ruled Capricorn on the health house brings chronic but manageable conditions. "
            "Joint pain, arthritis, dental issues, knee problems, and skin dryness develop gradually over time. "
            "Your constitution strengthens with age -- health in the 40s is often better than in the 20s. "
            "Calcium-rich diet, joint mobility exercises, and patience with slow-healing conditions are advised."
        ),
        "Aquarius": (
            "Aquarius influencing health brings unusual or hard-to-diagnose conditions affecting circulation "
            "and the nervous system. Varicose veins, ankle injuries, and sudden onset ailments are characteristic. "
            "Your health benefits greatly from unconventional healing modalities -- acupuncture, energy healing, "
            "and Ayurvedic approaches may work better than conventional medicine for your constitution."
        ),
        "Pisces": (
            "Pisces on the 6th house creates sensitivity to allergies, foot problems, and immune system "
            "fluctuations. Lymphatic congestion, psychosomatic illness, and sensitivity to medications are common. "
            "Your health is deeply influenced by your spiritual and emotional state. "
            "Meditation, swimming, adequate sleep, and avoiding intoxicants are your most powerful health practices."
        ),
    },
    "marriage": {
        "Aries": (
            "Mars-ruled Aries on the 7th house brings a passionate, dynamic, but sometimes combative marriage. "
            "You attract strong-willed, independent partners who challenge you to grow. Arguments are frequent "
            "but reconciliations are equally intense. Early marriage may face turbulence; maturity improves harmony. "
            "Physical attraction and mutual respect are the bedrock of your partnerships."
        ),
        "Taurus": (
            "Venus-ruled Taurus on the 7th house promises a stable, sensual, and materially comfortable marriage. "
            "Your spouse is likely attractive, loyal, and fond of good living. Possessiveness and stubbornness "
            "are the main challenges. The relationship deepens with time like fine wine. "
            "Shared appreciation for beauty, food, music, and nature strengthens the bond."
        ),
        "Gemini": (
            "Mercury's influence on your 7th house brings an intellectually stimulating partnership. "
            "Your spouse is communicative, witty, and possibly younger in spirit or age. Variety and mental "
            "connection matter more than physical passion. The risk is superficiality or multiple attachments. "
            "A partner who shares your curiosity and love of learning makes marriage a lifelong conversation."
        ),
        "Cancer": (
            "The Moon ruling your 7th house gives an emotionally deep and nurturing marriage. Your spouse is "
            "caring, domestic, and deeply attached to family. Mood swings and emotional dependency can strain "
            "the relationship. A secure home environment is essential for marital happiness. "
            "Children and family traditions become the glue that holds the partnership together."
        ),
        "Leo": (
            "The Sun on your 7th house attracts a proud, dignified, and authoritative spouse. Your partner "
            "commands attention and expects loyalty and admiration. Power struggles are the main challenge. "
            "When both egos are managed, the marriage is grand, warm, and generous. "
            "Public status and social standing of the couple matter significantly in this combination."
        ),
        "Virgo": (
            "Mercury-ruled Virgo on the 7th house brings a practical, service-oriented marriage. Your spouse "
            "is detail-oriented, health-conscious, and possibly critical. Perfectionism can create friction. "
            "The partnership improves when both focus on serving each other rather than finding faults. "
            "Shared routines, health goals, and intellectual pursuits create lasting harmony."
        ),
        "Libra": (
            "Venus-ruled Libra on the 7th house is the ideal placement for marriage. Partnership, romance, "
            "and mutual respect come naturally. Your spouse is charming, fair-minded, and socially graceful. "
            "Indecisiveness and avoidance of conflict are the only weaknesses. "
            "This placement favours love marriage and enduring conjugal happiness built on true companionship."
        ),
        "Scorpio": (
            "Mars-Ketu ruled Scorpio on the 7th house creates an intensely transformative marriage. "
            "Passion runs deep but so do jealousy and possessiveness. Your spouse has magnetic appeal and "
            "strong willpower. Trust issues and power dynamics require conscious work. "
            "When both partners surrender control, the marriage becomes a vehicle for profound spiritual growth."
        ),
        "Sagittarius": (
            "Jupiter's blessing on the 7th house brings an expansive, philosophical, and fortunate marriage. "
            "Your spouse is wise, optimistic, and often from a different cultural or educational background. "
            "Freedom within the relationship is essential -- neither partner tolerates possessiveness. "
            "Travel, higher learning, and shared spiritual values keep the marriage vibrant across decades."
        ),
        "Capricorn": (
            "Saturn-ruled Capricorn on the 7th house delays marriage but ensures its durability. Your spouse "
            "is mature, responsible, and possibly older. The early years may feel dry or burdensome. "
            "With patience, the partnership becomes a rock-solid foundation for shared ambitions. "
            "Mutual respect for each other's career goals and a practical approach to love are the keys."
        ),
        "Aquarius": (
            "Saturn-Rahu ruled Aquarius on the 7th house creates an unconventional marriage. Your spouse is "
            "independent, progressive, and possibly eccentric. Traditional relationship expectations are challenged. "
            "Friendship-based marriage works best; possessiveness destroys the bond. "
            "Shared humanitarian values, intellectual companionship, and personal space sustain this unusual union."
        ),
        "Pisces": (
            "Jupiter-ruled Pisces on the 7th house brings a spiritually elevated and compassionate marriage. "
            "Your spouse is gentle, intuitive, artistic, and possibly self-sacrificing. Boundaries may blur. "
            "Escapism through fantasy or substances is the main risk. "
            "When grounded in devotion and mutual care, this marriage feels like a divine partnership."
        ),
    },
    "finance": {
        "Aries": (
            "Mars-ruled Aries on the 2nd house gives aggressive earning capacity and bold financial decisions. "
            "Income comes through competitive fields, sports, engineering, or self-employment. You earn quickly "
            "but spend impulsively. Building savings requires conscious discipline against your fiery nature. "
            "Investments in real estate and metals tend to be more profitable than speculative ventures."
        ),
        "Taurus": (
            "Venus-ruled Taurus on the 2nd house is the most favourable placement for wealth accumulation. "
            "Steady income, a love of saving, and good taste in investments mark your financial life. "
            "Banking, agriculture, luxury goods, and real estate are your strongest wealth channels. "
            "Family wealth and inheritance are likely, and your financial position improves steadily with age."
        ),
        "Gemini": (
            "Mercury-ruled Gemini on the 2nd house creates multiple income streams and financial versatility. "
            "Earnings come through communication, trading, brokerage, writing, or intellectual property. "
            "Your financial situation fluctuates -- brilliant gains alternate with careless losses. "
            "Systematic investing and avoiding gossip-driven financial decisions protect your wealth."
        ),
        "Cancer": (
            "The Moon on the 2nd house makes finances subject to emotional tides and cyclical patterns. "
            "Income from food, hospitality, real estate, and maternal family is indicated. "
            "Savings grow when you feel emotionally secure; insecurity triggers spending on comfort. "
            "Property investment, particularly residential, is your safest and most rewarding avenue."
        ),
        "Leo": (
            "The Sun on the 2nd house brings wealth through government, authority, and positions of power. "
            "You earn well but spend lavishly on maintaining status and generosity toward dependents. "
            "Gold, government bonds, and investments in entertainment or education are favourable. "
            "Your financial peak often coincides with periods of public recognition or political influence."
        ),
        "Virgo": (
            "Mercury-ruled Virgo on the 2nd house gives careful, analytical financial management. "
            "Income from healthcare, service industries, accounting, and detailed work is indicated. "
            "You rarely make impulsive financial decisions and prefer low-risk, steady-return investments. "
            "Tax planning and budgeting come naturally, making you financially secure if not spectacularly wealthy."
        ),
        "Libra": (
            "Venus-ruled Libra on the 2nd house attracts wealth through partnerships and aesthetic enterprises. "
            "Fashion, jewellery, art dealing, legal practice, and collaborative ventures are profitable. "
            "Your financial success is often intertwined with your spouse's or business partner's fortunes. "
            "Balanced spending on beauty and comfort does not diminish wealth but rather attracts more of it."
        ),
        "Scorpio": (
            "Mars-Ketu ruled Scorpio on the 2nd house creates intense financial experiences -- inheritance, "
            "insurance payouts, or sudden gains and losses. Research, mining, surgery, and occult-related income. "
            "You have a secretive approach to money and rarely reveal your true financial position. "
            "Transformation through financial crises ultimately leads to deeper wisdom about true value."
        ),
        "Sagittarius": (
            "Jupiter's blessing on the 2nd house is highly auspicious for wealth and family prosperity. "
            "Income from teaching, law, publishing, foreign trade, and religious or spiritual work. "
            "You are generous with money and your open-handedness is rewarded by Providence. "
            "Long-term investments, especially in education and foreign markets, yield excellent returns."
        ),
        "Capricorn": (
            "Saturn-ruled Capricorn on the 2nd house builds wealth slowly but permanently. "
            "Income from government, construction, mining, oil, and traditional industries. "
            "Early life may see financial constraints, but discipline creates substantial wealth by middle age. "
            "Real estate, fixed deposits, and conservative blue-chip investments suit your cautious temperament."
        ),
        "Aquarius": (
            "Saturn-Rahu ruled Aquarius on the 2nd house brings unconventional income sources. "
            "Technology, cryptocurrency, network marketing, aviation, and social enterprises are indicated. "
            "Your financial philosophy is progressive -- you value freedom over accumulation. "
            "Sudden gains through innovation or technology disruption can dramatically change your financial standing."
        ),
        "Pisces": (
            "Jupiter-ruled Pisces on the 2nd house attracts wealth through intuition and spiritual alignment. "
            "Income from music, cinema, hospital administration, charity, marine activities, and healing arts. "
            "You are generous to a fault and may lose money through misplaced trust or lack of boundaries. "
            "When your financial decisions align with your spiritual values, abundance flows naturally."
        ),
    },
    "education": {
        "Aries": (
            "Mars-ruled Aries influencing education gives a competitive, fast-learning mind that excels under "
            "pressure. You prefer practical, hands-on learning over theoretical study. Engineering, military "
            "science, surgery, and sports education are naturally suited fields. Early academic life may show "
            "impulsiveness, but focused coaching channels your energy into impressive academic achievements."
        ),
        "Taurus": (
            "Venus-ruled Taurus on the education house gives a steady, methodical learning approach. "
            "You absorb knowledge slowly but retain it permanently. Fine arts, music, agriculture, economics, "
            "and culinary arts are ideal fields of study. A comfortable, aesthetically pleasing study environment "
            "dramatically improves your concentration and academic output."
        ),
        "Gemini": (
            "Mercury-ruled Gemini is among the strongest placements for intellectual achievement. "
            "You excel in languages, mathematics, commerce, journalism, and computer science. Your learning "
            "speed is exceptional but depth may suffer due to scattered interests. Debate, quizzing, and "
            "competitive examinations showcase your mental agility and communication skills."
        ),
        "Cancer": (
            "Moon-ruled Cancer on the education house gives excellent memory and intuitive learning ability. "
            "History, psychology, nursing, home science, and marine biology suit your emotional intelligence. "
            "Your academic performance fluctuates with emotional state -- supportive teachers matter immensely. "
            "Education received at home or in a nurturing environment yields the best results."
        ),
        "Leo": (
            "Sun-ruled Leo influencing education gives confidence and flair in academic settings. "
            "Political science, performing arts, administration, and leadership programmes suit you well. "
            "You prefer being the best student in class rather than part of the crowd. "
            "Government scholarships and recognition for academic excellence are strongly indicated."
        ),
        "Virgo": (
            "Mercury-ruled Virgo is the finest placement for analytical and scientific education. "
            "Medicine, pharmacy, statistics, editing, research methodology, and environmental science are ideal. "
            "Your attention to detail makes you a natural scholar who produces meticulous work. "
            "Overly critical self-assessment can create examination anxiety despite strong preparation."
        ),
        "Libra": (
            "Venus-ruled Libra on the education house favours artistic and social sciences. "
            "Law, diplomacy, fashion design, architecture, and international relations are naturally suited fields. "
            "You learn best through discussion and collaboration rather than solitary study. "
            "Aesthetic subjects and those requiring balanced judgement bring out your highest intellectual abilities."
        ),
        "Scorpio": (
            "Mars-Ketu ruled Scorpio influencing education gives intense, focused research ability. "
            "Psychology, forensic science, surgery, occult studies, and detective work suit your probing mind. "
            "You are drawn to hidden knowledge and excel in subjects others find dark or difficult. "
            "Academic breakthroughs often come through obsessive deep study rather than breadth of learning."
        ),
        "Sagittarius": (
            "Jupiter's blessing on the education house is supremely favourable for higher learning. "
            "Philosophy, theology, law, foreign languages, and university teaching are natural fields. "
            "You are drawn to wisdom traditions and excel in environments that value ethical thinking. "
            "Study abroad or distance education from foreign universities is strongly indicated and successful."
        ),
        "Capricorn": (
            "Saturn-ruled Capricorn on the education house delays academic success but makes it permanent. "
            "Civil engineering, architecture, geology, public administration, and traditional crafts suit you. "
            "Early academic life may show obstacles or late starts, but persistence pays off handsomely. "
            "Professional certifications and practical qualifications serve you better than theoretical degrees."
        ),
        "Aquarius": (
            "Saturn-Rahu influenced Aquarius on the education house favours cutting-edge and unconventional study. "
            "Aerospace, information technology, social sciences, astrology, and futuristic research suit you. "
            "You learn best through experimentation and may be self-taught in key areas. "
            "Group study and online learning platforms enhance your naturally network-oriented intelligence."
        ),
        "Pisces": (
            "Jupiter-ruled Pisces influencing education gives exceptional intuitive and creative intelligence. "
            "Fine arts, music, spiritual philosophy, marine science, and healing arts are your ideal fields. "
            "Your learning style is absorptive rather than analytical -- you understand through feeling. "
            "Meditation and retreats may contribute more to your real education than formal classroom instruction."
        ),
    },
    "character": {
        "Aries": (
            "You are a born pioneer with a courageous, direct, and fiercely independent character. "
            "Honesty to the point of bluntness, quick temper that cools equally fast, and restless energy "
            "define your personality. You lead from the front and cannot tolerate cowardice or dishonesty. "
            "Your greatest virtue is courage; your greatest challenge is patience."
        ),
        "Taurus": (
            "You possess a steady, patient, and deeply loyal character rooted in material reality. "
            "Reliability, sensuality, and a stubborn refusal to be rushed are your hallmarks. "
            "You value comfort, beauty, and security above adventure or novelty. "
            "Your greatest virtue is dependability; your greatest challenge is resistance to change."
        ),
        "Gemini": (
            "An intellectually curious, quick-witted, and endlessly adaptable character defines you. "
            "You process information faster than most and communicate with charm and precision. "
            "Duality is inherent -- you can argue both sides of any issue with equal conviction. "
            "Your greatest virtue is versatility; your greatest challenge is consistency."
        ),
        "Cancer": (
            "You carry a deeply emotional, nurturing, and protective character beneath a tough exterior. "
            "Family and emotional security are your core motivations in every decision you make. "
            "Your memory is powerful and you hold onto both love and grudges with equal tenacity. "
            "Your greatest virtue is devotion; your greatest challenge is letting go of the past."
        ),
        "Leo": (
            "A generous, dignified, and magnificently confident character radiates from your being. "
            "You command attention effortlessly and feel most alive when appreciated and respected. "
            "Leadership comes naturally, though your pride can make you vulnerable to flattery. "
            "Your greatest virtue is magnanimity; your greatest challenge is ego management."
        ),
        "Virgo": (
            "You embody a precise, analytical, and service-oriented character with exacting standards. "
            "Detail-oriented to a remarkable degree, you notice what others miss entirely. "
            "Self-criticism and a desire for perfection drive both your achievements and your anxieties. "
            "Your greatest virtue is discrimination; your greatest challenge is self-acceptance."
        ),
        "Libra": (
            "Balance, harmony, and aesthetic refinement characterise your elegant personality. "
            "You seek fairness in all dealings and are deeply uncomfortable with conflict or ugliness. "
            "Partnership is essential -- you understand yourself best through relationship with others. "
            "Your greatest virtue is diplomacy; your greatest challenge is decisiveness."
        ),
        "Scorpio": (
            "Intensity, depth, and unwavering determination define your powerful character. "
            "You see beneath surfaces and are drawn to life's hidden dimensions -- psychology, mystery, power. "
            "Loyalty to your chosen few is absolute, but betrayal triggers devastating consequences. "
            "Your greatest virtue is transformative power; your greatest challenge is releasing control."
        ),
        "Sagittarius": (
            "An optimistic, freedom-loving, and philosophically minded character propels your life. "
            "You seek meaning above material gain and feel stifled by routine or narrow thinking. "
            "Honesty is your default mode, sometimes delivered with uncomfortable directness. "
            "Your greatest virtue is wisdom-seeking; your greatest challenge is commitment."
        ),
        "Capricorn": (
            "Disciplined, ambitious, and profoundly responsible -- your character is built for endurance. "
            "You take life seriously, often shouldering burdens others would refuse, without complaint. "
            "Time is your ally; you grow stronger, wiser, and more prosperous as you age. "
            "Your greatest virtue is perseverance; your greatest challenge is allowing joy."
        ),
        "Aquarius": (
            "You are an independent thinker with a humanitarian, progressive, and sometimes eccentric character. "
            "Conventional expectations feel like chains to you; your mind operates ahead of its time. "
            "You value friendship and collective well-being over personal emotional attachment. "
            "Your greatest virtue is originality; your greatest challenge is emotional warmth."
        ),
        "Pisces": (
            "A deeply compassionate, intuitive, and spiritually attuned character flows through your being. "
            "You absorb others' emotions like a sponge and feel the pain of the world acutely. "
            "Artistic and mystical gifts are abundant, though practical reality can feel overwhelming. "
            "Your greatest virtue is unconditional compassion; your greatest challenge is boundaries."
        ),
    },
    "hobbies": {
        "Aries": (
            "You are naturally drawn to high-energy, competitive pursuits. Martial arts, trekking, motorsports, "
            "and adventure travel satisfy your Mars-driven need for adrenaline. You enjoy being the first to try "
            "new activities and quickly lose interest in passive entertainment. Physical challenges, outdoor sports, "
            "and DIY projects keep your restless spirit engaged and happy."
        ),
        "Taurus": (
            "Sensory pleasures define your leisure time. Cooking, gardening, music appreciation, pottery, "
            "and collecting fine objects bring deep satisfaction. You prefer hobbies that produce tangible results "
            "and engage the senses. Nature walks, wine tasting, and interior decoration reflect your Venus-ruled "
            "desire for beauty and comfort in every aspect of life."
        ),
        "Gemini": (
            "Intellectual stimulation is the thread connecting all your hobbies. Reading, puzzles, board games, "
            "podcasting, blogging, and learning new languages keep your Mercury-ruled mind active. "
            "You tend to have many hobbies simultaneously and cycle between them. Social hobbies -- debating, "
            "quiz competitions, and book clubs -- satisfy your need for mental sparring and human connection."
        ),
        "Cancer": (
            "Home-centred and emotionally nourishing activities are your preferred pastimes. Cooking family "
            "recipes, scrapbooking, home decoration, swimming, and genealogy research satisfy your lunar nature. "
            "You enjoy hobbies that connect you with your roots and create lasting memories. "
            "Caring for pets, tending a home garden, and hosting intimate gatherings bring genuine joy."
        ),
        "Leo": (
            "Creative performance and self-expression drive your leisure pursuits. Theatre, dance, painting, "
            "photography, and any activity where you can shine before an audience captivate you. "
            "You enjoy organising events and being the life of social gatherings. "
            "Luxury hobbies -- fine dining, fashion, and travel to glamorous destinations -- appeal to your royal nature."
        ),
        "Virgo": (
            "Precision-based and health-oriented hobbies suit your analytical Virgo nature. Yoga, herbal "
            "gardening, journaling, jigsaw puzzles, and craft-making satisfy your need for order and detail. "
            "You enjoy hobbies that improve your skills incrementally over time. Reading non-fiction, organising "
            "spaces, and volunteering for service-oriented causes bring quiet but deep fulfilment."
        ),
        "Libra": (
            "Aesthetic and social hobbies define your leisure. Painting, music, fashion design, ballroom dancing, "
            "and art gallery visits feed your Venus-ruled craving for beauty and harmony. "
            "You enjoy activities you can share with a partner or close friends. "
            "Hosting elegant gatherings, interior styling, and cultural events are pastimes you naturally excel at."
        ),
        "Scorpio": (
            "Intense, investigative, and transformative hobbies attract you. True crime research, psychology "
            "study, scuba diving, martial arts, and mystery-solving games engage your probing Scorpio nature. "
            "You prefer depth over variety and may pursue a single hobby with obsessive dedication. "
            "Occult studies, tantric meditation, and extreme sports provide the intensity you crave."
        ),
        "Sagittarius": (
            "Adventure and learning are inseparable in your leisure life. Long-distance travel, horse riding, "
            "archery, philosophy reading, and foreign culture exploration light up your Jupiter-ruled spirit. "
            "You are the eternal student who finds joy in every new experience and place. "
            "Outdoor activities, spiritual retreats, and cultural festivals are your favourite pastimes."
        ),
        "Capricorn": (
            "Structured, goal-oriented hobbies satisfy your Saturn-ruled temperament. Mountain climbing, chess, "
            "woodworking, numismatics, and historical study appeal to your disciplined nature. "
            "You prefer hobbies that build skill over time and produce measurable results. "
            "Antique collecting, architecture appreciation, and strategic board games are lifelong interests."
        ),
        "Aquarius": (
            "Unconventional and technology-driven hobbies excite your progressive nature. Astronomy, coding, "
            "drone flying, electronic music production, and social activism are characteristic pursuits. "
            "You enjoy hobbies that connect you with like-minded communities or push societal boundaries. "
            "Science fiction, futuristic gadgets, and humanitarian volunteering reflect your visionary Aquarian spirit."
        ),
        "Pisces": (
            "Creative and spiritual hobbies nourish your sensitive Piscean soul. Music, painting, poetry, "
            "swimming, meditation, and dream journaling are natural outlets for your vast imagination. "
            "You are drawn to activities near water and those that allow emotional or spiritual expression. "
            "Film appreciation, charity work, and healing arts like Reiki or crystal therapy bring deep peace."
        ),
    },
    "family": {
        "Aries": (
            "Mars energy on the 4th house creates a dynamic but sometimes volatile home environment. "
            "You take charge of family matters with decisive authority. Property disputes or renovation "
            "projects are common themes. Independence was established early -- you may have left home young. "
            "Family relationships improve when you channel competitive energy into protecting rather than controlling."
        ),
        "Taurus": (
            "Venus-ruled Taurus on the 4th house is excellent for domestic happiness and property ownership. "
            "Your home is comfortable, well-decorated, and a source of genuine pride. Family bonds are strong "
            "and enduring, especially with your mother. Ancestral property and family wealth are likely. "
            "Stability and tradition are the pillars of your family life across generations."
        ),
        "Gemini": (
            "Mercury's influence on the 4th house creates an intellectually stimulating home environment. "
            "Family discussions, debates, and a house full of books and media define your domestic space. "
            "You may change residences frequently or have multiple properties. Family communication "
            "is lively but sometimes superficial -- deeper emotional bonding requires conscious effort."
        ),
        "Cancer": (
            "The Moon ruling the 4th house is the most natural and powerful placement for family happiness. "
            "Your mother's influence is profound and your attachment to ancestral home and traditions is deep. "
            "Nurturing your family is your primary source of emotional fulfilment. "
            "Property near water, a well-stocked kitchen, and family gatherings define your domestic bliss."
        ),
        "Leo": (
            "Sun-ruled Leo on the 4th house creates a proud, dignified home environment. "
            "Your residence reflects your status -- spacious, well-lit, and impressive. Father's influence "
            "on family culture is strong. You take pride in your lineage and family achievements. "
            "Generosity toward family members and a regal household atmosphere characterise your home life."
        ),
        "Virgo": (
            "Mercury-ruled Virgo on the 4th house creates an orderly, health-conscious home environment. "
            "Cleanliness, routine, and practical efficiency define your domestic life. Your mother is "
            "detail-oriented and health-focused. Property investments are carefully researched and sensible. "
            "Family relationships improve when you relax your critical standards and accept imperfection."
        ),
        "Libra": (
            "Venus-ruled Libra on the 4th house blesses the home with beauty, harmony, and social grace. "
            "Your residence is tastefully decorated and serves as a gathering place for friends and family. "
            "Both parents contribute equally to your upbringing. Property with aesthetic appeal attracts you. "
            "Family peace depends on maintaining balance and avoiding taking sides in domestic disputes."
        ),
        "Scorpio": (
            "Mars-Ketu ruled Scorpio on the 4th house creates deep, intense family dynamics. "
            "Family secrets, ancestral karma, and transformative domestic experiences shape your inner life. "
            "Property matters may involve disputes or dramatic changes. Your emotional attachment to home "
            "runs very deep despite an outward appearance of detachment. Healing family karma is a life theme."
        ),
        "Sagittarius": (
            "Jupiter's blessing on the 4th house creates an expansive, philosophical, and fortunate home life. "
            "Your family values education, ethics, and spiritual growth. Property ownership is indicated, "
            "often in multiple locations or abroad. Your home functions as a place of learning and wisdom. "
            "International connections within the family and a liberal, open-minded household atmosphere prevail."
        ),
        "Capricorn": (
            "Saturn-ruled Capricorn on the 4th house creates a structured, disciplined family environment. "
            "Emotional warmth may have been scarce in early life, replaced by duty and responsibility. "
            "Property accumulation is slow but substantial. Family traditions and ancestral obligations are "
            "taken seriously. Domestic happiness increases markedly after middle age as Saturn rewards patience."
        ),
        "Aquarius": (
            "Saturn-Rahu influenced Aquarius on the 4th house creates an unconventional home life. "
            "Your family may be progressive, scattered geographically, or non-traditional in structure. "
            "Technology plays a large role in your domestic space. Emotional distance from roots is possible "
            "but compensated by chosen-family bonds. Property in unusual locations or modern apartments suits you."
        ),
        "Pisces": (
            "Jupiter-ruled Pisces on the 4th house creates a spiritually rich and emotionally nourishing home. "
            "Your mother is compassionate and possibly spiritually inclined. The home serves as a sanctuary "
            "from the world's harshness. Property near water is highly favourable. "
            "Family life is gentle, artistic, and deeply connected to devotion and selfless love."
        ),
    },
}


# ============================================================
# 11. NAKSHATRA_PHAL -- 27 Nakshatras x 4 Padas Predictions
# ============================================================

NAKSHATRA_PHAL: Dict[str, Dict[int, str]] = {
    "Ashwini": {
        1: (
            "Born in Ashwini Pada 1 (Aries navamsha), you are blessed with extraordinary healing abilities "
            "and a pioneering spirit. Your energy is electric -- you initiate projects with remarkable speed "
            "and inspire others through fearless action. Career success comes in medicine, emergency services, "
            "or entrepreneurship. Spiritually, you carry the gift of renewal and can help others recover from crisis."
        ),
        2: (
            "Ashwini Pada 2 (Taurus navamsha) natives combine healing gifts with a strong material drive. "
            "You seek financial security through your skills and are attracted to luxury and beauty. "
            "Career in veterinary science, ayurveda, cosmetics, or automobile industries is favoured. "
            "Family life is comfortable and you invest wisely. Spiritual growth comes through grounding practices."
        ),
        3: (
            "Ashwini Pada 3 (Gemini navamsha) brings intellectual agility combined with Ashwini's healing nature. "
            "You are an excellent communicator who can translate complex health or technical knowledge for others. "
            "Media, medical writing, pharmaceutical marketing, and technical education suit you. "
            "Restlessness is your challenge -- multiple interests scatter your considerable talents."
        ),
        4: (
            "Ashwini Pada 4 (Cancer navamsha) natives are nurturing healers with deep emotional intelligence. "
            "You are drawn to caregiving professions and have an intuitive understanding of others' pain. "
            "Nursing, paediatrics, midwifery, and emotional counselling are ideal careers. "
            "Family bonds are exceptionally strong and your home serves as a healing sanctuary for many."
        ),
    },
    "Bharani": {
        1: (
            "Bharani Pada 1 (Leo navamsha) gives a fiery, creative personality with strong reproductive energy. "
            "You are a natural leader in creative fields -- cinema, theatre, fertility medicine, and event management. "
            "Your magnetism attracts attention but also jealousy. Children and creative projects define your legacy. "
            "Spiritual evolution comes through learning to channel Bharani's intense Venusian-Yama energy wisely."
        ),
        2: (
            "Bharani Pada 2 (Virgo navamsha) balances Bharani's intensity with analytical precision. "
            "You are methodical in managing life's transformative events -- birth, death, inheritance, taxation. "
            "Career in forensic accounting, surgery, quality control, or critical care nursing suits you well. "
            "Health-consciousness and self-improvement are lifelong themes. Perfectionism needs moderation."
        ),
        3: (
            "Bharani Pada 3 (Libra navamsha) combines Bharani's transformative power with Venusian grace. "
            "You navigate life's extremes with remarkable poise and attract deep, passionate relationships. "
            "Career in marriage counselling, family law, luxury hospitality, or reproductive health is ideal. "
            "Partnership is central to your evolution; the right spouse transforms your entire life trajectory."
        ),
        4: (
            "Bharani Pada 4 (Scorpio navamsha) is Bharani at its most intense -- Pushkara navamsha amplifies depth. "
            "You are drawn to life's mysteries: psychology, tantra, inheritance law, and transformative healing. "
            "Emotional resilience is extraordinary but trust issues need conscious work. "
            "Your spiritual path involves confronting death, rebirth, and the deepest layers of consciousness."
        ),
    },
    "Krittika": {
        1: (
            "Krittika Pada 1 (Sagittarius navamsha) combines fire with wisdom -- you are a righteous warrior. "
            "Truth and dharma are non-negotiable principles in your life. Teaching, law, military leadership, "
            "and religious scholarship suit you. Your sharp tongue can wound, but your intentions are pure. "
            "Spiritual advancement comes through discipline, fire rituals, and adherence to ethical conduct."
        ),
        2: (
            "Krittika Pada 2 (Capricorn navamsha) natives are disciplined, ambitious, and sharply focused. "
            "You climb to positions of authority through sheer determination and principled conduct. "
            "Government administration, metallurgy, heavy industry, and structural engineering suit you. "
            "Patience is your greatest asset -- success comes late but is permanent and deeply respected."
        ),
        3: (
            "Krittika Pada 3 (Aquarius navamsha) directs Krittika's fire toward humanitarian and innovative goals. "
            "You fight for social justice with a sharp, incisive mind. Technology, social reform, astronomy, "
            "and network-based leadership are your fields. Unconventional approaches to traditional knowledge "
            "set you apart. Spiritual growth comes through service to collective humanity."
        ),
        4: (
            "Krittika Pada 4 (Pisces navamsha) softens the fire with compassion and spiritual depth. "
            "You are a mystic warrior -- fierce in protecting the vulnerable yet gentle in personal dealings. "
            "Charity work, spiritual healing, music, and temple administration suit you. "
            "Your life purpose involves purifying karma through selfless service and devotion to the divine."
        ),
    },
    "Rohini": {
        1: (
            "Rohini Pada 1 (Aries navamsha) combines Rohini's fertility with Martian initiative. "
            "You are an assertive creator -- agriculture, fashion launching, product development, and business "
            "startups thrive under your hands. Material abundance comes through bold, beautiful ventures. "
            "Impulsive spending is the main challenge; channelling creative urges into lasting projects builds wealth."
        ),
        2: (
            "Rohini Pada 2 (Taurus navamsha) is Rohini at its most powerful -- Pushkara navamsha in own sign. "
            "You embody Venus-Moon synergy: beauty, wealth, artistic talent, and sensual magnetism. "
            "Agriculture, music, fashion, jewellery, and luxury real estate are ideal careers. "
            "Family life is rich and comfortable. Material and romantic fulfilment come with remarkable ease."
        ),
        3: (
            "Rohini Pada 3 (Gemini navamsha) adds intellectual sparkle to Rohini's creative beauty. "
            "You are a charming communicator with talent in advertising, beauty writing, social media, and trading. "
            "Multiple income sources from creative and commercial activities are indicated. "
            "Restlessness in relationships needs attention; settling down requires conscious commitment."
        ),
        4: (
            "Rohini Pada 4 (Cancer navamsha) deepens Rohini's nurturing quality to its most maternal expression. "
            "You create abundance through emotional connection -- hospitality, food, real estate, and caregiving. "
            "Your home is beautiful and abundantly stocked. Mother's influence is profound and protective. "
            "Emotional security is your primary need; when fulfilled, creativity and wealth flow effortlessly."
        ),
    },
    "Mrigashira": {
        1: (
            "Mrigashira Pada 1 (Leo navamsha) combines the searching nature with regal confidence. "
            "You pursue knowledge and creative expression with dramatic flair. Entertainment, academic research, "
            "fashion, and wildlife exploration suit you. Your curiosity attracts admirers who enjoy your stories. "
            "The challenge is finishing what you start; royal focus on a single pursuit yields the greatest results."
        ),
        2: (
            "Mrigashira Pada 2 (Virgo navamsha) brings analytical precision to the eternal search. "
            "You are a meticulous researcher, naturalist, or scientist who finds beauty in detail. "
            "Textile analysis, botanical research, editing, and pharmaceutical work suit your nature. "
            "Overthinking and excessive caution can delay action; trust your instinct alongside your analysis."
        ),
        3: (
            "Mrigashira Pada 3 (Libra navamsha) directs the search toward beauty, balance, and partnership. "
            "You are a gentle aesthete who seeks harmony in relationships and surroundings. "
            "Interior design, textile art, music, and diplomacy are ideal career paths. "
            "Marriage is an important milestone; the right partner satisfies your restless search for completion."
        ),
        4: (
            "Mrigashira Pada 4 (Scorpio navamsha) intensifies the search into deep, investigative territory. "
            "You probe beneath surfaces and are drawn to mystery, research, and hidden knowledge. "
            "Detective work, archaeological research, mining, and psychological therapy suit your nature. "
            "Obsessive searching can become a trap; knowing when you have found enough is the key to peace."
        ),
    },
    "Ardra": {
        1: (
            "Ardra Pada 1 (Sagittarius navamsha) channels the storm energy toward philosophical wisdom. "
            "You transform suffering into teaching and guide others through their own storms. "
            "Higher education, philosophical counselling, and transformative coaching are your calling. "
            "Life presents extreme challenges early, but your optimism and wisdom ultimately triumph."
        ),
        2: (
            "Ardra Pada 2 (Capricorn navamsha) grounds Ardra's intensity in practical, worldly ambition. "
            "You are a tough, resilient worker who endures hardship without complaint. "
            "Technology, engineering, government service under pressure, and crisis management suit you. "
            "Emotional expression is difficult; learning to communicate feelings prevents internal storms."
        ),
        3: (
            "Ardra Pada 3 (Aquarius navamsha) combines Ardra's transformative power with humanitarian vision. "
            "You are a revolutionary thinker who disrupts outdated systems for collective benefit. "
            "Software development, social reform, electrical engineering, and scientific innovation are ideal. "
            "Detachment from personal ego allows your considerable intellect to serve the greater good."
        ),
        4: (
            "Ardra Pada 4 (Pisces navamsha) softens the storm with compassion and spiritual sensitivity. "
            "You feel the world's suffering deeply and are motivated to heal through creative or spiritual means. "
            "Music therapy, spiritual counselling, charity, and marine research suit your nature. "
            "Emotional overwhelm is your challenge; establishing boundaries protects your sensitive constitution."
        ),
    },
    "Punarvasu": {
        1: (
            "Punarvasu Pada 1 (Aries navamsha) combines renewal energy with initiative and courage. "
            "You bounce back from setbacks with remarkable speed and inspire others through resilient action. "
            "Startup entrepreneurship, coaching, emergency restoration, and sports training suit you. "
            "Your optimism is contagious; you are the person others turn to when hope seems lost."
        ),
        2: (
            "Punarvasu Pada 2 (Taurus navamsha) brings material stability to Punarvasu's renewing nature. "
            "You rebuild financial security after disruption with patient, steady effort. "
            "Real estate restoration, agriculture, banking, and luxury goods renewal suit your talent. "
            "Comfort and beauty return to your life cyclically; each restoration cycle builds greater wealth."
        ),
        3: (
            "Punarvasu Pada 3 (Gemini navamsha) expresses renewal through intellectual communication. "
            "You are a gifted teacher who helps others rediscover lost knowledge and forgotten truths. "
            "Publishing, archival research, language revival, and counselling are ideal careers. "
            "Your versatile mind bounces between subjects, always returning to core wisdom."
        ),
        4: (
            "Punarvasu Pada 4 (Cancer navamsha) is the most nurturing expression -- returning to the cosmic mother. "
            "You create safe emotional havens for yourself and others. Home restoration, family counselling, "
            "nutritional healing, and maternal care are your gifts. Each emotional setback deepens your compassion. "
            "Your spiritual path leads back to the heart, to nurturing, and to unconditional acceptance."
        ),
    },
    "Pushya": {
        1: (
            "Pushya Pada 1 (Leo navamsha) combines nourishing energy with leadership and generosity. "
            "You are a magnanimous provider who nourishes communities through authoritative guidance. "
            "Hospital administration, government welfare, education leadership, and charitable foundations suit you. "
            "Your dignified generosity earns deep respect and lasting influence in society."
        ),
        2: (
            "Pushya Pada 2 (Virgo navamsha) brings meticulous service to Pushya's nourishing nature. "
            "You are a precise caregiver who improves systems of support with analytical skill. "
            "Healthcare management, dietary science, social work planning, and agricultural optimisation are ideal. "
            "Your attention to detail ensures that help reaches those who need it most effectively."
        ),
        3: (
            "Pushya Pada 3 (Libra navamsha) directs nourishment through partnership and social harmony. "
            "You build bridges between people and create nourishing communities through diplomacy and grace. "
            "Marriage counselling, cooperative business, social events management, and arts patronage suit you. "
            "Your greatest nourishment comes through balanced, loving relationships."
        ),
        4: (
            "Pushya Pada 4 (Scorpio navamsha) deepens nourishment into transformative emotional healing. "
            "You are drawn to heal the deepest wounds -- trauma, grief, addiction, and family dysfunction. "
            "Psychotherapy, hospice care, rehabilitation counselling, and regenerative medicine are your calling. "
            "Your own suffering becomes the fuel for profound compassion and therapeutic power."
        ),
    },
    "Ashlesha": {
        1: (
            "Ashlesha Pada 1 (Sagittarius navamsha) channels serpent wisdom into philosophical and ethical teaching. "
            "You understand hidden truths and use this knowledge to guide others toward dharmic living. "
            "Vedic astrology, philosophical counselling, snake venom research, and toxicology suit you. "
            "Your penetrating insight sees through deception, making you a natural guardian of truth."
        ),
        2: (
            "Ashlesha Pada 2 (Capricorn navamsha) grounds serpent intelligence in worldly power structures. "
            "You navigate political and corporate hierarchies with strategic brilliance. "
            "Pharmaceutical industry, political strategy, mining, and intelligence services are ideal fields. "
            "Ambition is intense; ethical boundaries prevent your power from becoming self-destructive."
        ),
        3: (
            "Ashlesha Pada 3 (Aquarius navamsha) combines Ashlesha's cunning with humanitarian innovation. "
            "You devise unconventional solutions to deep-rooted problems others cannot even perceive. "
            "Genetic research, environmental toxicology, social hacking for good, and cybersecurity suit you. "
            "Your genius operates best when directed toward collective benefit rather than personal gain."
        ),
        4: (
            "Ashlesha Pada 4 (Pisces navamsha) dissolves the serpent's grip through spiritual surrender. "
            "You carry deep karmic patterns that seek resolution through devotion and compassion. "
            "Kundalini yoga, spiritual healing, marine biology, and addiction counselling are your paths. "
            "Release of control and trust in the divine current transforms your powerful serpent energy into moksha."
        ),
    },
    "Magha": {
        1: (
            "Magha Pada 1 (Aries navamsha) combines royal ancestry energy with pioneering action. "
            "You are a born leader who carries ancestral authority into new territories. "
            "Government leadership, military command, corporate founding, and dynasty building suit you. "
            "Your connection to ancestors is palpable -- pitru karma shapes major life decisions and turning points."
        ),
        2: (
            "Magha Pada 2 (Taurus navamsha) directs royal energy toward wealth preservation and legacy building. "
            "You protect and grow family assets with unwavering dedication. "
            "Heritage management, luxury brands, ancestral property, and traditional crafts suit you. "
            "Material legacy and cultural preservation are sacred duties you fulfil with dignity."
        ),
        3: (
            "Magha Pada 3 (Gemini navamsha) channels ancestral wisdom through communication and teaching. "
            "You are a storyteller who preserves family history and cultural narratives for future generations. "
            "Genealogy, historical writing, cultural documentation, and ancestral research are ideal pursuits. "
            "Your intellect connects past wisdom with present application, bridging generations."
        ),
        4: (
            "Magha Pada 4 (Cancer navamsha) deepens the ancestral connection to its most emotional and nurturing level. "
            "You feel your ancestors' presence and channel their blessings into family care. "
            "Temple trust management, family counselling, maternal health, and ancestral rituals are your domain. "
            "Home is your throne -- a place where past and present merge in loving continuity."
        ),
    },
    "Purva Phalguni": {
        1: (
            "Purva Phalguni Pada 1 (Leo navamsha) amplifies creative, royal, and romantic energy to its peak. "
            "You are a star performer -- charismatic, generous, and meant for the spotlight. "
            "Entertainment, fine arts, luxury hospitality, and creative direction are your domains. "
            "Love and romance are central themes; your heart's desires shape your life's grandest chapters."
        ),
        2: (
            "Purva Phalguni Pada 2 (Virgo navamsha) refines the pleasure principle with practical discernment. "
            "You create beauty with precision and manage luxury enterprises with analytical skill. "
            "Event planning, fashion quality control, cosmetic formulation, and arts administration suit you. "
            "Balancing indulgence with discipline is your lifelong theme; when achieved, success flows abundantly."
        ),
        3: (
            "Purva Phalguni Pada 3 (Libra navamsha) expresses love and creativity through partnership and social grace. "
            "You are the consummate host, diplomat, and social connector who brings people together in joy. "
            "Wedding planning, social media, luxury partnerships, and artistic collaboration are ideal. "
            "Your happiest moments are shared ones; partnership in both love and business elevates your life."
        ),
        4: (
            "Purva Phalguni Pada 4 (Scorpio navamsha) takes pleasure into transformative and intense depths. "
            "Your creative and romantic life is marked by intensity, passion, and occasional upheaval. "
            "Tantric arts, transformative therapy, deep relationship work, and crisis-born creativity suit you. "
            "You discover your greatest artistic power through emotional catharsis and fearless self-expression."
        ),
    },
    "Uttara Phalguni": {
        1: (
            "Uttara Phalguni Pada 1 (Sagittarius navamsha) combines patronage with wisdom and philosophical purpose. "
            "You are a generous benefactor who supports education, religion, and ethical enterprise. "
            "University endowment, dharmic leadership, publishing, and philanthropic management suit you. "
            "Your life's purpose is to use Sun-ruled authority to uplift others through wisdom and generosity."
        ),
        2: (
            "Uttara Phalguni Pada 2 (Capricorn navamsha) channels patronage energy into disciplined institution-building. "
            "You create lasting structures -- organisations, trusts, and enterprises that outlive you. "
            "Government administration, corporate law, institutional reform, and estate management are ideal. "
            "Patience and structure transform your generous impulses into permanent societal contributions."
        ),
        3: (
            "Uttara Phalguni Pada 3 (Aquarius navamsha) directs Uttara Phalguni's helping nature toward social innovation. "
            "You build networks of support that reach underserved communities through progressive methods. "
            "Social enterprise, technology for good, cooperative housing, and innovative welfare programs suit you. "
            "Your philanthropic vision is ahead of its time; persistence eventually brings recognition."
        ),
        4: (
            "Uttara Phalguni Pada 4 (Pisces navamsha) dissolves the patron's ego into selfless spiritual service. "
            "You give without expectation and find deepest fulfilment in anonymous acts of kindness. "
            "Ashram management, spiritual retreat centres, hospital charity, and devotional arts are your calling. "
            "Your generous heart becomes a channel for divine grace when personal ambition is transcended."
        ),
    },
    "Hasta": {
        1: (
            "Hasta Pada 1 (Aries navamsha) directs Hasta's manual skill and cunning toward bold enterprise. "
            "You are a quick-handed entrepreneur -- skilled in crafts, surgery, and mechanical innovation. "
            "Surgical specialisation, precision engineering, gem-cutting, and artisan entrepreneurship suit you. "
            "Your hands are blessed; what you make or fix becomes more valuable through your touch."
        ),
        2: (
            "Hasta Pada 2 (Taurus navamsha) brings Hasta's dexterity into the realm of material beauty and value. "
            "You create tangible wealth through skilled craftsmanship and aesthetic production. "
            "Jewellery making, pottery, massage therapy, cooking, and luxury crafts are ideal careers. "
            "Your steady hands produce works of lasting beauty that appreciate in value over time."
        ),
        3: (
            "Hasta Pada 3 (Gemini navamsha) combines manual skill with intellectual versatility and communication. "
            "You are equally adept with hands and words -- writing, sign language, typing, and gesture-based arts. "
            "Calligraphy, technical writing, data entry systems, and hand-based healing modalities suit you. "
            "Your ability to translate thought into precise physical action makes you exceptionally productive."
        ),
        4: (
            "Hasta Pada 4 (Cancer navamsha) nurtures through Hasta's healing touch and emotional sensitivity. "
            "You are a natural healer whose hands carry soothing, maternal energy. "
            "Nursing, midwifery, infant massage, cooking therapy, and emotionally supportive bodywork suit you. "
            "Your home cooking and handmade gifts carry a quality of love that commercially produced goods cannot match."
        ),
    },
    "Chitra": {
        1: (
            "Chitra Pada 1 (Leo navamsha) amplifies the celestial architect's creative fire into dramatic self-expression. "
            "You are a visionary artist whose creations demand attention and admiration. "
            "Architecture, fashion design, film direction, and monumental sculpture are ideal fields. "
            "Your creative ego is powerful -- channelling it into magnificent works rather than personal drama is key."
        ),
        2: (
            "Chitra Pada 2 (Virgo navamsha) refines Chitra's creative impulse with Mercury's analytical precision. "
            "You are a detail-oriented creator who achieves perfection through painstaking refinement. "
            "Industrial design, technical illustration, precision engineering, and medical device design suit you. "
            "Your creations work flawlessly because you obsess over every detail until it meets your exacting standards."
        ),
        3: (
            "Chitra Pada 3 (Libra navamsha) directs the celestial architect toward beauty, partnership, and social harmony. "
            "You create beauty that brings people together -- public spaces, fashion, music, and social platforms. "
            "Interior architecture, event design, fashion styling, and arts curation are your talents. "
            "Collaboration with equally talented partners produces your most stunning work."
        ),
        4: (
            "Chitra Pada 4 (Scorpio navamsha) takes Chitra's creative power into intense, transformative territory. "
            "You create works that disturb, transform, and provoke deep emotional responses. "
            "Tattoo artistry, reconstructive surgery, avant-garde art, and architectural renovation suit you. "
            "Your creativity reaches its peak when you work with materials others consider broken or discarded."
        ),
    },
    "Swati": {
        1: (
            "Swati Pada 1 (Sagittarius navamsha) combines independence with philosophical purpose and ethical conduct. "
            "You are a free-spirited seeker of truth who travels widely in pursuit of wisdom. "
            "International trade, philosophical writing, travel industry, and diplomatic service suit you. "
            "Your independence is not rebellion but a genuine quest for higher meaning and broader horizons."
        ),
        2: (
            "Swati Pada 2 (Capricorn navamsha) grounds Swati's restless independence in disciplined worldly achievement. "
            "You are a self-made professional who builds success through patient, solitary effort. "
            "Wind energy, aviation maintenance, corporate consulting, and independent business suit you. "
            "Financial discipline transforms your freedom-loving nature into lasting prosperity."
        ),
        3: (
            "Swati Pada 3 (Aquarius navamsha) amplifies Swati's independence into social innovation and networking. "
            "You connect diverse groups and ideas, creating unexpected synergies. "
            "Technology startups, social networking, cooperative ventures, and progressive advocacy suit you. "
            "Your greatest achievements come through empowering others' independence rather than centralising power."
        ),
        4: (
            "Swati Pada 4 (Pisces navamsha) dissolves Swati's fierce independence into spiritual surrender. "
            "You learn that true freedom comes through releasing attachment rather than accumulating options. "
            "Spiritual retreat facilitation, music, oceanic research, and pilgrimage organising suit you. "
            "Your restless wind settles into the vast ocean of consciousness, finding peace in surrender."
        ),
    },
    "Vishakha": {
        1: (
            "Vishakha Pada 1 (Aries navamsha) ignites the goal-focused energy with fiery initiative. "
            "You are a relentless achiever who attacks targets with singular military precision. "
            "Competitive sports, military strategy, surgical specialisation, and executive leadership suit you. "
            "Your determination is unmatched; you define a goal and will not rest until it is conquered."
        ),
        2: (
            "Vishakha Pada 2 (Taurus navamsha) directs Vishakha's goal-orientation toward material wealth and stability. "
            "You pursue financial targets with unwavering patience and practical strategy. "
            "Banking, agricultural empire building, luxury brand development, and real estate suit you. "
            "Your determination combined with Venusian patience creates substantial, lasting wealth."
        ),
        3: (
            "Vishakha Pada 3 (Gemini navamsha) combines single-minded pursuit with intellectual versatility. "
            "You are a strategic communicator who convinces others to support your vision. "
            "Political campaigning, sales management, media strategy, and debate competition suit you. "
            "Your ability to articulate goals and rally support makes you a formidable force in any arena."
        ),
        4: (
            "Vishakha Pada 4 (Cancer navamsha) channels Vishakha's determination toward emotional and family goals. "
            "You pursue domestic security and family well-being with the same intensity others reserve for career. "
            "Family business leadership, maternal healthcare, home building, and heritage preservation suit you. "
            "Your deepest fulfilment comes when professional success translates into family prosperity."
        ),
    },
    "Anuradha": {
        1: (
            "Anuradha Pada 1 (Leo navamsha) combines devotion and friendship with regal self-expression. "
            "You are a loyal leader whose authority comes from genuine love for your people. "
            "Organisational leadership, diplomatic corps, creative direction, and social enterprise suit you. "
            "Your devotion to friends and causes inspires fierce loyalty in return."
        ),
        2: (
            "Anuradha Pada 2 (Virgo navamsha) brings analytical precision to Anuradha's devotional nature. "
            "You serve your chosen cause with meticulous attention and practical competence. "
            "Data-driven social work, health service coordination, religious scholarship, and NGO management suit you. "
            "Your devotion is expressed through perfect execution rather than emotional display."
        ),
        3: (
            "Anuradha Pada 3 (Libra navamsha) directs devotion through partnership, beauty, and social harmony. "
            "You are a bridge-builder whose friendships span diverse groups and cultures. "
            "International relations, arts patronage, marriage counselling, and cultural exchange suit you. "
            "Your greatest spiritual growth comes through devoted, balanced partnership."
        ),
        4: (
            "Anuradha Pada 4 (Scorpio navamsha) intensifies devotion into profound, transformative spiritual practice. "
            "You are drawn to mystery traditions, deep meditation, and unwavering spiritual commitment. "
            "Tantra, psychotherapy, mystery school teaching, and regenerative medicine suit you. "
            "Your devotion to truth takes you into the darkest corners, where you find the brightest light."
        ),
    },
    "Jyeshtha": {
        1: (
            "Jyeshtha Pada 1 (Sagittarius navamsha) channels elder authority into philosophical leadership. "
            "You are a wise ruler who earns respect through ethical conduct and expansive vision. "
            "University administration, judicial authority, religious leadership, and philanthropic direction suit you. "
            "Your protective nature extends beyond family to encompass entire communities."
        ),
        2: (
            "Jyeshtha Pada 2 (Capricorn navamsha) grounds Jyeshtha's power in practical, structural authority. "
            "You are a disciplined administrator who builds lasting institutions through patient effort. "
            "Government bureaucracy, corporate governance, infrastructure planning, and elder care management suit you. "
            "Your authority grows with age; the latter half of life is far more powerful than the first."
        ),
        3: (
            "Jyeshtha Pada 3 (Aquarius navamsha) transforms Jyeshtha's hierarchical power into democratic leadership. "
            "You challenge outdated power structures while maintaining respect for genuine authority. "
            "Social reform, technology governance, cooperative management, and progressive politics suit you. "
            "Your greatest legacy is dismantling unjust systems while preserving what genuinely serves humanity."
        ),
        4: (
            "Jyeshtha Pada 4 (Pisces navamsha) dissolves worldly power into spiritual authority and selfless service. "
            "You learn that true authority comes from surrender to the divine rather than worldly dominance. "
            "Ashram leadership, spiritual counselling, charitable hospital management, and prayer suit you. "
            "The power you release from ego returns multiplied as spiritual grace and inner peace."
        ),
    },
    "Mula": {
        1: (
            "Mula Pada 1 (Aries navamsha) combines root-destruction energy with fiery initiative and courage. "
            "You are a fearless destroyer of what no longer serves -- old systems, outdated beliefs, toxic patterns. "
            "Crisis management, demolition engineering, root cause analysis, and revolutionary leadership suit you. "
            "Your life begins with destruction of the old so that something authentic can emerge."
        ),
        2: (
            "Mula Pada 2 (Taurus navamsha) grounds Mula's destructive power in practical, material rebuilding. "
            "After uprooting the old, you rebuild with patient attention to quality and lasting value. "
            "Soil science, dental surgery, foundation engineering, and heritage restoration suit you. "
            "Your unique gift is transforming destruction into creation -- what you rebuild endures."
        ),
        3: (
            "Mula Pada 3 (Gemini navamsha) channels root energy through intellectual inquiry and communication. "
            "You question fundamental assumptions and communicate disruptive truths with clarity. "
            "Investigative journalism, linguistic etymology, genetic research, and philosophical deconstruction suit you. "
            "Your mind goes to the root of every question; superficial answers are intolerable."
        ),
        4: (
            "Mula Pada 4 (Cancer navamsha) directs Mula's root energy toward emotional and ancestral healing. "
            "You are drawn to heal family trauma, ancestral patterns, and deep-seated emotional wounds. "
            "Family therapy, genealogical healing, real estate clearing, and maternal lineage work suit you. "
            "Your most profound transformation comes through returning to your roots and healing them from within."
        ),
    },
    "Purva Ashadha": {
        1: (
            "Purva Ashadha Pada 1 (Leo navamsha) combines invincible energy with creative, regal self-expression. "
            "You declare your intentions boldly and follow through with unwavering commitment to victory. "
            "Motivational speaking, political campaigning, film production, and sports coaching suit you. "
            "Your confidence is infectious; you are the person others follow into battle knowing victory is certain."
        ),
        2: (
            "Purva Ashadha Pada 2 (Virgo navamsha) brings analytical strategy to Purva Ashadha's invincibility. "
            "You win through superior preparation, attention to detail, and methodical execution. "
            "Military intelligence, surgical excellence, quality assurance, and research triumph suit you. "
            "Your victories are built on data and precision; nothing is left to chance."
        ),
        3: (
            "Purva Ashadha Pada 3 (Libra navamsha) achieves victory through diplomacy, partnership, and grace. "
            "You win hearts rather than battles and achieve your goals through charm and strategic alliances. "
            "Diplomatic service, legal advocacy, peace negotiation, and luxury brand ambassadorship suit you. "
            "Your invincibility comes from making allies of former adversaries."
        ),
        4: (
            "Purva Ashadha Pada 4 (Scorpio navamsha) takes invincibility into the deepest, most transformative battles. "
            "You conquer fear, death, and the darkest challenges that would destroy lesser souls. "
            "Trauma surgery, crisis therapy, undercover investigation, and spiritual warfare suit you. "
            "Your greatest victory is over your own shadow -- once achieved, no external challenge can defeat you."
        ),
    },
    "Uttara Ashadha": {
        1: (
            "Uttara Ashadha Pada 1 (Sagittarius navamsha) amplifies the universal soldier's wisdom and purpose. "
            "You fight for dharma with philosophical conviction and international perspective. "
            "International law, humanitarian aid, educational reform, and ethical leadership suit you. "
            "Your authority is recognised universally because it serves truth rather than personal power."
        ),
        2: (
            "Uttara Ashadha Pada 2 (Capricorn navamsha) is Uttara Ashadha at its most powerful -- Sun exalted potential. "
            "You build structures of authority that serve universal justice and lasting governance. "
            "Government founding, constitutional law, institutional leadership, and national service suit you. "
            "Your discipline and moral authority place you in positions of permanent, respected power."
        ),
        3: (
            "Uttara Ashadha Pada 3 (Aquarius navamsha) directs universal authority toward humanitarian innovation. "
            "You reform systems to serve all people equally, using technology and progressive thinking. "
            "International development, technology policy, democratic reform, and scientific governance suit you. "
            "Your leadership style is inclusive and forward-looking; hierarchy serves function, not ego."
        ),
        4: (
            "Uttara Ashadha Pada 4 (Pisces navamsha) dissolves worldly authority into spiritual universality. "
            "You recognise that the highest authority belongs to the divine and serve as its humble instrument. "
            "Spiritual leadership, interfaith dialogue, charitable governance, and selfless public service suit you. "
            "Your final victory is not over others but over your own attachment to power and recognition."
        ),
    },
    "Shravana": {
        1: (
            "Shravana Pada 1 (Aries navamsha) combines deep listening ability with bold, initiative-driven action. "
            "You hear what others miss and act on it before anyone else can react. "
            "Intelligence gathering, strategic consulting, emergency dispatch, and audio engineering suit you. "
            "Your listening is not passive but active -- you hear and act with warrior-like precision."
        ),
        2: (
            "Shravana Pada 2 (Taurus navamsha) brings Shravana's listening ability into practical, wealth-generating activity. "
            "You translate what you hear in the market into profitable, stable ventures. "
            "Music production, market research, agricultural advisory, and acoustic engineering suit you. "
            "Your ear for quality and value makes you an exceptional judge of investments and opportunities."
        ),
        3: (
            "Shravana Pada 3 (Gemini navamsha) amplifies the listening-communication loop to extraordinary levels. "
            "You are a master interviewer, translator, and connector who bridges different worlds through words. "
            "Journalism, language interpretation, counselling, and podcast production suit you. "
            "Your ability to truly hear and then clearly articulate makes you invaluable in any field requiring mediation."
        ),
        4: (
            "Shravana Pada 4 (Cancer navamsha) deepens listening into emotional and intuitive hearing. "
            "You hear the unspoken -- feelings, needs, and ancestral whispers guide your actions. "
            "Therapy, maternal counselling, music therapy, and intuitive healing suit you. "
            "Your home is a place of deep listening where family members feel truly heard and understood."
        ),
    },
    "Dhanishta": {
        1: (
            "Dhanishta Pada 1 (Leo navamsha) combines rhythmic wealth energy with dramatic, regal creative expression. "
            "You are a prosperous performer whose rhythm attracts abundance and admiration. "
            "Music performance, entertainment industry leadership, sports drumming, and gold trading suit you. "
            "Your natural sense of timing makes you lucky in speculation and performance arts."
        ),
        2: (
            "Dhanishta Pada 2 (Virgo navamsha) refines Dhanishta's rhythm and wealth through analytical precision. "
            "You build wealth through systematic, rhythmic effort -- consistent saving and measured investment. "
            "Musical instrument crafting, financial auditing, rhythmic therapy, and precision manufacturing suit you. "
            "Your disciplined approach to wealth ensures steady growth without speculative risk."
        ),
        3: (
            "Dhanishta Pada 3 (Libra navamsha) channels rhythmic energy into social harmony and partnership wealth. "
            "You create prosperity through collaborative ventures and socially harmonious enterprises. "
            "Wedding music, social event management, cooperative banking, and arts partnership suit you. "
            "Your sense of rhythm extends to relationships -- you know when to give, receive, and balance."
        ),
        4: (
            "Dhanishta Pada 4 (Scorpio navamsha) intensifies the rhythm into transformative, powerful beats. "
            "You are drawn to intense musical forms, deep financial markets, and hidden wealth channels. "
            "Percussion mastery, investment banking, insurance, and inheritance management suit you. "
            "Your rhythm penetrates surfaces; you find wealth and power where others see only noise."
        ),
    },
    "Shatabhisha": {
        1: (
            "Shatabhisha Pada 1 (Sagittarius navamsha) combines the hundred healers' energy with philosophical wisdom. "
            "You are a visionary healer who understands the broader principles behind specific cures. "
            "Medical research, public health policy, pharmaceutical philosophy, and holistic education suit you. "
            "Your healing extends beyond individuals to entire populations through wise, principled practice."
        ),
        2: (
            "Shatabhisha Pada 2 (Capricorn navamsha) grounds the healing energy in practical, institutional structures. "
            "You build hospitals, clinics, and healthcare systems that endure and serve reliably. "
            "Hospital administration, pharmaceutical manufacturing, public health infrastructure, and medical governance suit you. "
            "Your disciplined approach to healing ensures consistent, accessible care for communities."
        ),
        3: (
            "Shatabhisha Pada 3 (Aquarius navamsha) is Shatabhisha at full power -- the innovative healer-scientist. "
            "You invent new healing technologies, medicines, and methodologies that transform healthcare. "
            "Medical technology, space medicine, electrical therapies, and scientific research suit you. "
            "Your unique healing insights come from unconventional thinking and willingness to experiment."
        ),
        4: (
            "Shatabhisha Pada 4 (Pisces navamsha) dissolves the healer's science into spiritual and intuitive medicine. "
            "You heal through prayer, energy, water therapies, and compassionate presence. "
            "Spiritual healing, hydrotherapy, music medicine, and charitable healthcare suit you. "
            "Your most powerful healing occurs when you surrender scientific ego to compassionate intuition."
        ),
    },
    "Purva Bhadrapada": {
        1: (
            "Purva Bhadrapada Pada 1 (Aries navamsha) ignites the one-footed goat's fire into explosive spiritual action. "
            "You are a fierce spiritual warrior who attacks ignorance and injustice with zealous passion. "
            "Social revolution, spiritual combat, emergency spiritual counselling, and fire rituals suit you. "
            "Your intensity burns away impurities; what survives your fire is genuinely sacred."
        ),
        2: (
            "Purva Bhadrapada Pada 2 (Taurus navamsha) grounds the intense spiritual fire in practical, material expression. "
            "You fund spiritual causes, build temples, and create material foundations for transcendent work. "
            "Charitable trust management, temple construction, spiritual commerce, and occult investment suit you. "
            "Your wealth serves your spiritual mission; money is a tool for transformation, not accumulation."
        ),
        3: (
            "Purva Bhadrapada Pada 3 (Gemini navamsha) channels transformative fire through words and communication. "
            "You are a powerful orator whose words can inflame or illuminate depending on your maturity. "
            "Fiery journalism, spiritual writing, transformative coaching, and political speechwriting suit you. "
            "Your words carry the power to change minds and hearts; choose them with care."
        ),
        4: (
            "Purva Bhadrapada Pada 4 (Cancer navamsha) brings the spiritual fire into emotional and domestic realms. "
            "You transform family karma through intense emotional processing and spiritual practice at home. "
            "Family healing, ancestral ritual, home-based spiritual practice, and maternal spiritual guidance suit you. "
            "Your home becomes an ashram; emotional intensity is the fuel for your family's spiritual evolution."
        ),
    },
    "Uttara Bhadrapada": {
        1: (
            "Uttara Bhadrapada Pada 1 (Leo navamsha) combines deep serpent wisdom with regal, generous self-expression. "
            "You are a wise elder whose depth of understanding inspires respect and devotion. "
            "Spiritual leadership, Vedic teaching, charitable governance, and wisdom literature suit you. "
            "Your calm authority comes from genuine inner depth rather than worldly power."
        ),
        2: (
            "Uttara Bhadrapada Pada 2 (Virgo navamsha) brings analytical precision to Uttara Bhadrapada's deep wisdom. "
            "You are a meticulous scholar who organises spiritual knowledge into accessible, practical systems. "
            "Religious scholarship, scriptural translation, monastic administration, and ethical auditing suit you. "
            "Your detailed spiritual knowledge serves others by making the profound simple and applicable."
        ),
        3: (
            "Uttara Bhadrapada Pada 3 (Libra navamsha) channels deep wisdom through balanced partnership and social grace. "
            "You counsel others with compassionate fairness and create harmony in turbulent environments. "
            "Marriage counselling, interfaith dialogue, judicial mediation, and spiritual partnership suit you. "
            "Your wisdom is most effective when shared through loving, balanced relationships."
        ),
        4: (
            "Uttara Bhadrapada Pada 4 (Scorpio navamsha) takes the deep serpent into the most intense, transformative waters. "
            "You are drawn to the deepest mysteries of existence -- birth, death, and what lies beyond. "
            "Hospice spiritual care, death midwifery, kundalini research, and mystical practice suit you. "
            "Your spiritual depth is unfathomable; few can accompany you to the places you naturally go."
        ),
    },
    "Revati": {
        1: (
            "Revati Pada 1 (Sagittarius navamsha) combines Revati's compassionate journey-end with philosophical wisdom. "
            "You guide others to their destination -- physical, emotional, or spiritual -- with wise counsel. "
            "Travel guidance, spiritual pilgrimage organisation, philosophical counselling, and end-of-life care suit you. "
            "Your presence brings comfort at life's major transitions and journeys' ends."
        ),
        2: (
            "Revati Pada 2 (Capricorn navamsha) grounds Revati's gentle, final-journey energy in practical service. "
            "You organise the practical details of life's transitions with caring efficiency. "
            "Estate planning, funeral direction, retirement counselling, and heritage preservation suit you. "
            "Your disciplined kindness ensures that endings are handled with dignity and completeness."
        ),
        3: (
            "Revati Pada 3 (Aquarius navamsha) channels compassion into innovative, collective care systems. "
            "You build networks of support that ensure no one faces life's final chapters alone. "
            "Hospice innovation, elder-care technology, community end-of-life services, and progressive charity suit you. "
            "Your humanitarian vision transforms how society cares for its most vulnerable members."
        ),
        4: (
            "Revati Pada 4 (Pisces navamsha) is the final expression of the entire zodiac -- complete surrender to the divine. "
            "You embody pure compassion, artistic sensitivity, and readiness for spiritual liberation. "
            "Devotional music, spiritual art, meditation mastery, and selfless service are your domain. "
            "Your soul is completing its journey; peace, surrender, and divine love are your natural state."
        ),
    },
}


# ============================================================
# 12. ASCENDANT_PERSONALITY -- Extended Profiles per Ascendant
# ============================================================

ASCENDANT_PERSONALITY: Dict[str, Dict[str, str]] = {
    "Aries": {
        "overview": (
            "The Aries ascendant stamps the personality with Mars energy -- courageous, impulsive, and fiercely "
            "independent. You are a natural pioneer who leads from the front without waiting for permission. "
            "First impressions are of someone direct, energetic, and perhaps slightly intimidating. "
            "You live in the present moment, making quick decisions and taking immediate action. "
            "Challenges excite rather than frighten you; boredom is your true enemy. "
            "Your life story is one of constant new beginnings, bold initiatives, and hard-won victories."
        ),
        "health_tendencies": (
            "The head, brain, and adrenal system are your most sensitive areas. Migraines, fevers, "
            "and inflammatory conditions flare under stress. Your metabolism runs fast, burning through "
            "energy quickly -- regular meals and adequate sleep prevent burnout. Physical activity is "
            "not optional but essential for maintaining both mental and physical equilibrium."
        ),
        "temperament": (
            "Quick to anger and equally quick to forgive, your emotional responses are intense but brief. "
            "You cannot hold grudges for long because your attention naturally moves forward. "
            "Patience is your lifelong lesson; learning to wait without losing enthusiasm "
            "transforms your impulsive nature into strategic boldness."
        ),
        "physical_appearance": (
            "Medium to tall stature with an athletic, lean build and quick, purposeful movements. "
            "The forehead is typically prominent, and the eyes carry a sharp, alert expression. "
            "A scar or birthmark on the face or head is commonly observed. "
            "You age well, maintaining physical vitality longer than most ascendant types."
        ),
        "career_aptitude": (
            "You excel in roles requiring initiative, courage, and independent decision-making. "
            "Military, surgery, sports, entrepreneurship, emergency services, and engineering are ideal. "
            "Subordinate roles without autonomy drain your spirit; you need freedom to lead and act. "
            "Self-employment or a position with significant independence produces your best work."
        ),
    },
    "Taurus": {
        "overview": (
            "The Taurus ascendant radiates stability, sensuality, and quiet strength under Venus's gracious rule. "
            "You move through life at a measured, deliberate pace that others may mistake for slowness. "
            "First impressions are of warmth, reliability, and an undeniable appreciation for beauty. "
            "Material security is not mere desire but a psychological necessity for your peace of mind. "
            "Loyalty runs deep -- once you commit, whether to a person, project, or principle, you are unwavering. "
            "Your life builds slowly toward impressive material and emotional wealth that endures across generations."
        ),
        "health_tendencies": (
            "The throat, thyroid, and neck are your most vulnerable areas. Tonsillitis, thyroid imbalance, "
            "and cervical spondylosis are conditions to watch. Your metabolism tends toward slowness, "
            "making weight management a lifelong consideration. Rich food and sedentary habits are your "
            "health enemies; regular walking and dietary moderation are your best medicines."
        ),
        "temperament": (
            "Calm, patient, and slow to anger, but once provoked your fury is formidable and unforgettable. "
            "You process emotions slowly and thoroughly, rarely making impulsive emotional decisions. "
            "Stubbornness is your shadow side -- an inability to change course even when the evidence demands it. "
            "Learning flexibility without losing your grounded stability is the Taurus ascendant's emotional mastery."
        ),
        "physical_appearance": (
            "Strong, well-proportioned body with broad shoulders and a thick, attractive neck. "
            "The face is pleasant with large, expressive eyes and full lips. Voice is typically melodious. "
            "There is a natural elegance to your movement despite a solid build. "
            "You tend toward weight gain in middle age, particularly around the midsection."
        ),
        "career_aptitude": (
            "You thrive in careers offering stability, beauty, and tangible rewards. "
            "Banking, agriculture, real estate, luxury goods, hospitality, music, and fine arts are ideal. "
            "You need time to do things properly and produce your best work in unhurried environments. "
            "Roles involving financial management, aesthetic judgement, or resource stewardship leverage your natural gifts."
        ),
    },
    "Gemini": {
        "overview": (
            "The Gemini ascendant electrifies the personality with Mercury's quicksilver intelligence. "
            "You process information at extraordinary speed and communicate with wit and charm. "
            "First impressions are of someone youthful, curious, and endlessly interesting to talk to. "
            "Duality is your nature -- you genuinely hold multiple perspectives simultaneously. "
            "Social connections are your currency; you know everyone and can bridge any two worlds. "
            "Your life is a tapestry of varied experiences, multiple careers, and an ever-expanding network of knowledge."
        ),
        "health_tendencies": (
            "The nervous system, lungs, arms, and hands are your vulnerable areas. Anxiety, insomnia, "
            "bronchitis, and carpal tunnel syndrome are conditions to watch. Your mind's restless activity "
            "can exhaust the body; nervous exhaustion is a real risk. Regular breathing exercises, digital "
            "detox periods, and calming routines counterbalance your naturally overactive nervous system."
        ),
        "temperament": (
            "Intellectually restless, socially charming, and emotionally variable -- your moods shift with your thoughts. "
            "You avoid emotional depth not from coldness but from an instinctive preference for lightness and movement. "
            "Boredom is genuinely painful to you; you need constant mental stimulation to feel alive. "
            "Developing emotional consistency without losing your brilliant adaptability is your growth edge."
        ),
        "physical_appearance": (
            "Slim, tall build with long limbs and expressive, animated hand gestures. "
            "The face is youthful with bright, darting eyes that reflect constant mental activity. "
            "Your appearance tends to be fashionable and current, as you naturally adopt new styles. "
            "You maintain a youthful look well into middle age, appearing younger than your years."
        ),
        "career_aptitude": (
            "You excel in careers requiring communication, intellectual versatility, and social networking. "
            "Journalism, teaching, marketing, trading, IT, translation, and public relations are ideal fields. "
            "Monotonous, routine-heavy roles are unbearable; you need variety and mental challenges. "
            "Portfolio careers with multiple simultaneous projects suit your nature better than a single lifelong role."
        ),
    },
    "Cancer": {
        "overview": (
            "The Cancer ascendant wraps the personality in the Moon's protective, nurturing, and emotionally rich energy. "
            "You approach the world through feeling rather than thinking, absorbing emotional atmospheres instantly. "
            "First impressions are of warmth, sensitivity, and a caring nature that puts others at ease. "
            "Home and family are not just priorities but the very foundation of your identity and well-being. "
            "Memory is your superpower -- you remember kindnesses and slights with photographic emotional detail. "
            "Your life builds around creating and protecting a secure, loving environment for yourself and those you cherish."
        ),
        "health_tendencies": (
            "The stomach, chest, breasts, and lymphatic system are your sensitive areas. Acidity, "
            "digestive disorders, water retention, and hormonal imbalances follow emotional cycles. "
            "Your health directly reflects your emotional state -- stress goes straight to the stomach. "
            "Warm, home-cooked meals, emotional security, and regular emotional expression are your best medicines."
        ),
        "temperament": (
            "Deeply emotional, protective, and occasionally moody -- your emotional landscape is as changeable as the Moon. "
            "You care profoundly for loved ones and will sacrifice enormously to protect them. "
            "Retreating into your shell when hurt is instinctive; learning to communicate pain rather than withdraw "
            "is the Cancer ascendant's great emotional breakthrough."
        ),
        "physical_appearance": (
            "Medium height with a round, pleasant face and large, expressive, often watery eyes. "
            "The chest area is typically broad or prominent. Skin is fair and sensitive to the sun. "
            "Body type tends toward soft and curvy rather than angular. "
            "Your facial expressions are remarkably transparent, reflecting every inner emotion."
        ),
        "career_aptitude": (
            "You excel in careers involving nurturing, emotional intelligence, and domestic arts. "
            "Hospitality, nursing, cooking, real estate, counselling, and maternal healthcare are ideal. "
            "You work best in environments that feel like extended family rather than cold corporate settings. "
            "Entrepreneurship in food, home goods, or childcare leverages your natural protective instincts."
        ),
    },
    "Leo": {
        "overview": (
            "The Leo ascendant blazes with the Sun's majestic, generous, and commanding energy. "
            "You radiate warmth and confidence that naturally draws others into your orbit. "
            "First impressions are of someone dignified, warm-hearted, and unmistakably present. "
            "Leadership is not something you pursue -- it follows you because people instinctively look to you for direction. "
            "Recognition and appreciation are as essential to your well-being as food and water. "
            "Your life is a grand narrative of creative expression, generous service, and the pursuit of personal significance."
        ),
        "health_tendencies": (
            "The heart, spine, and eyes are your most vulnerable areas. Blood pressure, cardiac issues, "
            "and spinal problems require monitoring especially after age 40. Your vitality is naturally strong "
            "but can be depleted by emotional wounds to your pride. Cardiovascular exercise, avoiding excessive "
            "anger, and receiving genuine appreciation are essential to your long-term health."
        ),
        "temperament": (
            "Generous, warm, and magnanimous in your natural state, but wounded pride can trigger dramatic anger. "
            "You need to be appreciated -- not from vanity but from a deep need to know your light matters. "
            "Flattery can deceive you because you want to believe the best about yourself. "
            "Learning humility without losing your magnificent confidence is the Leo ascendant's mastery."
        ),
        "physical_appearance": (
            "Commanding presence with a broad chest, strong shoulders, and often a mane-like quality to the hair. "
            "The face is broad with a warm, radiant smile. Eyes are bright and engaging. "
            "Your posture is naturally upright and regal; you carry yourself with unconscious dignity. "
            "You tend to dress with flair, favouring bold colours and statement pieces."
        ),
        "career_aptitude": (
            "You excel in careers requiring leadership, creative direction, and public presence. "
            "Politics, entertainment, senior management, education leadership, and creative arts are ideal. "
            "You need a role that offers both authority and recognition; behind-the-scenes work frustrates you. "
            "Government service, theatre direction, and positions with ceremonial significance satisfy your Sun-ruled nature."
        ),
    },
    "Virgo": {
        "overview": (
            "The Virgo ascendant refines the personality with Mercury's analytical, service-oriented, and perfectionist energy. "
            "You see the world in terms of systems, details, and opportunities for improvement. "
            "First impressions are of someone neat, intelligent, and observant with a quiet, unassuming manner. "
            "Service to others is not a burden but your natural mode of expression and source of fulfilment. "
            "You notice what everyone else misses -- the typo, the misaligned beam, the overlooked symptom. "
            "Your life is a continuous process of refinement, improvement, and the quiet pursuit of perfection."
        ),
        "health_tendencies": (
            "The intestines, digestive system, and nervous system are your sensitive areas. IBS, food allergies, "
            "and anxiety-related digestive issues are common. Hypochondria can amplify minor symptoms. "
            "Your health obsession is both a strength and a weakness -- it keeps you healthy but also anxious. "
            "Simple, clean eating, regular routines, and mental relaxation practices maintain your delicate balance."
        ),
        "temperament": (
            "Analytical, self-critical, and quietly devoted to those you love. Your emotional expression is reserved "
            "but your loyalty and care are demonstrated through practical acts of service. "
            "You can be harshly critical of both yourself and others when standards are not met. "
            "Learning to accept imperfection -- in yourself and the world -- is the Virgo ascendant's deepest lesson."
        ),
        "physical_appearance": (
            "Neat, refined appearance with a slender to medium build. The face is oval with intelligent, "
            "observant eyes and a tendency toward a youthful look. Hands are typically well-shaped and expressive. "
            "Your appearance is always tidy and appropriate; you prefer understated elegance to flashy display. "
            "Posture may reflect tension in the shoulders and neck from carrying responsibility."
        ),
        "career_aptitude": (
            "You excel in careers demanding precision, analysis, and service orientation. "
            "Healthcare, accounting, editing, research, quality control, and data science are ideal fields. "
            "You produce your best work in structured environments with clear standards and measurable outcomes. "
            "Roles involving improvement of systems, health advisory, or meticulous research leverage your Mercury gifts."
        ),
    },
    "Libra": {
        "overview": (
            "The Libra ascendant graces the personality with Venus's aesthetic sensibility, diplomatic skill, and partnership focus. "
            "You experience the world through relationship and are most fully yourself in the mirror of another person. "
            "First impressions are of someone charming, fair-minded, and aesthetically refined. "
            "Balance is your obsession -- you instinctively weigh options, opinions, and outcomes before deciding. "
            "Injustice and ugliness disturb you at a visceral level; you are driven to create harmony wherever you go. "
            "Your life is a continuous negotiation between self and other, independence and partnership, beauty and truth."
        ),
        "health_tendencies": (
            "The kidneys, lower back, and bladder are your vulnerable areas. Urinary tract issues, "
            "lower back pain, and skin conditions related to blood impurity need attention. "
            "Your health deteriorates when relationships are troubled -- emotional harmony is physical medicine. "
            "Adequate hydration, anti-inflammatory foods, and stress management protect your sensitive system."
        ),
        "temperament": (
            "Diplomatic, charming, and conflict-averse to a fault. You can see every perspective, "
            "which makes decisive action genuinely difficult. You avoid ugliness -- emotional and aesthetic. "
            "People-pleasing can override your own needs and create suppressed resentment. "
            "Learning to choose and stand firm, even when it creates temporary disharmony, is your growth edge."
        ),
        "physical_appearance": (
            "Attractive, well-proportioned body with a graceful, balanced build. The face is often symmetrical "
            "and classically handsome or beautiful with a pleasant, disarming smile. "
            "You have a natural sense of style and present yourself with effortless elegance. "
            "Dimples, a clear complexion, and an overall impression of refined beauty are typical."
        ),
        "career_aptitude": (
            "You excel in careers requiring partnership, aesthetic judgement, and diplomatic skill. "
            "Law, judiciary, fashion, art curation, diplomacy, interior design, and counselling are ideal. "
            "You work best in partnership or team settings rather than solo ventures. "
            "Careers that combine beauty with justice -- courtroom advocacy, design, or mediation -- are your sweet spot."
        ),
    },
    "Scorpio": {
        "overview": (
            "The Scorpio ascendant forges the personality in Mars-Ketu's intense, transformative, and deeply perceptive fire. "
            "You see beneath surfaces -- pretence, hidden motives, and buried truths are transparent to your penetrating gaze. "
            "First impressions are of someone magnetic, intense, and perhaps slightly dangerous. "
            "You live at life's extremes; mediocrity is intolerable to your all-or-nothing nature. "
            "Trust is earned slowly with you, but once given, your loyalty is absolute and your betrayal catastrophic. "
            "Your life is a series of deaths and rebirths -- you reinvent yourself more completely than any other ascendant."
        ),
        "health_tendencies": (
            "The reproductive organs, excretory system, and pelvic region are your sensitive areas. "
            "Infections, surgical needs, and conditions requiring deep intervention are characteristic health themes. "
            "Your constitution is actually very resilient -- you recover from crises that would devastate others. "
            "Regular detoxification, honest expression of emotions, and sexual health awareness maintain your powerful system."
        ),
        "temperament": (
            "Intense, passionate, and emotionally powerful with a tendency toward all-or-nothing responses. "
            "You feel everything deeply and forgive nothing easily -- grudges can persist for years. "
            "Jealousy and possessiveness are your shadow emotions; control is your defence mechanism. "
            "Learning to trust, release, and transform rather than destroy is the Scorpio ascendant's ultimate evolution."
        ),
        "physical_appearance": (
            "Medium build with a magnetic, intense presence that belies physical stature. "
            "The eyes are the defining feature -- deep, penetrating, and impossible to look away from. "
            "Features may be sharp, with a prominent nose and defined jawline. "
            "Your physical presence commands attention not through size but through sheer energetic intensity."
        ),
        "career_aptitude": (
            "You excel in careers requiring investigation, transformation, and working with hidden dimensions. "
            "Surgery, psychology, research, detective work, insurance, mining, and crisis management are ideal. "
            "You need work that has real stakes and genuine depth; superficial roles bore you immediately. "
            "Positions of behind-the-scenes power suit you better than public-facing leadership roles."
        ),
    },
    "Sagittarius": {
        "overview": (
            "The Sagittarius ascendant expands the personality with Jupiter's wisdom, optimism, and restless love of freedom. "
            "You are a seeker -- of truth, meaning, adventure, and the furthest horizons of human experience. "
            "First impressions are of someone enthusiastic, honest, and infectiously optimistic. "
            "Your mind naturally operates at the level of principles and big pictures rather than details. "
            "Freedom -- intellectual, physical, and spiritual -- is non-negotiable for your well-being. "
            "Your life is an epic journey through philosophies, cultures, and experiences that continuously expand your worldview."
        ),
        "health_tendencies": (
            "The hips, thighs, liver, and sciatic nerve are your vulnerable areas. Sciatica, liver disorders, "
            "and weight gain from overindulgence are common health patterns. Your optimistic nature means you "
            "often ignore symptoms until they become serious. Moderation in eating and drinking, hip-opening "
            "exercises, and periodic liver cleanses maintain your naturally robust constitution."
        ),
        "temperament": (
            "Optimistic, philosophically inclined, and brutally honest -- sometimes to the point of tactlessness. "
            "Your enthusiasm for ideas can make you preachy or dogmatic without realising it. "
            "Commitment is your deepest challenge -- the next horizon always beckons. "
            "Learning depth alongside breadth, and devotion alongside freedom, is your path to emotional maturity."
        ),
        "physical_appearance": (
            "Tall, athletic build with long limbs and an open, friendly face. The forehead is broad, "
            "and the expression is characteristically cheerful and approachable. "
            "Your gait is energetic, often with a slight bounce that reflects your optimistic nature. "
            "You tend toward a larger frame in later years, particularly in the hip and thigh area."
        ),
        "career_aptitude": (
            "You excel in careers involving wisdom, teaching, travel, and expansive vision. "
            "Higher education, law, philosophy, publishing, foreign trade, and religious leadership are ideal. "
            "You need a role that allows travel, continued learning, and exposure to diverse cultures. "
            "Academic institutions, international organisations, and spiritual teaching platforms are your natural homes."
        ),
    },
    "Capricorn": {
        "overview": (
            "The Capricorn ascendant structures the personality with Saturn's discipline, ambition, and profound sense of duty. "
            "You take life seriously from a young age and carry responsibilities that others your age would refuse. "
            "First impressions are of someone mature, reserved, and perhaps older than their years. "
            "Achievement through sustained effort is your fundamental approach to everything in life. "
            "You may lack the sparkle of fire signs or the charm of air signs, but your results speak louder. "
            "Your life follows a reverse trajectory -- difficult youth gives way to increasingly prosperous and satisfied maturity."
        ),
        "health_tendencies": (
            "The knees, joints, bones, teeth, and skin are your vulnerable areas. Arthritis, dental issues, "
            "knee injuries, and skin dryness are characteristic conditions. Your health actually improves with age "
            "as Saturn rewards your disciplined lifestyle. Cold and damp aggravate your conditions. "
            "Calcium-rich diet, weight-bearing exercise, and consistent health routines are your best medicines."
        ),
        "temperament": (
            "Serious, responsible, and emotionally reserved with a dry wit that surprises those who know you well. "
            "You suppress emotions in favour of duty and may struggle to express vulnerability. "
            "Pessimism and melancholy are real tendencies, especially in youth. "
            "Learning that joy is not frivolous and that emotional expression is not weakness transforms your inner life."
        ),
        "physical_appearance": (
            "Lean, bony frame with prominent bone structure, especially cheekbones and jawline. "
            "The face tends to be long and serious with deep-set, observant eyes. "
            "You may appear older than your age in youth but age remarkably well, looking distinguished in maturity. "
            "Posture is typically upright and controlled, reflecting your disciplined nature."
        ),
        "career_aptitude": (
            "You excel in careers requiring structure, authority, and long-term strategic thinking. "
            "Government administration, corporate management, engineering, architecture, and law are ideal. "
            "You build your career brick by brick and reach peak positions through undeniable competence. "
            "Roles with clear hierarchy and measurable advancement suit your patient, ambitious nature."
        ),
    },
    "Aquarius": {
        "overview": (
            "The Aquarius ascendant electrifies the personality with Saturn-Rahu's unique combination of discipline and eccentricity. "
            "You think differently from everyone around you -- not for rebellion's sake but because your mind genuinely operates on different frequencies. "
            "First impressions are of someone intelligent, detached, and slightly unconventional. "
            "Individuality is sacred to you; conforming to expectations feels like a betrayal of your nature. "
            "Friendship and collective well-being matter more to you than romantic attachment or family tradition. "
            "Your life is dedicated to ideas, innovation, and the betterment of humanity through progressive action."
        ),
        "health_tendencies": (
            "The calves, ankles, circulatory system, and nervous system are your vulnerable areas. "
            "Varicose veins, ankle sprains, blood circulation issues, and sudden-onset nervous conditions are typical. "
            "Your health benefits from unconventional healing modalities that others might dismiss. "
            "Regular leg exercises, adequate circulation, and avoiding prolonged standing protect your lower extremities."
        ),
        "temperament": (
            "Intellectually brilliant, emotionally detached, and firmly committed to personal freedom. "
            "You value friendship above romance and ideas above emotions. Your detachment is not coldness "
            "but a genuine orientation toward universal rather than personal concerns. "
            "Learning to be present with individual emotional experiences without intellectualising them is your growth path."
        ),
        "physical_appearance": (
            "Tall, lean build with distinctive features -- something about your appearance is memorable and unusual. "
            "The face may be angular with bright, intelligent eyes that seem to look at something beyond the immediate. "
            "Your style of dress tends toward the unique or unconventional, often ahead of fashion trends. "
            "An electric quality to your presence makes you recognisable even in a crowd."
        ),
        "career_aptitude": (
            "You excel in careers involving innovation, technology, and humanitarian service. "
            "Software development, aerospace, social reform, scientific research, and network-based enterprises are ideal. "
            "Conventional corporate environments stifle your creativity; you need intellectual freedom. "
            "Startups, research institutions, NGOs, and technology companies provide the progressive environment you require."
        ),
    },
    "Pisces": {
        "overview": (
            "The Pisces ascendant dissolves the personality's boundaries with Jupiter's compassion and Neptune's mystical sensitivity. "
            "You absorb the emotional atmosphere of every room you enter and feel others' pain as your own. "
            "First impressions are of someone gentle, dreamy, and radiating a subtle, otherworldly quality. "
            "Your imagination is vast, your intuition uncanny, and your capacity for compassion seemingly limitless. "
            "Material reality often feels less real to you than the inner world of feelings, visions, and spiritual perception. "
            "Your life is a poetic journey through the realms of art, devotion, sacrifice, and the search for divine connection."
        ),
        "health_tendencies": (
            "The feet, lymphatic system, and immune system are your sensitive areas. Foot problems, "
            "allergies, susceptibility to infections, and sensitivity to medications and substances are characteristic. "
            "Your constitution is absorbent -- you take in environmental toxins and emotional pollution easily. "
            "Clean environments, pure food, adequate sleep, and spiritual practice are essential for maintaining your delicate health."
        ),
        "temperament": (
            "Compassionate, imaginative, and emotionally absorbent to an extraordinary degree. "
            "You feel everything -- your own emotions and those of everyone around you simultaneously. "
            "Escapism through fantasy, substances, or withdrawal is your defence when overwhelmed. "
            "Learning healthy boundaries while keeping your heart open is the Pisces ascendant's great spiritual challenge."
        ),
        "physical_appearance": (
            "Medium build, often with a soft, rounded quality. The eyes are large, dreamy, and deeply expressive -- "
            "often the most memorable feature. Skin tends to be sensitive and fair. "
            "There is an ethereal, otherworldly quality to your appearance that others find captivating. "
            "Your movements are fluid and graceful, almost as if you are swimming through air rather than walking."
        ),
        "career_aptitude": (
            "You excel in careers requiring imagination, compassion, and spiritual sensitivity. "
            "Music, cinema, spiritual teaching, nursing, marine biology, art therapy, and charitable work are ideal. "
            "You need work that feels meaningful at a soul level; purely profit-driven roles drain your spirit. "
            "Creative environments, healing institutions, and spiritual communities are where you produce your finest work."
        ),
    },
}


# ============================================================
# 13. MAHADASHA_DETAILED -- Mahadasha Effects by House Placement
# ============================================================

MAHADASHA_DETAILED: Dict[str, Dict[int, str]] = {
    "Sun": {
        1: (
            "Sun Mahadasha with Sun in the 1st house brings a powerful period of self-assertion and personal authority. "
            "Health and vitality are strong; you gain recognition through your own merits and personality. "
            "Government favour, promotion, and leadership roles come naturally. Ego conflicts with authority figures "
            "need management. This is a period of self-discovery, confidence-building, and establishing your identity."
        ),
        2: (
            "Sun Mahadasha with Sun in the 2nd house activates wealth through government or authority positions. "
            "Speech becomes commanding and influential; family life gains structure and direction. "
            "Inheritance from father or government grants is possible. Eye or dental issues may surface. "
            "Investments in gold and government securities yield good returns during this period."
        ),
        3: (
            "Sun Mahadasha with Sun in the 3rd house stimulates courage, communication, and short travels. "
            "Relations with siblings improve if Sun is well-placed; conflicts arise if afflicted. "
            "Success in media, writing, and administrative communication. Self-confidence in daily dealings increases. "
            "Chest and shoulder strength improve; physical vitality supports adventurous pursuits."
        ),
        4: (
            "Sun Mahadasha with Sun in the 4th house brings focus to home, mother, and property matters. "
            "Government land allocation or property through authority connections is possible. "
            "Domestic peace may be disturbed by father's dominance or authority conflicts at home. "
            "Heart health needs monitoring. Inner confidence grows despite external domestic challenges."
        ),
        5: (
            "Sun Mahadasha with Sun in the 5th house is excellent for intelligence, creativity, and children. "
            "Speculative gains, success in competitive examinations, and political connections flourish. "
            "Romantic life carries dignity and warmth. Children bring pride and recognition. "
            "Stomach or digestive issues may arise. Spiritual inclination through mantra practice increases."
        ),
        6: (
            "Sun Mahadasha with Sun in the 6th house brings victory over enemies and competitors. "
            "Government jobs, especially in defence, police, or medical services, are highly favoured. "
            "Health issues related to bile, acidity, and inflammation surface but are overcome through treatment. "
            "Legal disputes resolve favourably. Service-oriented work brings recognition and steady advancement."
        ),
        7: (
            "Sun Mahadasha with Sun in the 7th house activates partnerships, marriage, and public dealings. "
            "The spouse may be authoritative or connected to government. Business partnerships with "
            "powerful individuals are indicated. Ego clashes in marriage need careful handling. "
            "Public reputation rises but personal relationships require humility and compromise."
        ),
        8: (
            "Sun Mahadasha with Sun in the 8th house is a period of transformation and hidden challenges. "
            "Health crises, particularly related to bones, heart, or vitality, require vigilance. "
            "Inheritance or insurance matters come to the forefront. Research and occult interests deepen. "
            "Government penalties or sudden falls from grace are possible if Sun is afflicted. Inner strength grows through trials."
        ),
        9: (
            "Sun Mahadasha with Sun in the 9th house is highly auspicious for fortune, dharma, and higher learning. "
            "Father's blessings and guidance bring prosperity. Pilgrimages, foreign travel, and spiritual growth flourish. "
            "Recognition in academic, legal, or religious circles. Government patronage for educational pursuits. "
            "This is one of the best periods for overall luck, wisdom, and righteous living."
        ),
        10: (
            "Sun Mahadasha with Sun in the 10th house is the zenith of career and public achievement. "
            "Government positions, political power, and administrative authority are at their peak. "
            "Professional reputation soars; you become a figure of authority and respect in your field. "
            "Father's influence supports career growth. Health remains strong as purpose drives vitality."
        ),
        11: (
            "Sun Mahadasha with Sun in the 11th house brings fulfilment of desires and significant income gains. "
            "Powerful friends, government connections, and influential social circles expand your reach. "
            "Elder siblings prosper. Speculative and investment income is favourable. "
            "Recognition and awards for past achievements arrive. This is an excellent period for networking and ambition."
        ),
        12: (
            "Sun Mahadasha with Sun in the 12th house directs energy toward spirituality, foreign lands, and seclusion. "
            "Expenditure increases; foreign travel or residence abroad is possible. Hospitalisation or retreat "
            "may be necessary. Father may face health challenges. Government matters cause hidden expenses. "
            "Spiritual awakening through solitude and meditation is the highest expression of this placement."
        ),
    },
    "Moon": {
        1: (
            "Moon Mahadasha with Moon in the 1st house brings emotional prominence, public visibility, and "
            "heightened sensitivity. Your popularity increases as others find you approachable and empathetic. "
            "Health fluctuates with emotional state; skin and chest areas need attention. "
            "This is a period of self-awareness, emotional maturation, and establishing your public persona."
        ),
        2: (
            "Moon Mahadasha with Moon in the 2nd house activates family wealth, eloquent speech, and domestic prosperity. "
            "Income from food, hospitality, or liquid assets increases. Family gatherings and traditions strengthen. "
            "Your voice and communication carry emotional power that influences others deeply. "
            "Eye health and dietary balance need attention. Savings grow through emotionally intelligent decisions."
        ),
        3: (
            "Moon Mahadasha with Moon in the 3rd house brings creative communication, short travels, and sibling bonding. "
            "Writing, blogging, and artistic expression flourish. Emotional courage develops through small adventures. "
            "Relations with neighbours and siblings become emotionally rich. "
            "Mental restlessness needs grounding; creative hobbies provide the best outlet."
        ),
        4: (
            "Moon Mahadasha with Moon in the 4th house is deeply auspicious for domestic happiness, property, and maternal bonds. "
            "Purchase of home, vehicle, or land is strongly indicated. Mother's influence is profound and supportive. "
            "Inner peace and emotional security reach a high point. Educational pursuits succeed. "
            "This is one of the most comfortable and emotionally fulfilling dasha periods."
        ),
        5: (
            "Moon Mahadasha with Moon in the 5th house blesses with emotional intelligence, romance, and creative output. "
            "Children bring joy and emotional fulfilment. Love relationships are emotionally deep and nurturing. "
            "Artistic pursuits, especially music and poetry, flourish. Speculative gains through intuition are possible. "
            "Stomach health needs monitoring. Spiritual practice through devotional means deepens."
        ),
        6: (
            "Moon Mahadasha with Moon in the 6th house brings emotional challenges through enemies, illness, or service demands. "
            "Digestive issues, water-related ailments, and emotional disturbances from workplace conflicts arise. "
            "Service in hospitals, food industry, or maternal care brings purpose despite difficulties. "
            "Emotional resilience grows through overcoming adversity; mother's health may need attention."
        ),
        7: (
            "Moon Mahadasha with Moon in the 7th house activates marriage, partnerships, and public emotional engagement. "
            "The spouse is nurturing, emotionally expressive, and deeply connected. Business partnerships "
            "based on emotional trust prosper. Public popularity increases dramatically. "
            "Emotional dependency in relationships needs balancing; healthy boundaries preserve marital happiness."
        ),
        8: (
            "Moon Mahadasha with Moon in the 8th house is a period of emotional transformation and hidden disturbances. "
            "Inheritance through maternal family is possible. Emotional crises lead to deep psychological growth. "
            "Chronic health issues related to hormones, chest, or reproductive system may surface. "
            "Occult interests and psychic abilities develop. This period transforms emotional vulnerability into spiritual power."
        ),
        9: (
            "Moon Mahadasha with Moon in the 9th house brings emotional wisdom, maternal blessings, and fortunate travels. "
            "Pilgrimages to sacred water bodies are especially favoured. Mother's spiritual guidance influences your path. "
            "Higher education in arts, counselling, or spirituality succeeds. Fortune comes through emotional intelligence. "
            "This is a deeply auspicious period for dharmic living and spiritual maturation."
        ),
        10: (
            "Moon Mahadasha with Moon in the 10th house brings public recognition through emotionally resonant work. "
            "Career in hospitality, nursing, public welfare, or food industry reaches its peak. "
            "Professional reputation benefits from your empathetic, caring approach. Mother's influence supports career. "
            "Emotional fluctuations at work need management; consistency in public image builds lasting success."
        ),
        11: (
            "Moon Mahadasha with Moon in the 11th house brings income through networks, elder siblings, and fulfilled desires. "
            "Social circle expands with emotionally supportive friendships. Income from female contacts or public dealings. "
            "Elder siblings and maternal connections bring opportunities. Speculative gains through intuition prosper. "
            "This is a period of emotional abundance, social fulfilment, and material comfort."
        ),
        12: (
            "Moon Mahadasha with Moon in the 12th house directs emotional energy toward spiritual liberation and foreign lands. "
            "Expenditure on spiritual pursuits, hospitalisation, or foreign residence increases. "
            "Sleep quality and dream life become significant. Emotional isolation may feel overwhelming at times. "
            "Meditation near water, charitable acts, and surrender to the divine bring the deepest peace."
        ),
    },
    "Mars": {
        1: (
            "Mars Mahadasha with Mars in the 1st house is a period of intense energy, courage, and physical dynamism. "
            "Athletic ability, personal initiative, and self-assertion reach their peak. Leadership through action inspires others. "
            "Anger management is critical; accidents and head injuries need vigilance. "
            "This period forges an indomitable will through challenges that demand physical and moral courage."
        ),
        2: (
            "Mars Mahadasha with Mars in the 2nd house brings aggressive earning, property acquisition, and family conflicts. "
            "Speech becomes sharp and commanding. Income through engineering, real estate, or military service increases. "
            "Dental and eye issues may arise. Family arguments over money or property need diplomatic handling. "
            "Savings grow rapidly when impulse spending is controlled."
        ),
        3: (
            "Mars Mahadasha with Mars in the 3rd house is excellent for courage, siblings, and physical endeavours. "
            "Victory in competitions, sports achievements, and success in short journeys are indicated. "
            "Relations with siblings are dynamic and competitive but ultimately strengthening. "
            "Communication becomes bold and effective. Physical strength and stamina reach impressive levels."
        ),
        4: (
            "Mars Mahadasha with Mars in the 4th house brings property-related activity, domestic energy, and potential conflict at home. "
            "Land purchase, construction, or renovation of property is strongly indicated. Vehicle acquisition is likely. "
            "Domestic peace is disrupted by arguments or aggressive home energy. Mother's health needs monitoring. "
            "Real estate investments made during this period yield significant long-term value."
        ),
        5: (
            "Mars Mahadasha with Mars in the 5th house activates competitive intelligence, sports, and children's affairs. "
            "Success in competitive examinations, sports, and speculative ventures is indicated. "
            "Children may be athletic or competitive. Romantic relationships are passionate but potentially conflictual. "
            "Stomach and digestive fire are strong. Mantra practice with fiery deities yields powerful results."
        ),
        6: (
            "Mars Mahadasha with Mars in the 6th house is one of the best placements for defeating enemies and disease. "
            "Legal victories, competitive triumphs, and physical recovery from illness are strongly favoured. "
            "Career in military, police, surgery, or competitive sports thrives. Physical fitness improves dramatically. "
            "Debts are cleared through aggressive action. This is a period of conquering all obstacles through force of will."
        ),
        7: (
            "Mars Mahadasha with Mars in the 7th house brings passionate but potentially turbulent partnerships. "
            "Marriage is dynamic with strong physical attraction but frequent arguments. Business partnerships "
            "are energetic but need conflict management. Mangala Dosha effects manifest most strongly. "
            "Marital counselling and conscious anger management preserve the relationship's powerful potential."
        ),
        8: (
            "Mars Mahadasha with Mars in the 8th house is a period of intense transformation, surgery, and hidden battles. "
            "Surgical interventions, accident risk, and sudden health crises demand caution. "
            "Inheritance or insurance matters bring unexpected gains. Occult and tantric interests intensify. "
            "This challenging period destroys the weak within you and forges an unbreakable inner warrior."
        ),
        9: (
            "Mars Mahadasha with Mars in the 9th house energises dharma, father, and long-distance endeavours. "
            "Pilgrimages with physical challenge, defence-related higher education, and father's health are themes. "
            "Religious or philosophical debates become passionate. Fortune comes through bold, courageous action. "
            "Property or land connected to temples or religious institutions is possible."
        ),
        10: (
            "Mars Mahadasha with Mars in the 10th house is the peak of professional power through action and initiative. "
            "Career in engineering, military, surgery, sports, or real estate reaches its zenith. "
            "Authority comes through demonstrated competence and fearless leadership. "
            "Workplace conflicts are won decisively. Physical projects and construction ventures succeed spectacularly."
        ),
        11: (
            "Mars Mahadasha with Mars in the 11th house brings income through competition, siblings, and aggressive networking. "
            "Desires are fulfilled through forceful pursuit. Friendships with military, sports, or engineering professionals benefit you. "
            "Elder siblings prosper or provide support. Speculative gains through bold market moves are indicated. "
            "This is a period of ambition fulfilled through action and competitive excellence."
        ),
        12: (
            "Mars Mahadasha with Mars in the 12th house increases expenditure, foreign travel, and hidden conflicts. "
            "Hospitalisation due to surgery or accidents is possible. Foreign employment, especially in military or engineering. "
            "Bed pleasures and secret activities increase. Spiritual growth through rigorous physical practices like yoga. "
            "Mars energy turned inward through discipline becomes a powerful force for liberation."
        ),
    },
    "Mercury": {
        1: (
            "Mercury Mahadasha with Mercury in the 1st house enhances intelligence, communication, and youthful appearance. "
            "Business acumen, intellectual confidence, and social networking ability reach their peak. "
            "Skin health and nervous system need attention. Speech and writing become primary tools of success. "
            "This is an excellent period for starting businesses, learning new skills, and building intellectual reputation."
        ),
        2: (
            "Mercury Mahadasha with Mercury in the 2nd house is superb for wealth through intellect and speech. "
            "Income from trading, writing, accounting, and communication-based businesses flourishes. "
            "Family life is intellectually stimulating. Voice and speech become commercially valuable assets. "
            "Financial planning skills peak; investments in education and intellectual property yield returns."
        ),
        3: (
            "Mercury Mahadasha with Mercury in the 3rd house is the finest period for communication, media, and short travel. "
            "Writing, blogging, journalism, and media production succeed brilliantly. Relations with siblings improve "
            "through shared intellectual interests. Short courses and skill-building workshops yield immediate career benefits. "
            "Courage in expressing ideas leads to recognition in your immediate environment."
        ),
        4: (
            "Mercury Mahadasha with Mercury in the 4th house brings intellectual activity at home and educational success. "
            "Study environment improves; academic qualifications are completed. Home becomes a place of learning "
            "and intellectual exchange. Property transactions through documentation and legal work succeed. "
            "Mother's intellectual influence is significant. Mental peace comes through knowledge and learning."
        ),
        5: (
            "Mercury Mahadasha with Mercury in the 5th house blesses with sharp intelligence, creative writing, and speculative gains. "
            "Success in competitive examinations, intellectual competitions, and academic research is strongly indicated. "
            "Children show intellectual precocity. Romantic relationships begin through intellectual connection. "
            "Mantra practice yields quick results; Mercury-related mantras are especially powerful."
        ),
        6: (
            "Mercury Mahadasha with Mercury in the 6th house helps overcome enemies through intellectual strategy. "
            "Legal matters are resolved through documentation and logical argument. Health issues related to "
            "nervous system, skin, or digestive tract surface but respond well to analytical medical approaches. "
            "Career in healthcare documentation, legal analysis, or service industry management prospers."
        ),
        7: (
            "Mercury Mahadasha with Mercury in the 7th house activates intellectual partnerships and business dealings. "
            "Marriage or partnership with an intelligent, communicative person is indicated. Business contracts "
            "and legal agreements are exceptionally well-crafted. Trading and brokerage partnerships prosper. "
            "Communication is the foundation of marital harmony during this period."
        ),
        8: (
            "Mercury Mahadasha with Mercury in the 8th house activates research, investigation, and hidden knowledge. "
            "Insurance, inheritance documentation, and forensic work succeed. Nervous system and skin need attention. "
            "Interest in astrology, occult sciences, and mystery traditions deepens. "
            "Analytical ability applied to life's mysteries yields profound understanding."
        ),
        9: (
            "Mercury Mahadasha with Mercury in the 9th house is superb for higher education, publishing, and fortune through intellect. "
            "Academic degrees, published works, and philosophical teaching bring recognition. "
            "Travel for educational purposes is highly favourable. Father's intellectual legacy benefits you. "
            "This is one of the most intellectually productive and fortunate periods of life."
        ),
        10: (
            "Mercury Mahadasha with Mercury in the 10th house elevates career through communication and intellectual authority. "
            "Positions in media, education, IT, publishing, and administrative communication reach their peak. "
            "Professional reputation is built on intellectual competence and articulate expression. "
            "Business ventures using technology and communication flourish during this highly productive period."
        ),
        11: (
            "Mercury Mahadasha with Mercury in the 11th house brings income through networks, intellect, and multiple streams. "
            "Friendships with intellectuals, writers, and business professionals expand your opportunities. "
            "Income from trading, consulting, and intellectual property is significant. Social media and digital platforms "
            "become especially profitable. This is a period of abundant intellectual and financial networking gains."
        ),
        12: (
            "Mercury Mahadasha with Mercury in the 12th house directs intellect toward foreign lands and spiritual study. "
            "Foreign education, online international business, and remote intellectual work are indicated. "
            "Expenditure on education and communication tools increases. Sleep disturbances and nervous tension abroad. "
            "Spiritual knowledge through study of scriptures and philosophical texts deepens understanding."
        ),
    },
    "Jupiter": {
        1: (
            "Jupiter Mahadasha with Jupiter in the 1st house is one of the most auspicious periods for personal growth and wisdom. "
            "Health, fortune, and social reputation expand simultaneously. Spiritual inclination deepens naturally. "
            "Weight gain and liver health need attention. You become a source of guidance and wisdom for others. "
            "This period establishes your reputation as a person of integrity, learning, and generous spirit."
        ),
        2: (
            "Jupiter Mahadasha with Jupiter in the 2nd house is supremely auspicious for wealth, family, and speech. "
            "Income through education, religious work, counselling, and financial advisory flourishes. "
            "Family life is prosperous and harmonious. Speech carries wisdom and influence. "
            "Savings grow substantially; gold, education funds, and traditional investments are highly favourable."
        ),
        3: (
            "Jupiter Mahadasha with Jupiter in the 3rd house brings wisdom to communication, travel, and sibling relationships. "
            "Religious writing, philosophical publishing, and wise counsel to siblings characterise this period. "
            "Short pilgrimages and educational tours are beneficial. Courage rooted in faith develops. "
            "Your communication carries weight and authority; mentoring others becomes a natural role."
        ),
        4: (
            "Jupiter Mahadasha with Jupiter in the 4th house blesses with property, domestic peace, and educational achievement. "
            "Purchase of a spacious, auspicious home is strongly indicated. Mother's blessings flow abundantly. "
            "Higher education or advanced degrees are completed successfully. Vehicles and comforts increase. "
            "This is a period of deep contentment, inner wisdom, and domestic prosperity."
        ),
        5: (
            "Jupiter Mahadasha with Jupiter in the 5th house is outstanding for children, intelligence, and spiritual practice. "
            "Birth of children, especially sons, is strongly indicated. Creative and intellectual output is at its finest. "
            "Speculative gains through wise investment are favourable. Romantic relationships carry dignity and depth. "
            "Mantra siddhi and spiritual initiation are powerfully supported during this exceptionally blessed period."
        ),
        6: (
            "Jupiter Mahadasha with Jupiter in the 6th house brings mixed results -- triumph over enemies but potential health excess. "
            "Legal victories and defeat of competitors through ethical means are indicated. "
            "Liver, obesity, and diabetic tendencies need monitoring. Service in educational or religious institutions prospers. "
            "Enemies are transformed into allies through your magnanimous and fair approach to conflict."
        ),
        7: (
            "Jupiter Mahadasha with Jupiter in the 7th house is highly auspicious for marriage, partnerships, and public life. "
            "Marriage to a wise, educated, and spiritually inclined partner is indicated. Business partnerships "
            "based on ethical principles prosper enormously. Public reputation for fairness and wisdom grows. "
            "This is one of the finest periods for marital happiness and partnership-based prosperity."
        ),
        8: (
            "Jupiter Mahadasha with Jupiter in the 8th house brings spiritual transformation, longevity, and hidden gains. "
            "Interest in philosophy, metaphysics, and life after death deepens. Insurance and inheritance matters "
            "are resolved favourably. Longevity increases; recovery from illness is supported by divine grace. "
            "This period transforms material loss into spiritual wealth through surrender and wisdom."
        ),
        9: (
            "Jupiter Mahadasha with Jupiter in the 9th house is the most auspicious of all -- Dharma Karmadhipati Yoga potential. "
            "Fortune, father's blessings, higher education, and spiritual initiation all flourish simultaneously. "
            "International travel, particularly for religious or educational purposes, is strongly favoured. "
            "This period represents the highest expression of Jupiter: wisdom, generosity, dharma, and divine grace."
        ),
        10: (
            "Jupiter Mahadasha with Jupiter in the 10th house brings the pinnacle of professional success through wisdom. "
            "Career in education, judiciary, banking, counselling, or religious leadership reaches its zenith. "
            "Public reputation for integrity and competence is at its highest. Government recognition is possible. "
            "Professional authority is earned through genuine wisdom and ethical conduct during this powerful period."
        ),
        11: (
            "Jupiter Mahadasha with Jupiter in the 11th house brings maximum fulfilment of desires and abundant income. "
            "Wealthy and wise friendships expand your horizons. Income through education, advisory, and investments flourishes. "
            "Elder siblings prosper. All major desires -- property, vehicle, marriage, children -- move toward fulfilment. "
            "This is a period of abundance, social recognition, and the materialisation of long-held aspirations."
        ),
        12: (
            "Jupiter Mahadasha with Jupiter in the 12th house is exceptional for spiritual liberation and foreign prosperity. "
            "Foreign travel for education, spiritual retreat, or pilgrimage is strongly indicated. "
            "Expenditure on charitable and spiritual causes increases but returns spiritual dividends. "
            "Moksha-oriented practices deepen. Hospital or ashram-related work brings inner peace and divine connection."
        ),
    },
    "Venus": {
        1: (
            "Venus Mahadasha with Venus in the 1st house is a period of beauty, charm, and material comfort. "
            "Personal attractiveness increases dramatically; romantic opportunities multiply. "
            "Artistic talents flourish and your aesthetic sensibility earns appreciation. "
            "Health is generally good but reproductive system needs attention. This is a period of pleasure, luxury, and self-love."
        ),
        2: (
            "Venus Mahadasha with Venus in the 2nd house brings wealth, family harmony, and sweet speech. "
            "Income through arts, fashion, jewellery, luxury goods, and beauty products increases substantially. "
            "Family life is filled with celebrations, feasts, and material abundance. Voice becomes melodious and persuasive. "
            "Savings in gold, diamonds, and beautiful assets appreciate in value. This is one of the finest periods for wealth."
        ),
        3: (
            "Venus Mahadasha with Venus in the 3rd house activates artistic communication, creative media, and pleasant journeys. "
            "Success in creative writing, music production, fashion blogging, and artistic media is strongly indicated. "
            "Relations with younger siblings are harmonious and mutually beneficial. Short romantic getaways bring joy. "
            "Artistic courage develops; you express beauty and love through creative media confidently."
        ),
        4: (
            "Venus Mahadasha with Venus in the 4th house blesses with a beautiful home, vehicle, and domestic luxury. "
            "Purchase of an aesthetically pleasing property is strongly indicated. Vehicle acquisition, especially luxury. "
            "Mother's love and artistic influence enrich your inner life. Academic success in arts and culture. "
            "This is a period of domestic beauty, emotional comfort, and deep inner peace."
        ),
        5: (
            "Venus Mahadasha with Venus in the 5th house is exceptional for romance, creativity, and artistic achievement. "
            "Love relationships are deeply fulfilling and may lead to marriage. Creative output reaches its artistic peak. "
            "Speculative gains through art, entertainment, or luxury investments are favourable. "
            "Children are artistically gifted. This is the most romantically and creatively blessed period."
        ),
        6: (
            "Venus Mahadasha with Venus in the 6th house brings challenges to relationships and health but success through service. "
            "Reproductive health, kidney, and sugar-related issues need monitoring. Workplace conflicts involve jealousy. "
            "Success in beauty services, fashion healthcare, or artistic therapy provides income. "
            "The period teaches that true beauty endures through service and overcoming vanity."
        ),
        7: (
            "Venus Mahadasha with Venus in the 7th house is the most powerful period for marriage, love, and partnership. "
            "Marriage to a beautiful, charming, and cultured partner is strongly indicated. Business partnerships "
            "in luxury, beauty, or arts prosper enormously. Public image radiates grace and attractiveness. "
            "This is Venus at its most powerful for conjugal happiness and partnership-based wealth creation."
        ),
        8: (
            "Venus Mahadasha with Venus in the 8th house brings transformation through relationships and hidden pleasures. "
            "Inheritance through spouse or in-laws is possible. Sexual magnetism and secretive romantic experiences increase. "
            "Reproductive health and urinary tract need attention. Insurance and shared financial resources grow. "
            "The deepest beauty and love are discovered through vulnerability and emotional transformation."
        ),
        9: (
            "Venus Mahadasha with Venus in the 9th house brings fortune through beauty, art, and cultural pursuits. "
            "International travel to beautiful destinations is indicated. Marriage to someone from a different cultural background. "
            "Higher education in fine arts, music, or culture studies succeeds. Father's support is gracious. "
            "This period combines dharma with beauty -- your fortune comes through aesthetic and cultural excellence."
        ),
        10: (
            "Venus Mahadasha with Venus in the 10th house elevates career in beauty, arts, and luxury industries. "
            "Career in fashion, cinema, hospitality, interior design, or luxury management reaches its peak. "
            "Professional reputation for elegance and artistic excellence grows. Government recognition in cultural fields. "
            "The public sees you as graceful and accomplished during this highly successful professional period."
        ),
        11: (
            "Venus Mahadasha with Venus in the 11th house brings income through arts, luxury, and social networks. "
            "Wealthy, influential friendships in arts and fashion expand your reach. Income from beauty products, "
            "entertainment investments, and luxury ventures is substantial. All material desires move toward fulfilment. "
            "Elder siblings prosper. Social life is vibrant, glamorous, and financially rewarding."
        ),
        12: (
            "Venus Mahadasha with Venus in the 12th house directs pleasure toward spiritual experiences and foreign lands. "
            "Foreign travel to beautiful destinations, spiritual retreats, and artistic pilgrimages are indicated. "
            "Bed pleasures, dream life, and private romantic experiences are heightened. "
            "Expenditure on luxury and beauty increases. Spiritual growth through art, music, and devotion deepens."
        ),
    },
    "Saturn": {
        1: (
            "Saturn Mahadasha with Saturn in the 1st house is a period of serious self-reflection, discipline, and endurance. "
            "Health challenges, particularly bones, joints, and teeth, demand attention. Physical appearance may age. "
            "Responsibilities increase dramatically. Character is tested and tempered through sustained difficulty. "
            "This period builds indestructible inner strength; what you endure now becomes your greatest source of authority."
        ),
        2: (
            "Saturn Mahadasha with Saturn in the 2nd house restricts finances initially but builds lasting wealth through discipline. "
            "Speech becomes measured and authoritative. Family responsibilities weigh heavily. "
            "Income grows slowly but steadily through traditional industries, government, or agriculture. "
            "Dental and eye issues need attention. Savings built through extreme frugality create permanent security."
        ),
        3: (
            "Saturn Mahadasha with Saturn in the 3rd house develops courage through hardship and persistent effort. "
            "Relations with siblings are burdened with responsibility. Short travels involve hard work. "
            "Communication becomes serious and authoritative. Physical stamina builds through sustained effort. "
            "Success in writing, administrative work, and disciplined media production comes late but endures."
        ),
        4: (
            "Saturn Mahadasha with Saturn in the 4th house brings domestic hardship, property burdens, and emotional austerity. "
            "Mother's health or emotional availability may be limited. Property comes with responsibilities or litigation. "
            "Emotional comfort is scarce; inner life feels austere. Educational achievements require double effort. "
            "The period teaches that true security comes from inner discipline, not external comfort."
        ),
        5: (
            "Saturn Mahadasha with Saturn in the 5th house creates challenges in children, creativity, and romance. "
            "Delayed children or difficulties with education are possible. Romantic life is serious and lacks spontaneity. "
            "Creative output is disciplined rather than inspired. Speculative ventures need extreme caution. "
            "Traditional spiritual practices requiring discipline -- japa, austerity, fasting -- yield deep results."
        ),
        6: (
            "Saturn Mahadasha with Saturn in the 6th house is excellent for overcoming enemies and chronic health management. "
            "Legal victories through persistent litigation. Career in law, medicine, or government service prospers. "
            "Chronic health issues are identified and managed with disciplined treatment protocols. "
            "Debts are cleared through systematic repayment. This is Saturn at its most constructively powerful."
        ),
        7: (
            "Saturn Mahadasha with Saturn in the 7th house brings delayed but durable marriage and serious partnerships. "
            "Spouse is older, mature, or Saturnine in temperament. Marriage improves significantly after initial difficulties. "
            "Business partnerships require patience and long-term commitment to yield results. "
            "Public dealings are characterised by seriousness and reliability. Marital maturity develops over time."
        ),
        8: (
            "Saturn Mahadasha with Saturn in the 8th house is among the most challenging -- chronic illness, obstacles, and transformation. "
            "Health crises involving bones, chronic conditions, or surgical needs demand vigilance. "
            "Inheritance matters are delayed or disputed. Longevity is actually protected despite apparent dangers. "
            "Spiritual transformation through confronting mortality and suffering is the profound gift of this difficult period."
        ),
        9: (
            "Saturn Mahadasha with Saturn in the 9th house tests faith, fortune, and relationship with father. "
            "Father's health or fortune declines. Higher education is delayed but eventually completed. "
            "Religious practices become austere and disciplined. Fortune requires extreme patience. "
            "Travel is for duty rather than pleasure. This period builds unshakeable faith through testing."
        ),
        10: (
            "Saturn Mahadasha with Saturn in the 10th house is the period of maximum professional achievement through discipline. "
            "Career in government, construction, mining, agriculture, or traditional industries peaks. "
            "Authority is earned through demonstrated competence and years of disciplined service. "
            "Professional legacy is established during this period. The fruits of decades of effort finally materialise."
        ),
        11: (
            "Saturn Mahadasha with Saturn in the 11th house gradually fulfils long-held desires and builds income. "
            "Friendships with older, experienced professionals provide lasting support. Income increases steadily. "
            "Elder siblings may face challenges. Social position improves through reliable, consistent contribution. "
            "This is one of Saturn's better placements -- rewards for patience and persistent effort arrive."
        ),
        12: (
            "Saturn Mahadasha with Saturn in the 12th house brings isolation, foreign residence, and spiritual austerity. "
            "Expenditure increases through hospitalisation, foreign living, or spiritual retreats. "
            "Sleep disturbances and chronic health issues in foreign lands need management. "
            "Spiritual growth through solitude, renunciation, and disciplined meditation is profound. "
            "This period teaches liberation through letting go of worldly attachments."
        ),
    },
    "Rahu": {
        1: (
            "Rahu Mahadasha with Rahu in the 1st house creates an intense period of identity transformation and worldly ambition. "
            "Personality undergoes dramatic shifts; you may reinvent yourself completely. "
            "Unconventional appearance or lifestyle changes attract attention. Health anxieties and skin issues arise. "
            "This period propels you toward your karmic destiny through desire-driven action and bold self-presentation."
        ),
        2: (
            "Rahu Mahadasha with Rahu in the 2nd house brings unconventional wealth and speech patterns. "
            "Income from foreign sources, technology, speculation, or unconventional means increases. "
            "Family life is disrupted by unusual circumstances. Speech becomes persuasive but potentially deceptive. "
            "Financial volatility is high; disciplined investment of sudden gains creates lasting wealth."
        ),
        3: (
            "Rahu Mahadasha with Rahu in the 3rd house is powerful for media, communication, and courageous ventures. "
            "Success in technology-driven media, social networking, and unconventional communication flourishes. "
            "Relations with siblings involve unusual dynamics. Short travels to unusual destinations are indicated. "
            "Bold marketing, viral content creation, and innovative communication strategies succeed spectacularly."
        ),
        4: (
            "Rahu Mahadasha with Rahu in the 4th house creates unusual domestic circumstances and property opportunities. "
            "Residence in foreign lands or unconventional properties is indicated. Mother's health or situation is unusual. "
            "Property through unconventional means -- foreign investment, technology land deals. "
            "Inner peace is disturbed by restless desires; meditation and grounding practices are essential."
        ),
        5: (
            "Rahu Mahadasha with Rahu in the 5th house amplifies intelligence, speculation, and unconventional creativity. "
            "Speculative gains through technology, foreign markets, or unconventional investments are possible. "
            "Children may be precocious or unusual. Romantic relationships are intense and unconventional. "
            "Creative output is innovative and ahead of its time. Risk management in speculation is crucial."
        ),
        6: (
            "Rahu Mahadasha with Rahu in the 6th house is excellent for defeating enemies through unconventional strategies. "
            "Foreign enemies are defeated. Legal matters involving international or unusual circumstances resolve well. "
            "Health issues may be rare, unusual, or hard to diagnose. Career in technology, foreign companies, or investigation prospers. "
            "This is one of Rahu's better placements -- desire energy channelled into overcoming obstacles yields victory."
        ),
        7: (
            "Rahu Mahadasha with Rahu in the 7th house brings intense, unconventional partnerships and foreign spouse. "
            "Marriage to someone from a different culture, religion, or background is strongly indicated. "
            "Business partnerships involving foreign elements or technology prosper. "
            "Obsession in relationships needs management. The most transformative growth comes through partnership."
        ),
        8: (
            "Rahu Mahadasha with Rahu in the 8th house is a period of intense hidden transformation and sudden events. "
            "Unexpected gains or losses through inheritance, insurance, or sudden reversals mark this period. "
            "Health anxieties and unusual medical conditions may arise. Occult interests deepen dramatically. "
            "Research into hidden subjects yields breakthrough understanding. This period destroys illusions and reveals truth."
        ),
        9: (
            "Rahu Mahadasha with Rahu in the 9th house creates unconventional spiritual journeys and foreign fortune. "
            "Higher education abroad or in unconventional subjects is indicated. Father's situation involves foreign elements. "
            "Religious beliefs may shift dramatically. Fortune comes through foreign connections and innovation. "
            "This period challenges traditional belief systems and builds a unique spiritual philosophy."
        ),
        10: (
            "Rahu Mahadasha with Rahu in the 10th house is a period of ambitious career expansion and public image transformation. "
            "Career in technology, foreign companies, media, or unconventional industries skyrockets. "
            "Public reputation may be controversial but commanding. Political ambitions manifest. "
            "Professional success comes through innovative approaches that disrupt established patterns."
        ),
        11: (
            "Rahu Mahadasha with Rahu in the 11th house is the most materially rewarding -- maximum desire fulfilment. "
            "Income through technology, foreign connections, networks, and unconventional means soars. "
            "Social circle expands with powerful, unusual personalities. All worldly desires accelerate toward fulfilment. "
            "Elder siblings face unusual circumstances. This is Rahu's most powerful placement for material abundance."
        ),
        12: (
            "Rahu Mahadasha with Rahu in the 12th house intensifies foreign residence, spiritual seeking, and expenditure. "
            "Long-term residence abroad is strongly indicated. Expenditure on foreign luxury and unusual comforts increases. "
            "Sleep disturbances, vivid dreams, and psychic experiences are characteristic. "
            "Spiritual growth through foreign mystical traditions or unconventional meditation practices is profound."
        ),
    },
    "Ketu": {
        1: (
            "Ketu Mahadasha with Ketu in the 1st house brings spiritual awakening, detachment, and identity dissolution. "
            "Physical appearance may become austere or unusual. Health issues involving skin or mysterious ailments arise. "
            "Worldly ambitions diminish as spiritual interests intensify. You become increasingly detached from ego-driven pursuits. "
            "This period strips away false identities, revealing your essential spiritual nature."
        ),
        2: (
            "Ketu Mahadasha with Ketu in the 2nd house creates detachment from family wealth and conventional speech. "
            "Financial patterns are unpredictable -- sudden losses alternate with unexpected gains. "
            "Family relationships feel distant or karmically complex. Speech becomes cryptic or spiritually oriented. "
            "Eye and dental health need attention. Liberation from material attachment is this period's deepest gift."
        ),
        3: (
            "Ketu Mahadasha with Ketu in the 3rd house develops inner courage through spiritual practice rather than worldly action. "
            "Relations with siblings may be distant or karmically complex. Communication becomes introverted. "
            "Interest in mystical writing, silent meditation, and solitary spiritual practice increases. "
            "Physical stamina is unpredictable. True courage -- facing inner demons -- is the gift of this period."
        ),
        4: (
            "Ketu Mahadasha with Ketu in the 4th house creates detachment from home, mother, and domestic comfort. "
            "Sudden changes in residence, emotional distance from mother, and property-related spiritual lessons arise. "
            "Inner peace comes through renunciation rather than accumulation. Academic interests become spiritual. "
            "This period teaches that true home is within -- external domesticity is temporary."
        ),
        5: (
            "Ketu Mahadasha with Ketu in the 5th house brings spiritual intelligence, past-life connections, and mystical creativity. "
            "Children's karma plays a significant role. Romantic relationships carry past-life intensity. "
            "Creative output is mystical, abstract, or spiritually inspired. Speculative losses teach non-attachment. "
            "Mantra practice, especially Ketu-related mantras, yields extraordinary spiritual progress."
        ),
        6: (
            "Ketu Mahadasha with Ketu in the 6th house is excellent for spiritual victory over enemies and disease. "
            "Mysterious healing abilities develop. Enemies are neutralised through spiritual means rather than confrontation. "
            "Health issues may involve unusual diagnoses but respond to alternative healing. "
            "Service becomes selfless and karmically liberating. This is one of Ketu's most constructive placements."
        ),
        7: (
            "Ketu Mahadasha with Ketu in the 7th house creates spiritual lessons through partnerships and marriage. "
            "Marriage may feel empty or karmically burdened. Spouse may be spiritually inclined or detached. "
            "Business partnerships dissolve or transform into spiritual collaborations. "
            "The deepest lesson is that union with the divine matters more than any worldly partnership."
        ),
        8: (
            "Ketu Mahadasha with Ketu in the 8th house is profoundly transformative -- moksha-oriented and intensely spiritual. "
            "Mystical experiences, kundalini awakening, and psychic abilities may manifest. "
            "Health crises involving mysterious conditions lead to spiritual breakthroughs. "
            "Inheritance karma resolves. This is one of the most powerful placements for spiritual liberation and occult mastery."
        ),
        9: (
            "Ketu Mahadasha with Ketu in the 9th house challenges conventional religion and builds personal spiritual philosophy. "
            "Father's health or fortune may decline. Traditional religious practices feel empty. "
            "Pilgrimage to unusual or remote spiritual sites is indicated. Foreign spiritual teachers guide your path. "
            "This period replaces inherited belief with direct spiritual experience and personal realisation."
        ),
        10: (
            "Ketu Mahadasha with Ketu in the 10th house creates detachment from career and worldly ambition. "
            "Professional reputation may suffer or shift dramatically. Interest in spiritual vocation increases. "
            "Government or corporate positions lose appeal. Alternative or spiritual career paths emerge. "
            "This period teaches that lasting legacy comes through spiritual service, not worldly achievement."
        ),
        11: (
            "Ketu Mahadasha with Ketu in the 11th house reduces material desires and transforms social connections. "
            "Income fluctuates as attachment to money decreases. Friendships become spiritually oriented. "
            "Elder siblings' karma affects you. Desires fulfilled in this period carry a quality of hollowness "
            "that teaches the ultimate lesson: fulfilment comes from within, not from external achievement."
        ),
        12: (
            "Ketu Mahadasha with Ketu in the 12th house is the ultimate moksha placement -- total spiritual liberation potential. "
            "Foreign spiritual journeys, prolonged meditation retreats, and complete worldly detachment are indicated. "
            "Health issues dissolve through spiritual healing. Expenditure is on spiritual causes exclusively. "
            "This is the rarest and most powerful placement for enlightenment, samadhi, and final liberation of the soul."
        ),
    },
}

from typing import Dict, Any, Tuple

DASHA_INTERPRETATIONS: Dict[str, Dict[str, Any]] = {'Sun': {'general': [{'en': 'Rise in authority, government favour and '
                            'recognition',
                      'hi': 'अधिकार, सरकारी पक्ष और मान्यता में वृद्धि'},
                     {'en': 'Improved health and vitality, recovery from '
                            'chronic ailments',
                      'hi': 'बेहतर स्वास्थ्य और जीवन शक्ति, पुरानी बीमारियों '
                            'से रिकवरी'},
                     {'en': 'Relations with father become significant (good or '
                            'strained based on dignity)',
                      'hi': 'पिता के साथ संबंध महत्वपूर्ण हो जाते हैं (सम्मान '
                            'के आधार पर अच्छे या तनावपूर्ण)'},
                     {'en': 'Career advancement, especially in leadership and '
                            'administrative roles',
                      'hi': 'कैरियर में उन्नति, विशेषकर नेतृत्व और प्रशासनिक '
                            'भूमिकाओं में'},
                     {'en': 'Increased self-confidence and assertiveness',
                      'hi': 'आत्मविश्वास और दृढ़ता में वृद्धि'},
                     {'en': 'Possible conflicts with authority if Sun is '
                            'afflicted',
                      'hi': 'सूर्य के पीड़ित होने पर अधिकारियों से टकराव संभव '
                            'है'},
                     {'en': 'Heart and eye health require attention',
                      'hi': 'हृदय और नेत्र स्वास्थ्य पर ध्यान देने की आवश्यकता '
                            'है'}],
         'specific_good': [{'en': 'Promotion and recognition in government or '
                                  'corporate sectors',
                            'hi': 'सरकारी या कॉर्पोरेट क्षेत्रों में पदोन्नति '
                                  'और मान्यता'},
                           {'en': 'Pilgrimage and religious activities bring '
                                  'peace',
                            'hi': 'तीर्थयात्रा और धार्मिक गतिविधियों से शांति '
                                  'मिलती है'},
                           {'en': 'Children prosper and bring pride',
                            'hi': 'बच्चे समृद्ध होते हैं और गौरव लाते हैं'},
                           {'en': 'Political connections strengthen social '
                                  'standing',
                            'hi': 'राजनीतिक संबंध सामाजिक प्रतिष्ठा को मजबूत '
                                  'करते हैं'}],
         'specific_bad': [{'en': 'Ego conflicts with superiors and father',
                           'hi': 'वरिष्ठजनों एवं पिता से अहंकार का टकराव होता '
                                 'है'},
                          {'en': 'Eye problems, heart ailments, bone weakness',
                           'hi': 'आंखों की समस्या, हृदय रोग, हड्डियों की '
                                 'कमजोरी'},
                          {'en': 'Government penalties or tax issues if Sun is '
                                 'afflicted',
                           'hi': 'सूर्य के पीड़ित होने पर सरकारी जुर्माना या '
                                 'कर संबंधी समस्याएं आती हैं'},
                          {'en': 'Separation from family or loss of position '
                                 'in extreme cases',
                           'hi': 'चरम मामलों में परिवार से अलगाव या पद की '
                                 'हानि'}]},
 'Moon': {'general': [{'en': 'Emotional sensitivity heightened, mood '
                             'fluctuations increase',
                       'hi': 'भावनात्मक संवेदनशीलता बढ़ जाती है, मनोदशा में '
                             'उतार-चढ़ाव बढ़ जाता है'},
                      {'en': "Mother's influence and well-being become central "
                             'themes',
                       'hi': 'माँ का प्रभाव और कल्याण केंद्रीय विषय बन जाते '
                             'हैं'},
                      {'en': 'Travel, especially overseas or to water bodies',
                       'hi': 'यात्रा, विशेषकर विदेश या जलाशयों की यात्रा'},
                      {'en': "Mental peace depends on Moon's dignity -- calm "
                             'if strong, anxious if weak',
                       'hi': 'मानसिक शांति चंद्रमा की गरिमा पर निर्भर करती है '
                             '- मजबूत होने पर शांत, कमजोर होने पर चिंतित'},
                      {'en': 'Gains through public, women, and liquid-related '
                             'businesses',
                       'hi': 'सार्वजनिक, महिलाओं और तरल-संबंधी व्यवसायों से '
                             'लाभ'},
                      {'en': 'Interest in agriculture, hospitality, nursing, '
                             'or caregiving',
                       'hi': 'कृषि, आतिथ्य, नर्सिंग या देखभाल में रुचि'},
                      {'en': 'Dreams become vivid and psychic sensitivity '
                             'increases',
                       'hi': 'सपने ज्वलंत हो जाते हैं और मानसिक संवेदनशीलता '
                             'बढ़ जाती है'}],
          'specific_good': [{'en': 'Happy domestic life, property and vehicle '
                                   'acquisition',
                             'hi': 'सुखी घरेलू जीवन, संपत्ति और वाहन की '
                                   'प्राप्ति'},
                            {'en': "Mother's blessings and support",
                             'hi': 'माँ का आशीर्वाद और सहयोग'},
                            {'en': 'Popularity with masses, public-facing '
                                   'success',
                             'hi': 'जनता के बीच लोकप्रियता, जनता के सामने '
                                   'सफलता'},
                            {'en': 'Marriage and romantic fulfilment if of '
                                   'marriageable age',
                             'hi': 'यदि विवाह योग्य उम्र हो तो विवाह और '
                                   'रोमांटिक संतुष्टि'}],
          'specific_bad': [{'en': 'Anxiety, depression, insomnia if Moon is '
                                  'weak or afflicted',
                            'hi': 'चंद्रमा के कमजोर या पीड़ित होने पर चिंता, '
                                  'अवसाद, अनिद्रा होती है'},
                           {'en': 'Cold, cough, water-borne diseases',
                            'hi': 'सर्दी, खांसी, जल जनित रोग'},
                           {'en': "Mother's health may decline",
                            'hi': 'माता के स्वास्थ्य में गिरावट आ सकती है'},
                           {'en': 'Emotional instability leading to poor '
                                  'decisions',
                            'hi': 'भावनात्मक अस्थिरता के कारण ग़लत निर्णय लिए '
                                  'जा सकते हैं'}]},
 'Mars': {'general': [{'en': 'Energy and courage increase dramatically',
                       'hi': 'ऊर्जा और साहस में नाटकीय रूप से वृद्धि होती है'},
                      {'en': 'Property and land transactions become prominent',
                       'hi': 'संपत्ति और भूमि लेनदेन प्रमुख हो जाते हैं'},
                      {'en': 'Brothers and siblings come into focus (support '
                             'or conflict)',
                       'hi': 'भाई-बहन फोकस में आते हैं (समर्थन या संघर्ष)'},
                      {'en': 'Career in technical, military, police, surgery, '
                             'or engineering thrives',
                       'hi': 'तकनीकी, सैन्य, पुलिस, सर्जरी या इंजीनियरिंग में '
                             'करियर फलता-फूलता है'},
                      {'en': 'Physical activity increases; sports and exercise '
                             'benefit',
                       'hi': 'शारीरिक गतिविधि बढ़ जाती है; खेल और व्यायाम से '
                             'लाभ'},
                      {'en': 'Risk of accidents, surgery, and injuries rises',
                       'hi': 'दुर्घटनाओं, सर्जरी और चोटों का खतरा बढ़ जाता है'},
                      {'en': 'Legal disputes and conflicts with authority '
                             'possible',
                       'hi': 'कानूनी विवाद और अधिकारियों से टकराव संभव'}],
          'specific_good': [{'en': 'Property purchase, construction, or land '
                                   'deals succeed',
                             'hi': 'संपत्ति खरीद, निर्माण या भूमि सौदे सफल '
                                   'होते हैं'},
                            {'en': 'Victory over enemies and competitors',
                             'hi': 'शत्रुओं और प्रतिस्पर्धियों पर विजय'},
                            {'en': 'Technical and engineering projects produce '
                                   'results',
                             'hi': 'तकनीकी और इंजीनियरिंग परियोजनाएँ परिणाम '
                                   'देती हैं'},
                            {'en': 'Blood disorders resolve, physical fitness '
                                   'improves',
                             'hi': 'रक्त विकार दूर होते हैं, शारीरिक स्वस्थता '
                                   'बढ़ती है'}],
          'specific_bad': [{'en': 'Accidents, burns, cuts, or surgery',
                            'hi': 'दुर्घटनाएँ, जलना, कटना, या सर्जरी'},
                           {'en': 'Marital conflicts and aggression at home',
                            'hi': 'वैवाहिक कलह और घर में आक्रामकता'},
                           {'en': 'Blood pressure, fevers, and inflammatory '
                                  'conditions',
                            'hi': 'रक्तचाप, बुखार और सूजन की स्थिति'},
                           {'en': 'Legal battles, property disputes, or police '
                                  'trouble',
                            'hi': 'कानूनी लड़ाई, संपत्ति विवाद, या पुलिस '
                                  'परेशानी'}]},
 'Mercury': {'general': [{'en': 'Intellectual pursuits, education and '
                                'communication highlighted',
                          'hi': 'बौद्धिक गतिविधियों, शिक्षा और संचार पर प्रकाश '
                                'डाला गया'},
                         {'en': 'Business and trade opportunities expand',
                          'hi': 'व्यवसाय और व्यापार के अवसरों का विस्तार होता '
                                'है'},
                         {'en': 'Writing, media, IT and analytical careers '
                                'flourish',
                          'hi': 'लेखन, मीडिया, आईटी और विश्लेषणात्मक करियर '
                                'फलते-फूलते हैं'},
                         {'en': 'Nervous system and skin health need attention',
                          'hi': 'तंत्रिका तंत्र और त्वचा के स्वास्थ्य पर ध्यान '
                                'देने की आवश्यकता है'},
                         {'en': 'Short travels, networking and social '
                                'interactions increase',
                          'hi': 'छोटी यात्राएँ, नेटवर्किंग और सामाजिक संपर्क '
                                'बढ़ते हैं'},
                         {'en': 'Maternal uncle and friends become important',
                          'hi': 'मामा और मित्र महत्वपूर्ण हो जाते हैं'},
                         {'en': 'Financial acumen sharpens -- good for '
                                'investments',
                          'hi': 'वित्तीय कौशल तेज होता है--निवेश के लिए अच्छा '
                                'है'}],
             'specific_good': [{'en': 'Academic success, degrees, and '
                                      'certifications',
                                'hi': 'शैक्षणिक सफलता, डिग्री और प्रमाणपत्र'},
                               {'en': 'New business ventures and trade '
                                      'partnerships',
                                'hi': 'नए व्यावसायिक उद्यम और व्यापार '
                                      'साझेदारी'},
                               {'en': 'Writing, publishing, or media '
                                      'recognition',
                                'hi': 'लेखन, प्रकाशन, या मीडिया मान्यता'},
                               {'en': 'Children excel in education',
                                'hi': 'बच्चे शिक्षा में उत्कृष्टता प्राप्त '
                                      'करते हैं'}],
             'specific_bad': [{'en': 'Nervous disorders, skin allergies, '
                                     'speech problems',
                               'hi': 'तंत्रिका संबंधी विकार, त्वचा की एलर्जी, '
                                     'बोलने में समस्या'},
                              {'en': 'Overthinking leads to anxiety and '
                                     'insomnia',
                               'hi': 'ज़्यादा सोचने से चिंता और अनिद्रा होती '
                                     'है'},
                              {'en': 'Business fraud or deception from '
                                     'partners',
                               'hi': 'व्यापारिक धोखाधड़ी या साझेदारों से धोखा'},
                              {'en': 'Cousin or friend betrayals',
                               'hi': 'चचेरे भाई या मित्र से विश्वासघात'}]},
 'Jupiter': {'general': [{'en': 'Wisdom, spirituality and fortune increase '
                                'markedly',
                          'hi': 'बुद्धि, आध्यात्मिकता और भाग्य में उल्लेखनीय '
                                'वृद्धि होती है'},
                         {'en': 'Marriage, children, and family expansion',
                          'hi': 'विवाह, बच्चे और परिवार का विस्तार'},
                         {'en': 'Guru or teacher enters life with significant '
                                'guidance',
                          'hi': 'गुरु या शिक्षक महत्वपूर्ण मार्गदर्शन लेकर '
                                'जीवन में प्रवेश करते हैं'},
                         {'en': 'Wealth accumulation through ethical means',
                          'hi': 'नैतिक साधनों से धन संचय'},
                         {'en': 'Higher education, law, religion, or '
                                'philosophy become central',
                          'hi': 'उच्च शिक्षा, कानून, धर्म या दर्शन केंद्र बन '
                                'जाते हैं'},
                         {'en': 'Liver and weight gain need monitoring',
                          'hi': 'लीवर और वजन बढ़ने पर निगरानी की जरूरत है'},
                         {'en': 'Charitable disposition and religious '
                                'activities increase',
                          'hi': 'दानशील प्रवृत्ति और धार्मिक गतिविधियों में '
                                'वृद्धि होती है'}],
             'specific_good': [{'en': 'Marriage, birth of children, and family '
                                      'celebrations',
                                'hi': 'विवाह, बच्चों का जन्म और पारिवारिक '
                                      'उत्सव'},
                               {'en': 'Professional promotion and financial '
                                      'prosperity',
                                'hi': 'व्यावसायिक पदोन्नति और वित्तीय समृद्धि'},
                               {'en': 'Spiritual initiation or deepening of '
                                      'religious practice',
                                'hi': 'आध्यात्मिक दीक्षा या धार्मिक अभ्यास को '
                                      'गहरा करना'},
                               {'en': 'Foreign travel for education or '
                                      'pilgrimage',
                                'hi': 'शिक्षा या तीर्थयात्रा के लिए विदेश '
                                      'यात्रा'}],
             'specific_bad': [{'en': 'Over-optimism leads to poor financial '
                                     'decisions',
                               'hi': 'अति-आशावाद खराब वित्तीय निर्णयों की ओर '
                                     'ले जाता है'},
                              {'en': 'Liver disorders, diabetes, obesity, or '
                                     'cholesterol issues',
                               'hi': 'लीवर विकार, मधुमेह, मोटापा, या '
                                     'कोलेस्ट्रॉल संबंधी समस्याएं'},
                              {'en': 'Conflicts with religious figures or '
                                     'teachers',
                               'hi': 'धार्मिक हस्तियों या शिक्षकों के साथ '
                                     'संघर्ष'},
                              {'en': 'Legal issues related to education or '
                                     'religious institutions',
                               'hi': 'शिक्षा या धार्मिक संस्थानों से संबंधित '
                                     'कानूनी मुद्दे'}]},
 'Venus': {'general': [{'en': 'Love, marriage, and romantic relationships are '
                              'central themes',
                        'hi': 'प्रेम, विवाह और रोमांटिक रिश्ते केंद्रीय विषय '
                              'हैं'},
                       {'en': 'Material comforts, luxury, and aesthetic '
                              'pleasures increase',
                        'hi': 'भौतिक सुख-सुविधाएं, विलासिता और सौंदर्य संबंधी '
                              'सुखों में वृद्धि होती है'},
                       {'en': 'Artistic and creative talents flourish',
                        'hi': 'कलात्मक एवं रचनात्मक प्रतिभाएँ निखरती हैं'},
                       {'en': 'Vehicles, jewellery, and fine clothing acquired',
                        'hi': 'वाहन, आभूषण और बढ़िया वस्त्र प्राप्त हुए'},
                       {'en': 'Women play significant roles in life events',
                        'hi': 'महिलाएं जीवन की घटनाओं में महत्वपूर्ण भूमिका '
                              'निभाती हैं'},
                       {'en': 'Reproductive health requires attention',
                        'hi': 'प्रजनन स्वास्थ्य पर ध्यान देने की आवश्यकता है'},
                       {'en': 'Social life becomes vibrant and enjoyable',
                        'hi': 'सामाजिक जीवन जीवंत और आनंददायक हो जाता है'}],
           'specific_good': [{'en': 'Happy marriage, romantic fulfilment, and '
                                    'partnership harmony',
                              'hi': 'सुखी विवाह, रोमांटिक संतुष्टि, और '
                                    'साझेदारी में सामंजस्य'},
                             {'en': 'Wealth through arts, fashion, beauty, or '
                                    'luxury goods',
                              'hi': 'कला, फैशन, सौंदर्य, या विलासिता की '
                                    'वस्तुओं के माध्यम से धन'},
                             {'en': 'Acquisition of vehicles, property, and '
                                    'ornaments',
                              'hi': 'वाहन, संपत्ति और आभूषणों का अधिग्रहण'},
                             {'en': 'Travel to beautiful destinations',
                              'hi': 'सुंदर स्थलों की यात्रा करें'}],
           'specific_bad': [{'en': 'Overindulgence in sensual pleasures',
                             'hi': 'कामुक सुखों में अत्यधिक लिप्त होना'},
                            {'en': 'Reproductive and urinary health issues',
                             'hi': 'प्रजनन और मूत्र संबंधी स्वास्थ्य संबंधी '
                                   'समस्याएं'},
                            {'en': 'Marital discord if Venus is afflicted or '
                                   'in dusthana',
                             'hi': 'यदि शुक्र पीड़ित हो या दुःस्थान में हो तो '
                                   'वैवाहिक कलह होती है'},
                            {'en': 'Financial loss through luxury spending or '
                                   'women-related matters',
                             'hi': 'विलासितापूर्ण खर्च या महिला संबंधी मामलों '
                                   'से वित्तीय हानि'}]},
 'Saturn': {'general': [{'en': 'Hard work, discipline and perseverance define '
                               'this period',
                         'hi': 'कड़ी मेहनत, अनुशासन और दृढ़ता इस अवधि को '
                               'परिभाषित करती है'},
                        {'en': 'Karma manifests -- rewards for past effort or '
                               'consequences of neglect',
                         'hi': 'कर्म प्रकट होता है - पिछले प्रयास का पुरस्कार '
                               'या उपेक्षा का परिणाम'},
                        {'en': 'Career in service, manufacturing, mining, '
                               'agriculture, or law',
                         'hi': 'सेवा, विनिर्माण, खनन, कृषि, या कानून में '
                               'करियर'},
                        {'en': 'Chronic health issues surface; joints, bones, '
                               'and teeth affected',
                         'hi': 'पुरानी स्वास्थ्य समस्याएं सतह पर; जोड़, '
                               'हड्डियाँ और दाँत प्रभावित'},
                        {'en': 'Delays and obstacles test patience and '
                               'endurance',
                         'hi': 'देरी और बाधाएँ धैर्य और सहनशक्ति की परीक्षा '
                               'लेती हैं'},
                        {'en': 'Separation from family or loved ones possible',
                         'hi': 'परिवार या प्रियजनों से अलगाव संभव'},
                        {'en': 'Spiritual maturity through suffering and '
                               'discipline',
                         'hi': 'कष्ट और अनुशासन के माध्यम से आध्यात्मिक '
                               'परिपक्वता'},
                        {'en': 'Democratic or servant-leadership roles emerge',
                         'hi': 'लोकतांत्रिक या सेवक-नेतृत्व की भूमिकाएँ उभरती '
                               'हैं'}],
            'specific_good': [{'en': 'Lasting career achievements after '
                                     'initial struggle',
                               'hi': 'शुरुआती संघर्ष के बाद करियर में स्थायी '
                                     'उपलब्धियां'},
                              {'en': 'Property from sustained effort or '
                                     'inheritance',
                               'hi': 'निरंतर प्रयास या विरासत से प्राप्त '
                                     'संपत्ति'},
                              {'en': 'Spiritual depth and philosophical '
                                     'maturity',
                               'hi': 'आध्यात्मिक गहराई और दार्शनिक परिपक्वता'},
                              {'en': 'Service to society brings recognition',
                               'hi': 'समाज की सेवा से पहचान मिलती है'}],
            'specific_bad': [{'en': 'Chronic ailments: arthritis, knee pain, '
                                    'dental problems',
                              'hi': 'पुरानी बीमारियाँ: गठिया, घुटने का दर्द, '
                                    'दाँत की समस्याएँ'},
                             {'en': 'Depression, loneliness, and pessimism',
                              'hi': 'अवसाद, अकेलापन और निराशावाद'},
                             {'en': 'Financial losses through litigation or '
                                    'government penalties',
                              'hi': 'मुकदमेबाजी या सरकारी दंड के माध्यम से '
                                    'वित्तीय हानि'},
                             {'en': 'Separation from family, exile, or '
                                    'demotion',
                              'hi': 'परिवार से अलगाव, निर्वासन, या पदावनति'}]},
 'Rahu': {'general': [{'en': 'Unconventional path, breaking from tradition',
                       'hi': 'अपरंपरागत मार्ग, परंपरा से हटकर'},
                      {'en': 'Foreign connections, travel, or residence abroad',
                       'hi': 'विदेशी संबंध, यात्रा, या विदेश में निवास'},
                      {'en': 'Technology, media, and modern industries offer '
                             'success',
                       'hi': 'प्रौद्योगिकी, मीडिया और आधुनिक उद्योग सफलता '
                             'प्रदान करते हैं'},
                      {'en': 'Confusion, deception, and illusion test '
                             'discernment',
                       'hi': 'भ्रम, धोखा और भ्रम विवेक का परीक्षण करते हैं'},
                      {'en': 'Obsessive desires and worldly ambitions '
                             'intensify',
                       'hi': 'जुनूनी इच्छाएं और सांसारिक महत्वाकांक्षाएं तीव्र '
                             'हो जाती हैं'},
                      {'en': 'Health: mysterious ailments, poisoning risk, '
                             'mental fog',
                       'hi': 'स्वास्थ्य: रहस्यमय बीमारियाँ, जहर का खतरा, '
                             'मानसिक कोहरा'},
                      {'en': 'Sudden rise or fall in status possible',
                       'hi': 'पद में अचानक वृद्धि या गिरावट संभव'}],
          'specific_good': [{'en': 'Breakthrough in technology, media, or '
                                   'foreign business',
                             'hi': 'प्रौद्योगिकी, मीडिया, या विदेशी व्यापार '
                                   'में सफलता'},
                            {'en': 'Political power or public influence '
                                   'through unconventional means',
                             'hi': 'अपरंपरागत तरीकों से राजनीतिक शक्ति या '
                                   'सार्वजनिक प्रभाव'},
                            {'en': 'Foreign travel and settlement',
                             'hi': 'विदेश यात्रा एवं निपटान'},
                            {'en': 'Gains through speculation or stock market',
                             'hi': 'सट्टेबाजी या शेयर बाज़ार से लाभ'}],
          'specific_bad': [{'en': 'Deception, fraud, or scandal involving '
                                  'others or self',
                            'hi': 'दूसरों या स्वयं से जुड़ा धोखा, धोखाधड़ी या '
                                  'घोटाला'},
                           {'en': 'Mysterious diseases, food poisoning, snake '
                                  'bite',
                            'hi': 'रहस्यमय बीमारियाँ, भोजन विषाक्तता, साँप का '
                                  'काटना'},
                           {'en': 'Family estrangement, marital breakdown',
                            'hi': 'पारिवारिक अलगाव, वैवाहिक विघटन'},
                           {'en': 'Sudden loss of reputation or wealth',
                            'hi': 'अचानक प्रतिष्ठा या धन की हानि'}]},
 'Ketu': {'general': [{'en': 'Spiritual awakening and detachment from material '
                             'world',
                       'hi': 'आध्यात्मिक जागृति और भौतिक संसार से वैराग्य'},
                      {'en': 'Past-life karmas manifest -- sudden events '
                             'without clear cause',
                       'hi': 'पिछले जीवन के कर्म प्रकट होते हैं - बिना किसी '
                             'स्पष्ट कारण के अचानक होने वाली घटनाएँ'},
                      {'en': 'Interest in meditation, yoga, moksha, and occult '
                             'sciences',
                       'hi': 'ध्यान, योग, मोक्ष और गुप्त विज्ञान में रुचि'},
                      {'en': 'Health: digestive issues, mysterious fevers, '
                             'wounds',
                       'hi': 'स्वास्थ्य: पाचन संबंधी समस्याएं, रहस्यमय बुखार, '
                             'घाव'},
                      {'en': 'Loss of worldly comforts pushes toward inner '
                             'growth',
                       'hi': 'सांसारिक सुख-सुविधाओं की हानि आंतरिक विकास की ओर '
                             'धकेलती है'},
                      {'en': 'Isolation, introspection, and withdrawal from '
                             'society',
                       'hi': 'अलगाव, आत्मनिरीक्षण और समाज से अलगाव'},
                      {'en': 'Technical and research skills sharpen',
                       'hi': 'तकनीकी और अनुसंधान कौशल तेज होते हैं'}],
          'specific_good': [{'en': 'Spiritual enlightenment and liberation '
                                   'experiences',
                             'hi': 'आध्यात्मिक ज्ञान और मुक्ति के अनुभव'},
                            {'en': 'Success in research, technology, and '
                                   'occult sciences',
                             'hi': 'अनुसंधान, प्रौद्योगिकी और गुप्त विज्ञान '
                                   'में सफलता'},
                            {'en': 'Past-life skills (healing, languages, '
                                   'arts) reawaken',
                             'hi': 'पिछले जीवन के कौशल (उपचार, भाषाएँ, कला) '
                                   'पुनः जागृत होते हैं'},
                            {'en': 'Detachment resolves long-standing material '
                                   'problems',
                             'hi': 'वैराग्य लंबे समय से चली आ रही भौतिक '
                                   'समस्याओं का समाधान करता है'}],
          'specific_bad': [{'en': 'Mysterious chronic ailments, surgery, or '
                                  'accidents',
                            'hi': 'रहस्यमय पुरानी बीमारियाँ, सर्जरी, या '
                                  'दुर्घटनाएँ'},
                           {'en': 'Loss of position, wealth, or family support',
                            'hi': 'पद, धन, या पारिवारिक समर्थन की हानि'},
                           {'en': 'Mental confusion, hallucinations if '
                                  'afflicted',
                            'hi': 'पीड़ित होने पर मानसिक भ्रम, मतिभ्रम'},
                           {'en': 'Scandal or disgrace from past actions '
                                  'surfacing',
                            'hi': 'पिछले कार्यों से लांछन या अपमान सामने '
                                  'आना'}]}}

ANTARDASHA_INTERPRETATIONS: Dict[Tuple[str, str], Any] = {('Sun', 'Sun'): {'en': 'Peak of self-expression and authority. Government '
                        "favour. Father's role is significant. Health "
                        'generally good if Sun is strong.',
                  'hi': 'आत्म-अभिव्यक्ति और अधिकार का शिखर। सरकारी मेहरबानी. '
                        'पिता की भूमिका अहम है. यदि सूर्य मजबूत हो तो '
                        'स्वास्थ्य आमतौर पर अच्छा रहता है।'},
 ('Sun', 'Moon'): {'en': 'Emotional sensitivity rises. Mother and public '
                         'relations become important. Travel for work. Mood '
                         'fluctuations affect authority.',
                   'hi': 'भावनात्मक संवेदनशीलता बढ़ती है. माँ और जनसंपर्क '
                         'महत्वपूर्ण हो जाते हैं। काम के सिलसिले में यात्रा '
                         'करें। मनोदशा में उतार-चढ़ाव अधिकार को प्रभावित करता '
                         'है।'},
 ('Sun', 'Mars'): {'en': 'Courage and energy combine with authority. Property '
                         'gains, technical projects succeed. Risk of conflicts '
                         'with authority and blood-related health issues.',
                   'hi': 'साहस और ऊर्जा अधिकार के साथ जुड़ते हैं। संपत्ति लाभ, '
                         'तकनीकी परियोजनाएं सफल होती हैं। अधिकारियों के साथ '
                         'संघर्ष और रक्त संबंधी स्वास्थ्य समस्याओं का जोखिम।'},
 ('Sun', 'Mercury'): {'en': 'Intellectual pursuits shine. Business acumen '
                            'combines with authority. Good for examinations, '
                            'writing, and trade. Skin or nervous issues '
                            'possible.',
                      'hi': 'बौद्धिक गतिविधियाँ चमकती हैं। व्यावसायिक कौशल '
                            'अधिकार के साथ जुड़ता है। परीक्षा, लेखन और व्यापार '
                            'के लिए अच्छा है। त्वचा या तंत्रिका संबंधी समस्या '
                            'संभव।'},
 ('Sun', 'Jupiter'): {'en': 'Highly auspicious -- wisdom, wealth and '
                            "recognition. Guru's blessings. Promotion, "
                            'children prosper. Spiritual and material growth '
                            'together.',
                      'hi': 'अत्यधिक शुभ--बुद्धि, धन और पहचान। गुरु का '
                            'आशीर्वाद. पदोन्नति, संतान की उन्नति. आध्यात्मिक '
                            'और भौतिक विकास एक साथ।'},
 ('Sun', 'Venus'): {'en': 'Luxury, comfort and romantic fulfilment. Creative '
                          'expression enhanced. Vehicles and ornaments '
                          'acquired. Reproductive health needs attention.',
                    'hi': 'विलासिता, आराम और रोमांटिक पूर्ति। रचनात्मक '
                          'अभिव्यक्ति बढ़ी. वाहन एवं आभूषण प्राप्त हुए। प्रजनन '
                          'स्वास्थ्य पर ध्यान देने की जरूरत है.'},
 ('Sun', 'Saturn'): {'en': 'Hard work meets authority. Delays in recognition. '
                           "Father's health may suffer. Bone, joint, or eye "
                           'ailments possible. Karmic lessons.',
                     'hi': 'कड़ी मेहनत से अधिकार मिलते हैं। पहचान में देरी. '
                           'पिता का स्वास्थ्य खराब हो सकता है। हड्डी, जोड़ या '
                           'नेत्र रोग संभव। कर्म पाठ.'},
 ('Sun', 'Rahu'): {'en': 'Unconventional rise in authority. Foreign '
                         'connections benefit career. Risk of ego-driven '
                         'mistakes and sudden reputation damage.',
                   'hi': 'अधिकार में अपरंपरागत वृद्धि. विदेशी संपर्कों से '
                         'करियर में लाभ होता है। अहंकार से प्रेरित गलतियों और '
                         'अचानक प्रतिष्ठा को नुकसान पहुंचने का जोखिम।'},
 ('Sun', 'Ketu'): {'en': 'Spiritual introspection during authoritative period. '
                         'Detachment from ego. Father faces challenges. '
                         'Mysterious health issues possible.',
                   'hi': 'आधिकारिक काल के दौरान आध्यात्मिक आत्मनिरीक्षण। '
                         'अहंकार से वैराग्य. पिता को चुनौतियों का सामना करना '
                         'पड़ता है. रहस्यमय स्वास्थ्य समस्याएं संभव।'},
 ('Moon', 'Moon'): {'en': "Peak emotional period. Mother's role is central. "
                          'Mental peace if Moon is strong; anxiety if weak. '
                          'Property and public gains.',
                    'hi': 'चरम भावनात्मक अवधि. माँ की भूमिका केन्द्रीय है। '
                          'चंद्रमा मजबूत हो तो मानसिक शांति मिलती है। चिंता '
                          'अगर कमजोर है. संपत्ति और सार्वजनिक लाभ.'},
 ('Moon', 'Mars'): {'en': 'Emotional energy channelled into action. Property '
                          'deals and courage. Emotional conflicts at home. '
                          'Blood pressure and stomach issues.',
                    'hi': 'भावनात्मक ऊर्जा को क्रियान्वित किया गया। संपत्ति के '
                          'सौदे एवं साहस। घर में भावनात्मक संघर्ष। रक्तचाप और '
                          'पेट की समस्या.'},
 ('Moon', 'Mercury'): {'en': 'Intellectual clarity improves. Good for '
                             'business, communication and education. '
                             'Mother-related travel. Mental agility is sharp.',
                       'hi': 'बौद्धिक स्पष्टता में सुधार होता है। व्यवसाय, '
                             'संचार और शिक्षा के लिए अच्छा है। माता संबंधी '
                             'यात्रा. मानसिक चपलता तीव्र होती है.'},
 ('Moon', 'Jupiter'): {'en': 'Very auspicious -- emotional wisdom, family '
                             'expansion. Marriage or childbirth likely. Mother '
                             'is well. Spiritual contentment.',
                       'hi': 'अत्यंत शुभ--भावनात्मक बुद्धि, पारिवारिक विस्तार। '
                             'विवाह या संतानोत्पत्ति की संभावना। मां ठीक हैं. '
                             'आध्यात्मिक संतुष्टि.'},
 ('Moon', 'Venus'): {'en': 'Romantic fulfilment, luxury and aesthetic '
                           'pleasures. Emotional bond with partner deepens. '
                           'Women play beneficial roles.',
                     'hi': 'रोमांटिक संतुष्टि, विलासिता और सौंदर्य सुख। '
                           'पार्टनर के साथ भावनात्मक रिश्ता गहरा होता है। '
                           'महिलाएं लाभकारी भूमिका निभाती हैं।'},
 ('Moon', 'Saturn'): {'en': 'Emotional heaviness, depression tendency. '
                            "Mother's health may suffer. Delays in domestic "
                            'matters. Hard work needed for peace.',
                      'hi': 'भावनात्मक भारीपन, अवसाद की प्रवृत्ति। माता का '
                            'स्वास्थ्य ख़राब हो सकता है। घरेलू मामलों में '
                            'देरी. शांति के लिए कड़ी मेहनत की जरूरत.'},
 ('Moon', 'Rahu'): {'en': 'Mental confusion and emotional turbulence. Foreign '
                          'travel. Mother faces unusual challenges. Nightmares '
                          'and anxiety increase.',
                    'hi': 'मानसिक भ्रम और भावनात्मक उथल-पुथल. विदेश यात्रा. '
                          'माँ को असामान्य चुनौतियों का सामना करना पड़ता है। '
                          'बुरे सपने और चिंता बढ़ जाती है।'},
 ('Moon', 'Ketu'): {'en': 'Emotional detachment, spiritual seeking. Mother '
                          'faces health issues. Psychic experiences intensify. '
                          'Stomach and chest ailments.',
                    'hi': 'भावनात्मक वैराग्य, आध्यात्मिक खोज। माता को '
                          'स्वास्थ्य संबंधी परेशानियां रहती हैं। मानसिक अनुभव '
                          'तीव्र हो जाते हैं। पेट और छाती के रोग।'},
 ('Moon', 'Sun'): {'en': 'Authority and emotions intersect. Public '
                         'recognition. Father and mother both influential. '
                         'Health and vitality improve.',
                   'hi': 'अधिकार और भावनाएँ प्रतिच्छेद करती हैं। सार्वजनिक '
                         'मान्यता। पिता और माता दोनों प्रभावशाली. स्वास्थ्य और '
                         'जीवन शक्ति में सुधार होता है।'},
 ('Mars', 'Mars'): {'en': 'Peak energy and courage. Property transactions. '
                          'Risk of accidents, cuts, burns. Victory over '
                          'enemies. Physical fitness improves.',
                    'hi': 'चरम ऊर्जा और साहस. संपत्ति लेनदेन. दुर्घटना, कटने, '
                          'जलने का खतरा। शत्रुओं पर विजय. शारीरिक फिटनेस में '
                          'सुधार होता है।'},
 ('Mars', 'Mercury'): {'en': 'Technical intellect shines. Property deals '
                             'through negotiation. Business partnerships in '
                             'engineering or technology.',
                       'hi': 'तकनीकी बुद्धि चमकती है. संपत्ति का सौदा बातचीत '
                             'से होता है। इंजीनियरिंग या प्रौद्योगिकी में '
                             'व्यावसायिक साझेदारी।'},
 ('Mars', 'Jupiter'): {'en': 'Auspicious -- dharmic courage. Property through '
                             'fortune. Brothers prosper. Children and '
                             'education benefit. Legal victory.',
                       'hi': 'शुभ--धार्मिक साहस. भाग्य से संपत्ति. भाइयों की '
                             'उन्नति हो. संतान और शिक्षा से लाभ होता है। '
                             'कानूनी जीत.'},
 ('Mars', 'Venus'): {'en': 'Passion and luxury combine. Romantic relationships '
                           'intensify. Property acquisition. Reproductive '
                           'health needs attention.',
                     'hi': 'जुनून और विलासिता का मेल। रोमांटिक रिश्ते प्रगाढ़ '
                           'होते हैं। संपत्ति अधिग्रहण. प्रजनन स्वास्थ्य पर '
                           'ध्यान देने की जरूरत है.'},
 ('Mars', 'Saturn'): {'en': 'Conflict between energy and restriction. '
                            'Accidents or surgery risk. Property disputes. '
                            'Joint and bone injuries possible.',
                      'hi': 'ऊर्जा और प्रतिबंध के बीच संघर्ष. दुर्घटना या '
                            'सर्जरी का जोखिम. संपत्ति विवाद. जोड़ एवं हड्डी '
                            'में चोट संभव।'},
 ('Mars', 'Rahu'): {'en': 'Reckless courage and unconventional action. Foreign '
                          'property dealings. Risk of explosions, accidents, '
                          'or deception.',
                    'hi': 'लापरवाह साहस और अपरंपरागत कार्रवाई. विदेशी संपत्ति '
                          'का लेन-देन. विस्फोट, दुर्घटना या धोखे का जोखिम।'},
 ('Mars', 'Ketu'): {'en': 'Spiritual warrior energy. Past-life martial skills '
                          'resurface. Surgery or accident risk. Detachment '
                          'from material aggression.',
                    'hi': 'आध्यात्मिक योद्धा ऊर्जा. पिछले जीवन का मार्शल कौशल '
                          'फिर से उभर आया है। सर्जरी या दुर्घटना का जोखिम. '
                          'भौतिक आक्रामकता से अलगाव.'},
 ('Mars', 'Sun'): {'en': 'Authority and courage combine. Government property. '
                         'Father and brothers interact. Leadership in '
                         'competitive fields.',
                   'hi': 'अधिकार और साहस का मेल है। सरकारी संपत्ति. पिता और '
                         'भाई आपस में बातचीत करते हैं. प्रतिस्पर्धी क्षेत्रों '
                         'में नेतृत्व.'},
 ('Mars', 'Moon'): {'en': 'Emotional courage. Mother and property connected. '
                          'Domestic energy high. Stomach and blood pressure '
                          'issues possible.',
                    'hi': 'भावनात्मक साहस. माँ और संपत्ति जुड़े हुए हैं. घरेलू '
                          'ऊर्जा उच्च. पेट एवं रक्तचाप की समस्या संभव।'},
 ('Mercury', 'Mercury'): {'en': 'Peak intellectual period. Business '
                                'flourishes. Communication and networking at '
                                'their best. Skin and nervous health need '
                                'care.',
                          'hi': 'चरम बौद्धिक काल. व्यापार फलता-फूलता है. संचार '
                                'और नेटवर्किंग अपने सर्वोत्तम स्तर पर। त्वचा '
                                'और तंत्रिका स्वास्थ्य को देखभाल की ज़रूरत '
                                'है।'},
 ('Mercury', 'Jupiter'): {'en': 'Wisdom and intellect combine beautifully. '
                                'Education, publishing, legal success. '
                                'Financial growth through ethical business.',
                          'hi': 'बुद्धि और बुद्धि का सुन्दर मेल होता है। '
                                'शिक्षा, प्रकाशन, कानूनी सफलता। नैतिक व्यवसाय '
                                'के माध्यम से वित्तीय विकास।'},
 ('Mercury', 'Venus'): {'en': 'Creative communication and artistic business. '
                              'Fashion, media, and design succeed. Romantic '
                              'correspondence. Social life vibrant.',
                        'hi': 'रचनात्मक संचार और कलात्मक व्यवसाय। फ़ैशन, '
                              'मीडिया और डिज़ाइन सफल हैं। रोमांटिक पत्राचार. '
                              'सामाजिक जीवन जीवंत.'},
 ('Mercury', 'Saturn'): {'en': 'Disciplined intellect. Serious study and '
                               'long-term business planning. Nervous '
                               'exhaustion possible. Dental issues.',
                         'hi': 'अनुशासित बुद्धि. गंभीर अध्ययन और दीर्घकालिक '
                               'व्यापार योजना। घबराहट संबंधी थकावट संभव। दंत '
                               'संबंधी समस्याएं.'},
 ('Mercury', 'Rahu'): {'en': 'Unconventional business opportunities. '
                             'Technology and foreign trade. Risk of fraud or '
                             'deception. Mental confusion if afflicted.',
                       'hi': 'अपरंपरागत व्यावसायिक अवसर. प्रौद्योगिकी और '
                             'विदेशी व्यापार. धोखाधड़ी या धोखे का जोखिम. '
                             'पीड़ित होने पर मानसिक भ्रम।'},
 ('Mercury', 'Ketu'): {'en': 'Spiritual intellect, interest in astrology and '
                             'occult study. Communication breakdowns. Skin '
                             'ailments and nervous disorders.',
                       'hi': 'आध्यात्मिक बुद्धि, ज्योतिष और गुप्त अध्ययन में '
                             'रुचि। संचार टूटना. त्वचा रोग और तंत्रिका संबंधी '
                             'विकार।'},
 ('Mercury', 'Sun'): {'en': 'Authority through intellect. Government business. '
                            'Father supports education. Speech commands '
                            'respect.',
                      'hi': 'बुद्धि द्वारा अधिकार। सरकारी कामकाज. पिता शिक्षा '
                            'का समर्थन करते हैं। वाणी सम्मान दिलाती है.'},
 ('Mercury', 'Moon'): {'en': 'Emotional intelligence sharpens. Public '
                             'communication roles. Mother supports business. '
                             'Travel for trade.',
                       'hi': 'भावनात्मक बुद्धिमत्ता तीव्र होती है। सार्वजनिक '
                             'संचार भूमिकाएँ. मां बिजनेस में सहयोग करती हैं. '
                             'व्यापार के लिए यात्रा करें।'},
 ('Mercury', 'Mars'): {'en': 'Technical communication and engineering '
                             'intellect. Property negotiations. Sibling '
                             'business partnerships. Arguments possible.',
                       'hi': 'तकनीकी संचार और इंजीनियरिंग बुद्धि। संपत्ति '
                             'वार्ता. भाई-बहन की व्यावसायिक साझेदारी। '
                             'तर्क-वितर्क संभव.'},
 ('Jupiter', 'Jupiter'): {'en': 'Peak of wisdom, fortune and expansion. '
                                'Marriage, children, wealth all prosper. '
                                "Guru's grace is strongest. Spiritual growth.",
                          'hi': 'ज्ञान, भाग्य और विस्तार का शिखर। विवाह, '
                                'बच्चे, धन सभी समृद्ध होते हैं। गुरु की कृपा '
                                'सबसे प्रबल है. आध्यात्मिक विकास.'},
 ('Jupiter', 'Venus'): {'en': 'Wealth and luxury through wisdom. Happy '
                              'marriage. Artistic and creative prosperity. '
                              'Vehicles and ornaments. Social prestige.',
                        'hi': 'बुद्धि से धन और विलासिता। शुभ विवाह। कलात्मक '
                              'एवं रचनात्मक समृद्धि. वाहन और आभूषण. सामाजिक '
                              'प्रतिष्ठा.'},
 ('Jupiter', 'Saturn'): {'en': 'Disciplined wisdom. Long-term investments '
                               'mature. Health caution needed -- liver and '
                               'joints. Spiritual lessons through hardship.',
                         'hi': 'अनुशासित बुद्धि. लंबी अवधि के निवेश परिपक्व '
                               'होते हैं. स्वास्थ्य संबंधी सावधानी '
                               'आवश्यक--यकृत और जोड़। कठिनाई के माध्यम से '
                               'आध्यात्मिक शिक्षा.'},
 ('Jupiter', 'Rahu'): {'en': 'Unconventional expansion. Foreign guru or '
                             'education. Risk of misplaced faith. Technology '
                             'and modern ventures through wisdom.',
                       'hi': 'अपरंपरागत विस्तार. विदेशी गुरु या शिक्षा. ग़लत '
                             'विश्वास का ख़तरा. ज्ञान के माध्यम से '
                             'प्रौद्योगिकी और आधुनिक उद्यम।'},
 ('Jupiter', 'Ketu'): {'en': 'Deep spiritual awakening. Detachment from '
                             'material wealth. Meditation and moksha '
                             'practices. Health fluctuations.',
                       'hi': 'गहरी आध्यात्मिक जागृति. भौतिक संपदा से विरक्ति. '
                             'ध्यान और मोक्ष अभ्यास. स्वास्थ्य में '
                             'उतार-चढ़ाव.'},
 ('Jupiter', 'Sun'): {'en': 'Authority blessed by wisdom. Government '
                            'recognition and honour. Father prospers. Career '
                            'promotion through merit.',
                      'hi': 'प्राधिकरण को बुद्धि का आशीर्वाद प्राप्त है। '
                            'सरकारी मान्यता और सम्मान. पिता की उन्नति होती है. '
                            'योग्यता के माध्यम से करियर में उन्नति.'},
 ('Jupiter', 'Moon'): {'en': 'Emotional wisdom and family happiness. Mother is '
                             'well. Property and domestic expansion. Public '
                             'favour.',
                       'hi': 'भावनात्मक ज्ञान और पारिवारिक खुशी। मां ठीक हैं. '
                             'संपत्ति एवं घरेलू विस्तार. जनता का उपकार.'},
 ('Jupiter', 'Mars'): {'en': 'Courageous wisdom. Property through fortune. '
                             'Brothers benefit. Legal and dharmic victories. '
                             'Technical education.',
                       'hi': 'साहसी बुद्धि. भाग्य से संपत्ति. भाइयों से लाभ '
                             'होता है. कानूनी और धार्मिक जीत. तकनीकी शिक्षा।'},
 ('Jupiter', 'Mercury'): {'en': 'Intellectual fortune. Business and education '
                                'prosper simultaneously. Publishing success. '
                                'Children excel academically.',
                          'hi': 'बौद्धिक भाग्य. व्यवसाय और शिक्षा एक साथ '
                                'समृद्ध होते हैं। प्रकाशन सफलता. बच्चे '
                                'शैक्षणिक रूप से उत्कृष्ट होते हैं।'},
 ('Venus', 'Venus'): {'en': 'Peak of luxury, romance, and artistic expression. '
                            'Marriage or renewal of vows. Vehicles, property, '
                            'and wealth. Social prominence.',
                      'hi': 'विलासिता, रोमांस और कलात्मक अभिव्यक्ति का शिखर। '
                            'विवाह या प्रतिज्ञा का नवीनीकरण। वाहन, संपत्ति और '
                            'धन. सामाजिक प्रमुखता.'},
 ('Venus', 'Saturn'): {'en': 'Disciplined luxury. Long-term artistic projects. '
                             'Reproductive and urinary health issues. Delayed '
                             'romantic fulfilment.',
                       'hi': 'अनुशासित विलासिता. दीर्घकालिक कलात्मक '
                             'परियोजनाएँ। प्रजनन और मूत्र संबंधी स्वास्थ्य '
                             'संबंधी समस्याएं. रोमांटिक पूर्ति में देरी।'},
 ('Venus', 'Rahu'): {'en': 'Unconventional romance and foreign luxury. '
                           'Technology in arts. Risk of scandalous affairs. '
                           'Skin and allergy issues.',
                     'hi': 'अपरंपरागत रोमांस और विदेशी विलासिता। कला में '
                           'प्रौद्योगिकी. निंदनीय मामलों का जोखिम. त्वचा और '
                           'एलर्जी संबंधी समस्याएं.'},
 ('Venus', 'Ketu'): {'en': 'Spiritual detachment from pleasures. Past-life '
                           'artistic talents resurface. Romantic '
                           'disappointments lead to growth.',
                     'hi': 'सुखों से आध्यात्मिक वैराग्य. पिछले जीवन की कलात्मक '
                           'प्रतिभाएँ फिर से उभर कर सामने आती हैं। रोमांटिक '
                           'निराशाएँ विकास की ओर ले जाती हैं।'},
 ('Venus', 'Sun'): {'en': 'Authority in creative fields. Government arts '
                          'funding. Glamorous public role. Father and spouse '
                          'dynamics.',
                    'hi': 'रचनात्मक क्षेत्रों में प्राधिकार. सरकारी कला निधि. '
                          'ग्लैमरस सार्वजनिक भूमिका. पिता और जीवनसाथी की '
                          'गतिशीलता.'},
 ('Venus', 'Moon'): {'en': 'Emotional romance and domestic beauty. Mother and '
                           'spouse connected. Home decoration. Water travel.',
                     'hi': 'भावनात्मक रोमांस और घरेलू सुंदरता। माँ और जीवनसाथी '
                           'जुड़े हुए हैं। घर की सजावट. जल यात्रा.'},
 ('Venus', 'Mars'): {'en': 'Passionate romance, bold artistic expression. '
                           'Property acquisition. Reproductive health needs '
                           'care. Energy in creative projects.',
                     'hi': 'भावुक रोमांस, साहसिक कलात्मक अभिव्यक्ति। संपत्ति '
                           'अधिग्रहण. प्रजनन स्वास्थ्य को देखभाल की आवश्यकता '
                           'है। रचनात्मक परियोजनाओं में ऊर्जा.'},
 ('Venus', 'Mercury'): {'en': 'Creative business and artistic communication. '
                              'Fashion, media, and design prosper. Social '
                              'networking expands.',
                        'hi': 'रचनात्मक व्यवसाय और कलात्मक संचार। फैशन, मीडिया '
                              'और डिज़ाइन समृद्ध हुए। सोशल नेटवर्किंग का '
                              'विस्तार हो रहा है.'},
 ('Venus', 'Jupiter'): {'en': 'Wisdom and luxury combined. Happy marriage and '
                              'family expansion. Wealth through ethical '
                              'creative enterprise.',
                        'hi': 'बुद्धि और विलासिता संयुक्त। शुभ विवाह एवं '
                              'परिवार विस्तार। नैतिक रचनात्मक उद्यम के माध्यम '
                              'से धन.'},
 ('Saturn', 'Saturn'): {'en': 'Peak of karma manifestation. Hard work defines '
                              'life. Chronic health issues surface. Lasting '
                              'achievements through discipline.',
                        'hi': 'कर्म अभिव्यक्ति का चरम. कड़ी मेहनत जीवन को '
                              'परिभाषित करती है। पुरानी स्वास्थ्य समस्याएं सतह '
                              'पर। अनुशासन के माध्यम से स्थायी उपलब्धियाँ।'},
 ('Saturn', 'Rahu'): {'en': 'Unconventional hardship. Foreign obstacles. '
                            'Technology and modern challenges. Risk of '
                            'deception during difficult times.',
                      'hi': 'अपरंपरागत कठिनाई. विदेशी बाधाएँ. प्रौद्योगिकी और '
                            'आधुनिक चुनौतियाँ। कठिन समय में धोखे का जोखिम.'},
 ('Saturn', 'Ketu'): {'en': 'Spiritual suffering and deep karmic clearing. '
                            'Health crises lead to detachment. Past-life '
                            'karmas resolve painfully.',
                      'hi': 'आध्यात्मिक पीड़ा और गहन कर्म शुद्धि। स्वास्थ्य '
                            'संकट वैराग्य की ओर ले जाता है। पिछले जीवन के कर्म '
                            'कष्टदायक ढंग से हल होते हैं।'},
 ('Saturn', 'Sun'): {'en': 'Authority restricted by karma. Government '
                           "obstacles. Father's health declines. Eye and bone "
                           'issues. Frustration with hierarchy.',
                     'hi': 'प्राधिकार कर्म द्वारा प्रतिबंधित है। सरकारी '
                           'बाधाएँ. पिता के स्वास्थ्य में गिरावट. आंख और हड्डी '
                           'संबंधी समस्या. पदानुक्रम से निराशा.'},
 ('Saturn', 'Moon'): {'en': "Emotional heaviness and depression. Mother's "
                            'suffering. Domestic hardship. Mental health needs '
                            'serious attention.',
                      'hi': 'भावनात्मक भारीपन और अवसाद. माँ की पीड़ा. घरेलू '
                            'कठिनाई. मानसिक स्वास्थ्य पर गंभीरता से ध्यान देने '
                            'की जरूरत है।'},
 ('Saturn', 'Mars'): {'en': 'Accidents, surgery, and conflicts during '
                            'difficult period. Property disputes. Joint and '
                            'bone injuries. Legal battles.',
                      'hi': 'कठिन अवधि के दौरान दुर्घटनाएं, सर्जरी और संघर्ष। '
                            'संपत्ति विवाद. जोड़ और हड्डी में चोट. कानूनी '
                            'लड़ाई.'},
 ('Saturn', 'Mercury'): {'en': 'Intellectual discipline and serious study. '
                               'Business requires patience. Nervous '
                               'exhaustion. Delayed results.',
                         'hi': 'बौद्धिक अनुशासन और गंभीर अध्ययन. व्यवसाय के '
                               'लिए धैर्य की आवश्यकता होती है। घबराहट भरी '
                               'थकावट. विलंबित परिणाम.'},
 ('Saturn', 'Jupiter'): {'en': 'Wisdom through suffering. Spiritual maturity. '
                               'Financial stability slowly returns. Guru helps '
                               'through hardship.',
                         'hi': 'दुख के माध्यम से बुद्धि. आध्यात्मिक परिपक्वता. '
                               'वित्तीय स्थिरता धीरे-धीरे लौट आती है। गुरु '
                               'कठिनाई में सहायता करते हैं।'},
 ('Saturn', 'Venus'): {'en': 'Artistic discipline bears fruit. Late romantic '
                             'fulfilment. Chronic reproductive issues. '
                             'Vehicles and luxury delayed.',
                       'hi': 'कलात्मक अनुशासन फल देता है. देर से रोमांटिक '
                             'पूर्ति. जीर्ण प्रजनन संबंधी समस्याएं. वाहन एवं '
                             'विलासिता में विलंब।'},
 ('Rahu', 'Rahu'): {'en': 'Peak of worldly obsession and unconventional path. '
                          'Foreign connections strongest. Maximum confusion '
                          'and ambition. Sudden changes.',
                    'hi': 'सांसारिक जुनून और अपरंपरागत पथ का चरम. विदेशी संबंध '
                          'सबसे मजबूत. अधिकतम भ्रम और महत्वाकांक्षा. अचानक '
                          'परिवर्तन.'},
 ('Rahu', 'Ketu'): {'en': 'Spiritual crisis within material obsession. Axis of '
                          'karma activates. Sudden events without logic. '
                          'Health disturbances.',
                    'hi': 'भौतिक जुनून के भीतर आध्यात्मिक संकट। कर्म की धुरी '
                          'सक्रिय हो जाती है. बिना तर्क के अचानक घटनाएँ। '
                          'स्वास्थ्य में गड़बड़ी.'},
 ('Rahu', 'Sun'): {'en': 'Unconventional authority. Foreign government roles. '
                         'Father faces unusual challenges. Ego-driven ambition '
                         'peaks.',
                   'hi': 'अपरंपरागत अधिकार. विदेशी सरकार की भूमिकाएँ. पिता को '
                         'असामान्य चुनौतियों का सामना करना पड़ता है। अहंकार से '
                         'प्रेरित महत्वाकांक्षा चरम पर है।'},
 ('Rahu', 'Moon'): {'en': 'Mental turbulence and emotional confusion. Mother '
                          'faces foreign challenges. Nightmares and psychic '
                          'disturbances.',
                    'hi': 'मानसिक अशांति और भावनात्मक भ्रम। माँ को विदेशी '
                          'चुनौतियों का सामना करना पड़ता है। बुरे सपने और '
                          'मानसिक अशांति.'},
 ('Rahu', 'Mars'): {'en': 'Reckless action and unconventional courage. '
                          'Accidents, explosions, surgery risk. Foreign '
                          'property. Violent disputes.',
                    'hi': 'लापरवाह कार्रवाई और अपरंपरागत साहस. दुर्घटनाएँ, '
                          'विस्फोट, सर्जरी का जोखिम। विदेशी संपत्ति. हिंसक '
                          'विवाद.'},
 ('Rahu', 'Mercury'): {'en': 'Technology and foreign business flourish. Risk '
                             'of intellectual fraud. Media and communication '
                             'breakthroughs.',
                       'hi': 'प्रौद्योगिकी और विदेशी व्यापार फलता-फूलता है। '
                             'बौद्धिक धोखाधड़ी का खतरा. मीडिया और संचार की '
                             'सफलताएँ।'},
 ('Rahu', 'Jupiter'): {'en': 'Unconventional wisdom. Foreign education or '
                             'guru. Expansion through modern means. Risk of '
                             'misplaced faith.',
                       'hi': 'अपरंपरागत ज्ञान. विदेशी शिक्षा या गुरु. आधुनिक '
                             'तरीकों से विस्तार. ग़लत विश्वास का ख़तरा.'},
 ('Rahu', 'Venus'): {'en': 'Foreign romance and unconventional luxury. '
                           'Technology in arts. Scandalous relationships if '
                           'afflicted. Material obsession.',
                     'hi': 'विदेशी रोमांस और अपरंपरागत विलासिता। कला में '
                           'प्रौद्योगिकी. पीड़ित होने पर निंदनीय रिश्ते। भौतिक '
                           'जुनून.'},
 ('Rahu', 'Saturn'): {'en': 'Double malefic period. Extreme hardship and '
                            'karmic lessons. Foreign exile. Chronic ailments '
                            'worsen. Perseverance essential.',
                      'hi': 'दोहरा अशुभ काल. अत्यधिक कठिनाई और कर्म पाठ। '
                            'विदेशी निर्वासन. पुरानी बीमारियाँ बिगड़ जाती हैं। '
                            'दृढ़ता आवश्यक.'},
 ('Ketu', 'Ketu'): {'en': 'Peak of spiritual detachment. Past-life karmas '
                          'culminate. Mysterious events and health issues. '
                          'Moksha-oriented period.',
                    'hi': 'आध्यात्मिक वैराग्य का चरम. पिछले जीवन के कर्म '
                          'समाप्त हो जाते हैं। रहस्यमय घटनाएँ और स्वास्थ्य '
                          'संबंधी समस्याएँ। मोक्षोन्मुख काल।'},
 ('Ketu', 'Sun'): {'en': 'Detachment from authority and ego. Father faces '
                         'spiritual crisis. Loss of position leads to inner '
                         'growth.',
                   'hi': 'अधिकार और अहंकार से अलगाव. पिता को आध्यात्मिक संकट '
                         'का सामना करना पड़ा. पद की हानि से आंतरिक विकास होता '
                         'है।'},
 ('Ketu', 'Moon'): {'en': 'Emotional detachment and psychic sensitivity. '
                          "Mother's health. Mental disturbances. Vivid dreams "
                          'and visions.',
                    'hi': 'भावनात्मक वैराग्य और मानसिक संवेदनशीलता. माता का '
                          'स्वास्थ्य. मानसिक अशांति. ज्वलंत सपने और दर्शन.'},
 ('Ketu', 'Mars'): {'en': 'Spiritual warrior mode. Surgery or accident risk. '
                          'Past-life martial energy surfaces. Detachment from '
                          'aggression.',
                    'hi': 'आध्यात्मिक योद्धा मोड. सर्जरी या दुर्घटना का जोखिम. '
                          'पिछले जीवन की मार्शल ऊर्जा सतह पर है। आक्रामकता से '
                          'अलगाव.'},
 ('Ketu', 'Mercury'): {'en': 'Interest in occult study, astrology, and ancient '
                             'languages. Communication breakdowns. Nervous and '
                             'skin issues.',
                       'hi': 'गुप्त अध्ययन, ज्योतिष एवं प्राचीन भाषाओं में '
                             'रुचि। संचार टूटना. तंत्रिका और त्वचा संबंधी '
                             'समस्याएं.'},
 ('Ketu', 'Jupiter'): {'en': 'Deep spiritual wisdom manifests. Guru appears. '
                             'Detachment brings unexpected fortune. Meditation '
                             'bears fruit.',
                       'hi': 'गहन आध्यात्मिक ज्ञान प्रकट होता है। गुरु प्रकट '
                             'होते हैं. वैराग्य अप्रत्याशित भाग्य लाता है। '
                             'ध्यान फलीभूत होता है.'},
 ('Ketu', 'Venus'): {'en': 'Detachment from romantic and material pleasures. '
                           'Artistic spirituality. Past-life creative talents '
                           'resurface.',
                     'hi': 'रोमांटिक और भौतिक सुखों से अलगाव। कलात्मक '
                           'आध्यात्मिकता. पिछले जीवन की रचनात्मक प्रतिभाएँ फिर '
                           'से उभर कर सामने आती हैं।'},
 ('Ketu', 'Saturn'): {'en': 'Extreme karmic clearing. Health crises and '
                            'isolation. Spiritual suffering has deep purpose. '
                            'Joint and skin ailments.',
                      'hi': 'अत्यधिक कर्म समाशोधन. स्वास्थ्य संकट और अलगाव. '
                            'आध्यात्मिक पीड़ा का गहरा उद्देश्य है. जोड़ों और '
                            'त्वचा के रोग.'},
 ('Ketu', 'Rahu'): {'en': 'Karmic axis fully activated. Confusion between '
                          'spirit and matter. Sudden reversals. Health '
                          'disturbances. Transformation.',
                    'hi': 'कार्मिक अक्ष पूरी तरह से सक्रिय है। आत्मा और पदार्थ '
                          'के बीच भ्रम. अचानक उलटफेर. स्वास्थ्य में गड़बड़ी. '
                          'परिवर्तन.'}}

MANGALA_DOSHA_TEXT: Dict[str, Any] = {'classical_shlokas': [{'source': {'en': 'Agastya Samhita',
                                   'hi': 'अगस्त्य संहिता'},
                        'text': {'en': 'If Mars is placed in the 1st, 4th, '
                                       '7th, 8th, or 12th house from the '
                                       'Lagna, Moon, or Venus, the native is '
                                       'said to have Mangala Dosha (Kuja '
                                       'Dosha). Such placement causes '
                                       'disturbance in marital life and '
                                       'discord with the spouse.',
                                 'hi': 'यदि मंगल लग्न, चंद्रमा या शुक्र से 1, '
                                       '4, 7, 8, या 12वें भाव में स्थित हो, तो '
                                       'जातक को मंगल दोष (कुजा दोष) कहा जाता '
                                       'है। ऐसा स्थान वैवाहिक जीवन में अशांति '
                                       'और जीवनसाथी के साथ कलह का कारण बनता '
                                       'है।'}},
                       {'source': {'en': 'Maanasagari', 'hi': 'मानसागरी'},
                        'text': {'en': 'Mars in the 1st house destroys the '
                                       'spouse. In the 4th, it causes loss of '
                                       'domestic happiness. In the 7th, there '
                                       'is constant strife. In the 8th, the '
                                       'spouse faces chronic illness. In the '
                                       '12th, there is loss of marital bliss.',
                                 'hi': 'प्रथम भाव में मंगल जीवनसाथी को नष्ट कर '
                                       'देता है। चतुर्थ भाव में घरेलू सुख की '
                                       'हानि होती है। 7वें भाव में निरंतर कलह '
                                       'बनी रहती है। 8वें भाव में जीवनसाथी को '
                                       'दीर्घकालिक बीमारी का सामना करना पड़ता '
                                       'है। 12वें भाव में वैवाहिक सुख में कमी '
                                       'आती है।'}},
                       {'source': {'en': 'Brihat Jyotishasara',
                                   'hi': 'बृहत् ज्योतिषसार'},
                        'text': {'en': 'When Mars occupies the said houses '
                                       'from Lagna, Moon or Venus, the native '
                                       'faces widowhood or widowerhood, '
                                       'separation, or chronic marital '
                                       'suffering. Matching charts of both '
                                       'partners is essential.',
                                 'hi': 'जब मंगल लग्न, चंद्रमा या शुक्र से उक्त '
                                       'घरों में होता है, तो जातक को वैधव्य या '
                                       'विधवापन, अलगाव, या दीर्घकालिक वैवाहिक '
                                       'पीड़ा का सामना करना पड़ता है। दोनों '
                                       'भागीदारों के चार्ट का मिलान आवश्यक '
                                       'है।'}},
                       {'source': {'en': 'Bhava Deepika', 'hi': 'भव दीपिका'},
                        'text': {'en': 'Kuja Dosha is neutralized when both '
                                       'partners have Mars in the specified '
                                       'houses. Also cancelled if Mars is in '
                                       'its own sign (Aries, Scorpio), exalted '
                                       '(Capricorn), or aspected by benefics '
                                       '(Jupiter, Venus).',
                                 'hi': 'जब दोनों साझेदारों के निर्दिष्ट घरों '
                                       'में मंगल हो तो कुजा दोष निष्प्रभावी हो '
                                       'जाता है। यदि मंगल अपनी ही राशि (मेष, '
                                       'वृश्चिक), उच्च राशि (मकर) में हो, या '
                                       'शुभ ग्रह (बृहस्पति, शुक्र) से दृष्ट हो '
                                       'तो भी रद्द कर दिया जाता है।'}},
                       {'source': {'en': 'Brihat Parashara Hora Shastra',
                                   'hi': 'बृहत् पाराशर होरा शास्त्र'},
                        'text': {'en': 'The wise should examine Mars from '
                                       'Lagna, Moon, and Venus. If Kuja Dosha '
                                       'exists from all three, it is of the '
                                       'highest severity. From two, it is '
                                       'medium. From one alone, it is mild.',
                                 'hi': 'बुद्धिमानों को लग्न, चन्द्रमा और शुक्र '
                                       'से मंगल का परीक्षण करना चाहिए। यदि '
                                       'कुजा दोष तीनों में से मौजूद है, तो यह '
                                       'उच्चतम गंभीरता का है। दो से यह मध्यम '
                                       'है। एक से ही हल्का है.'}}],
 'results': {'en': 'Mangala Dosha indicates challenges in marital life '
                   'including: delay in marriage, discord between spouses, '
                   'separation or divorce, health issues of the partner, and '
                   'in severe cases, bereavement. The severity depends on the '
                   'house Mars occupies and whether the dosha is from Lagna, '
                   'Moon, Venus, or multiple reference points. Cancellation '
                   'conditions include: Mars in own sign/exalted, both '
                   "partners having equal dosha, Jupiter's aspect on Mars, and "
                   'Mars placed in Aries/Scorpio/Capricorn in the respective '
                   'houses.',
             'hi': 'मंगल दोष वैवाहिक जीवन में चुनौतियों का संकेत देता है '
                   'जिनमें शामिल हैं: विवाह में देरी, पति-पत्नी के बीच कलह, '
                   'अलगाव या तलाक, साथी के स्वास्थ्य संबंधी मुद्दे और गंभीर '
                   'मामलों में, वियोग। गंभीरता इस बात पर निर्भर करती है कि '
                   'मंगल किस घर में है और क्या दोष लग्न, चंद्रमा, शुक्र या कई '
                   'संदर्भ बिंदुओं से है। रद्द करने की शर्तों में शामिल हैं: '
                   'मंगल स्वराशि/उच्च में, दोनों साझेदारों में समान दोष, मंगल '
                   'पर बृहस्पति की दृष्टि, और मंगल संबंधित घरों में '
                   'मेष/वृश्चिक/मकर राशि में स्थित है।'},
 'remedies': {'mantras': [{'en': 'Chant Hanuman Chalisa daily, especially on '
                                 'Tuesdays',
                           'hi': 'प्रतिदिन विशेषकर मंगलवार को हनुमान चालीसा का '
                                 'जाप करें'},
                          {'en': "Recite 'Om Kraam Kreem Kraum Sah Bhaumaya "
                                 "Namah' 108 times daily",
                           'hi': "'ॐ क्रां क्रीं क्रौं सः भौमाय नमः' का "
                                 'प्रतिदिन 108 बार जाप करें'},
                          {'en': 'Navagraha Shanti Puja with special focus on '
                                 'Mars',
                           'hi': 'मंगल ग्रह पर विशेष ध्यान के साथ नवग्रह शांति '
                                 'पूजा'}],
              'fasting': [{'en': 'Fast on Tuesdays (Mangalvar Vrat) for 21 '
                                 'consecutive Tuesdays',
                           'hi': 'मंगलवार (मंगलवार व्रत) का व्रत लगातार 21 '
                                 'मंगलवार तक करें'},
                          {'en': 'Consume only single-grain meal on fasting '
                                 'day',
                           'hi': 'उपवास के दिन केवल एक अनाज वाला भोजन ही '
                                 'खाएं'}],
              'worship': [{'en': 'Worship Lord Hanuman with sindoor and red '
                                 'flowers on Tuesdays',
                           'hi': 'मंगलवार के दिन हनुमान जी की पूजा सिन्दूर और '
                                 'लाल फूल से करें'},
                          {'en': 'Perform Kumbh Vivah (symbolic marriage to '
                                 'pot/tree) before actual marriage',
                           'hi': 'वास्तविक विवाह से पहले कुंभ विवाह '
                                 '(बर्तन/पेड़ से प्रतीकात्मक विवाह) करें'},
                          {'en': 'Visit Mangalnath temple in Ujjain for Mars '
                                 'pacification',
                           'hi': 'मंगल ग्रह की शांति के लिए उज्जैन में मंगलनाथ '
                                 'मंदिर जाएँ'},
                          {'en': 'Donate red lentils (masoor dal), red cloth, '
                                 'and jaggery on Tuesdays',
                           'hi': 'मंगलवार के दिन लाल मसूर दाल, लाल कपड़ा और '
                                 'गुड़ का दान करें'}],
              'gemstone': {'en': 'Wear Red Coral (Moonga) in gold/copper on '
                                 'the ring finger after proper energization '
                                 'with Mars mantra on a Tuesday during Shukla '
                                 'Paksha.',
                           'hi': 'शुक्ल पक्ष के मंगलवार के दिन लाल मूंगा को '
                                 'सोने/तांबे में मंगल मंत्र से अभिमंत्रित करके '
                                 'अनामिका उंगली में धारण करें।'}}}

LIFE_PREDICTIONS: Dict[str, Dict[str, Any]] = {'career': {'Aries': {'en': 'Strong leadership drives your professional life. '
                            'You excel in competitive environments where '
                            'initiative and courage are rewarded -- military, '
                            'sports, surgery, engineering, or '
                            'entrepreneurship. Mars energy makes you a '
                            'self-starter who prefers to lead rather than '
                            'follow. Career breakthroughs often come through '
                            'bold, independent action rather than patient '
                            'waiting.',
                      'hi': 'मजबूत नेतृत्व आपके पेशेवर जीवन को संचालित करता '
                            'है। आप प्रतिस्पर्धी माहौल में उत्कृष्टता प्राप्त '
                            'करते हैं जहां पहल और साहस को पुरस्कृत किया जाता '
                            'है - सैन्य, खेल, सर्जरी, इंजीनियरिंग, या '
                            'उद्यमिता। मंगल की ऊर्जा आपको एक स्व-स्टार्टर '
                            'बनाती है जो अनुसरण करने के बजाय नेतृत्व करना पसंद '
                            'करता है। करियर में सफलताएं अक्सर धैर्यपूर्वक '
                            'इंतजार करने के बजाय साहसिक, स्वतंत्र कार्रवाई से '
                            'आती हैं।'},
            'Taurus': {'en': 'Steady career growth through persistence and '
                             'reliability defines your professional journey. '
                             'You thrive in banking, agriculture, real estate, '
                             'luxury goods, hospitality, and fine arts. '
                             'Venus-ruled Taurus on the 10th gives an eye for '
                             'aesthetics that can translate into profitable '
                             'ventures. Financial security matters more to you '
                             'than fame, and your patience eventually builds '
                             'lasting wealth.',
                       'hi': 'दृढ़ता और विश्वसनीयता के माध्यम से स्थिर कैरियर '
                             'विकास आपकी पेशेवर यात्रा को परिभाषित करता है। आप '
                             'बैंकिंग, कृषि, रियल एस्टेट, विलासिता के सामान, '
                             'आतिथ्य और ललित कला में फलते-फूलते हैं। 10 तारीख '
                             'को शुक्र-शासित वृषभ सौंदर्यशास्त्र की दृष्टि '
                             'देता है जो लाभदायक उद्यमों में तब्दील हो सकता '
                             'है। वित्तीय सुरक्षा आपके लिए प्रसिद्धि से अधिक '
                             'मायने रखती है, और आपका धैर्य अंततः स्थायी धन का '
                             'निर्माण करता है।'},
            'Gemini': {'en': 'Communication is the cornerstone of your career '
                             'success. You shine in writing, journalism, '
                             'teaching, marketing, trading, and information '
                             "technology. Mercury's influence gives "
                             'versatility -- you may hold multiple roles or '
                             'change fields more than once. Your networking '
                             'ability and quick wit open doors that remain '
                             'closed to others, but focus is essential to '
                             'avoid scattered energies.',
                       'hi': 'संचार आपके करियर की सफलता की आधारशिला है। आप '
                             'लेखन, पत्रकारिता, शिक्षण, विपणन, व्यापार और '
                             'सूचना प्रौद्योगिकी में चमकते हैं। बुध का प्रभाव '
                             'बहुमुखी प्रतिभा देता है - आप कई भूमिकाएँ निभा '
                             'सकते हैं या एक से अधिक बार क्षेत्र बदल सकते हैं। '
                             'आपकी नेटवर्किंग क्षमता और त्वरित बुद्धि ऐसे '
                             'दरवाजे खोलती है जो दूसरों के लिए बंद रहते हैं, '
                             'लेकिन बिखरी हुई ऊर्जा से बचने के लिए ध्यान '
                             'केंद्रित करना आवश्यक है।'},
            'Cancer': {'en': 'Your career flourishes in nurturing, caregiving, '
                             'and emotionally resonant professions. '
                             'Hospitality, food industry, nursing, '
                             'counselling, interior design, and public welfare '
                             "suit you well. The Moon's rulership makes your "
                             'professional life subject to emotional tides -- '
                             'periods of intense productivity alternate with '
                             'withdrawal. Working close to home or in family '
                             'businesses is highly favourable.',
                       'hi': 'आपका करियर पालन-पोषण, देखभाल और भावनात्मक रूप से '
                             'जुड़े व्यवसायों में फलता-फूलता है। आतिथ्य, खाद्य '
                             'उद्योग, नर्सिंग, परामर्श, इंटीरियर डिजाइन और '
                             'सार्वजनिक कल्याण आपके लिए उपयुक्त हैं। चंद्रमा '
                             'का शासन आपके पेशेवर जीवन को भावनात्मक ज्वार के '
                             'अधीन बनाता है - तीव्र उत्पादकता की अवधि वापसी के '
                             'साथ वैकल्पिक होती है। घर के नजदीक या पारिवारिक '
                             'व्यवसायों में काम करना अत्यधिक अनुकूल है।'},
            'Leo': {'en': 'The stage is your natural workplace. Politics, '
                          'entertainment, senior management, government, and '
                          'creative direction are fields where your Sun-ruled '
                          '10th house sign shines brightest. You need '
                          'recognition and authority in your role; subordinate '
                          'positions breed discontent. Your generosity and '
                          'personal magnetism attract loyal teams, making you '
                          'a natural CEO or director.',
                    'hi': 'मंच आपका स्वाभाविक कार्यस्थल है। राजनीति, मनोरंजन, '
                          'वरिष्ठ प्रबंधन, सरकार और रचनात्मक दिशा ऐसे क्षेत्र '
                          'हैं जहां आपका सूर्य-शासित 10वां घर चिन्ह सबसे '
                          'चमकीला है। आपको अपनी भूमिका में मान्यता और अधिकार '
                          'की आवश्यकता है; अधीनस्थ पद असंतोष उत्पन्न करते हैं। '
                          'आपकी उदारता और व्यक्तिगत चुंबकत्व वफादार टीमों को '
                          'आकर्षित करते हैं, जिससे आप एक स्वाभाविक सीईओ या '
                          'निदेशक बन जाते हैं।'},
            'Virgo': {'en': 'Analytical precision and service orientation '
                            'define your professional path. Healthcare, '
                            'accounting, editing, quality control, data '
                            'science, and pharmaceutical work suit you '
                            "perfectly. Mercury's rulership gives meticulous "
                            'attention to detail that others find '
                            'extraordinary. Promotions may come slowly but '
                            'your work speaks for itself and builds an '
                            'impeccable reputation over time.',
                      'hi': 'विश्लेषणात्मक सटीकता और सेवा अभिविन्यास आपके '
                            'पेशेवर पथ को परिभाषित करते हैं। हेल्थकेयर, '
                            'अकाउंटिंग, संपादन, गुणवत्ता नियंत्रण, डेटा '
                            'विज्ञान और फार्मास्युटिकल कार्य आपके लिए बिल्कुल '
                            'उपयुक्त हैं। बुध का शासन उन विवरणों पर '
                            'सावधानीपूर्वक ध्यान देता है जो दूसरों को असाधारण '
                            'लगते हैं। पदोन्नति धीरे-धीरे हो सकती है लेकिन '
                            'आपका काम खुद बोलता है और समय के साथ बेदाग '
                            'प्रतिष्ठा बनाता है।'},
            'Libra': {'en': 'Partnership and diplomacy are central to your '
                            'career success. Law, judiciary, diplomacy, '
                            'fashion design, mediation, and luxury retail are '
                            'ideal fields. Venus-ruled Libra on the 10th gives '
                            'an elegant public image and skill in managing '
                            'relationships. Joint ventures and collaborations '
                            'bring greater success than solo efforts, and '
                            'fairness in dealings earns lasting professional '
                            'respect.',
                      'hi': 'साझेदारी और कूटनीति आपके करियर की सफलता के केंद्र '
                            'में हैं। कानून, न्यायपालिका, कूटनीति, फैशन '
                            'डिजाइन, मध्यस्थता और लक्जरी रिटेल आदर्श क्षेत्र '
                            'हैं। 10 तारीख को शुक्र-शासित तुला राशि एक सुंदर '
                            'सार्वजनिक छवि और रिश्तों को प्रबंधित करने में '
                            'कौशल प्रदान करती है। संयुक्त उद्यम और सहयोग एकल '
                            'प्रयासों की तुलना में अधिक सफलता लाते हैं, और '
                            'व्यवहार में निष्पक्षता स्थायी पेशेवर सम्मान '
                            'अर्जित करती है।'},
            'Scorpio': {'en': 'Intensity and transformation mark your '
                              'professional journey. Research, investigation, '
                              'surgery, psychology, insurance, occult '
                              'sciences, and crisis management are your forte. '
                              "Mars and Ketu's combined influence gives "
                              'unmatched focus and willingness to probe hidden '
                              'truths. Your career often involves dramatic '
                              'shifts that ultimately lead to positions of '
                              'deep influence behind the scenes.',
                        'hi': 'तीव्रता और परिवर्तन आपकी पेशेवर यात्रा को '
                              'चिह्नित करते हैं। अनुसंधान, जांच, सर्जरी, '
                              'मनोविज्ञान, बीमा, गुप्त विज्ञान और संकट प्रबंधन '
                              'आपकी विशेषता हैं। मंगल और केतु का संयुक्त '
                              'प्रभाव छिपे हुए सत्य की जांच करने के लिए बेजोड़ '
                              'फोकस और इच्छा देता है। आपके करियर में अक्सर '
                              'नाटकीय बदलाव शामिल होते हैं जो अंततः पर्दे के '
                              'पीछे गहरे प्रभाव वाले पदों तक ले जाते हैं।'},
            'Sagittarius': {'en': 'Wisdom and expansion drive your career. '
                                  'Higher education, law, publishing, foreign '
                                  'trade, philosophy, religious leadership, '
                                  'and long-distance travel industries suit '
                                  "you. Jupiter's rulership bestows optimism "
                                  'and ethical conduct that earns trust in '
                                  'positions of authority. International '
                                  'connections play a significant role, and '
                                  'your career often takes you far from your '
                                  'birthplace.',
                            'hi': 'बुद्धि और विस्तार आपके करियर को आगे बढ़ाते '
                                  'हैं। उच्च शिक्षा, कानून, प्रकाशन, विदेशी '
                                  'व्यापार, दर्शन, धार्मिक नेतृत्व और लंबी '
                                  'दूरी की यात्रा उद्योग आपके लिए उपयुक्त हैं। '
                                  'बृहस्पति का शासन आशावाद और नैतिक आचरण '
                                  'प्रदान करता है जो प्राधिकारी पदों पर '
                                  'विश्वास अर्जित करता है। अंतर्राष्ट्रीय '
                                  'संपर्क एक महत्वपूर्ण भूमिका निभाते हैं, और '
                                  'आपका करियर अक्सर आपको आपके जन्मस्थान से दूर '
                                  'ले जाता है।'},
            'Capricorn': {'en': 'Ambition and structure are the pillars of '
                                'your professional life. Government '
                                'administration, mining, construction, '
                                'corporate management, and traditional '
                                'industries reward your disciplined nature. '
                                "Saturn's rulership demands patience -- career "
                                'heights are reached in the 30s and 40s rather '
                                'than early. Your capacity for hard work and '
                                'organisational skill eventually places you in '
                                'positions of lasting authority.',
                          'hi': 'महत्वाकांक्षा और संरचना आपके पेशेवर जीवन के '
                                'आधार हैं। सरकारी प्रशासन, खनन, निर्माण, '
                                'कॉर्पोरेट प्रबंधन और पारंपरिक उद्योग आपके '
                                'अनुशासित स्वभाव को पुरस्कृत करते हैं। शनि के '
                                'शासन के लिए धैर्य की आवश्यकता होती है - '
                                'कैरियर की ऊंचाई जल्दी के बजाय 30 और 40 के दशक '
                                'में पहुंचती है। कड़ी मेहनत और संगठनात्मक कौशल '
                                'की आपकी क्षमता अंततः आपको स्थायी प्राधिकारी '
                                'के पदों पर स्थापित करती है।'},
            'Aquarius': {'en': 'Innovation and social reform characterise your '
                               'career path. Technology, aviation, social '
                               'work, NGO leadership, scientific research, and '
                               'network-based businesses are ideal. Saturn and '
                               "Rahu's combined influence gives both "
                               'discipline and unconventional thinking. Your '
                               'greatest professional success comes through '
                               'serving collective goals rather than purely '
                               'personal ambition.',
                         'hi': 'नवाचार और सामाजिक सुधार आपके करियर पथ की '
                               'विशेषताएँ हैं। प्रौद्योगिकी, विमानन, सामाजिक '
                               'कार्य, एनजीओ नेतृत्व, वैज्ञानिक अनुसंधान और '
                               'नेटवर्क-आधारित व्यवसाय आदर्श हैं। शनि और राहु '
                               'का संयुक्त प्रभाव अनुशासन और अपरंपरागत सोच '
                               'दोनों देता है। आपकी सबसे बड़ी व्यावसायिक सफलता '
                               'विशुद्ध रूप से व्यक्तिगत महत्वाकांक्षा के बजाय '
                               'सामूहिक लक्ष्यों की पूर्ति से आती है।'},
            'Pisces': {'en': 'Intuition and compassion guide your professional '
                             'life. Spiritual teaching, music, cinema, marine '
                             'industries, hospital administration, charitable '
                             "work, and the healing arts suit you. Jupiter's "
                             'rulership bestows wisdom and selflessness that '
                             'earns deep respect. Your career may lack '
                             "conventional structure but its impact on others' "
                             'lives is profound and your reputation endures.',
                       'hi': 'अंतर्ज्ञान और करुणा आपके पेशेवर जीवन का '
                             'मार्गदर्शन करते हैं। आध्यात्मिक शिक्षण, संगीत, '
                             'सिनेमा, समुद्री उद्योग, अस्पताल प्रशासन, '
                             'धर्मार्थ कार्य और उपचार कलाएँ आपके लिए उपयुक्त '
                             'हैं। बृहस्पति का शासन ज्ञान और निस्वार्थता '
                             'प्रदान करता है जो गहरा सम्मान अर्जित करता है। '
                             'आपके करियर में पारंपरिक संरचना का अभाव हो सकता '
                             'है लेकिन दूसरों के जीवन पर इसका प्रभाव गहरा होता '
                             'है और आपकी प्रतिष्ठा कायम रहती है।'}},
 'health': {'Aries': {'en': 'With Aries influencing your health house, you are '
                            'prone to acute conditions -- fevers, '
                            'inflammation, headaches, and blood-related '
                            'disorders. Your body runs hot and responds '
                            'quickly to both illness and recovery. Regular '
                            'physical activity is essential to channel excess '
                            'Mars energy. Guard especially against head '
                            'injuries, migraines, and skin eruptions caused by '
                            'pitta imbalance.',
                      'hi': 'मेष राशि के आपके स्वास्थ्य भाव को प्रभावित करने '
                            'से, आपको तीव्र स्थितियों - बुखार, सूजन, सिरदर्द '
                            'और रक्त संबंधी विकारों का खतरा है। आपका शरीर गर्म '
                            'रहता है और बीमारी और रिकवरी दोनों के प्रति तुरंत '
                            'प्रतिक्रिया करता है। मंगल की अतिरिक्त ऊर्जा को '
                            'प्रवाहित करने के लिए नियमित शारीरिक गतिविधि '
                            'आवश्यक है। विशेष रूप से सिर की चोटों, माइग्रेन और '
                            'पित्त असंतुलन के कारण होने वाली त्वचा के फटने से '
                            'बचाव करें।'},
            'Taurus': {'en': 'Taurus on the 6th house gives a generally robust '
                             'constitution but vulnerability in the throat, '
                             'thyroid, and cervical spine. Overindulgence in '
                             'rich foods leads to weight gain and metabolic '
                             'issues. Your recovery from illness is slow but '
                             'thorough once you commit to treatment. Diabetes, '
                             'tonsillitis, and neck stiffness are conditions '
                             'to monitor throughout life.',
                       'hi': 'छठे घर पर वृषभ आम तौर पर एक मजबूत संविधान देता '
                             'है लेकिन गले, थायरॉयड और ग्रीवा रीढ़ में कमजोरी '
                             'देता है। गरिष्ठ खाद्य पदार्थों का अधिक सेवन करने '
                             'से वजन बढ़ता है और चयापचय संबंधी समस्याएं होती '
                             'हैं। एक बार जब आप उपचार के लिए प्रतिबद्ध हो जाते '
                             'हैं तो बीमारी से आपकी रिकवरी धीमी लेकिन पूरी तरह '
                             'से होती है। मधुमेह, टॉन्सिलिटिस और गर्दन की '
                             'अकड़न ऐसी स्थितियाँ हैं जिन पर जीवन भर निगरानी '
                             'रखी जानी चाहिए।'},
            'Gemini': {'en': 'Gemini influencing health brings nervous system '
                             'sensitivity and respiratory vulnerability. '
                             'Anxiety, insomnia, bronchial issues, and '
                             'shoulder-arm complaints are common patterns. '
                             'Your mental health is deeply tied to physical '
                             'well-being -- stress manifests as bodily '
                             'symptoms quickly. Regular pranayama, moderate '
                             'exercise, and digital detoxes protect your '
                             'delicate nervous constitution.',
                       'hi': 'स्वास्थ्य को प्रभावित करने वाला मिथुन तंत्रिका '
                             'तंत्र संवेदनशीलता और श्वसन संबंधी कमजोरी लाता '
                             'है। चिंता, अनिद्रा, ब्रोन्कियल समस्याएं और '
                             'कंधे-बांह की शिकायतें सामान्य पैटर्न हैं। आपका '
                             'मानसिक स्वास्थ्य शारीरिक कल्याण से गहराई से '
                             'जुड़ा हुआ है - तनाव शारीरिक लक्षणों के रूप में '
                             'शीघ्रता से प्रकट होता है। नियमित प्राणायाम, '
                             'मध्यम व्यायाम और डिजिटल डिटॉक्स आपके नाजुक '
                             'तंत्रिका तंत्र की रक्षा करते हैं।'},
            'Cancer': {'en': "The Moon's influence on your health house makes "
                             'you susceptible to digestive and emotional '
                             'ailments. Acidity, water retention, chest '
                             'congestion, and hormonal fluctuations follow '
                             'lunar cycles. Emotional eating and '
                             'comfort-seeking behaviour can lead to stomach '
                             'disorders. A calm domestic environment and '
                             'regular meal timing are your best preventive '
                             'medicines.',
                       'hi': 'आपके स्वास्थ्य भाव पर चंद्रमा का प्रभाव आपको '
                             'पाचन और भावनात्मक बीमारियों के प्रति संवेदनशील '
                             'बनाता है। अम्लता, जल प्रतिधारण, छाती में जमाव और '
                             'हार्मोनल उतार-चढ़ाव चंद्र चक्र के अनुसार होते '
                             'हैं। भावनात्मक खान-पान और आराम-पसंद व्यवहार से '
                             'पेट संबंधी विकार हो सकते हैं। एक शांत घरेलू '
                             'वातावरण और नियमित भोजन का समय आपकी सबसे अच्छी '
                             'निवारक दवाएँ हैं।'},
            'Leo': {'en': 'Leo on the 6th house gives vitality but '
                          'vulnerability in the heart, spine, and eyes. Blood '
                          'pressure, cardiac rhythm issues, and spinal '
                          'problems require monitoring after age 35. Your '
                          'constitution is strong when the Sun is well-placed '
                          'but weakens dramatically under stress. Regular '
                          'cardiovascular exercise, avoiding excessive anger, '
                          'and sun salutations keep you robust.',
                    'hi': 'छठे भाव में सिंह जीवन शक्ति देता है लेकिन हृदय, '
                          'रीढ़ और आंखों में कमजोरी देता है। 35 वर्ष की आयु के '
                          'बाद रक्तचाप, हृदय गति संबंधी समस्याएं और रीढ़ की '
                          'हड्डी की समस्याओं पर निगरानी की आवश्यकता होती है। '
                          'जब सूर्य अच्छी स्थिति में होता है तो आपका शरीर '
                          'मजबूत होता है लेकिन तनाव में नाटकीय रूप से कमजोर हो '
                          'जाता है। नियमित हृदय व्यायाम, अत्यधिक क्रोध से बचना '
                          'और सूर्य नमस्कार आपको मजबूत बनाए रखते हैं।'},
            'Virgo': {'en': 'Mercury-ruled Virgo on the health house creates '
                            'sensitivity in the intestines and nervous '
                            'digestion. IBS, food allergies, skin issues from '
                            'internal toxins, and anxiety-driven ailments are '
                            'common. Your tendency to worry amplifies minor '
                            'symptoms into major concerns. A clean diet, '
                            'herbal supplements, and routine health check-ups '
                            'serve you far better than overthinking.',
                      'hi': 'स्वास्थ्य भाव पर बुध-शासित कन्या राशि आंतों और '
                            'तंत्रिका पाचन में संवेदनशीलता पैदा करती है। '
                            'आईबीएस, खाद्य एलर्जी, आंतरिक विषाक्त पदार्थों से '
                            'त्वचा संबंधी समस्याएं और चिंता से प्रेरित '
                            'बीमारियाँ आम हैं। आपकी चिंता करने की प्रवृत्ति '
                            'छोटे लक्षणों को बड़ी चिंताओं में बदल देती है। '
                            'स्वच्छ आहार, हर्बल सप्लीमेंट और नियमित स्वास्थ्य '
                            'जांच आपको ज़्यादा सोचने से कहीं बेहतर मदद करती '
                            'है।'},
            'Libra': {'en': 'Libra influencing health brings kidney, lower '
                            'back, and urinary tract vulnerabilities. Sugar '
                            'imbalances, skin conditions related to blood '
                            'impurity, and reproductive health issues arise. '
                            'Your health improves dramatically when emotional '
                            'relationships are harmonious. Adequate water '
                            'intake, avoiding processed foods, and maintaining '
                            'work-life balance are essential.',
                      'hi': 'स्वास्थ्य को प्रभावित करने वाला तुला राशि गुर्दे, '
                            'पीठ के निचले हिस्से और मूत्र पथ में कमज़ोरियाँ '
                            'लाता है। शर्करा असंतुलन, रक्त अशुद्धता से संबंधित '
                            'त्वचा की स्थिति और प्रजनन स्वास्थ्य संबंधी '
                            'समस्याएं उत्पन्न होती हैं। जब भावनात्मक रिश्ते '
                            'सामंजस्यपूर्ण होते हैं तो आपके स्वास्थ्य में '
                            'नाटकीय रूप से सुधार होता है। पर्याप्त पानी का '
                            'सेवन, प्रसंस्कृत खाद्य पदार्थों से परहेज और '
                            'कार्य-जीवन संतुलन बनाए रखना आवश्यक है।'},
            'Scorpio': {'en': 'Scorpio on the 6th house indicates intense '
                              'health crises that ultimately lead to '
                              'transformation. Reproductive organs, excretory '
                              'system, and hidden infections are vulnerable '
                              'areas. Surgical interventions may be necessary '
                              'at some point in life but lead to complete '
                              'recovery. Detoxification routines, sexual '
                              'health awareness, and regular screening prevent '
                              'serious complications.',
                        'hi': 'छठे भाव पर वृश्चिक गहन स्वास्थ्य संकट का संकेत '
                              'देता है जो अंततः परिवर्तन की ओर ले जाता है। '
                              'प्रजनन अंग, उत्सर्जन तंत्र और छिपे हुए संक्रमण '
                              'संवेदनशील क्षेत्र हैं। जीवन में किसी बिंदु पर '
                              'सर्जिकल हस्तक्षेप आवश्यक हो सकता है लेकिन इससे '
                              'पूरी तरह ठीक हो जाता है। विषहरण दिनचर्या, यौन '
                              'स्वास्थ्य जागरूकता और नियमित जांच गंभीर '
                              'जटिलताओं को रोकती है।'},
            'Sagittarius': {'en': "Jupiter's influence on health gives a "
                                  'generally optimistic constitution but '
                                  'excess in liver, hips, and thighs. Fatty '
                                  'liver, sciatica, and weight gain from '
                                  'overindulgence are common patterns. Your '
                                  'faith and positive outlook aid recovery '
                                  'remarkably well. Moderation in diet, '
                                  'hip-strengthening exercises, and periodic '
                                  'fasting maintain your natural vitality.',
                            'hi': 'स्वास्थ्य पर बृहस्पति का प्रभाव आम तौर पर '
                                  'आशावादी गठन देता है लेकिन यकृत, कूल्हों और '
                                  'जांघों में अधिकता देता है। फैटी लीवर, '
                                  'कटिस्नायुशूल, और अतिभोग से वजन बढ़ना '
                                  'सामान्य पैटर्न हैं। आपका विश्वास और '
                                  'सकारात्मक दृष्टिकोण उल्लेखनीय रूप से ठीक '
                                  'होने में सहायता करता है। आहार में संयम, '
                                  'कूल्हों को मजबूत बनाने वाले व्यायाम और '
                                  'समय-समय पर उपवास आपकी प्राकृतिक जीवन शक्ति '
                                  'को बनाए रखते हैं।'},
            'Capricorn': {'en': 'Saturn-ruled Capricorn on the health house '
                                'brings chronic but manageable conditions. '
                                'Joint pain, arthritis, dental issues, knee '
                                'problems, and skin dryness develop gradually '
                                'over time. Your constitution strengthens with '
                                'age -- health in the 40s is often better than '
                                'in the 20s. Calcium-rich diet, joint mobility '
                                'exercises, and patience with slow-healing '
                                'conditions are advised.',
                          'hi': 'स्वास्थ्य घर पर शनि-शासित मकर राशि पुरानी '
                                'लेकिन प्रबंधनीय स्थितियाँ लाती है। जोड़ों का '
                                'दर्द, गठिया, दांतों की समस्या, घुटनों की '
                                'समस्या और त्वचा का सूखापन समय के साथ '
                                'धीरे-धीरे विकसित होता है। उम्र के साथ आपका '
                                'संविधान मजबूत होता जाता है - 40 की उम्र में '
                                'स्वास्थ्य अक्सर 20 की तुलना में बेहतर होता '
                                'है। कैल्शियम युक्त आहार, जोड़ों की गतिशीलता '
                                'के व्यायाम और धीमी गति से ठीक होने वाली '
                                'स्थितियों में धैर्य रखने की सलाह दी जाती है।'},
            'Aquarius': {'en': 'Aquarius influencing health brings unusual or '
                               'hard-to-diagnose conditions affecting '
                               'circulation and the nervous system. Varicose '
                               'veins, ankle injuries, and sudden onset '
                               'ailments are characteristic. Your health '
                               'benefits greatly from unconventional healing '
                               'modalities -- acupuncture, energy healing, and '
                               'Ayurvedic approaches may work better than '
                               'conventional medicine for your constitution.',
                         'hi': 'स्वास्थ्य को प्रभावित करने वाला कुंभ राशि '
                               'परिसंचरण और तंत्रिका तंत्र को प्रभावित करने '
                               'वाली असामान्य या निदान करने में कठिन स्थितियां '
                               'लाती है। वैरिकाज़ नसें, टखने की चोटें और अचानक '
                               'शुरू होने वाली बीमारियाँ इसकी विशेषता हैं। '
                               'अपरंपरागत उपचार पद्धतियों से आपके स्वास्थ्य को '
                               'बहुत लाभ होता है - एक्यूपंक्चर, ऊर्जा उपचार और '
                               'आयुर्वेदिक दृष्टिकोण आपके संविधान के लिए '
                               'पारंपरिक चिकित्सा से बेहतर काम कर सकते हैं।'},
            'Pisces': {'en': 'Pisces on the 6th house creates sensitivity to '
                             'allergies, foot problems, and immune system '
                             'fluctuations. Lymphatic congestion, '
                             'psychosomatic illness, and sensitivity to '
                             'medications are common. Your health is deeply '
                             'influenced by your spiritual and emotional '
                             'state. Meditation, swimming, adequate sleep, and '
                             'avoiding intoxicants are your most powerful '
                             'health practices.',
                       'hi': 'छठे भाव में मीन राशि एलर्जी, पैरों की समस्याओं '
                             'और प्रतिरक्षा प्रणाली में उतार-चढ़ाव के प्रति '
                             'संवेदनशीलता पैदा करती है। लसीका जमाव, मनोदैहिक '
                             'बीमारी और दवाओं के प्रति संवेदनशीलता आम हैं। '
                             'आपका स्वास्थ्य आपकी आध्यात्मिक और भावनात्मक '
                             'स्थिति से गहराई से प्रभावित होता है। ध्यान, '
                             'तैराकी, पर्याप्त नींद और नशीले पदार्थों से परहेज '
                             'आपकी सबसे शक्तिशाली स्वास्थ्य आदतें हैं।'}},
 'marriage': {'Aries': {'en': 'Mars-ruled Aries on the 7th house brings a '
                              'passionate, dynamic, but sometimes combative '
                              'marriage. You attract strong-willed, '
                              'independent partners who challenge you to grow. '
                              'Arguments are frequent but reconciliations are '
                              'equally intense. Early marriage may face '
                              'turbulence; maturity improves harmony. Physical '
                              'attraction and mutual respect are the bedrock '
                              'of your partnerships.',
                        'hi': 'सातवें घर पर मंगल शासित मेष राशि एक भावुक, '
                              'गतिशील, लेकिन कभी-कभी जुझारू विवाह लाती है। आप '
                              'मजबूत इरादों वाले, स्वतंत्र साझेदारों को '
                              'आकर्षित करते हैं जो आपको आगे बढ़ने के लिए '
                              'चुनौती देते हैं। बहसें अक्सर होती रहती हैं '
                              'लेकिन सुलह भी उतनी ही तीव्र होती है। शीघ्र '
                              'विवाह में अशांति का सामना करना पड़ सकता है; '
                              'परिपक्वता से सामंजस्य में सुधार होता है। '
                              'शारीरिक आकर्षण और आपसी सम्मान आपकी साझेदारियों '
                              'का आधार हैं।'},
              'Taurus': {'en': 'Venus-ruled Taurus on the 7th house promises a '
                               'stable, sensual, and materially comfortable '
                               'marriage. Your spouse is likely attractive, '
                               'loyal, and fond of good living. Possessiveness '
                               'and stubbornness are the main challenges. The '
                               'relationship deepens with time like fine wine. '
                               'Shared appreciation for beauty, food, music, '
                               'and nature strengthens the bond.',
                         'hi': 'सातवें घर पर शुक्र-शासित वृषभ एक स्थिर, कामुक '
                               'और भौतिक रूप से आरामदायक विवाह का वादा करता '
                               'है। आपका जीवनसाथी संभवतः आकर्षक, वफादार और '
                               'अच्छे जीवन का शौकीन है। स्वामित्व और जिद मुख्य '
                               'चुनौतियां हैं। समय के साथ रिश्ता बढ़िया शराब '
                               'की तरह गहरा होता जाता है। सुंदरता, भोजन, संगीत '
                               'और प्रकृति के लिए साझा सराहना बंधन को मजबूत '
                               'करती है।'},
              'Gemini': {'en': "Mercury's influence on your 7th house brings "
                               'an intellectually stimulating partnership. '
                               'Your spouse is communicative, witty, and '
                               'possibly younger in spirit or age. Variety and '
                               'mental connection matter more than physical '
                               'passion. The risk is superficiality or '
                               'multiple attachments. A partner who shares '
                               'your curiosity and love of learning makes '
                               'marriage a lifelong conversation.',
                         'hi': 'आपके सातवें घर पर बुध का प्रभाव बौद्धिक रूप से '
                               'प्रेरक साझेदारी लाता है। आपका जीवनसाथी '
                               'मिलनसार, मजाकिया और संभवतः आत्मा या उम्र में '
                               'छोटा है। विविधता और मानसिक जुड़ाव शारीरिक '
                               'जुनून से ज्यादा मायने रखता है। जोखिम सतहीपन या '
                               'एकाधिक अनुलग्नक है। एक साथी जो आपकी जिज्ञासा '
                               'और सीखने के प्यार को साझा करता है, वह शादी को '
                               'आजीवन बातचीत बना देता है।'},
              'Cancer': {'en': 'The Moon ruling your 7th house gives an '
                               'emotionally deep and nurturing marriage. Your '
                               'spouse is caring, domestic, and deeply '
                               'attached to family. Mood swings and emotional '
                               'dependency can strain the relationship. A '
                               'secure home environment is essential for '
                               'marital happiness. Children and family '
                               'traditions become the glue that holds the '
                               'partnership together.',
                         'hi': 'आपके सातवें घर पर शासन करने वाला चंद्रमा '
                               'भावनात्मक रूप से गहरा और पोषित विवाह देता है। '
                               'आपका जीवनसाथी देखभाल करने वाला, घरेलू और '
                               'परिवार से गहराई से जुड़ा हुआ है। मूड में बदलाव '
                               'और भावनात्मक निर्भरता रिश्ते में तनाव पैदा कर '
                               'सकती है। वैवाहिक सुख के लिए सुरक्षित घरेलू '
                               'वातावरण आवश्यक है। बच्चे और पारिवारिक परंपराएँ '
                               'साझेदारी को एकजुट रखने वाली गोंद बन जाती हैं।'},
              'Leo': {'en': 'The Sun on your 7th house attracts a proud, '
                            'dignified, and authoritative spouse. Your partner '
                            'commands attention and expects loyalty and '
                            'admiration. Power struggles are the main '
                            'challenge. When both egos are managed, the '
                            'marriage is grand, warm, and generous. Public '
                            'status and social standing of the couple matter '
                            'significantly in this combination.',
                      'hi': 'आपके 7वें घर पर सूर्य एक गौरवान्वित, प्रतिष्ठित '
                            'और आधिकारिक जीवनसाथी को आकर्षित करता है। आपका '
                            'साथी ध्यान आकर्षित करता है और वफादारी और प्रशंसा '
                            'की अपेक्षा करता है। सत्ता संघर्ष मुख्य चुनौती है. '
                            'जब दोनों अहं प्रबंधित होते हैं, तो विवाह भव्य, '
                            'गर्मजोशीपूर्ण और उदार होता है। इस संयोजन में '
                            'जोड़े की सार्वजनिक स्थिति और सामाजिक प्रतिष्ठा '
                            'महत्वपूर्ण रूप से मायने रखती है।'},
              'Virgo': {'en': 'Mercury-ruled Virgo on the 7th house brings a '
                              'practical, service-oriented marriage. Your '
                              'spouse is detail-oriented, health-conscious, '
                              'and possibly critical. Perfectionism can create '
                              'friction. The partnership improves when both '
                              'focus on serving each other rather than finding '
                              'faults. Shared routines, health goals, and '
                              'intellectual pursuits create lasting harmony.',
                        'hi': '7वें घर पर बुध-शासित कन्या एक व्यावहारिक, '
                              'सेवा-उन्मुख विवाह लाती है। आपका जीवनसाथी '
                              'विस्तार-उन्मुख, स्वास्थ्य के प्रति जागरूक और '
                              'संभवतः आलोचनात्मक है। पूर्णतावाद घर्षण पैदा कर '
                              'सकता है। साझेदारी तब बेहतर होती है जब दोनों दोष '
                              'ढूंढने के बजाय एक-दूसरे की सेवा करने पर ध्यान '
                              'केंद्रित करते हैं। साझा दिनचर्या, स्वास्थ्य '
                              'लक्ष्य और बौद्धिक गतिविधियाँ स्थायी सद्भाव पैदा '
                              'करती हैं।'},
              'Libra': {'en': 'Venus-ruled Libra on the 7th house is the ideal '
                              'placement for marriage. Partnership, romance, '
                              'and mutual respect come naturally. Your spouse '
                              'is charming, fair-minded, and socially '
                              'graceful. Indecisiveness and avoidance of '
                              'conflict are the only weaknesses. This '
                              'placement favours love marriage and enduring '
                              'conjugal happiness built on true companionship.',
                        'hi': 'सातवें घर पर शुक्र-शासित तुला राशि विवाह के लिए '
                              'आदर्श स्थान है। साझेदारी, रोमांस और आपसी सम्मान '
                              'स्वाभाविक रूप से आते हैं। आपका जीवनसाथी आकर्षक, '
                              'निष्पक्ष विचारों वाला और सामाजिक रूप से शालीन '
                              'है। अनिर्णय और संघर्ष से बचना ही एकमात्र '
                              'कमज़ोरियाँ हैं। यह स्थिति प्रेम विवाह और सच्चे '
                              'साहचर्य पर निर्मित स्थायी वैवाहिक सुख का पक्ष '
                              'लेती है।'},
              'Scorpio': {'en': 'Mars-Ketu ruled Scorpio on the 7th house '
                                'creates an intensely transformative marriage. '
                                'Passion runs deep but so do jealousy and '
                                'possessiveness. Your spouse has magnetic '
                                'appeal and strong willpower. Trust issues and '
                                'power dynamics require conscious work. When '
                                'both partners surrender control, the marriage '
                                'becomes a vehicle for profound spiritual '
                                'growth.',
                          'hi': '7वें घर पर मंगल-केतु का आधिपत्य वृश्चिक राशि '
                                'में अत्यधिक परिवर्तनकारी विवाह बनाता है। '
                                'जुनून गहरा होता है लेकिन ईर्ष्या और स्वामित्व '
                                'भी गहरा होता है। आपके जीवनसाथी में चुंबकीय '
                                'आकर्षण और दृढ़ इच्छाशक्ति है। विश्वास के '
                                'मुद्दों और शक्ति की गतिशीलता के लिए सचेत '
                                'कार्य की आवश्यकता होती है। जब दोनों साझेदार '
                                'नियंत्रण छोड़ देते हैं, तो विवाह गहन '
                                'आध्यात्मिक विकास का माध्यम बन जाता है।'},
              'Sagittarius': {'en': "Jupiter's blessing on the 7th house "
                                    'brings an expansive, philosophical, and '
                                    'fortunate marriage. Your spouse is wise, '
                                    'optimistic, and often from a different '
                                    'cultural or educational background. '
                                    'Freedom within the relationship is '
                                    'essential -- neither partner tolerates '
                                    'possessiveness. Travel, higher learning, '
                                    'and shared spiritual values keep the '
                                    'marriage vibrant across decades.',
                              'hi': '7वें घर पर बृहस्पति का आशीर्वाद एक '
                                    'विस्तृत, दार्शनिक और भाग्यशाली विवाह लाता '
                                    'है। आपका जीवनसाथी बुद्धिमान, आशावादी और '
                                    'अक्सर एक अलग सांस्कृतिक या शैक्षिक '
                                    'पृष्ठभूमि से होता है। रिश्ते के भीतर '
                                    'स्वतंत्रता आवश्यक है - कोई भी साथी '
                                    'स्वामित्व की भावना को बर्दाश्त नहीं करता '
                                    'है। यात्रा, उच्च शिक्षा और साझा '
                                    'आध्यात्मिक मूल्य दशकों तक विवाह को जीवंत '
                                    'बनाए रखते हैं।'},
              'Capricorn': {'en': 'Saturn-ruled Capricorn on the 7th house '
                                  'delays marriage but ensures its durability. '
                                  'Your spouse is mature, responsible, and '
                                  'possibly older. The early years may feel '
                                  'dry or burdensome. With patience, the '
                                  'partnership becomes a rock-solid foundation '
                                  'for shared ambitions. Mutual respect for '
                                  "each other's career goals and a practical "
                                  'approach to love are the keys.',
                            'hi': '7वें घर पर शनि-शासित मकर राशि विवाह में '
                                  'देरी कराती है लेकिन उसका स्थायित्व '
                                  'सुनिश्चित करती है। आपका जीवनसाथी परिपक्व, '
                                  'जिम्मेदार और संभवतः अधिक उम्र का है। '
                                  'शुरुआती वर्ष शुष्क या बोझिल लग सकते हैं। '
                                  'धैर्य के साथ, साझेदारी साझा महत्वाकांक्षाओं '
                                  'के लिए एक ठोस आधार बन जाती है। एक-दूसरे के '
                                  'करियर लक्ष्यों के लिए पारस्परिक सम्मान और '
                                  'प्यार के प्रति व्यावहारिक दृष्टिकोण ही '
                                  'कुंजी हैं।'},
              'Aquarius': {'en': 'Saturn-Rahu ruled Aquarius on the 7th house '
                                 'creates an unconventional marriage. Your '
                                 'spouse is independent, progressive, and '
                                 'possibly eccentric. Traditional relationship '
                                 'expectations are challenged. '
                                 'Friendship-based marriage works best; '
                                 'possessiveness destroys the bond. Shared '
                                 'humanitarian values, intellectual '
                                 'companionship, and personal space sustain '
                                 'this unusual union.',
                           'hi': '7वें घर पर कुंभ राशि पर शासन करने वाला '
                                 'शनि-राहु एक अपरंपरागत विवाह बनाता है। आपका '
                                 'जीवनसाथी स्वतंत्र, प्रगतिशील और संभवतः '
                                 'विलक्षण है। पारंपरिक संबंध अपेक्षाओं को '
                                 'चुनौती दी गई है। मित्रता-आधारित विवाह '
                                 'सर्वोत्तम कार्य करता है; स्वामित्व बंधन को '
                                 'नष्ट कर देता है। साझा मानवीय मूल्य, बौद्धिक '
                                 'साहचर्य और व्यक्तिगत स्थान इस असामान्य मिलन '
                                 'को बनाए रखते हैं।'},
              'Pisces': {'en': 'Jupiter-ruled Pisces on the 7th house brings a '
                               'spiritually elevated and compassionate '
                               'marriage. Your spouse is gentle, intuitive, '
                               'artistic, and possibly self-sacrificing. '
                               'Boundaries may blur. Escapism through fantasy '
                               'or substances is the main risk. When grounded '
                               'in devotion and mutual care, this marriage '
                               'feels like a divine partnership.',
                         'hi': '7वें घर पर बृहस्पति शासित मीन राशि आध्यात्मिक '
                               'रूप से उन्नत और दयालु विवाह लाती है। आपका '
                               'जीवनसाथी सौम्य, सहज, कलात्मक और संभवतः '
                               'आत्म-त्यागी करने वाला है। सीमाएं धुंधली हो '
                               'सकती हैं. कल्पना या पदार्थों के माध्यम से '
                               'पलायनवाद मुख्य जोखिम है। जब भक्ति और आपसी '
                               'देखभाल पर आधारित होता है, तो यह विवाह एक दिव्य '
                               'साझेदारी जैसा लगता है।'}},
 'finance': {'Aries': {'en': 'Mars-ruled Aries on the 2nd house gives '
                             'aggressive earning capacity and bold financial '
                             'decisions. Income comes through competitive '
                             'fields, sports, engineering, or self-employment. '
                             'You earn quickly but spend impulsively. Building '
                             'savings requires conscious discipline against '
                             'your fiery nature. Investments in real estate '
                             'and metals tend to be more profitable than '
                             'speculative ventures.',
                       'hi': 'दूसरे घर पर मंगल द्वारा शासित मेष राशि आक्रामक '
                             'कमाई क्षमता और साहसिक वित्तीय निर्णय देती है। आय '
                             'प्रतिस्पर्धी क्षेत्रों, खेल, इंजीनियरिंग या '
                             'स्व-रोजगार के माध्यम से आती है। आप जल्दी कमाते '
                             'हैं लेकिन बिना सोचे-समझे खर्च कर देते हैं। बचत '
                             'के निर्माण के लिए आपके उग्र स्वभाव के विरुद्ध '
                             'सचेत अनुशासन की आवश्यकता होती है। सट्टा उद्यमों '
                             'की तुलना में रियल एस्टेट और धातुओं में निवेश '
                             'अधिक लाभदायक होता है।'},
             'Taurus': {'en': 'Venus-ruled Taurus on the 2nd house is the most '
                              'favourable placement for wealth accumulation. '
                              'Steady income, a love of saving, and good taste '
                              'in investments mark your financial life. '
                              'Banking, agriculture, luxury goods, and real '
                              'estate are your strongest wealth channels. '
                              'Family wealth and inheritance are likely, and '
                              'your financial position improves steadily with '
                              'age.',
                        'hi': 'दूसरे घर पर शुक्र-शासित वृषभ धन संचय के लिए '
                              'सबसे अनुकूल स्थान है। स्थिर आय, बचत का प्यार और '
                              'निवेश में अच्छा स्वाद आपके वित्तीय जीवन को '
                              'चिह्नित करता है। बैंकिंग, कृषि, विलासिता के '
                              'सामान और रियल एस्टेट आपके सबसे मजबूत धन चैनल '
                              'हैं। पारिवारिक संपत्ति और विरासत की संभावना है, '
                              'और उम्र के साथ आपकी वित्तीय स्थिति में लगातार '
                              'सुधार होता है।'},
             'Gemini': {'en': 'Mercury-ruled Gemini on the 2nd house creates '
                              'multiple income streams and financial '
                              'versatility. Earnings come through '
                              'communication, trading, brokerage, writing, or '
                              'intellectual property. Your financial situation '
                              'fluctuates -- brilliant gains alternate with '
                              'careless losses. Systematic investing and '
                              'avoiding gossip-driven financial decisions '
                              'protect your wealth.',
                        'hi': 'दूसरे घर पर बुध-शासित मिथुन कई आय धाराएं और '
                              'वित्तीय बहुमुखी प्रतिभा बनाता है। कमाई संचार, '
                              'व्यापार, दलाली, लेखन, या बौद्धिक संपदा के '
                              'माध्यम से होती है। आपकी वित्तीय स्थिति में '
                              'उतार-चढ़ाव होता रहता है - शानदार लाभ के साथ-साथ '
                              'लापरवाह नुकसान भी होता रहता है। व्यवस्थित निवेश '
                              'और गपशप-संचालित वित्तीय निर्णयों से बचना आपके '
                              'धन की रक्षा करता है।'},
             'Cancer': {'en': 'The Moon on the 2nd house makes finances '
                              'subject to emotional tides and cyclical '
                              'patterns. Income from food, hospitality, real '
                              'estate, and maternal family is indicated. '
                              'Savings grow when you feel emotionally secure; '
                              'insecurity triggers spending on comfort. '
                              'Property investment, particularly residential, '
                              'is your safest and most rewarding avenue.',
                        'hi': 'दूसरे घर में चंद्रमा वित्त को भावनात्मक ज्वार '
                              'और चक्रीय पैटर्न के अधीन बनाता है। भोजन, '
                              'आतिथ्य, अचल संपत्ति और मातृ परिवार से आय का '
                              'संकेत दिया गया है। जब आप भावनात्मक रूप से '
                              'सुरक्षित महसूस करते हैं तो बचत बढ़ती है; '
                              'असुरक्षा आराम पर खर्च करने को प्रेरित करती है। '
                              'संपत्ति निवेश, विशेष रूप से आवासीय, आपका सबसे '
                              'सुरक्षित और सबसे फायदेमंद तरीका है।'},
             'Leo': {'en': 'The Sun on the 2nd house brings wealth through '
                           'government, authority, and positions of power. You '
                           'earn well but spend lavishly on maintaining status '
                           'and generosity toward dependents. Gold, government '
                           'bonds, and investments in entertainment or '
                           'education are favourable. Your financial peak '
                           'often coincides with periods of public recognition '
                           'or political influence.',
                     'hi': 'दूसरे घर पर सूर्य सरकार, प्राधिकरण और सत्ता के '
                           'पदों के माध्यम से धन लाता है। आप अच्छा कमाते हैं '
                           'लेकिन रुतबा बनाए रखने और आश्रितों के प्रति उदारता '
                           'बरतने पर खूब खर्च करते हैं। सोना, सरकारी बांड और '
                           'मनोरंजन या शिक्षा में निवेश अनुकूल हैं। आपका '
                           'वित्तीय शिखर अक्सर सार्वजनिक मान्यता या राजनीतिक '
                           'प्रभाव की अवधि के साथ मेल खाता है।'},
             'Virgo': {'en': 'Mercury-ruled Virgo on the 2nd house gives '
                             'careful, analytical financial management. Income '
                             'from healthcare, service industries, accounting, '
                             'and detailed work is indicated. You rarely make '
                             'impulsive financial decisions and prefer '
                             'low-risk, steady-return investments. Tax '
                             'planning and budgeting come naturally, making '
                             'you financially secure if not spectacularly '
                             'wealthy.',
                       'hi': 'दूसरे घर पर बुध-शासित कन्या राशि सावधानीपूर्वक, '
                             'विश्लेषणात्मक वित्तीय प्रबंधन देती है। स्वास्थ्य '
                             'देखभाल, सेवा उद्योग, लेखांकन और विस्तृत कार्य से '
                             'आय का संकेत दिया गया है। आप शायद ही कभी '
                             'आवेगपूर्ण वित्तीय निर्णय लेते हैं और कम जोखिम '
                             'वाले, स्थिर रिटर्न वाले निवेश को प्राथमिकता देते '
                             'हैं। कर योजना और बजट बनाना स्वाभाविक रूप से आते '
                             'हैं, जो आपको शानदार अमीर नहीं तो वित्तीय रूप से '
                             'सुरक्षित बनाते हैं।'},
             'Libra': {'en': 'Venus-ruled Libra on the 2nd house attracts '
                             'wealth through partnerships and aesthetic '
                             'enterprises. Fashion, jewellery, art dealing, '
                             'legal practice, and collaborative ventures are '
                             'profitable. Your financial success is often '
                             "intertwined with your spouse's or business "
                             "partner's fortunes. Balanced spending on beauty "
                             'and comfort does not diminish wealth but rather '
                             'attracts more of it.',
                       'hi': 'दूसरे घर पर शुक्र-शासित तुला साझेदारी और सौंदर्य '
                             'उद्यमों के माध्यम से धन को आकर्षित करती है। '
                             'फैशन, आभूषण, कला व्यवहार, कानूनी अभ्यास और '
                             'सहयोगी उद्यम लाभदायक हैं। आपकी वित्तीय सफलता '
                             'अक्सर आपके जीवनसाथी या व्यावसायिक साझेदार के '
                             'भाग्य से जुड़ी होती है। सुंदरता और आराम पर '
                             'संतुलित खर्च करने से धन कम नहीं होता, बल्कि वह '
                             'और अधिक आकर्षित होता है।'},
             'Scorpio': {'en': 'Mars-Ketu ruled Scorpio on the 2nd house '
                               'creates intense financial experiences -- '
                               'inheritance, insurance payouts, or sudden '
                               'gains and losses. Research, mining, surgery, '
                               'and occult-related income. You have a '
                               'secretive approach to money and rarely reveal '
                               'your true financial position. Transformation '
                               'through financial crises ultimately leads to '
                               'deeper wisdom about true value.',
                         'hi': 'दूसरे घर पर मंगल-केतु शासित वृश्चिक तीव्र '
                               'वित्तीय अनुभव पैदा करता है - विरासत, बीमा '
                               'भुगतान, या अचानक लाभ और हानि। अनुसंधान, खनन, '
                               'सर्जरी, और गुप्त-संबंधी आय। पैसे के प्रति आपका '
                               'दृष्टिकोण गुप्त रहता है और आप शायद ही कभी अपनी '
                               'वास्तविक वित्तीय स्थिति प्रकट करते हैं। '
                               'वित्तीय संकटों के माध्यम से परिवर्तन अंततः '
                               'सच्चे मूल्य के बारे में गहन ज्ञान की ओर ले '
                               'जाता है।'},
             'Sagittarius': {'en': "Jupiter's blessing on the 2nd house is "
                                   'highly auspicious for wealth and family '
                                   'prosperity. Income from teaching, law, '
                                   'publishing, foreign trade, and religious '
                                   'or spiritual work. You are generous with '
                                   'money and your open-handedness is rewarded '
                                   'by Providence. Long-term investments, '
                                   'especially in education and foreign '
                                   'markets, yield excellent returns.',
                             'hi': 'दूसरे घर पर बृहस्पति का आशीर्वाद धन और '
                                   'पारिवारिक समृद्धि के लिए अत्यधिक शुभ है। '
                                   'शिक्षण, कानून, प्रकाशन, विदेशी व्यापार और '
                                   'धार्मिक या आध्यात्मिक कार्यों से आय। आप '
                                   'पैसे के मामले में उदार हैं और आपकी खुले '
                                   'दिल की इच्छा को प्रोविडेंस द्वारा पुरस्कृत '
                                   'किया जाता है। लंबी अवधि के निवेश, खासकर '
                                   'शिक्षा और विदेशी बाजारों में, उत्कृष्ट '
                                   'रिटर्न देते हैं।'},
             'Capricorn': {'en': 'Saturn-ruled Capricorn on the 2nd house '
                                 'builds wealth slowly but permanently. Income '
                                 'from government, construction, mining, oil, '
                                 'and traditional industries. Early life may '
                                 'see financial constraints, but discipline '
                                 'creates substantial wealth by middle age. '
                                 'Real estate, fixed deposits, and '
                                 'conservative blue-chip investments suit your '
                                 'cautious temperament.',
                           'hi': 'दूसरे घर पर शनि द्वारा शासित मकर राशि '
                                 'धीरे-धीरे लेकिन स्थायी रूप से धन का निर्माण '
                                 'करती है। सरकार, निर्माण, खनन, तेल और '
                                 'पारंपरिक उद्योगों से आय। प्रारंभिक जीवन में '
                                 'वित्तीय बाधाएं देखी जा सकती हैं, लेकिन '
                                 'अनुशासन मध्य आयु तक पर्याप्त धन पैदा करता '
                                 'है। रियल एस्टेट, सावधि जमा और रूढ़िवादी '
                                 'ब्लू-चिप निवेश आपके सतर्क स्वभाव के अनुकूल '
                                 'हैं।'},
             'Aquarius': {'en': 'Saturn-Rahu ruled Aquarius on the 2nd house '
                                'brings unconventional income sources. '
                                'Technology, cryptocurrency, network '
                                'marketing, aviation, and social enterprises '
                                'are indicated. Your financial philosophy is '
                                'progressive -- you value freedom over '
                                'accumulation. Sudden gains through innovation '
                                'or technology disruption can dramatically '
                                'change your financial standing.',
                          'hi': 'दूसरे घर पर शनि-राहु का स्वामित्व कुंभ राशि '
                                'पर है जो अपरंपरागत आय स्रोत लाता है। '
                                'प्रौद्योगिकी, क्रिप्टोकरेंसी, नेटवर्क '
                                'मार्केटिंग, विमानन और सामाजिक उद्यमों का '
                                'संकेत दिया गया है। आपका वित्तीय दर्शन '
                                'प्रगतिशील है - आप संचय से अधिक स्वतंत्रता को '
                                'महत्व देते हैं। नवाचार या प्रौद्योगिकी '
                                'व्यवधान के माध्यम से अचानक लाभ आपकी वित्तीय '
                                'स्थिति को नाटकीय रूप से बदल सकता है।'},
             'Pisces': {'en': 'Jupiter-ruled Pisces on the 2nd house attracts '
                              'wealth through intuition and spiritual '
                              'alignment. Income from music, cinema, hospital '
                              'administration, charity, marine activities, and '
                              'healing arts. You are generous to a fault and '
                              'may lose money through misplaced trust or lack '
                              'of boundaries. When your financial decisions '
                              'align with your spiritual values, abundance '
                              'flows naturally.',
                        'hi': 'दूसरे घर पर बृहस्पति शासित मीन राशि अंतर्ज्ञान '
                              'और आध्यात्मिक संरेखण के माध्यम से धन को आकर्षित '
                              'करती है। संगीत, सिनेमा, अस्पताल प्रशासन, दान, '
                              'समुद्री गतिविधियों और उपचार कला से आय। आप किसी '
                              'गलती के प्रति उदार हैं और गलत विश्वास या सीमाओं '
                              'की कमी के कारण धन खो सकते हैं। जब आपके वित्तीय '
                              'निर्णय आपके आध्यात्मिक मूल्यों के साथ संरेखित '
                              'होते हैं, तो प्रचुरता स्वाभाविक रूप से प्रवाहित '
                              'होती है।'}},
 'education': {'Aries': {'en': 'Mars-ruled Aries influencing education gives a '
                               'competitive, fast-learning mind that excels '
                               'under pressure. You prefer practical, hands-on '
                               'learning over theoretical study. Engineering, '
                               'military science, surgery, and sports '
                               'education are naturally suited fields. Early '
                               'academic life may show impulsiveness, but '
                               'focused coaching channels your energy into '
                               'impressive academic achievements.',
                         'hi': 'शिक्षा को प्रभावित करने वाला मंगल-शासित मेष एक '
                               'प्रतिस्पर्धी, तेजी से सीखने वाला दिमाग देता है '
                               'जो दबाव में उत्कृष्टता प्राप्त करता है। आप '
                               'सैद्धांतिक अध्ययन की अपेक्षा व्यावहारिक, '
                               'व्यावहारिक शिक्षा को प्राथमिकता देते हैं। '
                               'इंजीनियरिंग, सैन्य विज्ञान, सर्जरी और खेल '
                               'शिक्षा स्वाभाविक रूप से अनुकूल क्षेत्र हैं। '
                               'प्रारंभिक शैक्षणिक जीवन में आवेग दिख सकता है, '
                               'लेकिन केंद्रित कोचिंग आपकी ऊर्जा को प्रभावशाली '
                               'शैक्षणिक उपलब्धियों में बदल देती है।'},
               'Taurus': {'en': 'Venus-ruled Taurus on the education house '
                                'gives a steady, methodical learning approach. '
                                'You absorb knowledge slowly but retain it '
                                'permanently. Fine arts, music, agriculture, '
                                'economics, and culinary arts are ideal fields '
                                'of study. A comfortable, aesthetically '
                                'pleasing study environment dramatically '
                                'improves your concentration and academic '
                                'output.',
                          'hi': 'शिक्षा घर पर शुक्र-शासित वृषभ एक स्थिर, '
                                'व्यवस्थित सीखने का दृष्टिकोण देता है। आप '
                                'ज्ञान को धीरे-धीरे ग्रहण करते हैं लेकिन उसे '
                                'स्थायी रूप से बनाए रखते हैं। ललित कला, संगीत, '
                                'कृषि, अर्थशास्त्र और पाक कला अध्ययन के आदर्श '
                                'क्षेत्र हैं। एक आरामदायक, सौंदर्यपूर्ण रूप से '
                                'मनभावन अध्ययन वातावरण नाटकीय रूप से आपकी '
                                'एकाग्रता और शैक्षणिक आउटपुट में सुधार करता '
                                'है।'},
               'Gemini': {'en': 'Mercury-ruled Gemini is among the strongest '
                                'placements for intellectual achievement. You '
                                'excel in languages, mathematics, commerce, '
                                'journalism, and computer science. Your '
                                'learning speed is exceptional but depth may '
                                'suffer due to scattered interests. Debate, '
                                'quizzing, and competitive examinations '
                                'showcase your mental agility and '
                                'communication skills.',
                          'hi': 'बुध शासित मिथुन बौद्धिक उपलब्धि के लिए सबसे '
                                'मजबूत स्थानों में से एक है। आप भाषा, गणित, '
                                'वाणिज्य, पत्रकारिता और कंप्यूटर विज्ञान में '
                                'उत्कृष्ट हैं। आपकी सीखने की गति असाधारण है '
                                'लेकिन बिखरी हुई रुचियों के कारण गहराई '
                                'प्रभावित हो सकती है। वाद-विवाद, प्रश्नोत्तरी '
                                'और प्रतियोगी परीक्षाएं आपकी मानसिक चपलता और '
                                'संचार कौशल को प्रदर्शित करती हैं।'},
               'Cancer': {'en': 'Moon-ruled Cancer on the education house '
                                'gives excellent memory and intuitive learning '
                                'ability. History, psychology, nursing, home '
                                'science, and marine biology suit your '
                                'emotional intelligence. Your academic '
                                'performance fluctuates with emotional state '
                                '-- supportive teachers matter immensely. '
                                'Education received at home or in a nurturing '
                                'environment yields the best results.',
                          'hi': 'शिक्षा घर पर चंद्रमा शासित कर्क राशि उत्कृष्ट '
                                'स्मृति और सहज ज्ञान युक्त सीखने की क्षमता '
                                'देती है। इतिहास, मनोविज्ञान, नर्सिंग, गृह '
                                'विज्ञान और समुद्री जीव विज्ञान आपकी भावनात्मक '
                                'बुद्धिमत्ता के अनुकूल हैं। भावनात्मक स्थिति '
                                'के साथ आपके शैक्षणिक प्रदर्शन में उतार-चढ़ाव '
                                'होता रहता है - सहायक शिक्षक बहुत मायने रखते '
                                'हैं। घर पर या पालन-पोषण वाले वातावरण में '
                                'प्राप्त शिक्षा सर्वोत्तम परिणाम देती है।'},
               'Leo': {'en': 'Sun-ruled Leo influencing education gives '
                             'confidence and flair in academic settings. '
                             'Political science, performing arts, '
                             'administration, and leadership programmes suit '
                             'you well. You prefer being the best student in '
                             'class rather than part of the crowd. Government '
                             'scholarships and recognition for academic '
                             'excellence are strongly indicated.',
                       'hi': 'सूर्य शासित सिंह राशि शिक्षा को प्रभावित करने से '
                             'शैक्षणिक सेटिंग्स में आत्मविश्वास और प्रतिभा '
                             'मिलती है। राजनीति विज्ञान, प्रदर्शन कला, प्रशासन '
                             'और नेतृत्व कार्यक्रम आपके लिए उपयुक्त हैं। आप '
                             'भीड़ का हिस्सा बनने के बजाय कक्षा में '
                             'सर्वश्रेष्ठ छात्र बनना पसंद करते हैं। सरकारी '
                             'छात्रवृत्ति और शैक्षणिक उत्कृष्टता के लिए '
                             'मान्यता का जोरदार संकेत दिया गया है।'},
               'Virgo': {'en': 'Mercury-ruled Virgo is the finest placement '
                               'for analytical and scientific education. '
                               'Medicine, pharmacy, statistics, editing, '
                               'research methodology, and environmental '
                               'science are ideal. Your attention to detail '
                               'makes you a natural scholar who produces '
                               'meticulous work. Overly critical '
                               'self-assessment can create examination anxiety '
                               'despite strong preparation.',
                         'hi': 'विश्लेषणात्मक और वैज्ञानिक शिक्षा के लिए '
                               'बुध-शासित कन्या राशि सर्वोत्तम स्थान है। '
                               'चिकित्सा, फार्मेसी, सांख्यिकी, संपादन, '
                               'अनुसंधान पद्धति और पर्यावरण विज्ञान आदर्श हैं। '
                               'विस्तार पर आपका ध्यान आपको एक स्वाभाविक '
                               'विद्वान बनाता है जो सावधानीपूर्वक काम करता है। '
                               'अत्यधिक आलोचनात्मक आत्म-मूल्यांकन मजबूत तैयारी '
                               'के बावजूद परीक्षा की चिंता पैदा कर सकता है।'},
               'Libra': {'en': 'Venus-ruled Libra on the education house '
                               'favours artistic and social sciences. Law, '
                               'diplomacy, fashion design, architecture, and '
                               'international relations are naturally suited '
                               'fields. You learn best through discussion and '
                               'collaboration rather than solitary study. '
                               'Aesthetic subjects and those requiring '
                               'balanced judgement bring out your highest '
                               'intellectual abilities.',
                         'hi': 'शिक्षा घर पर शुक्र-शासित तुला कलात्मक और '
                               'सामाजिक विज्ञान का पक्षधर है। कानून, कूटनीति, '
                               'फैशन डिजाइन, वास्तुकला और अंतर्राष्ट्रीय संबंध '
                               'स्वाभाविक रूप से उपयुक्त क्षेत्र हैं। आप अकेले '
                               'अध्ययन के बजाय चर्चा और सहयोग के माध्यम से '
                               'सबसे अच्छा सीखते हैं। सौंदर्य संबंधी विषय और '
                               'संतुलित निर्णय की आवश्यकता वाले विषय आपकी '
                               'उच्चतम बौद्धिक क्षमताओं को सामने लाते हैं।'},
               'Scorpio': {'en': 'Mars-Ketu ruled Scorpio influencing '
                                 'education gives intense, focused research '
                                 'ability. Psychology, forensic science, '
                                 'surgery, occult studies, and detective work '
                                 'suit your probing mind. You are drawn to '
                                 'hidden knowledge and excel in subjects '
                                 'others find dark or difficult. Academic '
                                 'breakthroughs often come through obsessive '
                                 'deep study rather than breadth of learning.',
                           'hi': 'मंगल-केतु शासित वृश्चिक शिक्षा को प्रभावित '
                                 'करते हुए गहन, केंद्रित अनुसंधान क्षमता देता '
                                 'है। मनोविज्ञान, फोरेंसिक विज्ञान, सर्जरी, '
                                 'गुप्त अध्ययन और जासूसी कार्य आपके जांच दिमाग '
                                 'के लिए उपयुक्त हैं। आप छिपे हुए ज्ञान की ओर '
                                 'आकर्षित होते हैं और उन विषयों में उत्कृष्टता '
                                 'प्राप्त करते हैं जो दूसरों को कठिन या कठिन '
                                 'लगते हैं। शैक्षणिक सफलताएं अक्सर सीखने की '
                                 'व्यापकता के बजाय जुनूनी गहन अध्ययन से आती '
                                 'हैं।'},
               'Sagittarius': {'en': "Jupiter's blessing on the education "
                                     'house is supremely favourable for higher '
                                     'learning. Philosophy, theology, law, '
                                     'foreign languages, and university '
                                     'teaching are natural fields. You are '
                                     'drawn to wisdom traditions and excel in '
                                     'environments that value ethical '
                                     'thinking. Study abroad or distance '
                                     'education from foreign universities is '
                                     'strongly indicated and successful.',
                               'hi': 'शिक्षा घर पर बृहस्पति का आशीर्वाद उच्च '
                                     'शिक्षा के लिए अत्यंत अनुकूल है। '
                                     'दर्शनशास्त्र, धर्मशास्त्र, कानून, विदेशी '
                                     'भाषाएँ और विश्वविद्यालय शिक्षण प्राकृतिक '
                                     'क्षेत्र हैं। आप ज्ञान परंपराओं की ओर '
                                     'आकर्षित होते हैं और ऐसे वातावरण में '
                                     'उत्कृष्टता प्राप्त करते हैं जो नैतिक सोच '
                                     'को महत्व देता है। विदेश में अध्ययन या '
                                     'विदेशी विश्वविद्यालयों से दूरस्थ शिक्षा '
                                     'दृढ़ता से संकेतित और सफल है।'},
               'Capricorn': {'en': 'Saturn-ruled Capricorn on the education '
                                   'house delays academic success but makes it '
                                   'permanent. Civil engineering, '
                                   'architecture, geology, public '
                                   'administration, and traditional crafts '
                                   'suit you. Early academic life may show '
                                   'obstacles or late starts, but persistence '
                                   'pays off handsomely. Professional '
                                   'certifications and practical '
                                   'qualifications serve you better than '
                                   'theoretical degrees.',
                             'hi': 'शिक्षा घर पर शनि का शासन मकर राशि में होने '
                                   'से शैक्षणिक सफलता में देरी होती है लेकिन '
                                   'यह उसे स्थायी बनाती है। सिविल इंजीनियरिंग, '
                                   'वास्तुकला, भूविज्ञान, सार्वजनिक प्रशासन और '
                                   'पारंपरिक शिल्प आपके लिए उपयुक्त हैं। '
                                   'प्रारंभिक शैक्षणिक जीवन में बाधाएँ आ सकती '
                                   'हैं या देर से शुरुआत हो सकती है, लेकिन '
                                   'दृढ़ता से अच्छा परिणाम मिलता है। '
                                   'व्यावसायिक प्रमाणपत्र और व्यावहारिक '
                                   'योग्यताएँ आपको सैद्धांतिक डिग्री से बेहतर '
                                   'सेवा प्रदान करती हैं।'},
               'Aquarius': {'en': 'Saturn-Rahu influenced Aquarius on the '
                                  'education house favours cutting-edge and '
                                  'unconventional study. Aerospace, '
                                  'information technology, social sciences, '
                                  'astrology, and futuristic research suit '
                                  'you. You learn best through experimentation '
                                  'and may be self-taught in key areas. Group '
                                  'study and online learning platforms enhance '
                                  'your naturally network-oriented '
                                  'intelligence.',
                            'hi': 'शिक्षा भाव पर शनि-राहु का प्रभाव कुम्भ राशि '
                                  'वालों को अत्याधुनिक और अपरंपरागत अध्ययन का '
                                  'पक्षधर है। एयरोस्पेस, सूचना प्रौद्योगिकी, '
                                  'सामाजिक विज्ञान, ज्योतिष और भविष्य संबंधी '
                                  'शोध आपके लिए उपयुक्त हैं। आप प्रयोग के '
                                  'माध्यम से सबसे अच्छा सीखते हैं और प्रमुख '
                                  'क्षेत्रों में स्वयं-सिखाया जा सकता है। समूह '
                                  'अध्ययन और ऑनलाइन शिक्षण प्लेटफ़ॉर्म आपकी '
                                  'स्वाभाविक रूप से नेटवर्क-उन्मुख बुद्धि को '
                                  'बढ़ाते हैं।'},
               'Pisces': {'en': 'Jupiter-ruled Pisces influencing education '
                                'gives exceptional intuitive and creative '
                                'intelligence. Fine arts, music, spiritual '
                                'philosophy, marine science, and healing arts '
                                'are your ideal fields. Your learning style is '
                                'absorptive rather than analytical -- you '
                                'understand through feeling. Meditation and '
                                'retreats may contribute more to your real '
                                'education than formal classroom instruction.',
                          'hi': 'शिक्षा को प्रभावित करने वाली बृहस्पति शासित '
                                'मीन राशि असाधारण सहज और रचनात्मक बुद्धि देती '
                                'है। ललित कला, संगीत, आध्यात्मिक दर्शन, '
                                'समुद्री विज्ञान और उपचार कला आपके आदर्श '
                                'क्षेत्र हैं। आपकी सीखने की शैली विश्लेषणात्मक '
                                'के बजाय अवशोषक है - आप महसूस करके समझते हैं। '
                                'औपचारिक कक्षा निर्देश की तुलना में ध्यान और '
                                'एकांतवास आपकी वास्तविक शिक्षा में अधिक योगदान '
                                'दे सकते हैं।'}},
 'character': {'Aries': {'en': 'You are a born pioneer with a courageous, '
                               'direct, and fiercely independent character. '
                               'Honesty to the point of bluntness, quick '
                               'temper that cools equally fast, and restless '
                               'energy define your personality. You lead from '
                               'the front and cannot tolerate cowardice or '
                               'dishonesty. Your greatest virtue is courage; '
                               'your greatest challenge is patience.',
                         'hi': 'आप साहसी, प्रत्यक्ष और अत्यंत स्वतंत्र चरित्र '
                               'वाले जन्मजात अग्रणी हैं। बेबाकी की हद तक '
                               'ईमानदारी, उतनी ही तेजी से ठंडा होने वाला '
                               'त्वरित स्वभाव और बेचैन ऊर्जा आपके व्यक्तित्व '
                               'को परिभाषित करती है। आप आगे बढ़कर नेतृत्व करते '
                               'हैं और कायरता या बेईमानी बर्दाश्त नहीं कर '
                               'सकते। आपका सबसे बड़ा गुण साहस है; आपकी सबसे '
                               'बड़ी चुनौती धैर्य है.'},
               'Taurus': {'en': 'You possess a steady, patient, and deeply '
                                'loyal character rooted in material reality. '
                                'Reliability, sensuality, and a stubborn '
                                'refusal to be rushed are your hallmarks. You '
                                'value comfort, beauty, and security above '
                                'adventure or novelty. Your greatest virtue is '
                                'dependability; your greatest challenge is '
                                'resistance to change.',
                          'hi': 'आपके पास भौतिक वास्तविकता में निहित एक स्थिर, '
                                'धैर्यवान और गहरा वफादार चरित्र है। '
                                'विश्वसनीयता, कामुकता और जल्दबाजी से इनकार '
                                'करना आपकी पहचान है। आप रोमांच या नवीनता से '
                                'ऊपर आराम, सुंदरता और सुरक्षा को महत्व देते '
                                'हैं। आपका सबसे बड़ा गुण निर्भरता है; आपकी '
                                'सबसे बड़ी चुनौती परिवर्तन का प्रतिरोध है।'},
               'Gemini': {'en': 'An intellectually curious, quick-witted, and '
                                'endlessly adaptable character defines you. '
                                'You process information faster than most and '
                                'communicate with charm and precision. Duality '
                                'is inherent -- you can argue both sides of '
                                'any issue with equal conviction. Your '
                                'greatest virtue is versatility; your greatest '
                                'challenge is consistency.',
                          'hi': 'एक बौद्धिक रूप से जिज्ञासु, त्वरित-समझदार और '
                                'अंतहीन रूप से अनुकूलनीय चरित्र आपको परिभाषित '
                                'करता है। आप अन्य लोगों की तुलना में सूचनाओं '
                                'को तेजी से संसाधित करते हैं और आकर्षण और '
                                'सटीकता के साथ संचार करते हैं। द्वंद्व '
                                'अंतर्निहित है - आप किसी भी मुद्दे के दोनों '
                                'पक्षों पर समान दृढ़ विश्वास के साथ बहस कर '
                                'सकते हैं। आपका सबसे बड़ा गुण बहुमुखी प्रतिभा '
                                'है; आपकी सबसे बड़ी चुनौती निरंतरता है।'},
               'Cancer': {'en': 'You carry a deeply emotional, nurturing, and '
                                'protective character beneath a tough '
                                'exterior. Family and emotional security are '
                                'your core motivations in every decision you '
                                'make. Your memory is powerful and you hold '
                                'onto both love and grudges with equal '
                                'tenacity. Your greatest virtue is devotion; '
                                'your greatest challenge is letting go of the '
                                'past.',
                          'hi': 'आप अपने सख्त बाहरी स्वरूप के साथ-साथ एक गहरा '
                                'भावनात्मक, पालन-पोषण करने वाला और सुरक्षात्मक '
                                'चरित्र रखते हैं। आपके प्रत्येक निर्णय में '
                                'परिवार और भावनात्मक सुरक्षा आपकी मुख्य '
                                'प्रेरणाएँ हैं। आपकी याददाश्त शक्तिशाली है और '
                                'आप प्यार और नाराजगी दोनों को समान दृढ़ता से '
                                'पकड़ते हैं। आपका सबसे बड़ा गुण भक्ति है; आपकी '
                                'सबसे बड़ी चुनौती अतीत को जाने देना है।'},
               'Leo': {'en': 'A generous, dignified, and magnificently '
                             'confident character radiates from your being. '
                             'You command attention effortlessly and feel most '
                             'alive when appreciated and respected. Leadership '
                             'comes naturally, though your pride can make you '
                             'vulnerable to flattery. Your greatest virtue is '
                             'magnanimity; your greatest challenge is ego '
                             'management.',
                       'hi': 'एक उदार, गरिमामय और भव्य आत्मविश्वास वाला चरित्र '
                             'आपके अस्तित्व से झलकता है। आप सहजता से ध्यान '
                             'आकर्षित करते हैं और सराहना और सम्मान मिलने पर '
                             'सबसे अधिक जीवंत महसूस करते हैं। नेतृत्व '
                             'स्वाभाविक रूप से आता है, हालाँकि आपका अहंकार '
                             'आपको चापलूसी के प्रति संवेदनशील बना सकता है। '
                             'आपका सबसे बड़ा गुण उदारता है; आपकी सबसे बड़ी '
                             'चुनौती अहंकार प्रबंधन है।'},
               'Virgo': {'en': 'You embody a precise, analytical, and '
                               'service-oriented character with exacting '
                               'standards. Detail-oriented to a remarkable '
                               'degree, you notice what others miss entirely. '
                               'Self-criticism and a desire for perfection '
                               'drive both your achievements and your '
                               'anxieties. Your greatest virtue is '
                               'discrimination; your greatest challenge is '
                               'self-acceptance.',
                         'hi': 'आप सटीक मानकों के साथ एक सटीक, विश्लेषणात्मक '
                               'और सेवा-उन्मुख चरित्र का प्रतीक हैं। उल्लेखनीय '
                               'स्तर तक विस्तार-उन्मुख, आप नोटिस करते हैं कि '
                               'अन्य लोग पूरी तरह से क्या भूल जाते हैं। '
                               'आत्म-आलोचना और पूर्णता की इच्छा आपकी '
                               'उपलब्धियों और चिंताओं दोनों को प्रेरित करती '
                               'है। आपका सबसे बड़ा गुण विवेक है; आपकी सबसे '
                               'बड़ी चुनौती आत्म-स्वीकृति है।'},
               'Libra': {'en': 'Balance, harmony, and aesthetic refinement '
                               'characterise your elegant personality. You '
                               'seek fairness in all dealings and are deeply '
                               'uncomfortable with conflict or ugliness. '
                               'Partnership is essential -- you understand '
                               'yourself best through relationship with '
                               'others. Your greatest virtue is diplomacy; '
                               'your greatest challenge is decisiveness.',
                         'hi': 'संतुलन, सामंजस्य और सौंदर्य परिष्कार आपके '
                               'सुरुचिपूर्ण व्यक्तित्व की विशेषता है। आप सभी '
                               'व्यवहारों में निष्पक्षता चाहते हैं और संघर्ष '
                               'या कुरूपता से बहुत असहज हैं। साझेदारी आवश्यक '
                               'है - आप दूसरों के साथ संबंधों के माध्यम से '
                               'स्वयं को सबसे अच्छी तरह समझते हैं। आपका सबसे '
                               'बड़ा गुण कूटनीति है; आपकी सबसे बड़ी चुनौती '
                               'निर्णायकता है।'},
               'Scorpio': {'en': 'Intensity, depth, and unwavering '
                                 'determination define your powerful '
                                 'character. You see beneath surfaces and are '
                                 "drawn to life's hidden dimensions -- "
                                 'psychology, mystery, power. Loyalty to your '
                                 'chosen few is absolute, but betrayal '
                                 'triggers devastating consequences. Your '
                                 'greatest virtue is transformative power; '
                                 'your greatest challenge is releasing '
                                 'control.',
                           'hi': 'तीव्रता, गहराई और अटूट दृढ़ संकल्प आपके '
                                 'शक्तिशाली चरित्र को परिभाषित करते हैं। आप '
                                 'सतहों के नीचे देखते हैं और जीवन के छिपे हुए '
                                 'आयामों - मनोविज्ञान, रहस्य, शक्ति - की ओर '
                                 'आकर्षित होते हैं। अपने चुने हुए कुछ लोगों के '
                                 'प्रति वफादारी पूर्ण है, लेकिन विश्वासघात '
                                 'विनाशकारी परिणामों को ट्रिगर करता है। आपका '
                                 'सबसे बड़ा गुण परिवर्तनकारी शक्ति है; आपकी '
                                 'सबसे बड़ी चुनौती नियंत्रण जारी करना है।'},
               'Sagittarius': {'en': 'An optimistic, freedom-loving, and '
                                     'philosophically minded character propels '
                                     'your life. You seek meaning above '
                                     'material gain and feel stifled by '
                                     'routine or narrow thinking. Honesty is '
                                     'your default mode, sometimes delivered '
                                     'with uncomfortable directness. Your '
                                     'greatest virtue is wisdom-seeking; your '
                                     'greatest challenge is commitment.',
                               'hi': 'एक आशावादी, स्वतंत्रता-प्रेमी और '
                                     'दार्शनिक विचारधारा वाला चरित्र आपके जीवन '
                                     'को आगे बढ़ाता है। आप भौतिक लाभ से ऊपर '
                                     'अर्थ तलाशते हैं और नियमित या संकीर्ण सोच '
                                     'से दबा हुआ महसूस करते हैं। ईमानदारी आपका '
                                     'डिफ़ॉल्ट तरीका है, कभी-कभी असुविधाजनक '
                                     'प्रत्यक्षता के साथ प्रस्तुत किया जाता '
                                     'है। आपका सबसे बड़ा गुण ज्ञान-प्राप्ति '
                                     'है; आपकी सबसे बड़ी चुनौती प्रतिबद्धता '
                                     'है।'},
               'Capricorn': {'en': 'Disciplined, ambitious, and profoundly '
                                   'responsible -- your character is built for '
                                   'endurance. You take life seriously, often '
                                   'shouldering burdens others would refuse, '
                                   'without complaint. Time is your ally; you '
                                   'grow stronger, wiser, and more prosperous '
                                   'as you age. Your greatest virtue is '
                                   'perseverance; your greatest challenge is '
                                   'allowing joy.',
                             'hi': 'अनुशासित, महत्वाकांक्षी और अत्यधिक '
                                   'जिम्मेदार - आपका चरित्र धैर्य के लिए बनाया '
                                   'गया है। आप जीवन को गंभीरता से लेते हैं, '
                                   'अक्सर ऐसे बोझ उठाने से जिन्हें दूसरे लोग '
                                   'बिना किसी शिकायत के मना कर देते हैं। समय '
                                   'आपका सहयोगी है; जैसे-जैसे आपकी उम्र बढ़ती '
                                   'है आप मजबूत, समझदार और अधिक समृद्ध होते '
                                   'जाते हैं। आपका सबसे बड़ा गुण दृढ़ता है; '
                                   'आपकी सबसे बड़ी चुनौती आनंद को अनुमति देना '
                                   'है।'},
               'Aquarius': {'en': 'You are an independent thinker with a '
                                  'humanitarian, progressive, and sometimes '
                                  'eccentric character. Conventional '
                                  'expectations feel like chains to you; your '
                                  'mind operates ahead of its time. You value '
                                  'friendship and collective well-being over '
                                  'personal emotional attachment. Your '
                                  'greatest virtue is originality; your '
                                  'greatest challenge is emotional warmth.',
                            'hi': 'आप मानवतावादी, प्रगतिशील और कभी-कभी विलक्षण '
                                  'चरित्र वाले एक स्वतंत्र विचारक हैं। '
                                  'पारंपरिक अपेक्षाएँ आपको जंजीरों की तरह '
                                  'महसूस होती हैं; आपका दिमाग अपने समय से पहले '
                                  'काम करता है। आप व्यक्तिगत भावनात्मक लगाव से '
                                  'अधिक मित्रता और सामूहिक भलाई को महत्व देते '
                                  'हैं। आपका सबसे बड़ा गुण मौलिकता है; आपकी '
                                  'सबसे बड़ी चुनौती भावनात्मक गर्मजोशी है।'},
               'Pisces': {'en': 'A deeply compassionate, intuitive, and '
                                'spiritually attuned character flows through '
                                "your being. You absorb others' emotions like "
                                'a sponge and feel the pain of the world '
                                'acutely. Artistic and mystical gifts are '
                                'abundant, though practical reality can feel '
                                'overwhelming. Your greatest virtue is '
                                'unconditional compassion; your greatest '
                                'challenge is boundaries.',
                          'hi': 'एक गहन दयालु, सहज ज्ञान युक्त और आध्यात्मिक '
                                'रूप से समायोजित चरित्र आपके अस्तित्व में '
                                'प्रवाहित होता है। आप स्पंज की तरह दूसरों की '
                                'भावनाओं को सोख लेते हैं और दुनिया के दर्द को '
                                'तीव्रता से महसूस करते हैं। कलात्मक और रहस्यमय '
                                'उपहार प्रचुर मात्रा में हैं, हालांकि '
                                'व्यावहारिक वास्तविकता भारी लग सकती है। आपका '
                                'सबसे बड़ा गुण बिना शर्त करुणा है; आपकी सबसे '
                                'बड़ी चुनौती सीमाएँ हैं।'}},
 'hobbies': {'Aries': {'en': 'You are naturally drawn to high-energy, '
                             'competitive pursuits. Martial arts, trekking, '
                             'motorsports, and adventure travel satisfy your '
                             'Mars-driven need for adrenaline. You enjoy being '
                             'the first to try new activities and quickly lose '
                             'interest in passive entertainment. Physical '
                             'challenges, outdoor sports, and DIY projects '
                             'keep your restless spirit engaged and happy.',
                       'hi': 'आप स्वाभाविक रूप से उच्च-ऊर्जा, प्रतिस्पर्धी '
                             'गतिविधियों की ओर आकर्षित होते हैं। मार्शल आर्ट, '
                             'ट्रैकिंग, मोटरस्पोर्ट्स और साहसिक यात्राएं आपकी '
                             'मंगल-प्रेरित एड्रेनालाईन की आवश्यकता को पूरा '
                             'करती हैं। आप नई गतिविधियों को सबसे पहले आज़माने '
                             'में आनंद लेते हैं और निष्क्रिय मनोरंजन में रुचि '
                             'जल्दी ही खो देते हैं। शारीरिक चुनौतियाँ, आउटडोर '
                             'खेल और DIY प्रोजेक्ट आपकी बेचैन आत्मा को व्यस्त '
                             'और खुश रखते हैं।'},
             'Taurus': {'en': 'Sensory pleasures define your leisure time. '
                              'Cooking, gardening, music appreciation, '
                              'pottery, and collecting fine objects bring deep '
                              'satisfaction. You prefer hobbies that produce '
                              'tangible results and engage the senses. Nature '
                              'walks, wine tasting, and interior decoration '
                              'reflect your Venus-ruled desire for beauty and '
                              'comfort in every aspect of life.',
                        'hi': 'संवेदी सुख आपके ख़ाली समय को परिभाषित करते हैं। '
                              'खाना पकाना, बागवानी करना, संगीत की प्रशंसा '
                              'करना, मिट्टी के बर्तन बनाना और बढ़िया वस्तुएँ '
                              'इकट्ठा करना गहरी संतुष्टि लाता है। आप ऐसे शौक '
                              'पसंद करते हैं जो ठोस परिणाम देते हैं और '
                              'इंद्रियों को व्यस्त रखते हैं। प्रकृति की सैर, '
                              'वाइन चखना और आंतरिक सजावट जीवन के हर पहलू में '
                              'सुंदरता और आराम की आपकी शुक्र-शासित इच्छा को '
                              'दर्शाती है।'},
             'Gemini': {'en': 'Intellectual stimulation is the thread '
                              'connecting all your hobbies. Reading, puzzles, '
                              'board games, podcasting, blogging, and learning '
                              'new languages keep your Mercury-ruled mind '
                              'active. You tend to have many hobbies '
                              'simultaneously and cycle between them. Social '
                              'hobbies -- debating, quiz competitions, and '
                              'book clubs -- satisfy your need for mental '
                              'sparring and human connection.',
                        'hi': 'बौद्धिक उत्तेजना आपके सभी शौक को जोड़ने वाला '
                              'धागा है। पढ़ना, पहेलियाँ, बोर्ड गेम, '
                              'पॉडकास्टिंग, ब्लॉगिंग और नई भाषाएँ सीखना आपके '
                              'बुध-शासित दिमाग को सक्रिय रखता है। आप एक साथ कई '
                              'शौक पालते हैं और उनके बीच समय-समय पर चलते रहते '
                              'हैं। सामाजिक शौक - वाद-विवाद, प्रश्नोत्तरी '
                              'प्रतियोगिताएं, और पुस्तक क्लब - मानसिक बहस और '
                              'मानवीय संबंध की आपकी आवश्यकता को पूरा करते '
                              'हैं।'},
             'Cancer': {'en': 'Home-centred and emotionally nourishing '
                              'activities are your preferred pastimes. Cooking '
                              'family recipes, scrapbooking, home decoration, '
                              'swimming, and genealogy research satisfy your '
                              'lunar nature. You enjoy hobbies that connect '
                              'you with your roots and create lasting '
                              'memories. Caring for pets, tending a home '
                              'garden, and hosting intimate gatherings bring '
                              'genuine joy.',
                        'hi': 'घर-केंद्रित और भावनात्मक रूप से पौष्टिक '
                              'गतिविधियाँ आपका पसंदीदा शगल हैं। पारिवारिक '
                              'व्यंजन पकाना, स्क्रैपबुकिंग, घर की सजावट, '
                              'तैराकी और वंशावली अनुसंधान आपके चंद्र स्वभाव को '
                              'संतुष्ट करते हैं। आप ऐसे शौक का आनंद लेते हैं '
                              'जो आपको अपनी जड़ों से जोड़ते हैं और स्थायी '
                              'यादें बनाते हैं। पालतू जानवरों की देखभाल करना, '
                              'घर के बगीचे की देखभाल करना और अंतरंग समारोहों '
                              'की मेजबानी करना वास्तविक आनंद लाता है।'},
             'Leo': {'en': 'Creative performance and self-expression drive '
                           'your leisure pursuits. Theatre, dance, painting, '
                           'photography, and any activity where you can shine '
                           'before an audience captivate you. You enjoy '
                           'organising events and being the life of social '
                           'gatherings. Luxury hobbies -- fine dining, '
                           'fashion, and travel to glamorous destinations -- '
                           'appeal to your royal nature.',
                     'hi': 'रचनात्मक प्रदर्शन और आत्म-अभिव्यक्ति आपके अवकाश '
                           'कार्यों को संचालित करते हैं। थिएटर, नृत्य, '
                           'पेंटिंग, फ़ोटोग्राफ़ी, और कोई भी गतिविधि जहाँ आप '
                           'दर्शकों को मंत्रमुग्ध करने के लिए चमक सकें। आप '
                           'कार्यक्रम आयोजित करने और सामाजिक समारोहों की जान '
                           'बनने का आनंद लेते हैं। विलासितापूर्ण शौक - बढ़िया '
                           'भोजन, फैशन और ग्लैमरस स्थलों की यात्रा - आपके शाही '
                           'स्वभाव को आकर्षित करते हैं।'},
             'Virgo': {'en': 'Precision-based and health-oriented hobbies suit '
                             'your analytical Virgo nature. Yoga, herbal '
                             'gardening, journaling, jigsaw puzzles, and '
                             'craft-making satisfy your need for order and '
                             'detail. You enjoy hobbies that improve your '
                             'skills incrementally over time. Reading '
                             'non-fiction, organising spaces, and volunteering '
                             'for service-oriented causes bring quiet but deep '
                             'fulfilment.',
                       'hi': 'परिशुद्धता-आधारित और स्वास्थ्य-उन्मुख शौक आपके '
                             'विश्लेषणात्मक कन्या स्वभाव के अनुकूल हैं। योग, '
                             'हर्बल बागवानी, जर्नलिंग, जिग्सॉ पहेलियां और '
                             'शिल्प-निर्माण ऑर्डर और विवरण की आपकी आवश्यकता को '
                             'पूरा करते हैं। आप ऐसे शौक का आनंद लेते हैं जो '
                             'समय के साथ आपके कौशल में उत्तरोत्तर सुधार करते '
                             'हैं। नॉन-फिक्शन पढ़ना, स्थान व्यवस्थित करना और '
                             'सेवा-उन्मुख कार्यों के लिए स्वयंसेवा करना शांत '
                             'लेकिन गहरी तृप्ति लाता है।'},
             'Libra': {'en': 'Aesthetic and social hobbies define your '
                             'leisure. Painting, music, fashion design, '
                             'ballroom dancing, and art gallery visits feed '
                             'your Venus-ruled craving for beauty and harmony. '
                             'You enjoy activities you can share with a '
                             'partner or close friends. Hosting elegant '
                             'gatherings, interior styling, and cultural '
                             'events are pastimes you naturally excel at.',
                       'hi': 'सौंदर्यात्मक और सामाजिक शौक आपके ख़ाली समय को '
                             'परिभाषित करते हैं। पेंटिंग, संगीत, फैशन डिज़ाइन, '
                             'बॉलरूम नृत्य और आर्ट गैलरी का दौरा आपकी '
                             'शुक्र-शासित सुंदरता और सद्भाव की लालसा को बढ़ाता '
                             'है। आप उन गतिविधियों का आनंद लेते हैं जिन्हें आप '
                             'किसी साथी या करीबी दोस्तों के साथ साझा कर सकते '
                             'हैं। सुंदर समारोहों की मेजबानी करना, आंतरिक '
                             'सज्जा और सांस्कृतिक कार्यक्रम ऐसे शगल हैं जिनमें '
                             'आप स्वाभाविक रूप से उत्कृष्टता प्राप्त करते '
                             'हैं।'},
             'Scorpio': {'en': 'Intense, investigative, and transformative '
                               'hobbies attract you. True crime research, '
                               'psychology study, scuba diving, martial arts, '
                               'and mystery-solving games engage your probing '
                               'Scorpio nature. You prefer depth over variety '
                               'and may pursue a single hobby with obsessive '
                               'dedication. Occult studies, tantric '
                               'meditation, and extreme sports provide the '
                               'intensity you crave.',
                         'hi': 'गहन, खोजी और परिवर्तनकारी शौक आपको आकर्षित '
                               'करते हैं। सच्चा अपराध अनुसंधान, मनोविज्ञान '
                               'अध्ययन, स्कूबा डाइविंग, मार्शल आर्ट और '
                               'रहस्य-सुलझाने वाले खेल आपके वृश्चिक स्वभाव की '
                               'जांच करते हैं। आप विविधता से अधिक गहराई को '
                               'पसंद करते हैं और जुनूनी समर्पण के साथ एक ही '
                               'शौक को पूरा कर सकते हैं। गुप्त अध्ययन, '
                               'तांत्रिक ध्यान और चरम खेल वह तीव्रता प्रदान '
                               'करते हैं जो आप चाहते हैं।'},
             'Sagittarius': {'en': 'Adventure and learning are inseparable in '
                                   'your leisure life. Long-distance travel, '
                                   'horse riding, archery, philosophy reading, '
                                   'and foreign culture exploration light up '
                                   'your Jupiter-ruled spirit. You are the '
                                   'eternal student who finds joy in every new '
                                   'experience and place. Outdoor activities, '
                                   'spiritual retreats, and cultural festivals '
                                   'are your favourite pastimes.',
                             'hi': 'आपके ख़ाली जीवन में रोमांच और सीखना '
                                   'अविभाज्य हैं। लंबी दूरी की यात्रा, '
                                   'घुड़सवारी, तीरंदाजी, दर्शनशास्त्र पढ़ना और '
                                   'विदेशी संस्कृति की खोज आपकी बृहस्पति-शासित '
                                   'भावना को उजागर करती है। आप शाश्वत छात्र '
                                   'हैं जो हर नए अनुभव और स्थान में आनंद पाते '
                                   'हैं। बाहरी गतिविधियाँ, आध्यात्मिक विश्राम '
                                   'और सांस्कृतिक उत्सव आपके पसंदीदा शगल हैं।'},
             'Capricorn': {'en': 'Structured, goal-oriented hobbies satisfy '
                                 'your Saturn-ruled temperament. Mountain '
                                 'climbing, chess, woodworking, numismatics, '
                                 'and historical study appeal to your '
                                 'disciplined nature. You prefer hobbies that '
                                 'build skill over time and produce measurable '
                                 'results. Antique collecting, architecture '
                                 'appreciation, and strategic board games are '
                                 'lifelong interests.',
                           'hi': 'संरचित, लक्ष्य-उन्मुख शौक आपके शनि-शासित '
                                 'स्वभाव को संतुष्ट करते हैं। पर्वतारोहण, '
                                 'शतरंज, लकड़ी का काम, मुद्राशास्त्र और '
                                 'ऐतिहासिक अध्ययन आपके अनुशासित स्वभाव को '
                                 'आकर्षित करते हैं। आप ऐसे शौक पसंद करते हैं '
                                 'जो समय के साथ कौशल का निर्माण करते हैं और '
                                 'मापने योग्य परिणाम देते हैं। प्राचीन वस्तुओं '
                                 'का संग्रह, वास्तुकला की सराहना और रणनीतिक '
                                 'बोर्ड गेम आजीवन रुचि रखते हैं।'},
             'Aquarius': {'en': 'Unconventional and technology-driven hobbies '
                                'excite your progressive nature. Astronomy, '
                                'coding, drone flying, electronic music '
                                'production, and social activism are '
                                'characteristic pursuits. You enjoy hobbies '
                                'that connect you with like-minded communities '
                                'or push societal boundaries. Science fiction, '
                                'futuristic gadgets, and humanitarian '
                                'volunteering reflect your visionary Aquarian '
                                'spirit.',
                          'hi': 'अपरंपरागत और प्रौद्योगिकी-संचालित शौक आपके '
                                'प्रगतिशील स्वभाव को उत्साहित करते हैं। खगोल '
                                'विज्ञान, कोडिंग, ड्रोन उड़ान, इलेक्ट्रॉनिक '
                                'संगीत उत्पादन और सामाजिक सक्रियता विशिष्ट '
                                'गतिविधियाँ हैं। आप ऐसे शौक का आनंद लेते हैं '
                                'जो आपको समान विचारधारा वाले समुदायों से '
                                'जोड़ते हैं या सामाजिक सीमाओं को तोड़ते हैं। '
                                'विज्ञान कथा, भविष्य के गैजेट और मानवीय '
                                'स्वयंसेवा आपकी दूरदर्शी कुंभ भावना को दर्शाते '
                                'हैं।'},
             'Pisces': {'en': 'Creative and spiritual hobbies nourish your '
                              'sensitive Piscean soul. Music, painting, '
                              'poetry, swimming, meditation, and dream '
                              'journaling are natural outlets for your vast '
                              'imagination. You are drawn to activities near '
                              'water and those that allow emotional or '
                              'spiritual expression. Film appreciation, '
                              'charity work, and healing arts like Reiki or '
                              'crystal therapy bring deep peace.',
                        'hi': 'रचनात्मक और आध्यात्मिक शौक आपकी संवेदनशील मीन '
                              'आत्मा को पोषण देते हैं। संगीत, पेंटिंग, कविता, '
                              'तैराकी, ध्यान और स्वप्न जर्नलिंग आपकी विशाल '
                              'कल्पना के लिए प्राकृतिक आउटलेट हैं। आप पानी के '
                              'निकट की गतिविधियों और ऐसी गतिविधियों की ओर '
                              'आकर्षित होते हैं जो भावनात्मक या आध्यात्मिक '
                              'अभिव्यक्ति की अनुमति देती हैं। फिल्म की सराहना, '
                              'दान कार्य और रेकी या क्रिस्टल थेरेपी जैसी उपचार '
                              'कलाएं गहरी शांति लाती हैं।'}},
 'family': {'Aries': {'en': 'Mars energy on the 4th house creates a dynamic '
                            'but sometimes volatile home environment. You take '
                            'charge of family matters with decisive authority. '
                            'Property disputes or renovation projects are '
                            'common themes. Independence was established early '
                            '-- you may have left home young. Family '
                            'relationships improve when you channel '
                            'competitive energy into protecting rather than '
                            'controlling.',
                      'hi': 'चौथे घर पर मंगल की ऊर्जा एक गतिशील लेकिन कभी-कभी '
                            'अस्थिर घरेलू वातावरण बनाती है। आप पारिवारिक '
                            'मामलों की जिम्मेदारी निर्णायक अधिकार के साथ लेते '
                            'हैं। संपत्ति विवाद या नवीकरण परियोजनाएं आम विषय '
                            'हैं। स्वतंत्रता की स्थापना जल्दी हो गई थी - हो '
                            'सकता है कि आपने युवावस्था में ही घर छोड़ दिया हो। '
                            'जब आप प्रतिस्पर्धी ऊर्जा को नियंत्रित करने के '
                            'बजाय सुरक्षा में लगाते हैं तो पारिवारिक रिश्ते '
                            'बेहतर होते हैं।'},
            'Taurus': {'en': 'Venus-ruled Taurus on the 4th house is excellent '
                             'for domestic happiness and property ownership. '
                             'Your home is comfortable, well-decorated, and a '
                             'source of genuine pride. Family bonds are strong '
                             'and enduring, especially with your mother. '
                             'Ancestral property and family wealth are likely. '
                             'Stability and tradition are the pillars of your '
                             'family life across generations.',
                       'hi': 'चौथे घर पर शुक्र-शासित वृषभ घरेलू सुख और संपत्ति '
                             'के स्वामित्व के लिए उत्कृष्ट है। आपका घर '
                             'आरामदायक, अच्छी तरह से सजाया हुआ और वास्तविक '
                             'गौरव का स्रोत है। पारिवारिक बंधन मजबूत और स्थायी '
                             'होते हैं, विशेषकर आपकी माँ के साथ। पैतृक संपत्ति '
                             'और पारिवारिक संपत्ति मिलने की संभावना है। '
                             'स्थिरता और परंपरा पीढ़ियों तक आपके पारिवारिक '
                             'जीवन के आधार हैं।'},
            'Gemini': {'en': "Mercury's influence on the 4th house creates an "
                             'intellectually stimulating home environment. '
                             'Family discussions, debates, and a house full of '
                             'books and media define your domestic space. You '
                             'may change residences frequently or have '
                             'multiple properties. Family communication is '
                             'lively but sometimes superficial -- deeper '
                             'emotional bonding requires conscious effort.',
                       'hi': 'चतुर्थ भाव पर बुध का प्रभाव घर में बौद्धिक रूप '
                             'से उत्साहवर्धक वातावरण बनाता है। पारिवारिक '
                             'चर्चाएँ, बहसें और किताबों और मीडिया से भरा घर '
                             'आपके घरेलू स्थान को परिभाषित करता है। आप बार-बार '
                             'आवास बदल सकते हैं या आपके पास कई संपत्तियां हो '
                             'सकती हैं। पारिवारिक संचार जीवंत लेकिन कभी-कभी '
                             'सतही होता है - गहरे भावनात्मक बंधन के लिए सचेत '
                             'प्रयास की आवश्यकता होती है।'},
            'Cancer': {'en': 'The Moon ruling the 4th house is the most '
                             'natural and powerful placement for family '
                             "happiness. Your mother's influence is profound "
                             'and your attachment to ancestral home and '
                             'traditions is deep. Nurturing your family is '
                             'your primary source of emotional fulfilment. '
                             'Property near water, a well-stocked kitchen, and '
                             'family gatherings define your domestic bliss.',
                       'hi': 'चतुर्थ भाव पर शासन करने वाला चंद्रमा पारिवारिक '
                             'सुख के लिए सबसे प्राकृतिक और शक्तिशाली स्थान है। '
                             'आपकी माँ का प्रभाव गहरा है और पैतृक घर और '
                             'परंपराओं से आपका लगाव गहरा है। अपने परिवार का '
                             'पालन-पोषण आपकी भावनात्मक संतुष्टि का प्राथमिक '
                             'स्रोत है। पानी के पास की संपत्ति, एक अच्छी तरह '
                             'से भंडारित रसोईघर और पारिवारिक समारोह आपके घरेलू '
                             'आनंद को परिभाषित करते हैं।'},
            'Leo': {'en': 'Sun-ruled Leo on the 4th house creates a proud, '
                          'dignified home environment. Your residence reflects '
                          'your status -- spacious, well-lit, and impressive. '
                          "Father's influence on family culture is strong. You "
                          'take pride in your lineage and family achievements. '
                          'Generosity toward family members and a regal '
                          'household atmosphere characterise your home life.',
                    'hi': 'चौथे घर पर सूर्य शासित सिंह राशि एक गौरवपूर्ण, '
                          'सम्मानजनक घरेलू वातावरण बनाती है। आपका निवास आपकी '
                          'स्थिति को दर्शाता है - विशाल, अच्छी रोशनी वाला और '
                          'प्रभावशाली। पारिवारिक संस्कृति पर पिता का प्रभाव '
                          'प्रबल होता है। आप अपनी वंशावली और पारिवारिक '
                          'उपलब्धियों पर गर्व करते हैं। परिवार के सदस्यों के '
                          'प्रति उदारता और शाही घरेलू माहौल आपके घरेलू जीवन की '
                          'विशेषता है।'},
            'Virgo': {'en': 'Mercury-ruled Virgo on the 4th house creates an '
                            'orderly, health-conscious home environment. '
                            'Cleanliness, routine, and practical efficiency '
                            'define your domestic life. Your mother is '
                            'detail-oriented and health-focused. Property '
                            'investments are carefully researched and '
                            'sensible. Family relationships improve when you '
                            'relax your critical standards and accept '
                            'imperfection.',
                      'hi': 'चौथे घर पर बुध-शासित कन्या एक व्यवस्थित, '
                            'स्वास्थ्य के प्रति जागरूक घरेलू वातावरण बनाता है। '
                            'स्वच्छता, दिनचर्या और व्यावहारिक दक्षता आपके '
                            'घरेलू जीवन को परिभाषित करती है। आपकी माँ '
                            'विस्तार-उन्मुख और स्वास्थ्य-केंद्रित हैं। संपत्ति '
                            'निवेश सावधानीपूर्वक शोधित और समझदारीपूर्ण होता '
                            'है। जब आप अपने महत्वपूर्ण मानकों को शिथिल करते '
                            'हैं और अपूर्णता को स्वीकार करते हैं तो पारिवारिक '
                            'रिश्ते बेहतर होते हैं।'},
            'Libra': {'en': 'Venus-ruled Libra on the 4th house blesses the '
                            'home with beauty, harmony, and social grace. Your '
                            'residence is tastefully decorated and serves as a '
                            'gathering place for friends and family. Both '
                            'parents contribute equally to your upbringing. '
                            'Property with aesthetic appeal attracts you. '
                            'Family peace depends on maintaining balance and '
                            'avoiding taking sides in domestic disputes.',
                      'hi': 'चौथे घर पर शुक्र-शासित तुला घर को सुंदरता, सद्भाव '
                            'और सामाजिक अनुग्रह का आशीर्वाद देती है। आपका '
                            'निवास शानदार ढंग से सजाया गया है और दोस्तों और '
                            'परिवार के लिए एक सभा स्थल के रूप में कार्य करता '
                            'है। आपके पालन-पोषण में माता-पिता दोनों समान रूप '
                            'से योगदान देते हैं। सौन्दर्यात्मक आकर्षण वाली '
                            'संपत्ति आपको आकर्षित करती है। पारिवारिक शांति '
                            'संतुलन बनाए रखने और घरेलू विवादों में किसी का '
                            'पक्ष लेने से बचने पर निर्भर करती है।'},
            'Scorpio': {'en': 'Mars-Ketu ruled Scorpio on the 4th house '
                              'creates deep, intense family dynamics. Family '
                              'secrets, ancestral karma, and transformative '
                              'domestic experiences shape your inner life. '
                              'Property matters may involve disputes or '
                              'dramatic changes. Your emotional attachment to '
                              'home runs very deep despite an outward '
                              'appearance of detachment. Healing family karma '
                              'is a life theme.',
                        'hi': 'चतुर्थ भाव पर मंगल-केतु का आधिपत्य वृश्चिक राशि '
                              'में गहरी, गहन पारिवारिक गतिशीलता पैदा करता है। '
                              'पारिवारिक रहस्य, पैतृक कर्म और परिवर्तनकारी '
                              'घरेलू अनुभव आपके आंतरिक जीवन को आकार देते हैं। '
                              'संपत्ति के मामलों में विवाद या नाटकीय परिवर्तन '
                              'शामिल हो सकते हैं। बाहरी अलगाव के बावजूद घर से '
                              'आपका भावनात्मक लगाव बहुत गहरा है। पारिवारिक '
                              'कर्म को ठीक करना जीवन का विषय है।'},
            'Sagittarius': {'en': "Jupiter's blessing on the 4th house creates "
                                  'an expansive, philosophical, and fortunate '
                                  'home life. Your family values education, '
                                  'ethics, and spiritual growth. Property '
                                  'ownership is indicated, often in multiple '
                                  'locations or abroad. Your home functions as '
                                  'a place of learning and wisdom. '
                                  'International connections within the family '
                                  'and a liberal, open-minded household '
                                  'atmosphere prevail.',
                            'hi': 'चतुर्थ भाव पर बृहस्पति का आशीर्वाद एक '
                                  'विस्तृत, दार्शनिक और भाग्यशाली घरेलू जीवन '
                                  'बनाता है। आपका परिवार शिक्षा, नैतिकता और '
                                  'आध्यात्मिक विकास को महत्व देता है। संपत्ति '
                                  'के स्वामित्व का संकेत अक्सर कई स्थानों या '
                                  'विदेश में दिया जाता है। आपका घर सीखने और '
                                  'ज्ञान के स्थान के रूप में कार्य करता है। '
                                  'परिवार के भीतर अंतर्राष्ट्रीय संबंध और एक '
                                  'उदार, खुले विचारों वाला घरेलू माहौल कायम '
                                  'है।'},
            'Capricorn': {'en': 'Saturn-ruled Capricorn on the 4th house '
                                'creates a structured, disciplined family '
                                'environment. Emotional warmth may have been '
                                'scarce in early life, replaced by duty and '
                                'responsibility. Property accumulation is slow '
                                'but substantial. Family traditions and '
                                'ancestral obligations are taken seriously. '
                                'Domestic happiness increases markedly after '
                                'middle age as Saturn rewards patience.',
                          'hi': 'चौथे घर पर शनि द्वारा शासित मकर राशि एक '
                                'संरचित, अनुशासित पारिवारिक वातावरण बनाती है। '
                                'प्रारंभिक जीवन में भावनात्मक गर्मजोशी कम रही '
                                'होगी, उसकी जगह कर्तव्य और जिम्मेदारी ने ले '
                                'ली। संपत्ति संचय धीमा है लेकिन पर्याप्त है। '
                                'पारिवारिक परंपराओं और पैतृक दायित्वों को '
                                'गंभीरता से लिया जाता है। मध्य आयु के बाद '
                                'घरेलू सुख में उल्लेखनीय वृद्धि होती है '
                                'क्योंकि शनि धैर्य का पुरस्कार देता है।'},
            'Aquarius': {'en': 'Saturn-Rahu influenced Aquarius on the 4th '
                               'house creates an unconventional home life. '
                               'Your family may be progressive, scattered '
                               'geographically, or non-traditional in '
                               'structure. Technology plays a large role in '
                               'your domestic space. Emotional distance from '
                               'roots is possible but compensated by '
                               'chosen-family bonds. Property in unusual '
                               'locations or modern apartments suits you.',
                         'hi': 'चतुर्थ भाव पर शनि-राहु से प्रभावित कुंभ राशि '
                               'एक अपरंपरागत घरेलू जीवन बनाती है। आपका परिवार '
                               'प्रगतिशील, भौगोलिक रूप से बिखरा हुआ, या संरचना '
                               'में गैर-पारंपरिक हो सकता है। प्रौद्योगिकी आपके '
                               'घरेलू क्षेत्र में एक बड़ी भूमिका निभाती है। '
                               'जड़ों से भावनात्मक दूरी संभव है लेकिन इसकी '
                               'भरपाई चुने हुए पारिवारिक बंधनों से होती है। '
                               'असामान्य स्थानों या आधुनिक अपार्टमेंट में '
                               'संपत्ति आपके लिए उपयुक्त है।'},
            'Pisces': {'en': 'Jupiter-ruled Pisces on the 4th house creates a '
                             'spiritually rich and emotionally nourishing '
                             'home. Your mother is compassionate and possibly '
                             'spiritually inclined. The home serves as a '
                             "sanctuary from the world's harshness. Property "
                             'near water is highly favourable. Family life is '
                             'gentle, artistic, and deeply connected to '
                             'devotion and selfless love.',
                       'hi': 'चौथे घर पर बृहस्पति शासित मीन राशि आध्यात्मिक '
                             'रूप से समृद्ध और भावनात्मक रूप से पौष्टिक घर '
                             'बनाती है। आपकी माँ दयालु हैं और संभवतः '
                             'आध्यात्मिक रुझान वाली हैं। घर दुनिया की कठोरता '
                             'से एक अभयारण्य के रूप में कार्य करता है। पानी के '
                             'पास की संपत्ति अत्यधिक अनुकूल होती है। पारिवारिक '
                             'जीवन सौम्य, कलात्मक और भक्ति और निस्वार्थ प्रेम '
                             'से गहराई से जुड़ा हुआ है।'}}}
