"""
numerology_insight_engine.py — Master Insight Layer
====================================================
Consumes output from calculate_numerology() and produces a structured
"insights" block: core personality profile, top problems detected, top
actionable advice, success path, Lo Shu diagnosis, and timeline context.

No AI — pure deterministic rules derived from Pythagorean numerology tradition.
"""

from __future__ import annotations
from datetime import date as _date
from typing import Any

# ---------------------------------------------------------------------------
# NUMBER CORE TRAITS (positive face of each number)
# ---------------------------------------------------------------------------
_TRAITS: dict[int, dict] = {
    1:  {"en": "Natural leader", "hi": "स्वाभाविक नेता"},
    2:  {"en": "Sensitive diplomat", "hi": "संवेदनशील कूटनीतिज्ञ"},
    3:  {"en": "Creative communicator", "hi": "रचनात्मक संचारक"},
    4:  {"en": "Disciplined builder", "hi": "अनुशासित निर्माता"},
    5:  {"en": "Adaptable freedom-seeker", "hi": "अनुकूलनशील स्वतंत्रता-खोजी"},
    6:  {"en": "Caring nurturer", "hi": "देखभाल करने वाला पालनकर्ता"},
    7:  {"en": "Deep analytical thinker", "hi": "गहरा विश्लेषणात्मक विचारक"},
    8:  {"en": "Ambitious achiever", "hi": "महत्वाकांक्षी उपलब्धिकर्ता"},
    9:  {"en": "Compassionate humanitarian", "hi": "करुणामय मानवतावादी"},
    11: {"en": "Visionary intuitive", "hi": "दूरदर्शी अंतर्ज्ञानी"},
    22: {"en": "Master builder", "hi": "महा निर्माता"},
    33: {"en": "Master teacher", "hi": "महा शिक्षक"},
}

# ---------------------------------------------------------------------------
# NUMBER SHADOW (the dark / challenge side — where problems come from)
# ---------------------------------------------------------------------------
_SHADOW: dict[int, dict] = {
    1:  {
        "problem": "Stubborn and difficulty accepting others' ideas",
        "problem_hi": "जिद्दी स्वभाव और दूसरों के विचार स्वीकार न करना",
        "action": "Consciously ask for input before deciding — leadership also means listening",
        "action_hi": "निर्णय से पहले जानबूझकर दूसरों की राय लें — नेतृत्व का अर्थ सुनना भी है",
    },
    2:  {
        "problem": "Over-sensitivity and difficulty making decisions alone",
        "problem_hi": "अत्यधिक संवेदनशीलता और अकेले निर्णय लेने में कठिनाई",
        "action": "Set a 24-hour decision window — avoid seeking approval from too many people",
        "action_hi": "24 घंटे की निर्णय सीमा तय करें — बहुत अधिक लोगों से मंजूरी मांगने से बचें",
    },
    3:  {
        "problem": "Scattered energy — starting many things without finishing",
        "problem_hi": "बिखरी ऊर्जा — बहुत काम शुरू करना लेकिन पूरा न करना",
        "action": "Limit active projects to 2 at a time, finish before starting new ones",
        "action_hi": "एक समय में केवल 2 काम रखें, नया शुरू करने से पहले पुराना पूरा करें",
    },
    4:  {
        "problem": "Rigidity and resistance to change — can miss opportunities",
        "problem_hi": "कठोरता और बदलाव का विरोध — अवसर चूक सकते हैं",
        "action": "Try one new approach each month — flexibility is a strength, not a threat",
        "action_hi": "हर महीने एक नया तरीका अपनाएं — लचीलापन शक्ति है, खतरा नहीं",
    },
    5:  {
        "problem": "Restlessness and inability to stay committed long-term",
        "problem_hi": "बेचैनी और दीर्घकालिक प्रतिबद्धता में कठिनाई",
        "action": "Commit to one goal for 90 days minimum before evaluating — depth creates freedom",
        "action_hi": "मूल्यांकन से पहले एक लक्ष्य पर कम से कम 90 दिन टिकें — गहराई ही असली स्वतंत्रता है",
    },
    6:  {
        "problem": "Over-giving and difficulty saying no — leads to resentment",
        "problem_hi": "अत्यधिक देना और 'न' कहने में कठिनाई — मन में कड़वाहट आ सकती है",
        "action": "Schedule personal time as a non-negotiable appointment every week",
        "action_hi": "हर सप्ताह अपना समय एक अटल नियुक्ति की तरह तय करें",
    },
    7:  {
        "problem": "Isolation and emotional detachment from people",
        "problem_hi": "एकांत में खो जाना और लोगों से भावनात्मक दूरी",
        "action": "Force one meaningful social connection per week — wisdom shared grows stronger",
        "action_hi": "हर सप्ताह एक अर्थपूर्ण सामाजिक संपर्क जरूर बनाएं — साझा ज्ञान बढ़ता है",
    },
    8:  {
        "problem": "Workaholism and difficulty separating identity from achievement",
        "problem_hi": "काम की लत और पहचान को उपलब्धि से अलग न कर पाना",
        "action": "Block 2 evenings per week with zero work — you are more than your results",
        "action_hi": "प्रति सप्ताह 2 शामें बिना काम के रखें — आप अपनी उपलब्धियों से ज़्यादा हैं",
    },
    9:  {
        "problem": "Emotional overload and difficulty letting go of the past",
        "problem_hi": "भावनात्मक अधिभार और अतीत को जाने देने में कठिनाई",
        "action": "Practice a weekly release ritual — journal what you are letting go each Sunday",
        "action_hi": "साप्ताहिक मुक्ति अभ्यास करें — हर रविवार जो छोड़ रहे हैं वो लिखें",
    },
    11: {
        "problem": "Nervous tension and hypersensitivity to environment and criticism",
        "problem_hi": "तंत्रिका तनाव और वातावरण व आलोचना के प्रति अत्यधिक संवेदनशीलता",
        "action": "10 minutes grounding meditation every morning before checking phone or messages",
        "action_hi": "हर सुबह फोन या संदेश देखने से पहले 10 मिनट की ग्राउंडिंग ध्यान करें",
    },
    22: {
        "problem": "Overwhelm from perfectionism — paralysis when vision feels too large",
        "problem_hi": "पूर्णतावाद से अभिभूत होना — दृष्टि बड़ी लगने पर रुक जाना",
        "action": "Break every big goal into weekly deliverables — execution beats perfect planning",
        "action_hi": "हर बड़े लक्ष्य को साप्ताहिक कार्यों में तोड़ें — क्रियान्वयन परफेक्ट प्लान से बड़ा है",
    },
    33: {
        "problem": "Self-sacrifice to the point of emotional depletion",
        "problem_hi": "इतना त्याग कि खुद भावनात्मक रूप से खाली हो जाएं",
        "action": "You cannot pour from an empty cup — schedule self-care as seriously as service",
        "action_hi": "खाली बर्तन से पानी नहीं मिलता — अपनी देखभाल को सेवा जितनी गंभीरता से लें",
    },
}

# ---------------------------------------------------------------------------
# KARMIC DEBT EXTRA PROBLEMS (stacked on top if debt present)
# ---------------------------------------------------------------------------
_KARMIC_EXTRA: dict[int, dict] = {
    13: {
        "problem": "Tendency to skip foundational work and look for shortcuts",
        "problem_hi": "बुनियादी काम छोड़ना और शॉर्टकट ढूंढने की प्रवृत्ति",
        "action": "Commit to mastering basics first — every shortcut taken now costs double later",
        "action_hi": "पहले मूल बातें सीखें — अभी लिया हर शॉर्टकट बाद में दोगुना पड़ता है",
    },
    14: {
        "problem": "Overindulgence and lack of moderation in pleasures",
        "problem_hi": "अत्यधिक भोग और सुखों में संयम की कमी",
        "action": "Pick one habit to moderate this month — small discipline = large freedom",
        "action_hi": "इस महीने एक आदत में संयम लाएं — छोटा अनुशासन = बड़ी आजादी",
    },
    16: {
        "problem": "Ego attachment that invites sudden falls — pride before clarity",
        "problem_hi": "अहंकार से जुड़ाव जो अचानक पतन को आमंत्रित करता है",
        "action": "Before any major decision, ask: 'Is my ego or my wisdom driving this?'",
        "action_hi": "किसी भी बड़े निर्णय से पहले पूछें: 'यह मेरा अहंकार चला रहा है या मेरी बुद्धि?'",
    },
    19: {
        "problem": "Independence that tips into isolation — refusing help when needed",
        "problem_hi": "स्वतंत्रता जो अकेलेपन में बदल जाती है — जरूरत पर भी मदद से इनकार",
        "action": "Identify one person you trust completely — share your real challenges with them",
        "action_hi": "एक ऐसा व्यक्ति पहचानें जिस पर पूरा भरोसा हो — उनसे अपनी असली समस्याएं साझा करें",
    },
}

# ---------------------------------------------------------------------------
# CAREER PATHS per Life Path number
# ---------------------------------------------------------------------------
_CAREERS: dict[int, dict] = {
    1:  {
        "best": ["Entrepreneur", "Business founder", "Military officer", "Innovation leader"],
        "best_hi": ["उद्यमी", "व्यवसाय संस्थापक", "सैन्य अधिकारी", "नवाचार नेता"],
        "avoid": ["Assistant or support roles", "Highly repetitive tasks", "Work with no autonomy"],
        "avoid_hi": ["सहायक या समर्थन भूमिकाएं", "अत्यधिक दोहराव वाले काम", "स्वायत्तता रहित कार्य"],
    },
    2:  {
        "best": ["Counselor", "Mediator", "Diplomat", "Therapist", "Music teacher"],
        "best_hi": ["परामर्शदाता", "मध्यस्थ", "राजनयिक", "चिकित्सक", "संगीत शिक्षक"],
        "avoid": ["High-pressure sales", "Confrontational leadership roles", "Isolation-heavy work"],
        "avoid_hi": ["उच्च दबाव की बिक्री", "टकराव वाली नेतृत्व भूमिकाएं", "अकेलेपन का काम"],
    },
    3:  {
        "best": ["Writer", "Content creator", "Public speaker", "Actor", "Marketing professional"],
        "best_hi": ["लेखक", "कंटेंट क्रिएटर", "सार्वजनिक वक्ता", "अभिनेता", "मार्केटिंग पेशेवर"],
        "avoid": ["Highly analytical data work", "Isolated research", "Repetitive manufacturing"],
        "avoid_hi": ["उच्च विश्लेषणात्मक डेटा कार्य", "एकांत अनुसंधान", "दोहराव वाला उत्पादन"],
    },
    4:  {
        "best": ["Engineer", "Architect", "Accountant", "Project manager", "Real estate developer"],
        "best_hi": ["इंजीनियर", "वास्तुकार", "लेखाकार", "परियोजना प्रबंधक", "रियल एस्टेट डेवलपर"],
        "avoid": ["Unpredictable startup chaos", "Purely creative roles without structure", "Frequent travel jobs"],
        "avoid_hi": ["अनिश्चित स्टार्टअप माहौल", "बिना संरचना के रचनात्मक भूमिकाएं", "बार-बार यात्रा वाले काम"],
    },
    5:  {
        "best": ["Journalist", "Travel industry", "Sales professional", "Digital nomad", "PR consultant"],
        "best_hi": ["पत्रकार", "यात्रा उद्योग", "बिक्री पेशेवर", "डिजिटल नोमैड", "पीआर सलाहकार"],
        "avoid": ["Desk jobs with no variety", "Long-term fixed projects", "Bureaucratic government roles"],
        "avoid_hi": ["बिना विविधता के डेस्क काम", "दीर्घकालिक निश्चित परियोजनाएं", "नौकरशाही सरकारी भूमिकाएं"],
    },
    6:  {
        "best": ["Doctor", "Teacher", "Interior designer", "Social worker", "Family therapist"],
        "best_hi": ["डॉक्टर", "शिक्षक", "इंटीरियर डिज़ाइनर", "समाज सेवक", "परिवार चिकित्सक"],
        "avoid": ["Cutthroat competitive business", "Work that ignores human impact", "Isolated technical roles"],
        "avoid_hi": ["बेरहम प्रतिस्पर्धी व्यवसाय", "मानवीय प्रभाव की उपेक्षा करने वाला काम", "एकांत तकनीकी भूमिकाएं"],
    },
    7:  {
        "best": ["Researcher", "Philosopher", "Data scientist", "Astrologer", "Psychologist"],
        "best_hi": ["अनुसंधानकर्ता", "दार्शनिक", "डेटा वैज्ञानिक", "ज्योतिषी", "मनोवैज्ञानिक"],
        "avoid": ["High-volume client-facing sales", "Constant social networking", "Routine administrative work"],
        "avoid_hi": ["उच्च मात्रा की ग्राहक-सामना बिक्री", "निरंतर सामाजिक नेटवर्किंग", "नियमित प्रशासनिक कार्य"],
    },
    8:  {
        "best": ["CEO", "Investor", "Banker", "Corporate lawyer", "Real estate mogul"],
        "best_hi": ["सीईओ", "निवेशक", "बैंकर", "कॉर्पोरेट वकील", "रियल एस्टेट मुगल"],
        "avoid": ["Charity-only roles with no financial growth", "Support roles with no authority", "Creative arts without business"],
        "avoid_hi": ["बिना आर्थिक विकास की दान भूमिकाएं", "बिना अधिकार की सहायता भूमिकाएं", "बिना व्यवसाय की रचनात्मक कलाएं"],
    },
    9:  {
        "best": ["NGO leader", "Healer", "Teacher", "Spiritual guide", "International aid worker"],
        "best_hi": ["एनजीओ नेता", "उपचारक", "शिक्षक", "आध्यात्मिक मार्गदर्शक", "अंतरराष्ट्रीय सहायता कर्मी"],
        "avoid": ["Pure profit-driven business", "Roles that ignore human welfare", "Short-term transactional jobs"],
        "avoid_hi": ["शुद्ध लाभ-चालित व्यवसाय", "मानव कल्याण की उपेक्षा करने वाली भूमिकाएं", "अल्पकालिक लेन-देन के काम"],
    },
    11: {
        "best": ["Spiritual teacher", "Innovative artist", "Visionary entrepreneur", "Inspirational speaker"],
        "best_hi": ["आध्यात्मिक शिक्षक", "अभिनव कलाकार", "दूरदर्शी उद्यमी", "प्रेरणादायक वक्ता"],
        "avoid": ["Pure routine administration", "High-pressure deadline-driven roles", "Work that ignores intuition"],
        "avoid_hi": ["शुद्ध नियमित प्रशासन", "उच्च दबाव की समय-सीमा भूमिकाएं", "अंतर्ज्ञान की उपेक्षा करने वाला काम"],
    },
    22: {
        "best": ["Large-scale project leader", "Urban planner", "Social reformer", "Global NGO director"],
        "best_hi": ["बड़े पैमाने की परियोजना नेता", "शहरी योजनाकार", "सामाजिक सुधारक", "वैश्विक एनजीओ निदेशक"],
        "avoid": ["Small-scope work with no vision", "Roles limited to individual output only", "Work without measurable impact"],
        "avoid_hi": ["बिना दृष्टि के छोटे दायरे का काम", "केवल व्यक्तिगत उत्पादन तक सीमित भूमिकाएं", "बिना मापनीय प्रभाव का काम"],
    },
    33: {
        "best": ["Healer", "Master teacher", "Counselor", "Community leader", "Humanitarian activist"],
        "best_hi": ["उपचारक", "महा शिक्षक", "परामर्शदाता", "सामुदायिक नेता", "मानवतावादी कार्यकर्ता"],
        "avoid": ["Profit-only corporate roles", "Work that creates division", "Roles requiring constant competition"],
        "avoid_hi": ["केवल लाभ वाली कॉर्पोरेट भूमिकाएं", "विभाजन पैदा करने वाला काम", "निरंतर प्रतिस्पर्धा की भूमिकाएं"],
    },
}

# ---------------------------------------------------------------------------
# AFFIRMATIONS per Life Path
# ---------------------------------------------------------------------------
_AFFIRMATIONS: dict[int, dict] = {
    1:  {"en": "I lead with courage and inspire through action — my path creates the way for others.",
         "hi": "मैं साहस से नेतृत्व करता/करती हूँ — मेरा मार्ग दूसरों के लिए रास्ता बनाता है।"},
    2:  {"en": "My sensitivity is my superpower — I build bridges others cannot see.",
         "hi": "मेरी संवेदनशीलता मेरी महाशक्ति है — मैं वे सेतु बनाता/बनाती हूँ जो दूसरे नहीं देख सकते।"},
    3:  {"en": "My voice and creativity are my gifts to the world — I express freely and completely.",
         "hi": "मेरी आवाज़ और रचनात्मकता दुनिया को मेरा उपहार है — मैं स्वतंत्र और पूर्णता से व्यक्त करता/करती हूँ।"},
    4:  {"en": "I build with patience and purpose — everything I create lasts because I care deeply.",
         "hi": "मैं धैर्य और उद्देश्य से निर्माण करता/करती हूँ — जो मैं बनाता/बनाती हूँ वह टिकता है क्योंकि मैं गहराई से परवाह करता/करती हूँ।"},
    5:  {"en": "Change is my ally — I grow through every experience and bring wisdom to new horizons.",
         "hi": "बदलाव मेरा साथी है — मैं हर अनुभव से बढ़ता/बढ़ती हूँ और नए क्षितिज पर ज्ञान लाता/लाती हूँ।"},
    6:  {"en": "I give love generously and receive it fully — my home is my sanctuary and strength.",
         "hi": "मैं प्रेम उदारता से देता/देती हूँ और पूर्णता से पाता/पाती हूँ — मेरा घर मेरी शक्ति है।"},
    7:  {"en": "My depth of understanding is rare — I trust my inner knowing and share it wisely.",
         "hi": "मेरी समझ की गहराई दुर्लभ है — मैं अपने आंतरिक ज्ञान पर भरोसा करता/करती हूँ और इसे बुद्धिमानी से साझा करता/करती हूँ।"},
    8:  {"en": "I create abundance with integrity — my success empowers everyone around me.",
         "hi": "मैं ईमानदारी से समृद्धि बनाता/बनाती हूँ — मेरी सफलता मेरे आसपास के सभी को सशक्त बनाती है।"},
    9:  {"en": "My compassion changes lives — I release the past and embrace the full beauty of now.",
         "hi": "मेरी करुणा जीवन बदलती है — मैं अतीत को छोड़ता/छोड़ती हूँ और अभी की पूर्ण सुंदरता को अपनाता/अपनाती हूँ।"},
    11: {"en": "My intuition guides me to extraordinary purpose — I trust the light within.",
         "hi": "मेरा अंतर्ज्ञान मुझे असाधारण उद्देश्य तक ले जाता है — मैं अपने भीतर की रोशनी पर भरोसा करता/करती हूँ।"},
    22: {"en": "I am here to build what has never existed — my vision becomes reality through disciplined action.",
         "hi": "मैं वह बनाने के लिए यहाँ हूँ जो कभी नहीं था — मेरी दृष्टि अनुशासित कार्य से वास्तविकता बनती है।"},
    33: {"en": "My love and teaching heal the world — I am nourished by giving when I honor myself first.",
         "hi": "मेरा प्रेम और शिक्षण दुनिया को ठीक करता है — जब मैं पहले खुद का सम्मान करता/करती हूँ तो देने से पोषण मिलता है।"},
}

# ---------------------------------------------------------------------------
# LO SHU PLANE DIAGNOSIS (which plane weak = what problem)
# ---------------------------------------------------------------------------
_PLANE_WEAK: dict[str, dict] = {
    "mental": {
        "issue": "Difficulty with planning and logical thinking",
        "issue_hi": "योजना बनाने और तार्किक सोच में कठिनाई",
        "fix": "Daily reading and writing practice — even 15 minutes trains the mental plane",
        "fix_hi": "दैनिक पढ़ने-लिखने का अभ्यास — 15 मिनट भी मानसिक तल को प्रशिक्षित करता है",
    },
    "emotional": {
        "issue": "Emotional instability or difficulty expressing feelings",
        "issue_hi": "भावनात्मक अस्थिरता या भावनाएं व्यक्त करने में कठिनाई",
        "fix": "Journaling 3 emotions daily — naming emotions reduces their power over you",
        "fix_hi": "रोज़ 3 भावनाएं लिखें — भावनाओं को नाम देने से उनकी शक्ति कम होती है",
    },
    "practical": {
        "issue": "Lack of follow-through — ideas exist but execution is weak",
        "issue_hi": "अनुसरण की कमी — विचार हैं लेकिन क्रियान्वयन कमजोर है",
        "fix": "Create one physical checklist each morning — action beats intention every time",
        "fix_hi": "हर सुबह एक भौतिक चेकलिस्ट बनाएं — क्रिया हर बार इरादे को हराती है",
    },
}


def _current_age(birth_date: str) -> int:
    try:
        y, m, d = int(birth_date[:4]), int(birth_date[5:7]), int(birth_date[8:10])
        today = _date.today()
        return today.year - y - ((today.month, today.day) < (m, d))
    except Exception:
        return 35


def _pick_current_pinnacle(pinnacles_block: dict, birth_date: str) -> dict | None:
    try:
        age = _current_age(birth_date)
        for p in pinnacles_block.get("pinnacles", []):
            if p["age_start"] <= age < p["age_end"]:
                return p
    except Exception:
        pass
    return None


def _weak_planes(loshu_planes: dict) -> list[str]:
    weak = []
    for plane_key in ("mental", "emotional", "practical"):
        plane = loshu_planes.get(plane_key, {})
        count = plane.get("count", None)
        numbers = plane.get("numbers", [])
        if count is None:
            count = len([n for n in numbers if loshu_planes.get(plane_key, {}).get("present", True)])
        if count == 0:
            weak.append(plane_key)
    return weak


def generate_insights(result: dict, birth_date: str = "") -> dict:
    """
    Generate the master insight block from a calculate_numerology() result.

    Args:
        result: Full dict returned by calculate_numerology()
        birth_date: YYYY-MM-DD string (used for age calculations)

    Returns:
        dict with core_profile, top_problems, top_actions, success_path,
        lo_shu_diagnosis, timeline_now, affirmation
    """
    lp = result.get("life_path", 9)
    destiny = result.get("destiny", 9)
    soul_urge = result.get("soul_urge", 9)
    personality = result.get("personality", 9)
    karmic_debts = result.get("karmic_debts", [])
    missing_nums = result.get("missing_numbers", [])
    loshu_planes = result.get("loshu_planes", {})
    pinnacles_block = result.get("pinnacles", {})
    personal_year = result.get("personal_year", 1)
    personal_year_pred = result.get("personal_year_prediction", {})

    # ------------------------------------------------------------------
    # 1. CORE PROFILE — top 3 traits from LP + Destiny + Soul Urge
    # ------------------------------------------------------------------
    seen_nums: set[int] = set()
    trait_sources = [lp, destiny, soul_urge]
    traits_en, traits_hi = [], []
    for n in trait_sources:
        if n not in seen_nums and n in _TRAITS:
            seen_nums.add(n)
            traits_en.append(_TRAITS[n]["en"])
            traits_hi.append(_TRAITS[n]["hi"])

    lp_theme = result.get("predictions", {}).get("life_path", {}).get("theme", "")
    lp_theme_hi = result.get("predictions", {}).get("life_path", {}).get("theme_hi", "")
    dest_theme = result.get("predictions", {}).get("destiny", {}).get("theme", "")
    dest_theme_hi = result.get("predictions", {}).get("destiny", {}).get("theme_hi", "")

    # Strip leading "The " from theme strings (e.g. "The Humanitarian" → "Humanitarian")
    def _clean(s: str) -> str:
        return s[4:] if s.startswith("The ") else s

    if lp_theme and dest_theme:
        summary_en = (
            f"You are a {_clean(lp_theme)} at heart ({lp}) with a {_clean(dest_theme)} life mission ({destiny}). "
            f"Your soul craves {_TRAITS.get(soul_urge, {}).get('en', 'depth')} in everything you do."
        )
        summary_hi = (
            f"आप मूल रूप से {lp_theme_hi} ({lp}) हैं और आपका जीवन उद्देश्य {dest_theme_hi} ({destiny}) है। "
            f"आपकी आत्मा हर काम में {_TRAITS.get(soul_urge, {}).get('hi', 'गहराई')} चाहती है।"
        )
    else:
        summary_en = f"Life Path {lp} combined with Destiny {destiny} — you are built for meaningful, purposeful work."
        summary_hi = f"जीवन पथ {lp} और नियति {destiny} — आप अर्थपूर्ण, उद्देश्यपूर्ण कार्य के लिए बने हैं।"

    core_profile = {
        "traits": traits_en[:3],
        "traits_hi": traits_hi[:3],
        "summary": summary_en,
        "summary_hi": summary_hi,
    }

    # ------------------------------------------------------------------
    # 2. TOP PROBLEMS — LP shadow + Destiny shadow (deduplicated) + karmic debt
    # ------------------------------------------------------------------
    problems: list[dict] = []
    seen_problems: set[str] = set()

    def _add_problem(p: str, p_hi: str, source: str, action: str, action_hi: str) -> None:
        if p not in seen_problems and len(problems) < 3:
            seen_problems.add(p)
            problems.append({
                "problem": p,
                "problem_hi": p_hi,
                "source": source,
                "action": action,
                "action_hi": action_hi,
            })

    lp_shadow = _SHADOW.get(lp)
    if lp_shadow:
        _add_problem(lp_shadow["problem"], lp_shadow["problem_hi"],
                     f"Life Path {lp}", lp_shadow["action"], lp_shadow["action_hi"])

    dest_shadow = _SHADOW.get(destiny)
    if dest_shadow and destiny != lp:
        _add_problem(dest_shadow["problem"], dest_shadow["problem_hi"],
                     f"Destiny {destiny}", dest_shadow["action"], dest_shadow["action_hi"])

    for kd in karmic_debts[:2]:
        n = kd.get("number")
        extra = _KARMIC_EXTRA.get(n)
        if extra:
            _add_problem(extra["problem"], extra["problem_hi"],
                         f"Karmic Debt {n}", extra["action"], extra["action_hi"])

    # Fallback: soul urge shadow if still < 3 problems
    su_shadow = _SHADOW.get(soul_urge)
    if su_shadow and soul_urge not in (lp, destiny):
        _add_problem(su_shadow["problem"], su_shadow["problem_hi"],
                     f"Soul Urge {soul_urge}", su_shadow["action"], su_shadow["action_hi"])

    # ------------------------------------------------------------------
    # 3. TOP ACTIONS (extracted from problems, deduplicated)
    # ------------------------------------------------------------------
    top_actions = [
        {
            "action": p["action"],
            "action_hi": p["action_hi"],
            "why": f"Addresses your {p['source']} pattern",
            "why_hi": f"आपके {p['source']} पैटर्न को संबोधित करता है",
        }
        for p in problems
    ]

    # ------------------------------------------------------------------
    # 4. SUCCESS PATH — from LP (primary career driver)
    # ------------------------------------------------------------------
    career_data = _CAREERS.get(lp, _CAREERS[9])
    success_path = {
        "best_careers": career_data["best"],
        "best_careers_hi": career_data["best_hi"],
        "avoid": career_data["avoid"],
        "avoid_hi": career_data["avoid_hi"],
        "note": f"Career alignment is driven by Life Path {lp}. Your Destiny {destiny} adds the style and approach.",
        "note_hi": f"करियर संरेखण जीवन पथ {lp} द्वारा संचालित है। आपकी नियति {destiny} शैली और दृष्टिकोण जोड़ती है।",
    }

    # ------------------------------------------------------------------
    # 5. LO SHU DIAGNOSIS — missing numbers + weak planes
    # ------------------------------------------------------------------
    lo_shu_issues: list[dict] = []
    lo_shu_fixes: list[str] = []
    lo_shu_fixes_hi: list[str] = []

    for mn in missing_nums[:3]:
        n = mn.get("number")
        meaning = mn.get("meaning", "")
        meaning_hi = mn.get("meaning_hi", "")
        remedy = mn.get("remedy", "")
        remedy_hi = mn.get("remedy_hi", "")
        if meaning:
            lo_shu_issues.append({
                "missing_number": n,
                "issue": meaning,
                "issue_hi": meaning_hi,
            })
        if remedy:
            lo_shu_fixes.append(f"Missing {n}: {remedy}")
            lo_shu_fixes_hi.append(f"अनुपस्थित {n}: {remedy_hi}" if remedy_hi else f"अनुपस्थित {n}: {remedy}")

    # Weak plane diagnosis (count == 0 means no digits for that plane)
    plane_diagnoses: list[dict] = []
    for plane_key in ("mental", "emotional", "practical"):
        plane = loshu_planes.get(plane_key, {})
        if isinstance(plane, dict) and plane.get("count", 1) == 0:
            diag = _PLANE_WEAK.get(plane_key, {})
            if diag:
                plane_diagnoses.append({
                    "plane": plane_key,
                    "issue": diag["issue"],
                    "issue_hi": diag["issue_hi"],
                    "fix": diag["fix"],
                    "fix_hi": diag["fix_hi"],
                })

    lo_shu_diagnosis = {
        "missing_numbers": lo_shu_issues,
        "fixes": lo_shu_fixes,
        "fixes_hi": lo_shu_fixes_hi,
        "weak_planes": plane_diagnoses,
        "has_issues": bool(lo_shu_issues or plane_diagnoses),
    }

    # ------------------------------------------------------------------
    # 6. TIMELINE NOW — current pinnacle + personal year context
    # ------------------------------------------------------------------
    current_p = _pick_current_pinnacle(pinnacles_block, birth_date) if birth_date else None
    age = _current_age(birth_date) if birth_date else None

    if current_p:
        p_pred = current_p.get("prediction", {})
        timeline_now = {
            "age": age,
            "age_range": current_p.get("period", ""),
            "age_range_hi": current_p.get("period_hi", ""),
            "pinnacle_number": current_p.get("number"),
            "phase_name": p_pred.get("theme", ""),
            "phase_name_hi": p_pred.get("theme_hi", ""),
            "phase_summary": p_pred.get("opportunity", p_pred.get("description", "")),
            "phase_summary_hi": p_pred.get("opportunity_hi", p_pred.get("description_hi", "")),
            "personal_year": personal_year,
            "personal_year_theme": personal_year_pred.get("theme", ""),
            "personal_year_theme_hi": personal_year_pred.get("theme_hi", ""),
            "combined_advice": (
                f"You are in a {p_pred.get('theme', 'transition')} phase. "
                f"This year (Personal Year {personal_year}) adds {personal_year_pred.get('theme', 'energy')} energy. "
                f"Use both forces together."
            ),
            "combined_advice_hi": (
                f"आप {p_pred.get('theme_hi', 'परिवर्तन')} चरण में हैं। "
                f"यह वर्ष (व्यक्तिगत वर्ष {personal_year}) {personal_year_pred.get('theme_hi', 'ऊर्जा')} जोड़ता है। "
                f"दोनों शक्तियों को एक साथ उपयोग करें।"
            ),
        }
    else:
        timeline_now = {
            "age": age,
            "personal_year": personal_year,
            "personal_year_theme": personal_year_pred.get("theme", ""),
            "personal_year_theme_hi": personal_year_pred.get("theme_hi", ""),
            "combined_advice": f"Personal Year {personal_year}: {personal_year_pred.get('theme', '')}. Focus on this year's unique energy.",
            "combined_advice_hi": f"व्यक्तिगत वर्ष {personal_year}: {personal_year_pred.get('theme_hi', '')}। इस वर्ष की अनूठी ऊर्जा पर ध्यान दें।",
        }

    # ------------------------------------------------------------------
    # 7. AFFIRMATION — from LP (personalized to their primary driver)
    # ------------------------------------------------------------------
    aff = _AFFIRMATIONS.get(lp, _AFFIRMATIONS[9])

    return {
        "core_profile": core_profile,
        "top_problems": problems,
        "top_actions": top_actions,
        "success_path": success_path,
        "lo_shu_diagnosis": lo_shu_diagnosis,
        "timeline_now": timeline_now,
        "affirmation": aff["en"],
        "affirmation_hi": aff["hi"],
    }
