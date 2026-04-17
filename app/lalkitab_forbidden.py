"""
lalkitab_forbidden.py — Dynamic Forbidden Actions List
=======================================================
A comprehensive rule engine that maps (planet, house) combinations
to specific forbidden actions with reasons and consequences.
Goes beyond get_prohibitions() in lalkitab_advanced.py by including
non-charitable prohibitions (construction, pets, objects, behavior).
"""
from typing import List, Dict, Any, Tuple

# ============================================================
# FORBIDDEN RULES — (planet, house) → list of prohibitions
# ============================================================
FORBIDDEN_RULES: Dict[Tuple[str, int], List[Dict[str, str]]] = {
    # Jupiter placements
    ("Jupiter", 7): [
        {
            "action": {"en": "Donating yellow cloth or saffron to a priest/temple", "hi": "पुजारी/मंदिर को पीला वस्त्र या केसर दान करना"},
            "reason": {"en": "Jupiter in 7th is your 'merchant in his own shop' — giving away his goods weakens the partnership house.", "hi": "7वें में गुरु 'अपनी दुकान का व्यापारी' है — उसका सामान देना साझेदारी घर कमजोर करता है।"},
            "consequence": {"en": "Financial loss, marital discord, betrayal by trusted partners.", "hi": "आर्थिक हानि, वैवाहिक कलह, विश्वस्त साझेदारों द्वारा विश्वासघात।"},
            "category": "charity",
        },
        {
            "action": {"en": "Feeding turmeric/yellow sweet to others as charity", "hi": "दूसरों को हल्दी/पीली मिठाई दान के रूप में देना"},
            "reason": {"en": "Yellow items amplify Jupiter. In the 7th, this backfires — you lose Jupiter's blessings to others.", "hi": "पीली वस्तुएं गुरु को बढ़ाती हैं। 7वें में यह उल्टा पड़ता है।"},
            "consequence": {"en": "Business partners betray. Marriage faces repeated conflicts.", "hi": "व्यापार साझेदार धोखा देते हैं। विवाह बार-बार संघर्षों का सामना करता है।"},
            "category": "charity",
        }
    ],
    ("Jupiter", 10): [
        {
            "action": {"en": "Feeding others with emotional display or pity (showing off generosity)", "hi": "भावनात्मक प्रदर्शन या दया के साथ दूसरों को खाना खिलाना"},
            "reason": {"en": "Jupiter in 10th acts like poison when its charitable energy is performative — it collapses career.", "hi": "10वें में गुरु जहर की तरह काम करता है जब उसकी दानशीलता दिखावटी होती है।"},
            "consequence": {"en": "Severe professional setbacks. Position and reputation destroyed.", "hi": "गंभीर व्यावसायिक असफलताएं। पद और प्रतिष्ठा नष्ट।"},
            "category": "behavior",
        }
    ],
    # Saturn placements
    ("Saturn", 8): [
        {
            "action": {"en": "Building a house or purchasing property before age 48", "hi": "48 वर्ष की आयु से पहले घर बनाना या संपत्ति खरीदना"},
            "reason": {"en": "Saturn in 8th represents a 'house of death' under construction. Starting your own home before 48 activates this destructive energy prematurely.", "hi": "8वें में शनि निर्माणाधीन 'मृत्यु का घर' है। 48 से पहले घर बनाना इस विनाशकारी ऊर्जा को समय से पहले सक्रिय करता है।"},
            "consequence": {"en": "Serious health crisis for self or family, incomplete construction, financial ruin.", "hi": "स्वयं या परिवार के लिए गंभीर स्वास्थ्य संकट, अधूरा निर्माण, आर्थिक बर्बादी।"},
            "category": "construction",
        },
        {
            "action": {"en": "Donating iron or black sesame as a remedy without expert guidance", "hi": "विशेषज्ञ मार्गदर्शन के बिना लोहा या काले तिल उपाय के रूप में दान करना"},
            "reason": {"en": "Saturn in 8th already carries heavy karmic weight. Incorrect Saturn remedies amplify the damage.", "hi": "8वें में शनि पहले से भारी कर्मिक भार वहन करता है। गलत शनि उपाय नुकसान बढ़ाते हैं।"},
            "consequence": {"en": "Chronic illness, sudden accidents, loss of inherited assets.", "hi": "पुरानी बीमारी, अचानक दुर्घटनाएं, विरासत में मिली संपत्ति की हानि।"},
            "category": "remedies",
        }
    ],
    ("Saturn", 4): [
        {
            "action": {"en": "Donating oil or serving liquor/alcohol at home", "hi": "घर पर तेल दान करना या शराब परोसना"},
            "reason": {"en": "Saturn in 4th afflicts the Moon (home, mother). Oil and alcohol increase Saturn's heaviness on the domestic sphere.", "hi": "4वें में शनि चंद्रमा को प्रभावित करता है। तेल और शराब घरेलू क्षेत्र पर शनि का भार बढ़ाते हैं।"},
            "consequence": {"en": "Mother's health deteriorates. Property conflicts. Domestic peace destroyed.", "hi": "माता का स्वास्थ्य खराब होता है। संपत्ति विवाद। घरेलू शांति नष्ट।"},
            "category": "household",
        }
    ],
    ("Saturn", 10): [
        {
            "action": {"en": "Building a house before age 48 (career house variant)", "hi": "48 वर्ष से पहले घर बनाना (करियर घर संस्करण)"},
            "reason": {"en": "Saturn in 10th represents career edifice. Building a literal house before cementing career is disastrous.", "hi": "10वें में शनि करियर संरचना है। करियर स्थापित करने से पहले घर बनाना विनाशकारी है।"},
            "consequence": {"en": "Complete financial destruction. Career collapse follows construction.", "hi": "पूर्ण आर्थिक विनाश। निर्माण के बाद करियर का पतन।"},
            "category": "construction",
        }
    ],
    # Rahu placements
    ("Rahu", 4): [
        {
            "action": {"en": "Keeping a dog at home", "hi": "घर पर कुत्ता रखना"},
            "reason": {"en": "Rahu in 4th afflicts Moon (mother, peace of mind). A dog's barking energy further destabilizes 4th house peace.", "hi": "4वें में राहु चंद्रमा को प्रभावित करता है। कुत्ते की भौंकने की ऊर्जा 4वें घर की शांति को और अस्थिर करती है।"},
            "consequence": {"en": "Constant domestic turmoil, mother's ill-health, mental restlessness and anxiety.", "hi": "निरंतर घरेलू उथल-पुथल, माता की बीमारी, मानसिक अशांति।"},
            "category": "household",
        },
        {
            "action": {"en": "Demolishing or selling ancestral property", "hi": "पैतृक संपत्ति को तोड़ना या बेचना"},
            "reason": {"en": "Rahu in 4th already disrupts ancestral connections. Physically breaking the ancestral home activates severe consequences.", "hi": "4वें में राहु पहले से पैतृक संबंधों को बाधित करता है।"},
            "consequence": {"en": "Loss of maternal line blessings. Health crisis for mother and children.", "hi": "मातृ वंश के आशीर्वाद की हानि।"},
            "category": "property",
        }
    ],
    ("Rahu", 6): [
        {
            "action": {"en": "Donating blue or black cloth or gemstones", "hi": "नीले या काले कपड़े या रत्न दान करना"},
            "reason": {"en": "Rahu in 6th is already a spy in the enemy house. Donating its dark items empowers enemies.", "hi": "6वें में राहु पहले से शत्रु घर में जासूस है। उसकी काली वस्तुएं दान करना शत्रुओं को शक्तिशाली बनाता है।"},
            "consequence": {"en": "Legal entanglements, chronic disease, enemies multiply.", "hi": "कानूनी उलझन, पुरानी बीमारी, शत्रु बढ़ते हैं।"},
            "category": "charity",
        }
    ],
    ("Rahu", 1): [
        {
            "action": {"en": "Starting a new business on Saturday", "hi": "शनिवार को नया व्यापार शुरू करना"},
            "reason": {"en": "Rahu in 1st already brings confusion about identity. Saturn's day amplifies Rahu's shadow on new beginnings.", "hi": "लग्न में राहु पहचान के बारे में भ्रम लाता है।"},
            "consequence": {"en": "Business built on unstable foundation, identity conflicts with work.", "hi": "अस्थिर नींव पर व्यापार।"},
            "category": "timing",
        }
    ],
    # Ketu placements
    ("Ketu", 5): [
        {
            "action": {"en": "Using yellow-colored items in puja room or meditation space", "hi": "पूजा कक्ष या ध्यान स्थान में पीले रंग की वस्तुएं रखना"},
            "reason": {"en": "Ketu in 5th acts as a monk who rejects Jupiter (yellow). Activating yellow energy confronts Ketu's spiritual resistance.", "hi": "5वें में केतु एक संन्यासी की तरह कार्य करता है जो गुरु को अस्वीकार करता है।"},
            "consequence": {"en": "Issues with children (conception difficulties or health). Loss of spiritual merit.", "hi": "बच्चों के साथ समस्याएं (गर्भधारण की कठिनाइयां या स्वास्थ्य)।"},
            "category": "spiritual",
        },
        {
            "action": {"en": "Giving yellow flowers at a temple on behalf of children's health", "hi": "बच्चों के स्वास्थ्य के लिए मंदिर में पीले फूल चढ़ाना"},
            "reason": {"en": "Ketu in 5th resists Jupiter-Mercury synergy. Yellow temple offerings backfire for children's matters.", "hi": "5वें में केतु गुरु-बुध तालमेल का विरोध करता है।"},
            "consequence": {"en": "Children's issues worsen temporarily. Spiritual merit is lost.", "hi": "बच्चों की समस्याएं अस्थायी रूप से बिगड़ती हैं।"},
            "category": "spiritual",
        }
    ],
    ("Ketu", 6): [
        {
            "action": {"en": "Keeping pets (especially small animals) at home", "hi": "घर पर पालतू जानवर (विशेषकर छोटे जानवर) रखना"},
            "reason": {"en": "Ketu in 6th (Pakka Ghar) amplifies detachment from service duties. Animals in this condition face karmic sacrifice.", "hi": "6वें में केतु (पक्का घर) सेवा कर्तव्यों से वैराग्य को बढ़ाता है।"},
            "consequence": {"en": "Pets face illness or early death. Karmic burden increases.", "hi": "पालतू जानवर बीमारी या जल्दी मृत्यु का सामना करते हैं।"},
            "category": "household",
        }
    ],
    # Mars placements
    ("Mars", 8): [
        {
            "action": {"en": "Donating red cloth, copper vessels, or red items", "hi": "लाल कपड़ा, तांबे के बर्तन या लाल वस्तुएं दान करना"},
            "reason": {"en": "Mars in 8th is already in its destructive house. Donating red items adds fuel to 8th house fire.", "hi": "8वें में मंगल पहले से विनाशकारी घर में है। लाल वस्तुएं दान करना 8वें घर की आग में ईंधन डालता है।"},
            "consequence": {"en": "Accident proneness increases significantly. Blood diseases and surgical risks.", "hi": "दुर्घटना की प्रवृत्ति काफी बढ़ जाती है। रक्त रोग और शल्य जोखिम।"},
            "category": "charity",
        },
        {
            "action": {"en": "Starting construction or renovation of kitchen (fire area)", "hi": "रसोई (अग्नि क्षेत्र) का निर्माण या नवीकरण शुरू करना"},
            "reason": {"en": "Mars rules fire/kitchen. In 8th, construction related to fire zones triggers accidents.", "hi": "मंगल अग्नि/रसोई पर शासन करता है। 8वें में अग्नि क्षेत्र से संबंधित निर्माण दुर्घटनाएं ट्रिगर करता है।"},
            "consequence": {"en": "Fire accidents, injury during construction, health emergency.", "hi": "अग्नि दुर्घटनाएं, निर्माण के दौरान चोट, स्वास्थ्य आपात।"},
            "category": "construction",
        }
    ],
    # Venus placements
    ("Venus", 9): [
        {
            "action": {"en": "Financial aid to widows or donating money to poor girls", "hi": "विधवाओं को वित्तीय सहायता या गरीब लड़कियों को पैसा दान"},
            "reason": {"en": "Venus in 9th creates a conflict — while charitable, this specific action activates obstruction to children (5th house).", "hi": "9वें में शुक्र विरोधाभास बनाता है — यह क्रिया संतान में बाधा सक्रिय करती है।"},
            "consequence": {"en": "Progeny obstruction, marital conflict, difficulty having children.", "hi": "संतान प्राप्ति में बाधा, वैवाहिक कलह।"},
            "category": "charity",
        }
    ],
    # Moon placements
    ("Moon", 12): [
        {
            "action": {"en": "Donating to temples, saints, or construction of places of worship", "hi": "मंदिरों, संतों या पूजा स्थलों के निर्माण में दान"},
            "reason": {"en": "Moon in 12th already drains emotional resources through spiritual giving. Amplifying this creates mental health crisis.", "hi": "12वें में चंद्रमा पहले से आध्यात्मिक दान से भावनात्मक संसाधन खींचता है।"},
            "consequence": {"en": "Mental health crisis, poverty, anxiety disorders.", "hi": "मानसिक स्वास्थ्य संकट, गरीबी, चिंता विकार।"},
            "category": "charity",
        }
    ],
    # Mercury placements
    ("Mercury", 3): [
        {
            "action": {"en": "Giving away green items or plants as gifts", "hi": "हरी वस्तुएं या पौधे उपहार के रूप में देना"},
            "reason": {"en": "Mercury in 3rd is strong but giving green items (Mercury's color) to others weakens its power.", "hi": "3वें में बुध मजबूत है लेकिन हरी वस्तुएं (बुध का रंग) देना इसकी शक्ति कमजोर करता है।"},
            "consequence": {"en": "Sibling conflicts, communication breakdown, short travel mishaps.", "hi": "भाई-बहन विवाद, संचार टूटना।"},
            "category": "gifts",
        }
    ],
    ("Mercury", 8): [
        {
            "action": {"en": "Donating green cloth or emerald gemstone", "hi": "हरा कपड़ा या पन्ना रत्न दान करना"},
            "reason": {"en": "Mercury in 8th is already in a hidden, deep house. Giving away its color items removes Mercury's protective shield.", "hi": "8वें में बुध पहले से छिपे, गहरे घर में है। उसके रंग की वस्तुएं देना सुरक्षा कवच हटाता है।"},
            "consequence": {"en": "Travel accidents, speech problems, trade betrayals.", "hi": "यात्रा दुर्घटनाएं, वाणी समस्याएं, व्यापारिक विश्वासघात।"},
            "category": "charity",
        }
    ],
    # Sun placements
    ("Sun", 7): [
        {
            "action": {"en": "Making specific morning or evening donations (timed charity)", "hi": "विशिष्ट सुबह या शाम का दान (समयबद्ध दान)"},
            "reason": {"en": "Sun in 7th loses its timing-based strength. Donations at sunrise/sunset amplify the weakness.", "hi": "7वें में सूर्य अपनी समय-आधारित शक्ति खो देता है।"},
            "consequence": {"en": "Authority loss, partnership conflicts, health issues for spouse.", "hi": "अधिकार हानि, साझेदारी संघर्ष, जीवनसाथी के स्वास्थ्य मुद्दे।"},
            "category": "timing",
        }
    ],
}


def get_forbidden_remedies(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Returns forbidden actions specific to this chart's planet placements.

    planet_positions: [{"planet": "Jupiter", "house": 7}, ...]
    """
    p_map = {p["planet"]: p["house"] for p in planet_positions}
    results = []

    for planet, house in p_map.items():
        key = (planet, house)
        if key in FORBIDDEN_RULES:
            for rule in FORBIDDEN_RULES[key]:
                results.append({
                    "planet": planet,
                    "house": house,
                    "action": rule["action"],
                    "reason": rule["reason"],
                    "consequence": rule["consequence"],
                    "category": rule.get("category", "general"),
                })

    # Sort by severity: construction > charity > household > spiritual > others
    category_order = {"construction": 0, "charity": 1, "household": 2, "spiritual": 3, "property": 4, "remedies": 5, "behavior": 6, "timing": 7, "gifts": 8, "general": 9}
    results.sort(key=lambda r: category_order.get(r["category"], 99))

    return results
