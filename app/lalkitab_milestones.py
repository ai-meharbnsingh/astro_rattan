"""
lalkitab_milestones.py — Safar-e-Zindagi (Age Milestone Triggers)
==================================================================
Lal Kitab defines specific trigger ages where a ruling planet's quality
determines major life events. These are fixed regardless of Varshphal.
"""
from typing import List, Dict, Any, Optional
from datetime import date

# ============================================================
# AGE MILESTONES — Lal Kitab fixed trigger ages
# ============================================================
LK_MILESTONES: List[Dict[str, Any]] = [
    {
        "age": 8,  "theme": "health",    "ruler": "Saturn",
        "theme_en": "Health Foundation",     "theme_hi": "स्वास्थ्य की नींव",
        "icon": "🏥",
        "description": {
            "en": "Saturn tests the physical constitution at age 8. The strength of Saturn in your chart determines your childhood health resilience.",
            "hi": "शनि 8 वर्ष की आयु में शारीरिक संरचना की परीक्षा लेता है। आपकी कुंडली में शनि की शक्ति बचपन के स्वास्थ्य की लचीलापन निर्धारित करती है।"
        }
    },
    {
        "age": 16, "theme": "education", "ruler": "Mercury",
        "theme_en": "Education & Intellect",  "theme_hi": "शिक्षा और बुद्धि",
        "icon": "📚",
        "description": {
            "en": "Mercury governs the 16th year. Its house placement reveals the nature of education — whether academic excellence or practical learning.",
            "hi": "बुध 16वें वर्ष को नियंत्रित करता है। इसकी घर स्थिति शिक्षा की प्रकृति प्रकट करती है।"
        }
    },
    {
        "age": 22, "theme": "career",    "ruler": "Venus",
        "theme_en": "Career Begins",          "theme_hi": "करियर की शुरुआत",
        "icon": "💼",
        "description": {
            "en": "Venus awakens the 22nd year — the start of professional life. A strong Venus brings charm and opportunities; weak Venus means delays.",
            "hi": "शुक्र 22वें वर्ष को जगाता है — व्यावसायिक जीवन की शुरुआत। मजबूत शुक्र आकर्षण और अवसर लाता है।"
        }
    },
    {
        "age": 24, "theme": "marriage",  "ruler": "Mars",
        "theme_en": "Marriage & Partnership",  "theme_hi": "विवाह और साझेदारी",
        "icon": "💍",
        "description": {
            "en": "Mars triggers the marriage age at 24. Position of Mars determines passion vs. conflict in partnerships.",
            "hi": "मंगल 24 वर्ष में विवाह की आयु को ट्रिगर करता है। मंगल की स्थिति साझेदारी में जुनून बनाम संघर्ष निर्धारित करती है।"
        }
    },
    {
        "age": 28, "theme": "fortune",   "ruler": "Sun",
        "theme_en": "Fortune & Recognition",   "theme_hi": "भाग्य और पहचान",
        "icon": "☀️",
        "description": {
            "en": "The Sun activates fortune and social recognition at age 28. A strong Sun here means career peaks; weak Sun means father's shadow over progress.",
            "hi": "सूर्य 28 वर्ष में भाग्य और सामाजिक पहचान को सक्रिय करता है।"
        }
    },
    {
        "age": 36, "theme": "shift",     "ruler": "Jupiter",
        "theme_en": "Major Life Shift",        "theme_hi": "जीवन का बड़ा मोड़",
        "icon": "🔄",
        "description": {
            "en": "Jupiter brings the most significant life transformation at 36. A pivotal decision made here sets the course for the next 12 years.",
            "hi": "गुरु 36 वर्ष में सबसे महत्वपूर्ण जीवन परिवर्तन लाता है। यहां लिया गया निर्णय अगले 12 वर्षों की दिशा तय करता है।"
        }
    },
    {
        "age": 42, "theme": "wealth",    "ruler": "Moon",
        "theme_en": "Wealth & Stability",     "theme_hi": "धन और स्थिरता",
        "icon": "💰",
        "description": {
            "en": "Moon governs the 42nd year — the age of emotional and financial maturity. Accumulated wealth either multiplies or erodes based on Moon's dignity.",
            "hi": "चंद्रमा 42वें वर्ष को नियंत्रित करता है — भावनात्मक और आर्थिक परिपक्वता की आयु।"
        }
    },
    {
        "age": 48, "theme": "property",  "ruler": "Saturn",
        "theme_en": "Property & Legacy",      "theme_hi": "संपत्ति और विरासत",
        "icon": "🏠",
        "description": {
            "en": "Saturn returns at 48 for property and legacy decisions. Building a house before this age is prohibited if Saturn is in the 8th or 10th house.",
            "hi": "शनि 48 वर्ष में संपत्ति और विरासत के निर्णयों के लिए लौटता है।"
        }
    },
]

# Planet-house prediction bank (simplified LK rules)
_PLANET_HOUSE_PREDICTION: Dict[str, Dict[int, Dict[str, str]]] = {
    "Saturn": {
        1:  {"en": "Strong health foundation. Saturn in 1st protects the body robustly.", "hi": "मजबूत स्वास्थ्य नींव। लग्न में शनि शरीर की मजबूत रक्षा करता है।"},
        2:  {"en": "Delayed wealth but solid savings. Health improves with age.", "hi": "विलंबित धन लेकिन ठोस बचत। उम्र के साथ स्वास्थ्य में सुधार।"},
        3:  {"en": "Siblings may cause health challenges. Respiratory issues possible.", "hi": "भाई-बहन स्वास्थ्य चुनौतियां दे सकते हैं।"},
        4:  {"en": "Mother's health or home environment creates stress. Resolve domestic issues.", "hi": "माता का स्वास्थ्य या घर का माहौल तनाव देता है।"},
        5:  {"en": "Stress from children or past-life karma affects health. Spiritual practices help.", "hi": "बच्चों या पूर्वजन्म कर्म से तनाव स्वास्थ्य प्रभावित करता है।"},
        6:  {"en": "Health improves dramatically after battles with illness. Chronic issues eventually resolved.", "hi": "बीमारी से लड़ाई के बाद स्वास्थ्य में नाटकीय सुधार।"},
        7:  {"en": "Partnership with a practical, older or serious person. Delayed but stable marriage.", "hi": "व्यावहारिक, वृद्ध या गंभीर व्यक्ति के साथ साझेदारी।"},
        8:  {"en": "Major karmic health event. Chronic or serious condition may emerge. Build immunity.", "hi": "प्रमुख कर्मिक स्वास्थ्य घटना। प्रतिरोधक क्षमता बनाएं।"},
        9:  {"en": "Father's health or pilgrimage-related expenses. Delayed fortune through discipline.", "hi": "पिता का स्वास्थ्य या तीर्थ संबंधी खर्च।"},
        10: {"en": "Career success in government/authority roles but demands patience.", "hi": "सरकारी/प्राधिकरण भूमिकाओं में करियर सफलता लेकिन धैर्य की आवश्यकता।"},
        11: {"en": "Financial gains come from disciplined effort. Long-term savings pay off.", "hi": "अनुशासित प्रयास से वित्तीय लाभ। दीर्घकालिक बचत का फल मिलता है।"},
        12: {"en": "Hidden spiritual transformation. Losses lead to liberation if accepted.", "hi": "छिपा आध्यात्मिक परिवर्तन। यदि स्वीकार किया जाए तो हानि मुक्ति की ओर।"},
    },
    "Mercury": {
        1:  {"en": "Brilliant communicator. Education comes naturally. Excel in languages and commerce.", "hi": "प्रतिभाशाली संचारक। शिक्षा स्वाभाविक रूप से आती है।"},
        2:  {"en": "Wealth through writing, teaching, or business. Financial intelligence is high.", "hi": "लेखन, शिक्षण या व्यापार से धन। वित्तीय बुद्धि उच्च है।"},
        3:  {"en": "Brilliant in short-distance travel and communication. Siblings support education.", "hi": "छोटी यात्राओं और संचार में प्रतिभाशाली।"},
        4:  {"en": "Educated family environment. Mother is intellectually influential.", "hi": "शिक्षित पारिवारिक माहौल। माता बौद्धिक रूप से प्रभावशाली।"},
        5:  {"en": "Creative intelligence. Good at mathematics, arts, and speculation.", "hi": "रचनात्मक बुद्धि। गणित, कला और अनुमान में अच्छे।"},
        6:  {"en": "Challenges in learning due to nervous system issues. Practical skills over academics.", "hi": "तंत्रिका तंत्र समस्याओं से सीखने में चुनौतियां।"},
        7:  {"en": "Business partnerships and contractual agreements. Mercury here is in Pakka Ghar — stable wealth.", "hi": "व्यावसायिक साझेदारी और अनुबंध समझौते।"},
        8:  {"en": "Hidden knowledge and research abilities. Occult or investigative studies favored.", "hi": "छिपा ज्ञान और शोध क्षमताएं।"},
        9:  {"en": "Philosophy and higher studies bring recognition. Long-distance travel for education.", "hi": "दर्शन और उच्च अध्ययन से पहचान।"},
        10: {"en": "Career in media, technology, or communication. Public speech is powerful.", "hi": "मीडिया, तकनीक या संचार में करियर।"},
        11: {"en": "Financial gains through networks and communication. Social intelligence = income.", "hi": "नेटवर्क और संचार से वित्तीय लाभ।"},
        12: {"en": "Secret knowledge. Spiritual texts and hidden wisdom are your strength.", "hi": "गुप्त ज्ञान। आध्यात्मिक ग्रंथ आपकी शक्ति हैं।"},
    },
    "Venus": {
        1:  {"en": "Charming personality. Career starts with creative or artistic opportunities.", "hi": "आकर्षक व्यक्तित्व। करियर रचनात्मक अवसरों से शुरू होता है।"},
        2:  {"en": "Wealth through beauty industry, arts, or family business. Early earnings.", "hi": "सौंदर्य उद्योग, कला या पारिवारिक व्यापार से धन।"},
        3:  {"en": "Siblings in creative fields. Short artistic projects bring recognition.", "hi": "रचनात्मक क्षेत्रों में भाई-बहन।"},
        4:  {"en": "Beautiful home. Supportive mother. Real estate brings wealth.", "hi": "सुंदर घर। सहायक माता। रियल एस्टेट से धन।"},
        5:  {"en": "Romance leads to career. Creative intelligence = financial growth.", "hi": "रोमांस करियर की ओर ले जाता है।"},
        6:  {"en": "Career delays due to health or relationship conflicts. Service industry works well.", "hi": "स्वास्थ्य या संबंध संघर्षों के कारण करियर में विलंब।"},
        7:  {"en": "Marriage brings career opportunities. Venus in 7th = Pakka Ghar. Stable partnership.", "hi": "विवाह करियर के अवसर लाता है। साझेदारी स्थिर।"},
        8:  {"en": "Wealth through inheritance or partner's resources. Secretive in love.", "hi": "विरासत या साथी के संसाधनों से धन।"},
        9:  {"en": "Career in spiritual or educational fields. Foreign lands bring prosperity.", "hi": "आध्यात्मिक या शैक्षिक क्षेत्रों में करियर।"},
        10: {"en": "Successful career in arts, beauty, fashion or diplomacy. Public recognition.", "hi": "कला, सौंदर्य, फैशन या कूटनीति में सफल करियर।"},
        11: {"en": "Profits from artistic networks. Friends bring career and romantic opportunities.", "hi": "कलात्मक नेटवर्क से लाभ।"},
        12: {"en": "Private romantic life. Hidden artistic talents. Foreign travel for career.", "hi": "निजी रोमांटिक जीवन। विदेश यात्रा करियर के लिए।"},
    },
    "Mars": {
        1:  {"en": "Passionate and direct in relationships. Marriage partner is energetic, independent.", "hi": "रिश्तों में जोशीला और सीधा। विवाह साथी ऊर्जावान, स्वतंत्र।"},
        2:  {"en": "Financial conflicts in marriage. Money management needs attention.", "hi": "विवाह में वित्तीय संघर्ष। धन प्रबंधन पर ध्यान।"},
        3:  {"en": "Siblings and friends support marriage. Courage brings relationship success.", "hi": "भाई-बहन और मित्र विवाह में सहयोग देते हैं।"},
        4:  {"en": "Domestic conflicts. Mars in 4th creates tension at home. Choose partner carefully.", "hi": "घरेलू संघर्ष। 4वें घर में मंगल घर पर तनाव देता है।"},
        5:  {"en": "Passionate romance. Love affairs before marriage. Children bring fulfillment.", "hi": "जोशीला रोमांस। विवाह से पहले प्रेम संबंध।"},
        6:  {"en": "Delays in marriage due to legal or health issues. Eventual victory in conflicts.", "hi": "कानूनी या स्वास्थ्य समस्याओं के कारण विवाह में विलंब।"},
        7:  {"en": "Mars aspects 1st house from 7th. Manglik energy strong. Choose wisely.", "hi": "मंगल 7वें से लग्न पर दृष्टि। मांगलिक ऊर्जा मजबूत।"},
        8:  {"en": "Intense, transformative partnership. Hidden conflicts in marriage. Need for transparency.", "hi": "तीव्र, परिवर्तनकारी साझेदारी।"},
        9:  {"en": "Foreign marriage possible. Partner from different religion or culture.", "hi": "विदेश में विवाह संभव। अलग धर्म या संस्कृति का साथी।"},
        10: {"en": "Marriage to a career-oriented person. Professional life improves after marriage.", "hi": "करियर-उन्मुख व्यक्ति से विवाह।"},
        11: {"en": "Marriage through social circles. Partner brings financial prosperity.", "hi": "सामाजिक मंडलियों से विवाह।"},
        12: {"en": "Hidden relationship or delayed marriage. Secret affairs possible. Need for clarity.", "hi": "छिपा संबंध या विलंबित विवाह।"},
    },
    "Sun": {
        1:  {"en": "Natural leader. Fortune through government or authority. Father is supportive.", "hi": "स्वाभाविक नेता। सरकार या प्राधिकरण से भाग्य।"},
        2:  {"en": "Fortune through family business or inherited wealth. Speech = authority.", "hi": "पारिवारिक व्यापार या विरासत से भाग्य।"},
        3:  {"en": "Fortune through communication, short trips, and sibling support.", "hi": "संचार, छोटी यात्राओं और भाई-बहन के सहयोग से भाग्य।"},
        4:  {"en": "Real estate and ancestral property bring fortune. Mother's blessings are pivotal.", "hi": "रियल एस्टेट और पैतृक संपत्ति से भाग्य।"},
        5:  {"en": "Speculation and creative ventures bring fortune. Children are lucky symbols.", "hi": "अटकलें और रचनात्मक उद्यम भाग्य लाते हैं।"},
        6:  {"en": "Fortune through service, legal victory, and defeating enemies.", "hi": "सेवा, कानूनी विजय और शत्रुओं को हराने से भाग्य।"},
        7:  {"en": "Fortune through partnerships. But Sun in 7th weakens partner's health. Balance needed.", "hi": "साझेदारी से भाग्य। लेकिन 7वें में सूर्य साथी का स्वास्थ्य कमजोर करता है।"},
        8:  {"en": "Fortune hidden in transformative events. Inheritance and legacy wealth.", "hi": "परिवर्तनकारी घटनाओं में छिपा भाग्य।"},
        9:  {"en": "Fortune through father's blessings and religious acts. Higher studies pay off.", "hi": "पिता के आशीर्वाद और धार्मिक कार्यों से भाग्य।"},
        10: {"en": "Exceptional career fortune. Government jobs, leadership roles, and public recognition.", "hi": "असाधारण करियर भाग्य।"},
        11: {"en": "Fortune through networks and government connections. Senior friends help.", "hi": "नेटवर्क और सरकारी संपर्कों से भाग्य।"},
        12: {"en": "Fortune through foreign lands or spiritual service. Hidden benefactors.", "hi": "विदेश या आध्यात्मिक सेवा से भाग्य।"},
    },
    "Jupiter": {
        1:  {"en": "Jupiter in 1st brings wisdom-led transformation at 36. Philosophical life shift.", "hi": "लग्न में गुरु 36 वर्ष में बुद्धि-नेतृत्व परिवर्तन लाता है।"},
        2:  {"en": "Wealth expansion at 36. Jupiter in Pakka Ghar amplifies family prosperity.", "hi": "36 वर्ष में धन विस्तार। पक्के घर में गुरु पारिवारिक समृद्धि बढ़ाता है।"},
        3:  {"en": "Major shift in communication, writing, or sibling relationships at 36.", "hi": "36 वर्ष में संचार, लेखन या भाई-बहन संबंधों में बड़ा बदलाव।"},
        4:  {"en": "Major property acquisition or home change at 36. Mother's health pivotal.", "hi": "36 वर्ष में संपत्ति अधिग्रहण या घर बदलाव।"},
        5:  {"en": "Creative breakthrough at 36. Children, arts, or romance triggers life shift.", "hi": "36 वर्ष में रचनात्मक सफलता।"},
        6:  {"en": "Health transformation at 36. Jupiter in 6th tests faith through illness.", "hi": "36 वर्ष में स्वास्थ्य परिवर्तन।"},
        7:  {"en": "Major relationship shift at 36 — marriage, divorce, or business pivot.", "hi": "36 वर्ष में प्रमुख संबंध बदलाव।"},
        8:  {"en": "Spiritual transformation at 36. Occult research or inheritance changes life.", "hi": "36 वर्ष में आध्यात्मिक परिवर्तन।"},
        9:  {"en": "Guru appears at 36. Higher learning, pilgrimage, or foreign opportunity.", "hi": "36 वर्ष में गुरु प्रकट होते हैं।"},
        10: {"en": "Career peak at 36. Leadership role or business expansion defines this year.", "hi": "36 वर्ष में करियर शिखर।"},
        11: {"en": "Major financial network expansion at 36. Social circle changes significantly.", "hi": "36 वर्ष में प्रमुख वित्तीय नेटवर्क विस्तार।"},
        12: {"en": "Spiritual retreat or foreign move at 36. Letting go of material attachments.", "hi": "36 वर्ष में आध्यात्मिक एकांत या विदेश।"},
    },
    "Moon": {
        1:  {"en": "Emotional wealth accumulation at 42. Public appeal brings financial stability.", "hi": "42 वर्ष में भावनात्मक धन संचय।"},
        2:  {"en": "Family wealth multiplies at 42. Moon in 2nd = speech brings money.", "hi": "42 वर्ष में पारिवारिक धन बढ़ता है।"},
        3:  {"en": "Creative writing or media work pays off financially at 42.", "hi": "42 वर्ष में रचनात्मक लेखन या मीडिया काम वित्तीय रूप से फलता है।"},
        4:  {"en": "Moon in Pakka Ghar. Property and emotional security peak at 42.", "hi": "चंद्रमा पक्के घर में। 42 वर्ष में संपत्ति और भावनात्मक सुरक्षा।"},
        5:  {"en": "Investment profits at 42. Children bring financial opportunities.", "hi": "42 वर्ष में निवेश लाभ।"},
        6:  {"en": "Health expenses eat wealth at 42. Avoid unnecessary risks.", "hi": "42 वर्ष में स्वास्थ्य खर्च धन खाता है।"},
        7:  {"en": "Partner's income or business partnerships stabilize wealth at 42.", "hi": "42 वर्ष में साथी की आय या व्यापार साझेदारी धन स्थिर करती है।"},
        8:  {"en": "Inheritance or occult-related income at 42. Secret wealth revealed.", "hi": "42 वर्ष में विरासत या गुप्त आय।"},
        9:  {"en": "Religious or educational investments pay off financially at 42.", "hi": "42 वर्ष में धार्मिक या शैक्षिक निवेश फलते हैं।"},
        10: {"en": "Career and business income peaks at 42. Authority = prosperity.", "hi": "42 वर्ष में करियर और व्यापार आय।"},
        11: {"en": "Network income and passive streams grow at 42.", "hi": "42 वर्ष में नेटवर्क आय बढ़ती है।"},
        12: {"en": "Hidden income from foreign or spiritual sources at 42.", "hi": "42 वर्ष में विदेश या आध्यात्मिक स्रोतों से आय।"},
    },
}

# Remedy map per planet
_MILESTONE_REMEDIES: Dict[str, Dict[str, str]] = {
    "Saturn": {"en": "Feed black sesame to crows every Saturday for 43 days.", "hi": "43 दिन प्रत्येक शनिवार कौओं को काले तिल खिलाएं।"},
    "Mercury": {"en": "Plant a green plant and water it daily. Study for minimum 1 hour daily.", "hi": "हरा पौधा लगाएं और प्रतिदिन पानी दें। प्रतिदिन न्यूनतम 1 घंटा अध्ययन करें।"},
    "Venus":   {"en": "Donate white sweets on Friday. Keep your partner's photo near you.", "hi": "शुक्रवार को सफेद मिठाई दान करें।"},
    "Mars":    {"en": "Recite Hanuman Chalisa on Tuesdays. Donate red lentils.", "hi": "मंगलवार को हनुमान चालीसा पढ़ें। लाल दाल दान करें।"},
    "Sun":     {"en": "Offer water to Sun at sunrise for 41 days. Serve your father.", "hi": "41 दिन सूर्योदय पर जल अर्पित करें। पिता की सेवा करें।"},
    "Jupiter": {"en": "Feed cows yellow items on Thursdays. Respect your Guru.", "hi": "गुरुवार को गायों को पीली वस्तुएं खिलाएं। गुरु का सम्मान करें।"},
    "Moon":    {"en": "Offer milk to Shiva on Mondays. Keep silver with you.", "hi": "सोमवार को शिव को दूध अर्पित करें। चांदी साथ रखें।"},
}


def calculate_age_milestones(
    birth_date: str,
    planet_positions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    birth_date: "YYYY-MM-DD"
    planet_positions: [{"planet": "Saturn", "house": 8}, ...]
    """
    from app.lalkitab_advanced import PAKKA_GHAR

    today = date.today()
    try:
        bdate = date.fromisoformat(birth_date)
    except Exception:
        bdate = today.replace(year=today.year - 30)

    # Current age in years
    current_age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))

    p_map = {p["planet"]: p["house"] for p in planet_positions}

    milestone_list = []
    next_milestone = None

    for m in LK_MILESTONES:
        ruler = m["ruler"]
        ruler_house = p_map.get(ruler, 0)
        pakka = PAKKA_GHAR.get(ruler, 0)
        is_past = current_age > m["age"]
        is_next_flag = (not next_milestone) and (current_age <= m["age"])

        # Determine ruler status
        if ruler_house == pakka:
            ruler_status = "strong"
        elif ruler_house in {6, 8, 12}:
            ruler_status = "weak"
        else:
            ruler_status = "moderate"

        # Prediction
        planet_preds = _PLANET_HOUSE_PREDICTION.get(ruler, {})
        pred = planet_preds.get(ruler_house, {
            "en": f"{ruler} in house {ruler_house} influences this milestone.",
            "hi": f"घर {ruler_house} में {ruler} इस मील के पत्थर को प्रभावित करता है।"
        })

        # Remedy needed if upcoming and weak
        remedy_needed = (not is_past) and (ruler_status == "weak") and (m["age"] - current_age <= 6)
        remedy = _MILESTONE_REMEDIES.get(ruler) if remedy_needed else None

        # Countdown for next
        countdown = None
        if is_next_flag:
            trigger_year = bdate.year + m["age"]
            trigger_date = bdate.replace(year=trigger_year)
            delta = trigger_date - today
            if delta.days > 0:
                countdown = {
                    "years": delta.days // 365,
                    "months": (delta.days % 365) // 30,
                    "days": (delta.days % 365) % 30,
                    "total_days": delta.days,
                }
            else:
                countdown = {"years": 0, "months": 0, "days": 0, "total_days": 0}

        entry = {
            "age": m["age"],
            "theme": m["theme"],
            "theme_en": m["theme_en"],
            "theme_hi": m["theme_hi"],
            "icon": m["icon"],
            "ruler": ruler,
            "ruler_house": ruler_house,
            "ruler_status": ruler_status,
            "description_en": m["description"]["en"],
            "description_hi": m["description"]["hi"],
            "prediction_en": pred["en"],
            "prediction_hi": pred["hi"],
            "remedy_needed": remedy_needed,
            "remedy": remedy,
            "is_past": is_past,
            "is_current": current_age == m["age"],
            "is_next": is_next_flag,
        }
        if is_next_flag and countdown:
            entry["countdown"] = countdown
            next_milestone = entry

        milestone_list.append(entry)

    if not next_milestone and milestone_list:
        next_milestone = milestone_list[-1]  # all past — show last

    return {
        "current_age": current_age,
        "birth_date": birth_date,
        "next_milestone": next_milestone,
        "milestones": milestone_list,
    }
