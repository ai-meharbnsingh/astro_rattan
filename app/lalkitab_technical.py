"""
lalkitab_technical.py — Advanced Lal Kitab Technical Logic
============================================================
1. Chalti Gaadi  — Moving Train (Houses 1, 7, 8)
2. Dhur-Dhur-Aage — The Push (consecutive house planets)
3. Soya Ghar (Enhanced) — Sleeping Houses with aspect-based awakening
4. Sarkari / Gair-Sarkari — Government vs Private status
5. Bhedi Grah — Spy Planet (house 8→2, 6→12, 3→9 axes)
6. Zakhmi Grah — Wounded Planet (Takkar from 7th)
7. Pardesi Grah — Foreigner Planet (no natural connection)
8. Muth-Thi — Fistful logic (in-hand vs out-hand planets)
"""
from typing import List, Dict, Any, Optional

# ============================================================
# SHARED CONSTANTS
# ============================================================
# Pakka Ghar imported from lalkitab_advanced
_PAKKA: Dict[str, int] = {
    "Sun": 1, "Moon": 4, "Mars": 3, "Mercury": 7,
    "Jupiter": 2, "Venus": 7, "Saturn": 8, "Rahu": 12, "Ketu": 6,
}

LK_ENEMIES: Dict[str, set] = {
    "Sun":     {"Saturn", "Rahu", "Ketu"},
    "Moon":    {"Rahu", "Ketu"},
    "Mars":    {"Mercury", "Ketu"},
    "Mercury": {"Moon", "Ketu"},
    "Jupiter": {"Mercury", "Venus", "Rahu", "Ketu", "Saturn"},
    "Venus":   {"Sun", "Moon", "Rahu"},
    "Saturn":  {"Sun", "Moon", "Mars"},
    "Rahu":    {"Sun", "Moon", "Jupiter"},
    "Ketu":    {"Moon", "Mars"},
}

BENEFIC_PLANETS = {"Jupiter", "Venus", "Moon", "Mercury"}
MALEFIC_PLANETS = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}

# Natural house connections for Pardesi check
_NATURAL_HOUSES: Dict[str, set] = {
    "Sun":     {1, 5, 9, 10},
    "Moon":    {2, 4, 11},
    "Mars":    {1, 3, 6, 8, 10},
    "Mercury": {2, 6, 7, 10},
    "Jupiter": {2, 5, 9, 11, 12},
    "Venus":   {2, 4, 7, 8, 12},
    "Saturn":  {6, 8, 10, 11, 12},
    "Rahu":    {6, 8, 12},
    "Ketu":    {6, 8, 12},
}

# Sarkari (Government) planets + houses
_SARKARI_PLANETS = {"Sun", "Mars", "Jupiter"}
_SARKARI_HOUSES = {1, 5, 9, 10, 11}

# ============================================================
# 1. CHALTI GAADI (Moving Train)
# ============================================================

def _safe_positions(planet_positions: List[Dict]) -> List[Dict]:
    """Filter out malformed entries missing planet or house."""
    return [p for p in planet_positions if p.get("planet") and isinstance(p.get("house"), int)]


def _get_strongest_planet(planet_positions: List[Dict], house: int) -> Optional[str]:
    planets_in = [p["planet"] for p in _safe_positions(planet_positions) if p["house"] == house]
    if not planets_in:
        return None
    # Priority: Pakka Ghar > non-dusthana > anything
    for p in planets_in:
        if _PAKKA.get(p) == house:
            return p
    for p in planets_in:
        if house not in {6, 8, 12}:
            return p
    return planets_in[0]


def calculate_chalti_gaadi(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Engine (house 1) + Passenger (house 7) + Brakes (house 8)
    Determines the status and dynamic of the life-train.
    """
    engine   = _get_strongest_planet(planet_positions, 1)
    passenger = _get_strongest_planet(planet_positions, 7)
    brakes   = _get_strongest_planet(planet_positions, 8)

    def is_enemy(p1: Optional[str], p2: Optional[str]) -> bool:
        if not p1 or not p2:
            return False
        return p2 in LK_ENEMIES.get(p1, set()) or p1 in LK_ENEMIES.get(p2, set())

    def is_friend(p1: Optional[str], p2: Optional[str]) -> bool:
        if not p1 or not p2 or p1 == p2:
            return False
        return not is_enemy(p1, p2) and p1 != p2

    rules = []
    # Determine status
    if not engine and not passenger and not brakes:
        train_status = "empty"
        interp_en = "No planets in the train houses (1, 7, 8). Life progresses steadily without dramatic peaks or sudden stops."
        interp_hi = "ट्रेन घरों (1, 7, 8) में कोई ग्रह नहीं। जीवन बिना नाटकीय उतार-चढ़ाव के शांत रूप से आगे बढ़ता है।"
    elif engine and passenger and is_enemy(engine, passenger) and brakes:
        train_status = "stalled"
        interp_en = f"Engine {engine} and Passenger {passenger} are enemies — efforts don't translate to results. The journey is blocked."
        interp_hi = f"इंजन {engine} और यात्री {passenger} शत्रु हैं — प्रयास परिणाम नहीं देते। यात्रा अवरुद्ध है।"
        rules.append({"rule": "enemy_engine_passenger", "applies": True, "note": {"en": "Conflicts between initiative and partnership delay progress.", "hi": "पहल और साझेदारी के बीच संघर्ष प्रगति में देरी करता है।"}})
    elif engine and brakes and is_enemy(engine, brakes):
        train_status = "dangerous"
        interp_en = f"Engine {engine} is blocked by Brakes {brakes} — enemies in 1st and 8th cause sudden accidents or health crises."
        interp_hi = f"इंजन {engine} ब्रेक {brakes} से अवरुद्ध है — 1st और 8th में शत्रु अचानक दुर्घटना या स्वास्थ्य संकट का कारण।"
        rules.append({"rule": "enemy_engine_brakes", "applies": True, "note": {"en": "High accident and health risk. Avoid rash decisions.", "hi": "उच्च दुर्घटना और स्वास्थ्य जोखिम।"}})
    elif engine and passenger and is_friend(engine, passenger):
        train_status = "smooth"
        interp_en = f"Engine {engine} and Passenger {passenger} are friends — life progresses naturally, efforts bring results, partnerships are harmonious."
        interp_hi = f"इंजन {engine} और यात्री {passenger} मित्र हैं — जीवन स्वाभाविक रूप से आगे बढ़ता है, प्रयास परिणाम देते हैं।"
        rules.append({"rule": "friend_engine_passenger", "applies": True, "note": {"en": "Smooth life journey with cooperative relationships.", "hi": "सहकारी संबंधों के साथ सुगम जीवन यात्रा।"}})
    elif not engine and passenger:
        train_status = "drifting"
        interp_en = "No engine — life is directed by others. Passengers (partners) hold the wheel. Develop independence."
        interp_hi = "इंजन नहीं — जीवन दूसरों द्वारा निर्देशित है। स्वतंत्रता विकसित करें।"
    elif not brakes:
        train_status = "uncontrolled"
        interp_en = "No brakes — rapid cycles of gain and loss. Discipline required to avoid reckless decisions."
        interp_hi = "ब्रेक नहीं — तीव्र लाभ और हानि के चक्र। अनुशासन आवश्यक।"
    else:
        train_status = "moving"
        interp_en = "The train is in motion. Mixed signals — progress is possible with awareness."
        interp_hi = "ट्रेन चल रही है। मिश्रित संकेत — जागरूकता के साथ प्रगति संभव।"

    # Passenger+Brakes friend = protected
    if passenger and brakes and is_friend(passenger, brakes):
        rules.append({"rule": "friend_passenger_brakes", "applies": True, "note": {"en": "Partnerships survive shocks — brakes are gentle.", "hi": "साझेदारी झटकों से बचती है।"}})

    from app.lalkitab_source_tags import source_of
    return {
        "engine":     {"planet": engine, "house": 1} if engine else None,
        "passenger":  {"planet": passenger, "house": 7} if passenger else None,
        "brakes":     {"planet": brakes, "house": 8} if brakes else None,
        "train_status": train_status,
        "interpretation": {"en": interp_en, "hi": interp_hi},
        "specific_rules": rules,
        "source": source_of("calculate_chalti_gaadi"),  # PRODUCT
    }


# ============================================================
# 2. DHUR-DHUR-AAGE (The Push)
# ============================================================

def calculate_dhur_dhur_aage(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Planet in house N-1 pushes planet in house N.
    House 12 pushes house 1 (circular).
    """
    h_map: Dict[int, List[str]] = {}
    for p in _safe_positions(planet_positions):
        h_map.setdefault(p["house"], []).append(p["planet"])

    pushes = []
    push_count: Dict[str, int] = {}
    pushed_count: Dict[str, int] = {}

    for house in range(1, 13):
        prev_house = 12 if house == 1 else house - 1
        pushers = h_map.get(prev_house, [])
        receivers = h_map.get(house, [])

        if pushers and receivers:
            for pusher in pushers:
                for receiver in receivers:
                    # Direction
                    if pusher in BENEFIC_PLANETS and prev_house not in {6, 8, 12}:
                        direction = "benefic"
                        interp_en = f"{pusher} (house {prev_house}) benevolently propels {receiver} (house {house}) toward positive results."
                        interp_hi = f"{pusher} (घर {prev_house}) {receiver} (घर {house}) को सकारात्मक परिणामों की ओर धकेलता है।"
                    elif pusher in MALEFIC_PLANETS or prev_house in {6, 8, 12}:
                        direction = "malefic"
                        interp_en = f"{pusher} (house {prev_house}) forces {receiver} (house {house}) into distress and obstacles."
                        interp_hi = f"{pusher} (घर {prev_house}) {receiver} (घर {house}) को कष्ट और बाधाओं में धकेलता है।"
                    else:
                        direction = "neutral"
                        interp_en = f"{pusher} (house {prev_house}) creates mild momentum for {receiver} (house {house})."
                        interp_hi = f"{pusher} (घर {prev_house}) {receiver} (घर {house}) के लिए हल्की गति बनाता है।"

                    pushes.append({
                        "pusher": pusher,
                        "pusher_house": prev_house,
                        "receiver": receiver,
                        "receiver_house": house,
                        "direction": direction,
                        "interpretation": {"en": interp_en, "hi": interp_hi},
                    })
                    push_count[pusher] = push_count.get(pusher, 0) + 1
                    pushed_count[receiver] = pushed_count.get(receiver, 0) + 1

    most_pushed = max(pushed_count, key=pushed_count.get) if pushed_count else None
    most_pushful = max(push_count, key=push_count.get) if push_count else None

    if not pushes:
        summary = {"en": "No consecutive house planet pairs found. No direct push relationships in this chart.", "hi": "लगातार घर ग्रह जोड़े नहीं मिले।"}
    else:
        summary = {"en": f"{len(pushes)} push relationship(s) detected. {most_pushful} is the primary force; {most_pushed} receives the most pressure.", "hi": f"{len(pushes)} धक्का संबंध मिले।"}

    return {
        "pushes": pushes,
        "most_pushed_planet": most_pushed,
        "most_pushful_planet": most_pushful,
        "summary": summary,
    }


# ============================================================
# 3. SOYA GHAR (Enhanced — with Aspect-Based Awakening)
# ============================================================

# LK Aspect pairs: planet in house X aspects house Y
_LK_ASPECT_PAIRS: List[tuple] = [
    (1, 7), (7, 1),
    (4, 10), (10, 4),
    (5, 9), (9, 5),
    (3, 9), (9, 3),
    (1, 5), (5, 1),
    (2, 8), (8, 2),
    (6, 12), (12, 6),
]

_SLEEPING_HOUSE_EFFECTS: Dict[int, Dict[str, str]] = {
    1:  {"en": "Sleeping 1st house: Self-confidence and identity are dormant. Personality lacks direction.", "hi": "सोया हुआ पहला घर: आत्मविश्वास और पहचान सुप्त हैं।"},
    2:  {"en": "Sleeping 2nd house: Wealth and family harmony are inactive. Financial flow is blocked.", "hi": "सोया हुआ दूसरा घर: धन और पारिवारिक सामंजस्य निष्क्रिय हैं।"},
    3:  {"en": "Sleeping 3rd house: Communication and initiative are weak. Siblings may be distant.", "hi": "सोया हुआ तीसरा घर: संचार और पहल कमजोर है।"},
    4:  {"en": "Sleeping 4th house: Home and mother's blessings are inactive. Emotional security lacks foundation.", "hi": "सोया हुआ चौथा घर: घर और माता के आशीर्वाद निष्क्रिय हैं।"},
    5:  {"en": "Sleeping 5th house: Creativity and intelligence are dormant. Children or speculative gains may be delayed.", "hi": "सोया हुआ पांचवां घर: रचनात्मकता और बुद्धि सुप्त हैं।"},
    6:  {"en": "Sleeping 6th house: Enemies sleep too — minimal conflicts. Service and health routines need activation.", "hi": "सोया हुआ छठा घर: शत्रु भी सो रहे हैं — न्यूनतम संघर्ष।"},
    7:  {"en": "Sleeping 7th house: Partnerships and marriage are delayed or passive. Business ventures lack spark.", "hi": "सोया हुआ सातवां घर: साझेदारी और विवाह निष्क्रिय हैं।"},
    8:  {"en": "Sleeping 8th house: Karmic debts are inactive — life is relatively shielded from sudden transformations.", "hi": "सोया हुआ आठवां घर: कर्मिक ऋण निष्क्रिय हैं।"},
    9:  {"en": "Sleeping 9th house: Fortune and father's blessings are inactive. Spiritual path needs effort.", "hi": "सोया हुआ नौवां घर: भाग्य और पिता के आशीर्वाद निष्क्रिय हैं।"},
    10: {"en": "Sleeping 10th house: Career is stagnant. Ambition needs awakening through consistent effort.", "hi": "सोया हुआ दसवां घर: करियर स्थिर है।"},
    11: {"en": "Sleeping 11th house: Income streams and social networks are inactive. Focus on building connections.", "hi": "सोया हुआ ग्यारहवां घर: आय धाराएं और सामाजिक नेटवर्क निष्क्रिय हैं।"},
    12: {"en": "Sleeping 12th house: Foreign opportunities and spiritual liberation are not yet activated.", "hi": "सोया हुआ बारहवां घर: विदेशी अवसर और आध्यात्मिक मुक्ति सक्रिय नहीं।"},
}

_SLEEPING_HOUSE_REMEDIES: Dict[int, Dict[str, str]] = {
    1:  {"en": "Start a daily sunrise meditation practice. Engage in active self-improvement.", "hi": "प्रतिदिन सूर्योदय ध्यान करें।"},
    2:  {"en": "Keep a silver coin in your wallet. Recite 'Om Hreem Shreem' 108 times daily.", "hi": "बटुए में चांदी का सिक्का रखें।"},
    3:  {"en": "Write a letter or journal daily. Connect with siblings or cousins.", "hi": "प्रतिदिन पत्र या जर्नल लिखें।"},
    4:  {"en": "Spend time at home daily. Serve your mother. Plant a tulsi plant.", "hi": "प्रतिदिन घर पर समय बिताएं। माता की सेवा करें।"},
    5:  {"en": "Engage in creative activities daily. Play with children or teach.", "hi": "प्रतिदिन रचनात्मक गतिविधियां करें।"},
    6:  {"en": "Exercise daily. Serve animals. Donate to medical causes on Tuesdays.", "hi": "प्रतिदिन व्यायाम करें।"},
    7:  {"en": "Strengthen your primary relationship. Make time for partnerships.", "hi": "अपने प्राथमिक संबंध को मजबूत करें।"},
    8:  {"en": "Study occult or spiritual texts. Accept transformations as growth.", "hi": "आध्यात्मिक ग्रंथ पढ़ें।"},
    9:  {"en": "Respect elders and teachers. Visit a place of worship weekly.", "hi": "बड़ों और शिक्षकों का सम्मान करें।"},
    10: {"en": "Set a 90-day career goal and pursue it consistently.", "hi": "90 दिन का करियर लक्ष्य निर्धारित करें।"},
    11: {"en": "Join a professional network. Connect with one new person weekly.", "hi": "एक पेशेवर नेटवर्क से जुड़ें।"},
    12: {"en": "Meditate or do spiritual practice for 20 minutes before sleep.", "hi": "सोने से पहले 20 मिनट ध्यान करें।"},
}


def calculate_soya_ghar(
    planet_positions: List[Dict[str, Any]],
    planet_strengths: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Enhanced sleeping house calculation with aspect-based awakening.
    """
    h_map: Dict[int, List[str]] = {}
    for p in _safe_positions(planet_positions):
        h_map.setdefault(p["house"], []).append(p["planet"])

    # Determine waking planets
    waking_planets = []
    for p in _safe_positions(planet_positions):
        planet = p["planet"]
        house = p["house"]
        pakka = _PAKKA.get(planet, 0)
        strength = (planet_strengths or {}).get(planet, 0.5)
        # Waking if in Pakka Ghar, or strong (>0.5) and not in dusthana
        if house == pakka or (strength > 0.5 and house not in {6, 8, 12}):
            if planet not in waking_planets:
                waking_planets.append(planet)

    # Build aspect map: which houses does each waking planet aspect?
    house_waking_aspects: Dict[int, List[Dict]] = {h: [] for h in range(1, 13)}
    for p in _safe_positions(planet_positions):
        if p["planet"] not in waking_planets:
            continue
        from_house = p["house"]
        for (h1, h2) in _LK_ASPECT_PAIRS:
            if h1 == from_house:
                house_waking_aspects[h2].append({"from_planet": p["planet"], "from_house": from_house})

    awake_houses = []
    sleeping_houses = []
    sleeping_house_effects = []

    for house in range(1, 13):
        has_planet = bool(h_map.get(house))
        has_waking_aspect = bool(house_waking_aspects[house])
        if has_planet or has_waking_aspect:
            awake_houses.append(house)
        else:
            sleeping_houses.append(house)
            effect = _SLEEPING_HOUSE_EFFECTS.get(house, {"en": f"House {house} is inactive.", "hi": f"घर {house} निष्क्रिय है।"})
            remedy = _SLEEPING_HOUSE_REMEDIES.get(house, {"en": "Activate this house through consistent effort.", "hi": "लगातार प्रयास से इस घर को सक्रिय करें।"})
            sleeping_house_effects.append({
                "house": house,
                "effect": effect,
                "remedy": remedy,
            })

    return {
        "awake_houses": awake_houses,
        "sleeping_houses": sleeping_houses,
        "waking_planets": waking_planets,
        "house_waking_aspects": house_waking_aspects,
        "sleeping_house_effects": sleeping_house_effects,
        "summary": {
            "en": f"{len(awake_houses)} awake houses, {len(sleeping_houses)} sleeping. Waking planets: {', '.join(waking_planets) or 'None'}.",
            "hi": f"{len(awake_houses)} जागते घर, {len(sleeping_houses)} सोते घर।"
        },
    }


# ============================================================
# 4. SARKARI / GAIR-SARKARI + BHEDI + ZAKHMI + PARDESI
# ============================================================

def classify_all_planet_statuses(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Classifies each planet with 4 advanced LK status flags.
    Returns list of planet dicts with status info.
    """
    safe = _safe_positions(planet_positions)
    # Use last occurrence for any duplicate planet (chart data integrity issue — caller should deduplicate)
    p_map: Dict[str, int] = {}
    for p in safe:
        p_map[p["planet"]] = p["house"]
    house_planets: Dict[int, List[str]] = {}
    for p in safe:
        house_planets.setdefault(p["house"], []).append(p["planet"])

    results = []

    for planet, house in p_map.items():
        # 1. Sarkari
        sarkari = (planet in _SARKARI_PLANETS) and (house in _SARKARI_HOUSES)
        sarkari_detail = ""
        if sarkari:
            sarkari_detail = f"{planet} in house {house} — Government authority. Legal/tax issues if afflicted."
        # Gair-Sarkari = not sarkari but in authority house
        gair_sarkari = (planet not in _SARKARI_PLANETS) and (house in _SARKARI_HOUSES)
        gair_sarkari_detail = f"{planet} in house {house} — Private sector authority. Works independently of government." if gair_sarkari else ""

        # 2. Bhedi Grah (spy)
        spy_axis_map = {8: 2, 6: 12, 3: 9, 2: 8, 12: 6, 9: 3}
        bhedi = False
        bhedi_detail = ""
        if house in spy_axis_map:
            target_house = spy_axis_map[house]
            if target_house in house_planets:
                victims = house_planets[target_house]
                bhedi = True
                bhedi_detail = f"{planet} in house {house} spies on {', '.join(victims)} in house {target_house} — leaking their strength."

        # 3. Zakhmi Grah (wounded)
        takkar_house = ((house - 1 + 6) % 12) + 1  # 7th from current
        zakhmi = False
        zakhmi_detail = ""
        # Bidirectional: attacker considers PLANET an enemy OR planet considers attacker an enemy
        attackers = [
            p for p in house_planets.get(takkar_house, [])
            if p in LK_ENEMIES.get(planet, set()) or planet in LK_ENEMIES.get(p, set())
        ]
        if attackers:
            zakhmi = True
            zakhmi_detail = f"{planet} is wounded by {', '.join(attackers)} attacking from house {takkar_house} (Takkar). Results are permanently scarred."

        # 4. Pardesi Grah (foreigner)
        natural = _NATURAL_HOUSES.get(planet, set())
        pardesi = house not in natural and house != _PAKKA.get(planet, 0)
        pardesi_detail = f"{planet} is a foreigner in house {house} — no natural connection. Gives erratic, unpredictable results." if pardesi else ""

        status = {
            "sarkari": sarkari,
            "gair_sarkari": gair_sarkari,
            "bhedi": bhedi,
            "zakhmi": zakhmi,
            "pardesi": pardesi,
            "details": {
                k: v for k, v in {
                    "sarkari": sarkari_detail,
                    "gair_sarkari": gair_sarkari_detail,
                    "bhedi": bhedi_detail,
                    "zakhmi": zakhmi_detail,
                    "pardesi": pardesi_detail,
                }.items() if v
            }
        }

        results.append({
            "planet": planet,
            "house": house,
            "status": status,
        })

    return results


# ============================================================
# 5. MUTH-THI LOGIC
# ============================================================

def calculate_muththi(planet_positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Houses 1-6 = 'in hand' (self-made destiny)
    Houses 7-12 = 'outside hand' (ancestral karma)
    """
    safe = _safe_positions(planet_positions)
    in_hand = [p["planet"] for p in safe if 1 <= p["house"] <= 6]
    out_hand = [p["planet"] for p in safe if 7 <= p["house"] <= 12]
    score = len(in_hand)
    total = len(safe)

    if score >= 6:
        verdict_en = "Strong self-determination. Your destiny is decisively in your own hands. You are the architect of your life."
        verdict_hi = "दृढ़ स्व-निर्धारण। आपका भाग्य निर्णायक रूप से आपके अपने हाथों में है। आप अपने जीवन के निर्माता हैं।"
        archetype = "Self-Made"
        archetype_hi = "स्व-निर्मित"
    elif score >= 4:
        verdict_en = "Good self-initiative with some ancestral influence. You shape your destiny but inherited patterns play a role."
        verdict_hi = "अच्छी स्व-पहल, कुछ पैतृक प्रभाव के साथ। आप भाग्य को आकार देते हैं लेकिन विरासत में मिले पैटर्न भी भूमिका निभाते हैं।"
        archetype = "Self-Reliant"
        archetype_hi = "आत्म-निर्भर"
    elif score >= 2:
        verdict_en = "A balance between self-effort and pre-destined circumstances. Both free will and karma operate equally."
        verdict_hi = "स्व-प्रयास और पूर्व-नियत परिस्थितियों के बीच संतुलन।"
        archetype = "Balanced"
        archetype_hi = "संतुलित"
    elif score == 1:
        verdict_en = "Destiny is largely controlled by ancestral karma. External forces guide your life more than personal will."
        verdict_hi = "भाग्य अधिकतर पैतृक कर्म से नियंत्रित है।"
        archetype = "Karma-Driven"
        archetype_hi = "कर्म-संचालित"
    else:
        verdict_en = "All planets outside the hand. Destiny is entirely in the hands of ancestral karma and external forces. Remedies strongly recommended."
        verdict_hi = "सभी ग्रह हाथ के बाहर। भाग्य पूरी तरह पैतृक कर्म के हाथों में।"
        archetype = "Ancestral"
        archetype_hi = "पैतृक"

    recommendation = None
    if score < 3:
        recommendation = {
            "en": "Perform Pitru Tarpan on Amavasya. Connect with elders. Honor ancestors through service.",
            "hi": "अमावस्या पर पितृ तर्पण करें। बड़ों से जुड़ें। सेवा से पूर्वजों का सम्मान करें।"
        }

    return {
        "in_hand": in_hand,
        "out_hand": out_hand,
        "score": score,
        "total_planets": total,
        "archetype": archetype,
        "archetype_hi": archetype_hi,
        "verdict": verdict_en,
        "verdict_hi": verdict_hi,
        "recommendation": recommendation,
    }
