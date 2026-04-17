"""
Chandra Chalana 43-day protocol tasks (backend).

The protocol itself is tracked in DB via lk_chandra_protocol + lk_journal_entries.
The daily task list is served from here so the frontend does not carry a hardcoded
task table.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal


TaskCategory = Literal["action", "donation", "meditation", "fasting", "mantra"]


CHANDRA_CHAALANA_TASKS: List[Dict[str, Any]] = [
    {"day": 1, "en": "Begin with a cold water bath at sunrise. Offer white flowers to Moon image.", "hi": "सूर्योदय पर ठंडे पानी से स्नान करें। चंद्रमा की छवि पर सफेद फूल चढ़ाएं।", "category": "action"},
    {"day": 2, "en": "Donate white rice and milk to a needy family.", "hi": "किसी जरूरतमंद परिवार को सफेद चावल और दूध दान करें।", "category": "donation"},
    {"day": 3, "en": 'Recite "Om Som Somaya Namaha" 108 times after moonrise.', "hi": 'चंद्रोदय के बाद "ॐ सोम सोमाय नमः" 108 बार जपें।', "category": "mantra"},
    {"day": 4, "en": "Keep a silver glass of water by your bedside. Pour it on a plant in the morning.", "hi": "बिस्तर के पास चांदी के गिलास में पानी रखें। सुबह पौधे पर डालें।", "category": "action"},
    {"day": 5, "en": "Fast on rice and milk only. No fried or spicy food.", "hi": "केवल चावल और दूध पर उपवास रखें। तला या मसालेदार नहीं।", "category": "fasting"},
    {"day": 6, "en": "Feed fish or birds with rice at a water body.", "hi": "नदी या तालाब में मछलियों या पक्षियों को चावल खिलाएं।", "category": "action"},
    {"day": 7, "en": "Meditate on a full moon image for 15 minutes. Visualize calm blue light.", "hi": "पूर्णिमा की छवि पर 15 मिनट ध्यान करें। शांत नीली रोशनी की कल्पना करें।", "category": "meditation"},
    {"day": 8, "en": "Wear white or cream clothes all day. Avoid black and red.", "hi": "पूरे दिन सफेद या क्रीम कपड़े पहनें। काले और लाल से बचें।", "category": "action"},
    {"day": 9, "en": "Donate a white bedsheet or white cloth to an elderly woman.", "hi": "किसी बुजुर्ग महिला को सफेद चादर या सफेद कपड़ा दान करें।", "category": "donation"},
    {"day": 10, "en": 'Recite "Om Shram Shrim Shraum Sah Chandraya Namah" 108 times.', "hi": '"ॐ श्रां श्रीं श्रौं सः चंद्राय नमः" 108 बार जपें।', "category": "mantra"},
    {"day": 11, "en": "Keep a small pearl or moonstone in your wallet.", "hi": "अपने पर्स में छोटा मोती या मूनस्टोन रखें।", "category": "action"},
    {"day": 12, "en": "Feed a white cow with rice and sugar.", "hi": "सफेद गाय को चावल और चीनी खिलाएं।", "category": "action"},
    {"day": 13, "en": "Write a forgiveness letter (not necessarily sent). Keep it with you.", "hi": "एक क्षमा पत्र लिखें (भेजना जरूरी नहीं)। उसे अपने पास रखें।", "category": "meditation"},
    {"day": 14, "en": "Wash a square piece of silver and keep it on you all day.", "hi": "चांदी के चौकोर टुकड़े को धोएं और पूरे दिन अपने पास रखें।", "category": "action"},
    {"day": 15, "en": "Mid-point milestone: donate white sweets to at least 7 people.", "hi": "मध्य बिंदु: कम से कम 7 लोगों को सफेद मिठाई दान करें।", "category": "donation"},
    {"day": 16, "en": "Take a bath with sandalwood-mixed water. Avoid soap today.", "hi": "चंदन मिले पानी से स्नान करें। आज साबुन से बचें।", "category": "action"},
    {"day": 17, "en": "Meditate near open water (river, lake, or fountain) for 20 minutes.", "hi": "खुले पानी (नदी, झील, फव्वारे) के पास 20 मिनट ध्यान करें।", "category": "meditation"},
    {"day": 18, "en": 'Recite "Om Hreem Chandraya Namaha" 108 times.', "hi": '"ॐ ह्रीं चंद्राय नमः" 108 बार जपें।', "category": "mantra"},
    {"day": 19, "en": "Donate milk and rice to a temple or orphanage.", "hi": "किसी मंदिर या अनाथालय में दूध और चावल दान करें।", "category": "donation"},
    {"day": 20, "en": "Keep your home clean and free of clutter. Light a white candle.", "hi": "अपना घर साफ और गंदगी मुक्त रखें। एक सफेद मोमबत्ती जलाएं।", "category": "action"},
    {"day": 21, "en": "Three-week milestone: observe silence for 2 hours in the evening.", "hi": "तीन सप्ताह का मील का पत्थर: शाम को 2 घंटे मौन रखें।", "category": "meditation"},
    {"day": 22, "en": "Feed crows and birds with white rice in the morning.", "hi": "सुबह कौओं और पक्षियों को सफेद चावल खिलाएं।", "category": "action"},
    {"day": 23, "en": "Donate a white umbrella or white cloth to a needy person.", "hi": "किसी जरूरतमंद को सफेद छाता या सफेद कपड़ा दान करें।", "category": "donation"},
    {"day": 24, "en": "Recite the Chandra Gayatri Mantra 21 times after moonrise.", "hi": "चंद्रोदय के बाद चंद्र गायत्री मंत्र 21 बार जपें।", "category": "mantra"},
    {"day": 25, "en": "Eat only sattvic food (no garlic or onion). Drink coconut water.", "hi": "केवल सात्विक भोजन करें (लहसुन-प्याज नहीं)। नारियल पानी पीएं।", "category": "fasting"},
    {"day": 26, "en": "Spend time near a water body or watch the moon rise today.", "hi": "पानी के पास समय बिताएं या आज चंद्रोदय देखें।", "category": "meditation"},
    {"day": 27, "en": "Write down 27 things you are grateful for in your life.", "hi": "अपने जीवन में जिन 27 चीजों के लिए आभारी हैं उन्हें लिखें।", "category": "meditation"},
    {"day": 28, "en": "Float a coconut with white flowers in flowing water.", "hi": "बहते पानी में सफेद फूलों के साथ नारियल बहाएं।", "category": "action"},
    {"day": 29, "en": "Donate a silver coin to a place of worship.", "hi": "किसी पूजा स्थल पर चांदी का सिक्का दान करें।", "category": "donation"},
    {"day": 30, "en": "Recite Moon mantra 108 times. Meditate for 15 minutes.", "hi": "चंद्र मंत्र 108 बार जपें। 15 मिनट ध्यान करें।", "category": "mantra"},
    {"day": 31, "en": "Keep a bowl of milk on your rooftop under moonlight overnight.", "hi": "रात भर छत पर दूध का कटोरा चांदनी में रखें।", "category": "action"},
    {"day": 32, "en": "Complete fast today. Consume only water and milk.", "hi": "आज पूर्ण उपवास रखें। केवल पानी और दूध लें।", "category": "fasting"},
    {"day": 33, "en": "Write a letter of intention — what change you want from this protocol.", "hi": "एक इरादे का पत्र लिखें — इस प्रोटोकॉल से आप क्या बदलाव चाहते हैं।", "category": "meditation"},
    {"day": 34, "en": "Donate white sesame seeds and rice to a Shiva temple.", "hi": "शिव मंदिर में सफेद तिल और चावल दान करें।", "category": "donation"},
    {"day": 35, "en": 'Recite Moon mantra 108 times walking barefoot on grass at dawn.', "hi": "भोर में घास पर नंगे पांव चलते हुए चंद्र मंत्र 108 बार जपें।", "category": "mantra"},
    {"day": 36, "en": "Keep your water intake high. Drink from a silver cup if possible.", "hi": "पानी की मात्रा अधिक रखें। हो सके तो चांदी के कप से पीएं।", "category": "action"},
    {"day": 37, "en": "Donate food (rice, lentils, milk) to at least 43 people.", "hi": "कम से कम 43 लोगों को खाना (चावल, दाल, दूध) दान करें।", "category": "donation"},
    {"day": 38, "en": "Meditate on white light filling your body for 20 minutes.", "hi": "सफेद रोशनी से अपना शरीर भरने पर 20 मिनट ध्यान करें।", "category": "meditation"},
    {"day": 39, "en": 'Recite "Om Shrim Chandra Namaha" 1008 times today.', "hi": '"ॐ श्रीम् चंद्र नमः" आज 1008 बार जपें।', "category": "mantra"},
    {"day": 40, "en": "Offer white flowers and milk at a Shiva or Devi temple.", "hi": "शिव या देवी मंदिर में सफेद फूल और दूध चढ़ाएं।", "category": "action"},
    {"day": 41, "en": "Reflect on the last 40 days. Write what has changed or improved.", "hi": "पिछले 40 दिनों पर विचार करें। लिखें क्या बदला या बेहतर हुआ।", "category": "meditation"},
    {"day": 42, "en": "Donate a small pearl or white cloth to a senior female family member.", "hi": "परिवार की वरिष्ठ महिला को छोटा मोती या सफेद कपड़ा दान करें।", "category": "donation"},
    {"day": 43, "en": "Final day: Float 43 white flowers in flowing water. Chandra Chalana complete!", "hi": "अंतिम दिन: बहते पानी में 43 सफेद फूल बहाएं। चंद्र चालना पूर्ण!", "category": "action"},
]

