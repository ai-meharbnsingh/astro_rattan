"""
numerology_forecast_engine.py — Personal Year/Month/Day Numerology Forecasts
=============================================================================
Calculates Personal Year, Personal Month, Personal Day, and Universal
Year/Month/Day numbers with bilingual (en + hi) predictions.

Uses _reduce_to_single from numerology_engine (preserves master numbers 11, 22, 33).
"""
from datetime import date, datetime
from typing import Optional

from app.numerology_engine import _reduce_to_single


# ─── Helper: sum all digits of a number ───────────────────────────────────────

def _digit_sum(n: int) -> int:
    """Sum individual digits of a positive integer."""
    return sum(int(d) for d in str(abs(n)))


# ─── Personal Year / Month / Day ──────────────────────────────────────────────

def calculate_personal_year(birth_month: int, birth_day: int, year: int) -> int:
    """
    Personal Year = reduce(birth_month_digit_sum + birth_day_digit_sum + year_digit_sum).

    Each component is reduced to its digit sum first, then the total is reduced
    to a single digit or master number.
    """
    month_sum = _digit_sum(birth_month)
    day_sum = _digit_sum(birth_day)
    year_sum = _digit_sum(year)
    total = month_sum + day_sum + year_sum
    return _reduce_to_single(total)


def calculate_personal_month(personal_year: int, month: int) -> int:
    """Personal Month = reduce(personal_year + calendar_month_digit_sum)."""
    return _reduce_to_single(personal_year + _digit_sum(month))


def calculate_personal_day(personal_month: int, day: int) -> int:
    """Personal Day = reduce(personal_month + calendar_day_digit_sum)."""
    return _reduce_to_single(personal_month + _digit_sum(day))


# ─── Universal Year / Month / Day ─────────────────────────────────────────────

def calculate_universal_year(year: int) -> int:
    """Universal Year = reduce(sum of year digits)."""
    return _reduce_to_single(_digit_sum(year))


def calculate_universal_month(universal_year: int, month: int) -> int:
    """Universal Month = reduce(universal_year + calendar_month_digit_sum)."""
    return _reduce_to_single(universal_year + _digit_sum(month))


def calculate_universal_day(universal_year: int, month: int, day: int) -> int:
    """Universal Day = reduce(universal_month + calendar_day_digit_sum)."""
    um = calculate_universal_month(universal_year, month)
    return _reduce_to_single(um + _digit_sum(day))


# ─── Prediction Data (bilingual en + hi) ──────────────────────────────────────

PERSONAL_YEAR_PREDICTIONS = {
    1: {
        "theme": "New Beginnings",
        "theme_hi": "नई शुरुआत",
        "description": "A year of fresh starts, independence, and planting seeds for the future. "
                       "Take initiative and embrace your individuality. This is the time to launch "
                       "new projects and step into leadership.",
        "description_hi": "नई शुरुआत, स्वतंत्रता और भविष्य के लिए बीज बोने का वर्ष। "
                          "पहल करें और अपनी व्यक्तिगतता को अपनाएं। यह नई परियोजनाएं शुरू करने "
                          "और नेतृत्व में कदम रखने का समय है।",
        "focus_areas": "Career launches, self-improvement, personal branding, bold decisions",
        "focus_areas_hi": "करियर की शुरुआत, आत्म-सुधार, व्यक्तिगत ब्रांडिंग, साहसिक निर्णय",
        "advice": "Trust your instincts and act decisively. Do not wait for others to lead.",
        "advice_hi": "अपनी प्रवृत्ति पर भरोसा करें और निर्णायक रूप से कार्य करें। दूसरों के नेतृत्व की प्रतीक्षा न करें।",
        "lucky_months": [1, 5, 10],
    },
    2: {
        "theme": "Patience & Partnerships",
        "theme_hi": "धैर्य और साझेदारी",
        "description": "A year of cooperation, diplomacy, and building relationships. "
                       "Progress comes through patience and working with others. "
                       "Avoid forcing outcomes — let things unfold naturally.",
        "description_hi": "सहयोग, कूटनीति और रिश्ते बनाने का वर्ष। "
                          "धैर्य और दूसरों के साथ काम करने से प्रगति होती है। "
                          "परिणामों को जबरदस्ती न लाएं — चीजों को स्वाभाविक रूप से होने दें।",
        "focus_areas": "Relationships, teamwork, mediation, emotional intelligence, patience",
        "focus_areas_hi": "रिश्ते, टीमवर्क, मध्यस्थता, भावनात्मक बुद्धिमत्ता, धैर्य",
        "advice": "Listen more than you speak. Partnerships formed now will bear fruit later.",
        "advice_hi": "बोलने से ज्यादा सुनें। अभी बनी साझेदारी बाद में फल देगी।",
        "lucky_months": [2, 6, 9],
    },
    3: {
        "theme": "Creativity & Self-Expression",
        "theme_hi": "रचनात्मकता और आत्म-अभिव्यक्ति",
        "description": "A vibrant year for creative projects, socializing, and expressing yourself. "
                       "Joy, optimism, and artistic endeavors flourish. "
                       "Communication skills are heightened — write, speak, perform.",
        "description_hi": "रचनात्मक परियोजनाओं, सामाजिकता और आत्म-अभिव्यक्ति के लिए जीवंत वर्ष। "
                          "खुशी, आशावाद और कलात्मक प्रयास फलते-फूलते हैं। "
                          "संचार कौशल बढ़ा हुआ है — लिखें, बोलें, प्रदर्शन करें।",
        "focus_areas": "Art, writing, public speaking, social gatherings, joy, entertainment",
        "focus_areas_hi": "कला, लेखन, सार्वजनिक भाषण, सामाजिक समारोह, आनंद, मनोरंजन",
        "advice": "Express your authentic self without fear. Scatter seeds of inspiration.",
        "advice_hi": "बिना डर के अपना प्रामाणिक स्वरूप व्यक्त करें। प्रेरणा के बीज बिखेरें।",
        "lucky_months": [3, 5, 12],
    },
    4: {
        "theme": "Hard Work & Foundation",
        "theme_hi": "कठिन परिश्रम और नींव निर्माण",
        "description": "A year of discipline, structure, and building solid foundations. "
                       "Results come from sustained effort, not shortcuts. "
                       "Focus on health, finances, and long-term stability.",
        "description_hi": "अनुशासन, संरचना और ठोस नींव बनाने का वर्ष। "
                          "परिणाम निरंतर प्रयास से आते हैं, शॉर्टकट से नहीं। "
                          "स्वास्थ्य, वित्त और दीर्घकालिक स्थिरता पर ध्यान दें।",
        "focus_areas": "Work ethic, finances, health routines, home improvement, planning",
        "focus_areas_hi": "कार्य नैतिकता, वित्त, स्वास्थ्य दिनचर्या, गृह सुधार, योजना",
        "advice": "Be patient with slow progress. The foundations you build now last decades.",
        "advice_hi": "धीमी प्रगति में धैर्य रखें। अभी जो नींव बनाते हैं वह दशकों तक टिकेगी।",
        "lucky_months": [4, 8, 10],
    },
    5: {
        "theme": "Change & Freedom",
        "theme_hi": "परिवर्तन और स्वतंत्रता",
        "description": "A dynamic year of change, travel, and adventure. "
                       "Expect the unexpected — embrace flexibility and new experiences. "
                       "Freedom and variety are essential to your growth.",
        "description_hi": "परिवर्तन, यात्रा और साहस का गतिशील वर्ष। "
                          "अप्रत्याशित की उम्मीद करें — लचीलेपन और नए अनुभवों को अपनाएं। "
                          "स्वतंत्रता और विविधता आपके विकास के लिए आवश्यक है।",
        "focus_areas": "Travel, relocation, new relationships, risk-taking, breaking routines",
        "focus_areas_hi": "यात्रा, स्थानांतरण, नए रिश्ते, जोखिम लेना, दिनचर्या तोड़ना",
        "advice": "Say yes to opportunities. Avoid clinging to what no longer serves you.",
        "advice_hi": "अवसरों को हां कहें। जो अब आपके काम का नहीं है उससे चिपके न रहें।",
        "lucky_months": [5, 7, 11],
    },
    6: {
        "theme": "Home, Family & Responsibility",
        "theme_hi": "घर, परिवार और जिम्मेदारी",
        "description": "A nurturing year centered on family, home, and community. "
                       "Responsibilities increase but so does love and fulfillment. "
                       "Marriage, children, and domestic matters take center stage.",
        "description_hi": "परिवार, घर और समुदाय पर केंद्रित पोषक वर्ष। "
                          "जिम्मेदारियां बढ़ती हैं लेकिन प्यार और संतुष्टि भी। "
                          "विवाह, बच्चे और घरेलू मामले मुख्य होते हैं।",
        "focus_areas": "Family bonds, home renovation, marriage, caregiving, community service",
        "focus_areas_hi": "पारिवारिक बंधन, घर का नवीनीकरण, विवाह, देखभाल, सामुदायिक सेवा",
        "advice": "Give generously but set healthy boundaries. Self-care is not selfish.",
        "advice_hi": "उदारता से दें लेकिन स्वस्थ सीमाएं निर्धारित करें। आत्म-देखभाल स्वार्थ नहीं है।",
        "lucky_months": [2, 6, 9],
    },
    7: {
        "theme": "Reflection & Spirituality",
        "theme_hi": "आत्मचिंतन और आध्यात्मिकता",
        "description": "A deeply introspective year for spiritual growth and inner wisdom. "
                       "Solitude, study, and meditation bring clarity. "
                       "Avoid rushing decisions — trust the process of inner knowing.",
        "description_hi": "आध्यात्मिक विकास और आंतरिक ज्ञान के लिए गहन आत्मनिरीक्षण वर्ष। "
                          "एकांत, अध्ययन और ध्यान स्पष्टता लाता है। "
                          "निर्णय जल्दी न लें — आंतरिक ज्ञान की प्रक्रिया पर भरोसा करें।",
        "focus_areas": "Meditation, research, spiritual practice, solitude, learning, health",
        "focus_areas_hi": "ध्यान, शोध, आध्यात्मिक अभ्यास, एकांत, सीखना, स्वास्थ्य",
        "advice": "Withdraw from noise and listen to your inner voice. Quality over quantity.",
        "advice_hi": "शोर से दूर हटें और अपनी आंतरिक आवाज सुनें। मात्रा से अधिक गुणवत्ता।",
        "lucky_months": [3, 7, 12],
    },
    8: {
        "theme": "Power, Money & Achievement",
        "theme_hi": "शक्ति, धन और उपलब्धि",
        "description": "A powerful year for material success, business, and authority. "
                       "Financial opportunities abound but karma demands integrity. "
                       "Step into your power and claim what you have earned.",
        "description_hi": "भौतिक सफलता, व्यापार और अधिकार के लिए शक्तिशाली वर्ष। "
                          "वित्तीय अवसर प्रचुर हैं लेकिन कर्म ईमानदारी की मांग करता है। "
                          "अपनी शक्ति में कदम रखें और जो अर्जित किया है उस पर दावा करें।",
        "focus_areas": "Business growth, investments, promotions, leadership, financial planning",
        "focus_areas_hi": "व्यापार वृद्धि, निवेश, पदोन्नति, नेतृत्व, वित्तीय योजना",
        "advice": "Use power wisely. What you give returns multiplied. Avoid greed.",
        "advice_hi": "शक्ति का बुद्धिमानी से उपयोग करें। जो देते हैं वह गुणित होकर लौटता है। लालच से बचें।",
        "lucky_months": [1, 8, 10],
    },
    9: {
        "theme": "Completion & Humanitarianism",
        "theme_hi": "समापन और मानवता सेवा",
        "description": "A year of endings, release, and humanitarian service. "
                       "Let go of what no longer serves your highest good. "
                       "Generosity and compassion bring deep fulfillment.",
        "description_hi": "समापन, मुक्ति और मानवतावादी सेवा का वर्ष। "
                          "जो अब आपके सर्वोच्च हित में नहीं है उसे जाने दें। "
                          "उदारता और करुणा गहरी संतुष्टि लाती है।",
        "focus_areas": "Charity, forgiveness, decluttering, closure, spiritual service, travel",
        "focus_areas_hi": "दान, क्षमा, अव्यवस्था दूर करना, समापन, आध्यात्मिक सेवा, यात्रा",
        "advice": "Release attachments gracefully. Clear space for the new cycle ahead.",
        "advice_hi": "आसक्तियों को शालीनता से छोड़ें। आगे के नए चक्र के लिए जगह बनाएं।",
        "lucky_months": [3, 9, 12],
    },
    11: {
        "theme": "Master Intuition & Illumination",
        "theme_hi": "मास्टर अंतर्ज्ञान और प्रकाश",
        "description": "A master number year of heightened intuition, spiritual awakening, and "
                       "visionary insight. You may feel called to inspire others. "
                       "Channel nervous energy into creative and spiritual pursuits.",
        "description_hi": "उच्च अंतर्ज्ञान, आध्यात्मिक जागृति और दूरदर्शी अंतर्दृष्टि का मास्टर नंबर वर्ष। "
                          "आप दूसरों को प्रेरित करने के लिए बुलाए जा सकते हैं। "
                          "घबराहट की ऊर्जा को रचनात्मक और आध्यात्मिक कार्यों में लगाएं।",
        "focus_areas": "Spiritual teaching, creative inspiration, healing work, partnerships",
        "focus_areas_hi": "आध्यात्मिक शिक्षण, रचनात्मक प्रेरणा, उपचार कार्य, साझेदारी",
        "advice": "Trust your inner visions. You are being guided toward a higher purpose.",
        "advice_hi": "अपने आंतरिक दृष्टिकोण पर भरोसा करें। आपको एक उच्च उद्देश्य की ओर मार्गदर्शित किया जा रहा है।",
        "lucky_months": [2, 7, 11],
    },
    22: {
        "theme": "Master Builder",
        "theme_hi": "मास्टर बिल्डर",
        "description": "A rare master number year for turning grand visions into concrete reality. "
                       "Large-scale projects, practical idealism, and lasting impact. "
                       "You can achieve extraordinary things with disciplined effort.",
        "description_hi": "भव्य दृष्टिकोण को ठोस वास्तविकता में बदलने का दुर्लभ मास्टर नंबर वर्ष। "
                          "बड़े पैमाने की परियोजनाएं, व्यावहारिक आदर्शवाद और स्थायी प्रभाव। "
                          "अनुशासित प्रयास से आप असाधारण चीजें हासिल कर सकते हैं।",
        "focus_areas": "Large projects, infrastructure, legacy building, leadership, global impact",
        "focus_areas_hi": "बड़ी परियोजनाएं, बुनियादी ढांचा, विरासत निर्माण, नेतृत्व, वैश्विक प्रभाव",
        "advice": "Think big but plan meticulously. Your work can outlast your lifetime.",
        "advice_hi": "बड़ा सोचें लेकिन सावधानी से योजना बनाएं। आपका कार्य आपके जीवनकाल से आगे रह सकता है।",
        "lucky_months": [4, 8, 11],
    },
    33: {
        "theme": "Master Teacher & Healer",
        "theme_hi": "मास्टर शिक्षक और उपचारक",
        "description": "The highest master number year — selfless service, healing, and uplifting humanity. "
                       "You are called to teach, nurture, and love unconditionally. "
                       "Personal sacrifice leads to profound spiritual rewards.",
        "description_hi": "सर्वोच्च मास्टर नंबर वर्ष — निःस्वार्थ सेवा, उपचार और मानवता का उत्थान। "
                          "आपको बिना शर्त सिखाने, पोषण करने और प्यार करने के लिए बुलाया गया है। "
                          "व्यक्तिगत त्याग गहन आध्यात्मिक पुरस्कार की ओर ले जाता है।",
        "focus_areas": "Teaching, healing, community upliftment, compassion, artistic service",
        "focus_areas_hi": "शिक्षण, उपचार, सामुदायिक उत्थान, करुणा, कलात्मक सेवा",
        "advice": "Serve without expectation. Your greatest power is unconditional love.",
        "advice_hi": "बिना अपेक्षा के सेवा करें। आपकी सबसे बड़ी शक्ति बिना शर्त प्रेम है।",
        "lucky_months": [3, 6, 9],
    },
}


PERSONAL_MONTH_PREDICTIONS = {
    1: {
        "theme": "Initiative",
        "theme_hi": "पहल",
        "description": "A month to start new projects and take bold action. Lead with confidence.",
        "description_hi": "नई परियोजनाएं शुरू करने और साहसिक कदम उठाने का महीना। आत्मविश्वास से नेतृत्व करें।",
    },
    2: {
        "theme": "Cooperation",
        "theme_hi": "सहयोग",
        "description": "Focus on relationships and teamwork. Patience and diplomacy yield results.",
        "description_hi": "रिश्तों और टीमवर्क पर ध्यान दें। धैर्य और कूटनीति से परिणाम मिलते हैं।",
    },
    3: {
        "theme": "Expression",
        "theme_hi": "अभिव्यक्ति",
        "description": "Creative energy peaks. Socialize, write, and share your ideas freely.",
        "description_hi": "रचनात्मक ऊर्जा चरम पर है। मेलजोल बढ़ाएं, लिखें और अपने विचार साझा करें।",
    },
    4: {
        "theme": "Discipline",
        "theme_hi": "अनुशासन",
        "description": "Time for hard work and organization. Build structure and stick to plans.",
        "description_hi": "कठिन परिश्रम और व्यवस्था का समय। संरचना बनाएं और योजनाओं पर टिके रहें।",
    },
    5: {
        "theme": "Freedom",
        "theme_hi": "स्वतंत्रता",
        "description": "Expect changes and surprises. Embrace flexibility and try something new.",
        "description_hi": "बदलाव और आश्चर्य की उम्मीद करें। लचीलापन अपनाएं और कुछ नया आजमाएं।",
    },
    6: {
        "theme": "Nurturing",
        "theme_hi": "पोषण",
        "description": "Family and home take priority. Give love and accept responsibility.",
        "description_hi": "परिवार और घर प्राथमिकता लेते हैं। प्यार दें और जिम्मेदारी स्वीकार करें।",
    },
    7: {
        "theme": "Reflection",
        "theme_hi": "चिंतन",
        "description": "Go inward. Study, meditate, and seek deeper understanding. Avoid rush.",
        "description_hi": "अंतर्मुखी हों। अध्ययन करें, ध्यान करें और गहरी समझ की खोज करें। जल्दबाजी से बचें।",
    },
    8: {
        "theme": "Achievement",
        "theme_hi": "उपलब्धि",
        "description": "Financial and career opportunities arise. Act with authority and integrity.",
        "description_hi": "वित्तीय और करियर के अवसर आते हैं। अधिकार और ईमानदारी से कार्य करें।",
    },
    9: {
        "theme": "Release",
        "theme_hi": "मुक्ति",
        "description": "Complete unfinished business. Let go of what weighs you down. Give generously.",
        "description_hi": "अधूरे काम पूरे करें। जो बोझ है उसे छोड़ दें। उदारता से दें।",
    },
    11: {
        "theme": "Spiritual Insight",
        "theme_hi": "आध्यात्मिक अंतर्दृष्टि",
        "description": "Heightened intuition and spiritual downloads. Trust your inner guidance.",
        "description_hi": "बढ़ा हुआ अंतर्ज्ञान और आध्यात्मिक मार्गदर्शन। अपनी आंतरिक मार्गदर्शिका पर भरोसा करें।",
    },
    22: {
        "theme": "Grand Plans",
        "theme_hi": "भव्य योजनाएं",
        "description": "Manifest large-scale visions. Practical steps toward ambitious goals.",
        "description_hi": "बड़े पैमाने के दृष्टिकोण को साकार करें। महत्वाकांक्षी लक्ष्यों की ओर व्यावहारिक कदम।",
    },
    33: {
        "theme": "Selfless Service",
        "theme_hi": "निःस्वार्थ सेवा",
        "description": "Devote energy to healing and uplifting others. Compassion is your superpower.",
        "description_hi": "दूसरों को ठीक करने और उत्थान के लिए ऊर्जा समर्पित करें। करुणा आपकी महाशक्ति है।",
    },
}


PERSONAL_DAY_PREDICTIONS = {
    1: {
        "theme": "Action",
        "theme_hi": "कार्रवाई",
        "description": "Take the lead today. Start something new. Be assertive and original.",
        "description_hi": "आज नेतृत्व करें। कुछ नया शुरू करें। दृढ़ और मौलिक बनें।",
    },
    2: {
        "theme": "Harmony",
        "theme_hi": "सामंजस्य",
        "description": "Cooperate and listen. A good day for meetings, partnerships, and patience.",
        "description_hi": "सहयोग करें और सुनें। बैठकों, साझेदारी और धैर्य के लिए अच्छा दिन।",
    },
    3: {
        "theme": "Joy",
        "theme_hi": "आनंद",
        "description": "Express yourself creatively. Socialize, laugh, and share your gifts.",
        "description_hi": "रचनात्मक रूप से अपनी अभिव्यक्ति करें। मेलजोल करें, हंसें और अपनी प्रतिभा साझा करें।",
    },
    4: {
        "theme": "Effort",
        "theme_hi": "प्रयास",
        "description": "Focus on work and details. Organize, plan, and execute methodically.",
        "description_hi": "काम और विवरणों पर ध्यान दें। व्यवस्थित रूप से योजना बनाएं और निष्पादित करें।",
    },
    5: {
        "theme": "Adventure",
        "theme_hi": "साहस",
        "description": "Break routine. Travel, explore, or try something completely different.",
        "description_hi": "दिनचर्या तोड़ें। यात्रा करें, खोजें, या कुछ बिल्कुल अलग आजमाएं।",
    },
    6: {
        "theme": "Care",
        "theme_hi": "देखभाल",
        "description": "Attend to family and loved ones. Beautify your surroundings. Be generous.",
        "description_hi": "परिवार और प्रियजनों की देखभाल करें। अपने परिवेश को सुंदर बनाएं। उदार बनें।",
    },
    7: {
        "theme": "Contemplation",
        "theme_hi": "विचार",
        "description": "Spend time alone. Read, meditate, and reflect. Avoid major decisions.",
        "description_hi": "अकेले समय बिताएं। पढ़ें, ध्यान करें और विचार करें। बड़े फैसलों से बचें।",
    },
    8: {
        "theme": "Power",
        "theme_hi": "शक्ति",
        "description": "Make financial moves. Negotiate, invest, or ask for what you deserve.",
        "description_hi": "वित्तीय कदम उठाएं। बातचीत करें, निवेश करें, या जो आप योग्य हैं वह मांगें।",
    },
    9: {
        "theme": "Closure",
        "theme_hi": "समापन",
        "description": "Finish what you started. Forgive, release, and prepare for renewal.",
        "description_hi": "जो शुरू किया उसे पूरा करें। क्षमा करें, छोड़ दें और नवीनीकरण की तैयारी करें।",
    },
    11: {
        "theme": "Inspiration",
        "theme_hi": "प्रेरणा",
        "description": "A day of flashes of insight. Trust your gut. Spiritual connections deepen.",
        "description_hi": "अंतर्दृष्टि की चमक का दिन। अपनी अंतरात्मा पर भरोसा करें। आध्यात्मिक संबंध गहरे होते हैं।",
    },
    22: {
        "theme": "Manifestation",
        "theme_hi": "अभिव्यक्ति",
        "description": "Turn big ideas into action. A day for practical execution of grand plans.",
        "description_hi": "बड़े विचारों को कार्य में बदलें। भव्य योजनाओं के व्यावहारिक निष्पादन का दिन।",
    },
    33: {
        "theme": "Compassion",
        "theme_hi": "करुणा",
        "description": "Heal and serve others unconditionally. Your presence is a blessing today.",
        "description_hi": "बिना शर्त दूसरों की सेवा और उपचार करें। आज आपकी उपस्थिति एक आशीर्वाद है।",
    },
}


# ─── Main Forecast Function ──────────────────────────────────────────────────

def calculate_forecast(birth_date: str, target_date: Optional[str] = None) -> dict:
    """
    Calculate personal and universal numerology forecast.

    Args:
        birth_date: Date of birth as YYYY-MM-DD string.
        target_date: Target date as YYYY-MM-DD string (defaults to today).

    Returns:
        Dictionary with personal_year, personal_month, personal_day,
        universal_year, universal_month, universal_day, and predictions.
    """
    # Parse birth date
    try:
        bd = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError(f"Invalid birth_date format: {birth_date}. Expected YYYY-MM-DD.")

    # Parse target date (default today)
    if target_date:
        try:
            td = datetime.strptime(target_date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            raise ValueError(f"Invalid target_date format: {target_date}. Expected YYYY-MM-DD.")
    else:
        td = date.today()

    # Calculate personal numbers
    py = calculate_personal_year(bd.month, bd.day, td.year)
    pm = calculate_personal_month(py, td.month)
    pd_ = calculate_personal_day(pm, td.day)

    # Calculate universal numbers
    uy = calculate_universal_year(td.year)
    um = calculate_universal_month(uy, td.month)
    ud = calculate_universal_day(uy, td.month, td.day)

    # Look up predictions (fall back to reduced single digit if master not found)
    py_pred = PERSONAL_YEAR_PREDICTIONS.get(py, PERSONAL_YEAR_PREDICTIONS.get(_reduce_to_single(py), {}))
    pm_pred = PERSONAL_MONTH_PREDICTIONS.get(pm, PERSONAL_MONTH_PREDICTIONS.get(_reduce_to_single(pm), {}))
    pd_pred = PERSONAL_DAY_PREDICTIONS.get(pd_, PERSONAL_DAY_PREDICTIONS.get(_reduce_to_single(pd_), {}))

    return {
        "personal_year": py,
        "personal_month": pm,
        "personal_day": pd_,
        "universal_year": uy,
        "universal_month": um,
        "universal_day": ud,
        "birth_date": birth_date,
        "target_date": td.isoformat(),
        "predictions": {
            "personal_year": py_pred,
            "personal_month": pm_pred,
            "personal_day": pd_pred,
        },
    }
