"""
numerology_engine.py — Vedic Numerology Engine
================================================
Pythagorean numerology: Life Path, Expression, Soul Urge, Personality numbers.
Reduces to single digit (1-9) or master numbers (11, 22, 33).
"""

# Pythagorean number mapping: A=1, B=2, ... I=9, J=1, K=2, ...
PYTHAGOREAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8,
}

# Chaldean mapping (alternative system used for names)
CHALDEAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7,
}

VOWELS = set('AEIOU')
MASTER_NUMBERS = {11, 22, 33}

# Life path prediction templates keyed by number
LIFE_PATH_PREDICTIONS = {
    1: {
        "theme": "The Pioneer",
        "theme_hi": "अग्रदूत",
        "description": "Natural leader with pioneering spirit. Independent, ambitious, and driven to forge new paths. This period favors bold initiatives and self-reliance.",
        "description_hi": "प्राकृतिक नेता और अग्रदूत। स्वतंत्र, महत्वाकांक्षी और नए रास्ते बनाने के लिए प्रेरित। यह समय साहसी पहल और आत्मनिर्भरता का पक्षधर है।",
        "focus_areas": "Leadership, entrepreneurship, innovation, self-development, new ventures",
        "focus_areas_hi": "नेतृत्व, उद्यमिता, नवाचार, आत्म-विकास, नई शुरुआत",
        "advice": "Trust your instincts and act decisively. Avoid stubbornness — great leaders also listen.",
        "advice_hi": "अपनी सहज बुद्धि पर भरोसा करें और निर्णायक रूप से कार्य करें। जिद से बचें — महान नेता सुनते भी हैं।",
        "lucky_months": [1, 4, 7, 10],
    },
    2: {
        "theme": "The Peacemaker",
        "theme_hi": "शांतिदूत",
        "description": "Diplomat and peacemaker. Cooperation, sensitivity, and partnerships define your journey. Seek harmony in relationships and trust your intuition.",
        "description_hi": "कूटनीतिज्ञ और शांतिदूत। सहयोग, संवेदनशीलता और साझेदारी आपकी यात्रा को परिभाषित करती है। रिश्तों में सामंजस्य खोजें और अंतर्ज्ञान पर भरोसा करें।",
        "focus_areas": "Partnerships, diplomacy, counseling, music, healing, mediation",
        "focus_areas_hi": "साझेदारी, कूटनीति, परामर्श, संगीत, उपचार, मध्यस्थता",
        "advice": "Your sensitivity is a gift, not a weakness. Speak up for yourself while maintaining harmony.",
        "advice_hi": "आपकी संवेदनशीलता एक उपहार है, कमज़ोरी नहीं। सामंजस्य बनाए रखते हुए खुद के लिए बोलें।",
        "lucky_months": [2, 6, 11],
    },
    3: {
        "theme": "The Creative Communicator",
        "theme_hi": "रचनात्मक संचारक",
        "description": "Creative expression and joyful communication. Artistic talents blossom. Social connections and optimism bring abundance.",
        "description_hi": "रचनात्मक अभिव्यक्ति और आनंदमय संवाद। कलात्मक प्रतिभाएं खिलती हैं। सामाजिक संबंध और आशावाद समृद्धि लाते हैं।",
        "focus_areas": "Writing, art, performance, social media, teaching, public speaking, entertainment",
        "focus_areas_hi": "लेखन, कला, प्रदर्शन, शिक्षण, सार्वजनिक भाषण, मनोरंजन",
        "advice": "Focus your creative gifts — scatter your energy and nothing gets completed. Depth matters.",
        "advice_hi": "अपनी रचनात्मक शक्ति को केंद्रित करें — ऊर्जा बिखेरने से कुछ पूरा नहीं होता। गहराई मायने रखती है।",
        "lucky_months": [3, 6, 9, 12],
    },
    4: {
        "theme": "The Builder",
        "theme_hi": "निर्माता",
        "description": "Builder and organizer. Stability, discipline, and hard work create lasting foundations. Patience and systematic effort lead to mastery.",
        "description_hi": "निर्माता और संयोजक। स्थिरता, अनुशासन और कठिन परिश्रम स्थायी नींव बनाते हैं। धैर्य और व्यवस्थित प्रयास महारत की ओर ले जाते हैं।",
        "focus_areas": "Construction, engineering, management, finance, systems, law, real estate",
        "focus_areas_hi": "निर्माण, इंजीनियरिंग, प्रबंधन, वित्त, प्रणाली, कानून, अचल संपत्ति",
        "advice": "Embrace structure without becoming rigid. Rest is not laziness — it is part of building.",
        "advice_hi": "कठोर हुए बिना संरचना अपनाएं। आराम आलस्य नहीं है — यह निर्माण का हिस्सा है।",
        "lucky_months": [4, 8, 1],
    },
    5: {
        "theme": "The Freedom Seeker",
        "theme_hi": "स्वतंत्रता खोजी",
        "description": "Freedom seeker and adventurer. Change, travel, and versatility are your allies. Embrace new experiences while maintaining inner balance.",
        "description_hi": "स्वतंत्रता खोजी और साहसी। परिवर्तन, यात्रा और बहुमुखी प्रतिभा आपके साथी हैं। आंतरिक संतुलन बनाए रखते हुए नए अनुभवों को अपनाएं।",
        "focus_areas": "Travel, sales, media, adventure, technology, communication, marketing",
        "focus_areas_hi": "यात्रा, बिक्री, मीडिया, साहसिक कार्य, प्रौद्योगिकी, संचार, विपणन",
        "advice": "Freedom is earned through commitment, not avoided through escape. Choose one path and go deep.",
        "advice_hi": "स्वतंत्रता प्रतिबद्धता से अर्जित होती है, पलायन से नहीं। एक राह चुनें और गहराई से जाएं।",
        "lucky_months": [5, 7, 11],
    },
    6: {
        "theme": "The Nurturer",
        "theme_hi": "पालनकर्ता",
        "description": "Nurturer and healer. Responsibility to family and community. Love, beauty, and domestic harmony are your life themes.",
        "description_hi": "पालनकर्ता और उपचारक। परिवार और समुदाय के प्रति जिम्मेदारी। प्रेम, सौंदर्य और घरेलू सामंजस्य आपके जीवन के विषय हैं।",
        "focus_areas": "Family, healing, teaching, counseling, art, home, community service, medicine",
        "focus_areas_hi": "परिवार, उपचार, शिक्षण, परामर्श, कला, घर, सामुदायिक सेवा, चिकित्सा",
        "advice": "Give generously but set boundaries — martyrdom does not serve those you love.",
        "advice_hi": "उदारता से दें लेकिन सीमाएं निर्धारित करें — आत्म-बलिदान उन्हें नहीं जो आप प्यार करते हैं।",
        "lucky_months": [6, 3, 9],
    },
    7: {
        "theme": "The Seeker of Truth",
        "theme_hi": "सत्य के खोजी",
        "description": "Spiritual seeker and analyst. Inner wisdom, contemplation, and research. Solitude and study unlock deeper truths.",
        "description_hi": "आध्यात्मिक खोजी और विश्लेषक। आंतरिक ज्ञान, चिंतन और अनुसंधान। एकांत और अध्ययन गहरे सत्य को उजागर करते हैं।",
        "focus_areas": "Research, science, philosophy, spirituality, writing, analysis, psychology, astrology",
        "focus_areas_hi": "अनुसंधान, विज्ञान, दर्शन, आध्यात्मिकता, लेखन, विश्लेषण, मनोविज्ञान, ज्योतिष",
        "advice": "Share your wisdom — isolation protects you but also hides your greatest gift from the world.",
        "advice_hi": "अपना ज्ञान साझा करें — एकांत आपकी रक्षा करता है लेकिन दुनिया से आपका सबसे बड़ा उपहार भी छुपाता है।",
        "lucky_months": [7, 2, 11],
    },
    8: {
        "theme": "The Material Master",
        "theme_hi": "भौतिक स्वामी",
        "description": "Material mastery and karmic balance. Business acumen and authority. Power must be wielded with integrity for lasting success.",
        "description_hi": "भौतिक निपुणता और कर्म संतुलन। व्यावसायिक कुशाग्रता और अधिकार। स्थायी सफलता के लिए शक्ति को ईमानदारी से उपयोग करना होगा।",
        "focus_areas": "Business, finance, real estate, law, politics, corporate leadership, banking",
        "focus_areas_hi": "व्यापार, वित्त, अचल संपत्ति, कानून, राजनीति, कॉर्पोरेट नेतृत्व, बैंकिंग",
        "advice": "Integrity is your greatest asset. Wealth gained through shortcuts invites karmic loss.",
        "advice_hi": "ईमानदारी आपकी सबसे बड़ी संपत्ति है। शॉर्टकट से अर्जित धन कर्म की हानि आमंत्रित करता है।",
        "lucky_months": [8, 4, 1],
    },
    9: {
        "theme": "The Humanitarian",
        "theme_hi": "मानवतावादी",
        "description": "Humanitarian and universal lover. Compassion, generosity, and completion. Service to others fulfills your highest purpose.",
        "description_hi": "मानवतावादी और सार्वभौमिक प्रेमी। करुणा, उदारता और समापन। दूसरों की सेवा आपका सर्वोच्च उद्देश्य पूरा करती है।",
        "focus_areas": "Philanthropy, teaching, healing, arts, spirituality, social work, global causes",
        "focus_areas_hi": "परोपकार, शिक्षण, उपचार, कला, आध्यात्मिकता, सामाजिक कार्य, वैश्विक उद्देश्य",
        "advice": "Release attachment to outcomes. Give without expectation. Forgiveness is your superpower.",
        "advice_hi": "परिणामों से आसक्ति छोड़ें। बिना अपेक्षा के दें। क्षमा आपकी महाशक्ति है।",
        "lucky_months": [3, 6, 9, 12],
    },
    11: {
        "theme": "The Master Intuitive",
        "theme_hi": "मास्टर अंतर्ज्ञानी",
        "description": "Master Intuitive. Heightened spiritual awareness and visionary insight. Channel inspiration into tangible form. Avoid nervous tension.",
        "description_hi": "मास्टर अंतर्ज्ञानी। उच्च आध्यात्मिक जागरूकता और दूरदर्शी अंतर्दृष्टि। प्रेरणा को ठोस रूप में प्रकट करें। तंत्रिका तनाव से बचें।",
        "focus_areas": "Spiritual leadership, counseling, art, healing, innovation, teaching, inspiration",
        "focus_areas_hi": "आध्यात्मिक नेतृत्व, परामर्श, कला, उपचार, नवाचार, शिक्षण, प्रेरणा",
        "advice": "Ground your visions in daily practice. Your light is needed — don't dim it with self-doubt.",
        "advice_hi": "अपने दृष्टिकोण को दैनिक अभ्यास में उतारें। आपका प्रकाश जरूरी है — आत्म-संदेह से इसे धुंधला मत करें।",
        "lucky_months": [1, 2, 11],
    },
    22: {
        "theme": "The Master Builder",
        "theme_hi": "मास्टर निर्माता",
        "description": "Master Builder. Ability to turn grand visions into reality on a massive scale. Practical idealism and global impact are your calling.",
        "description_hi": "मास्टर निर्माता। भव्य दृष्टिकोण को बड़े पैमाने पर वास्तविकता में बदलने की क्षमता। व्यावहारिक आदर्शवाद और वैश्विक प्रभाव आपकी पुकार है।",
        "focus_areas": "Large-scale construction, global organizations, philanthropy, infrastructure, leadership",
        "focus_areas_hi": "बड़े पैमाने पर निर्माण, वैश्विक संगठन, परोपकार, बुनियादी ढांचा, नेतृत्व",
        "advice": "Think big but act in disciplined steps. Grandiosity without execution wastes the gift.",
        "advice_hi": "बड़ा सोचें लेकिन अनुशासित कदमों से काम करें। क्रियान्वयन के बिना भव्यता उपहार को बर्बाद करती है।",
        "lucky_months": [4, 8, 11, 22],
    },
    33: {
        "theme": "The Master Teacher",
        "theme_hi": "मास्टर शिक्षक",
        "description": "Master Teacher. Selfless service, healing, and uplifting humanity. The highest expression of love in action.",
        "description_hi": "मास्टर शिक्षक। निःस्वार्थ सेवा, उपचार और मानवता का उत्थान। क्रिया में प्रेम की सर्वोच्च अभिव्यक्ति।",
        "focus_areas": "Healing, teaching, counseling, spiritual guidance, humanitarian service, arts",
        "focus_areas_hi": "उपचार, शिक्षण, परामर्श, आध्यात्मिक मार्गदर्शन, मानवतावादी सेवा, कला",
        "advice": "Your compassion must be boundless but your energy is finite — honour both.",
        "advice_hi": "आपकी करुणा असीमित होनी चाहिए लेकिन आपकी ऊर्जा सीमित है — दोनों का सम्मान करें।",
        "lucky_months": [3, 6, 9, 33],
    },
}

def _normalize_focus_areas(data):
    """Recursively convert any focus_areas / focus_areas_hi string values to lists."""
    if isinstance(data, dict):
        out = {}
        for k, v in data.items():
            if k in ("focus_areas", "focus_areas_hi") and isinstance(v, str):
                out[k] = [s.strip() for s in v.split(",") if s.strip()]
            elif isinstance(v, dict):
                out[k] = _normalize_focus_areas(v)
            elif isinstance(v, list):
                out[k] = [_normalize_focus_areas(i) if isinstance(i, dict) else i for i in v]
            else:
                out[k] = v
        return out
    return data


# Destiny number predictions (derived from full name)
DESTINY_PREDICTIONS = {
    1: {
        "theme": "Leader & Innovator",
        "theme_hi": "नेता और नवप्रवर्तक",
        "description": "Your destiny calls you to lead and innovate. You are meant to carve original paths and inspire others through decisive action. Embrace independence and trust your unique vision to leave a lasting mark.",
        "description_hi": "आपकी नियति आपको नेतृत्व और नवाचार के लिए बुलाती है। आप मौलिक रास्ते बनाने और दूसरों को निर्णायक कार्रवाई से प्रेरित करने के लिए बने हैं।",
        "focus_areas": "Pioneer new fields, take initiative, build your own enterprise",
        "focus_areas_hi": "नए क्षेत्र खोलें, पहल करें, अपना उद्यम बनाएं",
        "advice": "Your originality is your greatest asset — never dilute it to fit in.",
        "advice_hi": "आपकी मौलिकता आपकी सबसे बड़ी संपत्ति है — इसे कभी मत घटाएं।",
    },
    2: {
        "theme": "Diplomat & Unifier",
        "theme_hi": "कूटनीतिज्ञ और एकजुट करने वाला",
        "description": "Your destiny is rooted in partnership and diplomacy. You are here to mediate, unite, and bring balance to those around you. Your greatest achievements come through collaboration and gentle persuasion.",
        "description_hi": "आपकी नियति साझेदारी और कूटनीति में निहित है। आप मध्यस्थता, एकता और संतुलन लाने के लिए यहाँ हैं।",
        "focus_areas": "Build bridges between people, support others' visions, create harmony",
        "focus_areas_hi": "लोगों के बीच पुल बनाएं, दूसरों के दृष्टिकोण का समर्थन करें, सामंजस्य बनाएं",
        "advice": "Your power lies in influence, not control. Work behind the scenes with confidence.",
        "advice_hi": "आपकी शक्ति प्रभाव में है, नियंत्रण में नहीं। आत्मविश्वास के साथ पर्दे के पीछे काम करें।",
    },
    3: {
        "theme": "Creative Inspirer",
        "theme_hi": "रचनात्मक प्रेरक",
        "description": "Your destiny is one of creative self-expression. Writing, speaking, art, or performance are natural outlets for your vibrant energy. You uplift others through joy and are meant to inspire with your words.",
        "description_hi": "आपकी नियति रचनात्मक आत्म-अभिव्यक्ति की है। लेखन, भाषण, कला या प्रदर्शन आपकी जीवंत ऊर्जा के प्राकृतिक माध्यम हैं।",
        "focus_areas": "Create, communicate, perform, teach joy and possibility",
        "focus_areas_hi": "बनाएं, संवाद करें, प्रदर्शन करें, आनंद और संभावना सिखाएं",
        "advice": "Discipline your creativity — inspiration without execution is just daydreaming.",
        "advice_hi": "अपनी रचनात्मकता को अनुशासित करें — क्रियान्वयन के बिना प्रेरणा सिर्फ दिवास्वप्न है।",
    },
    4: {
        "theme": "Architect of Endurance",
        "theme_hi": "स्थायित्व का वास्तुकार",
        "description": "Your destiny demands structure and dedication. You are the architect of lasting systems and institutions. Through methodical effort and unwavering integrity, you build what endures beyond a lifetime.",
        "description_hi": "आपकी नियति संरचना और समर्पण की मांग करती है। आप स्थायी प्रणालियों और संस्थाओं के वास्तुकार हैं।",
        "focus_areas": "Build systems that outlast you, master your craft, establish lasting order",
        "focus_areas_hi": "ऐसी प्रणालियां बनाएं जो आपसे आगे जाएं, अपनी कला में निपुण हों, स्थायी व्यवस्था स्थापित करें",
        "advice": "Consistency over time is your magic. Show up every day, even when uninspired.",
        "advice_hi": "समय के साथ निरंतरता आपका जादू है। हर दिन आएं, भले ही प्रेरणा न हो।",
    },
    5: {
        "theme": "Adventurer & Change Agent",
        "theme_hi": "साहसी और परिवर्तन दूत",
        "description": "Your destiny thrives on change and exploration. You are meant to experience the full breadth of life and share those adventures with others. Adaptability and curiosity are your greatest gifts.",
        "description_hi": "आपकी नियति परिवर्तन और अन्वेषण पर फलती है। आप जीवन की पूरी विस्तृत श्रृंखला का अनुभव करने और उन साहसिक कार्यों को दूसरों के साथ साझा करने के लिए बने हैं।",
        "focus_areas": "Explore widely, adapt fearlessly, share discoveries, champion freedom",
        "focus_areas_hi": "व्यापक रूप से खोजें, निडरता से अनुकूल हों, खोजें साझा करें, स्वतंत्रता की वकालत करें",
        "advice": "Your restlessness is a signal to grow, not to escape. Find the adventure within commitment.",
        "advice_hi": "आपकी बेचैनी बढ़ने का संकेत है, पलायन का नहीं। प्रतिबद्धता के भीतर साहस खोजें।",
    },
    6: {
        "theme": "Guardian of Love",
        "theme_hi": "प्रेम का संरक्षक",
        "description": "Your destiny centers on love, responsibility, and service to family and community. You are a natural counselor and protector. Your fulfillment comes from creating beauty and harmony in your surroundings.",
        "description_hi": "आपकी नियति प्रेम, जिम्मेदारी और परिवार तथा समुदाय की सेवा पर केंद्रित है। आप एक प्राकृतिक परामर्शदाता और रक्षक हैं।",
        "focus_areas": "Heal relationships, beautify spaces, counsel and protect, serve community",
        "focus_areas_hi": "रिश्तों को ठीक करें, स्थानों को सुंदर बनाएं, परामर्श दें और रक्षा करें, समुदाय की सेवा करें",
        "advice": "You cannot pour from an empty cup — nurture yourself first, then others.",
        "advice_hi": "खाली कप से नहीं डाल सकते — पहले खुद का पोषण करें, फिर दूसरों का।",
    },
    7: {
        "theme": "Wisdom Seeker",
        "theme_hi": "ज्ञान खोजी",
        "description": "Your destiny lies in the pursuit of truth and wisdom. You are a natural researcher, philosopher, and spiritual seeker. Depth of understanding, not breadth, is your path to mastery.",
        "description_hi": "आपकी नियति सत्य और ज्ञान की खोज में निहित है। आप एक प्राकृतिक शोधकर्ता, दार्शनिक और आध्यात्मिक खोजी हैं।",
        "focus_areas": "Research deeply, develop expertise, teach what you discover, seek spiritual truth",
        "focus_areas_hi": "गहराई से शोध करें, विशेषज्ञता विकसित करें, जो खोजें उसे सिखाएं, आध्यात्मिक सत्य खोजें",
        "advice": "Trust the process of going inward — your answers live in silence, not noise.",
        "advice_hi": "भीतर जाने की प्रक्रिया पर भरोसा करें — आपके उत्तर शांति में हैं, शोर में नहीं।",
    },
    8: {
        "theme": "Master of Power & Karma",
        "theme_hi": "शक्ति और कर्म के स्वामी",
        "description": "Your destiny is tied to material achievement and the responsible use of power. You are meant to build prosperity and influence, but karmic balance demands that you wield authority with fairness.",
        "description_hi": "आपकी नियति भौतिक उपलब्धि और शक्ति के जिम्मेदार उपयोग से जुड़ी है। आप समृद्धि और प्रभाव बनाने के लिए बने हैं, लेकिन कर्म संतुलन के लिए न्यायपूर्ण अधिकार की आवश्यकता है।",
        "focus_areas": "Build wealth with integrity, lead organizations, master financial systems",
        "focus_areas_hi": "ईमानदारी से धन बनाएं, संगठनों का नेतृत्व करें, वित्तीय प्रणालियों में निपुण हों",
        "advice": "Power is your destiny, not your identity. Serve through it, don't be consumed by it.",
        "advice_hi": "शक्ति आपकी नियति है, आपकी पहचान नहीं। इसके माध्यम से सेवा करें, इसमें डूबें नहीं।",
    },
    9: {
        "theme": "Universal Servant",
        "theme_hi": "सार्वभौमिक सेवक",
        "description": "Your destiny is humanitarian service on a grand scale. You are meant to give selflessly and inspire compassion in others. Letting go of personal attachment frees you to serve your highest calling.",
        "description_hi": "आपकी नियति बड़े पैमाने पर मानवतावादी सेवा है। आप निःस्वार्थ रूप से देने और दूसरों में करुणा जगाने के लिए बने हैं।",
        "focus_areas": "Philanthropy, global healing, inspire through art, teach universal love",
        "focus_areas_hi": "परोपकार, वैश्विक उपचार, कला के माध्यम से प्रेरित करें, सार्वभौमिक प्रेम सिखाएं",
        "advice": "Everything you release comes back tenfold. The more you give, the more you receive.",
        "advice_hi": "आप जो छोड़ते हैं वह दस गुना लौटता है। जितना देते हैं, उतना पाते हैं।",
    },
    11: {
        "theme": "Spiritual Illuminator",
        "theme_hi": "आध्यात्मिक प्रकाशक",
        "description": "Your destiny carries the weight of spiritual illumination. As a master number, you channel higher truths into the world. Visionary leadership and inspired teaching are your sacred responsibilities.",
        "description_hi": "आपकी नियति आध्यात्मिक प्रकाश का भार वहन करती है। एक मास्टर अंक के रूप में, आप उच्च सत्यों को दुनिया में प्रसारित करते हैं।",
        "focus_areas": "Inspire millions, channel higher wisdom, lead through example",
        "focus_areas_hi": "लाखों को प्रेरित करें, उच्च ज्ञान को प्रसारित करें, उदाहरण के माध्यम से नेतृत्व करें",
        "advice": "Your sensitivity is the antenna that picks up what others miss. Protect it, don't suppress it.",
        "advice_hi": "आपकी संवेदनशीलता वह एंटीना है जो दूसरों से छूटा हुआ पकड़ती है। इसे संरक्षित करें, दबाएं नहीं।",
    },
    22: {
        "theme": "Master Manifestor",
        "theme_hi": "मास्टर प्रकटक",
        "description": "Your destiny is to manifest visionary ideals in concrete form. You possess rare ability to combine spiritual insight with practical genius. Large-scale projects that serve humanity are your life work.",
        "description_hi": "आपकी नियति दूरदर्शी आदर्शों को ठोस रूप में प्रकट करना है। आपके पास आध्यात्मिक अंतर्दृष्टि को व्यावहारिक प्रतिभा के साथ जोड़ने की दुर्लभ क्षमता है।",
        "focus_areas": "Build institutions, create systems at scale, combine vision with discipline",
        "focus_areas_hi": "संस्थाएं बनाएं, बड़े पैमाने पर प्रणालियां बनाएं, दृष्टि को अनुशासन के साथ जोड़ें",
        "advice": "Dream at the level of 22, execute at the level of 4. Both are you.",
        "advice_hi": "22 के स्तर पर सपने देखें, 4 के स्तर पर क्रियान्वित करें। दोनों आप हैं।",
    },
    33: {
        "theme": "Master of Compassionate Service",
        "theme_hi": "करुणामय सेवा के स्वामी",
        "description": "Your destiny is the highest form of loving service. You are called to heal, teach, and uplift on a profound level. Selfless devotion to others transforms both you and those you touch.",
        "description_hi": "आपकी नियति प्रेमपूर्ण सेवा का सर्वोच्च रूप है। आपको गहरे स्तर पर उपचार करने, सिखाने और उत्थान करने के लिए बुलाया गया है।",
        "focus_areas": "Heal at the deepest level, teach unconditional love, serve without ego",
        "focus_areas_hi": "गहरे स्तर पर उपचार करें, बिना शर्त प्रेम सिखाएं, अहंकार रहित सेवा करें",
        "advice": "You carry the world's pain — learn to transmute it rather than absorb it.",
        "advice_hi": "आप दुनिया का दर्द उठाते हैं — इसे अवशोषित करने के बजाय रूपांतरित करना सीखें।",
    },
}

# Soul Urge predictions (derived from vowels in name)
SOUL_URGE_PREDICTIONS = {
    1: {
        "theme": "Inner Independence",
        "theme_hi": "आंतरिक स्वतंत्रता",
        "description": "Deep within, you crave autonomy and the freedom to chart your own course. Your inner drive is to be first, to originate, and to stand apart. Honoring this need for independence fuels your spirit.",
        "description_hi": "गहरे भीतर, आप स्वायत्तता और अपना रास्ता खुद बनाने की स्वतंत्रता चाहते हैं। आपकी आंतरिक प्रेरणा पहले रहने, मौलिक होने और अलग खड़े होने की है।",
        "advice": "Honour your need to lead from within. Don't shrink to fit others' comfort.",
        "advice_hi": "भीतर से नेतृत्व करने की अपनी जरूरत का सम्मान करें। दूसरों की सुविधा के लिए खुद को छोटा मत करें।",
    },
    2: {
        "theme": "Inner Harmony",
        "theme_hi": "आंतरिक सामंजस्य",
        "description": "Your soul yearns for deep connection and emotional harmony. You find inner peace through loving partnerships and quiet acts of kindness. Being truly seen and valued by another fulfills you profoundly.",
        "description_hi": "आपकी आत्मा गहरे संबंध और भावनात्मक सामंजस्य के लिए तरसती है। आप प्रेमपूर्ण साझेदारी और दयालुता के शांत कार्यों के माध्यम से आंतरिक शांति पाते हैं।",
        "advice": "Your need for connection is valid. Ask for what you need — others cannot read your silence.",
        "advice_hi": "संबंध की आपकी जरूरत वैध है। जो चाहिए वह मांगें — दूसरे आपकी चुप्पी नहीं पढ़ सकते।",
    },
    3: {
        "theme": "Inner Creative Fire",
        "theme_hi": "आंतरिक रचनात्मक अग्नि",
        "description": "At your core, you desire joyful self-expression and creative freedom. Your inner world is vivid and imaginative. Sharing your ideas, humor, and artistic vision with others nourishes your deepest self.",
        "description_hi": "अपने मूल में, आप आनंदपूर्ण आत्म-अभिव्यक्ति और रचनात्मक स्वतंत्रता चाहते हैं। आपकी आंतरिक दुनिया जीवंत और कल्पनाशील है।",
        "advice": "Create daily — not for perfection, but for the joy of it. Your art is therapy.",
        "advice_hi": "प्रतिदिन बनाएं — पूर्णता के लिए नहीं, बल्कि इसके आनंद के लिए। आपकी कला चिकित्सा है।",
    },
    4: {
        "theme": "Inner Security",
        "theme_hi": "आंतरिक सुरक्षा",
        "description": "Your soul craves order, security, and a sense of accomplishment. You feel most at peace when life is stable and your efforts produce tangible results. Building a solid foundation satisfies your inner need.",
        "description_hi": "आपकी आत्मा व्यवस्था, सुरक्षा और उपलब्धि की भावना चाहती है। आप तब सबसे अधिक शांति में होते हैं जब जीवन स्थिर हो।",
        "advice": "Security comes from within. No external structure will ever feel 'enough' until you trust yourself.",
        "advice_hi": "सुरक्षा भीतर से आती है। जब तक आप खुद पर भरोसा नहीं करते, कोई बाहरी ढांचा 'पर्याप्त' नहीं लगेगा।",
    },
    5: {
        "theme": "Inner Freedom",
        "theme_hi": "आंतरिक स्वतंत्रता",
        "description": "Your innermost desire is for freedom, variety, and sensory experience. Routine stifles your spirit. You need adventure, travel, and the thrill of the unknown to feel truly alive.",
        "description_hi": "आपकी सबसे गहरी इच्छा स्वतंत्रता, विविधता और संवेदी अनुभव के लिए है। दिनचर्या आपकी आत्मा को दबाती है।",
        "advice": "True freedom is internal. Master discipline so that you choose your adventures rather than flee from discomfort.",
        "advice_hi": "सच्ची स्वतंत्रता आंतरिक है। अनुशासन में महारत हासिल करें ताकि आप असुविधा से भागने के बजाय अपने साहसिक कार्य चुनें।",
    },
    6: {
        "theme": "Inner Love",
        "theme_hi": "आंतरिक प्रेम",
        "description": "Your soul longs to nurture, protect, and create a harmonious home. Love and family are your deepest motivations. You feel most fulfilled when those you care for are happy and safe.",
        "description_hi": "आपकी आत्मा पोषण करने, सुरक्षा करने और सामंजस्यपूर्ण घर बनाने के लिए तरसती है। प्रेम और परिवार आपकी सबसे गहरी प्रेरणाएं हैं।",
        "advice": "You are not responsible for everyone's happiness. Love generously but release the need to fix everything.",
        "advice_hi": "आप सबकी खुशी के लिए जिम्मेदार नहीं हैं। उदारता से प्यार करें लेकिन सब कुछ ठीक करने की जरूरत छोड़ें।",
    },
    7: {
        "theme": "Inner Wisdom",
        "theme_hi": "आंतरिक ज्ञान",
        "description": "Your inner world craves solitude, reflection, and spiritual understanding. You need time alone to think, meditate, and explore the mysteries of existence. Inner peace comes through contemplation.",
        "description_hi": "आपकी आंतरिक दुनिया एकांत, चिंतन और आध्यात्मिक समझ चाहती है। आपको सोचने, ध्यान करने और अस्तित्व के रहस्यों का पता लगाने के लिए अकेले समय चाहिए।",
        "advice": "Protect your inner silence fiercely. The world will pull you out — let your solitude be sacred.",
        "advice_hi": "अपनी आंतरिक शांति की दृढ़ता से रक्षा करें। दुनिया आपको बाहर खींचेगी — अपने एकांत को पवित्र रहने दें।",
    },
    8: {
        "theme": "Inner Achievement Drive",
        "theme_hi": "आंतरिक उपलब्धि की प्रेरणा",
        "description": "Deep down, you desire recognition, achievement, and material security. You are driven to prove your competence and build something of lasting value. Success and respect satisfy your soul.",
        "description_hi": "गहरे भीतर, आप पहचान, उपलब्धि और भौतिक सुरक्षा चाहते हैं। आप अपनी क्षमता साबित करने और स्थायी मूल्य का कुछ बनाने के लिए प्रेरित हैं।",
        "advice": "Chase significance, not just success. Build legacy — money is a byproduct, not the goal.",
        "advice_hi": "सिर्फ सफलता नहीं, महत्व की ओर बढ़ें। विरासत बनाएं — पैसा उपोत्पाद है, लक्ष्य नहीं।",
    },
    9: {
        "theme": "Inner Universal Love",
        "theme_hi": "आंतरिक सार्वभौमिक प्रेम",
        "description": "Your soul urges you toward universal love and selfless giving. You feel most fulfilled when serving a cause greater than yourself. Compassion and idealism are the wellsprings of your inner life.",
        "description_hi": "आपकी आत्मा आपको सार्वभौमिक प्रेम और निःस्वार्थ दान की ओर प्रेरित करती है। जब आप खुद से बड़े किसी उद्देश्य की सेवा करते हैं तो आप सबसे अधिक संतुष्ट होते हैं।",
        "advice": "Let go of what is finished. Clinging to the past blocks the universal flow meant for you.",
        "advice_hi": "जो समाप्त हो गया उसे छोड़ दें। अतीत से चिपकना आपके लिए निर्धारित सार्वभौमिक प्रवाह को रोकता है।",
    },
    11: {
        "theme": "Inner Spiritual Calling",
        "theme_hi": "आंतरिक आध्यात्मिक पुकार",
        "description": "Your soul carries an intense longing for spiritual truth and inspired purpose. You sense a higher calling and feel restless until you align with it. Intuition is your most trusted inner guide.",
        "description_hi": "आपकी आत्मा आध्यात्मिक सत्य और प्रेरित उद्देश्य के लिए तीव्र लालसा वहन करती है। आप एक उच्च पुकार महसूस करते हैं और जब तक आप इसके साथ संरेखित नहीं होते तब तक बेचैन रहते हैं।",
        "advice": "Stop seeking permission to be spiritual. Your calling is real — act on it now.",
        "advice_hi": "आध्यात्मिक होने की अनुमति मांगना बंद करें। आपकी पुकार वास्तविक है — अभी इस पर कार्य करें।",
    },
    22: {
        "theme": "Inner Vision for Humanity",
        "theme_hi": "मानवता के लिए आंतरिक दृष्टि",
        "description": "Your deepest desire is to build something of lasting significance for humanity. Ordinary ambitions feel hollow. You are driven by a vision so large that only disciplined mastery can bring it to life.",
        "description_hi": "आपकी सबसे गहरी इच्छा मानवता के लिए स्थायी महत्व की कुछ चीज़ बनाना है। सामान्य महत्वाकांक्षाएं खोखली लगती हैं।",
        "advice": "Your vision is not arrogance — it is your assignment. Find the team that can help you execute it.",
        "advice_hi": "आपका दृष्टिकोण अहंकार नहीं है — यह आपका कार्यभार है। वह टीम खोजें जो इसे क्रियान्वित करने में मदद कर सके।",
    },
    33: {
        "theme": "Inner Compassionate Fire",
        "theme_hi": "आंतरिक करुणामय अग्नि",
        "description": "Your soul burns with compassion and a desire to heal the world. You carry the weight of empathy for all living things. Channeling this love into service brings you the deepest possible fulfillment.",
        "description_hi": "आपकी आत्मा करुणा और दुनिया को ठीक करने की इच्छा से जलती है। आप सभी जीवित प्राणियों के लिए सहानुभूति का बोझ वहन करते हैं।",
        "advice": "Feel it all, but don't drown in it. Boundaries are acts of love, not betrayal.",
        "advice_hi": "सब कुछ महसूस करें, लेकिन उसमें डूबें नहीं। सीमाएं प्रेम के कार्य हैं, विश्वासघात नहीं।",
    },
}

# Personality predictions (derived from consonants in name)
PERSONALITY_PREDICTIONS = {
    1: {
        "theme": "Projects Confidence",
        "theme_hi": "आत्मविश्वास प्रकट करता है",
        "description": "Others perceive you as confident, assertive, and self-assured. You project an image of strength and capability. People naturally look to you for direction and are drawn to your decisive energy.",
        "description_hi": "दूसरे आपको आत्मविश्वासी, दृढ़ और आश्वस्त मानते हैं। आप शक्ति और क्षमता की छवि प्रकट करते हैं। लोग स्वाभाविक रूप से दिशा के लिए आपकी ओर देखते हैं।",
        "advice": "Soften your exterior occasionally — vulnerability builds deeper trust than strength alone.",
        "advice_hi": "कभी-कभी अपनी बाहरी कठोरता को नरम करें — भेद्यता अकेली ताकत से गहरा विश्वास बनाती है।",
    },
    2: {
        "theme": "Projects Warmth",
        "theme_hi": "गर्मजोशी प्रकट करता है",
        "description": "You come across as warm, approachable, and tactful. Others see you as a supportive listener and a calming presence. Your gentle demeanor invites trust and puts people at ease.",
        "description_hi": "आप गर्म, सुलभ और चतुर लगते हैं। दूसरे आपको एक सहायक श्रोता और शांत उपस्थिति के रूप में देखते हैं।",
        "advice": "Your softness is not weakness. Own it as your most disarming and powerful trait.",
        "advice_hi": "आपकी कोमलता कमज़ोरी नहीं है। इसे अपनी सबसे निरस्त्रीकरण और शक्तिशाली विशेषता के रूप में स्वीकार करें।",
    },
    3: {
        "theme": "Projects Charisma",
        "theme_hi": "करिश्मा प्रकट करता है",
        "description": "You radiate charm, wit, and social magnetism. Others see you as entertaining, expressive, and full of life. Your outward personality draws people in and makes social situations effortless.",
        "description_hi": "आप आकर्षण, बुद्धिमत्ता और सामाजिक चुंबकत्व विकीर्ण करते हैं। दूसरे आपको मनोरंजक, अभिव्यंजक और जीवन से भरपूर देखते हैं।",
        "advice": "Don't perform joy — embody it. People sense when the mask slips.",
        "advice_hi": "आनंद का प्रदर्शन मत करें — इसे जिएं। लोग तब महसूस करते हैं जब नकाब फिसलता है।",
    },
    4: {
        "theme": "Projects Reliability",
        "theme_hi": "विश्वसनीयता प्रकट करता है",
        "description": "Others perceive you as reliable, grounded, and hardworking. You project stability and competence. People trust you with responsibility because your exterior signals discipline and dependability.",
        "description_hi": "दूसरे आपको विश्वसनीय, ज़मीन से जुड़े और मेहनती मानते हैं। आप स्थिरता और क्षमता प्रकट करते हैं।",
        "advice": "Let people see your passion, not just your process. Warmth builds loyalty beyond competence.",
        "advice_hi": "लोगों को अपनी प्रक्रिया नहीं, अपना जुनून देखने दें। गर्मजोशी क्षमता से परे वफादारी बनाती है।",
    },
    5: {
        "theme": "Projects Dynamic Energy",
        "theme_hi": "गतिशील ऊर्जा प्रकट करता है",
        "description": "You appear dynamic, energetic, and magnetically attractive. Others see you as someone who embraces life fully. Your outward persona suggests excitement, versatility, and a love of the unconventional.",
        "description_hi": "आप गतिशील, ऊर्जावान और चुंबकीय रूप से आकर्षक दिखते हैं। दूसरे आपको ऐसे व्यक्ति के रूप में देखते हैं जो जीवन को पूरी तरह अपनाता है।",
        "advice": "Your energy inspires — channel it with focus so others can follow, not just admire.",
        "advice_hi": "आपकी ऊर्जा प्रेरित करती है — इसे केंद्रित रूप से प्रसारित करें ताकि दूसरे अनुसरण कर सकें, न केवल प्रशंसा।",
    },
    6: {
        "theme": "Projects Nurturing Care",
        "theme_hi": "पोषणकारी देखभाल प्रकट करता है",
        "description": "Others see you as caring, responsible, and devoted. You project an aura of warmth and domestic grace. People turn to you for comfort and counsel, sensing your genuine concern for their well-being.",
        "description_hi": "दूसरे आपको देखभाल करने वाले, जिम्मेदार और समर्पित देखते हैं। आप गर्मजोशी और घरेलू अनुग्रह का आभामंडल प्रकट करते हैं।",
        "advice": "You attract those who need healing — discern who is growing versus who is draining.",
        "advice_hi": "आप उन लोगों को आकर्षित करते हैं जिन्हें उपचार की जरूरत है — जो बढ़ रहे हैं और जो थका रहे हैं उनमें भेद करें।",
    },
    7: {
        "theme": "Projects Mysterious Depth",
        "theme_hi": "रहस्यमय गहराई प्रकट करता है",
        "description": "You come across as reserved, intellectual, and somewhat mysterious. Others sense depth beneath your calm exterior. Your dignified bearing commands respect and invites curiosity rather than casual approach.",
        "description_hi": "आप आरक्षित, बौद्धिक और कुछ हद तक रहस्यमय लगते हैं। दूसरे आपकी शांत बाहरी उपस्थिति के नीचे गहराई महसूस करते हैं।",
        "advice": "Let a few chosen people in. True intimacy is not a threat to your solitude — it deepens it.",
        "advice_hi": "कुछ चुने हुए लोगों को अंदर आने दें। सच्ची अंतरंगता आपके एकांत के लिए खतरा नहीं है — यह इसे गहरा करती है।",
    },
    8: {
        "theme": "Projects Authority",
        "theme_hi": "अधिकार प्रकट करता है",
        "description": "Others perceive you as powerful, successful, and authoritative. You project an image of material competence and executive ability. Your presence commands attention in professional settings.",
        "description_hi": "दूसरे आपको शक्तिशाली, सफल और अधिकारपूर्ण मानते हैं। आप भौतिक क्षमता और कार्यकारी योग्यता की छवि प्रकट करते हैं।",
        "advice": "Approachability is a superpower for those in authority. Lower the walls occasionally.",
        "advice_hi": "सुलभता उन लोगों के लिए महाशक्ति है जो अधिकार में हैं। कभी-कभी दीवारें कम करें।",
    },
    9: {
        "theme": "Projects Worldly Wisdom",
        "theme_hi": "सांसारिक ज्ञान प्रकट करता है",
        "description": "You appear compassionate, worldly, and sophisticated. Others see you as someone with broad vision and generous spirit. Your exterior projects tolerance, wisdom, and a noble bearing.",
        "description_hi": "आप करुणामय, सांसारिक और परिष्कृत दिखते हैं। दूसरे आपको व्यापक दृष्टि और उदार आत्मा वाले व्यक्ति के रूप में देखते हैं।",
        "advice": "Don't give so much that you disappear. Your identity matters as much as your generosity.",
        "advice_hi": "इतना मत दें कि आप गायब हो जाएं। आपकी पहचान आपकी उदारता जितनी ही मायने रखती है।",
    },
    11: {
        "theme": "Projects Luminous Inspiration",
        "theme_hi": "प्रकाशमान प्रेरणा प्रकट करता है",
        "description": "Others perceive you as inspired, charismatic, and slightly otherworldly. You project a luminous quality that draws attention. People sense your heightened awareness and visionary nature.",
        "description_hi": "दूसरे आपको प्रेरित, करिश्माई और थोड़ा अलौकिक मानते हैं। आप एक प्रकाशमान गुण प्रकट करते हैं जो ध्यान आकर्षित करता है।",
        "advice": "Your presence already inspires — trust that and stop trying to earn the room's approval.",
        "advice_hi": "आपकी उपस्थिति पहले से प्रेरित करती है — उस पर भरोसा करें और कमरे की स्वीकृति अर्जित करने की कोशिश बंद करें।",
    },
    22: {
        "theme": "Projects Masterful Capability",
        "theme_hi": "दक्ष क्षमता प्रकट करता है",
        "description": "You come across as exceptionally capable and ambitious on a grand scale. Others see a master organizer with the power to transform ideas into reality. Your presence inspires confidence in large endeavors.",
        "description_hi": "आप बड़े पैमाने पर असाधारण रूप से सक्षम और महत्वाकांक्षी लगते हैं। दूसरे आपको विचारों को वास्तविकता में बदलने की शक्ति वाले मास्टर आयोजक के रूप में देखते हैं।",
        "advice": "Show your humanity alongside your mastery. Greatness with warmth endures longest.",
        "advice_hi": "अपनी महारत के साथ अपनी मानवता दिखाएं। गर्मजोशी के साथ महानता सबसे लंबे समय तक टिकती है।",
    },
    33: {
        "theme": "Projects Unconditional Compassion",
        "theme_hi": "बिना शर्त करुणा प्रकट करता है",
        "description": "Others perceive you as deeply compassionate and selflessly devoted. You project an almost saintly warmth that draws people seeking guidance. Your exterior radiates unconditional love and healing energy.",
        "description_hi": "दूसरे आपको गहरे करुणामय और निःस्वार्थ रूप से समर्पित मानते हैं। आप एक लगभग संत जैसी गर्मजोशी प्रकट करते हैं जो मार्गदर्शन मांगने वाले लोगों को आकर्षित करती है।",
        "advice": "You cannot save everyone. Discern where your healing is wanted versus where it is projected onto you.",
        "advice_hi": "आप सबको नहीं बचा सकते। पहचानें कि आपका उपचार कहाँ चाहा जाता है बनाम कहाँ आप पर प्रक्षेपित किया जाता है।",
    },
}


# ============================================================
# NAME NUMEROLOGY - Detailed Name Analysis
# ============================================================

NAME_NUMBER_PREDICTIONS = {
    1: {
        "title": "The Leader", "title_hi": "नेता",
        "ruling_planet": "Sun", "ruling_planet_hi": "सूर्य",
        "traits": ["Independent", "Ambitious", "Innovative", "Self-reliant", "Determined"],
        "traits_hi": ["स्वतंत्र", "महत्वाकांक्षी", "नवीन", "आत्मनिर्भर", "दृढ़निश्चयी"],
        "career": "Entrepreneurship, Management, Politics, Military, Sports, Any leadership role",
        "career_hi": "उद्यमिता, प्रबंधन, राजनीति, सैन्य, खेल, कोई भी नेतृत्व की भूमिका",
        "relationships": "You need a partner who respects your independence. You tend to take charge in relationships.",
        "relationships_hi": "आपको ऐसे साथी की ज़रूरत है जो आपकी स्वतंत्रता का सम्मान करे। आप रिश्तों में नेतृत्व करते हैं।",
        "health": "Heart, circulation, eyes. Avoid stress and overwork.",
        "health_hi": "हृदय, रक्त संचार, आँखें। तनाव और अत्यधिक काम से बचें।",
        "lucky_colors": ["Gold", "Orange", "Yellow"],
        "lucky_colors_hi": ["सोना", "नारंगी", "पीला"],
        "lucky_days": ["Sunday", "Monday"],
        "lucky_days_hi": ["रविवार", "सोमवार"],
        "advice": "Learn to delegate and listen to others. Your strength is in leading, not controlling.",
        "advice_hi": "दूसरों को काम सौंपना और उनकी सुनना सीखें। आपकी शक्ति नेतृत्व में है, नियंत्रण में नहीं।",
    },
    2: {
        "title": "The Peacemaker", "title_hi": "शांतिदूत",
        "ruling_planet": "Moon", "ruling_planet_hi": "चन्द्र",
        "traits": ["Diplomatic", "Sensitive", "Cooperative", "Intuitive", "Gentle"],
        "traits_hi": ["कूटनीतिक", "संवेदनशील", "सहयोगी", "अंतर्ज्ञानी", "कोमल"],
        "career": "Diplomacy, Counseling, Psychology, Art, Music, Nursing, Teaching",
        "career_hi": "कूटनीति, परामर्श, मनोविज्ञान, कला, संगीत, नर्सिंग, शिक्षण",
        "relationships": "You thrive in partnerships and need emotional connection. Avoid being overly dependent.",
        "relationships_hi": "आप साझेदारी में फलते-फूलते हैं और भावनात्मक जुड़ाव की ज़रूरत है। अत्यधिक निर्भरता से बचें।",
        "health": "Digestive system, fluids in body, emotional well-being. Practice meditation.",
        "health_hi": "पाचन तंत्र, शरीर के तरल पदार्थ, भावनात्मक स्वास्थ्य। ध्यान का अभ्यास करें।",
        "lucky_colors": ["White", "Silver", "Cream", "Green"],
        "lucky_colors_hi": ["सफेद", "चांदी", "क्रीम", "हरा"],
        "lucky_days": ["Sunday", "Monday"],
        "lucky_days_hi": ["रविवार", "सोमवार"],
        "advice": "Trust your intuition but don't let others take advantage of your kindness.",
        "advice_hi": "अपने अंतर्ज्ञान पर भरोसा करें लेकिन दूसरों को आपकी दयालुता का फायदा न उठाने दें।",
    },
    3: {
        "title": "The Creator", "title_hi": "सृजनकर्ता",
        "ruling_planet": "Jupiter", "ruling_planet_hi": "बृहस्पति",
        "traits": ["Creative", "Expressive", "Optimistic", "Social", "Artistic"],
        "traits_hi": ["रचनात्मक", "अभिव्यंजक", "आशावादी", "सामाजिक", "कलात्मक"],
        "career": "Writing, Acting, Singing, Teaching, Journalism, Marketing, Design",
        "career_hi": "लेखन, अभिनय, गायन, शिक्षण, पत्रकारिता, विपणन, डिजाइन",
        "relationships": "You are charming and popular. Seek depth in relationships beyond surface charm.",
        "relationships_hi": "आप आकर्षक और लोकप्रिय हैं। सतही आकर्षण से परे रिश्तों में गहराई खोजें।",
        "health": "Liver, skin, nervous system. Avoid excess in food and drink.",
        "health_hi": "यकृत, त्वचा, तंत्रिका तंत्र। खान-पान में अति से बचें।",
        "lucky_colors": ["Yellow", "Orange", "Purple"],
        "lucky_colors_hi": ["पीला", "नारंगी", "बैंगनी"],
        "lucky_days": ["Thursday", "Wednesday"],
        "lucky_days_hi": ["गुरुवार", "बुधवार"],
        "advice": "Focus your creative energy. Completion is as important as starting new projects.",
        "advice_hi": "अपनी रचनात्मक ऊर्जा को केंद्रित करें। नई परियोजनाएं शुरू करना जितना महत्वपूर्ण है, उन्हें पूरा करना भी उतना ही जरूरी है।",
    },
    4: {
        "title": "The Builder", "title_hi": "निर्माता",
        "ruling_planet": "Rahu", "ruling_planet_hi": "राहु",
        "traits": ["Practical", "Disciplined", "Reliable", "Organized", "Hardworking"],
        "traits_hi": ["व्यावहारिक", "अनुशासित", "विश्वसनीय", "व्यवस्थित", "मेहनती"],
        "career": "Engineering, Architecture, Accounting, Banking, Construction, IT",
        "career_hi": "इंजीनियरिंग, वास्तुकला, लेखांकन, बैंकिंग, निर्माण, आईटी",
        "relationships": "You are loyal and dependable. You need a partner who values stability.",
        "relationships_hi": "आप वफादार और भरोसेमंद हैं। आपको ऐसे साथी की ज़रूरत है जो स्थिरता को महत्व देता हो।",
        "health": "Bones, joints, digestion. Regular exercise and routine are essential.",
        "health_hi": "हड्डियाँ, जोड़, पाचन। नियमित व्यायाम और दिनचर्या आवश्यक है।",
        "lucky_colors": ["Blue", "Grey", "Black"],
        "lucky_colors_hi": ["नीला", "भूरा", "काला"],
        "lucky_days": ["Saturday", "Sunday"],
        "lucky_days_hi": ["शनिवार", "रविवार"],
        "advice": "Embrace change when necessary. Perfectionism can delay progress.",
        "advice_hi": "आवश्यकता पड़ने पर परिवर्तन को स्वीकार करें। पूर्णतावाद प्रगति में देरी कर सकता है।",
    },
    5: {
        "title": "The Adventurer", "title_hi": "साहसी",
        "ruling_planet": "Mercury", "ruling_planet_hi": "बुध",
        "traits": ["Versatile", "Curious", "Communicative", "Dynamic", "Freedom-loving"],
        "traits_hi": ["बहुमुखी", "जिज्ञासु", "संवादशील", "गतिशील", "स्वतंत्रता-प्रेमी"],
        "career": "Sales, Marketing, Travel, Journalism, Trading, Communication, Writing",
        "career_hi": "बिक्री, विपणन, यात्रा, पत्रकारिता, व्यापार, संचार, लेखन",
        "relationships": "You need variety and mental stimulation. Boredom is your enemy in relationships.",
        "relationships_hi": "आपको विविधता और मानसिक उत्तेजना की आवश्यकता है। रिश्तों में बोरियत आपकी दुश्मन है।",
        "health": "Nervous system, respiratory system. Practice breathing exercises.",
        "health_hi": "तंत्रिका तंत्र, श्वसन प्रणाली। श्वास संबंधी व्यायामों का अभ्यास करें।",
        "lucky_colors": ["Green", "Light Grey"],
        "lucky_colors_hi": ["हरा", "हल्का भूरा"],
        "lucky_days": ["Wednesday", "Friday"],
        "lucky_days_hi": ["बुधवार", "शुक्रवार"],
        "advice": "Commitment brings its own freedom. Don't run from stability.",
        "advice_hi": "प्रतिबद्धता अपनी स्वतंत्रता लाती है। स्थिरता से न भागें।",
    },
    6: {
        "title": "The Nurturer", "title_hi": "देखभाल करने वाला",
        "ruling_planet": "Venus", "ruling_planet_hi": "शुक्र",
        "traits": ["Loving", "Responsible", "Harmonious", "Artistic", "Protective"],
        "traits_hi": ["प्यार करने वाला", "जिम्मेदार", "सामंजस्यपूर्ण", "कलात्मक", "सुरक्षात्मक"],
        "career": "Teaching, Healing, Arts, Design, Hospitality, Counseling, Beauty Industry",
        "career_hi": "शिक्षण, उपचार, कला, डिजाइन, आतिथ्य, परामर्श, सौंदर्य उद्योग",
        "relationships": "Family and love are central to your life. You are devoted but avoid over-sacrifice.",
        "relationships_hi": "परिवार और प्यार आपके जीवन के केंद्र में हैं। आप समर्पित हैं लेकिन अत्यधिक त्याग से बचें।",
        "health": "Throat, kidneys, reproductive system. Maintain balance in lifestyle.",
        "health_hi": "गला, गुर्दे, प्रजनन प्रणाली। जीवनशैली में संतुलन बनाए रखें।",
        "lucky_colors": ["Pink", "Blue", "White"],
        "lucky_colors_hi": ["गुलाबी", "नीला", "सफेद"],
        "lucky_days": ["Friday", "Tuesday"],
        "lucky_days_hi": ["शुक्रवार", "मंगलवार"],
        "advice": "Love yourself first. You cannot pour from an empty cup.",
        "advice_hi": "पहले खुद से प्यार करें। आप खाली बर्तन से नहीं परोस सकते।",
    },
    7: {
        "title": "The Seeker", "title_hi": "सत्यान्वेषी",
        "ruling_planet": "Ketu", "ruling_planet_hi": "केतु",
        "traits": ["Spiritual", "Analytical", "Introspective", "Wise", "Mysterious"],
        "traits_hi": ["आध्यात्मिक", "विश्लेषणात्मक", "आत्मनिरीक्षण", "बुद्धिमान", "रहस्यमय"],
        "career": "Research, Science, Philosophy, Spirituality, Occult, Psychology, Analysis",
        "career_hi": "अनुसंधान, विज्ञान, दर्शन, आध्यात्मिकता, मनोगत, मनोविज्ञान, विश्लेषण",
        "relationships": "You need intellectual and spiritual connection. Surface relationships don't satisfy you.",
        "relationships_hi": "आपको बौद्धिक और आध्यात्मिक जुड़ाव की आवश्यकता है। सतही रिश्ते आपको संतुष्ट नहीं करते।",
        "health": "Nervous system, mental health. Meditation and solitude are healing.",
        "health_hi": "तंत्रिका तंत्र, मानसिक स्वास्थ्य। ध्यान और एकांत चंगा करने वाले हैं।",
        "lucky_colors": ["Green", "White", "Yellow"],
        "lucky_colors_hi": ["हरा", "सफेद", "पीला"],
        "lucky_days": ["Sunday", "Monday"],
        "lucky_days_hi": ["रविवार", "सोमवार"],
        "advice": "Balance solitude with social connection. Share your wisdom with the world.",
        "advice_hi": "एकांत को सामाजिक जुड़ाव के साथ संतुलित करें। अपना ज्ञान दुनिया के साथ साझा करें।",
    },
    8: {
        "title": "The Powerhouse", "title_hi": "शक्ति केंद्र",
        "ruling_planet": "Saturn", "ruling_planet_hi": "शनि",
        "traits": ["Ambitious", "Authoritative", "Practical", "Karmic", "Determined"],
        "traits_hi": ["महत्वाकांक्षी", "प्रभावशाली", "व्यावहारिक", "कार्मिक", "दृढ़निश्चयी"],
        "career": "Business, Law, Real Estate, Banking, Mining, Politics, Management",
        "career_hi": "व्यापार, कानून, रियल एस्टेट, बैंकिंग, खनन, राजनीति, प्रबंधन",
        "relationships": "Success comes later in life. Relationships require patience and maturity.",
        "relationships_hi": "सफलता जीवन में बाद में आती है। रिश्तों में धैर्य और परिपक्वता की आवश्यकता होती है।",
        "health": "Bones, joints, chronic conditions. Discipline in health routine is essential.",
        "health_hi": "हड्डियाँ, जोड़, पुरानी स्थितियाँ। स्वास्थ्य दिनचर्या में अनुशासन आवश्यक है।",
        "lucky_colors": ["Black", "Dark Blue", "Dark Grey"],
        "lucky_colors_hi": ["काला", "गहरा नीला", "गहरा भूरा"],
        "lucky_days": ["Saturday", "Sunday"],
        "lucky_days_hi": ["शनिवार", "रविवार"],
        "advice": "Success comes through persistent effort. Don't take shortcuts.",
        "advice_hi": "सफलता निरंतर प्रयास से आती है। शॉर्टकट न लें।",
    },
    9: {
        "title": "The Humanitarian", "title_hi": "मानवतावादी",
        "ruling_planet": "Mars", "ruling_planet_hi": "मंगल",
        "traits": ["Compassionate", "Generous", "Passionate", "Brave", "Idealistic"],
        "traits_hi": ["दयालु", "उदार", "जोशीला", "साहसी", "आदर्शवादी"],
        "career": "Social Work, Medicine, Teaching, Military, Engineering, Sports, NGO",
        "career_hi": "सामाजिक कार्य, चिकित्सा, शिक्षण, सैन्य, इंजीनियरिंग, खेल, एनजीओ",
        "relationships": "You love deeply and passionately. Channel Mars energy constructively.",
        "relationships_hi": "आप गहराई से और जोश के साथ प्यार करते हैं। मंगल ऊर्जा को रचनात्मक रूप से उपयोग करें।",
        "health": "Blood, muscles, head. Regular exercise is essential for you.",
        "health_hi": "रक्त, मांसपेशियाँ, सिर। नियमित व्यायाम आपके लिए आवश्यक है।",
        "lucky_colors": ["Red", "Coral", "Pink"],
        "lucky_colors_hi": ["लाल", "मूंगा", "गुलाबी"],
        "lucky_days": ["Tuesday", "Thursday"],
        "lucky_days_hi": ["मंगलवार", "गुरुवार"],
        "advice": "Letting go is as important as holding on. Forgiveness liberates you.",
        "advice_hi": "छोड़ना उतना ही महत्वपूर्ण है जितना थामे रखना। क्षमा आपको मुक्त करती है।",
    },
    11: {
        "title": "The Master Intuitive", "title_hi": "मास्टर अंतर्ज्ञानी",
        "ruling_planet": "Moon (Amplified)", "ruling_planet_hi": "चन्द्र (प्रवर्धित)",
        "traits": ["Visionary", "Intuitive", "Inspirational", "Sensitive", "Spiritual"],
        "traits_hi": ["दूरदर्शी", "अंतर्ज्ञानी", "प्रेरणादायक", "संवेदनशील", "आध्यात्मिक"],
        "career": "Spiritual Leadership, Counseling, Art, Healing, Innovation, Teaching",
        "career_hi": "आध्यात्मिक नेतृत्व, परामर्श, कला, उपचार, नवाचार, शिक्षण",
        "relationships": "You need a partner who understands your sensitivity and spiritual nature.",
        "relationships_hi": "आपको ऐसे साथी की ज़रूरत है जो आपकी संवेदनशीलता और आध्यात्मिक स्वभाव को समझे।",
        "health": "Nervous system, anxiety management. Ground your visions in reality.",
        "health_hi": "तंत्रिका तंत्र, चिंता प्रबंधन। अपने दृष्टिकोण को वास्तविकता में उतारें।",
        "lucky_colors": ["Silver", "White", "Cream"],
        "lucky_colors_hi": ["चांदी", "सफेद", "क्रीम"],
        "lucky_days": ["Sunday", "Monday"],
        "lucky_days_hi": ["रविवार", "सोमवार"],
        "advice": "Your intuition is a gift. Learn to trust it while staying grounded.",
        "advice_hi": "आपका अंतर्ज्ञान एक उपहार है। जमीन से जुड़े रहते हुए इस पर भरोसा करना सीखें।",
    },
    22: {
        "title": "The Master Builder", "title_hi": "मास्टर निर्माता",
        "ruling_planet": "Rahu (Amplified)", "ruling_planet_hi": "राहु (प्रवर्धित)",
        "traits": ["Practical Visionary", "Organized", "Influential", "Ambitious", "Systematic"],
        "traits_hi": ["व्यावहारिक दूरदर्शी", "व्यवस्थित", "प्रभावशाली", "महत्वाकांक्षी", "क्रमबद्ध"],
        "career": "Large-scale Projects, Architecture, Social Reform, International Business",
        "career_hi": "बड़े पैमाने की परियोजनाएं, वास्तुकला, सामाजिक सुधार, अंतर्राष्ट्रीय व्यापार",
        "relationships": "Your mission may overshadow relationships. Find someone who shares your vision.",
        "relationships_hi": "आपका मिशन रिश्तों पर भारी पड़ सकता है। कोई ऐसा व्यक्ति खोजें जो आपकी दृष्टि साझा करता हो।",
        "health": "Nervous exhaustion from big projects. Balance work with rest.",
        "health_hi": "बड़ी परियोजनाओं से तंत्रिका संबंधी थकावट। काम को आराम के साथ संतुलित करें।",
        "lucky_colors": ["Blue", "Grey", "White"],
        "lucky_colors_hi": ["नीला", "भूरा", "सफेद"],
        "lucky_days": ["Thursday", "Saturday"],
        "lucky_days_hi": ["गुरुवार", "शनिवार"],
        "advice": "You are here to build what lasts. Think big but don't overwhelm yourself.",
        "advice_hi": "आप वह बनाने के लिए यहाँ हैं जो स्थायी हो। बड़ा सोचें लेकिन खुद को अभिभूत न होने दें।",
    },
    33: {
        "title": "The Master Teacher", "title_hi": "मास्टर शिक्षक",
        "ruling_planet": "Jupiter (Amplified)", "ruling_planet_hi": "गुरु (प्रवर्धित)",
        "traits": ["Selfless", "Healing", "Compassionate", "Wise", "Uplifting"],
        "traits_hi": ["निस्वार्थ", "उपचारक", "दयालु", "बुद्धिमान", "उत्थानकारी"],
        "career": "Healing, Teaching, Spiritual Guidance, Counseling, Humanitarian Work",
        "career_hi": "उपचार, शिक्षण, आध्यात्मिक मार्गदर्शन, परामर्श, मानवतावादी कार्य",
        "relationships": "Your love is unconditional. Set boundaries to avoid burnout.",
        "relationships_hi": "आपका प्रेम बिना शर्त है। बर्नआउट से बचने के लिए सीमाएं निर्धारित करें।",
        "health": "Emotional health tied to giving. Self-care is not selfish for you.",
        "health_hi": "देने से जुड़ा भावनात्मक स्वास्थ्य। आपके लिए स्वयं की देखभाल स्वार्थ नहीं है।",
        "lucky_colors": ["Pink", "White", "Light Blue"],
        "lucky_colors_hi": ["गुलाबी", "सफेद", "हल्का नीला"],
        "lucky_days": ["Thursday", "Friday"],
        "lucky_days_hi": ["गुरुवार", "शुक्रवार"],
        "advice": "Your purpose is to heal and teach. Remember you are also worthy of receiving love.",
        "advice_hi": "आपका उद्देश्य चंगा करना और सिखाना है। याद रखें कि आप भी प्यार पाने के योग्य हैं।",
    },
}


# ============================================================
# CAR/VEHICLE NUMEROLOGY
# ============================================================

VEHICLE_PREDICTIONS = {
    1: {
        "energy": "Leadership & Independence",
        "energy_hi": "नेतृत्व और स्वतंत्रता",
        "prediction": "Your vehicle carries the vibration of independence and authority. It suits those who drive alone or in leadership positions. The vehicle may attract attention and commands respect on the road.",
        "prediction_hi": "आपका वाहन स्वतंत्रता और अधिकार की कंपन वहन करता है। यह उन लोगों के लिए उपयुक्त है जो अकेले या नेतृत्व की स्थिति में गाड़ी चलाते हैं। वाहन ध्यान आकर्षित कर सकता है और सड़क पर सम्मान प्राप्त करता है।",
        "driving_style": "Confident, sometimes aggressive. You take charge on the road.",
        "driving_style_hi": "आत्मविश्वासी, कभी-कभी आक्रामक। आप सड़क पर नेतृत्व संभालते हैं।",
        "best_for": "Business owners, CEOs, politicians, independent professionals",
        "best_for_hi": "व्यापार मालिक, सीईओ, राजनेता, स्वतंत्र पेशेवर",
        "caution": "Avoid road rage. Your dominant energy may intimidate other drivers.",
        "caution_hi": "सड़क पर क्रोध से बचें। आपकी प्रभुत्वशाली ऊर्जा अन्य चालकों को डरा सकती है।",
        "lucky_directions": ["East", "North"],
        "lucky_directions_hi": ["पूर्व", "उत्तर"],
        "vehicle_color": ["Gold", "Orange", "Red", "White"],
        "vehicle_color_hi": ["सोना", "नारंगी", "लाल", "सफेद"],
    },
    2: {
        "energy": "Cooperation & Harmony",
        "energy_hi": "सहयोग और सामंजस्य",
        "prediction": "This vehicle vibration brings smooth, harmonious journeys. Ideal for family vehicles and those who often travel with passengers. Creates peaceful energy inside the car.",
        "prediction_hi": "यह वाहन कंपन सुचारू, सामंजस्यपूर्ण यात्राएं लाता है। पारिवारिक वाहनों और उन लोगों के लिए आदर्श जो अक्सर यात्रियों के साथ सफर करते हैं। कार के अंदर शांतिपूर्ण ऊर्जा बनाता है।",
        "driving_style": "Cautious and considerate. You yield and cooperate with other drivers.",
        "driving_style_hi": "सावधान और विचारशील। आप अन्य चालकों के साथ रास्ता देते और सहयोग करते हैं।",
        "best_for": "Families, diplomats, counselors, those seeking peaceful commutes",
        "best_for_hi": "परिवार, राजनयिक, परामर्शदाता, शांतिपूर्ण आवागमन चाहने वाले",
        "caution": "Don't be too passive. Stand your ground when necessary for safety.",
        "caution_hi": "बहुत निष्क्रिय न हों। सुरक्षा के लिए जरूरत पड़ने पर अपनी स्थिति पर कायम रहें।",
        "lucky_directions": ["West", "North-West"],
        "lucky_directions_hi": ["पश्चिम", "उत्तर-पश्चिम"],
        "vehicle_color": ["White", "Silver", "Cream"],
        "vehicle_color_hi": ["सफेद", "चांदी", "क्रीम"],
    },
    3: {
        "energy": "Creativity & Expression",
        "energy_hi": "रचनात्मकता और अभिव्यक्ति",
        "prediction": "A joyful, sociable vehicle vibration. Perfect for those in creative fields or who enjoy road trips with friends. The car becomes a social hub and conversation starter.",
        "prediction_hi": "एक आनंदमय, मिलनसार वाहन कंपन। रचनात्मक क्षेत्रों में काम करने वालों या दोस्तों के साथ रोड ट्रिप का आनंद लेने वालों के लिए बिल्कुल सही। कार एक सामाजिक केंद्र और बातचीत शुरू करने वाली बन जाती है।",
        "driving_style": "Enthusiastic, sometimes distracted by music or conversations.",
        "driving_style_hi": "उत्साही, कभी-कभी संगीत या बातचीत से विचलित।",
        "best_for": "Artists, writers, marketers, social butterflies, entertainers",
        "best_for_hi": "कलाकार, लेखक, विपणक, मिलनसार लोग, मनोरंजनकर्ता",
        "caution": "Focus on the road. Your love of variety may lead to distraction.",
        "caution_hi": "सड़क पर ध्यान दें। विविधता का आपका प्रेम विचलन का कारण बन सकता है।",
        "lucky_directions": ["East", "North-East"],
        "lucky_directions_hi": ["पूर्व", "उत्तर-पूर्व"],
        "vehicle_color": ["Yellow", "Orange", "Purple", "Bright Colors"],
        "vehicle_color_hi": ["पीला", "नारंगी", "बैंगनी", "चमकीले रंग"],
    },
    4: {
        "energy": "Stability & Reliability",
        "energy_hi": "स्थिरता और विश्वसनीयता",
        "prediction": "This is a practical, dependable vehicle number. The car will be reliable but may require regular maintenance. Journeys are generally safe and uneventful.",
        "prediction_hi": "यह एक व्यावहारिक, भरोसेमंद वाहन संख्या है। कार विश्वसनीय होगी लेकिन नियमित रखरखाव की आवश्यकता हो सकती है। यात्राएं आमतौर पर सुरक्षित और सामान्य होती हैं।",
        "driving_style": "Methodical and rule-following. You prefer familiar routes.",
        "driving_style_hi": "व्यवस्थित और नियम-पालक। आप परिचित मार्गों को प्राथमिकता देते हैं।",
        "best_for": "Engineers, accountants, those who value reliability over speed",
        "best_for_hi": "इंजीनियर, लेखाकार, वे जो गति से अधिक विश्वसनीयता को महत्व देते हैं",
        "caution": "Rigidity can cause stress. Be flexible with routes and timing.",
        "caution_hi": "कठोरता तनाव का कारण बन सकती है। मार्गों और समय के बारे में लचीले रहें।",
        "lucky_directions": ["South", "West"],
        "lucky_directions_hi": ["दक्षिण", "पश्चिम"],
        "vehicle_color": ["Blue", "Grey", "Black"],
        "vehicle_color_hi": ["नीला", "भूरा", "काला"],
    },
    5: {
        "energy": "Freedom & Adventure",
        "energy_hi": "स्वतंत्रता और साहस",
        "prediction": "The perfect vibration for travel lovers and adventure seekers. This vehicle loves highways and new destinations. Expect frequent short trips and spontaneous journeys.",
        "prediction_hi": "यात्रा प्रेमियों और साहसिक खोजियों के लिए सही कंपन। यह वाहन राजमार्गों और नए गंतव्यों को पसंद करता है। बार-बार छोटी यात्राओं और अनायास सफरों की अपेक्षा करें।",
        "driving_style": "Fast, adaptable, loves overtaking. You get restless in traffic.",
        "driving_style_hi": "तेज, अनुकूलनीय, ओवरटेक करना पसंद। आप ट्रैफिक में बेचैन हो जाते हैं।",
        "best_for": "Salespeople, travelers, journalists, those who love road trips",
        "best_for_hi": "विक्रेता, यात्री, पत्रकार, रोड ट्रिप प्रेमी",
        "caution": "Speeding tickets are likely. Slow down and enjoy the journey.",
        "caution_hi": "तेज गति के चालान की संभावना है। धीमे चलें और यात्रा का आनंद लें।",
        "lucky_directions": ["North", "East", "Any direction"],
        "lucky_directions_hi": ["उत्तर", "पूर्व", "कोई भी दिशा"],
        "vehicle_color": ["Green", "Grey", "Multi-color"],
        "vehicle_color_hi": ["हरा", "भूरा", "बहुरंगी"],
    },
    6: {
        "energy": "Love & Nurturing",
        "energy_hi": "प्रेम और पोषण",
        "prediction": "The ultimate family vehicle number. Creates a warm, protective environment. Ideal for parents, especially mothers. The car feels like a second home.",
        "prediction_hi": "सर्वोत्तम पारिवारिक वाहन संख्या। एक गर्म, सुरक्षात्मक वातावरण बनाती है। माता-पिता के लिए आदर्श, विशेष रूप से माताओं के लिए। कार एक दूसरे घर जैसी लगती है।",
        "driving_style": "Careful and protective, especially with children in the car.",
        "driving_style_hi": "सावधान और सुरक्षात्मक, विशेष रूप से बच्चों के साथ गाड़ी में।",
        "best_for": "Parents, teachers, healers, those in caregiving professions",
        "best_for_hi": "माता-पिता, शिक्षक, उपचारक, देखभाल करने वाले पेशों में लोग",
        "caution": "Over-protectiveness can cause anxiety. Trust in safety measures.",
        "caution_hi": "अत्यधिक सुरक्षा चिंता का कारण बन सकती है। सुरक्षा उपायों पर भरोसा रखें।",
        "lucky_directions": ["South-East", "South"],
        "lucky_directions_hi": ["दक्षिण-पूर्व", "दक्षिण"],
        "vehicle_color": ["Pink", "White", "Light Blue", "Silver"],
        "vehicle_color_hi": ["गुलाबी", "सफेद", "हल्का नीला", "चांदी"],
    },
    7: {
        "energy": "Wisdom & Introspection",
        "energy_hi": "ज्ञान और आत्मनिरीक्षण",
        "prediction": "A contemplative vehicle vibration. The car becomes a space for thinking and reflection. Ideal for long solo drives and commutes to spiritual or educational places.",
        "prediction_hi": "एक चिंतनशील वाहन कंपन। कार सोचने और चिंतन का स्थान बन जाती है। लंबी अकेली ड्राइव और आध्यात्मिक या शैक्षणिक स्थानों के लिए आवागमन के लिए आदर्श।",
        "driving_style": "Thoughtful, sometimes lost in thought. Plan routes carefully.",
        "driving_style_hi": "विचारशील, कभी-कभी सोच में खो जाते हैं। मार्गों की सावधानी से योजना बनाएं।",
        "best_for": "Researchers, spiritual seekers, philosophers, deep thinkers",
        "best_for_hi": "शोधकर्ता, आध्यात्मिक खोजी, दार्शनिक, गहरे चिंतक",
        "caution": "Daydreaming while driving is dangerous. Stay present on the road.",
        "caution_hi": "गाड़ी चलाते समय दिवास्वप्न देखना खतरनाक है। सड़क पर वर्तमान में रहें।",
        "lucky_directions": ["West", "North-West"],
        "lucky_directions_hi": ["पश्चिम", "उत्तर-पश्चिम"],
        "vehicle_color": ["Green", "White", "Silver"],
        "vehicle_color_hi": ["हरा", "सफेद", "चांदी"],
    },
    8: {
        "energy": "Power & Authority",
        "energy_hi": "शक्ति और अधिकार",
        "prediction": "This vehicle commands respect and may be expensive or luxury class. It attracts business opportunities and denotes success. Karma is at play - ethical driving brings rewards.",
        "prediction_hi": "यह वाहन सम्मान पाता है और महंगा या लक्जरी श्रेणी का हो सकता है। यह व्यापारिक अवसर आकर्षित करता है और सफलता दर्शाता है। कर्म कार्यरत है — नैतिक ड्राइविंग पुरस्कार लाती है।",
        "driving_style": "Assertive and commanding. Other drivers make way for you.",
        "driving_style_hi": "दृढ़ और आदेशात्मक। अन्य चालक आपके लिए रास्ता बनाते हैं।",
        "best_for": "Executives, lawyers, real estate professionals, business owners",
        "best_for_hi": "अधिकारी, वकील, रियल एस्टेट पेशेवर, व्यापार मालिक",
        "caution": "Karmic energy is strong. Drive ethically and avoid using power recklessly.",
        "caution_hi": "कार्मिक ऊर्जा प्रबल है। नैतिक रूप से ड्राइव करें और लापरवाही से शक्ति का उपयोग करने से बचें।",
        "lucky_directions": ["West", "South-West"],
        "lucky_directions_hi": ["पश्चिम", "दक्षिण-पश्चिम"],
        "vehicle_color": ["Black", "Dark Blue", "Dark Grey", "Burgundy"],
        "vehicle_color_hi": ["काला", "गहरा नीला", "गहरा भूरा", "बरगंडी"],
    },
    9: {
        "energy": "Courage & Compassion",
        "energy_hi": "साहस और करुणा",
        "prediction": "A vehicle with protective warrior energy. Good for emergency responders and those in helping professions. The car seems to 'protect' its occupants in challenging situations.",
        "prediction_hi": "सुरक्षात्मक योद्धा ऊर्जा वाला वाहन। आपातकालीन सेवाकर्मियों और सहायक व्यवसायों में लोगों के लिए अच्छा। कार चुनौतीपूर्ण परिस्थितियों में अपने सवारों की 'रक्षा' करती प्रतीत होती है।",
        "driving_style": "Bold and confident, sometimes impulsive. Quick reflexes.",
        "driving_style_hi": "साहसी और आत्मविश्वासी, कभी-कभी आवेगी। त्वरित प्रतिक्रियाएं।",
        "best_for": "Doctors, military personnel, social workers, athletes, emergency services",
        "best_for_hi": "डॉक्टर, सैन्य कर्मी, समाज सेवक, खिलाड़ी, आपातकालीन सेवाएं",
        "caution": "Impulsiveness can lead to accidents. Count to 10 before reacting.",
        "caution_hi": "आवेगशीलता दुर्घटनाओं का कारण बन सकती है। प्रतिक्रिया देने से पहले 10 तक गिनें।",
        "lucky_directions": ["South", "East"],
        "lucky_directions_hi": ["दक्षिण", "पूर्व"],
        "vehicle_color": ["Red", "Coral", "Pink", "Maroon"],
        "vehicle_color_hi": ["लाल", "मूंगा", "गुलाबी", "मैरून"],
    },
    # Master Numbers — not reduced, carry amplified vibration
    11: {
        "energy": "Intuition & Illumination (Master 11)",
        "energy_hi": "अंतर्ज्ञान और प्रकाश (मास्टर 11)",
        "prediction": "Your vehicle carries the rare Master 11 vibration — the number of the spiritual messenger. This is not an ordinary car; it amplifies intuition and attracts synchronistic events during travel. The owner often receives sudden insights or important news while in this vehicle.",
        "prediction_hi": "आपके वाहन में दुर्लभ मास्टर 11 कंपन है — आध्यात्मिक संदेशवाहक की संख्या। यह एक साधारण कार नहीं है; यह अंतर्ज्ञान को बढ़ाती है और यात्रा के दौरान समकालिक घटनाओं को आकर्षित करती है। मालिक को अक्सर इस वाहन में अचानक अंतर्दृष्टि या महत्वपूर्ण समाचार मिलते हैं।",
        "driving_style": "Highly alert and intuitive. You sense road conditions before they appear.",
        "driving_style_hi": "अत्यंत सतर्क और सहज। आप सड़क की स्थिति प्रकट होने से पहले ही भांप लेते हैं।",
        "best_for": "Spiritual leaders, counselors, healers, teachers, visionaries",
        "best_for_hi": "आध्यात्मिक नेता, परामर्शदाता, उपचारक, शिक्षक, दूरदर्शी",
        "caution": "Master 11 brings high nervous energy. Avoid driving when emotionally overwhelmed.",
        "caution_hi": "मास्टर 11 उच्च तंत्रिका ऊर्जा लाता है। भावनात्मक रूप से अभिभूत होने पर गाड़ी चलाने से बचें।",
        "lucky_directions": ["North", "North-East"],
        "lucky_directions_hi": ["उत्तर", "उत्तर-पूर्व"],
        "vehicle_color": ["Silver", "White", "Cream", "Light Purple"],
        "vehicle_color_hi": ["चांदी", "सफेद", "क्रीम", "हल्का बैंगनी"],
    },
    22: {
        "energy": "Master Builder & Vision (Master 22)",
        "energy_hi": "मास्टर निर्माता और दृष्टि (मास्टर 22)",
        "prediction": "The most powerful vehicle vibration in numerology — Master 22 is the Master Builder. This vehicle is suited for those executing large-scale plans. It brings stability, discipline, and the capacity to turn dreams into reality on every journey.",
        "prediction_hi": "अंकशास्त्र में सबसे शक्तिशाली वाहन कंपन — मास्टर 22 है मास्टर बिल्डर। यह वाहन बड़े पैमाने पर योजनाएं क्रियान्वित करने वालों के लिए उपयुक्त है। यह प्रत्येक यात्रा में स्थिरता, अनुशासन और सपनों को वास्तविकता में बदलने की क्षमता लाता है।",
        "driving_style": "Precise, disciplined, and strategic. You plan routes well in advance.",
        "driving_style_hi": "सटीक, अनुशासित और रणनीतिक। आप मार्गों की बहुत पहले से योजना बनाते हैं।",
        "best_for": "Architects, engineers, entrepreneurs, government officials, project leaders",
        "best_for_hi": "वास्तुकार, इंजीनियर, उद्यमी, सरकारी अधिकारी, परियोजना नेता",
        "caution": "Perfectionism may cause stress. Accept that roads are unpredictable.",
        "caution_hi": "पूर्णतावाद तनाव का कारण बन सकता है। स्वीकार करें कि सड़कें अप्रत्याशित होती हैं।",
        "lucky_directions": ["South", "South-West"],
        "lucky_directions_hi": ["दक्षिण", "दक्षिण-पश्चिम"],
        "vehicle_color": ["Dark Blue", "Charcoal", "Forest Green", "Navy"],
        "vehicle_color_hi": ["गहरा नीला", "चारकोल", "गहरा हरा", "नेवी"],
    },
    33: {
        "energy": "Master Teacher & Universal Love (Master 33)",
        "energy_hi": "मास्टर शिक्षक और सार्वभौमिक प्रेम (मास्टर 33)",
        "prediction": "The rarest vehicle vibration — Master 33, the Master Teacher. This vehicle radiates compassion and healing energy wherever it travels. It is often used in service of others — transporting the ill, elderly, or those in need. The vehicle itself seems to offer comfort and calm.",
        "prediction_hi": "सबसे दुर्लभ वाहन कंपन — मास्टर 33, मास्टर शिक्षक। यह वाहन जहाँ भी जाता है करुणा और उपचार ऊर्जा विकीर्ण करता है। इसे अक्सर दूसरों की सेवा में उपयोग किया जाता है — बीमारों, बुजुर्गों या जरूरतमंदों को ले जाने के लिए। वाहन स्वयं आराम और शांति प्रदान करता प्रतीत होता है।",
        "driving_style": "Nurturing and protective. You prioritize passengers' comfort above all.",
        "driving_style_hi": "पोषणकारी और सुरक्षात्मक। आप सबसे ऊपर यात्रियों के आराम को प्राथमिकता देते हैं।",
        "best_for": "Doctors, social workers, spiritual teachers, humanitarian workers, healers",
        "best_for_hi": "डॉक्टर, समाज सेवक, आध्यात्मिक शिक्षक, मानवतावादी कार्यकर्ता, उपचारक",
        "caution": "You may neglect your own needs for others. Remember self-care applies to the driver too.",
        "caution_hi": "आप दूसरों के लिए अपनी जरूरतों की उपेक्षा कर सकते हैं। याद रखें, स्व-देखभाल चालक पर भी लागू होती है।",
        "lucky_directions": ["All directions — Master 33 is universally auspicious"],
        "lucky_directions_hi": ["सभी दिशाएं — मास्टर 33 सार्वभौमिक रूप से शुभ है"],
        "vehicle_color": ["Gold", "Purple", "Royal Blue", "White"],
        "vehicle_color_hi": ["सोना", "बैंगनी", "रॉयल ब्लू", "सफेद"],
    },
}


# ============================================================
# HOUSE NUMBER NUMEROLOGY
# ============================================================

HOUSE_PREDICTIONS = {
    1: {
        "energy": "Independence & New Beginnings",
        "energy_hi": "स्वतंत्रता और नई शुरुआत",
        "prediction": "This home carries strong, independent energy. It's perfect for self-starters, entrepreneurs, and those building new lives. The house fosters ambition and leadership.",
        "prediction_hi": "इस घर में मजबूत, स्वतंत्र ऊर्जा है। यह स्वयं से शुरुआत करने वालों, उद्यमियों और नया जीवन बनाने वालों के लिए बिल्कुल सही है। घर महत्वाकांक्षा और नेतृत्व को बढ़ावा देता है।",
        "best_for": "Entrepreneurs, leaders, independent professionals, singles seeking self-discovery",
        "best_for_hi": "उद्यमी, नेता, स्वतंत्र पेशेवर, आत्म-खोज करने वाले एकल लोग",
        "family_life": "Members tend to be self-reliant. Everyone needs their own space. Respect individuality.",
        "family_life_hi": "सदस्य आत्मनिर्भर होते हैं। सबको अपनी जगह चाहिए। व्यक्तित्व का सम्मान करें।",
        "career_impact": "Excellent for home offices. Business ventures started here have strong potential.",
        "career_impact_hi": "होम ऑफिस के लिए उत्कृष्ट। यहाँ शुरू किए गए व्यापारिक उद्यमों में मजबूत क्षमता है।",
        "relationships": "Partners must maintain independence. Co-dependency struggles may arise.",
        "relationships_hi": "साझेदारों को स्वतंत्रता बनाए रखनी होगी। सह-निर्भरता के संघर्ष उत्पन्न हो सकते हैं।",
        "health": "Good vitality but watch for stress-related issues. Create spaces for relaxation.",
        "health_hi": "अच्छी जीवन शक्ति लेकिन तनाव संबंधी समस्याओं पर ध्यान दें। विश्राम के लिए स्थान बनाएं।",
        "vastu_tip": "Keep the East direction open and well-lit. Place a red object near the entrance.",
        "vastu_tip_hi": "पूर्व दिशा को खुला और अच्छी तरह से रोशन रखें। प्रवेश द्वार के पास लाल वस्तु रखें।",
        "lucky_colors": ["Red", "Orange", "Gold", "Yellow"],
        "lucky_colors_hi": ["लाल", "नारंगी", "सोना", "पीला"],
        "remedies": ["Keep a water feature in North", "Place Sun symbol in East", "Avoid clutter in center"],
        "remedies_hi": ["उत्तर में जल तत्व रखें", "पूर्व में सूर्य प्रतीक रखें", "केंद्र में अव्यवस्था से बचें"],
    },
    2: {
        "energy": "Harmony & Partnership",
        "energy_hi": "सामंजस्य और साझेदारी",
        "prediction": "A nurturing, peaceful home perfect for couples and families. The energy here promotes cooperation, emotional bonding, and diplomatic resolutions to conflicts.",
        "prediction_hi": "जोड़ों और परिवारों के लिए उपयुक्त पोषणकारी, शांतिपूर्ण घर। यहाँ की ऊर्जा सहयोग, भावनात्मक बंधन और संघर्षों के राजनयिक समाधान को बढ़ावा देती है।",
        "best_for": "Couples, newlyweds, families with young children, diplomats, counselors",
        "best_for_hi": "जोड़े, नवविवाहित, छोटे बच्चों वाले परिवार, राजनयिक, परामर्शदाता",
        "family_life": "Strong emotional bonds. The home becomes a sanctuary. Sensitive to moods.",
        "family_life_hi": "मजबूत भावनात्मक बंधन। घर एक अभयारण्य बन जाता है। मनोदशाओं के प्रति संवेदनशील।",
        "career_impact": "Best for collaborative work from home. Partnerships formed here are blessed.",
        "career_impact_hi": "घर से सहयोगी कार्य के लिए सर्वोत्तम। यहाँ बनी साझेदारियां आशीर्वादित होती हैं।",
        "relationships": "Deepens romantic bonds. Brings peace to troubled relationships over time.",
        "relationships_hi": "रोमांटिक बंधन गहरे होते हैं। समय के साथ परेशान रिश्तों में शांति आती है।",
        "health": "Emotional well-being affects physical health. Create a peaceful bedroom environment.",
        "health_hi": "भावनात्मक कल्याण शारीरिक स्वास्थ्य को प्रभावित करता है। शांतिपूर्ण शयनकक्ष वातावरण बनाएं।",
        "vastu_tip": "North-West is favorable. Keep pairs of objects for harmony. White flowers help.",
        "vastu_tip_hi": "उत्तर-पश्चिम अनुकूल है। सामंजस्य के लिए वस्तुओं के जोड़े रखें। सफेद फूल सहायक हैं।",
        "lucky_colors": ["White", "Silver", "Cream", "Light Green"],
        "lucky_colors_hi": ["सफेद", "चांदी", "क्रीम", "हल्का हरा"],
        "remedies": ["Place two white candles in living room", "Keep North-West clean", "Moonstone in North-East"],
        "remedies_hi": ["बैठक में दो सफेद मोमबत्तियां रखें", "उत्तर-पश्चिम साफ रखें", "उत्तर-पूर्व में मूनस्टोन"],
    },
    3: {
        "energy": "Joy & Creativity",
        "energy_hi": "आनंद और रचनात्मकता",
        "prediction": "A vibrant, social home filled with laughter and creativity. Perfect for artists, writers, and social butterflies. The house loves gatherings and celebrations.",
        "prediction_hi": "हँसी और रचनात्मकता से भरा जीवंत, सामाजिक घर। कलाकारों, लेखकों और मिलनसार लोगों के लिए बिल्कुल सही। घर सभाओं और उत्सवों को पसंद करता है।",
        "best_for": "Artists, writers, entertainers, families with children, social hosts",
        "best_for_hi": "कलाकार, लेखक, मनोरंजनकर्ता, बच्चों वाले परिवार, सामाजिक मेजबान",
        "family_life": "Lively, sometimes chaotic. Children thrive here. Lots of activities and projects.",
        "family_life_hi": "जीवंत, कभी-कभी अव्यवस्थित। बच्चे यहाँ फलते-फूलते हैं। बहुत सी गतिविधियां और परियोजनाएं।",
        "career_impact": "Excellent for creative professionals. Ideas flow abundantly in this space.",
        "career_impact_hi": "रचनात्मक पेशेवरों के लिए उत्कृष्ट। इस स्थान में विचार प्रचुर मात्रा में आते हैं।",
        "relationships": "Fun and romance, but depth may need conscious effort. Keep communication open.",
        "relationships_hi": "मजेदार और रोमांटिक, लेकिन गहराई के लिए सचेत प्रयास जरूरी। संचार खुला रखें।",
        "health": "Mental stimulation is high. Ensure adequate rest and avoid over-commitment.",
        "health_hi": "मानसिक उत्तेजना अधिक है। पर्याप्त आराम सुनिश्चित करें और अत्यधिक प्रतिबद्धता से बचें।",
        "vastu_tip": "East and North-East are powerful directions. Display artwork and creative pieces.",
        "vastu_tip_hi": "पूर्व और उत्तर-पूर्व शक्तिशाली दिशाएं हैं। कलाकृतियां और रचनात्मक टुकड़े प्रदर्शित करें।",
        "lucky_colors": ["Yellow", "Orange", "Purple", "Gold"],
        "lucky_colors_hi": ["पीला", "नारंगी", "बैंगनी", "सोना"],
        "remedies": ["Place yellow flowers in East", "Keep space for creative work", "Wind chimes in North"],
        "remedies_hi": ["पूर्व में पीले फूल रखें", "रचनात्मक कार्य के लिए जगह बनाएं", "उत्तर में विंड चाइम"],
    },
    4: {
        "energy": "Stability & Foundation",
        "energy_hi": "स्थिरता और नींव",
        "prediction": "A solid, secure home that provides grounding and structure. Perfect for building long-term security. The energy here is reliable but can resist change.",
        "prediction_hi": "एक ठोस, सुरक्षित घर जो स्थिरता और संरचना प्रदान करता है। दीर्घकालिक सुरक्षा बनाने के लिए बिल्कुल सही। यहाँ की ऊर्जा विश्वसनीय है लेकिन परिवर्तन का प्रतिरोध कर सकती है।",
        "best_for": "Those seeking stability, retirees, accountants, engineers, long-term planners",
        "best_for_hi": "स्थिरता चाहने वाले, सेवानिवृत्त, लेखाकार, इंजीनियर, दीर्घकालिक योजनाकार",
        "family_life": "Structured routines benefit everyone. Traditional values are honored here.",
        "family_life_hi": "संरचित दिनचर्या सबको फायदा देती है। यहाँ पारंपरिक मूल्यों का सम्मान होता है।",
        "career_impact": "Slow but steady progress. Excellent for detailed, methodical work.",
        "career_impact_hi": "धीमी लेकिन स्थिर प्रगति। विस्तृत, पद्धतिगत कार्य के लिए उत्कृष्ट।",
        "relationships": "Loyalty and commitment are strong. Changes in relationship status are resisted.",
        "relationships_hi": "वफादारी और प्रतिबद्धता मजबूत है। रिश्ते की स्थिति में बदलाव का विरोध होता है।",
        "health": "Chronic conditions may stabilize. Focus on routine health maintenance.",
        "health_hi": "पुरानी स्थितियां स्थिर हो सकती हैं। नियमित स्वास्थ्य रखरखाव पर ध्यान दें।",
        "vastu_tip": "South and West directions are favorable. Heavy furniture can be placed here.",
        "vastu_tip_hi": "दक्षिण और पश्चिम दिशाएं अनुकूल हैं। यहाँ भारी फर्नीचर रखा जा सकता है।",
        "lucky_colors": ["Blue", "Grey", "Brown", "Green"],
        "lucky_colors_hi": ["नीला", "स्लेटी", "भूरा", "हरा"],
        "remedies": ["Square-shaped objects stabilize energy", "Plants in East bring growth", "Avoid irregular shapes"],
        "remedies_hi": ["वर्गाकार वस्तुएं ऊर्जा को स्थिर करती हैं", "पूर्व में पौधे विकास लाते हैं", "अनियमित आकारों से बचें"],
    },
    5: {
        "energy": "Change & Freedom",
        "energy_hi": "परिवर्तन और स्वतंत्रता",
        "prediction": "A dynamic, ever-changing home environment. Perfect for those who love variety and travel. The house rarely stays the same for long - renovations, moves, or frequent guests.",
        "prediction_hi": "एक गतिशील, बदलते रहने वाला घर का वातावरण। विविधता और यात्रा पसंद करने वालों के लिए बिल्कुल सही। घर लंबे समय तक एक जैसा नहीं रहता — नवीकरण, स्थानांतरण या बारंबार अतिथि।",
        "best_for": "Travelers, salespeople, young professionals, those in transition, journalists",
        "best_for_hi": "यात्री, विक्रेता, युवा पेशेवर, परिवर्तन में लोग, पत्रकार",
        "family_life": "Flexible and adaptable. Good for families who move frequently or love variety.",
        "family_life_hi": "लचीला और अनुकूलनीय। बार-बार स्थानांतरित होने वाले या विविधता पसंद करने वाले परिवारों के लिए अच्छा।",
        "career_impact": "Multiple income streams possible. Great for communication-based businesses.",
        "career_impact_hi": "आय के कई स्रोत संभव। संचार-आधारित व्यवसायों के लिए बढ़िया।",
        "relationships": "Exciting but unstable. Partners must embrace change and variety.",
        "relationships_hi": "रोमांचक लेकिन अस्थिर। साझेदारों को परिवर्तन और विविधता को अपनाना होगा।",
        "health": "Nervous energy is high. Meditation and grounding practices are essential.",
        "health_hi": "तंत्रिका ऊर्जा अधिक है। ध्यान और भूमि से जुड़ने की प्रथाएं आवश्यक हैं।",
        "vastu_tip": "Center of home should be open. North is favorable for opportunities.",
        "vastu_tip_hi": "घर का केंद्र खुला होना चाहिए। उत्तर दिशा अवसरों के लिए अनुकूल है।",
        "lucky_colors": ["Green", "Turquoise", "Light Grey", "White"],
        "lucky_colors_hi": ["हरा", "फ़िरोज़ा", "हल्का स्लेटी", "सफेद"],
        "remedies": ["Keep center of house empty", "Green plants in East", "Mercury symbol in North"],
        "remedies_hi": ["घर का केंद्र खाली रखें", "पूर्व में हरे पौधे", "उत्तर में बुध प्रतीक"],
    },
    6: {
        "energy": "Love & Responsibility",
        "energy_hi": "प्रेम और जिम्मेदारी",
        "prediction": "The ultimate family home. Nurturing, beautiful, and filled with love. Perfect for raising children and creating a beautiful living space. Strong maternal energy.",
        "prediction_hi": "परम पारिवारिक घर। पोषणकारी, सुंदर और प्रेम से भरा। बच्चों को पालने और सुंदर रहने की जगह बनाने के लिए बिल्कुल सही। मातृशक्ति की प्रबल ऊर्जा।",
        "best_for": "Families, parents, teachers, healers, artists, interior designers",
        "best_for_hi": "परिवार, माता-पिता, शिक्षक, उपचारक, कलाकार, इंटीरियर डिजाइनर",
        "family_life": "Warm and nurturing. Children feel secure. The home is the heart of family life.",
        "family_life_hi": "गर्म और पोषणकारी। बच्चे सुरक्षित महसूस करते हैं। घर पारिवारिक जीवन का केंद्र है।",
        "career_impact": "Good for caregiving professions, teaching, healing, and artistic work from home.",
        "career_impact_hi": "देखभाल पेशों, शिक्षण, उपचार और घर से कलात्मक कार्य के लिए अच्छा।",
        "relationships": "Deep love and commitment. Marriage and family life are blessed here.",
        "relationships_hi": "गहरा प्रेम और प्रतिबद्धता। यहाँ विवाह और पारिवारिक जीवन आशीर्वादित है।",
        "health": "Generally good for family health. Pay attention to women's health in particular.",
        "health_hi": "सामान्यतः पारिवारिक स्वास्थ्य के लिए अच्छा। महिलाओं के स्वास्थ्य पर विशेष ध्यान दें।",
        "vastu_tip": "South-East is favorable. Create beautiful, comfortable spaces. Venus energy here.",
        "vastu_tip_hi": "दक्षिण-पूर्व अनुकूल है। सुंदर, आरामदायक स्थान बनाएं। यहाँ शुक्र की ऊर्जा है।",
        "lucky_colors": ["Pink", "White", "Light Blue", "Pastels"],
        "lucky_colors_hi": ["गुलाबी", "सफेद", "हल्का नीला", "पेस्टल रंग"],
        "remedies": ["Pink roses in South-East", "Comfortable seating for family", "Balance of 5 elements"],
        "remedies_hi": ["दक्षिण-पूर्व में गुलाबी गुलाब", "परिवार के लिए आरामदायक बैठने की व्यवस्था", "5 तत्वों का संतुलन"],
    },
    7: {
        "energy": "Contemplation & Wisdom",
        "energy_hi": "चिंतन और ज्ञान",
        "prediction": "A peaceful, spiritual sanctuary perfect for study, meditation, and introspection. The energy here turns inward, making it ideal for seekers of wisdom.",
        "prediction_hi": "अध्ययन, ध्यान और आत्मनिरीक्षण के लिए बिल्कुल सही शांतिपूर्ण, आध्यात्मिक अभयारण्य। यहाँ की ऊर्जा अंतर्मुखी होती है, जो ज्ञान के साधकों के लिए आदर्श है।",
        "best_for": "Spiritual seekers, researchers, writers, scientists, those needing solitude",
        "best_for_hi": "आध्यात्मिक साधक, शोधकर्ता, लेखक, वैज्ञानिक, एकांत की आवश्यकता वाले",
        "family_life": "Quiet and respectful. Members value privacy. Deep conversations happen here.",
        "family_life_hi": "शांत और सम्मानजनक। सदस्य गोपनीयता को महत्व देते हैं। यहाँ गहरी बातचीत होती है।",
        "career_impact": "Excellent for research, writing, and spiritual teaching from home.",
        "career_impact_hi": "शोध, लेखन और घर से आध्यात्मिक शिक्षण के लिए उत्कृष्ट।",
        "relationships": "Soulful connections form here. Superficial relationships don't last in this energy.",
        "relationships_hi": "यहाँ आत्मिक संबंध बनते हैं। इस ऊर्जा में सतही रिश्ते नहीं टिकते।",
        "health": "Mental and spiritual health improve. Physical exercise may need conscious effort.",
        "health_hi": "मानसिक और आध्यात्मिक स्वास्थ्य में सुधार होता है। शारीरिक व्यायाम के लिए सचेत प्रयास जरूरी।",
        "vastu_tip": "South-West provides grounding. Create a dedicated meditation or study space.",
        "vastu_tip_hi": "दक्षिण-पश्चिम स्थिरता प्रदान करता है। समर्पित ध्यान या अध्ययन स्थान बनाएं।",
        "lucky_colors": ["Green", "White", "Purple", "Silver"],
        "lucky_colors_hi": ["हरा", "सफेद", "बैंगनी", "चांदी"],
        "remedies": ["Study room in West or South-West", "Keep North-East clean and spiritual", "Books enhance energy"],
        "remedies_hi": ["पश्चिम या दक्षिण-पश्चिम में अध्ययन कक्ष", "उत्तर-पूर्व साफ और आध्यात्मिक रखें", "किताबें ऊर्जा बढ़ाती हैं"],
    },
    8: {
        "energy": "Abundance & Authority",
        "energy_hi": "समृद्धि और अधिकार",
        "prediction": "A powerful home that attracts wealth and success. The energy here demands discipline and rewards hard work. Karma operates strongly - ethical living brings rewards.",
        "prediction_hi": "एक शक्तिशाली घर जो धन और सफलता को आकर्षित करता है। यहाँ की ऊर्जा अनुशासन की मांग करती है और कड़ी मेहनत को पुरस्कृत करती है। कर्म मजबूती से काम करता है — नैतिक जीवन पुरस्कार लाता है।",
        "best_for": "Business owners, executives, those seeking material success, lawyers",
        "best_for_hi": "व्यापार मालिक, कार्यकारी, भौतिक सफलता चाहने वाले, वकील",
        "family_life": "Authoritative structure. Respect is important. Traditional roles may be emphasized.",
        "family_life_hi": "सत्तावादी संरचना। सम्मान महत्वपूर्ण है। पारंपरिक भूमिकाओं पर जोर दिया जा सकता है।",
        "career_impact": "Exceptional for business success. Home office can become very prosperous.",
        "career_impact_hi": "व्यावसायिक सफलता के लिए असाधारण। होम ऑफिस बहुत समृद्ध हो सकता है।",
        "relationships": "Power dynamics may emerge. Partners should be equals to avoid conflicts.",
        "relationships_hi": "शक्ति की गतिशीलता उभर सकती है। संघर्ष से बचने के लिए साझेदार बराबर होने चाहिए।",
        "health": "Stress from overwork is the main concern. Balance material pursuits with rest.",
        "health_hi": "अत्यधिक काम का तनाव मुख्य चिंता है। भौतिक प्रयासों को आराम के साथ संतुलित करें।",
        "vastu_tip": "South-West is most powerful direction. Keep this area heavy and stable.",
        "vastu_tip_hi": "दक्षिण-पश्चिम सबसे शक्तिशाली दिशा है। इस क्षेत्र को भारी और स्थिर रखें।",
        "lucky_colors": ["Black", "Dark Blue", "Dark Grey", "Burgundy"],
        "lucky_colors_hi": ["काला", "गहरा नीला", "गहरा स्लेटी", "बरगंडी"],
        "remedies": ["Heavy furniture in South-West", "Blue stone or crystal", "Avoid South-West cuts"],
        "remedies_hi": ["दक्षिण-पश्चिम में भारी फर्नीचर", "नीला पत्थर या क्रिस्टल", "दक्षिण-पश्चिम के कटान से बचें"],
    },
    9: {
        "energy": "Completion & Humanitarianism",
        "energy_hi": "पूर्णता और मानवतावाद",
        "prediction": "A home of completion, ideal for ending old cycles and preparing for new ones. Compassionate energy that welcomes all. Perfect for those in service professions.",
        "prediction_hi": "पूर्णता का घर, पुराने चक्रों को समाप्त करने और नए की तैयारी के लिए आदर्श। करुणामयी ऊर्जा जो सबका स्वागत करती है। सेवा पेशों में लोगों के लिए बिल्कुल सही।",
        "best_for": "Humanitarians, doctors, social workers, those completing life phases, elders",
        "best_for_hi": "मानवतावादी, डॉक्टर, समाज सेवक, जीवन चरणों को पूरा करने वाले, बुजुर्ग",
        "family_life": "Inclusive and welcoming. Extended family and friends often gather here.",
        "family_life_hi": "समावेशी और स्वागत करने वाला। विस्तारित परिवार और दोस्त अक्सर यहाँ इकट्ठा होते हैं।",
        "career_impact": "Good for service-oriented work from home. Teaching and healing thrive.",
        "career_impact_hi": "घर से सेवा-उन्मुख कार्य के लिए अच्छा। शिक्षण और उपचार फलता-फूलता है।",
        "relationships": "Universal love dominates. Romantic relationships need conscious cultivation.",
        "relationships_hi": "सार्वभौमिक प्रेम हावी है। रोमांटिक रिश्तों को सचेत रूप से पोषित करना जरूरी है।",
        "health": "Healing energy is strong. Good for recovery from illness. Physical exercise needed.",
        "health_hi": "उपचार ऊर्जा मजबूत है। बीमारी से उबरने के लिए अच्छा। शारीरिक व्यायाम जरूरी है।",
        "vastu_tip": "South is favorable. The home should feel open and welcoming to all.",
        "vastu_tip_hi": "दक्षिण अनुकूल है। घर सबके लिए खुला और स्वागत करने वाला महसूस होना चाहिए।",
        "lucky_colors": ["Red", "Coral", "Pink", "Maroon"],
        "lucky_colors_hi": ["लाल", "मूंगा", "गुलाबी", "मैरून"],
        "remedies": ["Red accents in South", "Welcome guests warmly", "Donation corner in North-East"],
        "remedies_hi": ["दक्षिण में लाल उच्चारण", "अतिथियों का गर्मजोशी से स्वागत करें", "उत्तर-पूर्व में दान कोना"],
    },
}


# Mobile number vibration predictions keyed by reduced number
MOBILE_PREDICTIONS = {
    1: {
        "prediction": (
            "Your mobile number carries the vibration of leadership and independence. "
            "This number attracts opportunities for new beginnings, self-employment, and pioneering ventures. "
            "Calls and messages received on this number often bring proposals, business leads, and invitations to take charge."
        ),
        "lucky_qualities": ["Leadership", "Independence", "Ambition", "Originality", "Confidence"],
        "challenges": ["Stubbornness", "Isolation", "Over-dominance"],
        "best_for": "Entrepreneurs, CEOs, freelancers, and anyone starting a new venture",
        "compatibility_numbers": [1, 3, 5, 9],
    },
    2: {
        "prediction": (
            "Your mobile number resonates with diplomacy and partnership. "
            "This vibration attracts cooperation, emotional connections, and harmonious relationships. "
            "You may notice an increase in calls related to collaboration, mediation, and heartfelt conversations."
        ),
        "lucky_qualities": ["Diplomacy", "Sensitivity", "Cooperation", "Intuition", "Peacemaking"],
        "challenges": ["Indecisiveness", "Over-sensitivity", "Dependency"],
        "best_for": "Counselors, mediators, artists, and those seeking deep personal relationships",
        "compatibility_numbers": [2, 4, 6, 8],
    },
    3: {
        "prediction": (
            "Your mobile number vibrates with creativity and self-expression. "
            "This number attracts social invitations, artistic opportunities, and joyful communication. "
            "Expect lively conversations, networking calls, and creative collaborations through this number."
        ),
        "lucky_qualities": ["Creativity", "Joy", "Communication", "Optimism", "Social magnetism"],
        "challenges": ["Scattered energy", "Superficiality", "Overspending"],
        "best_for": "Writers, speakers, marketers, social media professionals, and entertainers",
        "compatibility_numbers": [1, 3, 5, 9],
    },
    4: {
        "prediction": (
            "Your mobile number carries the vibration of stability and hard work. "
            "This number attracts steady opportunities, reliable contacts, and structured progress. "
            "Calls received tend to involve practical matters, contracts, and long-term commitments."
        ),
        "lucky_qualities": ["Discipline", "Reliability", "Organization", "Patience", "Loyalty"],
        "challenges": ["Rigidity", "Overthinking", "Resistance to change"],
        "best_for": "Accountants, engineers, project managers, and anyone building long-term foundations",
        "compatibility_numbers": [2, 4, 6, 8],
    },
    5: {
        "prediction": (
            "Your mobile number vibrates with freedom and adventure. "
            "This number attracts exciting news, travel opportunities, and dynamic change. "
            "You may receive unexpected calls that open doors to new experiences and diverse connections."
        ),
        "lucky_qualities": ["Versatility", "Adventure", "Freedom", "Resourcefulness", "Curiosity"],
        "challenges": ["Restlessness", "Impulsiveness", "Lack of commitment"],
        "best_for": "Travelers, sales professionals, journalists, and those in dynamic industries",
        "compatibility_numbers": [1, 3, 5, 7],
    },
    6: {
        "prediction": (
            "Your mobile number resonates with love, family, and responsibility. "
            "This vibration attracts nurturing relationships, domestic harmony, and community connections. "
            "Calls often involve family matters, caregiving, and opportunities to help others."
        ),
        "lucky_qualities": ["Compassion", "Responsibility", "Harmony", "Nurturing", "Aesthetics"],
        "challenges": ["Over-sacrifice", "Worry", "Controlling tendencies"],
        "best_for": "Teachers, healers, interior designers, and family-oriented professionals",
        "compatibility_numbers": [2, 4, 6, 9],
    },
    7: {
        "prediction": (
            "Your mobile number carries the vibration of wisdom and spiritual seeking. "
            "This number attracts thoughtful conversations, research opportunities, and introspective connections. "
            "Calls may bring intellectual stimulation and invitations for deep, meaningful exchanges."
        ),
        "lucky_qualities": ["Wisdom", "Intuition", "Analysis", "Spiritual depth", "Mystery"],
        "challenges": ["Isolation", "Suspicion", "Emotional detachment"],
        "best_for": "Researchers, spiritual practitioners, analysts, and philosophers",
        "compatibility_numbers": [3, 5, 7, 9],
    },
    8: {
        "prediction": (
            "Your mobile number vibrates with abundance and karmic power. "
            "This number attracts financial opportunities, authority, and material success. "
            "Expect calls related to business deals, investments, and positions of influence."
        ),
        "lucky_qualities": ["Authority", "Abundance", "Business acumen", "Determination", "Manifestation"],
        "challenges": ["Workaholism", "Materialism", "Power struggles"],
        "best_for": "Business owners, investors, bankers, and corporate executives",
        "compatibility_numbers": [2, 4, 6, 8],
    },
    9: {
        "prediction": (
            "Your mobile number resonates with humanitarianism and universal love. "
            "This vibration attracts compassionate connections, global opportunities, and service-oriented calls. "
            "You may receive requests for guidance, charity, and cross-cultural collaboration."
        ),
        "lucky_qualities": ["Compassion", "Generosity", "Global vision", "Idealism", "Completion"],
        "challenges": ["Over-idealism", "Emotional burnout", "Difficulty letting go"],
        "best_for": "NGO workers, doctors, teachers, and anyone in humanitarian service",
        "compatibility_numbers": [1, 3, 6, 9],
    },
    11: {
        "prediction": (
            "Master Number 11 — Your mobile number carries the vibration of spiritual illumination and visionary insight. "
            "This is a highly charged number that attracts intuitive messages, inspired connections, and opportunities "
            "for spiritual leadership. Calls may feel synchronistic and deeply meaningful."
        ),
        "lucky_qualities": ["Visionary insight", "Spiritual awareness", "Inspiration", "Charisma", "Enlightenment"],
        "challenges": ["Nervous tension", "Hypersensitivity", "Anxiety"],
        "best_for": "Spiritual leaders, artists, innovators, and visionary entrepreneurs",
        "compatibility_numbers": [2, 4, 6, 11, 22],
    },
    22: {
        "prediction": (
            "Master Number 22 — Your mobile number vibrates with the power of the Master Builder. "
            "This extraordinary number attracts large-scale opportunities, influential contacts, and projects "
            "that can shape communities. Calls received often involve ambitious plans and transformative partnerships."
        ),
        "lucky_qualities": ["Master building", "Practical idealism", "Global impact", "Discipline", "Vision"],
        "challenges": ["Overwhelm", "Perfectionism", "Fear of failure"],
        "best_for": "Architects, city planners, large-scale project leaders, and social reformers",
        "compatibility_numbers": [4, 6, 8, 11, 22],
    },
    33: {
        "prediction": (
            "Master Number 33 — Your mobile number carries the vibration of the Master Teacher. "
            "This sacred number attracts healing relationships, teaching opportunities, and calls for selfless service. "
            "Conversations through this number tend to uplift, heal, and inspire both caller and receiver."
        ),
        "lucky_qualities": ["Healing", "Selfless service", "Master teaching", "Unconditional love", "Upliftment"],
        "challenges": ["Self-sacrifice", "Emotional overwhelm", "Martyrdom"],
        "best_for": "Healers, spiritual teachers, counselors, and humanitarian leaders",
        "compatibility_numbers": [6, 9, 11, 22, 33],
    },
}


# ============================================================
# Mobile Numerology — Comprehensive Analysis (Batraa Reference)
# ============================================================

# Planetary friendship/enemy table
# Key = digit, value = dict with 'friends' and 'enemies' sets
PLANET_RELATIONSHIPS = {
    1: {"friends": {2, 3, 9}, "enemies": {4, 6, 8}},       # Sun
    2: {"friends": {1, 3}, "enemies": {4, 5, 8}},           # Moon
    3: {"friends": {1, 2, 9}, "enemies": {4, 5, 6, 8}},     # Jupiter
    4: {"friends": {5, 6, 7}, "enemies": {1, 2, 8, 9}},     # Rahu
    5: {"friends": {4, 6}, "enemies": {2, 3}},               # Mercury
    6: {"friends": {4, 5, 7, 8}, "enemies": {1, 3}},        # Venus
    7: {"friends": {4, 6}, "enemies": {1, 2, 8, 9}},        # Ketu
    8: {"friends": {5, 6}, "enemies": {1, 2, 4, 7, 9}},     # Saturn
    9: {"friends": {1, 2, 3}, "enemies": {4, 5, 8}},        # Mars
}


def _build_pair_combination_table():
    """Build the 00-99 digit-pair combination table (Benefic/Neutral/Malefic).

    Rules:
    - If BOTH digits consider each other friends (mutual) -> Benefic
    - If EITHER digit considers the other an enemy -> Malefic
    - Otherwise -> Neutral
    - Pairs with 0 are always Neutral (0 has no planetary ruler)
    - Same-digit pairs: Benefic if digit has friends with itself concept,
      otherwise Neutral. By convention same-digit pairs are Benefic for
      1,3,5,6,9 and Neutral for 2,4,7,8.
    """
    table = {}
    for i in range(10):
        for j in range(10):
            pair_str = f"{i}{j}"
            if i == 0 or j == 0:
                table[pair_str] = "Neutral"
                continue
            if i == j:
                # Same digit — Benefic for strong/friendly numbers, Neutral for others
                if i in {1, 3, 5, 6, 9}:
                    table[pair_str] = "Benefic"
                else:
                    table[pair_str] = "Neutral"
                continue

            rel_i = PLANET_RELATIONSHIPS[i]
            rel_j = PLANET_RELATIONSHIPS[j]

            # If either considers the other an enemy -> Malefic
            if j in rel_i["enemies"] or i in rel_j["enemies"]:
                table[pair_str] = "Malefic"
            # If both consider each other friends -> Benefic
            elif j in rel_i["friends"] and i in rel_j["friends"]:
                table[pair_str] = "Benefic"
            else:
                table[pair_str] = "Neutral"
    return table


PAIR_COMBINATION_TABLE = _build_pair_combination_table()


# Lucky colors per mobile total
LUCKY_COLORS = {
    1: ["Red", "Orange", "Gold"],
    2: ["White", "Silver", "Cream"],
    3: ["Yellow", "Orange", "Gold"],
    4: ["Blue", "Grey"],
    5: ["Green", "Light Green"],
    6: ["Pink", "White", "Light Blue"],
    7: ["Green", "Yellow", "White"],
    8: ["Black", "Dark Blue", "Dark Grey"],
    9: ["Red", "Orange", "Pink", "Coral"],
    11: ["White", "Silver", "Cream"],      # same as 2 (1+1)
    22: ["Blue", "Grey"],                   # same as 4 (2+2)
    33: ["Pink", "White", "Light Blue"],    # same as 6 (3+3)
}

# Unlucky colors per mobile total (opposite energy)
UNLUCKY_COLORS = {
    1: ["Black", "Dark Grey"],
    2: ["Red", "Dark Red"],
    3: ["Black", "Dark Blue"],
    4: ["Red", "Orange"],
    5: ["Red", "Orange"],
    6: ["Black", "Dark Grey"],
    7: ["Black", "Dark Red"],
    8: ["Red", "Orange", "Gold"],
    9: ["Black", "Dark Blue"],
    11: ["Red", "Dark Red"],
    22: ["Red", "Orange"],
    33: ["Black", "Dark Grey"],
}


# Lucky / Unlucky / Neutral numbers per mobile total (based on friendship table)
def _build_number_affinities():
    """For each mobile total (1-9, 11, 22, 33), classify digits 1-9."""
    affinities = {}
    for total in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        rel = PLANET_RELATIONSHIPS[total]
        affinities[total] = {
            "lucky": sorted(rel["friends"]),
            "unlucky": sorted(rel["enemies"]),
            "neutral": sorted({1, 2, 3, 4, 5, 6, 7, 8, 9} - rel["friends"] - rel["enemies"] - {total}),
        }
    # Master numbers map to their root
    affinities[11] = affinities[2]
    affinities[22] = affinities[4]
    affinities[33] = affinities[6]
    return affinities


NUMBER_AFFINITIES = _build_number_affinities()


# Recommended totals based on DOB life path number
RECOMMENDED_TOTALS = {
    1: [1, 3, 5, 9],
    2: [1, 2, 3, 7],
    3: [1, 3, 5, 9],
    4: [4, 5, 6, 7],
    5: [1, 5, 6, 9],
    6: [4, 5, 6, 8],
    7: [4, 6, 7],
    8: [5, 6, 8],
    9: [1, 3, 5, 9],
    11: [1, 2, 3, 7],   # same as 2
    22: [4, 5, 6, 7],   # same as 4
    33: [4, 5, 6, 8],   # same as 6
}


# Standard Loshu Magic Square layout (positions for digits 1-9)
LOSHU_GRID_LAYOUT = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

# Vedic Grid layout
VEDIC_GRID_LAYOUT = [
    [3, 1, 9],
    [0, 7, 0],   # 0 = empty position
    [2, 8, 0],   # 0 = empty position
]


# Affirmations for areas of struggle
AFFIRMATIONS = {
    "health": (
        "I am healthy and full of energy. Every cell in my body vibrates with "
        "health and vitality. I nourish my body with wholesome food and pure water. "
        "I exercise regularly and my body responds with strength and endurance. "
        "I release all tension and stress from my body. I sleep deeply and wake "
        "refreshed. My immune system is strong and protects me from illness. "
        "I am grateful for my healthy body and treat it with love and respect. "
        "Every day, in every way, I am getting healthier and stronger."
    ),
    "relationship": (
        "I deserve real and authentic love. I attract loving, kind, and supportive "
        "people into my life. My relationships are built on mutual respect, trust, "
        "and genuine affection. I communicate openly and honestly with my partner. "
        "I release all past hurts and open my heart to new love. I am worthy of "
        "deep, meaningful connections. I give love freely and receive it graciously. "
        "My relationships bring joy, growth, and fulfillment to my life. "
        "I am surrounded by people who truly care about me."
    ),
    "career": (
        "There are so many great career opportunities available to me right now. "
        "I am confident in my skills and abilities. I attract success and abundance "
        "in my professional life. My work is meaningful and fulfilling. I am "
        "recognized and appreciated for my contributions. I grow and advance in "
        "my career with ease. I am open to new possibilities and embrace change "
        "as an opportunity for growth. My career path aligns with my purpose "
        "and passion. I create value wherever I go."
    ),
    "money": (
        "I experience wealth as a key part of my life. Money flows to me easily "
        "and abundantly. I am a magnet for financial prosperity. I manage my "
        "finances wisely and make sound investment decisions. I release all "
        "limiting beliefs about money and abundance. I deserve to be financially "
        "free and secure. Multiple streams of income flow into my life. I am "
        "grateful for the abundance that surrounds me. Wealth comes to me from "
        "expected and unexpected sources. I use my prosperity to create good "
        "in the world."
    ),
    "job": (
        "I am excited that every action I take moves me towards my perfect career. "
        "I attract the ideal job that matches my skills, values, and aspirations. "
        "My workplace is supportive and inspiring. I am valued and respected by "
        "my colleagues and superiors. I perform my duties with excellence and "
        "enthusiasm. Opportunities for advancement come to me naturally. I enjoy "
        "going to work each day. My job provides me with financial security and "
        "personal satisfaction. I am exactly where I need to be in my career "
        "journey, and the best is yet to come."
    ),
}


# Detailed predictions per mobile total (Batraa-style comprehensive readings)
MOBILE_PREDICTIONS_DETAILED = {
    1: (
        "Mobile Total 1 — The Leader's Number (Sun)\n\n"
        "Personality: You are a born leader with a magnetic personality. People are naturally "
        "drawn to your confidence and decisiveness. You have a strong sense of self and prefer "
        "to forge your own path rather than follow others.\n\n"
        "Career: This number is excellent for entrepreneurs, CEOs, government officials, and "
        "anyone in a leadership role. Calls received on this number often bring business "
        "proposals, partnership offers, and invitations to take charge of new projects.\n\n"
        "Relationships: You attract partners who admire your strength, but must guard against "
        "dominating relationships. Mutual respect is key. Family members look up to you for "
        "guidance and decision-making.\n\n"
        "Health: Strong vitality and constitution. Watch for stress-related issues due to "
        "overwork. Heart and eyes need attention. Regular breaks and meditation help maintain "
        "your energy.\n\n"
        "Finance: Money comes through personal effort and initiative. You are likely to build "
        "wealth through your own ventures rather than inheritance or luck. Investments in gold "
        "and government bonds suit you."
    ),
    2: (
        "Mobile Total 2 — The Diplomat's Number (Moon)\n\n"
        "Personality: You are sensitive, intuitive, and deeply empathetic. Your greatest "
        "strength lies in understanding others' emotions and mediating conflicts. You prefer "
        "harmony over confrontation.\n\n"
        "Career: Ideal for counselors, therapists, artists, musicians, and diplomats. This "
        "number attracts calls related to emotional support, creative collaboration, and "
        "partnership opportunities. Team-based work suits you best.\n\n"
        "Relationships: Deeply romantic and devoted. You form intense emotional bonds and "
        "value loyalty above all. Guard against mood swings and over-dependency on your "
        "partner's validation.\n\n"
        "Health: Pay attention to digestive health, water retention, and emotional well-being. "
        "The Moon's influence makes you susceptible to stress-induced ailments. Meditation, "
        "water therapy, and creative expression are healing.\n\n"
        "Finance: Wealth comes through partnerships and collaborative ventures rather than "
        "solo efforts. Investments in silver, pearls, and real estate near water bodies are "
        "auspicious."
    ),
    3: (
        "Mobile Total 3 — The Creative's Number (Jupiter)\n\n"
        "Personality: Optimistic, expressive, and socially magnetic. You light up any room "
        "you enter. Your natural charisma and communication skills make you an excellent "
        "networker and influencer.\n\n"
        "Career: Perfect for writers, speakers, marketers, teachers, and entertainers. This "
        "number attracts social invitations, media opportunities, and creative projects. "
        "You excel in roles that require public interaction.\n\n"
        "Relationships: Charming and popular, you attract many admirers. Romantic life is "
        "vibrant but you must guard against superficial connections. Seek depth over quantity "
        "in relationships.\n\n"
        "Health: Generally robust health blessed by Jupiter. Watch for liver-related issues, "
        "weight gain, and skin conditions. An active social life can lead to overindulgence — "
        "moderation is key.\n\n"
        "Finance: Jupiter blesses you with abundance and opportunities. Money comes through "
        "creative ventures, teaching, and advisory roles. Yellow sapphire and gold investments "
        "are favorable."
    ),
    4: (
        "Mobile Total 4 — The Builder's Number (Rahu)\n\n"
        "Personality: Unconventional, hardworking, and deeply analytical. You see the world "
        "differently and often challenge established norms. Rahu gives you a unique perspective "
        "and intense determination.\n\n"
        "Career: Suited for technology, research, occult sciences, and unconventional fields. "
        "This number attracts calls related to technical projects, innovation, and problem-solving. "
        "You may face sudden changes in career direction.\n\n"
        "Relationships: Relationships can be intense and sometimes unpredictable. You need a "
        "partner who understands your need for independence and can handle your unconventional "
        "nature. Loyalty runs deep once committed.\n\n"
        "Health: Rahu's influence can bring mysterious or hard-to-diagnose ailments. Mental "
        "health, nervous system, and sleep quality need attention. Grounding practices, "
        "routine, and nature walks are beneficial.\n\n"
        "Finance: Financial life may have sudden ups and downs. Wealth can come through "
        "technology, speculation (with caution), and unconventional business models. "
        "Avoid impulsive financial decisions."
    ),
    5: (
        "Mobile Total 5 — The Communicator's Number (Mercury)\n\n"
        "Personality: Quick-witted, versatile, and intellectually curious. You are a natural "
        "communicator who thrives on variety and mental stimulation. Adaptability is your "
        "superpower.\n\n"
        "Career: Excellent for sales, marketing, journalism, travel, trading, and any field "
        "requiring communication skills. This number attracts dynamic opportunities, travel "
        "plans, and networking calls. Business-related contacts increase.\n\n"
        "Relationships: You need intellectual stimulation in relationships. Boredom is your "
        "enemy. A partner who can match your mental agility and love of adventure will keep "
        "the spark alive.\n\n"
        "Health: Mercury governs the nervous system and respiratory tract. Watch for anxiety, "
        "skin allergies, and speech-related issues. Mental relaxation techniques and breathing "
        "exercises are recommended.\n\n"
        "Finance: Excellent business acumen. Money comes through trade, communication, and "
        "intellectual property. Green emerald and investments in communication or technology "
        "sectors are auspicious."
    ),
    6: (
        "Mobile Total 6 — The Lover's Number (Venus)\n\n"
        "Personality: Charming, artistic, and deeply devoted to beauty and harmony. Venus "
        "blesses you with aesthetic sensibility and a warm, loving nature. People find comfort "
        "in your presence.\n\n"
        "Career: Ideal for artists, designers, luxury goods, hospitality, beauty industry, "
        "and entertainment. This number attracts calls related to creative projects, romantic "
        "connections, and aesthetic endeavors.\n\n"
        "Relationships: Love is central to your life. You are a devoted partner who creates "
        "beautiful, harmonious relationships. Guard against possessiveness and the tendency "
        "to sacrifice too much for others.\n\n"
        "Health: Venus governs the reproductive system, kidneys, and throat. Maintain "
        "balance in diet and lifestyle. Luxury and indulgence can lead to health issues. "
        "Yoga and artistic expression are therapeutic.\n\n"
        "Finance: Wealth comes through beauty, art, luxury, and creative ventures. Diamond "
        "and white sapphire investments are favorable. Income through partnerships and "
        "marriage is also indicated."
    ),
    7: (
        "Mobile Total 7 — The Mystic's Number (Ketu)\n\n"
        "Personality: Deeply spiritual, introspective, and intuitive. Ketu gives you access "
        "to hidden knowledge and metaphysical understanding. You often feel like an old soul "
        "with wisdom beyond your years.\n\n"
        "Career: Suited for research, spiritual guidance, healing arts, astrology, and any "
        "field requiring deep analysis. This number attracts calls related to spiritual "
        "matters, research projects, and meaningful conversations.\n\n"
        "Relationships: You need a partner who respects your need for solitude and spiritual "
        "growth. Surface-level connections leave you unfulfilled. Deep, soulful bonds are "
        "what you seek.\n\n"
        "Health: Ketu can bring mysterious symptoms and psychosomatic conditions. Digestive "
        "system and nervous system need attention. Meditation, fasting, and spiritual "
        "practices are deeply healing for you.\n\n"
        "Finance: Material wealth is not your primary driver, yet it comes through spiritual "
        "or research-oriented work. Cat's eye gemstone is favorable. Avoid speculation and "
        "stick to stable investments."
    ),
    8: (
        "Mobile Total 8 — The Powerhouse Number (Saturn)\n\n"
        "Personality: Disciplined, ambitious, and enduring. Saturn gives you the resilience "
        "to overcome any obstacle. You are a late bloomer who achieves great success through "
        "persistent effort and patience.\n\n"
        "Career: Excellent for law, real estate, construction, mining, oil, and large-scale "
        "industries. This number attracts calls related to serious business matters, legal "
        "affairs, and long-term projects. Success comes after struggle.\n\n"
        "Relationships: Relationships may start slow but grow deeper with time. Saturn "
        "tests your bonds. Those who endure the initial challenges build unbreakable "
        "partnerships. Patience with your partner is essential.\n\n"
        "Health: Bones, joints, teeth, and chronic conditions fall under Saturn. Regular "
        "exercise, calcium-rich diet, and discipline in daily routine are essential. "
        "Avoid overwork — burnout is a real risk.\n\n"
        "Finance: Wealth accumulates slowly but surely. Saturn rewards patience and "
        "discipline. Blue sapphire (with caution) and investments in real estate, "
        "infrastructure, and established industries are favorable."
    ),
    9: (
        "Mobile Total 9 — The Warrior's Number (Mars)\n\n"
        "Personality: Courageous, passionate, and fiercely independent. Mars gives you "
        "tremendous energy, drive, and the fighting spirit to overcome any challenge. "
        "You are a natural protector and defender.\n\n"
        "Career: Ideal for military, police, sports, surgery, engineering, and any field "
        "requiring courage and physical energy. This number attracts calls related to "
        "competitive opportunities, physical activities, and leadership roles.\n\n"
        "Relationships: Passionate and intense in love. You need a partner who can match "
        "your energy and isn't intimidated by your strong personality. Channel Mars energy "
        "into protecting and supporting your loved ones.\n\n"
        "Health: Mars governs blood, muscles, and the head. Watch for injuries, "
        "inflammation, blood pressure, and anger-related stress. Regular physical exercise "
        "is essential to channel Mars energy constructively.\n\n"
        "Finance: Wealth comes through courage, competition, and leadership. Red coral "
        "and investments in real estate, land, and defense-related sectors are favorable. "
        "Avoid impulsive spending."
    ),
    11: (
        "Mobile Total 11 — Master Intuitive (Moon Amplified)\n\n"
        "Personality: You carry the heightened sensitivity of the Moon doubled. Master Number "
        "11 is one of the most intuitive vibrations in numerology. You possess visionary "
        "insight, spiritual awareness, and the ability to inspire others with your ideas.\n\n"
        "Career: Suited for spiritual leadership, counseling, art, music, and visionary "
        "entrepreneurship. This number attracts synchronistic calls and deeply meaningful "
        "connections that advance your life purpose.\n\n"
        "Relationships: Intensely emotional and spiritual bonds. You need a partner who "
        "understands your sensitivity and supports your higher calling. Guard against "
        "nervous tension and anxiety in relationships.\n\n"
        "Health: Heightened sensitivity means heightened vulnerability to stress. Nervous "
        "system, eyes, and emotional well-being need constant attention. Meditation and "
        "creative expression are non-negotiable.\n\n"
        "Finance: Money comes through inspired ideas and visionary projects. You may "
        "experience feast-or-famine cycles until you learn to ground your visions in "
        "practical reality."
    ),
    22: (
        "Mobile Total 22 — Master Builder (Rahu Amplified)\n\n"
        "Personality: The most powerful number in numerology. Master Number 22 combines "
        "the vision of 11 with the practical ability of 4. You can turn the grandest "
        "dreams into tangible reality.\n\n"
        "Career: Destined for large-scale projects — architecture, city planning, "
        "international business, and social reform. This number attracts contacts with "
        "influential people and opportunities to shape communities.\n\n"
        "Relationships: You need a partner who shares your grand vision or at least "
        "supports it. Ordinary domestic life may feel constraining. Find someone who "
        "understands your mission.\n\n"
        "Health: The intensity of this number can lead to exhaustion and burnout. "
        "Balance between work and rest is critical. Nervous system and mental health "
        "need proactive care.\n\n"
        "Finance: Massive wealth potential through large-scale ventures. Patience is "
        "key — your projects take time to bear fruit but the rewards are extraordinary."
    ),
    33: (
        "Mobile Total 33 — Master Teacher (Jupiter Amplified)\n\n"
        "Personality: The most spiritually evolved number. Master Number 33 embodies "
        "selfless love, healing wisdom, and the desire to uplift all of humanity. You "
        "are a natural healer and teacher.\n\n"
        "Career: Called to healing, teaching, counseling, and humanitarian service. This "
        "number attracts people seeking guidance, wisdom, and comfort. Your words carry "
        "profound healing power.\n\n"
        "Relationships: Unconditional love is your natural state, but guard against "
        "martyrdom. You must learn to receive love as freely as you give it. Set healthy "
        "boundaries.\n\n"
        "Health: Your health is tied to your emotional state. When you give too much "
        "without replenishing, burnout follows. Heart, thyroid, and immune system need "
        "attention. Self-care is not selfish.\n\n"
        "Finance: Money comes through service and teaching. You are not driven by "
        "material gain, yet the universe provides abundantly when you serve your "
        "highest purpose."
    ),
}


def _compute_loshu_grid(dob_digits: list) -> dict:
    """Compute Loshu Grid values from DOB digits.

    Returns dict with:
      - 'grid': the 3x3 Loshu layout [[4,9,2],[3,5,7],[8,1,6]]
      - 'values': {digit: repeated_string} e.g. {7: "77", 9: "9", 4: ""}
    """
    from collections import Counter
    counts = Counter(dob_digits)

    values = {}
    for d in range(1, 10):
        count = counts.get(d, 0)
        values[d] = str(d) * count if count > 0 else ""

    return {
        "grid": [row[:] for row in LOSHU_GRID_LAYOUT],
        "values": values,
    }


def _compute_vedic_grid(dob_digits: list) -> dict:
    """Compute Vedic Grid values from DOB digits.

    Returns dict with:
      - 'grid': the Vedic layout [[3,1,9],[0,7,0],[2,8,0]]
      - 'values': {digit: count} for digits present in the layout
    """
    from collections import Counter
    counts = Counter(dob_digits)

    # Vedic grid positions: only certain digits have slots
    vedic_positions = {3, 1, 9, 7, 2, 8}  # digits with slots in Vedic grid
    values = {}
    for d in range(0, 10):
        if d in vedic_positions:
            count = counts.get(d, 0)
            values[d] = str(d) * count if count > 0 else ""
        elif d == 0:
            values[d] = ""
        else:
            count = counts.get(d, 0)
            values[d] = str(d) * count if count > 0 else ""

    # Build the grid with DOB digit counts filling the positions
    grid = []
    for row in VEDIC_GRID_LAYOUT:
        grid_row = []
        for cell in row:
            if cell == 0:
                grid_row.append(0)
            else:
                grid_row.append(counts.get(cell, 0))
        grid.append(grid_row)

    return {
        "grid": grid,
        "values": values,
    }


def _extract_dob_digits(birth_date: str) -> list:
    """Extract individual digits from a YYYY-MM-DD date string, excluding 0."""
    return [int(ch) for ch in birth_date if ch.isdigit()]


def _extract_dob_digits_nonzero(birth_date: str) -> list:
    """Extract individual non-zero digits from a YYYY-MM-DD date string."""
    return [int(ch) for ch in birth_date if ch.isdigit() and ch != '0']


# ============================================================
# LO SHU GRID INTERPRETATION — Arrows, Planes, Missing, Repeated
# ============================================================
#
# Standard Lo Shu layout (same as LOSHU_GRID_LAYOUT above):
#   4 | 9 | 2
#   3 | 5 | 7
#   8 | 1 | 6
#
# Note on "planes":
# Some numerology sources also describe planes as digit triads
# (Mental: 3/6/9, Emotional: 2/5/8, Practical: 1/4/7). The app uses
# this triad-based definition to match product requirements.

ARROWS_OF_STRENGTH = {
    "determination": {
        "numbers": [1, 5, 9],
        "name": "Arrow of Determination",
        "name_hi": "दृढ़ संकल्प का तीर",
        "meaning": "Strong willpower, persistence, achieves goals against all odds",
        "meaning_hi": "दृढ़ इच्छाशक्ति, लगन, हर परिस्थिति में लक्ष्य प्राप्ति",
    },
    "spirituality": {
        "numbers": [3, 5, 7],
        "name": "Arrow of Spirituality",
        "name_hi": "आध्यात्मिकता का तीर",
        "meaning": "Deep inner wisdom, spiritual growth, strong intuition",
        "meaning_hi": "गहन आंतरिक ज्ञान, आध्यात्मिक विकास, प्रबल अंतर्ज्ञान",
    },
    "intellect": {
        "numbers": [4, 9, 2],
        "name": "Arrow of Intellect",
        "name_hi": "बुद्धि का तीर",
        "meaning": "Sharp thinking, good memory, analytical mind",
        "meaning_hi": "तीक्ष्ण सोच, अच्छी स्मृति, विश्लेषणात्मक दिमाग",
    },
    "action": {
        "numbers": [8, 1, 6],
        "name": "Arrow of Action",
        "name_hi": "कर्म का तीर",
        "meaning": "Practical, hardworking, materialistic success through effort",
        "meaning_hi": "व्यावहारिक, कठिन परिश्रम, प्रयास से भौतिक सफलता",
    },
    "planner": {
        "numbers": [4, 5, 6],
        "name": "Arrow of the Planner",
        "name_hi": "योजनाकार का तीर",
        "meaning": "Organized, good at planning, systematic approach to life",
        "meaning_hi": "व्यवस्थित, योजना में कुशल, जीवन के प्रति क्रमबद्ध दृष्टिकोण",
    },
    "willpower": {
        "numbers": [4, 3, 8],
        "name": "Arrow of Willpower",
        "name_hi": "इच्छाशक्ति का तीर",
        "meaning": "Strong will, determination to finish what is started",
        "meaning_hi": "दृढ़ इच्छा, शुरू किए काम को पूर्ण करने का संकल्प",
    },
    "prosperity": {
        "numbers": [2, 5, 8],
        "name": "Arrow of Prosperity",
        "name_hi": "समृद्धि का तीर",
        "meaning": "Material abundance, financial success, wealth attraction",
        "meaning_hi": "भौतिक प्रचुरता, आर्थिक सफलता, धन आकर्षण",
    },
    "frustration": {
        "numbers": [2, 7, 6],
        "name": "Arrow of Frustration",
        "name_hi": "निराशा का तीर",
        "meaning": "Emotional sensitivity, feeling misunderstood, inner turmoil",
        "meaning_hi": "भावनात्मक संवेदनशीलता, गलत समझे जाने की पीड़ा, आंतरिक अशांति",
    },
}

ARROWS_OF_WEAKNESS = {
    "determination": {
        "missing_meaning": "Lack of focus and direction, gives up easily when challenged",
        "missing_meaning_hi": "ध्यान और दिशा की कमी, चुनौती मिलने पर आसानी से हार मान लेते हैं",
    },
    "spirituality": {
        "missing_meaning": "Disconnected from inner self, superficial approach to life",
        "missing_meaning_hi": "आंतरिक आत्म से कटे हुए, जीवन के प्रति सतही दृष्टिकोण",
    },
    "intellect": {
        "missing_meaning": "Struggles with learning, poor memory and analytical weakness",
        "missing_meaning_hi": "सीखने में कठिनाई, कमजोर स्मृति और विश्लेषण शक्ति की कमी",
    },
    "action": {
        "missing_meaning": "Lazy, lacks practical sense and follow-through on plans",
        "missing_meaning_hi": "आलस्य, व्यावहारिक समझ की कमी, योजनाओं पर अमल नहीं",
    },
    "planner": {
        "missing_meaning": "Disorganized, poor at time management and planning",
        "missing_meaning_hi": "अव्यवस्थित, समय प्रबंधन और योजना बनाने में कमजोर",
    },
    "willpower": {
        "missing_meaning": "Weak determination, easily distracted, leaves tasks incomplete",
        "missing_meaning_hi": "कमजोर संकल्प, आसानी से विचलित, कार्य अधूरे छोड़ देते हैं",
    },
    "prosperity": {
        "missing_meaning": "Financial struggles, difficulty accumulating wealth",
        "missing_meaning_hi": "आर्थिक कठिनाइयाँ, धन संचय में परेशानी",
    },
    "frustration": {
        "missing_meaning": "Emotionally detached, difficulty understanding others' feelings",
        "missing_meaning_hi": "भावनात्मक रूप से अलग-थलग, दूसरों की भावनाएँ समझने में कठिनाई",
    },
}


def analyze_loshu_arrows(dob_digits: list) -> dict:
    """Detect Lo Shu arrows of strength and weakness from DOB digits.

    Strength: ALL 3 numbers of an arrow are present in DOB.
    Weakness: ALL 3 numbers of an arrow are ABSENT from DOB.
    (If only 1 or 2 present, the arrow is neither strength nor weakness.)

    Args:
        dob_digits: list of non-zero DOB digits (e.g. [1, 9, 9, 5, 5, 1, 9])

    Returns:
        dict with 'arrows_of_strength' and 'arrows_of_weakness' lists.
    """
    present = set(dob_digits)
    strength = []
    weakness = []

    for key, arrow in ARROWS_OF_STRENGTH.items():
        nums = arrow["numbers"]
        if all(n in present for n in nums):
            strength.append({**arrow, "key": key})
        elif not any(n in present for n in nums):
            weak_data = ARROWS_OF_WEAKNESS[key]
            weakness.append({
                **arrow,
                "key": key,
                "missing_meaning": weak_data["missing_meaning"],
                "missing_meaning_hi": weak_data["missing_meaning_hi"],
            })

    return {"arrows_of_strength": strength, "arrows_of_weakness": weakness}


# --- Planes Analysis ---

PLANE_INTERPRETATIONS = {
    "mental": {
        "name": "Mental Plane",
        "name_hi": "मानसिक तल",
        "strong": "Strong thinker, analytical mind, excellent memory and reasoning ability",
        "strong_hi": "प्रबल चिंतक, विश्लेषणात्मक दिमाग, उत्कृष्ट स्मृति और तर्कशक्ति",
        "weak": "May struggle with analysis and abstract thinking",
        "weak_hi": "विश्लेषण और अमूर्त सोच में कठिनाई हो सकती है",
    },
    "emotional": {
        "name": "Emotional Plane",
        "name_hi": "भावनात्मक तल",
        "strong": "Deeply intuitive, creative, emotionally rich inner world",
        "strong_hi": "गहन अंतर्ज्ञान, रचनात्मक, भावनात्मक रूप से समृद्ध आंतरिक संसार",
        "weak": "May find it hard to express feelings or connect emotionally",
        "weak_hi": "भावनाओं को व्यक्त करने या भावनात्मक रूप से जुड़ने में कठिनाई",
    },
    "practical": {
        "name": "Practical Plane",
        "name_hi": "व्यावहारिक तल",
        "strong": "Action-oriented, hardworking, excels at turning ideas into reality",
        "strong_hi": "कर्मठ, मेहनती, विचारों को वास्तविकता में बदलने में कुशल",
        "weak": "May struggle with practical execution and material matters",
        "weak_hi": "व्यावहारिक कार्यान्वयन और भौतिक मामलों में कठिनाई",
    },
}

DOMINANT_PLANE_INTERPRETATION = {
    "mental": {
        "interpretation": "You are a strong thinker. Your mind is your greatest asset — logic, analysis, and memory dominate your personality.",
        "interpretation_hi": "आप एक प्रबल विचारक हैं। आपका दिमाग आपकी सबसे बड़ी ताकत है — तर्क, विश्लेषण और स्मृति आपके व्यक्तित्व पर हावी हैं।",
    },
    "emotional": {
        "interpretation": "You are deeply emotional and intuitive. Creativity, feelings, and spiritual awareness define your life approach.",
        "interpretation_hi": "आप गहरे भावनात्मक और सहज ज्ञान वाले हैं। रचनात्मकता, भावनाएँ और आध्यात्मिक जागरूकता आपके जीवन दृष्टिकोण को परिभाषित करती हैं।",
    },
    "practical": {
        "interpretation": "You are action-oriented and grounded. Hard work, material success, and practical implementation are your strengths.",
        "interpretation_hi": "आप कर्मठ और व्यावहारिक हैं। कठिन परिश्रम, भौतिक सफलता और व्यावहारिक कार्यान्वयन आपकी ताकत हैं।",
    },
    "balanced": {
        "interpretation": "Your planes are balanced — you have a harmonious blend of thinking, feeling, and doing. This is rare and fortunate.",
        "interpretation_hi": "आपके तल संतुलित हैं — सोच, भावना और कर्म का सामंजस्यपूर्ण मिश्रण है। यह दुर्लभ और सौभाग्यशाली है।",
    },
}


def analyze_loshu_planes(dob_digits: list) -> dict:
    """Analyze the three Lo Shu planes from DOB digits.

    Planes (triad-based):
      Mental: 3, 6, 9
      Emotional: 2, 5, 8
      Practical: 1, 4, 7

    Args:
        dob_digits: list of non-zero DOB digits

    Returns:
        dict with mental, emotional, practical plane scores, percentages,
        dominant_plane, and bilingual interpretations.
    """
    from collections import Counter
    counts = Counter(dob_digits)

    mental_nums = [3, 6, 9]
    emotional_nums = [2, 5, 8]
    practical_nums = [1, 4, 7]

    mental = sum(counts.get(d, 0) for d in mental_nums)
    emotional = sum(counts.get(d, 0) for d in emotional_nums)
    practical = sum(counts.get(d, 0) for d in practical_nums)
    total = mental + emotional + practical

    mental_pct = round(mental / max(total, 1) * 100)
    emotional_pct = round(emotional / max(total, 1) * 100)
    practical_pct = round(practical / max(total, 1) * 100)

    # Determine dominant plane
    scores = {"mental": mental, "emotional": emotional, "practical": practical}
    max_score = max(scores.values())
    dominant_planes = [k for k, v in scores.items() if v == max_score]
    dominant = dominant_planes[0] if len(dominant_planes) == 1 else "balanced"

    interp = DOMINANT_PLANE_INTERPRETATION[dominant]

    return {
        "mental": {
            "score": mental,
            "percentage": mental_pct,
            "numbers": mental_nums,
            "name": PLANE_INTERPRETATIONS["mental"]["name"],
            "name_hi": PLANE_INTERPRETATIONS["mental"]["name_hi"],
            "interpretation": PLANE_INTERPRETATIONS["mental"]["weak" if mental == 0 else "strong"],
            "interpretation_hi": PLANE_INTERPRETATIONS["mental"]["weak_hi" if mental == 0 else "strong_hi"],
        },
        "emotional": {
            "score": emotional,
            "percentage": emotional_pct,
            "numbers": emotional_nums,
            "name": PLANE_INTERPRETATIONS["emotional"]["name"],
            "name_hi": PLANE_INTERPRETATIONS["emotional"]["name_hi"],
            "interpretation": PLANE_INTERPRETATIONS["emotional"]["weak" if emotional == 0 else "strong"],
            "interpretation_hi": PLANE_INTERPRETATIONS["emotional"]["weak_hi" if emotional == 0 else "strong_hi"],
        },
        "practical": {
            "score": practical,
            "percentage": practical_pct,
            "numbers": practical_nums,
            "name": PLANE_INTERPRETATIONS["practical"]["name"],
            "name_hi": PLANE_INTERPRETATIONS["practical"]["name_hi"],
            "interpretation": PLANE_INTERPRETATIONS["practical"]["weak" if practical == 0 else "strong"],
            "interpretation_hi": PLANE_INTERPRETATIONS["practical"]["weak_hi" if practical == 0 else "strong_hi"],
        },
        "dominant_plane": dominant,
        "interpretation": interp["interpretation"],
        "interpretation_hi": interp["interpretation_hi"],
    }


# --- Missing Numbers Remedies ---

MISSING_NUMBER_REMEDIES = {
    1: {
        "meaning": "Lack of confidence, difficulty expressing self, poor leadership",
        "meaning_hi": "आत्मविश्वास की कमी, स्वयं को व्यक्त करने में कठिनाई, कमजोर नेतृत्व",
        "remedy": "Wear red or orange on Sundays, chant Surya mantra (Om Suryaya Namah), develop leadership skills, wake up at sunrise",
        "remedy_hi": "रविवार को लाल या नारंगी रंग पहनें, सूर्य मंत्र (ॐ सूर्याय नमः) जपें, नेतृत्व कौशल विकसित करें, सूर्योदय पर उठें",
        "color": "Red / Orange",
        "color_hi": "लाल / नारंगी",
        "gemstone": "Ruby (Manik)",
        "gemstone_hi": "माणिक्य (माणिक)",
        "planet": "Sun",
    },
    2: {
        "meaning": "Sensitivity issues, relationship difficulties, indecisiveness",
        "meaning_hi": "संवेदनशीलता की समस्या, संबंधों में कठिनाई, अनिर्णय",
        "remedy": "Wear white or cream on Mondays, chant Chandra mantra (Om Chandraya Namah), practice patience, drink water from silver vessel",
        "remedy_hi": "सोमवार को सफेद या क्रीम रंग पहनें, चंद्र मंत्र (ॐ चंद्राय नमः) जपें, धैर्य का अभ्यास करें, चाँदी के बर्तन से पानी पिएँ",
        "color": "White / Cream",
        "color_hi": "सफेद / क्रीम",
        "gemstone": "Pearl (Moti)",
        "gemstone_hi": "मोती",
        "planet": "Moon",
    },
    3: {
        "meaning": "Difficulty with self-expression and creativity, lack of joy",
        "meaning_hi": "आत्म-अभिव्यक्ति और रचनात्मकता में कठिनाई, आनंद की कमी",
        "remedy": "Wear yellow on Thursdays, chant Guru mantra (Om Gurave Namah), engage in creative activities, teach or mentor others",
        "remedy_hi": "गुरुवार को पीला रंग पहनें, गुरु मंत्र (ॐ गुरवे नमः) जपें, रचनात्मक गतिविधियाँ करें, दूसरों को सिखाएँ",
        "color": "Yellow",
        "color_hi": "पीला",
        "gemstone": "Yellow Sapphire (Pukhraj)",
        "gemstone_hi": "पुखराज",
        "planet": "Jupiter",
    },
    4: {
        "meaning": "Lack of discipline and organization, scattered energy, instability",
        "meaning_hi": "अनुशासन और व्यवस्था की कमी, बिखरी ऊर्जा, अस्थिरता",
        "remedy": "Wear dark blue on Saturdays, chant Rahu mantra (Om Rahave Namah), create daily routines, practice meditation",
        "remedy_hi": "शनिवार को गहरा नीला रंग पहनें, राहु मंत्र (ॐ राहवे नमः) जपें, दैनिक दिनचर्या बनाएँ, ध्यान करें",
        "color": "Dark Blue / Grey",
        "color_hi": "गहरा नीला / स्लेटी",
        "gemstone": "Hessonite (Gomed)",
        "gemstone_hi": "गोमेद",
        "planet": "Rahu",
    },
    5: {
        "meaning": "Fear of change, rigidity, inability to adapt, stubbornness",
        "meaning_hi": "बदलाव का डर, कठोरता, अनुकूलन में असमर्थता, जिद",
        "remedy": "Wear green on Wednesdays, chant Budh mantra (Om Budhaya Namah), travel frequently, learn new skills",
        "remedy_hi": "बुधवार को हरा रंग पहनें, बुध मंत्र (ॐ बुधाय नमः) जपें, बार-बार यात्रा करें, नए कौशल सीखें",
        "color": "Green",
        "color_hi": "हरा",
        "gemstone": "Emerald (Panna)",
        "gemstone_hi": "पन्ना",
        "planet": "Mercury",
    },
    6: {
        "meaning": "Difficulty with responsibility and home life, relationship troubles",
        "meaning_hi": "जिम्मेदारी और पारिवारिक जीवन में कठिनाई, संबंधों में परेशानी",
        "remedy": "Wear pink or light blue on Fridays, chant Shukra mantra (Om Shukraya Namah), beautify surroundings, practice gratitude",
        "remedy_hi": "शुक्रवार को गुलाबी या हल्का नीला पहनें, शुक्र मंत्र (ॐ शुक्राय नमः) जपें, आसपास सुंदरता लाएँ, कृतज्ञता का अभ्यास करें",
        "color": "Pink / Light Blue",
        "color_hi": "गुलाबी / हल्का नीला",
        "gemstone": "Diamond (Heera)",
        "gemstone_hi": "हीरा",
        "planet": "Venus",
    },
    7: {
        "meaning": "Lack of spiritual depth, surface thinking, poor intuition",
        "meaning_hi": "आध्यात्मिक गहराई की कमी, सतही सोच, कमजोर अंतर्ज्ञान",
        "remedy": "Wear light green on Wednesdays, chant Ketu mantra (Om Ketave Namah), practice meditation and solitude, study spiritual texts",
        "remedy_hi": "बुधवार को हल्का हरा पहनें, केतु मंत्र (ॐ केतवे नमः) जपें, ध्यान और एकांत का अभ्यास करें, आध्यात्मिक ग्रंथ पढ़ें",
        "color": "Light Green / Grey",
        "color_hi": "हल्का हरा / स्लेटी",
        "gemstone": "Cat's Eye (Lahsuniya)",
        "gemstone_hi": "लहसुनिया (वैडूर्य)",
        "planet": "Ketu",
    },
    8: {
        "meaning": "Financial struggles, poor money management, karmic obstacles",
        "meaning_hi": "आर्थिक कठिनाइयाँ, खराब धन प्रबंधन, कार्मिक बाधाएँ",
        "remedy": "Wear dark blue or black on Saturdays, chant Shani mantra (Om Shanaye Namah), practice discipline, serve the elderly",
        "remedy_hi": "शनिवार को गहरा नीला या काला पहनें, शनि मंत्र (ॐ शनये नमः) जपें, अनुशासन का पालन करें, बुजुर्गों की सेवा करें",
        "color": "Dark Blue / Black",
        "color_hi": "गहरा नीला / काला",
        "gemstone": "Blue Sapphire (Neelam)",
        "gemstone_hi": "नीलम",
        "planet": "Saturn",
    },
    9: {
        "meaning": "Self-centeredness, lack of compassion, difficulty letting go",
        "meaning_hi": "आत्म-केंद्रितता, करुणा की कमी, छोड़ने में कठिनाई",
        "remedy": "Wear red on Tuesdays, chant Mangal mantra (Om Mangalaya Namah), volunteer and do charity, practice forgiveness",
        "remedy_hi": "मंगलवार को लाल रंग पहनें, मंगल मंत्र (ॐ मंगलाय नमः) जपें, स्वयंसेवा और दान करें, क्षमा का अभ्यास करें",
        "color": "Red / Coral",
        "color_hi": "लाल / मूँगा रंग",
        "gemstone": "Red Coral (Moonga)",
        "gemstone_hi": "मूँगा",
        "planet": "Mars",
    },
}


def analyze_missing_numbers(dob_digits: list) -> list:
    """Identify numbers 1-9 missing from DOB digits with remedies.

    Args:
        dob_digits: list of non-zero DOB digits

    Returns:
        list of dicts for each missing number, sorted ascending,
        each with meaning, remedy, color, gemstone, planet (bilingual).
    """
    present = set(dob_digits)
    missing = []
    for n in range(1, 10):
        if n not in present:
            missing.append({"number": n, **MISSING_NUMBER_REMEDIES[n]})
    return missing


# --- Repeated Numbers Significance ---

REPEATED_NUMBER_MEANINGS = {
    1: {
        2: {"meaning": "Good leadership, confident communicator", "meaning_hi": "अच्छा नेतृत्व, आत्मविश्वासी वक्ता"},
        3: {"meaning": "Dominating personality, may not listen to others", "meaning_hi": "प्रभुत्वशाली व्यक्तित्व, दूसरों की नहीं सुनते"},
        4: {"meaning": "Aggressive and stubborn, needs to practice patience", "meaning_hi": "आक्रामक और जिद्दी, धैर्य का अभ्यास आवश्यक"},
    },
    2: {
        2: {"meaning": "Sensitive and emotional, deeply caring", "meaning_hi": "संवेदनशील और भावनात्मक, गहरी देखभाल करने वाले"},
        3: {"meaning": "Oversensitive, easily hurt by others' words", "meaning_hi": "अति-संवेदनशील, दूसरों के शब्दों से आसानी से आहत"},
        4: {"meaning": "Mood swings, emotional instability", "meaning_hi": "मिजाज में उतार-चढ़ाव, भावनात्मक अस्थिरता"},
    },
    3: {
        2: {"meaning": "Creative thinker, imaginative and expressive", "meaning_hi": "रचनात्मक विचारक, कल्पनाशील और अभिव्यक्त"},
        3: {"meaning": "Self-absorbed, lives in fantasy world", "meaning_hi": "आत्म-लीन, काल्पनिक दुनिया में रहते हैं"},
        4: {"meaning": "Isolated from reality, needs grounding", "meaning_hi": "वास्तविकता से कटे हुए, ज़मीन से जुड़ने की ज़रूरत"},
    },
    4: {
        2: {"meaning": "Hardworking and methodical, detail-oriented", "meaning_hi": "मेहनती और व्यवस्थित, विस्तार पर ध्यान देने वाले"},
        3: {"meaning": "Over-cautious, misses opportunities due to rigidity", "meaning_hi": "अति-सतर्क, कठोरता के कारण अवसर चूक जाते हैं"},
        4: {"meaning": "Extremely rigid, resistant to all change", "meaning_hi": "अत्यंत कठोर, हर बदलाव का विरोध"},
    },
    5: {
        2: {"meaning": "Versatile and adaptable, quick thinker", "meaning_hi": "बहुमुखी और अनुकूलनशील, तेज़ सोच"},
        3: {"meaning": "Restless, cannot stay focused on one thing", "meaning_hi": "बेचैन, एक चीज़ पर ध्यान नहीं टिका सकते"},
        4: {"meaning": "Extremely scattered, prone to anxiety", "meaning_hi": "अत्यंत बिखरे हुए, चिंता की प्रवृत्ति"},
    },
    6: {
        2: {"meaning": "Loving and caring, devoted to family", "meaning_hi": "प्रेमपूर्ण और देखभाल करने वाले, परिवार के प्रति समर्पित"},
        3: {"meaning": "Overly possessive, smothering loved ones", "meaning_hi": "अत्यधिक अधिकार-भावना, प्रियजनों पर दबाव"},
        4: {"meaning": "Controlling in relationships, needs to trust more", "meaning_hi": "रिश्तों में नियंत्रक, अधिक विश्वास करने की आवश्यकता"},
    },
    7: {
        2: {"meaning": "Deeply spiritual, strong intuition and inner wisdom", "meaning_hi": "गहन आध्यात्मिक, प्रबल अंतर्ज्ञान और आंतरिक ज्ञान"},
        3: {"meaning": "Isolated, withdrawn from social life", "meaning_hi": "अकेले रहने वाले, सामाजिक जीवन से कटे हुए"},
        4: {"meaning": "Complete recluse, disconnected from world", "meaning_hi": "पूर्ण एकांतवासी, दुनिया से कटे हुए"},
    },
    8: {
        2: {"meaning": "Strong business sense, financial intelligence", "meaning_hi": "मजबूत व्यापारिक समझ, आर्थिक बुद्धिमत्ता"},
        3: {"meaning": "Obsessed with money and power", "meaning_hi": "पैसे और सत्ता का जुनून"},
        4: {"meaning": "Ruthless in pursuit of material goals", "meaning_hi": "भौतिक लक्ष्यों की खोज में निर्मम"},
    },
    9: {
        2: {"meaning": "Compassionate leader, humanitarian spirit", "meaning_hi": "करुणामय नेता, मानवतावादी भावना"},
        3: {"meaning": "Idealistic to a fault, disappointed by reality", "meaning_hi": "दोषपूर्ण आदर्शवादी, वास्तविकता से निराश"},
        4: {"meaning": "Fanatical about beliefs, needs balance", "meaning_hi": "विश्वासों के प्रति कट्टर, संतुलन आवश्यक"},
    },
}


def analyze_repeated_numbers(dob_digits: list) -> list:
    """Identify numbers appearing 2+ times in DOB digits with significance.

    Args:
        dob_digits: list of non-zero DOB digits

    Returns:
        list of dicts for each repeated number, sorted by number,
        each with number, count, meaning, meaning_hi.
    """
    from collections import Counter
    counts = Counter(dob_digits)
    repeated = []

    for num in sorted(counts):
        count = counts[num]
        if count >= 2 and num in REPEATED_NUMBER_MEANINGS:
            meanings = REPEATED_NUMBER_MEANINGS[num]
            # Use exact count if available, otherwise cap at highest defined
            max_defined = max(meanings.keys())
            lookup_count = min(count, max_defined)
            entry = meanings[lookup_count]
            repeated.append({
                "number": num,
                "count": count,
                "meaning": entry["meaning"],
                "meaning_hi": entry["meaning_hi"],
            })

    return repeated


def calculate_mobile_numerology(
    phone_number: str,
    name: str = "",
    birth_date: str = "",
    areas_of_struggle: list = None,
) -> dict:
    """
    Comprehensive mobile number numerology analysis (Batraa reference style).

    Args:
        phone_number: Phone number string (any format — digits extracted automatically)
        name: Optional full name for personalization
        birth_date: Optional date of birth in YYYY-MM-DD format (enables DOB features)
        areas_of_struggle: Optional list of areas like ["health", "career", "money"]

    Returns:
        dict with compound_number, mobile_total, prediction, loshu_grid, vedic_grid,
        recommended_totals, lucky/unlucky analysis, missing_numbers,
        mobile_combinations, affirmations, and more.
    """
    if areas_of_struggle is None:
        areas_of_struggle = []

    # Strip all non-digit characters
    cleaned = ''.join(ch for ch in phone_number if ch.isdigit())
    if not cleaned:
        raise ValueError("Phone number must contain at least one digit.")
    # Strip common country codes (91 for India) — calculate on local number only
    if len(cleaned) > 10 and cleaned.startswith('91'):
        cleaned = cleaned[2:]

    # --- Compound number & mobile total ---
    compound_number = sum(int(d) for d in cleaned)

    mobile_total = compound_number
    while mobile_total > 9 and mobile_total not in MASTER_NUMBERS:
        mobile_total = sum(int(d) for d in str(mobile_total))

    # --- Prediction ---
    prediction = MOBILE_PREDICTIONS_DETAILED.get(
        mobile_total, MOBILE_PREDICTIONS_DETAILED[9]
    )

    # Also include the legacy structured prediction for backward compat
    legacy_entry = MOBILE_PREDICTIONS.get(mobile_total, MOBILE_PREDICTIONS[9])

    # --- Missing numbers (digits 0-9 not present in phone number) ---
    phone_digit_set = set(int(d) for d in cleaned)
    missing_numbers = sorted([d for d in range(10) if d not in phone_digit_set])

    # --- Mobile combinations (consecutive digit pairs) ---
    mobile_combinations = []
    for i in range(len(cleaned) - 1):
        pair = cleaned[i:i+2]
        combo_type = PAIR_COMBINATION_TABLE.get(pair, "Neutral")
        mobile_combinations.append({"pair": pair, "type": combo_type})

    has_malefic = any(c["type"] == "Malefic" for c in mobile_combinations)
    benefic_count = sum(1 for c in mobile_combinations if c["type"] == "Benefic")
    malefic_count = sum(1 for c in mobile_combinations if c["type"] == "Malefic")

    if has_malefic:
        recommendation = (
            "This Mobile Number is Not Recommended Because It Contains "
            "Malefic Combinations."
        )
    elif benefic_count >= len(mobile_combinations) // 2:
        recommendation = (
            "This Mobile Number is Highly Recommended. It Contains Mostly "
            "Benefic Combinations."
        )
    else:
        recommendation = (
            "This Mobile Number is Acceptable. It Contains Mostly Neutral "
            "Combinations With No Malefic Pairs."
        )

    # --- Lucky / Unlucky colors and numbers ---
    lucky_colors = LUCKY_COLORS.get(mobile_total, LUCKY_COLORS[9])
    unlucky_colors = UNLUCKY_COLORS.get(mobile_total, UNLUCKY_COLORS[9])
    affinities = NUMBER_AFFINITIES.get(mobile_total, NUMBER_AFFINITIES[9])
    lucky_numbers = affinities["lucky"]
    unlucky_numbers = affinities["unlucky"]
    neutral_numbers = affinities["neutral"]

    # --- DOB-based features (only if birth_date provided) ---
    loshu_data = None
    vedic_data = None
    recommended_totals = None
    is_recommended = None
    life_path = None

    if birth_date and '-' in birth_date:
        try:
            dob_all_digits = _extract_dob_digits(birth_date)
            dob_nonzero = _extract_dob_digits_nonzero(birth_date)

            # Loshu grid uses all DOB digits (including 0 handling in grid)
            loshu_data = _compute_loshu_grid(dob_nonzero)
            vedic_data = _compute_vedic_grid(dob_all_digits)

            # Life path for recommended totals
            life_path = _life_path(birth_date)
            recommended_totals = RECOMMENDED_TOTALS.get(
                life_path, RECOMMENDED_TOTALS[9]
            )
            is_recommended = (mobile_total in recommended_totals) and not has_malefic
        except (ValueError, IndexError):
            # Invalid date — skip DOB features silently
            pass

    # --- Affirmations ---
    affirmations = {}
    valid_areas = {"health", "relationship", "career", "money", "job"}
    if areas_of_struggle:
        for area in areas_of_struggle:
            area_lower = area.lower().strip()
            if area_lower in valid_areas:
                affirmations[area_lower] = AFFIRMATIONS[area_lower]
    else:
        # Return all affirmations if no specific areas requested
        affirmations = dict(AFFIRMATIONS)

    # --- Build result ---
    result = {
        "phone_number": cleaned,
        "compound_number": compound_number,
        "mobile_total": mobile_total,
        "prediction": prediction,

        # Lucky / Unlucky analysis
        "lucky_colors": lucky_colors,
        "unlucky_colors": unlucky_colors,
        "lucky_numbers": lucky_numbers,
        "unlucky_numbers": unlucky_numbers,
        "neutral_numbers": neutral_numbers,

        # Missing numbers
        "missing_numbers": missing_numbers,

        # Mobile combinations
        "mobile_combinations": mobile_combinations,
        "has_malefic": has_malefic,
        "benefic_count": benefic_count,
        "malefic_count": malefic_count,
        "recommendation": recommendation,

        # Affirmations
        "affirmations": affirmations,

        # Legacy fields for backward compatibility
        "vibration_number": mobile_total,
        "total_sum": compound_number,
        "lucky_qualities": legacy_entry["lucky_qualities"],
        "challenges": legacy_entry["challenges"],
        "best_for": legacy_entry["best_for"],
        "compatibility_numbers": legacy_entry["compatibility_numbers"],
    }

    # DOB-based features (only present when birth_date provided)
    # NOTE: loshu_grid, loshu_values, missing_numbers here are derived from the
    # owner's date of birth — NOT from the phone number digits. Shown for
    # compatibility reference alongside the phone vibration analysis.
    if loshu_data is not None:
        result["loshu_grid"] = loshu_data["grid"]
        result["loshu_values"] = loshu_data["values"]
        result["loshu_source"] = "birth_date"
        # Lo Shu interpretation features
        dob_digits = [int(c) for c in birth_date.replace("-", "") if c.isdigit() and c != "0"] if birth_date else []
        if dob_digits:
            result["loshu_arrows"] = analyze_loshu_arrows(dob_digits)
            result["loshu_planes"] = analyze_loshu_planes(dob_digits)
            result["missing_numbers"] = analyze_missing_numbers(dob_digits)
            result["repeated_numbers"] = analyze_repeated_numbers(dob_digits)
    if vedic_data is not None:
        result["vedic_grid"] = vedic_data["grid"]
        result["vedic_values"] = vedic_data["values"]
    if recommended_totals is not None:
        result["recommended_totals"] = recommended_totals
        result["is_recommended"] = is_recommended
    if life_path is not None:
        result["life_path"] = life_path

    return result


# ============================================================
# PINNACLE PREDICTIONS (bilingual en + hi)
# Keys: 0-9, 11, 22, 33
# ============================================================

PINNACLE_PREDICTIONS = {
    0: {
        "title": "Inner Potential",
        "title_hi": "आंतरिक क्षमता",
        "opportunity": "Freedom to choose any direction; all paths are open to you.",
        "opportunity_hi": "कोई भी दिशा चुनने की स्वतंत्रता; सभी रास्ते आपके लिए खुले हैं।",
        "lesson": "Make deliberate choices rather than drifting without purpose.",
        "lesson_hi": "बिना उद्देश्य भटकने के बजाय सोच-समझकर निर्णय लें।",
    },
    1: {
        "title": "Leadership & Independence",
        "title_hi": "नेतृत्व और स्वतंत्रता",
        "opportunity": "Forge your own path. Take initiative and lead boldly.",
        "opportunity_hi": "अपना रास्ता खुद बनाएं। पहल करें और साहसपूर्वक नेतृत्व करें।",
        "lesson": "Balance independence with collaboration; avoid isolation.",
        "lesson_hi": "स्वतंत्रता को सहयोग के साथ संतुलित करें; अकेलेपन से बचें।",
    },
    2: {
        "title": "Cooperation & Patience",
        "title_hi": "सहयोग और धैर्य",
        "opportunity": "Partnerships and diplomacy bring great rewards during this period.",
        "opportunity_hi": "इस अवधि में साझेदारी और कूटनीति बड़े पुरस्कार लाती है।",
        "lesson": "Develop patience and sensitivity to others' needs.",
        "lesson_hi": "धैर्य और दूसरों की जरूरतों के प्रति संवेदनशीलता विकसित करें।",
    },
    3: {
        "title": "Creative Expression",
        "title_hi": "रचनात्मक अभिव्यक्ति",
        "opportunity": "Artistic talents blossom. Social connections open doors.",
        "opportunity_hi": "कलात्मक प्रतिभाएं खिलती हैं। सामाजिक संबंध दरवाजे खोलते हैं।",
        "lesson": "Focus creative energy; avoid scattering your talents.",
        "lesson_hi": "रचनात्मक ऊर्जा केंद्रित करें; अपनी प्रतिभाओं को बिखरने न दें।",
    },
    4: {
        "title": "Foundation Building",
        "title_hi": "नींव निर्माण",
        "opportunity": "Hard work and discipline create lasting stability.",
        "opportunity_hi": "कड़ी मेहनत और अनुशासन स्थायी स्थिरता बनाते हैं।",
        "lesson": "Embrace structure without becoming rigid or inflexible.",
        "lesson_hi": "कठोर या अनम्य बने बिना संरचना अपनाएं।",
    },
    5: {
        "title": "Freedom & Change",
        "title_hi": "स्वतंत्रता और परिवर्तन",
        "opportunity": "Travel, adventure, and new experiences bring growth.",
        "opportunity_hi": "यात्रा, साहसिक कार्य और नए अनुभव विकास लाते हैं।",
        "lesson": "Embrace change while maintaining inner stability.",
        "lesson_hi": "आंतरिक स्थिरता बनाए रखते हुए परिवर्तन को अपनाएं।",
    },
    6: {
        "title": "Love & Responsibility",
        "title_hi": "प्रेम और जिम्मेदारी",
        "opportunity": "Family, home, and community service bring deep fulfillment.",
        "opportunity_hi": "परिवार, घर और सामुदायिक सेवा गहरी पूर्णता लाती है।",
        "lesson": "Care for others without sacrificing your own well-being.",
        "lesson_hi": "अपनी भलाई का त्याग किए बिना दूसरों की देखभाल करें।",
    },
    7: {
        "title": "Spiritual Growth & Wisdom",
        "title_hi": "आध्यात्मिक विकास और ज्ञान",
        "opportunity": "Study, research, and inner reflection yield profound insights.",
        "opportunity_hi": "अध्ययन, शोध और आंतरिक चिंतन गहन अंतर्दृष्टि प्रदान करते हैं।",
        "lesson": "Balance solitude with meaningful connections.",
        "lesson_hi": "एकांत को सार्थक संबंधों के साथ संतुलित करें।",
    },
    8: {
        "title": "Material Mastery & Power",
        "title_hi": "भौतिक महारत और शक्ति",
        "opportunity": "Business acumen and financial success are favored.",
        "opportunity_hi": "व्यापार कौशल और वित्तीय सफलता अनुकूल है।",
        "lesson": "Use power with integrity; karmic balance demands fairness.",
        "lesson_hi": "ईमानदारी से शक्ति का उपयोग करें; कर्म संतुलन न्याय की मांग करता है।",
    },
    9: {
        "title": "Humanitarian Service",
        "title_hi": "मानवतावादी सेवा",
        "opportunity": "Compassion and selfless service bring the greatest rewards.",
        "opportunity_hi": "करुणा और निःस्वार्थ सेवा सबसे बड़ा पुरस्कार लाती है।",
        "lesson": "Let go of personal attachments; serve a higher purpose.",
        "lesson_hi": "व्यक्तिगत आसक्ति छोड़ें; उच्च उद्देश्य की सेवा करें।",
    },
    11: {
        "title": "Master Intuition",
        "title_hi": "मास्टर अंतर्ज्ञान",
        "opportunity": "Heightened spiritual awareness and visionary leadership.",
        "opportunity_hi": "उच्च आध्यात्मिक जागरूकता और दूरदर्शी नेतृत्व।",
        "lesson": "Channel inspiration into tangible form; manage nervous energy.",
        "lesson_hi": "प्रेरणा को मूर्त रूप दें; तनावपूर्ण ऊर्जा को प्रबंधित करें।",
    },
    22: {
        "title": "Master Builder",
        "title_hi": "मास्टर निर्माता",
        "opportunity": "Turn grand visions into reality on a massive scale.",
        "opportunity_hi": "बड़े पैमाने पर भव्य दृष्टिकोणों को वास्तविकता में बदलें।",
        "lesson": "Practical idealism — dream big but build step by step.",
        "lesson_hi": "व्यावहारिक आदर्शवाद — बड़े सपने देखें लेकिन कदम दर कदम बनाएं।",
    },
    33: {
        "title": "Master Teacher",
        "title_hi": "मास्टर शिक्षक",
        "opportunity": "Selfless healing and uplifting humanity through love.",
        "opportunity_hi": "निःस्वार्थ उपचार और प्रेम के माध्यम से मानवता का उत्थान।",
        "lesson": "The highest expression of service — heal yourself to heal others.",
        "lesson_hi": "सेवा की सर्वोच्च अभिव्यक्ति — दूसरों को ठीक करने के लिए स्वयं को ठीक करें।",
    },
}


# ============================================================
# CHALLENGE PREDICTIONS (bilingual en + hi)
# Keys: 0-9
# ============================================================

CHALLENGE_PREDICTIONS = {
    0: {
        "title": "The Choice",
        "title_hi": "चुनाव",
        "obstacle": "No single focused obstacle — but the challenge of choosing your direction.",
        "obstacle_hi": "कोई एक केंद्रित बाधा नहीं — लेकिन अपनी दिशा चुनने की चुनौती।",
        "growth": "Develop clarity of purpose; any path can be mastered with commitment.",
        "growth_hi": "उद्देश्य की स्पष्टता विकसित करें; प्रतिबद्धता से कोई भी मार्ग पर महारत हासिल की जा सकती है।",
    },
    1: {
        "title": "Independence vs Selfishness",
        "title_hi": "स्वतंत्रता बनाम स्वार्थ",
        "obstacle": "Struggle between asserting yourself and dominating others.",
        "obstacle_hi": "अपने आप को स्थापित करने और दूसरों पर हावी होने के बीच संघर्ष।",
        "growth": "Lead with confidence without steamrolling those around you.",
        "growth_hi": "आसपास के लोगों को कुचले बिना आत्मविश्वास से नेतृत्व करें।",
    },
    2: {
        "title": "Sensitivity vs Weakness",
        "title_hi": "संवेदनशीलता बनाम कमजोरी",
        "obstacle": "Over-sensitivity leading to emotional fragility or dependence.",
        "obstacle_hi": "अति-संवेदनशीलता भावनात्मक नाजुकता या निर्भरता की ओर ले जाती है।",
        "growth": "Use sensitivity as a strength — empathy without losing yourself.",
        "growth_hi": "संवेदनशीलता को ताकत के रूप में उपयोग करें — खुद को खोए बिना सहानुभूति।",
    },
    3: {
        "title": "Expression vs Scattering",
        "title_hi": "अभिव्यक्ति बनाम बिखराव",
        "obstacle": "Talent spread too thin; difficulty completing creative projects.",
        "obstacle_hi": "प्रतिभा बहुत बिखरी हुई; रचनात्मक परियोजनाओं को पूरा करने में कठिनाई।",
        "growth": "Focus your creative gifts; depth over breadth.",
        "growth_hi": "अपनी रचनात्मक प्रतिभाओं को केंद्रित करें; विस्तार से अधिक गहराई।",
    },
    4: {
        "title": "Order vs Rigidity",
        "title_hi": "व्यवस्था बनाम कठोरता",
        "obstacle": "Excessive need for control and resistance to change.",
        "obstacle_hi": "नियंत्रण की अत्यधिक आवश्यकता और परिवर्तन का प्रतिरोध।",
        "growth": "Build structure that allows flexibility; discipline without prison.",
        "growth_hi": "ऐसी संरचना बनाएं जो लचीलेपन की अनुमति दे; बंधन के बिना अनुशासन।",
    },
    5: {
        "title": "Freedom vs Excess",
        "title_hi": "स्वतंत्रता बनाम अतिरेक",
        "obstacle": "Restlessness, overindulgence, and fear of commitment.",
        "obstacle_hi": "बेचैनी, अतिभोग और प्रतिबद्धता का भय।",
        "growth": "Find freedom within commitment; adventure with responsibility.",
        "growth_hi": "प्रतिबद्धता में स्वतंत्रता खोजें; जिम्मेदारी के साथ साहसिक कार्य।",
    },
    6: {
        "title": "Responsibility vs Martyrdom",
        "title_hi": "जिम्मेदारी बनाम आत्म-बलिदान",
        "obstacle": "Overburdening yourself with others' problems; perfectionism.",
        "obstacle_hi": "दूसरों की समस्याओं से खुद को अत्यधिक बोझिल करना; पूर्णतावाद।",
        "growth": "Serve with healthy boundaries; love yourself as you love others.",
        "growth_hi": "स्वस्थ सीमाओं के साथ सेवा करें; जैसे आप दूसरों से प्यार करते हैं वैसे खुद से भी करें।",
    },
    7: {
        "title": "Faith vs Skepticism",
        "title_hi": "विश्वास बनाम संदेह",
        "obstacle": "Isolation, over-analysis, and difficulty trusting others.",
        "obstacle_hi": "अलगाव, अति-विश्लेषण और दूसरों पर भरोसा करने में कठिनाई।",
        "growth": "Balance intellect with faith; share your wisdom openly.",
        "growth_hi": "बुद्धि को विश्वास के साथ संतुलित करें; अपना ज्ञान खुलकर साझा करें।",
    },
    8: {
        "title": "Power vs Greed",
        "title_hi": "शक्ति बनाम लालच",
        "obstacle": "Material obsession, workaholism, and misuse of authority.",
        "obstacle_hi": "भौतिक जुनून, कार्यशीलता और अधिकार का दुरुपयोग।",
        "growth": "Earn success ethically; power wielded with wisdom endures.",
        "growth_hi": "नैतिक रूप से सफलता अर्जित करें; ज्ञान के साथ प्रयोग की गई शक्ति टिकती है।",
    },
    9: {
        "title": "Letting Go vs Clinging",
        "title_hi": "छोड़ना बनाम लिपटना",
        "obstacle": "Difficulty releasing the past; clinging to people and outcomes.",
        "obstacle_hi": "अतीत को छोड़ने में कठिनाई; लोगों और परिणामों से चिपकना।",
        "growth": "Serve universally; release attachments to find true fulfillment.",
        "growth_hi": "सार्वभौमिक रूप से सेवा करें; सच्ची पूर्णता पाने के लिए आसक्ति छोड़ें।",
    },
}


# ============================================================
# LIFE CYCLE PREDICTIONS (bilingual en + hi)
# Keys: 1-9, 11, 22, 33
# ============================================================

LIFE_CYCLE_PREDICTIONS = {
    1: {
        "title": "Independence Cycle",
        "title_hi": "स्वतंत्रता चक्र",
        "theme": "Developing individuality, courage, and self-reliance.",
        "theme_hi": "व्यक्तित्व, साहस और आत्मनिर्भरता विकसित करना।",
        "advice": "Trust your instincts and take the lead in your own life.",
        "advice_hi": "अपनी प्रवृत्ति पर भरोसा करें और अपने जीवन में नेतृत्व करें।",
    },
    2: {
        "title": "Partnership Cycle",
        "title_hi": "साझेदारी चक्र",
        "theme": "Learning cooperation, diplomacy, and emotional sensitivity.",
        "theme_hi": "सहयोग, कूटनीति और भावनात्मक संवेदनशीलता सीखना।",
        "advice": "Cultivate patience; your greatest strength is gentle persuasion.",
        "advice_hi": "धैर्य विकसित करें; आपकी सबसे बड़ी ताकत सौम्य प्रेरणा है।",
    },
    3: {
        "title": "Expression Cycle",
        "title_hi": "अभिव्यक्ति चक्र",
        "theme": "Creative self-expression, joy, and social connection.",
        "theme_hi": "रचनात्मक आत्म-अभिव्यक्ति, आनंद और सामाजिक संबंध।",
        "advice": "Speak your truth and let your creative gifts flow freely.",
        "advice_hi": "अपना सत्य बोलें और अपनी रचनात्मक प्रतिभाओं को स्वतंत्र रूप से बहने दें।",
    },
    4: {
        "title": "Foundation Cycle",
        "title_hi": "नींव चक्र",
        "theme": "Building stability through discipline, order, and hard work.",
        "theme_hi": "अनुशासन, व्यवस्था और कड़ी मेहनत से स्थिरता का निर्माण।",
        "advice": "Lay strong foundations now; they will support everything that follows.",
        "advice_hi": "अभी मजबूत नींव रखें; वे आगे आने वाली हर चीज का समर्थन करेंगी।",
    },
    5: {
        "title": "Freedom Cycle",
        "title_hi": "स्वतंत्रता चक्र",
        "theme": "Change, travel, adventure, and embracing new experiences.",
        "theme_hi": "परिवर्तन, यात्रा, साहसिक कार्य और नए अनुभवों को अपनाना।",
        "advice": "Embrace change as your teacher; freedom comes from adaptability.",
        "advice_hi": "परिवर्तन को अपना शिक्षक मानें; स्वतंत्रता अनुकूलनशीलता से आती है।",
    },
    6: {
        "title": "Responsibility Cycle",
        "title_hi": "जिम्मेदारी चक्र",
        "theme": "Family, love, duty, and nurturing those around you.",
        "theme_hi": "परिवार, प्रेम, कर्तव्य और अपने आसपास के लोगों का पालन-पोषण।",
        "advice": "Your heart is your compass; serve with love but protect your boundaries.",
        "advice_hi": "आपका हृदय आपकी दिशा है; प्रेम से सेवा करें लेकिन अपनी सीमाओं की रक्षा करें।",
    },
    7: {
        "title": "Wisdom Cycle",
        "title_hi": "ज्ञान चक्र",
        "theme": "Spiritual seeking, study, analysis, and inner growth.",
        "theme_hi": "आध्यात्मिक खोज, अध्ययन, विश्लेषण और आंतरिक विकास।",
        "advice": "Seek truth relentlessly; solitude is your sanctuary for growth.",
        "advice_hi": "अथक सत्य की खोज करें; एकांत विकास के लिए आपका अभयारण्य है।",
    },
    8: {
        "title": "Achievement Cycle",
        "title_hi": "उपलब्धि चक्र",
        "theme": "Material success, authority, and karmic lessons about power.",
        "theme_hi": "भौतिक सफलता, अधिकार और शक्ति के बारे में कर्म संबंधी पाठ।",
        "advice": "Build your empire with integrity; ethical success endures.",
        "advice_hi": "ईमानदारी से अपना साम्राज्य बनाएं; नैतिक सफलता टिकती है।",
    },
    9: {
        "title": "Completion Cycle",
        "title_hi": "पूर्णता चक्र",
        "theme": "Humanitarianism, compassion, and universal love.",
        "theme_hi": "मानवतावाद, करुणा और सार्वभौमिक प्रेम।",
        "advice": "Give freely; the more you release, the more flows back to you.",
        "advice_hi": "स्वतंत्र रूप से दें; जितना अधिक आप छोड़ेंगे, उतना अधिक आपके पास वापस आएगा।",
    },
    11: {
        "title": "Illumination Cycle",
        "title_hi": "प्रकाश चक्र",
        "theme": "Heightened intuition, spiritual awareness, and inspired leadership.",
        "theme_hi": "उच्च अंतर्ज्ञान, आध्यात्मिक जागरूकता और प्रेरित नेतृत्व।",
        "advice": "Trust your inner voice; you are here to illuminate the path for others.",
        "advice_hi": "अपनी आंतरिक आवाज पर भरोसा करें; आप दूसरों के लिए मार्ग रोशन करने के लिए हैं।",
    },
    22: {
        "title": "Master Builder Cycle",
        "title_hi": "मास्टर निर्माता चक्र",
        "theme": "Building great works that serve humanity on a massive scale.",
        "theme_hi": "बड़े पैमाने पर मानवता की सेवा करने वाले महान कार्यों का निर्माण।",
        "advice": "Think globally, build practically; your vision can reshape the world.",
        "advice_hi": "वैश्विक सोचें, व्यावहारिक बनाएं; आपकी दृष्टि दुनिया को नया रूप दे सकती है।",
    },
    33: {
        "title": "Master Healer Cycle",
        "title_hi": "मास्टर उपचारक चक्र",
        "theme": "Selfless service, healing, and uplifting consciousness.",
        "theme_hi": "निःस्वार्थ सेवा, उपचार और चेतना का उत्थान।",
        "advice": "Your love is medicine; pour it out and you will never run dry.",
        "advice_hi": "आपका प्रेम औषधि है; इसे बहाएं और आप कभी सूखेंगे नहीं।",
    },
}


def _reduce_to_single(n: int) -> int:
    """Reduce a number to single digit (1-9) or master number (11, 22, 33)."""
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


# Personal Year predictions keyed by number (1-9)
_PERSONAL_YEAR_PREDICTIONS: dict = {
    1: {
        "theme": "New Beginnings", "theme_hi": "नई शुरुआत",
        "description": "A year of planting seeds. Start new projects, establish independence, and take bold action. What you initiate now sets the tone for the next 9-year cycle.",
        "description_hi": "बीज बोने का वर्ष। नई परियोजनाएं शुरू करें, स्वतंत्रता स्थापित करें और साहसी कदम उठाएं। आप जो अभी शुरू करते हैं वह अगले 9 वर्षों के चक्र का आधार बनता है।",
        "focus": "Initiation, independence, leadership, self-development",
        "focus_hi": "शुरुआत, स्वतंत्रता, नेतृत्व, आत्म-विकास",
    },
    2: {
        "theme": "Cooperation & Patience", "theme_hi": "सहयोग और धैर्य",
        "description": "A year of relationships and diplomacy. Focus on partnerships, building trust, and developing patience. Progress is subtle but foundations are strengthening.",
        "description_hi": "रिश्तों और कूटनीति का वर्ष। साझेदारी पर ध्यान दें, विश्वास बनाएं और धैर्य विकसित करें। प्रगति सूक्ष्म है लेकिन नींव मजबूत हो रही है।",
        "focus": "Partnerships, diplomacy, emotional healing, listening",
        "focus_hi": "साझेदारी, कूटनीति, भावनात्मक उपचार, सुनना",
    },
    3: {
        "theme": "Expression & Growth", "theme_hi": "अभिव्यक्ति और विकास",
        "description": "A vibrant year of creativity and social expansion. Express yourself boldly — through art, writing, or communication. Joy and abundance follow authentic self-expression.",
        "description_hi": "रचनात्मकता और सामाजिक विस्तार का जीवंत वर्ष। साहसपूर्वक खुद को व्यक्त करें — कला, लेखन या संवाद के माध्यम से।",
        "focus": "Creativity, joy, socializing, self-expression, communication",
        "focus_hi": "रचनात्मकता, आनंद, सामाजिकता, आत्म-अभिव्यक्ति",
    },
    4: {
        "theme": "Work & Foundation", "theme_hi": "कार्य और नींव",
        "description": "A year of building and consolidating. Hard work, discipline, and practical systems are required. Avoid shortcuts — what you build now lasts decades.",
        "description_hi": "निर्माण और समेकन का वर्ष। कठिन परिश्रम, अनुशासन और व्यावहारिक प्रणालियां आवश्यक हैं। शॉर्टकट से बचें।",
        "focus": "Discipline, organization, health, career foundations, financial planning",
        "focus_hi": "अनुशासन, संगठन, स्वास्थ्य, करियर की नींव, वित्तीय योजना",
    },
    5: {
        "theme": "Freedom & Change", "theme_hi": "स्वतंत्रता और परिवर्तन",
        "description": "A dynamic year of change and new experiences. Travel, opportunities, and unexpected shifts keep life exciting. Stay adaptable and embrace transformation.",
        "description_hi": "परिवर्तन और नए अनुभवों का गतिशील वर्ष। यात्रा, अवसर और अप्रत्याशित बदलाव जीवन को रोमांचक बनाते हैं।",
        "focus": "Travel, change, freedom, versatility, adventure",
        "focus_hi": "यात्रा, परिवर्तन, स्वतंत्रता, बहुमुखी प्रतिभा, साहस",
    },
    6: {
        "theme": "Home & Responsibility", "theme_hi": "घर और जिम्मेदारी",
        "description": "A year of love, family, and service. Focus on home, relationships, and community. Healing occurs in close relationships when you lead with compassion.",
        "description_hi": "प्रेम, परिवार और सेवा का वर्ष। घर, रिश्तों और समुदाय पर ध्यान दें। करुणा के साथ नेतृत्व करने पर घनिष्ठ संबंधों में उपचार होता है।",
        "focus": "Family, home, service, healing, beauty, responsibility",
        "focus_hi": "परिवार, घर, सेवा, उपचार, सौंदर्य, जिम्मेदारी",
    },
    7: {
        "theme": "Reflection & Wisdom", "theme_hi": "चिंतन और ज्ञान",
        "description": "A year of inner work and spiritual deepening. Study, meditate, and go within. Answers come from silence, not external activity. Trust the process.",
        "description_hi": "आंतरिक कार्य और आध्यात्मिक गहराई का वर्ष। अध्ययन करें, ध्यान करें और भीतर जाएं। उत्तर मौन से आते हैं, बाहरी गतिविधि से नहीं।",
        "focus": "Spirituality, research, introspection, analysis, solitude",
        "focus_hi": "आध्यात्मिकता, शोध, आत्म-चिंतन, विश्लेषण, एकांत",
    },
    8: {
        "theme": "Power & Achievement", "theme_hi": "शक्ति और उपलब्धि",
        "description": "A year of material achievement and karmic harvest. Business, finance, and authority matters come to a head. Reap what you have sown in previous years.",
        "description_hi": "भौतिक उपलब्धि और कर्म फल का वर्ष। व्यवसाय, वित्त और अधिकार के मामले प्रमुख हो जाते हैं।",
        "focus": "Business, finances, career advancement, authority, manifestation",
        "focus_hi": "व्यापार, वित्त, करियर उन्नति, अधिकार, अभिव्यक्ति",
    },
    9: {
        "theme": "Completion & Release", "theme_hi": "समापन और मुक्ति",
        "description": "A year of endings and release. Let go of what no longer serves you — relationships, habits, beliefs. Compassionate service to others accelerates your own healing.",
        "description_hi": "अंत और मुक्ति का वर्ष। जो आपकी सेवा नहीं करता उसे जाने दें — रिश्ते, आदतें, विश्वास। दूसरों की करुणामय सेवा आपके अपने उपचार को तेज करती है।",
        "focus": "Completion, forgiveness, service, letting go, compassion",
        "focus_hi": "समापन, क्षमा, सेवा, त्याग, करुणा",
    },
}


def _personal_year_number(birth_date: str, target_year: int = None) -> int:
    """
    Personal Year Number = reduce(birth_month + birth_day + target_year_digits).
    Changes on January 1 of each year.
    """
    from datetime import date as _date
    if target_year is None:
        target_year = _date.today().year
    parts = birth_date.split("-")
    month_sum = _reduce_to_single(int(parts[1]))
    day_sum = _reduce_to_single(int(parts[2]))
    year_sum = _reduce_to_single(sum(int(d) for d in str(target_year)))
    return _reduce_to_single(month_sum + day_sum + year_sum)


def _life_path(birth_date: str) -> int:
    """
    Calculate life path number from birth date string (YYYY-MM-DD).
    Reduce each component (year, month, day) separately, then sum and reduce.
    """
    parts = birth_date.split('-')
    if len(parts) != 3:
        raise ValueError(f"Invalid birth_date format: {birth_date}. Expected YYYY-MM-DD.")

    year_str, month_str, day_str = parts

    # Reduce each part individually
    year_sum = _reduce_to_single(sum(int(d) for d in year_str))
    month_sum = _reduce_to_single(int(month_str))
    day_sum = _reduce_to_single(int(day_str))

    return _reduce_to_single(year_sum + month_sum + day_sum)


def _name_to_number(name: str) -> int:
    """Sum all letter values in name using Pythagorean mapping, then reduce."""
    total = 0
    for ch in name.upper():
        if ch in PYTHAGOREAN_MAP:
            total += PYTHAGOREAN_MAP[ch]
    return _reduce_to_single(total)


def _name_letter_breakdown(name: str) -> list:
    """Per-letter Pythagorean + Chaldean values with vowel/consonant classification."""
    result = []
    for ch in name.upper():
        if ch.isalpha():
            result.append({
                "letter": ch,
                "pythagorean": PYTHAGOREAN_MAP.get(ch, 0),
                "chaldean": CHALDEAN_MAP.get(ch, 0),
                "is_vowel": ch in VOWELS,
            })
    return result


def _vowels_number(name: str) -> int:
    """Sum vowel letter values in name (Soul Urge), then reduce."""
    total = 0
    for ch in name.upper():
        if ch in VOWELS and ch in PYTHAGOREAN_MAP:
            total += PYTHAGOREAN_MAP[ch]
    return _reduce_to_single(total)


def _consonants_number(name: str) -> int:
    """Sum consonant letter values in name (Personality), then reduce."""
    total = 0
    for ch in name.upper():
        if ch in PYTHAGOREAN_MAP and ch not in VOWELS:
            total += PYTHAGOREAN_MAP[ch]
    return _reduce_to_single(total)


def _chaldean_number(name: str) -> int:
    """Sum all letter values using Chaldean mapping, then reduce."""
    total = 0
    for ch in name.upper():
        if ch in CHALDEAN_MAP:
            total += CHALDEAN_MAP[ch]
    return _reduce_to_single(total)


# ============================================================
# PINNACLES, CHALLENGES, LIFE CYCLES
# ============================================================

def _determine_current_period(birth_date: str, first_end: int) -> int:
    """Return 1-indexed period number (1-4) based on current age.

    Periods:
        1: Birth to first_end
        2: first_end to first_end+9
        3: first_end+9 to first_end+18
        4: first_end+18 onward
    """
    from datetime import date as _date
    parts = birth_date.split('-')
    birth_year = int(parts[0])
    birth_month = int(parts[1])
    birth_day = int(parts[2])
    today = _date.today()
    age = today.year - birth_year
    if (today.month, today.day) < (birth_month, birth_day):
        age -= 1

    if age < first_end:
        return 1
    elif age < first_end + 9:
        return 2
    elif age < first_end + 18:
        return 3
    else:
        return 4


def _calculate_pinnacles(birth_date: str) -> dict:
    """Calculate 4 Pinnacle Numbers with timing and predictions.

    Args:
        birth_date: Date string in YYYY-MM-DD format.

    Returns:
        dict with 'pinnacles' list (4 items) and 'current_pinnacle' (1-indexed).
    """
    month = _reduce_to_single(int(birth_date[5:7]))
    day = _reduce_to_single(int(birth_date[8:10]))
    year = _reduce_to_single(sum(int(d) for d in birth_date[:4]))
    life_path = _life_path(birth_date)

    p1 = _reduce_to_single(month + day)       # First Pinnacle
    p2 = _reduce_to_single(day + year)         # Second Pinnacle
    p3 = _reduce_to_single(p1 + p2)            # Third Pinnacle
    p4 = _reduce_to_single(month + year)       # Fourth Pinnacle

    # Timing: First pinnacle ends at age (36 - life_path), minimum 27
    first_end = max(27, 36 - life_path)

    def _period_hi_birth_to(end_age: int) -> str:
        return f"जन्म से आयु {end_age} तक"

    def _period_hi_age_to(start_age: int, end_age: int) -> str:
        return f"आयु {start_age} से {end_age} तक"

    def _period_hi_age_plus(start_age: int) -> str:
        return f"आयु {start_age} से आगे"

    pinnacles = [
        {"number": p1, "period": f"Birth to age {first_end}", "period_hi": _period_hi_birth_to(first_end),
         "age_start": 0, "age_end": first_end,
         "prediction": PINNACLE_PREDICTIONS.get(p1, PINNACLE_PREDICTIONS[9])},
        {"number": p2, "period": f"Age {first_end} to {first_end + 9}", "period_hi": _period_hi_age_to(first_end, first_end + 9),
         "age_start": first_end, "age_end": first_end + 9,
         "prediction": PINNACLE_PREDICTIONS.get(p2, PINNACLE_PREDICTIONS[9])},
        {"number": p3, "period": f"Age {first_end + 9} to {first_end + 18}", "period_hi": _period_hi_age_to(first_end + 9, first_end + 18),
         "age_start": first_end + 9, "age_end": first_end + 18,
         "prediction": PINNACLE_PREDICTIONS.get(p3, PINNACLE_PREDICTIONS[9])},
        {"number": p4, "period": f"Age {first_end + 18}+", "period_hi": _period_hi_age_plus(first_end + 18),
         "age_start": first_end + 18, "age_end": 999,
         "prediction": PINNACLE_PREDICTIONS.get(p4, PINNACLE_PREDICTIONS[9])},
    ]

    return {
        "pinnacles": pinnacles,
        "current_pinnacle": _determine_current_period(birth_date, first_end),
    }


def _calculate_challenges(birth_date: str) -> dict:
    """Calculate 4 Challenge Numbers with timing and predictions.

    Args:
        birth_date: Date string in YYYY-MM-DD format.

    Returns:
        dict with 'challenges' list (4 items) and 'current_challenge' (1-indexed).
    """
    month = _reduce_to_single(int(birth_date[5:7]))
    day = _reduce_to_single(int(birth_date[8:10]))
    year = _reduce_to_single(sum(int(d) for d in birth_date[:4]))
    life_path = _life_path(birth_date)

    c1 = abs(month - day)            # First Challenge
    c2 = abs(day - year)             # Second Challenge
    c3 = abs(c1 - c2)               # Third (Main) Challenge
    c4 = abs(month - year)           # Fourth Challenge

    # Same timing as pinnacles
    first_end = max(27, 36 - life_path)

    def _period_hi_birth_to(end_age: int) -> str:
        return f"जन्म से आयु {end_age} तक"

    def _period_hi_age_to(start_age: int, end_age: int) -> str:
        return f"आयु {start_age} से {end_age} तक"

    def _period_hi_age_plus(start_age: int) -> str:
        return f"आयु {start_age} से आगे"

    challenges = [
        {"number": c1, "period": f"Birth to age {first_end}", "period_hi": _period_hi_birth_to(first_end),
         "age_start": 0, "age_end": first_end,
         "prediction": CHALLENGE_PREDICTIONS.get(c1, CHALLENGE_PREDICTIONS[0])},
        {"number": c2, "period": f"Age {first_end} to {first_end + 9}", "period_hi": _period_hi_age_to(first_end, first_end + 9),
         "age_start": first_end, "age_end": first_end + 9,
         "prediction": CHALLENGE_PREDICTIONS.get(c2, CHALLENGE_PREDICTIONS[0])},
        {"number": c3, "period": f"Age {first_end + 9} to {first_end + 18}", "period_hi": _period_hi_age_to(first_end + 9, first_end + 18),
         "age_start": first_end + 9, "age_end": first_end + 18,
         "prediction": CHALLENGE_PREDICTIONS.get(c3, CHALLENGE_PREDICTIONS[0])},
        {"number": c4, "period": f"Age {first_end + 18}+", "period_hi": _period_hi_age_plus(first_end + 18),
         "age_start": first_end + 18, "age_end": 999,
         "prediction": CHALLENGE_PREDICTIONS.get(c4, CHALLENGE_PREDICTIONS[0])},
    ]

    return {
        "challenges": challenges,
        "current_challenge": _determine_current_period(birth_date, first_end),
    }


def _calculate_life_cycles(birth_date: str) -> dict:
    """Calculate 3 Life Cycles with predictions.

    Args:
        birth_date: Date string in YYYY-MM-DD format.

    Returns:
        dict with 'cycles' list (3 items) and 'current_cycle' (1-indexed).
    """
    month_cycle = _reduce_to_single(int(birth_date[5:7]))   # Early life
    day_cycle = _reduce_to_single(int(birth_date[8:10]))     # Middle life
    year_cycle = _reduce_to_single(sum(int(d) for d in birth_date[:4]))  # Later life

    cycles = [
        {"number": month_cycle, "period": "Early Life (Birth to ~28)", "period_hi": "प्रारंभिक जीवन (जन्म से ~28)",
         "stage_note": "In early life, this number shapes identity formation, family patterns, and foundational beliefs.",
         "stage_note_hi": "प्रारंभिक जीवन में यह अंक पहचान, पारिवारिक स्वरूप और मूल विश्वासों को आकार देता है।",
         "theme": LIFE_CYCLE_PREDICTIONS.get(month_cycle, LIFE_CYCLE_PREDICTIONS[9])["theme"],
         "prediction": LIFE_CYCLE_PREDICTIONS.get(month_cycle, LIFE_CYCLE_PREDICTIONS[9])},
        {"number": day_cycle, "period": "Middle Life (~28 to ~56)", "period_hi": "मध्य जीवन (~28 से ~56)",
         "stage_note": "In middle life, this number governs career ambitions, relationships, and material achievement.",
         "stage_note_hi": "मध्य जीवन में यह अंक करियर, रिश्ते और भौतिक उपलब्धि को नियंत्रित करता है।",
         "theme": LIFE_CYCLE_PREDICTIONS.get(day_cycle, LIFE_CYCLE_PREDICTIONS[9])["theme"],
         "prediction": LIFE_CYCLE_PREDICTIONS.get(day_cycle, LIFE_CYCLE_PREDICTIONS[9])},
        {"number": year_cycle, "period": "Later Life (~56+)", "period_hi": "उत्तर जीवन (~56 से आगे)",
         "stage_note": "In later life, this number reflects legacy, wisdom, and spiritual completions.",
         "stage_note_hi": "उत्तर जीवन में यह अंक विरासत, ज्ञान और आध्यात्मिक पूर्णता को दर्शाता है।",
         "theme": LIFE_CYCLE_PREDICTIONS.get(year_cycle, LIFE_CYCLE_PREDICTIONS[9])["theme"],
         "prediction": LIFE_CYCLE_PREDICTIONS.get(year_cycle, LIFE_CYCLE_PREDICTIONS[9])},
    ]

    # Determine current cycle based on age
    from datetime import date as _date
    parts = birth_date.split('-')
    birth_year = int(parts[0])
    birth_month = int(parts[1])
    birth_day = int(parts[2])
    today = _date.today()
    age = today.year - birth_year
    if (today.month, today.day) < (birth_month, birth_day):
        age -= 1

    if age < 28:
        current_cycle = 1
    elif age < 56:
        current_cycle = 2
    else:
        current_cycle = 3

    return {
        "cycles": cycles,
        "current_cycle": current_cycle,
    }


def analyze_name_numerology(
    full_name: str,
    birth_date: str = "",
    name_type: str = "full_name"
) -> dict:
    """
    Comprehensive Name Numerology Analysis
    
    Args:
        full_name: The name to analyze (first, last, or full)
        birth_date: Optional DOB for compatibility analysis
        name_type: Type of name - 'first_name', 'last_name', 'full_name', 'business_name'
    
    Returns:
        dict with detailed name analysis including:
        - Pythagorean and Chaldean calculations
        - Vowel/Consonant analysis
        - First name / Last name breakdown
        - Detailed predictions
    """
    if not full_name or not full_name.strip():
        raise ValueError("Name cannot be empty")
    
    name_clean = full_name.strip()
    name_upper = name_clean.upper()
    
    # Split name into parts
    name_parts = name_clean.split()
    first_name = name_parts[0] if name_parts else ""
    last_name = name_parts[-1] if len(name_parts) > 1 else ""
    
    # Calculate numbers using different systems
    pythagorean_total = _name_to_number(name_clean)
    chaldean_total = _chaldean_number(name_clean)
    soul_urge = _vowels_number(name_clean)
    personality = _consonants_number(name_clean)
    
    # Individual name parts analysis
    first_name_number = _name_to_number(first_name) if first_name else 0
    last_name_number = _name_to_number(last_name) if last_name else 0
    
    # Get predictions
    pythagorean_prediction = NAME_NUMBER_PREDICTIONS.get(
        pythagorean_total, NAME_NUMBER_PREDICTIONS[1]
    )
    soul_urge_prediction = SOUL_URGE_PREDICTIONS.get(
        soul_urge, SOUL_URGE_PREDICTIONS[1]
    )
    personality_prediction = PERSONALITY_PREDICTIONS.get(
        personality, PERSONALITY_PREDICTIONS[1]
    )
    
    # Letter-by-letter breakdown
    letter_breakdown = []
    for ch in name_upper:
        if ch in PYTHAGOREAN_MAP:
            letter_breakdown.append({
                "letter": ch,
                "pythagorean": PYTHAGOREAN_MAP[ch],
                "chaldean": CHALDEAN_MAP.get(ch, 0),
                "is_vowel": ch in VOWELS
            })
    
    # Calculate compatibility with life path if birth_date provided
    life_path_compat = None
    if birth_date and '-' in birth_date:
        try:
            life_path = _life_path(birth_date)
            _lp_friends = PLANET_RELATIONSHIPS.get(life_path, {}).get("friends", set())
            _lp_enemies = PLANET_RELATIONSHIPS.get(life_path, {}).get("enemies", set())
            _name_friendly = pythagorean_total in _lp_friends or pythagorean_total == life_path
            _name_enemy = pythagorean_total in _lp_enemies
            life_path_compat = {
                "life_path": life_path,
                "name_number": pythagorean_total,
                "is_compatible": _name_friendly,
                "is_neutral": not _name_friendly and not _name_enemy,
                "compatibility_note": _get_name_life_path_compatibility(pythagorean_total, life_path)
            }
        except (ValueError, IndexError):
            pass
    
    # Lo Shu planes from DOB if birth_date provided
    loshu_analysis = None
    if birth_date and '-' in birth_date:
        try:
            dob_digits_name = [int(c) for c in birth_date.replace("-", "") if c.isdigit() and c != "0"]
            loshu_analysis = {
                "planes": analyze_loshu_planes(dob_digits_name),
                "arrows": analyze_loshu_arrows(dob_digits_name),
            }
        except Exception:
            pass

    result = {
        "name": name_clean,
        "name_type": name_type,
        "name_parts": {
            "first_name": first_name,
            "last_name": last_name,
            "total_parts": len(name_parts)
        },
        "numerology": {
            "pythagorean": {
                "number": pythagorean_total,
                "calculation": "A=1, B=2, C=3... (Western system)"
            },
            "chaldean": {
                "number": chaldean_total,
                "calculation": "Ancient Babylonian system"
            },
            "soul_urge": {
                "number": soul_urge,
                "description": "Inner desires from vowels"
            },
            "personality": {
                "number": personality,
                "description": "Outer expression from consonants"
            }
        },
        "first_name_analysis": {
            "name": first_name,
            "number": first_name_number,
            "traits": NAME_NUMBER_PREDICTIONS.get(first_name_number, {}).get("traits", [])
        } if first_name else None,
        "last_name_analysis": {
            "name": last_name,
            "number": last_name_number,
            "meaning": "Family karma and inherited traits"
        } if last_name else None,
        "loshu_analysis": loshu_analysis,
        "predictions": {
            "primary": pythagorean_prediction,
            "soul_urge": soul_urge_prediction,
            "personality": personality_prediction
        },
        "letter_breakdown": letter_breakdown,
        "life_path_compatibility": life_path_compat
    }

    return _normalize_focus_areas(result)


def _get_name_life_path_compatibility(name_num: int, life_path: int) -> str:
    """Get compatibility note between name number and life path."""
    if name_num == life_path:
        return "Perfect alignment! Your name naturally supports your life purpose."
    elif name_num in PLANET_RELATIONSHIPS.get(life_path, {}).get("friends", set()):
        return "Harmonious compatibility. Your name supports your life path."
    elif name_num in PLANET_RELATIONSHIPS.get(life_path, {}).get("enemies", set()):
        return "Challenging combination. Consider name spelling adjustments for better alignment."
    else:
        return "Neutral relationship. No major conflicts or special harmonies."


def calculate_vehicle_numerology(vehicle_number: str, owner_name: str = "", birth_date: str = "") -> dict:
    """
    Vehicle/Car Number Plate Numerology Analysis
    
    Args:
        vehicle_number: Vehicle registration number (e.g., "MH 01 AB 1234", "DL4CAX1234")
        owner_name: Optional owner's name
        birth_date: Optional owner's DOB for compatibility
    
    Returns:
        dict with vehicle numerology analysis
    """
    if not vehicle_number:
        raise ValueError("Vehicle number cannot be empty")
    
    # Extract digits from vehicle number
    digits_only = ''.join(ch for ch in vehicle_number if ch.isdigit())
    
    if not digits_only:
        raise ValueError("Vehicle number must contain at least one digit")
    
    # Calculate vehicle number (sum of all digits)
    total = sum(int(d) for d in digits_only)
    vehicle_number_vibration = _reduce_to_single(total)
    
    # Extract letters for analysis
    letters_only = ''.join(ch for ch in vehicle_number.upper() if ch.isalpha())
    letter_value = _name_to_number(letters_only) if letters_only else 0
    
    # Get prediction
    prediction = VEHICLE_PREDICTIONS.get(
        vehicle_number_vibration, VEHICLE_PREDICTIONS[1]
    )
    
    # Calculate owner compatibility if birth_date provided
    owner_compat = None
    if birth_date and '-' in birth_date:
        try:
            life_path = _life_path(birth_date)
            _veh_recommended = vehicle_number_vibration in RECOMMENDED_TOTALS.get(life_path, [])
            _veh_friendly = vehicle_number_vibration in PLANET_RELATIONSHIPS.get(life_path, {}).get("friends", set())
            _veh_enemy = vehicle_number_vibration in PLANET_RELATIONSHIPS.get(life_path, {}).get("enemies", set())
            owner_compat = {
                "owner_life_path": life_path,
                "vehicle_number": vehicle_number_vibration,
                "is_favorable": _veh_recommended or _veh_friendly,
                "is_neutral": not _veh_recommended and not _veh_friendly and not _veh_enemy,
                "recommendation": _get_vehicle_recommendation(vehicle_number_vibration, life_path)
            }
        except (ValueError, IndexError):
            pass
    
    # Analyze number patterns
    digit_analysis = []
    for i, d in enumerate(digits_only):
        digit_analysis.append({
            "position": i + 1,
            "digit": int(d),
            "meaning": _get_digit_meaning(int(d))
        })
    
    # Check for special combinations
    special_combinations = _check_special_combinations(digits_only)
    
    result = {
        "vehicle_number": vehicle_number,
        "digits_extracted": digits_only,
        "letters_extracted": letters_only,
        "vibration": {
            "number": vehicle_number_vibration,
            "digit_sum": total,
            "letter_value": letter_value
        },
        "prediction": prediction,
        "digit_analysis": digit_analysis,
        "special_combinations": special_combinations,
        "owner_compatibility": owner_compat,
        "lucky_days": NAME_NUMBER_PREDICTIONS.get(vehicle_number_vibration, {}).get("lucky_days", []),
        "lucky_colors": NAME_NUMBER_PREDICTIONS.get(vehicle_number_vibration, {}).get("lucky_colors", [])
    }
    
    return result


def _get_digit_meaning(digit: int) -> str:
    """Get the meaning of an individual digit."""
    meanings = {
        0: "Potential, void, cosmic connection",
        1: "Leadership, new beginnings, Sun energy",
        2: "Cooperation, Moon energy, diplomacy",
        3: "Creativity, Jupiter energy, expression",
        4: "Stability, Rahu energy, foundation",
        5: "Change, Mercury energy, freedom",
        6: "Love, Venus energy, harmony",
        7: "Mystery, Ketu energy, spirituality",
        8: "Power, Saturn energy, karma",
        9: "Completion, Mars energy, courage"
    }
    return meanings.get(digit, "Unknown")


def _check_special_combinations(digits: str) -> list:
    """Check for special number combinations in vehicle number."""
    combinations = []
    
    # Check for repeated digits
    for i in range(len(digits) - 1):
        if digits[i] == digits[i+1]:
            combinations.append({
                "type": "repeated_digit",
                "digits": digits[i:i+2],
                "meaning": f"Double {digits[i]} - Amplified {_get_digit_meaning(int(digits[i]))}"
            })
    
    # Check for ascending sequence
    if len(digits) >= 3:
        for i in range(len(digits) - 2):
            if int(digits[i+1]) == int(digits[i]) + 1 and int(digits[i+2]) == int(digits[i]) + 2:
                combinations.append({
                    "type": "ascending_sequence",
                    "digits": digits[i:i+3],
                    "meaning": "Ascending sequence - Progress and growth energy"
                })
    
    # Check for descending sequence
    if len(digits) >= 3:
        for i in range(len(digits) - 2):
            if int(digits[i+1]) == int(digits[i]) - 1 and int(digits[i+2]) == int(digits[i]) - 2:
                combinations.append({
                    "type": "descending_sequence",
                    "digits": digits[i:i+3],
                    "meaning": "Descending sequence - Release and completion energy"
                })
    
    # Master number check
    for master in ["11", "22", "33"]:
        if master in digits:
            combinations.append({
                "type": "master_number",
                "digits": master,
                "meaning": f"Master Number {master} - Special spiritual significance"
            })
    
    return combinations


def _get_vehicle_recommendation(vehicle_num: int, life_path: int) -> str:
    """Get vehicle recommendation based on life path."""
    recommended = RECOMMENDED_TOTALS.get(life_path, [])
    if vehicle_num in recommended:
        return "This vehicle number is highly favorable for you."
    elif vehicle_num in PLANET_RELATIONSHIPS.get(life_path, {}).get("friends", set()):
        return "This vehicle number is compatible with your life path."
    elif vehicle_num in PLANET_RELATIONSHIPS.get(life_path, {}).get("enemies", set()):
        return "This vehicle number may create challenges. Consider alternatives if possible."
    else:
        return "Neutral compatibility. No major concerns."


def calculate_house_numerology(address: str, birth_date: str = "") -> dict:
    """
    House/Property Address Numerology Analysis
    
    Args:
        address: Full address (e.g., "123 Main Street, Apt 4B")
        birth_date: Optional resident's DOB for compatibility
    
    Returns:
        dict with house numerology analysis
    """
    if not address:
        raise ValueError("Address cannot be empty")
    
    # Extract house number (digits at the beginning or standalone)
    address_upper = address.upper()
    
    # Try to extract house number - usually digits at start or before letters
    import re
    
    # Pattern to match house numbers (various formats: 123, 12B, A-123, etc.)
    patterns = [
        r'^(\d+)',  # Digits at start
        r'\b(\d+)[A-Z]?\b',  # Standalone digits optionally followed by letter
        r'APT\s*(\d+)',  # Apartment number
        r'UNIT\s*(\d+)',  # Unit number
        r'FLAT\s*(\d+)',  # Flat number
        r'#\s*(\d+)',  # # followed by number
    ]
    
    house_number = None
    house_number_raw = None
    
    for pattern in patterns:
        match = re.search(pattern, address_upper)
        if match:
            house_number_raw = match.group(1)
            house_number = int(house_number_raw)
            break
    
    if house_number is None:
        # If no house number found, use all digits
        all_digits = ''.join(ch for ch in address if ch.isdigit())
        if all_digits:
            house_number = int(all_digits)
            house_number_raw = all_digits
        else:
            raise ValueError("Could not extract house number from address")
    
    # Calculate house vibration
    house_vibration = _reduce_to_single(sum(int(d) for d in str(house_number)))
    
    # Get prediction
    prediction = HOUSE_PREDICTIONS.get(house_vibration, HOUSE_PREDICTIONS[1])
    
    # Street name analysis
    street_name = _extract_street_name(address)
    street_number = _name_to_number(street_name) if street_name else 0
    
    # Resident compatibility
    resident_compat = None
    if birth_date and '-' in birth_date:
        try:
            life_path = _life_path(birth_date)
            _house_recommended = house_vibration in RECOMMENDED_TOTALS.get(life_path, [])
            _house_friendly = house_vibration in PLANET_RELATIONSHIPS.get(life_path, {}).get("friends", set())
            _house_enemy = house_vibration in PLANET_RELATIONSHIPS.get(life_path, {}).get("enemies", set())
            resident_compat = {
                "resident_life_path": life_path,
                "house_number": house_vibration,
                "is_ideal": _house_recommended or house_vibration == life_path,
                "is_neutral": not _house_recommended and not _house_friendly and not _house_enemy and house_vibration != life_path,
                "compatibility_score": _calculate_house_compatibility(house_vibration, life_path),
                "recommendation": _get_house_recommendation(house_vibration, life_path)
            }
        except (ValueError, IndexError):
            pass
    
    # Analyze house number components
    house_digit_analysis = []
    for d in str(house_number):
        house_digit_analysis.append({
            "digit": int(d),
            "meaning": _get_digit_meaning(int(d))
        })
    
    result = {
        "address": address,
        "house_number": {
            "raw": house_number_raw,
            "numeric": house_number,
            "vibration": house_vibration
        },
        "street_name": {
            "name": street_name,
            "numerology": street_number,
            "influence": "Secondary influence from street energy"
        } if street_name else None,
        "prediction": prediction,
        "digit_analysis": house_digit_analysis,
        "resident_compatibility": resident_compat,
        "remedies": prediction.get("remedies", []),
        "enhancement_tips": _get_house_enhancement_tips(house_vibration),
        "enhancement_tips_hi": _get_house_enhancement_tips_hi(house_vibration)
    }
    
    return result


def _extract_street_name(address: str) -> str:
    """Extract street name from address."""
    import re
    
    # Remove house number and common suffixes
    cleaned = re.sub(r'^\d+[A-Z]?\s*', '', address.upper())
    cleaned = re.sub(r'\b(STREET|ST|ROAD|RD|AVENUE|AVE|BOULEVARD|BLVD|LANE|LN|DRIVE|DR|WAY|COURT|CT|PLACE|PL)\b.*', '', cleaned)
    cleaned = re.sub(r'\b(APARTMENT|APT|UNIT|FLAT|#)\b.*', '', cleaned)
    cleaned = re.sub(r',.*', '', cleaned)
    
    return cleaned.strip()


def _calculate_house_compatibility(house_num: int, life_path: int) -> str:
    """Calculate compatibility score between house and resident."""
    if house_num == life_path:
        return "Excellent - Perfect match for your life path"
    elif house_num in RECOMMENDED_TOTALS.get(life_path, []):
        return "Very Good - Highly favorable for you"
    elif house_num in PLANET_RELATIONSHIPS.get(life_path, {}).get("friends", set()):
        return "Good - Harmonious energy"
    elif house_num in PLANET_RELATIONSHIPS.get(life_path, {}).get("enemies", set()):
        return "Challenging - May require remedies"
    else:
        return "Neutral - No strong influence"


def _get_house_recommendation(house_num: int, life_path: int) -> str:
    """Get house recommendation based on life path."""
    score = _calculate_house_compatibility(house_num, life_path)
    
    if "Excellent" in score or "Very Good" in score:
        return "This house is ideal for you. The energy supports your life path perfectly."
    elif "Good" in score:
        return "This house is favorable. You should thrive here with minimal adjustments."
    elif "Challenging" in score:
        return "This house presents challenges. Consider Vastu remedies or keep looking."
    else:
        return "This house has neutral energy. Personal effort will determine your experience."


def _get_house_enhancement_tips(house_num: int) -> list:
    """Get tips to enhance house energy."""
    tips = {
        1: ["Place a red doormat", "Keep East direction open", "Display awards and achievements"],
        2: ["Use pairs of decorative items", "Place white flowers in North-West", "Create cozy nooks"],
        3: ["Display artwork and creative pieces", "Use yellow accents", "Create a social space"],
        4: ["Organize and declutter", "Use square-shaped furniture", "Create structured spaces"],
        5: ["Keep center of home empty or light", "Use green plants", "Allow for flexibility"],
        6: ["Create a beautiful entrance", "Use pink or white flowers", "Focus on family spaces"],
        7: ["Create a meditation corner", "Use purple or green accents", "Keep a library or study"],
        8: ["Place heavy furniture in South-West", "Use dark colors sparingly", "Create an office space"],
        9: ["Place red accents in South", "Welcome guests warmly", "Create space for gatherings"],
    }
    return tips.get(house_num, ["Keep home clean and organized", "Balance the 5 elements"])


def _get_house_enhancement_tips_hi(house_num: int) -> list:
    """Hindi enhancement tips to enhance house energy."""
    tips = {
        1: ["लाल डोरमैट रखें", "पूर्व दिशा खुली रखें", "पुरस्कार और उपलब्धियां प्रदर्शित करें"],
        2: ["सजावटी वस्तुओं की जोड़ियां उपयोग करें", "उत्तर-पश्चिम में सफेद फूल रखें", "आरामदायक कोने बनाएं"],
        3: ["कलाकृतियां और रचनात्मक वस्तुएं प्रदर्शित करें", "पीले रंग के उच्चारण उपयोग करें", "सामाजिक स्थान बनाएं"],
        4: ["व्यवस्थित और अव्यवस्था दूर करें", "वर्गाकार फर्नीचर उपयोग करें", "संरचित स्थान बनाएं"],
        5: ["घर का केंद्र हल्का या खाली रखें", "हरे पौधे उपयोग करें", "लचीलेपन की अनुमति दें"],
        6: ["सुंदर प्रवेश द्वार बनाएं", "गुलाबी या सफेद फूल उपयोग करें", "पारिवारिक स्थानों पर ध्यान दें"],
        7: ["ध्यान कोना बनाएं", "बैंगनी या हरे रंग के उच्चारण उपयोग करें", "पुस्तकालय या अध्ययन कक्ष रखें"],
        8: ["दक्षिण-पश्चिम में भारी फर्नीचर रखें", "गहरे रंगों का कम उपयोग करें", "कार्यालय स्थान बनाएं"],
        9: ["दक्षिण में लाल उच्चारण रखें", "अतिथियों का गर्मजोशी से स्वागत करें", "समारोहों के लिए जगह बनाएं"],
    }
    return tips.get(house_num, ["घर साफ और व्यवस्थित रखें", "5 तत्वों का संतुलन बनाएं"])


# ============================================================
# CORE NUMBERS: Birthday, Maturity, Karmic Debt, Hidden Passion,
#               Subconscious Self, Karmic Lessons
# ============================================================

def _birthday_number(birth_date: str) -> int:
    """Birthday Number — birth day reduced to single digit or master number."""
    return _reduce_to_single(int(birth_date[8:10]))

def _maturity_number(life_path: int, expression: int) -> int:
    """Maturity Number — Life Path + Expression, reduced."""
    return _reduce_to_single(life_path + expression)

def _detect_karmic_debt(birth_date: str, name: str) -> list:
    """Detect Karmic Debt numbers (13, 14, 16, 19) in intermediate sums."""
    KARMIC = {13, 14, 16, 19}
    debts = []

    def _trace_reduction(n: int) -> list:
        """
        Return all intermediate values encountered during digit-sum reduction.
        Example: 1990 year digit-sum is 19 -> [19, 10, 1]
        We intentionally keep 11/22/33 as terminal values, but karmic-debt
        detection is about 13/14/16/19 anywhere in the chain.
        """
        vals = [int(n)]
        cur = int(n)
        while cur > 9 and cur not in (11, 22, 33):
            cur = sum(int(c) for c in str(cur))
            vals.append(cur)
        return vals

    def _add_debt(num: int, source: str, source_hi: str) -> None:
        debts.append({"number": num, "source": source, "source_hi": source_hi})

    # DOB components
    m = int(birth_date[5:7])
    d = int(birth_date[8:10])
    y_digit_sum = sum(int(c) for c in birth_date[:4])  # e.g. 1990 -> 19

    # Birthday/day can itself be a karmic-debt number (13/14/16/19)
    for hit in _trace_reduction(d):
        if hit in KARMIC:
            _add_debt(hit, "birthday", "जन्म तिथि")
            break

    # Year digit-sum can be a karmic-debt number (common case: 19)
    for hit in _trace_reduction(y_digit_sum):
        if hit in KARMIC:
            _add_debt(hit, "birth_year", "जन्म वर्ष")
            break

    # Life path intermediate sum (month/day/year reduced then added) can also be karmic.
    mr = _reduce_to_single(m)
    dr = _reduce_to_single(d)
    yr = _reduce_to_single(y_digit_sum)
    lp_sum = mr + dr + yr
    for hit in _trace_reduction(lp_sum):
        if hit in KARMIC:
            _add_debt(hit, "life_path", "मूलांक")
            break

    # Name sums: Expression, Soul Urge, Personality (scan reduction trace, not just raw total)
    exp_raw = sum(PYTHAGOREAN_MAP.get(c.upper(), 0) for c in name if c.isalpha())
    for hit in _trace_reduction(exp_raw):
        if hit in KARMIC:
            _add_debt(hit, "expression", "भाग्यांक")
            break

    vowels = set("AEIOUaeiou")
    su_raw = sum(PYTHAGOREAN_MAP.get(c.upper(), 0) for c in name if c.isalpha() and c in vowels)
    for hit in _trace_reduction(su_raw):
        if hit in KARMIC:
            _add_debt(hit, "soul_urge", "आत्मांक")
            break

    con_raw = sum(PYTHAGOREAN_MAP.get(c.upper(), 0) for c in name if c.isalpha() and c not in vowels)
    for hit in _trace_reduction(con_raw):
        if hit in KARMIC:
            _add_debt(hit, "personality", "व्यक्तित्व अंक")
            break

    # Deduplicate (same debt may be found via multiple traces)
    seen = set()
    uniq = []
    for it in debts:
        k = (it.get("number"), it.get("source"))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(it)
    debts = uniq

    # Add interpretations
    for d in debts:
        interp = KARMIC_DEBT_INTERPRETATIONS.get(d["number"], {})
        # Keep legacy flattened keys (title/meaning/title_hi/meaning_hi) for UI,
        # but also expose a structured "interpretation" field for tests/consumers.
        d["interpretation"] = interp
        d.update(interp)
    return debts

KARMIC_DEBT_INTERPRETATIONS = {
    13: {"title": "Hard Work", "title_hi": "कठिन परिश्रम", "meaning": "Past-life laziness. Must work diligently, no shortcuts.", "meaning_hi": "पूर्व जन्म में आलस्य। कठिन परिश्रम करें, शॉर्टकट नहीं।"},
    14: {"title": "Freedom & Discipline", "title_hi": "स्वतंत्रता और अनुशासन", "meaning": "Past abuse of freedom. Must exercise moderation and self-control.", "meaning_hi": "स्वतंत्रता का दुरुपयोग। संयम और आत्म-नियंत्रण अपनाएं।"},
    16: {"title": "Ego Destruction", "title_hi": "अहंकार विनाश", "meaning": "Past vanity and ego. Ego will be destroyed to rebuild spiritually.", "meaning_hi": "पूर्व जन्म में अहंकार। आध्यात्मिक पुनर्निर्माण के लिए अहंकार नष्ट होगा।"},
    19: {"title": "Independence", "title_hi": "स्वावलंबन", "meaning": "Past selfishness. Must learn to stand alone while helping others.", "meaning_hi": "पूर्व जन्म में स्वार्थ। दूसरों की मदद करते हुए स्वावलंबी बनें।"},
}

def _hidden_passion(name: str) -> dict:
    """Hidden Passion — most repeated number (1-9) in full name."""
    counts = {}
    for c in name:
        if c.isalpha():
            n = PYTHAGOREAN_MAP.get(c.upper(), 0)
            if n: counts[n] = counts.get(n, 0) + 1
    if not counts: return {"number": 0, "count": 0, "tie_detected": False, "tied_numbers": []}
    # Deterministic tie-break: pick the smallest digit among the top counts.
    max_count = max(counts.values())
    top_nums = sorted(n for n, c in counts.items() if c == max_count)
    tie_detected = len(top_nums) > 1
    max_num = top_nums[0]
    return {
        "number": max_num,
        "count": counts[max_num],
        "tie_detected": tie_detected,
        "tied_numbers": top_nums if tie_detected else [],
        "tied_meanings": {str(n): HIDDEN_PASSION_PREDICTIONS.get(n, {}) for n in top_nums} if tie_detected else {},
        **HIDDEN_PASSION_PREDICTIONS.get(max_num, {}),
    }

HIDDEN_PASSION_PREDICTIONS = {
    1: {"title": "Leadership Drive", "title_hi": "नेतृत्व क्षमता", "meaning": "Passionate about independence and leading.", "meaning_hi": "स्वतंत्रता और नेतृत्व के प्रति जुनूनी।"},
    2: {"title": "Partnership", "title_hi": "साझेदारी", "meaning": "Deep need for harmony and cooperation.", "meaning_hi": "सामंजस्य और सहयोग की गहरी आवश्यकता।"},
    3: {"title": "Creative Expression", "title_hi": "रचनात्मक अभिव्यक्ति", "meaning": "Burning desire to express creatively.", "meaning_hi": "रचनात्मक अभिव्यक्ति की तीव्र इच्छा।"},
    4: {"title": "Stability Builder", "title_hi": "स्थिरता निर्माता", "meaning": "Driven to build solid foundations.", "meaning_hi": "मजबूत नींव बनाने की प्रेरणा।"},
    5: {"title": "Freedom Seeker", "title_hi": "स्वतंत्रता खोजी", "meaning": "Passionate about variety and adventure.", "meaning_hi": "विविधता और रोमांच के प्रति जुनूनी।"},
    6: {"title": "Nurturer", "title_hi": "पालनकर्ता", "meaning": "Deep desire to nurture and protect.", "meaning_hi": "पालन-पोषण और रक्षा की गहरी इच्छा।"},
    7: {"title": "Truth Seeker", "title_hi": "सत्य खोजी", "meaning": "Driven to understand deeper truths.", "meaning_hi": "गहरे सत्य को समझने की प्रेरणा।"},
    8: {"title": "Power & Achievement", "title_hi": "शक्ति और उपलब्धि", "meaning": "Passionate about material success.", "meaning_hi": "भौतिक सफलता के प्रति जुनूनी।"},
    9: {"title": "Humanitarian", "title_hi": "मानवतावादी", "meaning": "Deep compassion for humanity.", "meaning_hi": "मानवता के प्रति गहरी करुणा।"},
}

def _subconscious_self(name: str) -> dict:
    """Subconscious Self — count of distinct numbers (1-9) present in name."""
    present = set()
    for c in name:
        if c.isalpha():
            n = PYTHAGOREAN_MAP.get(c.upper(), 0)
            if n: present.add(n)
    missing = [n for n in range(1, 10) if n not in present]
    count = len(present)
    return {"number": count, "missing_count": len(missing), "missing_numbers": missing, **SUBCONSCIOUS_SELF_PREDICTIONS.get(count, {})}

SUBCONSCIOUS_SELF_PREDICTIONS = {
    3: {"title": "Scattered", "title_hi": "बिखरा हुआ", "meaning": "Many gaps in skills; easily overwhelmed.", "meaning_hi": "कौशल में कई कमियां; आसानी से अभिभूत।"},
    4: {"title": "Developing", "title_hi": "विकासशील", "meaning": "Several areas need growth.", "meaning_hi": "कई क्षेत्रों में विकास आवश्यक।"},
    5: {"title": "Balanced", "title_hi": "संतुलित", "meaning": "Average inner resources; can handle most situations.", "meaning_hi": "औसत आंतरिक संसाधन।"},
    6: {"title": "Capable", "title_hi": "सक्षम", "meaning": "Good inner strength; handles pressure well.", "meaning_hi": "अच्छी आंतरिक शक्ति।"},
    7: {"title": "Strong", "title_hi": "मजबूत", "meaning": "High inner resources; rarely caught off guard.", "meaning_hi": "उच्च आंतरिक संसाधन।"},
    8: {"title": "Very Strong", "title_hi": "बहुत मजबूत", "meaning": "Almost complete inner toolkit.", "meaning_hi": "लगभग पूर्ण आंतरिक क्षमता।"},
    9: {"title": "Complete", "title_hi": "पूर्ण", "meaning": "All 9 numbers present — complete inner strength.", "meaning_hi": "सभी 9 अंक उपस्थित — पूर्ण आंतरिक शक्ति।"},
}

def _karmic_lessons(name: str) -> list:
    """Karmic Lessons — numbers 1-9 absent from full birth name."""
    present = set()
    for c in name:
        if c.isalpha():
            n = PYTHAGOREAN_MAP.get(c.upper(), 0)
            if n: present.add(n)
    lessons = []
    for n in range(1, 10):
        if n not in present:
            entry = {"number": n, **KARMIC_LESSON_INTERPRETATIONS.get(n, {})}
            remedy = MISSING_NUMBER_REMEDIES.get(n, {})
            entry["gemstone"] = remedy.get("gemstone", "")
            entry["gemstone_hi"] = remedy.get("gemstone_hi", "")
            entry["planet"] = remedy.get("planet", "")
            lessons.append(entry)
    return lessons

KARMIC_LESSON_INTERPRETATIONS = {
    1: {"lesson": "Develop confidence and assertiveness.", "lesson_hi": "आत्मविश्वास और दृढ़ता विकसित करें।", "remedy": "Wear red, lead projects.", "remedy_hi": "लाल रंग पहनें, परियोजनाओं का नेतृत्व करें।"},
    2: {"lesson": "Learn patience and cooperation.", "lesson_hi": "धैर्य और सहयोग सीखें।", "remedy": "Practice diplomacy, wear white/cream.", "remedy_hi": "कूटनीति अपनाएं, सफेद/क्रीम पहनें।"},
    3: {"lesson": "Express yourself creatively.", "lesson_hi": "रचनात्मक रूप से अभिव्यक्ति करें।", "remedy": "Write, sing, paint. Wear yellow.", "remedy_hi": "लिखें, गाएं, चित्रकारी करें। पीला पहनें।"},
    4: {"lesson": "Build discipline and structure.", "lesson_hi": "अनुशासन और व्यवस्था बनाएं।", "remedy": "Follow routines, wear blue.", "remedy_hi": "दिनचर्या का पालन करें, नीला पहनें।"},
    5: {"lesson": "Embrace change and adaptability.", "lesson_hi": "परिवर्तन और अनुकूलता अपनाएं।", "remedy": "Travel, try new things. Wear grey.", "remedy_hi": "यात्रा करें, नई चीज़ें आज़माएं। भूरा पहनें।"},
    6: {"lesson": "Accept responsibility for others.", "lesson_hi": "दूसरों के लिए जिम्मेदारी स्वीकारें।", "remedy": "Serve family, wear pink.", "remedy_hi": "परिवार की सेवा करें, गुलाबी पहनें।"},
    7: {"lesson": "Develop spiritual depth.", "lesson_hi": "आध्यात्मिक गहराई विकसित करें।", "remedy": "Meditate, study philosophy. Wear purple.", "remedy_hi": "ध्यान करें, दर्शनशास्त्र पढ़ें। बैंगनी पहनें।"},
    8: {"lesson": "Master money and material world.", "lesson_hi": "धन और भौतिक जगत में महारत हासिल करें।", "remedy": "Budget carefully, wear dark tones.", "remedy_hi": "बजट सावधानी से बनाएं, गहरे रंग पहनें।"},
    9: {"lesson": "Develop compassion and selflessness.", "lesson_hi": "करुणा और निस्वार्थता विकसित करें।", "remedy": "Volunteer, help others. Wear gold.", "remedy_hi": "स्वयंसेवा करें, दूसरों की मदद करें। सुनहरा पहनें।"},
}

BIRTHDAY_PREDICTIONS = {
    # Single-digit base days (1–9)
    1: {"title": "The Leader", "title_hi": "नेता", "talent": "Natural leadership and originality.", "talent_hi": "प्राकृतिक नेतृत्व और मौलिकता।"},
    2: {"title": "The Diplomat", "title_hi": "राजनयिक", "talent": "Mediation and partnership skills.", "talent_hi": "मध्यस्थता और साझेदारी कौशल।"},
    3: {"title": "The Communicator", "title_hi": "संवादक", "talent": "Gifted self-expression and creativity.", "talent_hi": "प्रतिभाशाली आत्म-अभिव्यक्ति और रचनात्मकता।"},
    4: {"title": "The Builder", "title_hi": "निर्माता", "talent": "Systematic and disciplined approach.", "talent_hi": "व्यवस्थित और अनुशासित दृष्टिकोण।"},
    5: {"title": "The Adventurer", "title_hi": "साहसी", "talent": "Versatility and quick thinking.", "talent_hi": "बहुमुखी प्रतिभा और तीव्र सोच।"},
    6: {"title": "The Nurturer", "title_hi": "पालनकर्ता", "talent": "Caring and responsibility.", "talent_hi": "देखभाल और जिम्मेदारी।"},
    7: {"title": "The Analyst", "title_hi": "विश्लेषक", "talent": "Deep thinking and spiritual insight.", "talent_hi": "गहन चिंतन और आध्यात्मिक अंतर्दृष्टि।"},
    8: {"title": "The Achiever", "title_hi": "उपलब्धिकर्ता", "talent": "Business acumen and ambition.", "talent_hi": "व्यापार कौशल और महत्वाकांक्षा।"},
    9: {"title": "The Humanitarian", "title_hi": "मानवतावादी", "talent": "Compassion and global vision.", "talent_hi": "करुणा और वैश्विक दृष्टि।"},
    # Compound days 10–31 — each with unique identity
    10: {"title": "The Reinventor", "title_hi": "पुनर्आविष्कारक", "talent": "Ambition backed by creative reinvention; born to lead through innovation.", "talent_hi": "रचनात्मक पुनर्आविष्कार से समर्थित महत्वाकांक्षा; नवाचार के माध्यम से नेतृत्व करने के लिए जन्मे।"},
    11: {"title": "The Illuminator", "title_hi": "प्रकाशक", "talent": "Spiritual inspiration and intuition.", "talent_hi": "आध्यात्मिक प्रेरणा और अंतर्ज्ञान।"},
    12: {"title": "The Communicative Builder", "title_hi": "संवादी निर्माता", "talent": "Blending practical creativity with expressive communication to inspire and construct.", "talent_hi": "व्यावहारिक रचनात्मकता और अभिव्यंजक संचार का समन्वय करके प्रेरणा देना और निर्माण करना।"},
    13: {"title": "The Transformer", "title_hi": "परिवर्तक", "talent": "Karmic hard work and discipline that transforms obstacles into foundations.", "talent_hi": "कार्मिक कठिन परिश्रम और अनुशासन जो बाधाओं को नींव में बदलता है।"},
    14: {"title": "The Freedom Seeker", "title_hi": "स्वतंत्रता-खोजी", "talent": "Karmic adaptability and transformative change; thrives amid constant movement.", "talent_hi": "कार्मिक अनुकूलनशीलता और परिवर्तनकारी बदलाव; निरंतर गति के बीच फलते-फूलते हैं।"},
    15: {"title": "The Harmonizer", "title_hi": "सामंजस्य-स्थापक", "talent": "Weaving love, creativity, and responsibility into harmonious living.", "talent_hi": "प्यार, रचनात्मकता और जिम्मेदारी को सामंजस्यपूर्ण जीवन में पिरोना।"},
    16: {"title": "The Spiritual Seeker", "title_hi": "आध्यात्मिक-अन्वेषी", "talent": "Karmic introspection and wisdom; truth emerges through solitude and reflection.", "talent_hi": "कार्मिक आत्मनिरीक्षण और ज्ञान; एकांत और चिंतन के माध्यम से सत्य प्रकट होता है।"},
    17: {"title": "The Achiever", "title_hi": "उच्च-उपलब्धिकर्ता", "talent": "Material power combined with spiritual depth; ambition rooted in integrity.", "talent_hi": "भौतिक शक्ति और आध्यात्मिक गहराई का संयोजन; ईमानदारी में निहित महत्वाकांक्षा।"},
    18: {"title": "The Compassionate Leader", "title_hi": "करुणामय नेता", "talent": "Courage meets humanitarianism; leads with both strength and deep empathy.", "talent_hi": "साहस और मानवतावाद का मिलन; शक्ति और गहरी सहानुभूति दोनों से नेतृत्व करना।"},
    19: {"title": "The Independent Humanitarian", "title_hi": "स्वतंत्र मानवतावादी", "talent": "Karmic individuality fused with generosity; self-reliant service to all.", "talent_hi": "कार्मिक व्यक्तित्व और उदारता का संयोजन; सभी की स्वतंत्र सेवा।"},
    20: {"title": "The Peacemaker", "title_hi": "शांतिदूत", "talent": "Sensitivity and deep cooperation; brings harmony through gentle understanding.", "talent_hi": "संवेदनशीलता और गहरा सहयोग; कोमल समझ से सामंजस्य लाना।"},
    21: {"title": "The Creative Communicator", "title_hi": "रचनात्मक संवादक", "talent": "Expressive leadership that uplifts through joyful self-expression.", "talent_hi": "अभिव्यंजक नेतृत्व जो आनंदमय आत्म-अभिव्यक्ति से उत्थान करता है।"},
    22: {"title": "The Master Builder", "title_hi": "मास्टर निर्माता", "talent": "Turning grand visions into reality.", "talent_hi": "भव्य दृष्टिकोण को वास्तविकता में बदलना।"},
    23: {"title": "The Versatile Communicator", "title_hi": "बहुमुखी संवादक", "talent": "Freedom of expression across many fields; adapts and communicates with ease.", "talent_hi": "अनेक क्षेत्रों में अभिव्यक्ति की स्वतंत्रता; आसानी से अनुकूल होना और संवाद करना।"},
    24: {"title": "The Family Builder", "title_hi": "परिवार-निर्माता", "talent": "Deep love, harmony, and unwavering dedication to family and community.", "talent_hi": "गहरा प्रेम, सामंजस्य और परिवार एवं समुदाय के प्रति अटल समर्पण।"},
    25: {"title": "The Spiritual Analyst", "title_hi": "आध्यात्मिक विश्लेषक", "talent": "Reflective wisdom translated into meaningful action in the world.", "talent_hi": "चिंतनशील ज्ञान को दुनिया में अर्थपूर्ण कार्यों में अनुवादित करना।"},
    26: {"title": "The Ambitious Nurturer", "title_hi": "महत्वाकांक्षी पालनकर्ता", "talent": "Material success earned through responsibility and service to others.", "talent_hi": "जिम्मेदारी और दूसरों की सेवा के माध्यम से अर्जित भौतिक सफलता।"},
    27: {"title": "The Inspiring Humanitarian", "title_hi": "प्रेरक मानवतावादी", "talent": "Compassion and wisdom combined into visionary humanitarian work.", "talent_hi": "करुणा और ज्ञान का दूरदर्शी मानवतावादी कार्य में संयोजन।"},
    28: {"title": "The Independent Builder", "title_hi": "स्वतंत्र निर्माता", "talent": "Leadership in foundation-building; forges lasting structures through self-driven effort.", "talent_hi": "नींव-निर्माण में नेतृत्व; स्व-चालित प्रयास से स्थायी संरचनाएं बनाना।"},
    29: {"title": "The Master Intuitive", "title_hi": "मास्टर अंतर्बोधी", "talent": "Spiritual sensitivity and deep intuition carrying the amplified energy of 11.", "talent_hi": "आध्यात्मिक संवेदनशीलता और गहरा अंतर्ज्ञान जो 11 की प्रवर्धित ऊर्जा धारण करता है।"},
    30: {"title": "The Joyful Expresser", "title_hi": "आनंदमय अभिव्यक्तिकार", "talent": "Boundless creativity and optimism; uplifts others through joyful expression.", "talent_hi": "असीम रचनात्मकता और आशावाद; आनंदमय अभिव्यक्ति से दूसरों का उत्थान।"},
    31: {"title": "The Disciplined Creator", "title_hi": "अनुशासित सृजक", "talent": "Structured creativity that turns disciplined effort into enduring artistic legacy.", "talent_hi": "संरचित रचनात्मकता जो अनुशासित प्रयास को स्थायी कलात्मक विरासत में बदलती है।"},
    # Master number 33 — for lookup when birthday reduces to the master healer vibration
    33: {"title": "The Master Healer", "title_hi": "मास्टर उपचारक", "talent": "Selfless compassion and creative healing; born to uplift humanity through unconditional love.", "talent_hi": "निस्वार्थ करुणा और रचनात्मक उपचार; बिना शर्त प्रेम से मानवता का उत्थान करने के लिए जन्मे।"},
}

MATURITY_PREDICTIONS = {
    1: {
        "title": "Independent Maturity", "title_hi": "स्वतंत्र परिपक्वता",
        "theme": "Growing into leadership and self-reliance after 35-40.", "theme_hi": "35-40 के बाद नेतृत्व और आत्मनिर्भरता में विकास।",
        "description": "In your mature years the call to lead becomes undeniable. You step fully into originality, shed the need for external validation, and forge your own path with quiet confidence.",
        "description_hi": "परिपक्व वर्षों में नेतृत्व की पुकार अनिवार्य हो जाती है। आप पूरी तरह मौलिकता में कदम रखते हैं, बाहरी स्वीकृति की ज़रूरत छोड़ते हैं और शांत आत्मविश्वास से अपना मार्ग बनाते हैं।",
        "advice": "Embrace solo ventures and trust your instincts — your greatest achievements come when you act first and seek approval later.",
        "advice_hi": "एकल उद्यमों को अपनाएं और अपनी प्रवृत्ति पर भरोसा रखें — आपकी सबसे बड़ी उपलब्धियां तब आती हैं जब आप पहले कार्य करते हैं और बाद में अनुमोदन मांगते हैं।",
    },
    2: {
        "title": "Diplomatic Maturity", "title_hi": "कूटनीतिक परिपक्वता",
        "theme": "Deepening relationships and finding inner peace.", "theme_hi": "संबंध गहरे होना और आंतरिक शांति।",
        "description": "Maturity brings you the gift of deep, meaningful connection. You become a master mediator, valued for your empathy and capacity to hold space for others' emotions.",
        "description_hi": "परिपक्वता आपको गहरे, अर्थपूर्ण संबंध का उपहार लाती है। आप एक कुशल मध्यस्थ बनते हैं, अपनी सहानुभूति और दूसरों की भावनाओं के लिए जगह बनाने की क्षमता के लिए सम्मानित होते हैं।",
        "advice": "Invest in one or two deep relationships rather than spreading your emotional energy thin across many.",
        "advice_hi": "अपनी भावनात्मक ऊर्जा को अनेक लोगों में बिखेरने की बजाय एक या दो गहरे संबंधों में निवेश करें।",
    },
    3: {
        "title": "Creative Maturity", "title_hi": "रचनात्मक परिपक्वता",
        "theme": "Full creative expression blooms in later years.", "theme_hi": "बाद के वर्षों में पूर्ण रचनात्मक अभिव्यक्ति।",
        "description": "The second half of life becomes your creative renaissance. Years of experience fuel your artistic expression and your communication gifts reach their richest, most nuanced form.",
        "description_hi": "जीवन का दूसरा भाग आपका रचनात्मक पुनर्जागरण बन जाता है। वर्षों का अनुभव आपकी कलात्मक अभिव्यक्ति को पोषित करता है और आपके संचार उपहार अपने सबसे समृद्ध, सूक्ष्म रूप में पहुंचते हैं।",
        "advice": "Pick one creative medium and commit to mastering it — depth of craft will bring you more fulfillment than scattered dabbling.",
        "advice_hi": "एक रचनात्मक माध्यम चुनें और उसमें महारत हासिल करने के लिए प्रतिबद्ध रहें — शिल्प की गहराई बिखरे प्रयासों से कहीं अधिक संतुष्टि लाएगी।",
    },
    4: {
        "title": "Structured Maturity", "title_hi": "व्यवस्थित परिपक्वता",
        "theme": "Building lasting legacy through discipline.", "theme_hi": "अनुशासन से स्थायी विरासत निर्माण।",
        "description": "Your mature years are defined by solid achievement. Decades of disciplined effort crystallize into a legacy — a business, a craft, or a family institution — that outlasts you.",
        "description_hi": "आपके परिपक्व वर्ष ठोस उपलब्धि से परिभाषित होते हैं। दशकों का अनुशासित प्रयास एक विरासत में परिणत होता है — एक व्यवसाय, एक शिल्प, या एक पारिवारिक संस्था — जो आपसे अधिक समय तक टिकती है।",
        "advice": "Document your systems and processes so others can benefit from the structures you have built.",
        "advice_hi": "अपनी प्रणालियों और प्रक्रियाओं को दस्तावेज़ करें ताकि अन्य लोग आपके बनाए ढांचों से लाभ उठा सकें।",
    },
    5: {
        "title": "Freedom Maturity", "title_hi": "स्वतंत्रता परिपक्वता",
        "theme": "Embracing change and travel in later years.", "theme_hi": "बाद के वर्षों में परिवर्तन और यात्रा।",
        "description": "Maturity liberates you from convention. You shed obligations that no longer serve you and discover the world afresh — through travel, reinvention, or entirely new pursuits.",
        "description_hi": "परिपक्वता आपको परंपरा से मुक्त करती है। आप उन दायित्वों को छोड़ देते हैं जो अब आपके काम नहीं आते और दुनिया को नए सिरे से खोजते हैं — यात्रा, पुनर्आविष्कार, या पूरी तरह नई गतिविधियों के माध्यम से।",
        "advice": "Plan at least one major new adventure or life change every five years to keep your spirit energized.",
        "advice_hi": "अपनी ऊर्जा को जीवंत रखने के लिए हर पांच साल में कम से कम एक बड़े नए साहसिक कार्य या जीवन परिवर्तन की योजना बनाएं।",
    },
    6: {
        "title": "Family Maturity", "title_hi": "पारिवारिक परिपक्वता",
        "theme": "Deepening family bonds and community service.", "theme_hi": "पारिवारिक बंधन और सामुदायिक सेवा।",
        "description": "Love and family become the cornerstone of your later life. You evolve into the elder who holds the community together, offering wisdom, care, and a warm refuge for all.",
        "description_hi": "प्यार और परिवार आपके बाद के जीवन की आधारशिला बन जाते हैं। आप उस बुजुर्ग के रूप में विकसित होते हैं जो समुदाय को एकजुट रखता है, ज्ञान, देखभाल और सभी के लिए एक गर्म आश्रय प्रदान करता है।",
        "advice": "Create regular family or community rituals that give people a sense of belonging and shared identity.",
        "advice_hi": "नियमित पारिवारिक या सामुदायिक अनुष्ठान बनाएं जो लोगों को अपनेपन और साझी पहचान की भावना दें।",
    },
    7: {
        "title": "Spiritual Maturity", "title_hi": "आध्यात्मिक परिपक्वता",
        "theme": "Inner wisdom and spiritual seeking intensifies.", "theme_hi": "आंतरिक ज्ञान और आध्यात्मिक खोज तीव्र होती है।",
        "description": "The outer world quiets and the inner world becomes vast. You are drawn toward philosophy, meditation, and the deeper mysteries of existence — emerging as a guide for those seeking truth.",
        "description_hi": "बाहरी दुनिया शांत होती है और आंतरिक दुनिया विशाल हो जाती है। आप दर्शन, ध्यान और अस्तित्व के गहरे रहस्यों की ओर आकर्षित होते हैं — सत्य के खोजियों के लिए एक मार्गदर्शक के रूप में उभरते हैं।",
        "advice": "Establish a daily contemplative practice — even twenty minutes of silence each morning will dramatically deepen your inner clarity.",
        "advice_hi": "एक दैनिक चिंतनशील अभ्यास स्थापित करें — प्रतिदिन सुबह बीस मिनट की चुप्पी भी आपकी आंतरिक स्पष्टता को गहराई से बढ़ाएगी।",
    },
    8: {
        "title": "Material Maturity", "title_hi": "भौतिक परिपक्वता",
        "theme": "Financial mastery and power consolidation.", "theme_hi": "वित्तीय महारत और शक्ति संचय।",
        "description": "Decades of effort culminate in financial strength and authority. You step into positions of genuine influence and learn to wield power ethically for the benefit of many.",
        "description_hi": "दशकों का प्रयास वित्तीय शक्ति और अधिकार में परिणत होता है। आप वास्तविक प्रभाव के पदों पर कदम रखते हैं और अनेक लोगों के लाभ के लिए नैतिक रूप से शक्ति का उपयोग करना सीखते हैं।",
        "advice": "Use a portion of your accumulated wealth to mentor younger people — legacy built through others multiplies your impact beyond what money alone can achieve.",
        "advice_hi": "अपने संचित धन का एक हिस्सा युवाओं को मार्गदर्शन देने में लगाएं — दूसरों के माध्यम से बनाई विरासत आपके प्रभाव को उस सीमा से परे बढ़ाती है जो केवल पैसा हासिल कर सकता है।",
    },
    9: {
        "title": "Humanitarian Maturity", "title_hi": "मानवतावादी परिपक्वता",
        "theme": "Serving humanity and letting go of the personal.", "theme_hi": "मानवता की सेवा और व्यक्तिगत से ऊपर उठना।",
        "description": "Personal ambition gives way to universal purpose. You find profound fulfillment in service, philanthropy, and teaching — your life becomes an open gift to the world.",
        "description_hi": "व्यक्तिगत महत्वाकांक्षा सार्वभौमिक उद्देश्य को रास्ता देती है। आप सेवा, परोपकार और शिक्षण में गहरी संतुष्टि पाते हैं — आपका जीवन दुनिया के लिए एक खुला उपहार बन जाता है।",
        "advice": "Identify the single cause you care most about and commit wholeheartedly — scattered generosity dilutes your extraordinary capacity for impact.",
        "advice_hi": "उस एकल कारण को पहचानें जिसकी आपको सबसे अधिक परवाह है और पूरे दिल से प्रतिबद्ध रहें — बिखरी उदारता आपकी असाधारण प्रभाव क्षमता को कमजोर करती है।",
    },
    11: {
        "title": "Intuitive Maturity", "title_hi": "सहज परिपक्वता",
        "theme": "Becoming a spiritual guide for others.", "theme_hi": "दूसरों के लिए आध्यात्मिक मार्गदर्शक बनना।",
        "description": "Your heightened sensitivity matures into a steady, luminous wisdom. People seek you out for insight, and your intuitive knowing becomes a reliable compass for those around you.",
        "description_hi": "आपकी उच्च संवेदनशीलता एक स्थिर, चमकदार ज्ञान में परिपक्व होती है। लोग अंतर्दृष्टि के लिए आपके पास आते हैं और आपका अंतर्बोध आपके आसपास के लोगों के लिए एक विश्वसनीय दिशासूचक बन जाता है।",
        "advice": "Share your spiritual insights through writing, speaking, or teaching — your wisdom is meant to illuminate many, not just yourself.",
        "advice_hi": "लेखन, बोलने या शिक्षण के माध्यम से अपनी आध्यात्मिक अंतर्दृष्टि साझा करें — आपका ज्ञान केवल आपको नहीं, अनेकों को प्रकाशित करने के लिए है।",
    },
    22: {
        "title": "Visionary Maturity", "title_hi": "दूरदर्शी परिपक्वता",
        "theme": "Manifesting large-scale humanitarian projects.", "theme_hi": "बड़े पैमाने पर मानवतावादी परियोजनाओं को साकार करना।",
        "description": "The Master Builder reaches full power in maturity. Your capacity to organize, inspire, and execute on a grand scale becomes undeniable — institutions and movements bear your mark.",
        "description_hi": "मास्टर निर्माता परिपक्वता में पूर्ण शक्ति प्राप्त करता है। बड़े पैमाने पर व्यवस्थित करने, प्रेरित करने और क्रियान्वित करने की आपकी क्षमता अनिवार्य हो जाती है — संस्थाएं और आंदोलन आपकी छाप धारण करते हैं।",
        "advice": "Delegate ruthlessly and surround yourself with specialists — your role is to hold the vision, not to execute every detail personally.",
        "advice_hi": "निर्मम रूप से काम सौंपें और विशेषज्ञों से घिरे रहें — आपकी भूमिका दृष्टि धारण करना है, न कि व्यक्तिगत रूप से हर विवरण क्रियान्वित करना।",
    },
    33: {
        "title": "Selfless Maturity", "title_hi": "निस्वार्थ परिपक्वता",
        "theme": "Becoming a master healer and teacher.", "theme_hi": "मास्टर उपचारक और शिक्षक बनना।",
        "description": "You evolve into the rarest of archetypes: the healer-teacher whose very presence uplifts. Selfless service no longer feels like sacrifice — it becomes the natural expression of who you are.",
        "description_hi": "आप सबसे दुर्लभ आद्यरूप में विकसित होते हैं: वह उपचारक-शिक्षक जिनकी उपस्थिति मात्र से उत्थान होता है। निस्वार्थ सेवा अब त्याग की तरह नहीं लगती — यह आपके स्वभाव की स्वाभाविक अभिव्यक्ति बन जाती है।",
        "advice": "Protect your energy by choosing depth over breadth — serve fewer people more profoundly rather than spreading yourself thin.",
        "advice_hi": "गहराई को व्यापकता पर चुनकर अपनी ऊर्जा की रक्षा करें — खुद को बिखेरने की बजाय कम लोगों की अधिक गहराई से सेवा करें।",
    },
}


def calculate_numerology(name: str, birth_date: str) -> dict:
    """
    Full numerology calculation.

    Args:
        name: Full name string
        birth_date: Date string in YYYY-MM-DD format

    Returns:
        dict with life_path, destiny, soul_urge, personality, predictions
    """
    life_path = _life_path(birth_date)
    destiny = _name_to_number(name)
    soul_urge = _vowels_number(name)
    personality = _consonants_number(name)

    predictions = {
        "life_path": LIFE_PATH_PREDICTIONS.get(life_path, LIFE_PATH_PREDICTIONS[9]),
        "destiny": DESTINY_PREDICTIONS.get(destiny, DESTINY_PREDICTIONS[9]),
        "soul_urge": SOUL_URGE_PREDICTIONS.get(soul_urge, SOUL_URGE_PREDICTIONS[9]),
        "personality": PERSONALITY_PREDICTIONS.get(personality, PERSONALITY_PREDICTIONS[9]),
    }

    # DOB digits for Lo Shu analysis (non-zero digits only)
    dob_digits = [int(c) for c in birth_date.replace("-", "") if c.isdigit() and c != "0"]
    loshu_data = _compute_loshu_grid(dob_digits)

    birthday_raw = int(birth_date[8:10])          # raw calendar day (1-31)
    birthday_reduced = _birthday_number(birth_date)  # reduced to single/master
    maturity = _maturity_number(life_path, destiny)

    from datetime import date as _today_date
    current_year = _today_date.today().year
    personal_year = _personal_year_number(birth_date, current_year)
    next_year_personal = _personal_year_number(birth_date, current_year + 1)

    def _py_pred(n: int) -> dict:
        # Master numbers 11→2, 22→4, 33→6 for prediction lookup
        base = {11: 2, 22: 4, 33: 6}.get(n, n)
        return _PERSONAL_YEAR_PREDICTIONS.get(base, _PERSONAL_YEAR_PREDICTIONS[9])

    result = {
        "life_path": life_path,
        "destiny": destiny,
        "soul_urge": soul_urge,
        "personality": personality,
        "birthday_number": birthday_raw,
        "birthday_reduced": birthday_reduced,
        "birthday_prediction": BIRTHDAY_PREDICTIONS.get(birthday_raw, BIRTHDAY_PREDICTIONS.get(birthday_reduced, {})),
        "maturity_number": maturity,
        "maturity_prediction": MATURITY_PREDICTIONS.get(maturity, {}),
        "predictions": predictions,
        "pinnacles": _calculate_pinnacles(birth_date),
        "challenges": _calculate_challenges(birth_date),
        "life_cycles": _calculate_life_cycles(birth_date),
        "karmic_debts": _detect_karmic_debt(birth_date, name),
        "hidden_passion": _hidden_passion(name),
        "subconscious_self": _subconscious_self(name),
        "karmic_lessons": _karmic_lessons(name),
        "name_letter_breakdown": _name_letter_breakdown(name),
        # Lo Shu grid data (layout + filled values) for UI rendering
        "loshu_grid": loshu_data["grid"],
        "loshu_values": loshu_data["values"],
        "loshu_arrows": analyze_loshu_arrows(dob_digits),
        "loshu_planes": analyze_loshu_planes(dob_digits),
        "missing_numbers": analyze_missing_numbers(dob_digits),
        "missing_numbers_source": "birth_date",
        "repeated_numbers": analyze_repeated_numbers(dob_digits),
        # Personal Year Number — changes each Jan 1
        "personal_year": personal_year,
        "personal_year_prediction": _py_pred(personal_year),
        "next_personal_year": next_year_personal,
        "next_personal_year_prediction": _py_pred(next_year_personal),
    }
    return _normalize_focus_areas(result)
