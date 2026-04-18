"""
lalkitab_engine.py — Lal Kitab Remedies Engine
================================================
Provides Lal Kitab remedies for weak or afflicted planets.
Remedies are specific to each planet × house placement (house = sign number in LK system).
Remedies are prescribed only when planet strength < 0.5 (enemy/debilitated).

Key LK principles encoded:
- Physical materials: copper, silver, gold, iron, wheat, milk, sesame, honey, almonds, radishes, coconut
- Remedies relate to HOUSE themes: H2=wealth/family → donate silver; H7=marriage → offer sweets
- Day-based remedies match each planet's ruling day
- Water/river remedies, animal-feeding remedies, service remedies are core LK modalities
- Source: Pt. Roop Chand Joshi's Lal Kitab tradition; Er. Rohit Sharma's Nishaniya series
"""
from app.astro_iogita_engine import get_planet_strength
from app.lalkitab_remedy_context import REMEDY_CONTEXT as _REMEDY_CONTEXT

# Sign → LK house (Aries=1 through Pisces=12)
_SIGN_TO_LK_HOUSE = {
    'Aries': 1, 'Taurus': 2, 'Gemini': 3, 'Cancer': 4,
    'Leo': 5, 'Virgo': 6, 'Libra': 7, 'Scorpio': 8,
    'Sagittarius': 9, 'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12,
}

# ============================================================
# REMEDIES_BY_HOUSE — planet → house → remedy dict
# 9 planets × 12 houses = 108 entries
# Each entry: {"en": str, "hi": str (Devanagari), "material": str, "day": str, "urgency": str}
# ============================================================
REMEDIES_BY_HOUSE: dict = {

    # ── SUN ──────────────────────────────────────────────────
    "Sun": {
        1: {
            "en": "Offer water to the Sun every morning at sunrise facing east; keep a solid copper piece in your pocket.",
            "hi": "प्रतिदिन सूर्योदय के समय पूर्व दिशा में मुँह करके सूर्य को जल अर्पित करें; तांबे का टुकड़ा जेब में रखें।",
            "material": "copper/water",
            "day": "Sunday",
            "urgency": "high",
        },
        2: {
            "en": "Donate wheat and jaggery to a cow on Sundays; avoid accepting free food from strangers.",
            "hi": "रविवार को गाय को गेहूँ और गुड़ खिलाएं; अजनबियों से मुफ़्त भोजन स्वीकार करने से बचें।",
            "material": "wheat/jaggery",
            "day": "Sunday",
            "urgency": "medium",
        },
        3: {
            "en": "Float a piece of copper and red cloth in flowing water on Sundays; maintain good relations with siblings.",
            "hi": "रविवार को तांबे का टुकड़ा और लाल कपड़ा बहते पानी में प्रवाहित करें; भाई-बहनों से अच्छे संबंध बनाए रखें।",
            "material": "copper/red cloth",
            "day": "Sunday",
            "urgency": "medium",
        },
        4: {
            "en": "Keep a piece of copper buried in the northeast corner of your home; offer water to a Peepal tree on Sundays.",
            "hi": "घर के उत्तर-पूर्व कोने में तांबे का टुकड़ा दबाएं; रविवार को पीपल के पेड़ को जल चढ़ाएं।",
            "material": "copper",
            "day": "Sunday",
            "urgency": "medium",
        },
        5: {
            "en": "Apply saffron tilak on forehead on Sundays; donate wheat and red lentils at a Sun temple.",
            "hi": "रविवार को माथे पर केसर का तिलक लगाएं; सूर्य मंदिर में गेहूँ और मसूर दाल दान करें।",
            "material": "saffron/wheat",
            "day": "Sunday",
            "urgency": "medium",
        },
        6: {
            "en": "Float wheat grains in flowing river water on Sundays; serve food to the poor on Sunday mornings.",
            "hi": "रविवार को गेहूँ के दाने बहती नदी में प्रवाहित करें; रविवार की सुबह गरीबों को भोजन कराएं।",
            "material": "wheat",
            "day": "Sunday",
            "urgency": "low",
        },
        7: {
            "en": "Offer sweets made with jaggery to young girls on Sundays; wear copper ring on right-hand ring finger.",
            "hi": "रविवार को कन्याओं को गुड़ से बने मिठाई का भोग लगाएं; दाएं हाथ की अनामिका में तांबे की अंगूठी पहनें।",
            "material": "copper/jaggery sweets",
            "day": "Sunday",
            "urgency": "high",
        },
        8: {
            "en": "Donate copper vessel filled with water at a Shiva temple on Sundays; avoid ego and arrogance.",
            "hi": "रविवार को शिव मंदिर में पानी भरे तांबे के बर्तन का दान करें; अहंकार और घमंड से दूर रहें।",
            "material": "copper vessel/water",
            "day": "Sunday",
            "urgency": "high",
        },
        9: {
            "en": "Offer water at sunrise daily; donate wheat and sesame to Brahmins on Sundays; respect your father.",
            "hi": "प्रतिदिन सूर्योदय पर जल अर्पण करें; रविवार को ब्राह्मणों को गेहूँ और तिल दान करें; पिता का सम्मान करें।",
            "material": "wheat/sesame",
            "day": "Sunday",
            "urgency": "medium",
        },
        10: {
            "en": "Keep a copper coin in your wallet at all times; do not insult authority or government figures.",
            "hi": "हमेशा बटुए में तांबे का सिक्का रखें; सरकारी अधिकारियों या बड़ों का अपमान न करें।",
            "material": "copper coin",
            "day": "Sunday",
            "urgency": "medium",
        },
        11: {
            "en": "Float a copper coin in flowing water on Sundays; donate wheat flour to a temple on Sundays.",
            "hi": "रविवार को तांबे का सिक्का बहते पानी में प्रवाहित करें; रविवार को मंदिर में गेहूँ का आटा दान करें।",
            "material": "copper/wheat flour",
            "day": "Sunday",
            "urgency": "low",
        },
        12: {
            "en": "Donate copper and wheat to a hospital or shelter on Sundays; meditate at sunrise facing east.",
            "hi": "रविवार को अस्पताल या आश्रम में तांबा और गेहूँ दान करें; सूर्योदय पर पूर्व दिशा में ध्यान करें।",
            "material": "copper/wheat",
            "day": "Sunday",
            "urgency": "low",
        },
    },

    # ── MOON ─────────────────────────────────────────────────
    "Moon": {
        1: {
            "en": "Drink water from a silver glass daily; keep a square piece of silver with you.",
            "hi": "प्रतिदिन चांदी के गिलास में पानी पिएं; चांदी का चौकोर टुकड़ा अपने पास रखें।",
            "material": "silver",
            "day": "Monday",
            "urgency": "high",
        },
        2: {
            "en": "Donate white rice, milk, and silver items on Mondays; keep fresh water at home always.",
            "hi": "सोमवार को सफेद चावल, दूध और चांदी की वस्तुएं दान करें; घर में ताजा पानी हमेशा रखें।",
            "material": "silver/white rice/milk",
            "day": "Monday",
            "urgency": "medium",
        },
        3: {
            "en": "Float silver coin in flowing water on Mondays; wear white or cream-colored clothes on Mondays.",
            "hi": "सोमवार को बहते पानी में चांदी का सिक्का प्रवाहित करें; सोमवार को सफेद या क्रीम रंग के वस्त्र पहनें।",
            "material": "silver coin",
            "day": "Monday",
            "urgency": "medium",
        },
        4: {
            "en": "Keep fresh water by your bedside at night and pour it into a plant in the morning; honor your mother.",
            "hi": "रात को पलंग के पास ताजा पानी रखें और सुबह पौधे में डालें; माता का सम्मान करें।",
            "material": "water",
            "day": "Monday",
            "urgency": "high",
        },
        5: {
            "en": "Offer milk and white sweets at a Shiva temple on Mondays; give milk to children.",
            "hi": "सोमवार को शिव मंदिर में दूध और सफेद मिठाई चढ़ाएं; बच्चों को दूध पिलाएं।",
            "material": "milk/white sweets",
            "day": "Monday",
            "urgency": "medium",
        },
        6: {
            "en": "Feed dogs white rice and milk on Mondays; avoid starting milk-related business.",
            "hi": "सोमवार को कुत्तों को सफेद चावल और दूध खिलाएं; दूध से संबंधित व्यवसाय शुरू करने से बचें।",
            "material": "white rice/milk",
            "day": "Monday",
            "urgency": "low",
        },
        7: {
            "en": "Donate silver items to your wife or partner; offer milk and white flowers at a Devi temple on Mondays.",
            "hi": "पत्नी या साथी को चांदी की वस्तुएं भेंट करें; सोमवार को देवी मंदिर में दूध और सफेद फूल चढ़ाएं।",
            "material": "silver/white flowers/milk",
            "day": "Monday",
            "urgency": "high",
        },
        8: {
            "en": "Float a silver coin in river water on Mondays; avoid confrontations with female relatives.",
            "hi": "सोमवार को नदी में चांदी का सिक्का प्रवाहित करें; महिला रिश्तेदारों से टकराव से बचें।",
            "material": "silver coin/river water",
            "day": "Monday",
            "urgency": "medium",
        },
        9: {
            "en": "Donate white cloth and rice at a temple on Mondays; keep relationship with maternal family positive.",
            "hi": "सोमवार को मंदिर में सफेद कपड़ा और चावल दान करें; मातृपक्ष के साथ संबंध अच्छे रखें।",
            "material": "white cloth/rice",
            "day": "Monday",
            "urgency": "medium",
        },
        10: {
            "en": "Keep a silver coin in your pocket during work hours; do not disrespect women or your mother.",
            "hi": "काम के समय जेब में चांदी का सिक्का रखें; महिलाओं और माता का अपमान न करें।",
            "material": "silver coin",
            "day": "Monday",
            "urgency": "medium",
        },
        11: {
            "en": "Donate white items (rice, sugar, cloth) to elderly women on Mondays; drink milk before sleep.",
            "hi": "सोमवार को बुजुर्ग महिलाओं को सफेद वस्तुएं (चावल, चीनी, कपड़ा) दान करें; सोने से पहले दूध पिएं।",
            "material": "white rice/sugar/cloth",
            "day": "Monday",
            "urgency": "low",
        },
        12: {
            "en": "Keep a filled silver vessel at your place of worship; donate milk to a cow shelter on Mondays.",
            "hi": "पूजा स्थान पर चांदी का भरा हुआ पात्र रखें; सोमवार को गौशाला में दूध दान करें।",
            "material": "silver vessel/milk",
            "day": "Monday",
            "urgency": "low",
        },
    },

    # ── MARS ─────────────────────────────────────────────────
    "Mars": {
        1: {
            "en": "Apply saffron tilak on forehead daily; donate red lentils (masoor dal) on Tuesdays.",
            "hi": "प्रतिदिन माथे पर केसर का तिलक लगाएं; मंगलवार को मसूर दाल दान करें।",
            "material": "saffron/red lentils",
            "day": "Tuesday",
            "urgency": "high",
        },
        2: {
            "en": "Donate red masoor dal and red cloth on Tuesdays; feed jaggery to cows.",
            "hi": "मंगलवार को मसूर दाल और लाल कपड़ा दान करें; गायों को गुड़ खिलाएं।",
            "material": "red lentils/red cloth/jaggery",
            "day": "Tuesday",
            "urgency": "medium",
        },
        3: {
            "en": "Maintain sweet relationships with younger siblings; float red masoor dal in flowing water on Tuesdays.",
            "hi": "छोटे भाई-बहनों के साथ मधुर संबंध रखें; मंगलवार को बहते पानी में मसूर दाल प्रवाहित करें।",
            "material": "red lentils",
            "day": "Tuesday",
            "urgency": "medium",
        },
        4: {
            "en": "Fix all water leaks and broken walls in the home immediately; donate bricks or construction materials.",
            "hi": "घर में सभी पानी के रिसाव और टूटी दीवारों की तुरंत मरम्मत करें; ईंट या निर्माण सामग्री दान करें।",
            "material": "iron/bricks",
            "day": "Tuesday",
            "urgency": "high",
        },
        5: {
            "en": "Feed sweet bread (chapati with jaggery) to dogs on Tuesdays; offer red flowers at Hanuman temple.",
            "hi": "मंगलवार को कुत्तों को गुड़ वाली रोटी खिलाएं; हनुमान मंदिर में लाल फूल चढ़ाएं।",
            "material": "chapati/jaggery",
            "day": "Tuesday",
            "urgency": "medium",
        },
        6: {
            "en": "Donate blood when possible; feed red lentil bread to cows on Tuesdays.",
            "hi": "जब संभव हो रक्तदान करें; मंगलवार को गायों को मसूर की रोटी खिलाएं।",
            "material": "red lentils",
            "day": "Tuesday",
            "urgency": "low",
        },
        7: {
            "en": "Offer sweet red halwa to married women on Tuesdays; donate copper pot at a temple.",
            "hi": "मंगलवार को विवाहित महिलाओं को मीठा लाल हलवा भेंट करें; मंदिर में तांबे का बर्तन दान करें।",
            "material": "copper/sweet halwa",
            "day": "Tuesday",
            "urgency": "high",
        },
        8: {
            "en": "Cook bread on an iron griddle (tawa) and feed it to crows; avoid widows in harmful contexts.",
            "hi": "लोहे की तवे पर रोटी बनाकर कौवों को खिलाएं; विधवाओं का शोषण न करें।",
            "material": "iron tawa/bread",
            "day": "Tuesday",
            "urgency": "high",
        },
        9: {
            "en": "Visit a Hanuman temple on Tuesdays and donate red cloth; maintain good relations with younger brothers.",
            "hi": "मंगलवार को हनुमान मंदिर जाएं और लाल कपड़ा दान करें; छोटे भाइयों से अच्छे संबंध बनाए रखें।",
            "material": "red cloth",
            "day": "Tuesday",
            "urgency": "medium",
        },
        10: {
            "en": "Do not accept gifts of land or property from others freely; donate iron tools to laborers on Tuesdays.",
            "hi": "दूसरों से भूमि या संपत्ति मुफ़्त में स्वीकार न करें; मंगलवार को मजदूरों को लोहे के औज़ार दान करें।",
            "material": "iron tools",
            "day": "Tuesday",
            "urgency": "medium",
        },
        11: {
            "en": "Feed red lentil halwa to dogs on Tuesdays; donate to fire-service or military charities.",
            "hi": "मंगलवार को कुत्तों को मसूर दाल का हलवा खिलाएं; अग्नि-सेवा या सैन्य दान संस्थाओं में दान करें।",
            "material": "red lentils",
            "day": "Tuesday",
            "urgency": "low",
        },
        12: {
            "en": "Donate red masoor dal and copper vessel at a hospital on Tuesdays; practice silent prayer at night.",
            "hi": "मंगलवार को अस्पताल में मसूर दाल और तांबे का बर्तन दान करें; रात को मौन प्रार्थना करें।",
            "material": "red lentils/copper",
            "day": "Tuesday",
            "urgency": "low",
        },
    },

    # ── MERCURY ──────────────────────────────────────────────
    "Mercury": {
        1: {
            "en": "Donate green moong dal and green vegetables on Wednesdays; keep a small piece of copper with a hole.",
            "hi": "बुधवार को हरी मूंग दाल और हरी सब्जियाँ दान करें; बीच में छेद वाला तांबे का छोटा टुकड़ा रखें।",
            "material": "copper/green moong",
            "day": "Wednesday",
            "urgency": "medium",
        },
        2: {
            "en": "Feed green grass to cows on Wednesdays; maintain good relations with sisters and daughters.",
            "hi": "बुधवार को गायों को हरी घास खिलाएं; बहनों और बेटियों के साथ अच्छे संबंध रखें।",
            "material": "green grass",
            "day": "Wednesday",
            "urgency": "medium",
        },
        3: {
            "en": "Fill an earthen pot with honey and bury it in a secluded place; float green items in flowing water.",
            "hi": "शहद से भरा मिट्टी का बर्तन एकांत स्थान पर दबाएं; बहते पानी में हरी चीज़ें प्रवाहित करें।",
            "material": "honey/earthen pot",
            "day": "Wednesday",
            "urgency": "medium",
        },
        4: {
            "en": "Plant green plants in the home; donate green moong and green cloth to young girls on Wednesdays.",
            "hi": "घर में हरे पौधे लगाएं; बुधवार को कन्याओं को हरी मूंग और हरा कपड़ा दान करें।",
            "material": "green moong/green cloth",
            "day": "Wednesday",
            "urgency": "medium",
        },
        5: {
            "en": "Wear green colored clothes on Wednesdays; donate Emerald-colored items at a Ganesha temple.",
            "hi": "बुधवार को हरे रंग के कपड़े पहनें; गणेश मंदिर में हरे रंग की वस्तुएं दान करें।",
            "material": "green cloth",
            "day": "Wednesday",
            "urgency": "medium",
        },
        6: {
            "en": "Feed green fodder to cows; donate green vegetables at a temple on Wednesdays.",
            "hi": "गायों को हरा चारा खिलाएं; बुधवार को मंदिर में हरी सब्जियाँ दान करें।",
            "material": "green vegetables",
            "day": "Wednesday",
            "urgency": "low",
        },
        7: {
            "en": "Donate green moong and fennel seeds to young women on Wednesdays; keep fennel seeds under your pillow.",
            "hi": "बुधवार को युवतियों को हरी मूंग और सौंफ दान करें; तकिए के नीचे सौंफ रखें।",
            "material": "green moong/fennel",
            "day": "Wednesday",
            "urgency": "high",
        },
        8: {
            "en": "Bury green moong in a green cloth at a river bank on Wednesdays; avoid deception and fraud.",
            "hi": "बुधवार को नदी के किनारे हरे कपड़े में हरी मूंग दबाएं; धोखे और जालसाजी से बचें।",
            "material": "green moong/green cloth",
            "day": "Wednesday",
            "urgency": "high",
        },
        9: {
            "en": "Donate books and stationery to students on Wednesdays; respect teachers and scholars.",
            "hi": "बुधवार को छात्रों को किताबें और स्टेशनरी दान करें; शिक्षकों और विद्वानों का सम्मान करें।",
            "material": "books/stationery",
            "day": "Wednesday",
            "urgency": "medium",
        },
        10: {
            "en": "Keep a piece of copper in the workplace; donate green vegetables to a charitable kitchen on Wednesdays.",
            "hi": "कार्यस्थल पर तांबे का टुकड़ा रखें; बुधवार को सामुदायिक रसोई में हरी सब्जियाँ दान करें।",
            "material": "copper/green vegetables",
            "day": "Wednesday",
            "urgency": "medium",
        },
        11: {
            "en": "Feed parrots or green birds on Wednesdays; donate green moong at a Ganesha temple.",
            "hi": "बुधवार को तोते या हरे पक्षियों को चारा दें; गणेश मंदिर में हरी मूंग दान करें।",
            "material": "green moong",
            "day": "Wednesday",
            "urgency": "low",
        },
        12: {
            "en": "Sleep with fennel seeds under your pillow; donate green cloth to a hospital on Wednesdays.",
            "hi": "तकिए के नीचे सौंफ रखकर सोएं; बुधवार को अस्पताल में हरा कपड़ा दान करें।",
            "material": "fennel/green cloth",
            "day": "Wednesday",
            "urgency": "low",
        },
    },

    # ── JUPITER ──────────────────────────────────────────────
    "Jupiter": {
        1: {
            "en": "Apply saffron or turmeric tilak on forehead and navel daily; donate yellow items on Thursdays.",
            "hi": "प्रतिदिन माथे और नाभि पर केसर या हल्दी का तिलक लगाएं; गुरुवार को पीले रंग की वस्तुएं दान करें।",
            "material": "saffron/turmeric",
            "day": "Thursday",
            "urgency": "medium",
        },
        2: {
            "en": "Donate yellow chana dal and turmeric to Brahmins on Thursdays; water a banana tree every Thursday.",
            "hi": "गुरुवार को ब्राह्मणों को पीली चना दाल और हल्दी दान करें; प्रत्येक गुरुवार को केले के पेड़ को जल दें।",
            "material": "yellow chana/turmeric",
            "day": "Thursday",
            "urgency": "medium",
        },
        3: {
            "en": "Feed yellow sweets to Brahmins on Thursdays; keep a square piece of gold or brass with you.",
            "hi": "गुरुवार को ब्राह्मणों को पीली मिठाई खिलाएं; सोने या पीतल का चौकोर टुकड़ा अपने पास रखें।",
            "material": "gold/brass",
            "day": "Thursday",
            "urgency": "medium",
        },
        4: {
            "en": "Keep turmeric in the northeast corner of the home; serve food to Brahmins and elders on Thursdays.",
            "hi": "घर के उत्तर-पूर्व कोने में हल्दी रखें; गुरुवार को ब्राह्मणों और बुजुर्गों को भोजन कराएं।",
            "material": "turmeric",
            "day": "Thursday",
            "urgency": "medium",
        },
        5: {
            "en": "Donate yellow cloth and banana to a temple on Thursdays; teach or share knowledge freely.",
            "hi": "गुरुवार को मंदिर में पीला कपड़ा और केला दान करें; ज्ञान स्वतंत्र रूप से बाँटें।",
            "material": "yellow cloth/banana",
            "day": "Thursday",
            "urgency": "medium",
        },
        6: {
            "en": "Feed cows banana and chickpeas on Thursdays; donate yellow items to a cow shelter.",
            "hi": "गुरुवार को गायों को केला और चना खिलाएं; गौशाला में पीले रंग की वस्तुएं दान करें।",
            "material": "banana/chickpeas",
            "day": "Thursday",
            "urgency": "low",
        },
        7: {
            "en": "Respect your spouse and treat them with honor; donate yellow sweets to young girls on Thursdays.",
            "hi": "जीवनसाथी का सम्मान करें और उनके साथ आदर से व्यवहार करें; गुरुवार को कन्याओं को पीली मिठाई दें।",
            "material": "yellow sweets",
            "day": "Thursday",
            "urgency": "high",
        },
        8: {
            "en": "Donate yellow cloth and turmeric at a temple on Thursdays; avoid taking loans recklessly.",
            "hi": "गुरुवार को मंदिर में पीला कपड़ा और हल्दी दान करें; लापरवाही से कर्ज लेने से बचें।",
            "material": "yellow cloth/turmeric",
            "day": "Thursday",
            "urgency": "high",
        },
        9: {
            "en": "Serve and respect your guru and elders; donate yellow items and books at a temple on Thursdays.",
            "hi": "गुरु और बड़ों की सेवा और सम्मान करें; गुरुवार को मंदिर में पीले रंग की वस्तुएं और पुस्तकें दान करें।",
            "material": "yellow cloth/books",
            "day": "Thursday",
            "urgency": "medium",
        },
        10: {
            "en": "Bow to elders and authorities with respect; donate yellow lentils at a temple on Thursdays.",
            "hi": "बड़ों और अधिकारियों को सम्मान से प्रणाम करें; गुरुवार को मंदिर में पीली दाल दान करें।",
            "material": "yellow lentils",
            "day": "Thursday",
            "urgency": "medium",
        },
        11: {
            "en": "Donate turmeric and chickpeas to friends and social networks on Thursdays.",
            "hi": "गुरुवार को मित्रों और सामाजिक संपर्कों को हल्दी और चना दान करें।",
            "material": "turmeric/chickpeas",
            "day": "Thursday",
            "urgency": "low",
        },
        12: {
            "en": "Donate yellow cloth to temples or ashrams on Thursdays; meditate and chant Jupiter mantras.",
            "hi": "गुरुवार को मंदिरों या आश्रमों में पीला कपड़ा दान करें; गुरु मंत्रों का ध्यान और जप करें।",
            "material": "yellow cloth",
            "day": "Thursday",
            "urgency": "low",
        },
    },

    # ── VENUS ────────────────────────────────────────────────
    "Venus": {
        1: {
            "en": "Offer white flowers at a Devi temple on Fridays; keep a square piece of silver at home.",
            "hi": "शुक्रवार को देवी मंदिर में सफेद फूल चढ़ाएं; घर में चांदी का चौकोर टुकड़ा रखें।",
            "material": "silver/white flowers",
            "day": "Friday",
            "urgency": "medium",
        },
        2: {
            "en": "Donate white rice and ghee on Fridays; use perfume or fragrance regularly.",
            "hi": "शुक्रवार को सफेद चावल और घी दान करें; नियमित रूप से इत्र या सुगंध का उपयोग करें।",
            "material": "white rice/ghee",
            "day": "Friday",
            "urgency": "medium",
        },
        3: {
            "en": "Donate silk or white cloth to young women on Fridays; maintain beautiful and clean surroundings.",
            "hi": "शुक्रवार को युवतियों को रेशम या सफेद कपड़ा दान करें; सुंदर और स्वच्छ वातावरण बनाए रखें।",
            "material": "silk/white cloth",
            "day": "Friday",
            "urgency": "medium",
        },
        4: {
            "en": "Keep home spotlessly clean; feed white sweets to cows on Fridays; plant flowers at home.",
            "hi": "घर को बिल्कुल साफ रखें; शुक्रवार को गायों को सफेद मिठाई खिलाएं; घर में फूल लगाएं।",
            "material": "white sweets",
            "day": "Friday",
            "urgency": "medium",
        },
        5: {
            "en": "Offer white sweets and white flowers at a Lakshmi temple on Fridays; wear white on Fridays.",
            "hi": "शुक्रवार को लक्ष्मी मंदिर में सफेद मिठाई और सफेद फूल चढ़ाएं; शुक्रवार को सफेद वस्त्र पहनें।",
            "material": "white sweets/white flowers",
            "day": "Friday",
            "urgency": "medium",
        },
        6: {
            "en": "Feed white cows milk and rice on Fridays; donate white cloth to women in need.",
            "hi": "शुक्रवार को सफेद गायों को दूध और चावल खिलाएं; जरूरतमंद महिलाओं को सफेद कपड़ा दान करें।",
            "material": "white cloth/milk/rice",
            "day": "Friday",
            "urgency": "low",
        },
        7: {
            "en": "Offer white flowers and incense at a Devi temple on Fridays; be kind and gentle with your spouse.",
            "hi": "शुक्रवार को देवी मंदिर में सफेद फूल और अगरबत्ती चढ़ाएं; जीवनसाथी के साथ दयालु और कोमल रहें।",
            "material": "white flowers/incense",
            "day": "Friday",
            "urgency": "high",
        },
        8: {
            "en": "Donate white items and perfume to married women on Fridays; avoid vanity and excess.",
            "hi": "शुक्रवार को विवाहित महिलाओं को सफेद वस्तुएं और इत्र दान करें; घमंड और अति से बचें।",
            "material": "white items/perfume",
            "day": "Friday",
            "urgency": "high",
        },
        9: {
            "en": "Offer white flowers at a Devi temple and pray for blessings on Fridays; donate to women's education.",
            "hi": "शुक्रवार को देवी मंदिर में सफेद फूल चढ़ाएं और आशीर्वाद के लिए प्रार्थना करें; महिला शिक्षा में दान करें।",
            "material": "white flowers",
            "day": "Friday",
            "urgency": "medium",
        },
        10: {
            "en": "Keep workplace aesthetically pleasant; donate white cloth to a women's organization on Fridays.",
            "hi": "कार्यस्थल को सौंदर्यपूर्ण रखें; शुक्रवार को महिला संगठन को सफेद कपड़ा दान करें।",
            "material": "white cloth",
            "day": "Friday",
            "urgency": "medium",
        },
        11: {
            "en": "Gift white flowers or sweets to female friends on Fridays; maintain harmony in social circles.",
            "hi": "शुक्रवार को महिला मित्रों को सफेद फूल या मिठाई भेंट करें; सामाजिक दायरे में सामंजस्य बनाए रखें।",
            "material": "white flowers/sweets",
            "day": "Friday",
            "urgency": "low",
        },
        12: {
            "en": "Donate white cloth and sweets to a shelter for women on Fridays; avoid illicit relationships.",
            "hi": "शुक्रवार को महिला आश्रम में सफेद कपड़ा और मिठाई दान करें; अवैध संबंधों से बचें।",
            "material": "white cloth/sweets",
            "day": "Friday",
            "urgency": "medium",
        },
    },

    # ── SATURN ───────────────────────────────────────────────
    "Saturn": {
        1: {
            "en": "Feed crows with cooked rice mixed with sesame oil on Saturdays; donate black sesame seeds and mustard oil.",
            "hi": "शनिवार को तिल के तेल में पकाए चावल कौवों को खिलाएं; काले तिल और सरसों का तेल दान करें।",
            "material": "black sesame/mustard oil",
            "day": "Saturday",
            "urgency": "high",
        },
        2: {
            "en": "Donate black sesame, iron, and black blanket to the needy on Saturdays; serve the poor and elderly.",
            "hi": "शनिवार को जरूरतमंदों को काला तिल, लोहा और काला कंबल दान करें; गरीबों और बुजुर्गों की सेवा करें।",
            "material": "black sesame/iron/black blanket",
            "day": "Saturday",
            "urgency": "medium",
        },
        3: {
            "en": "Pour mustard oil in a drainage channel on Saturdays; fix all broken pipes or drains at home.",
            "hi": "शनिवार को नाली में सरसों का तेल डालें; घर में सभी टूटे पाइप या नालियाँ ठीक करवाएं।",
            "material": "mustard oil",
            "day": "Saturday",
            "urgency": "medium",
        },
        4: {
            "en": "Repair all broken drains and leaking roofs immediately; donate iron items to laborers on Saturdays.",
            "hi": "सभी टूटी नालियाँ और छत की टपकन तुरंत ठीक करवाएं; शनिवार को मजदूरों को लोहे की चीजें दान करें।",
            "material": "iron",
            "day": "Saturday",
            "urgency": "high",
        },
        5: {
            "en": "Avoid alcohol completely on Saturdays; donate black sesame and iron at a Shani temple.",
            "hi": "शनिवार को पूरी तरह से शराब से बचें; शनि मंदिर में काला तिल और लोहा दान करें।",
            "material": "black sesame/iron",
            "day": "Saturday",
            "urgency": "medium",
        },
        6: {
            "en": "Feed crows and feed stray dogs on Saturdays; donate leather shoes or blankets to the needy.",
            "hi": "शनिवार को कौवों को और आवारा कुत्तों को खाना खिलाएं; जरूरतमंदों को चमड़े के जूते या कंबल दान करें।",
            "material": "leather shoes/blankets",
            "day": "Saturday",
            "urgency": "low",
        },
        7: {
            "en": "Pour mustard oil on a piece of iron and donate both on Saturdays; respect all workers and laborers.",
            "hi": "शनिवार को लोहे के टुकड़े पर सरसों का तेल डालकर दोनों दान करें; सभी कामगारों और मजदूरों का सम्मान करें।",
            "material": "iron/mustard oil",
            "day": "Saturday",
            "urgency": "high",
        },
        8: {
            "en": "Keep a square piece of iron under your pillow; donate black sesame and oil to a Shani temple on Saturdays.",
            "hi": "तकिए के नीचे चौकोर लोहे का टुकड़ा रखें; शनिवार को शनि मंदिर में काला तिल और तेल दान करें।",
            "material": "iron/black sesame/oil",
            "day": "Saturday",
            "urgency": "high",
        },
        9: {
            "en": "Serve the disabled and destitute on Saturdays; donate black sesame and blanket to a religious place.",
            "hi": "शनिवार को विकलांगों और बेसहारा लोगों की सेवा करें; धार्मिक स्थान पर काला तिल और कंबल दान करें।",
            "material": "black sesame/blanket",
            "day": "Saturday",
            "urgency": "medium",
        },
        10: {
            "en": "Never disrespect laborers or servants; donate iron items and black cloth on Saturdays.",
            "hi": "मजदूरों या नौकरों का कभी अपमान न करें; शनिवार को लोहे की चीजें और काला कपड़ा दान करें।",
            "material": "iron/black cloth",
            "day": "Saturday",
            "urgency": "medium",
        },
        11: {
            "en": "Donate black items to elderly persons on Saturdays; avoid exploitation of workers.",
            "hi": "शनिवार को बुजुर्गों को काली वस्तुएं दान करें; मजदूरों का शोषण करने से बचें।",
            "material": "black cloth/sesame",
            "day": "Saturday",
            "urgency": "low",
        },
        12: {
            "en": "Donate black blanket and oil at a temple on Saturdays; meditate silently and serve the sick.",
            "hi": "शनिवार को मंदिर में काला कंबल और तेल दान करें; मौन ध्यान करें और बीमारों की सेवा करें।",
            "material": "black blanket/oil",
            "day": "Saturday",
            "urgency": "medium",
        },
    },

    # ── RAHU ─────────────────────────────────────────────────
    "Rahu": {
        1: {
            # Standard Rahu-in-H1 LK remedy. Do NOT recommend SW water
            # storage here — that contradicts the Vastu engine, which
            # correctly flags SW as Saturn's dry zone.
            "en": "Keep a solid silver square piece with you at all times "
                  "(in pocket or wallet); keep fennel seeds (saunf) "
                  "handy and avoid blue/black clothing near the face.",
            "hi": "हमेशा अपने पास एक ठोस चांदी का चौकोर टुकड़ा रखें "
                  "(जेब या पर्स में); सौंफ साथ रखें और नीले/काले "
                  "कपड़े चेहरे के पास पहनने से बचें।",
            "material": "silver square/fennel",
            "day": "Saturday",
            "urgency": "high",
        },
        2: {
            "en": "Donate radishes and coconut at a temple on Saturdays; keep fennel seeds under your pillow.",
            "hi": "शनिवार को मंदिर में मूली और नारियल दान करें; तकिए के नीचे सौंफ रखें।",
            "material": "radishes/coconut/fennel",
            "day": "Saturday",
            "urgency": "medium",
        },
        3: {
            "en": "Float coconut in flowing water on Saturdays; feed birds daily especially crows.",
            "hi": "शनिवार को बहते पानी में नारियल प्रवाहित करें; प्रतिदिन पक्षियों को, विशेषकर कौवों को दाना डालें।",
            "material": "coconut",
            "day": "Saturday",
            "urgency": "medium",
        },
        4: {
            "en": "Keep a piece of silver buried in the home; donate radishes and fennel to neighbors on Saturdays.",
            "hi": "घर में चांदी का टुकड़ा दबाकर रखें; शनिवार को पड़ोसियों को मूली और सौंफ दान करें।",
            "material": "silver/radishes/fennel",
            "day": "Saturday",
            "urgency": "medium",
        },
        5: {
            "en": "Donate black and white sesame seeds on Saturdays; avoid speculation and gambling.",
            "hi": "शनिवार को काले और सफेद तिल दान करें; सट्टेबाजी और जुए से बचें।",
            "material": "black and white sesame",
            "day": "Saturday",
            "urgency": "high",
        },
        6: {
            "en": "Feed birds and crows daily; donate radishes at a Shani or Durga temple on Saturdays.",
            "hi": "प्रतिदिन पक्षियों और कौवों को दाना डालें; शनिवार को शनि या दुर्गा मंदिर में मूली दान करें।",
            "material": "radishes",
            "day": "Saturday",
            "urgency": "low",
        },
        7: {
            "en": "Donate coconut and fennel at a temple on Saturdays; avoid partnerships that involve deception.",
            "hi": "शनिवार को मंदिर में नारियल और सौंफ दान करें; धोखे वाली साझेदारी से बचें।",
            "material": "coconut/fennel",
            "day": "Saturday",
            "urgency": "high",
        },
        8: {
            "en": "Float coconut and black sesame in flowing water on Saturdays; avoid sudden risky decisions.",
            "hi": "शनिवार को बहते पानी में नारियल और काला तिल प्रवाहित करें; अचानक जोखिम भरे निर्णयों से बचें।",
            "material": "coconut/black sesame",
            "day": "Saturday",
            "urgency": "high",
        },
        9: {
            "en": "Donate radishes and coconut at a religious place on Saturdays; avoid blind beliefs and superstitions.",
            "hi": "शनिवार को धार्मिक स्थान पर मूली और नारियल दान करें; अंधविश्वास और ढोंग से बचें।",
            "material": "radishes/coconut",
            "day": "Saturday",
            "urgency": "medium",
        },
        10: {
            "en": "Keep silver in your workplace; donate fennel seeds to the elderly on Saturdays.",
            "hi": "कार्यस्थल पर चांदी रखें; शनिवार को बुजुर्गों को सौंफ दान करें।",
            "material": "silver/fennel",
            "day": "Saturday",
            "urgency": "medium",
        },
        11: {
            "en": "Donate black and white sesame to social organizations on Saturdays; be honest in all dealings.",
            "hi": "शनिवार को सामाजिक संगठनों को काले और सफेद तिल दान करें; सभी लेन-देन में ईमानदार रहें।",
            "material": "black and white sesame",
            "day": "Saturday",
            "urgency": "low",
        },
        12: {
            "en": "Keep fennel seeds under your pillow while sleeping; donate coconut at a temple on Saturdays.",
            "hi": "सोते समय तकिए के नीचे सौंफ रखें; शनिवार को मंदिर में नारियल दान करें।",
            "material": "fennel/coconut",
            "day": "Saturday",
            "urgency": "low",
        },
    },

    # ── KETU ─────────────────────────────────────────────────
    "Ketu": {
        1: {
            "en": "Feed stray dogs regularly; keep saffron at your place of worship; apply saffron tilak daily.",
            "hi": "नियमित रूप से आवारा कुत्तों को भोजन दें; पूजा स्थान पर केसर रखें; प्रतिदिन केसर का तिलक लगाएं।",
            "material": "saffron",
            "day": "Tuesday",
            "urgency": "high",
        },
        2: {
            "en": "Donate a black and white blanket to a temple; keep a silver ball in your pocket.",
            "hi": "मंदिर को काला-सफेद कंबल दान करें; जेब में चांदी की गोली रखें।",
            "material": "silver/black-white blanket",
            "day": "Tuesday",
            "urgency": "medium",
        },
        3: {
            "en": "Donate sesame seeds and blankets on Tuesdays; maintain good relations with your maternal grandfather.",
            "hi": "मंगलवार को तिल और कंबल दान करें; नाना के साथ अच्छे संबंध बनाए रखें।",
            "material": "sesame/blanket",
            "day": "Tuesday",
            "urgency": "medium",
        },
        4: {
            "en": "Keep a dog as pet or feed neighborhood dogs; keep saffron thread tied at home entrance.",
            "hi": "कुत्ता पालें या मोहल्ले के कुत्तों को खाना खिलाएं; घर के प्रवेश द्वार पर केसर का धागा बांधें।",
            "material": "saffron/dog food",
            "day": "Tuesday",
            "urgency": "medium",
        },
        5: {
            "en": "Donate blanket and saffron at a Ganesh temple on Tuesdays; avoid excessive attachment to children.",
            "hi": "मंगलवार को गणेश मंदिर में कंबल और केसर दान करें; बच्चों के प्रति अत्यधिक मोह से बचें।",
            "material": "saffron/blanket",
            "day": "Tuesday",
            "urgency": "medium",
        },
        6: {
            "en": "Feed stray dogs rice and bread daily; donate to a dog shelter; keep surroundings clean.",
            "hi": "प्रतिदिन आवारा कुत्तों को चावल और रोटी खिलाएं; कुत्ते की देखभाल संस्था में दान करें; परिवेश स्वच्छ रखें।",
            "material": "rice/bread",
            "day": "Tuesday",
            "urgency": "low",
        },
        7: {
            "en": "Donate saffron and silver to a temple on Tuesdays; avoid spiritual pride in marriage.",
            "hi": "मंगलवार को मंदिर में केसर और चांदी दान करें; विवाह में आध्यात्मिक अहंकार से बचें।",
            "material": "saffron/silver",
            "day": "Tuesday",
            "urgency": "high",
        },
        8: {
            "en": "Donate black blanket and saffron to a temple on Tuesdays; respect ancestors and do not disturb burial sites.",
            "hi": "मंगलवार को मंदिर में काला कंबल और केसर दान करें; पूर्वजों का सम्मान करें और कब्रिस्तान को न छेड़ें।",
            "material": "saffron/black blanket",
            "day": "Tuesday",
            "urgency": "high",
        },
        9: {
            "en": "Visit pilgrimage places and donate saffron; keep a silver ball in pocket during travel.",
            "hi": "तीर्थस्थलों पर जाएं और केसर दान करें; यात्रा के दौरान जेब में चांदी की गोली रखें।",
            "material": "saffron/silver",
            "day": "Tuesday",
            "urgency": "medium",
        },
        10: {
            "en": "Apply saffron tilak before starting work; donate blankets to the homeless on Tuesdays.",
            "hi": "काम शुरू करने से पहले केसर का तिलक लगाएं; मंगलवार को बेघर लोगों को कंबल दान करें।",
            "material": "saffron/blankets",
            "day": "Tuesday",
            "urgency": "medium",
        },
        11: {
            "en": "Donate sesame and saffron to social organizations on Tuesdays; feed dogs in your neighborhood.",
            "hi": "मंगलवार को सामाजिक संगठनों को तिल और केसर दान करें; अपने मोहल्ले के कुत्तों को खाना खिलाएं।",
            "material": "sesame/saffron",
            "day": "Tuesday",
            "urgency": "low",
        },
        12: {
            "en": "Sleep with saffron tied in a small cloth near head; donate black blanket and sesame at a temple.",
            "hi": "सोते समय सिर के पास छोटे कपड़े में बंधा केसर रखें; मंदिर में काला कंबल और तिल दान करें।",
            "material": "saffron/black blanket/sesame",
            "day": "Tuesday",
            "urgency": "low",
        },
    },
}

# ============================================================
# REMEDIES — kept for backward compatibility (old tests import REMEDIES)
# Maps planet → list of generic remedy strings
# ============================================================
REMEDIES = {
    planet: [houses[h]["en"] for h in sorted(houses.keys())[:8]]
    for planet, houses in REMEDIES_BY_HOUSE.items()
}

# Dignity labels for display
DIGNITY_LABELS = {
    "Exalted": "exalted",
    "Own Sign": "in own sign",
    "Friendly": "in friendly sign",
    "Neutral": "in neutral sign",
    "Enemy": "in enemy sign",
    "Debilitated": "debilitated",
}


def _get_dignity_label(planet: str, sign: str) -> str:
    """Determine dignity label for a planet in a sign.

    NOTE: This is a simplified model based on SIGN ONLY.
    For full affliction analysis including house/combustion/retrograde/nakshatra,
    use `get_planet_strength_detailed()` instead.
    """
    from app.astro_iogita_engine import EXALTED, DEBILITATED, OWN_SIGNS, FRIEND_SIGNS, ENEMY_SIGNS

    if sign == EXALTED.get(planet):
        return "Exalted"
    if sign == DEBILITATED.get(planet):
        return "Debilitated"
    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"
    if sign in FRIEND_SIGNS.get(planet, []):
        return "Friendly"
    if sign in ENEMY_SIGNS.get(planet, []):
        return "Enemy"
    return "Neutral"


def get_planet_strength_detailed(
    planet: str,
    sign: str,
    house: "int | None" = None,
    is_retrograde: bool = False,
    is_combust: bool = False,
    nakshatra: "str | None" = None,
) -> dict:
    """
    Enriched Lal Kitab strength model — accounts for dignity, house,
    retrograde, combustion, and nakshatra.

    Unlike the sign-only `get_planet_strength()` (imported from
    `astro_iogita_engine`), this function returns a structured report
    that surfaces specific afflictions Codex flagged as missing from
    the shallow model: dusthana (6/8/12) placement, combustion near
    Sun, retrograde motion, and (future) nakshatra friendliness.

    Args:
        planet:        e.g., "Sun", "Mars", "Rahu"
        sign:          zodiac sign, e.g., "Aries"
        house:         1..12 house placement (optional)
        is_retrograde: planet in retrograde motion
        is_combust:    planet within combustion orb of Sun
        nakshatra:     nakshatra name (optional, reserved for future)

    Returns:
        {
            "dignity": str,              # Exalted/Own Sign/Friendly/Neutral/Enemy/Debilitated
            "strength_score": float,     # 0.0 (weakest) to 1.0 (strongest)
            "afflictions": list[str],    # e.g., ["combust", "debilitated", "in dusthana house 8"]
            "is_afflicted": bool,        # True if strength_score < 0.4
        }
    """
    # Base dignity label (string) — uses existing classical rule set
    dignity = _get_dignity_label(planet, sign)

    # Dignity → base score (matches astro_iogita_engine.get_planet_strength values
    # for parity with the rest of the system)
    dignity_score_map = {
        "Exalted": 1.0,
        "Own Sign": 0.85,
        "Friendly": 0.65,
        "Neutral": 0.5,
        "Enemy": 0.25,
        "Debilitated": 0.1,
    }
    base = dignity_score_map.get(dignity, 0.5)

    afflictions: list = []

    # House placement modifiers
    # Dusthana (6/8/12) weakens; Kendras (1/4/7/10) and Trikonas (1/5/9) strengthen
    house_modifier = 0.0
    if house is not None:
        if house in (6, 8, 12):
            house_modifier = -0.15
            afflictions.append(f"in dusthana house {house}")
        elif house in (1, 4, 5, 7, 9, 10):
            house_modifier = +0.10

    # Combustion (Asta) — penalize strength and surface as affliction.
    # Kept intentionally simple for reliability: fixed penalty.
    combust_modifier = 0.0
    if is_combust and planet not in ("Sun", "Moon"):
        combust_modifier = -0.2
        afflictions.append("combust")

    # Retrograde — Lal Kitab treats as "confused planet"
    # (Sun/Moon never retrograde; Rahu/Ketu are always retrograde by nature)
    retrograde_modifier = 0.0
    if is_retrograde and planet not in ("Sun", "Moon", "Rahu", "Ketu"):
        retrograde_modifier = -0.1
        afflictions.append("retrograde")

    # Nakshatra — reserved for future enrichment. Currently neutral hook.
    nakshatra_modifier = 0.0
    if nakshatra:
        # Future: compare nakshatra lord vs. planet friendship
        pass

    # Record dignity-based afflictions
    if dignity == "Debilitated":
        afflictions.append("debilitated")
    elif dignity == "Enemy":
        afflictions.append("in enemy sign")

    # Final score (clamped to 0..1)
    strength_score = (
        base
        + house_modifier
        + combust_modifier
        + retrograde_modifier
        + nakshatra_modifier
    )
    strength_score = max(0.0, min(1.0, strength_score))

    return {
        "dignity": dignity,
        "strength_score": round(strength_score, 3),
        "afflictions": afflictions,
        "is_afflicted": strength_score < 0.4,
    }


def get_remedies(planet_positions: dict, chart_data: "dict | None" = None) -> dict:
    """
    Get Lal Kitab remedies based on planet × house placement.

    Args:
        planet_positions: {planet_name: sign_name} where sign maps to LK house
            via _SIGN_TO_LK_HOUSE (Aries=1 through Pisces=12)
        chart_data: optional full chart dict (shape: {"planets": {planet: {house, retrograde,
            combust, nakshatra, ...}}}) — when provided, enriched strength is
            computed via `get_planet_strength_detailed` (accounts for combustion,
            retrograde, dusthana house, nakshatra) and the resulting
            `afflictions` list is added to each planet's entry.

    Returns:
        dict of {planet: {
            sign: str,
            lk_house: int,
            dignity: str,
            strength: float,
            remedy: dict (en/hi/material/day/urgency — always present for the house),
            has_remedy: bool (True when strength < 0.5),
            remedies: list[str]  (backward-compat: populated only when has_remedy=True),
            afflictions: list[str]  (only populated when chart_data provided)
        }}
        Remedies are prescribed only for planets with strength < 0.5
        (enemy or debilitated placements).
    """
    result = {}

    for planet, sign in planet_positions.items():
        # Invalid sign = unknown house, NOT Aries/house-1. Surface honestly.
        lk_house = _SIGN_TO_LK_HOUSE.get(sign, 0)
        if lk_house == 0:
            result[planet] = {
                "sign": sign,
                "lk_house": 0,
                "dignity": "Unknown",
                "strength": 0.0,
                "remedy": None,
                "has_remedy": False,
                "remedies": [],
                "error": f"Invalid sign '{sign}' — cannot compute Lal Kitab house",
            }
            continue
        afflictions: list = []

        if chart_data and isinstance(chart_data, dict) and "planets" in chart_data:
            p_info = chart_data["planets"].get(planet, {}) or {}
            detailed = get_planet_strength_detailed(
                planet=planet,
                sign=sign,
                house=p_info.get("house"),
                is_retrograde=p_info.get("retrograde", p_info.get("is_retrograde", False)),
                is_combust=p_info.get("combust", p_info.get("is_combust", False)),
                nakshatra=p_info.get("nakshatra"),
            )
            strength = detailed["strength_score"]
            dignity = detailed["dignity"]
            afflictions = detailed["afflictions"]
        else:
            # Backward compat path — sign-only strength
            strength = get_planet_strength(planet, sign)
            dignity = _get_dignity_label(planet, sign)

        # Get house-specific remedy (always present for reference)
        planet_houses = REMEDIES_BY_HOUSE.get(planet, {})
        house_remedy = planet_houses.get(lk_house, {
            "en": f"Propitiate {planet} with planet-specific offerings on its ruling day.",
            "hi": f"{planet} ग्रह की शांति के लिए उसके स्वामी दिन पर उपाय करें।",
            "material": "varies",
            "day": "Sunday",
            "urgency": "low",
        })

        is_weak = strength < 0.5

        # Merge remedy context (problem / reason / how_it_works) into remedy dict
        ctx = _REMEDY_CONTEXT.get((planet, lk_house), {})
        enriched_remedy = {**house_remedy, **ctx}

        # Backward-compat: old tests check result[planet]["remedies"] as a list
        compat_remedies = [house_remedy["en"]] if is_weak else []

        entry = {
            "sign": sign,
            "lk_house": lk_house,
            "dignity": dignity,
            "strength": round(strength, 2),
            "remedy": enriched_remedy,
            "has_remedy": is_weak,
            # Backward compatibility key — old tests expect this
            "remedies": compat_remedies,
        }
        # Only expose afflictions when the enriched path ran (keeps
        # backward-compat callers untouched)
        if chart_data and isinstance(chart_data, dict) and "planets" in chart_data:
            entry["afflictions"] = afflictions

        result[planet] = entry

    # Stamp each planet's entry + the result envelope with the LK_CANONICAL
    # provenance tag — these per-planet remedies come directly from the
    # position tables in Lal Kitab 1952.
    from app.lalkitab_source_tags import source_of
    from app.lalkitab_savdhaniyan import get_remedy_precautions
    from app.lalkitab_andhe_grah import detect_andhe_grah
    from app.lalkitab_remedy_classifier import stamp_classification
    src = source_of("get_remedies")

    # P0.2 — run blind-planet detector once so both remedy entries and
    # adjacency warnings are sourced from the same pass.
    pp_list = [
        {"planet": pn, "house": pe.get("lk_house"), "sign": pe.get("sign")}
        for pn, pe in result.items()
        if isinstance(pe.get("lk_house"), int) and pe.get("lk_house") > 0
    ]
    andhe = detect_andhe_grah(pp_list, chart_data=chart_data)
    blind_map = andhe.get("per_planet") or {}
    adjacency = {w["planet"]: w for w in (andhe.get("adjacency_warnings") or [])}

    for planet_name, planet_entry in result.items():
        planet_entry.setdefault("source", src)
        if isinstance(planet_entry.get("remedy"), dict):
            planet_entry["remedy"].setdefault("source", src)
            # P1.11 — stamp Trial / Remedy / Good Conduct tier on every remedy.
            stamp_classification(planet_entry["remedy"])

        # P0.1 — attach the Savdhaniyan bundle (LK 4.08 + 4.09) so the UI
        # surfaces every mandatory precaution BEFORE the remedy action.
        rem = planet_entry.get("remedy") or {}
        precaution_bundle = get_remedy_precautions(
            planet_name,
            house=planet_entry.get("lk_house"),
            remedy_material=rem.get("material", "") if isinstance(rem, dict) else "",
        )
        planet_entry["savdhaniyan"] = precaution_bundle
        planet_entry["time_rule"] = precaution_bundle["time_rule"]
        planet_entry["reversal_risk"] = precaution_bundle["reversal_risk"]

        # P0.3 — blind-planet warning attached to remedies that target a
        # blind planet OR a planet adjacent to one. Rendered BEFORE the
        # remedy per LK 4.14.
        blind_info = blind_map.get(planet_name) or {}
        adj_info = adjacency.get(planet_name)
        blind_warning = None
        if blind_info.get("is_blind"):
            blind_warning = {
                "kind": "blind_planet",
                "severity": blind_info.get("severity"),
                "reasons": blind_info.get("reasons"),
                "en": blind_info.get("warning_en"),
                "hi": blind_info.get("warning_hi"),
                "lk_ref": "4.14",
            }
        elif adj_info:
            blind_warning = {
                "kind": "adjacent_to_blind",
                "severity": "medium",
                "adjacent_to_blind": adj_info.get("adjacent_to_blind"),
                "en": adj_info.get("note_en"),
                "hi": adj_info.get("note_hi"),
                "lk_ref": "4.14",
            }
        if blind_warning:
            planet_entry["andhe_grah_warning"] = blind_warning

    return result
