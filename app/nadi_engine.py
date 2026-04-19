"""
nadi_engine.py -- Nadi Astrology Interpretive Engine
=====================================================
Implements Nadi Astrology principles based on planetary conjunctions,
house placements, and inter-planetary relationships.
"""

from typing import Any, Dict, List

# ── Conjunction Rules (planets in the same house) ─────────────────────
NADI_CONJUNCTION_RULES = [
    {
        "planets": {"Sun", "Mercury"},
        "title_en": "Budha-Aditya Yoga",
        "title_hi": "बुधादित्य योग",
        "desc_en": "High intelligence, administrative skills, and a career in communication or education.",
        "desc_hi": "उच्च बुद्धि, प्रशासनिक कौशल और संचार या शिक्षा के क्षेत्र में करियर।"
    },
    {
        "planets": {"Jupiter", "Mars"},
        "title_en": "Guru-Mangala Yoga",
        "title_hi": "गुरु-मंगल योग",
        "desc_en": "Noble character, leadership qualities, and success in legal or management fields.",
        "desc_hi": "नेक चरित्र, नेतृत्व गुण और कानूनी या प्रबंधन क्षेत्रों में सफलता।"
    },
    {
        "planets": {"Venus", "Mercury"},
        "title_en": "Lakshmi-Saraswati Yoga",
        "title_hi": "लक्ष्मी-सरस्वती योग",
        "desc_en": "Artistic talent, refined speech, and prosperity through creative ventures.",
        "desc_hi": "कलात्मक प्रतिभा, परिष्कृत वाणी और रचनात्मक कार्यों के माध्यम से समृद्धि।"
    },
    {
        "planets": {"Saturn", "Jupiter"},
        "title_en": "Dharma-Karmadhipati Yoga",
        "title_hi": "धर्म-कर्माधिपति योग",
        "desc_en": "Success through ethical conduct, social responsibility, and respected positions.",
        "desc_hi": "नैतिक आचरण, सामाजिक जिम्मेदारी और सम्मानित पदों के माध्यम से सफलता।"
    },
    {
        "planets": {"Mars", "Moon"},
        "title_en": "Chandra-Mangala Yoga",
        "title_hi": "चंद्र-मंगल योग",
        "desc_en": "Courageous mind, success in commerce, and ability to handle complex emotional situations.",
        "desc_hi": "साहसी मन, वाणिज्य में सफलता और जटिल भावनात्मक स्थितियों को संभालने की क्षमता।"
    },
    {
        "planets": {"Sun", "Jupiter"},
        "title_en": "Jiva-Atma Yoga",
        "title_hi": "जीव-आत्मा योग",
        "desc_en": "Spiritual growth, wisdom from elders, and recognition in religious or ethical circles.",
        "desc_hi": "आध्यात्मिक विकास, बड़ों से ज्ञान, और धार्मिक या नैतिक हलकों में पहचान।"
    },
    {
        "planets": {"Saturn", "Mars"},
        "title_en": "Karma-Shakti Yoga",
        "title_hi": "कर्म-शक्ति योग",
        "desc_en": "Intense drive, technical skills, and success through rigorous discipline and hard work.",
        "desc_hi": "तीव्र इच्छाशक्ति, तकनीकी कौशल और कठोर अनुशासन और कड़ी मेहनत के माध्यम से सफलता।"
    },
    {
        "planets": {"Moon", "Jupiter"},
        "title_en": "Gajakesari Nadi Conjunction",
        "title_hi": "गजकेसरी नाड़ी युति",
        "desc_en": "Wisdom married to intuition — the native is eloquent, respected, and blessed with spiritual insight.",
        "desc_hi": "ज्ञान और अंतर्ज्ञान का संयोग — वक्तृत्व शक्ति, सम्मान और आध्यात्मिक दृष्टि।"
    },
    {
        "planets": {"Venus", "Jupiter"},
        "title_en": "Shukra-Guru Yoga",
        "title_hi": "शुक्र-गुरु योग",
        "desc_en": "Wealth through wisdom — prosperity, marital happiness, and spiritual refinement together.",
        "desc_hi": "ज्ञान से समृद्धि — वैवाहिक सुख, आध्यात्मिक परिष्कार और आर्थिक उन्नति।"
    },
    {
        "planets": {"Sun", "Venus"},
        "title_en": "Surya-Shukra Yoga",
        "title_hi": "सूर्य-शुक्र योग",
        "desc_en": "Authority combined with artistic flair — success in government, arts, and luxury sectors.",
        "desc_hi": "अधिकार और कलात्मक प्रतिभा का संगम — सरकारी, कला और विलासिता क्षेत्र में सफलता।"
    },
    {
        "planets": {"Moon", "Venus"},
        "title_en": "Chandra-Shukra Yoga",
        "title_hi": "चंद्र-शुक्र योग",
        "desc_en": "Beauty, poetic sensitivity, and emotional depth — gifted in the arts and highly charismatic.",
        "desc_hi": "सौंदर्य, काव्य संवेदनशीलता और भावनात्मक गहराई — कला में प्रतिभा और उच्च आकर्षण।"
    },
    {
        "planets": {"Saturn", "Moon"},
        "title_en": "Shani-Chandra Yoga",
        "title_hi": "शनि-चंद्र योग",
        "desc_en": "Serious emotional nature, perseverance through hardship, and success via sustained effort.",
        "desc_hi": "गंभीर भावनात्मक स्वभाव, कठिनाइयों में दृढ़ता और निरंतर प्रयास से सफलता।"
    },
    {
        "planets": {"Sun", "Mars"},
        "title_en": "Surya-Mangala Yoga",
        "title_hi": "सूर्य-मंगल योग",
        "desc_en": "Fiery courage and leadership — military, sports, or executive success with dynamic authority.",
        "desc_hi": "साहस और नेतृत्व — सैन्य, खेल या कार्यकारी सफलता, गतिशील अधिकार।"
    },
    {
        "planets": {"Rahu", "Jupiter"},
        "title_en": "Guru-Chandala Yoga (Nadi)",
        "title_hi": "गुरु-चांडाल योग (नाड़ी)",
        "desc_en": "Unconventional wisdom — breaks traditional boundaries; success through innovative thinking but spiritual restlessness.",
        "desc_hi": "अपरंपरागत ज्ञान — परंपराओं की सीमाएं तोड़ना; अभिनव सोच से सफलता लेकिन आध्यात्मिक बेचैनी।"
    },
    {
        "planets": {"Rahu", "Saturn"},
        "title_en": "Shrapit Nadi Conjunction",
        "title_hi": "श्रापित नाड़ी युति",
        "desc_en": "Karmic delays and obstacles in career — requires patience; past-life karmic dues to be paid through this life's hardships.",
        "desc_hi": "करियर में कार्मिक विलंब और बाधाएं — धैर्य आवश्यक; पूर्व जन्म के कर्म इस जीवन की कठिनाइयों से चुकाने होंगे।"
    },
    {
        "planets": {"Ketu", "Jupiter"},
        "title_en": "Ketu-Guru Yoga (Nadi)",
        "title_hi": "केतु-गुरु योग (नाड़ी)",
        "desc_en": "Moksha-oriented wisdom — deep spiritual insight, past-life knowledge, and detachment from material pursuits.",
        "desc_hi": "मोक्ष-उन्मुख ज्ञान — गहरी आध्यात्मिक अंतर्दृष्टि, पूर्व जन्म का ज्ञान और भौतिक इच्छाओं से वैराग्य।"
    },
    {
        "planets": {"Mercury", "Mars"},
        "title_en": "Budha-Mangala Yoga",
        "title_hi": "बुध-मंगल योग",
        "desc_en": "Sharp analytical mind with decisive action — excellent for engineering, surgery, and strategic fields.",
        "desc_hi": "तीव्र विश्लेषणात्मक मन और निर्णायक कार्यशैली — इंजीनियरिंग, शल्य-चिकित्सा और रणनीतिक क्षेत्रों के लिए उत्कृष्ट।"
    },
    {
        "planets": {"Mercury", "Moon"},
        "title_en": "Budha-Chandra Yoga",
        "title_hi": "बुध-चंद्र योग",
        "desc_en": "Emotional intelligence and sharp memory — gifted in writing, counseling, and public relations.",
        "desc_hi": "भावनात्मक बुद्धि और तीव्र स्मृति — लेखन, परामर्श और जनसंपर्क में प्रतिभाशाली।"
    },
    {
        "planets": {"Venus", "Mars"},
        "title_en": "Shukra-Mangala Yoga",
        "title_hi": "शुक्र-मंगल योग",
        "desc_en": "Passionate creativity — dynamic artistic expression, strong physical vitality, and magnetic personality.",
        "desc_hi": "भावुक रचनात्मकता — गतिशील कलात्मक अभिव्यक्ति, शारीरिक जीवन शक्ति और चुंबकीय व्यक्तित्व।"
    },
    {
        "planets": {"Saturn", "Venus"},
        "title_en": "Shani-Shukra Yoga",
        "title_hi": "शनि-शुक्र योग",
        "desc_en": "Disciplined artistic pursuit — long-term gains in art, architecture, and luxury trades through perseverance.",
        "desc_hi": "अनुशासित कलात्मक अनुसरण — दृढ़ता से कला, वास्तुकला और विलासिता व्यापार में दीर्घकालिक लाभ।"
    },
]

# ── Per-Planet House Placement Insights ───────────────────────────────
# Key placements that always generate an insight regardless of conjunctions
_PLANET_HOUSE_INSIGHTS: Dict[tuple, Dict[str, str]] = {
    ("Sun", 1): {
        "title_en": "Sun in Lagna — Commanding Personality",
        "title_hi": "लग्न में सूर्य — आज्ञाकारी व्यक्तित्व",
        "desc_en": "The Nadi classical tradition identifies Sun in Lagna as the mark of a leader — authority is natural, government favor follows, and the native's vitality shapes their entire destiny.",
        "desc_hi": "नाड़ी परंपरा के अनुसार लग्न में सूर्य नेतृत्व का चिह्न है — सत्ता स्वाभाविक है, सरकारी कृपा मिलती है।"
    },
    ("Sun", 5): {
        "title_en": "Sun in 5th — Intellectual Authority",
        "title_hi": "पंचम में सूर्य — बौद्धिक प्राधिकार",
        "desc_en": "Nadi text: Sun illuminates the 5th — father's blessings, political intelligence, creative powers, and children who carry the father's legacy forward.",
        "desc_hi": "नाड़ी ग्रंथ: पंचम में सूर्य — पिता का आशीर्वाद, राजनीतिक बुद्धि, रचनात्मकता और पिता की विरासत आगे बढ़ाने वाली संतान।"
    },
    ("Sun", 9): {
        "title_en": "Sun in 9th — Dharmic Father",
        "title_hi": "नवम में सूर्य — धार्मिक पिता",
        "desc_en": "Nadi classical: Sun in the house of Dharma gives a noble father, respect in spiritual circles, and fortune through righteous deeds.",
        "desc_hi": "नाड़ी ग्रंथ: धर्म भाव में सूर्य — महान पिता, आध्यात्मिक क्षेत्रों में सम्मान और धार्मिक कर्मों से भाग्य।"
    },
    ("Sun", 10): {
        "title_en": "Sun in 10th — Career Peak",
        "title_hi": "दशम में सूर्य — करियर शिखर",
        "desc_en": "The Sun at the zenith of the chart: government service, executive positions, and a career that defines the family's standing in society.",
        "desc_hi": "कुंडली के शिखर पर सूर्य: सरकारी सेवा, कार्यकारी पद और समाज में परिवार की स्थिति को परिभाषित करने वाला करियर।"
    },
    ("Moon", 4): {
        "title_en": "Moon in 4th — Emotional Comfort & Property",
        "title_hi": "चतुर्थ में चंद्र — भावनात्मक सुख और संपत्ति",
        "desc_en": "Nadi text: Moon in the 4th house — mother's blessings are paramount; ancestral property, emotional comfort, and happiness from home form the core of this life.",
        "desc_hi": "नाड़ी ग्रंथ: चतुर्थ में चंद्र — माता का आशीर्वाद सर्वोपरि; पैतृक संपत्ति, भावनात्मक सुख और घर से खुशी।"
    },
    ("Moon", 7): {
        "title_en": "Moon in 7th — Emotional Partnerships",
        "title_hi": "सप्तम में चंद्र — भावनात्मक साझेदारी",
        "desc_en": "Moon in the house of relationships: the native seeks emotional security in partnerships; spouse is nurturing but relationships fluctuate with the Moon's phases.",
        "desc_hi": "सप्तम में चंद्र: साझेदारियों में भावनात्मक सुरक्षा की तलाश; जीवनसाथी पोषणकारी पर रिश्ते चंद्रमा की कलाओं के साथ बदलते हैं।"
    },
    ("Moon", 10): {
        "title_en": "Moon in 10th — Public Popularity",
        "title_hi": "दशम में चंद्र — सार्वजनिक लोकप्रियता",
        "desc_en": "Nadi classical: Moon at the career peak brings fluctuating but ultimately high public recognition; success in service industries, hospitality, and the public sphere.",
        "desc_hi": "नाड़ी ग्रंथ: दशम में चंद्र — उतार-चढ़ाव पर अंततः उच्च सार्वजनिक पहचान; सेवा उद्योगों और जन-क्षेत्र में सफलता।"
    },
    ("Jupiter", 1): {
        "title_en": "Jupiter in Lagna — Wisdom Embodied",
        "title_hi": "लग्न में गुरु — ज्ञान की साक्षात् मूर्ति",
        "desc_en": "Nadi text: Jupiter in Lagna makes the native a natural teacher and counselor; spiritual wisdom, noble character, and respect in society come naturally.",
        "desc_hi": "नाड़ी ग्रंथ: लग्न में गुरु — स्वाभाविक शिक्षक और परामर्शदाता; आध्यात्मिक ज्ञान, नेक चरित्र और समाज में सम्मान।"
    },
    ("Jupiter", 5): {
        "title_en": "Jupiter in 5th — Vidya & Progeny Blessings",
        "title_hi": "पंचम में गुरु — विद्या और संतान का आशीर्वाद",
        "desc_en": "The most auspicious placement for knowledge and children: Nadi traditions say Jupiter in the 5th gives scholarly children, deep learning, and devotional spiritual life.",
        "desc_hi": "विद्या और संतान के लिए सर्वाधिक शुभ स्थिति: नाड़ी परंपरा — पंचम में गुरु विद्वान संतान, गहन अध्ययन और भक्तिमय जीवन देता है।"
    },
    ("Jupiter", 9): {
        "title_en": "Jupiter in 9th — Dharma & Higher Learning",
        "title_hi": "नवम में गुरु — धर्म और उच्च ज्ञान",
        "desc_en": "Nadi classical: Jupiter in the house of Dharma — the guru principle is maximally expressed; pilgrimages, philosophy, and a life guided by higher principles.",
        "desc_hi": "नाड़ी ग्रंथ: धर्म भाव में गुरु — गुरु तत्व पूर्णतः व्यक्त; तीर्थयात्रा, दर्शन और उच्च सिद्धांतों से मार्गदर्शित जीवन।"
    },
    ("Venus", 7): {
        "title_en": "Venus in 7th — Auspicious Marriage",
        "title_hi": "सप्तम में शुक्र — शुभ विवाह",
        "desc_en": "Nadi text: Venus in its own house of partnership — beautiful spouse, harmonious marriage, and gains through business partnerships and the arts.",
        "desc_hi": "नाड़ी ग्रंथ: सप्तम में शुक्र — सुंदर जीवनसाथी, सामंजस्यपूर्ण विवाह और व्यापारिक साझेदारी से लाभ।"
    },
    ("Saturn", 10): {
        "title_en": "Saturn in 10th — Career Through Discipline",
        "title_hi": "दशम में शनि — अनुशासन से करियर",
        "desc_en": "Nadi text: Saturn in the 10th house indicates slow but steady career ascent — success comes late but is enduring; authority through service and hard work.",
        "desc_hi": "नाड़ी ग्रंथ: दशम में शनि — धीमी पर स्थिर करियर प्रगति; सफलता देर से आती है पर टिकाऊ होती है; सेवा से अधिकार।"
    },
    ("Mars", 3): {
        "title_en": "Mars in 3rd — Courageous Initiatives",
        "title_hi": "तृतीय में मंगल — साहसी पहल",
        "desc_en": "Nadi text: Mars in the 3rd gives tremendous courage, younger sibling support, and success through bold self-initiative in competitive fields.",
        "desc_hi": "नाड़ी ग्रंथ: तृतीय में मंगल — अत्यधिक साहस, छोटे भाई-बहनों का सहयोग और प्रतिस्पर्धी क्षेत्रों में साहसी पहल से सफलता।"
    },
    ("Mars", 10): {
        "title_en": "Mars in 10th — Executive Power",
        "title_hi": "दशम में मंगल — कार्यकारी शक्ति",
        "desc_en": "Nadi classical: Mars in the 10th brings authority, military or engineering career, and the ability to lead others through sheer willpower.",
        "desc_hi": "नाड़ी ग्रंथ: दशम में मंगल — सत्ता, सैन्य या इंजीनियरिंग करियर और इच्छाशक्ति से दूसरों का नेतृत्व।"
    },
    ("Mercury", 1): {
        "title_en": "Mercury in Lagna — Intellect as Identity",
        "title_hi": "लग्न में बुध — बुद्धि ही पहचान",
        "desc_en": "Nadi text: Mercury rising in Lagna makes intellect the defining trait — communication, commerce, and analytical ability shine throughout life.",
        "desc_hi": "नाड़ी ग्रंथ: लग्न में बुध — बुद्धि ही मुख्य गुण; संचार, व्यापार और विश्लेषणात्मक क्षमता जीवनभर चमकती है।"
    },
    ("Mercury", 10): {
        "title_en": "Mercury in 10th — Communication Career",
        "title_hi": "दशम में बुध — संचार करियर",
        "desc_en": "Nadi classical: Mercury at the career point — writing, journalism, teaching, and consultancy are highlighted paths; the native's words shape their professional destiny.",
        "desc_hi": "नाड़ी ग्रंथ: दशम में बुध — लेखन, पत्रकारिता, शिक्षण और परामर्श; वाणी से व्यावसायिक भाग्य।"
    },
    ("Sun", 4): {
        "title_en": "Sun in 4th — Ancestral Authority",
        "title_hi": "चतुर्थ में सूर्य — पैतृक प्राधिकार",
        "desc_en": "Nadi text: Sun in the 4th intensifies the father's influence on the home; ancestral prestige, property from government, and a life rooted in tradition and lineage.",
        "desc_hi": "नाड़ी ग्रंथ: चतुर्थ में सूर्य — पिता का घर पर गहरा प्रभाव; पैतृक प्रतिष्ठा, सरकार से संपत्ति और परंपरा में जीवन।"
    },
    ("Sun", 7): {
        "title_en": "Sun in 7th — Partner's Domination",
        "title_hi": "सप्तम में सूर्य — साथी का वर्चस्व",
        "desc_en": "Nadi classical: Sun in the 7th creates a powerful spouse dynamic — the native seeks authority in partnerships but must guard against ego conflicts in marriage.",
        "desc_hi": "नाड़ी ग्रंथ: सप्तम में सूर्य — शक्तिशाली जीवनसाथी; साझेदारी में अधिकार चाहते हैं पर विवाह में अहंकार के टकराव से बचें।"
    },
    ("Moon", 1): {
        "title_en": "Moon in Lagna — Emotional Nature Dominant",
        "title_hi": "लग्न में चंद्र — भावनात्मक स्वभाव प्रधान",
        "desc_en": "Nadi text: Moon in Lagna — the native's identity is emotionally driven; highly intuitive, nurturing, and deeply connected to their roots and mother.",
        "desc_hi": "नाड़ी ग्रंथ: लग्न में चंद्र — भावनाओं से संचालित व्यक्तित्व; अत्यंत सहज, पोषणकारी और माता से गहरा जुड़ाव।"
    },
    ("Moon", 5): {
        "title_en": "Moon in 5th — Creative Intuition",
        "title_hi": "पंचम में चंद्र — रचनात्मक अंतर्ज्ञान",
        "desc_en": "Nadi classical: Moon in the 5th — deep connection with children, artistic flair, and an emotionally driven creative life; education through intuitive learning.",
        "desc_hi": "नाड़ी ग्रंथ: पंचम में चंद्र — संतान से गहरा जुड़ाव, कलात्मक प्रतिभा और अंतर्ज्ञानात्मक रचनात्मक जीवन।"
    },
    ("Mars", 1): {
        "title_en": "Mars in Lagna — Warrior Personality",
        "title_hi": "लग्न में मंगल — योद्धा व्यक्तित्व",
        "desc_en": "Nadi text: Mars in the Lagna — the native is bold, action-oriented, and fiercely independent; success in competitive and physical fields is assured.",
        "desc_hi": "नाड़ी ग्रंथ: लग्न में मंगल — साहसी, कर्म-उन्मुख और दृढ़ स्वतंत्र; प्रतिस्पर्धी क्षेत्रों में सफलता निश्चित।"
    },
    ("Mars", 7): {
        "title_en": "Mars in 7th — Passionate Partnerships",
        "title_hi": "सप्तम में मंगल — उत्साही साझेदारी",
        "desc_en": "Nadi classical: Mars in the 7th activates Mangal Dosha — passionate relationships, assertive spouse, and gains through partnerships at the cost of marital friction.",
        "desc_hi": "नाड़ी ग्रंथ: सप्तम में मंगल — मांगलिक दोष; जुझारू जीवनसाथी और वैवाहिक घर्षण की कीमत पर साझेदारी से लाभ।"
    },
    ("Mercury", 3): {
        "title_en": "Mercury in 3rd — Master Communicator",
        "title_hi": "तृतीय में बुध — संचार के उस्ताद",
        "desc_en": "Nadi text: Mercury in the house of communication and short journeys — gifted writer, skilled orator, and successful in media, trade, and sibling connections.",
        "desc_hi": "नाड़ी ग्रंथ: संचार और यात्रा के भाव में बुध — कुशल लेखक, वक्ता और मीडिया, व्यापार एवं भाई-बहनों से सफलता।"
    },
    ("Mercury", 5): {
        "title_en": "Mercury in 5th — Academic Excellence",
        "title_hi": "पंचम में बुध — शैक्षणिक उत्कृष्टता",
        "desc_en": "Nadi classical: Mercury in the 5th — sharp analytical mind applied to speculation, education, and creative writing; children are intelligent and communicative.",
        "desc_hi": "नाड़ी ग्रंथ: पंचम में बुध — तीव्र विश्लेषण शक्ति; सट्टे, शिक्षा और रचनात्मक लेखन में सफलता; बुद्धिमान संतान।"
    },
    ("Venus", 3): {
        "title_en": "Venus in 3rd — Artistic Expression",
        "title_hi": "तृतीय में शुक्र — कलात्मक अभिव्यक्ति",
        "desc_en": "Nadi text: Venus in the 3rd — the native expresses love through art, music, and creative writing; harmony with younger siblings, and gains from artistic communication.",
        "desc_hi": "नाड़ी ग्रंथ: तृतीय में शुक्र — कला, संगीत और लेखन से प्रेम की अभिव्यक्ति; छोटे भाई-बहनों से सामंजस्य।"
    },
    ("Venus", 4): {
        "title_en": "Venus in 4th — Domestic Comfort",
        "title_hi": "चतुर्थ में शुक्र — घरेलू सुख",
        "desc_en": "Nadi classical: Venus in the 4th — beautiful home, devoted mother, property gains, and a life of domestic comfort; artistic sensibility in architecture and home décor.",
        "desc_hi": "नाड़ी ग्रंथ: चतुर्थ में शुक्र — सुंदर घर, समर्पित माता, संपत्ति से लाभ और घरेलू सुख।"
    },
    ("Saturn", 6): {
        "title_en": "Saturn in 6th — Victory Over Enemies",
        "title_hi": "षष्ठ में शनि — शत्रुओं पर विजय",
        "desc_en": "Nadi classical: Saturn in the 6th is powerful — the native defeats enemies through patience and strategy; good health through discipline, success in service and legal fields.",
        "desc_hi": "नाड़ी ग्रंथ: षष्ठ में शनि बलवान — धैर्य और रणनीति से शत्रु पराजित; अनुशासन से स्वास्थ्य और सेवा क्षेत्र में सफलता।"
    },
    ("Saturn", 7): {
        "title_en": "Saturn in 7th — Delayed Marriage",
        "title_hi": "सप्तम में शनि — विलंबित विवाह",
        "desc_en": "Nadi text: Saturn in the 7th delays marriage but makes it lasting — the native finds a mature, responsible spouse after initial relationship challenges.",
        "desc_hi": "नाड़ी ग्रंथ: सप्तम में शनि — विवाह में विलंब पर टिकाऊ; प्रारंभिक चुनौतियों के बाद परिपक्व जीवनसाथी।"
    },
    ("Rahu", 1): {
        "title_en": "Rahu in Lagna — Charismatic Maverick",
        "title_hi": "लग्न में राहु — करिश्माई विद्रोही",
        "desc_en": "Nadi classical: Rahu in the Lagna — magnetic personality, unconventional lifestyle, and a destiny shaped by foreign elements or breaking social norms.",
        "desc_hi": "नाड़ी ग्रंथ: लग्न में राहु — चुंबकीय व्यक्तित्व, अपरंपरागत जीवन और विदेशी तत्वों या सामाजिक मानदंडों को तोड़ने से बना भाग्य।"
    },
    ("Rahu", 12): {
        "title_en": "Rahu in 12th — Foreign Horizons",
        "title_hi": "द्वादश में राहु — विदेश के क्षितिज",
        "desc_en": "Nadi text: Rahu in the 12th — foreign lands, spiritual journeys, and hidden gains characterize this life; expenditure rises but so does spiritual evolution.",
        "desc_hi": "नाड़ी ग्रंथ: द्वादश में राहु — विदेश यात्रा, आध्यात्मिक यात्राएं और गुप्त लाभ; व्यय बढ़ता है पर आध्यात्मिक विकास भी।"
    },
    ("Ketu", 6): {
        "title_en": "Ketu in 6th — Healing Powers",
        "title_hi": "षष्ठ में केतु — उपचार शक्तियां",
        "desc_en": "Nadi classical: Ketu in the 6th — natural healer, victory over enemies through unconventional means, and a past-life karma of service; health fields are highlighted.",
        "desc_hi": "नाड़ी ग्रंथ: षष्ठ में केतु — स्वाभाविक उपचारक, अपरंपरागत माध्यमों से शत्रुओं पर विजय और सेवा का पूर्व जन्म कर्म।"
    },
    ("Jupiter", 1): {
        "title_en": "Jupiter in Lagna — Wisdom Embodied",
        "title_en": "Rahu in 10th — Ambition & Unconventional Career",
        "title_hi": "दशम में राहु — महत्वाकांक्षा और अपरंपरागत करियर",
        "desc_en": "Nadi text: Rahu in the 10th amplifies career ambitions — the native rises through unconventional paths, foreign connections, or technology; fame is possible but requires ethical grounding.",
        "desc_hi": "नाड़ी ग्रंथ: दशम में राहु — करियर महत्वाकांक्षा बढ़ती है; अपरंपरागत मार्ग, विदेशी संबंध या प्रौद्योगिकी से उत्थान।"
    },
    ("Ketu", 12): {
        "title_en": "Ketu in 12th — Moksha Orientation",
        "title_hi": "द्वादश में केतु — मोक्ष अभिमुखता",
        "desc_en": "Nadi classical: Ketu in the 12th is the classic moksha placement — past-life spiritual merit manifests as detachment, foreign journeys, and eventual liberation.",
        "desc_hi": "नाड़ी ग्रंथ: द्वादश में केतु — मोक्ष का क्लासिक स्थान; पूर्व जन्म की आध्यात्मिक योग्यता, वैराग्य और अंतिम मुक्ति।"
    },
}

# ── Mutual Aspect Rules (planets 7 houses apart — universal mutual aspect) ─
NADI_MUTUAL_ASPECT_INSIGHTS = [
    {
        "planets": ("Jupiter", "Moon"),
        "title_en": "Jupiter-Moon Mutual Vision",
        "title_hi": "गुरु-चंद्र परस्पर दृष्टि",
        "desc_en": "Jupiter's wisdom and Moon's intuition mutually reinforce each other across houses — strong protective influence, emotional wisdom, and spiritual clarity throughout life.",
        "desc_hi": "गुरु का ज्ञान और चंद्र की अंतर्ज्ञान शक्ति भावों में परस्पर सशक्त होती है — सुरक्षात्मक प्रभाव, भावनात्मक ज्ञान और आध्यात्मिक स्पष्टता।"
    },
    {
        "planets": ("Saturn", "Jupiter"),
        "title_en": "Saturn-Jupiter Mutual Aspect",
        "title_hi": "शनि-गुरु परस्पर दृष्टि",
        "desc_en": "The two great chronocrators in opposition: dharma meets karma — the native is tested by life's burdens but guided by wisdom; eventual triumph through patience.",
        "desc_hi": "दो महान कालकारक विरोध में: धर्म और कर्म का मिलन — जीवन के बोझ से परीक्षा पर ज्ञान से मार्गदर्शन; धैर्य से अंतिम विजय।"
    },
    {
        "planets": ("Mars", "Saturn"),
        "title_en": "Mars-Saturn Opposition",
        "title_hi": "मंगल-शनि परस्पर दृष्टि",
        "desc_en": "The fire of action meets the ice of discipline — intense pressure that can forge extraordinary achievers or cause frustration; the key is channeling force constructively.",
        "desc_hi": "क्रिया की अग्नि और अनुशासन की बर्फ का मिलन — असाधारण उपलब्धि या निराशा; कुंजी: शक्ति का रचनात्मक उपयोग।"
    },
    {
        "planets": ("Jupiter", "Mercury"),
        "title_en": "Jupiter-Mercury Mutual Vision",
        "title_hi": "गुरु-बुध परस्पर दृष्टि",
        "desc_en": "Wisdom aspecting intellect across houses: Nadi classical says this combination produces scholars, teachers, and communicators of profound knowledge — learning spans an entire lifetime.",
        "desc_hi": "बुद्धि पर ज्ञान की दृष्टि: नाड़ी ग्रंथ — यह संयोग विद्वान, शिक्षक और गहन ज्ञान के संचारक उत्पन्न करता है।"
    },
    {
        "planets": ("Venus", "Mars"),
        "title_en": "Venus-Mars Opposition",
        "title_hi": "शुक्र-मंगल परस्पर दृष्टि",
        "desc_en": "Desire meets drive in opposition — powerful creative tension, passionate relationships, and artistic ambition fueled by competitive energy.",
        "desc_hi": "इच्छा और गति का विरोध — शक्तिशाली रचनात्मक तनाव, भावुक रिश्ते और प्रतिस्पर्धी ऊर्जा से कलात्मक महत्वाकांक्षा।"
    },
    {
        "planets": ("Sun", "Saturn"),
        "title_en": "Sun-Saturn Opposition (Nadi)",
        "title_hi": "सूर्य-शनि परस्पर दृष्टि (नाड़ी)",
        "desc_en": "Nadi text: father vs. discipline — authority is earned through hardship; the native's relationship with authority figures shapes career; late but enduring recognition.",
        "desc_hi": "नाड़ी ग्रंथ: पिता बनाम अनुशासन — कठिनाई से अधिकार अर्जित; अधिकारियों से संबंध करियर को आकार देता है; देर से पर टिकाऊ पहचान।"
    },
    {
        "planets": ("Moon", "Saturn"),
        "title_en": "Moon-Saturn Opposition (Nadi)",
        "title_hi": "चंद्र-शनि परस्पर दृष्टि (नाड़ी)",
        "desc_en": "Nadi classical: emotional sensitivity aspected by karmic discipline — early emotional hardships forge inner resilience; the native succeeds through persistent emotional work.",
        "desc_hi": "नाड़ी ग्रंथ: भावनात्मक संवेदनशीलता पर कार्मिक अनुशासन की दृष्टि — प्रारंभिक कठिनाइयों से आंतरिक मजबूती; दृढ़ता से सफलता।"
    },
]


def calculate_nadi_insights(planet_positions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate Nadi astrology insights from planet placements.
    Covers: same-house conjunctions, key house placements, mutual aspects.
    """
    planets = planet_positions.get("planets", {})
    if not planets:
        return []

    def _safe_house(info: Any) -> int:
        if not isinstance(info, dict):
            return 0
        h = info.get("house", 0)
        try:
            h_int = int(h or 0)
        except (TypeError, ValueError):
            return 0
        return h_int if 1 <= h_int <= 12 else 0

    # Build house map
    house_map: Dict[int, List[str]] = {}
    for planet, info in planets.items():
        h = _safe_house(info)
        if h:
            house_map.setdefault(h, []).append(planet)

    insights: List[Dict[str, Any]] = []
    seen_titles: set = set()

    def _add(insight: dict) -> None:
        key = insight.get("title_en", "")
        if key not in seen_titles:
            seen_titles.add(key)
            insights.append(insight)

    # 1. Same-house conjunction rules
    for house, house_planets in house_map.items():
        if len(house_planets) < 2:
            continue
        planet_set = set(house_planets)
        for rule in NADI_CONJUNCTION_RULES:
            if rule["planets"].issubset(planet_set):
                _add({
                    "house": house,
                    "type": "conjunction",
                    "title_en": rule["title_en"],
                    "title_hi": rule["title_hi"],
                    "desc_en": rule["desc_en"],
                    "desc_hi": rule["desc_hi"],
                    "planets": list(rule["planets"]),
                })

    # 2. Per-planet key house placements
    for planet, info in planets.items():
        h = _safe_house(info)
        key = (planet, h)
        if key in _PLANET_HOUSE_INSIGHTS:
            entry = _PLANET_HOUSE_INSIGHTS[key]
            _add({
                "house": h,
                "type": "placement",
                "title_en": entry["title_en"],
                "title_hi": entry["title_hi"],
                "desc_en": entry["desc_en"],
                "desc_hi": entry["desc_hi"],
                "planets": [planet],
            })

    # 3. Mutual aspect insights (planets 7 houses apart)
    for rule in NADI_MUTUAL_ASPECT_INSIGHTS:
        p1, p2 = rule["planets"]
        h1 = _safe_house(planets.get(p1, {}))
        h2 = _safe_house(planets.get(p2, {}))
        if h1 and h2 and abs(h1 - h2) == 6:  # 7 houses apart (opposite houses)
            _add({
                "house": None,
                "type": "mutual_aspect",
                "title_en": rule["title_en"],
                "title_hi": rule["title_hi"],
                "desc_en": rule["desc_en"],
                "desc_hi": rule["desc_hi"],
                "planets": list(rule["planets"]),
                "houses": [h1, h2],
            })

    # 4. Fallback: generic house-cluster insight for any 2+ planet house
    if len(insights) < 5:
        for house, house_planets in house_map.items():
            if len(house_planets) >= 2:
                combo = " + ".join(sorted(house_planets[:3]))
                _add({
                    "house": house,
                    "type": "cluster",
                    "title_en": f"Planetary Cluster in House {house}",
                    "title_hi": f"भाव {house} में ग्रह समूह",
                    "desc_en": (
                        f"{combo} together in house {house} intensify its significations — "
                        "multiple planetary energies blend to create a concentrated life theme in this area."
                    ),
                    "desc_hi": (
                        f"भाव {house} में {combo} मिलकर उस भाव के महत्व को बढ़ाते हैं — "
                        "अनेक ग्रहों की ऊर्जाएं इस क्षेत्र में केंद्रित जीवन-विषय बनाती हैं।"
                    ),
                    "planets": house_planets[:3],
                })

    return insights
