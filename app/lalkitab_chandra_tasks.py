"""
Chandra Chalana 43-day protocol tasks (backend).

The protocol itself is tracked in DB via lk_chandra_protocol + lk_journal_entries.
The daily task list is served from here so the frontend does not carry a hardcoded
task table.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Literal, Optional


TaskCategory = Literal["action", "donation", "meditation", "fasting", "mantra"]

# Milestone days get house-specific overrides when moon_house is known
_MILESTONE_DAYS = {1, 5, 8, 15, 21, 28, 32, 43}

# Per-house override text for each milestone day.
# Keys: moon_house (1-12) → day → {en, hi, category}
_HOUSE_OVERRIDES: Dict[int, Dict[int, Dict[str, Any]]] = {
    1: {  # Moon H1 — self, identity, new beginnings
        1:  {"en": "Begin with a cold water bath at sunrise. Set one clear personal intention for this 43-day transformation.", "hi": "सूर्योदय पर ठंडे पानी से स्नान करें। इस 43-दिवसीय परिवर्तन के लिए एक स्पष्ट व्यक्तिगत इरादा निर्धारित करें।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Write down one false belief about yourself that you are releasing today.", "hi": "दूध और चावल पर उपवास। आज अपने बारे में एक झूठी धारणा लिखें जिसे आप छोड़ रहे हैं।", "category": "fasting"},
        8:  {"en": "Wear white all day — a symbol of your refreshed identity. Look in a mirror and affirm: 'I am becoming who I am meant to be.'", "hi": "पूरे दिन सफेद पहनें — नई पहचान का प्रतीक। दर्पण में देखें और पुष्टि करें: 'मैं वही बन रहा हूं जो मुझे बनना है।'", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to 7 people AND write a statement of the new self you are building.", "hi": "मध्य बिंदु: 7 लोगों को सफेद मिठाई दें और उस नए व्यक्तित्व का विवरण लिखें जो आप बना रहे हैं।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence — during this silence, observe how your identity has shifted in 21 days.", "hi": "तीन सप्ताह: 2 घंटे मौन — इस मौन में देखें कि 21 दिनों में आपकी पहचान कैसे बदली है।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers — symbolizing old identity released into the universe.", "hi": "सफेद फूलों के साथ नारियल बहाएं — पुरानी पहचान को ब्रह्मांड में छोड़ने का प्रतीक।", "category": "action"},
        32: {"en": "Complete fast on water and milk. Spend the day entirely in self-study and stillness.", "hi": "पानी और दूध पर पूर्ण उपवास। दिन पूरी तरह आत्म-अध्ययन और स्थिरता में बिताएं।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers. You have completed a full cycle of self-renewal. Chandra Chalana complete!", "hi": "अंतिम दिन: 43 सफेद फूल बहाएं। आपने आत्म-नवीनीकरण का पूरा चक्र पूरा कर लिया। चंद्र चालना पूर्ण!", "category": "action"},
    },
    2: {  # Moon H2 — speech, wealth, family
        1:  {"en": "Begin with a bath at sunrise. Today, speak only kind and true words — no criticism all day.", "hi": "सूर्योदय पर स्नान करें। आज केवल दयालु और सच्चे शब्द बोलें — पूरे दिन कोई आलोचना नहीं।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Donate food to a family in need — this blesses your family lineage.", "hi": "दूध और चावल पर उपवास। किसी जरूरतमंद परिवार को खाना दान करें — यह आपके परिवार को आशीर्वाद देता है।", "category": "fasting"},
        8:  {"en": "Wear white. Visit or call a family elder and speak words of love and respect.", "hi": "सफेद पहनें। परिवार के किसी बुजुर्ग से मिलें और प्रेम और सम्मान के शब्द बोलें।", "category": "action"},
        15: {"en": "Mid-point: prepare a family meal yourself and serve it with love. Donate white sweets after.", "hi": "मध्य बिंदु: स्वयं पारिवारिक भोजन बनाएं और प्रेम से परोसें। बाद में सफेद मिठाई दान करें।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence. Contemplate what family patterns you are healing.", "hi": "तीन सप्ताह: 2 घंटे मौन। सोचें कि आप कौन से पारिवारिक पैटर्न ठीक कर रहे हैं।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers at a river. Offer it for the healing of your family wealth and bonds.", "hi": "नदी में सफेद फूलों के साथ नारियल बहाएं। इसे अपने परिवार की समृद्धि और बंधन की चिकित्सा के लिए अर्पित करें।", "category": "action"},
        32: {"en": "Complete fast. Recite family ancestor names mentally and offer them gratitude.", "hi": "पूर्ण उपवास। मन में परिवार के पूर्वजों के नाम जपें और उन्हें धन्यवाद दें।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers for your family lineage. Chandra Chalana complete!", "hi": "अंतिम दिन: परिवार के लिए 43 सफेद फूल बहाएं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    3: {  # Moon H3 — siblings, courage, communication
        1:  {"en": "Begin at sunrise with a bath. Write a note of appreciation to a sibling or close colleague.", "hi": "सूर्योदय पर स्नान से शुरू करें। किसी भाई-बहन या करीबी सहकर्मी को सराहना का नोट लिखें।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Practice speaking your truth gently to one person today.", "hi": "दूध और चावल पर उपवास। आज एक व्यक्ति से अपनी बात कोमलता से कहें।", "category": "fasting"},
        8:  {"en": "Wear white. Take a short journey (even a walk) — Moon in H3 is activated by movement.", "hi": "सफेद पहनें। एक छोटी यात्रा करें (थोड़ी सी भी) — H3 का चंद्र आंदोलन से सक्रिय होता है।", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to 7 people, including someone you had a conflict with.", "hi": "मध्य बिंदु: 7 लोगों को सफेद मिठाई दें, जिनमें वह भी हों जिनसे आपका विवाद था।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence — write down three acts of courage you want to take.", "hi": "तीन सप्ताह: 2 घंटे मौन — तीन साहसी कार्य लिखें जो आप करना चाहते हैं।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers. Offer it for harmonious sibling relationships.", "hi": "सफेद फूलों के साथ नारियल बहाएं। भाई-बहनों के साथ सामंजस्य के लिए अर्पित करें।", "category": "action"},
        32: {"en": "Complete fast on water and milk. Spend time writing or creating — H3 Moon heals through expression.", "hi": "पानी और दूध पर पूर्ण उपवास। लिखने या रचना में समय बिताएं — H3 चंद्र अभिव्यक्ति से ठीक होता है।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers. Your courage and voice are renewed. Chandra Chalana complete!", "hi": "अंतिम दिन: 43 सफेद फूल बहाएं। आपका साहस और आवाज नवीनीकृत हैं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    4: {  # Moon H4 — home, mother, water, emotions
        1:  {"en": "Begin with a cold water bath at sunrise. Clean one room of your home before anything else — H4 Moon is healed by a clean home.", "hi": "सूर्योदय पर ठंडे पानी से स्नान। कुछ भी करने से पहले घर का एक कमरा साफ करें — H4 चंद्र साफ घर से ठीक होता है।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Cook one meal for your mother or a maternal figure — even symbolically prepare a dish in her honor.", "hi": "दूध और चावल पर उपवास। माँ या मातृ आकृति के लिए एक भोजन बनाएं — प्रतीकात्मक रूप से भी उनके सम्मान में भोजन तैयार करें।", "category": "fasting"},
        8:  {"en": "Wear white. Place fresh white flowers in the kitchen or dining area — center of the H4 home domain.", "hi": "सफेद पहनें। रसोई या भोजन क्षेत्र में ताजे सफेद फूल रखें — H4 घर का केंद्र।", "category": "action"},
        15: {"en": "Mid-point: prepare a home-cooked meal for 7 or more people. Service through home and kitchen activates Moon H4.", "hi": "मध्य बिंदु: 7 या अधिक लोगों के लिए घर पर भोजन बनाएं। घर और रसोई से सेवा H4 चंद्र को सक्रिय करती है।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence near water — a river, lake, or simply sit with a bowl of water at home.", "hi": "तीन सप्ताह: पानी के पास 2 घंटे मौन — नदी, झील, या घर पर पानी के कटोरे के पास बैठें।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers at the nearest body of water. Whisper a prayer for your mother and home.", "hi": "निकटतम जलाशय में सफेद फूलों के साथ नारियल बहाएं। अपनी माँ और घर के लिए प्रार्थना फुसफुसाएं।", "category": "action"},
        32: {"en": "Complete fast on water and milk. Spend the day at home, resting and nurturing yourself — as H4 Moon demands.", "hi": "पानी और दूध पर पूर्ण उपवास। घर पर दिन बिताएं, आराम करें और अपना ख्याल रखें — जैसे H4 चंद्र चाहता है।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers at water's edge. Your home and emotional roots are healed. Chandra Chalana complete!", "hi": "अंतिम दिन: पानी के किनारे 43 सफेद फूल बहाएं। आपका घर और भावनात्मक जड़ें ठीक हो गई हैं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    5: {  # Moon H5 — creativity, children, romance, merit
        1:  {"en": "Begin with a sunrise bath. Spend 10 minutes doing something purely creative — draw, sing, write a poem.", "hi": "सूर्योदय पर स्नान। 10 मिनट कुछ पूरी तरह रचनात्मक करें — चित्र बनाएं, गाएं, कविता लिखें।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Read or recite a sacred story — H5 Moon is strengthened by devotional literature.", "hi": "दूध और चावल पर उपवास। कोई पवित्र कहानी पढ़ें या सुनाएं — H5 चंद्र भक्ति साहित्य से मजबूत होता है।", "category": "fasting"},
        8:  {"en": "Wear white. Spend time with a child — play, teach, or simply listen to their world.", "hi": "सफेद पहनें। किसी बच्चे के साथ समय बिताएं — खेलें, सिखाएं, या बस उनकी दुनिया सुनें।", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to children. Create something — a drawing, a poem — and offer it as thanks.", "hi": "मध्य बिंदु: बच्चों को सफेद मिठाई दें। कुछ बनाएं — चित्र, कविता — और धन्यवाद के रूप में अर्पित करें।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours of creative silence — journal your visions and creative dreams.", "hi": "तीन सप्ताह: 2 घंटे रचनात्मक मौन — अपनी दृष्टि और रचनात्मक सपने लिखें।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers for the children of your lineage — born and unborn.", "hi": "अपने वंश के बच्चों के लिए — पैदा हुए और अजन्मे — सफेद फूलों के साथ नारियल बहाएं।", "category": "action"},
        32: {"en": "Complete fast on water and milk. Dedicate the day to prayer for the happiness of children around you.", "hi": "पानी और दूध पर पूर्ण उपवास। आपके आसपास के बच्चों की खुशी के लिए प्रार्थना में दिन समर्पित करें।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers — for every creative gift within you. Chandra Chalana complete!", "hi": "अंतिम दिन: 43 सफेद फूल बहाएं — आपके भीतर हर रचनात्मक उपहार के लिए। चंद्र चालना पूर्ण!", "category": "action"},
    },
    6: {  # Moon H6 — health, enemies, service, debts
        1:  {"en": "Begin with a sunrise bath. Today, perform one act of selfless service — help someone without expectation.", "hi": "सूर्योदय पर स्नान। आज निस्वार्थ सेवा का एक कार्य करें — बिना अपेक्षा के किसी की मदद करें।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Reflect on one recurring health issue — resolve to make one lifestyle change.", "hi": "दूध और चावल पर उपवास। एक बार-बार होने वाली स्वास्थ्य समस्या पर विचार करें — एक जीवनशैली बदलाव का संकल्प लें।", "category": "fasting"},
        8:  {"en": "Wear white. Volunteer or donate to a hospital, shelter, or service organization.", "hi": "सफेद पहनें। अस्पताल, आश्रय या सेवा संगठन में स्वयंसेवा करें या दान दें।", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to 7 service workers — cleaners, helpers, medical staff.", "hi": "मध्य बिंदु: 7 सेवा कर्मियों को सफेद मिठाई दें — सफाईकर्मी, सहायक, चिकित्सा कर्मचारी।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence — review your health habits and debts. Release resentment toward enemies.", "hi": "तीन सप्ताह: 2 घंटे मौन — अपनी स्वास्थ्य आदतों और ऋणों की समीक्षा करें। दुश्मनों के प्रति आक्रोश छोड़ें।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers. Offer it for healing of hidden health issues and clearing of karmic debts.", "hi": "सफेद फूलों के साथ नारियल बहाएं। छिपी स्वास्थ्य समस्याओं और कर्म ऋण की सफाई के लिए अर्पित करें।", "category": "action"},
        32: {"en": "Complete fast. Spend the day in conscious rest — H6 Moon heals fastest through disciplined self-care.", "hi": "पूर्ण उपवास। दिन सचेत आराम में बिताएं — H6 चंद्र अनुशासित आत्म-देखभाल से सबसे तेजी से ठीक होता है।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers — one for every debt, illness, or enemy you release. Chandra Chalana complete!", "hi": "अंतिम दिन: 43 सफेद फूल बहाएं — हर ऋण, बीमारी या दुश्मन के लिए जिसे आप छोड़ रहे हैं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    7: {  # Moon H7 — partnerships, marriage, open enemies
        1:  {"en": "Begin with a sunrise bath. Reach out to your partner or closest companion with a sincere expression of love.", "hi": "सूर्योदय पर स्नान। अपने साथी या करीबी मित्र से प्रेम की ईमानदार अभिव्यक्ति के साथ संपर्क करें।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Write down three qualities you seek in partnership — then embody them yourself today.", "hi": "दूध और चावल पर उपवास। साझेदारी में जो तीन गुण आप चाहते हैं उन्हें लिखें — फिर आज स्वयं उन्हें अपनाएं।", "category": "fasting"},
        8:  {"en": "Wear white. Spend quality time with your partner or a trusted friend — no devices, full presence.", "hi": "सफेद पहनें। अपने साथी या भरोसेमंद मित्र के साथ गुणवत्तापूर्ण समय बिताएं — कोई उपकरण नहीं, पूर्ण उपस्थिति।", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to 7 couples or families. Pray for all your partnerships to flourish.", "hi": "मध्य बिंदु: 7 जोड़ों या परिवारों को सफेद मिठाई दें। अपनी सभी साझेदारियों के फलने-फूलने की प्रार्थना करें।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence — reflect on your relationship patterns and what needs to heal.", "hi": "तीन सप्ताह: 2 घंटे मौन — अपने रिश्ते के पैटर्न पर विचार करें और क्या ठीक होने की जरूरत है।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers. Offer it for healing and harmony in all your partnerships.", "hi": "सफेद फूलों के साथ नारियल बहाएं। अपनी सभी साझेदारियों में उपचार और सामंजस्य के लिए अर्पित करें।", "category": "action"},
        32: {"en": "Complete fast on water and milk. Pray for a specific relationship that needs healing.", "hi": "पानी और दूध पर पूर्ण उपवास। उस विशिष्ट रिश्ते के लिए प्रार्थना करें जिसे उपचार की आवश्यकता है।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers for all souls you have been partnered with. Chandra Chalana complete!", "hi": "अंतिम दिन: उन सभी आत्माओं के लिए 43 सफेद फूल बहाएं जिनके साथ आप साझेदार रहे हैं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    8: {  # Moon H8 — transformation, grief, hidden things, in-laws
        1:  {"en": "Begin with a cold water bath at sunrise. Light a white candle and sit with whatever grief or fear you have been avoiding.", "hi": "सूर्योदय पर ठंडे पानी से स्नान। सफेद मोमबत्ती जलाएं और जो दुख या डर आप टाल रहे थे उसके साथ बैठें।", "category": "meditation"},
        5:  {"en": "Fast on milk and rice. Write a letter to someone you have lost — living or passed. Do not send. Burn it safely.", "hi": "दूध और चावल पर उपवास। किसी खोए हुए व्यक्ति को पत्र लिखें — जीवित या दिवंगत। न भेजें। सुरक्षित जलाएं।", "category": "fasting"},
        8:  {"en": "Wear white as an act of release. Moon in H8 is debilitated — wearing white today calls in the lunar healing light.", "hi": "मुक्ति के भाव से सफेद पहनें। H8 में चंद्र नीच का है — आज सफेद पहनना चंद्र उपचार प्रकाश को बुलाता है।", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to 7 people AND perform a small ritual releasing grief — float flowers at water's edge.", "hi": "मध्य बिंदु: 7 लोगों को सफेद मिठाई दें और एक छोटा दुख-मुक्ति अनुष्ठान करें — पानी के किनारे फूल बहाएं।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours of deep silence. Face one hidden truth about yourself that you have avoided.", "hi": "तीन सप्ताह: 2 घंटे गहरा मौन। अपने बारे में वह एक छिपी सच्चाई सामना करें जिससे आप बचते रहे हैं।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers — release the grief, fear, or hidden burden you carried into this protocol.", "hi": "सफेद फूलों के साथ नारियल बहाएं — वह दुख, डर या छिपा बोझ छोड़ें जो आप इस प्रोटोकॉल में लाए थे।", "category": "action"},
        32: {"en": "Complete fast today. This is the deepest purification day for H8 Moon — sit in silence and allow grief to move through.", "hi": "आज पूर्ण उपवास। यह H8 चंद्र के लिए सबसे गहरी शुद्धि का दिन है — मौन में बैठें और दुख को बहने दें।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers for every transformation and loss that made you who you are. Chandra Chalana complete!", "hi": "अंतिम दिन: हर उस परिवर्तन और हानि के लिए 43 सफेद फूल बहाएं जिसने आपको वह बनाया जो आप हैं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    9: {  # Moon H9 — dharma, father, guru, fortune, long journeys
        1:  {"en": "Begin with a sunrise bath. Offer a prayer to your guru, father, or highest spiritual ideal before starting this 43-day journey.", "hi": "सूर्योदय पर स्नान। इस 43-दिवसीय यात्रा शुरू करने से पहले अपने गुरु, पिता या उच्चतम आध्यात्मिक आदर्श को प्रार्थना करें।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Read from a sacred scripture or your teacher's teachings — H9 Moon feeds on dharmic wisdom.", "hi": "दूध और चावल पर उपवास। पवित्र शास्त्र या अपने गुरु की शिक्षाओं से पढ़ें — H9 चंद्र धर्मिक ज्ञान से पोषित होता है।", "category": "fasting"},
        8:  {"en": "Wear white. Take a short pilgrimage — even to a nearby temple or sacred spot — to activate H9 Moon energy.", "hi": "सफेद पहनें। एक छोटी तीर्थ यात्रा करें — पास के मंदिर या पवित्र स्थान पर भी — H9 चंद्र ऊर्जा सक्रिय करने के लिए।", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to 7 Brahmins, teachers, or spiritual seekers.", "hi": "मध्य बिंदु: 7 ब्राह्मणों, शिक्षकों या आध्यात्मिक साधकों को सफेद मिठाई दान करें।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence in a place of worship or under open sky — connect to your dharmic path.", "hi": "तीन सप्ताह: पूजा स्थल या खुले आकाश के नीचे 2 घंटे मौन — अपने धर्म पथ से जुड़ें।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers. Offer it with gratitude to your lineage of teachers and ancestors.", "hi": "सफेद फूलों के साथ नारियल बहाएं। अपने शिक्षकों और पूर्वजों की परंपरा के प्रति कृतज्ञता से अर्पित करें।", "category": "action"},
        32: {"en": "Complete fast on water and milk. Spend this day in prayer, scripture, and contemplation of your life's higher purpose.", "hi": "पानी और दूध पर पूर्ण उपवास। यह दिन प्रार्थना, शास्त्र और अपने जीवन के उच्च उद्देश्य के चिंतन में बिताएं।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers as a thanksgiving offering for all the grace in your life. Chandra Chalana complete!", "hi": "अंतिम दिन: अपने जीवन में सभी कृपा के लिए धन्यवाद अर्पण के रूप में 43 सफेद फूल बहाएं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    10: {  # Moon H10 — career, father, authority, public image
        1:  {"en": "Begin with a sunrise bath. Write down one professional commitment you are making during this 43-day protocol.", "hi": "सूर्योदय पर स्नान। एक पेशेवर प्रतिबद्धता लिखें जो आप इस 43-दिवसीय प्रोटोकॉल के दौरान कर रहे हैं।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Reflect on your career dharma — what work truly serves both you and the world.", "hi": "दूध और चावल पर उपवास। अपने करियर धर्म पर विचार करें — कौन सा काम वास्तव में आपकी और दुनिया दोनों की सेवा करता है।", "category": "fasting"},
        8:  {"en": "Wear white. Perform one act of excellence in your work today — H10 Moon rewards disciplined public action.", "hi": "सफेद पहनें। आज अपने काम में उत्कृष्टता का एक कार्य करें — H10 चंद्र अनुशासित सार्वजनिक कार्य को पुरस्कृत करता है।", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to 7 colleagues or people who support your work.", "hi": "मध्य बिंदु: 7 सहकर्मियों या कार्य सहायकों को सफेद मिठाई दान करें।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence — review your career path and public reputation with total honesty.", "hi": "तीन सप्ताह: 2 घंटे मौन — अपने करियर पथ और सार्वजनिक प्रतिष्ठा की पूरी ईमानदारी से समीक्षा करें।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers. Offer it for your highest career aspirations and your father's blessings.", "hi": "सफेद फूलों के साथ नारियल बहाएं। अपनी उच्चतम करियर आकांक्षाओं और पिता के आशीर्वाद के लिए अर्पित करें।", "category": "action"},
        32: {"en": "Complete fast on water and milk. Rest from all work — H10 Moon renews when given one day of true rest.", "hi": "पानी और दूध पर पूर्ण उपवास। सभी कार्य से विश्राम लें — H10 चंद्र एक दिन के सच्चे आराम से नवीनीकृत होता है।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers for every milestone in your career journey. Chandra Chalana complete!", "hi": "अंतिम दिन: अपनी करियर यात्रा के हर मील के पत्थर के लिए 43 सफेद फूल बहाएं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    11: {  # Moon H11 — gains, friends, elder siblings, desires
        1:  {"en": "Begin with a sunrise bath. Contact an old friend or elder sibling you have lost touch with.", "hi": "सूर्योदय पर स्नान। किसी पुराने मित्र या बड़े भाई-बहन से संपर्क करें जिनसे संपर्क टूट गया था।", "category": "action"},
        5:  {"en": "Fast on milk and rice. Write your 11 most important desires — not demands, but heartfelt wishes.", "hi": "दूध और चावल पर उपवास। अपनी 11 सबसे महत्वपूर्ण इच्छाएं लिखें — मांग नहीं, दिल की तमन्नाएं।", "category": "fasting"},
        8:  {"en": "Wear white. Gather with friends or community — H11 Moon gains strength from social connection.", "hi": "सफेद पहनें। मित्रों या समुदाय के साथ मिलें — H11 चंद्र सामाजिक संबंध से शक्ति प्राप्त करता है।", "category": "action"},
        15: {"en": "Mid-point: donate white sweets to 7 friends or community members who have supported you.", "hi": "मध्य बिंदु: उन 7 मित्रों या समुदाय के सदस्यों को सफेद मिठाई दें जिन्होंने आपका समर्थन किया है।", "category": "donation"},
        21: {"en": "Three-week milestone: 2 hours silence — list all the gains, blessings, and fulfilled desires in your life so far.", "hi": "तीन सप्ताह: 2 घंटे मौन — अपने जीवन में अब तक के सभी लाभ, आशीर्वाद और पूरी हुई इच्छाओं की सूची बनाएं।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers — for the fulfillment of your highest desire.", "hi": "सफेद फूलों के साथ नारियल बहाएं — अपनी उच्चतम इच्छा की पूर्ति के लिए।", "category": "action"},
        32: {"en": "Complete fast. Spend the day in prayer for your network — friends, allies, and all who help you grow.", "hi": "पूर्ण उपवास। अपने नेटवर्क — मित्रों, सहयोगियों और सभी जो आपकी वृद्धि में मदद करते हैं — के लिए प्रार्थना में दिन बिताएं।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers — for every wish granted and every friend who walked with you. Chandra Chalana complete!", "hi": "अंतिम दिन: हर पूरी हुई इच्छा और हर मित्र के लिए 43 सफेद फूल बहाएं। चंद्र चालना पूर्ण!", "category": "action"},
    },
    12: {  # Moon H12 — isolation, liberation, foreign lands, losses
        1:  {"en": "Begin with a cold water bath before sunrise, in near-silence. H12 Moon begins in stillness.", "hi": "सूर्योदय से पहले लगभग मौन में ठंडे पानी से स्नान। H12 चंद्र स्थिरता में शुरू होता है।", "category": "meditation"},
        5:  {"en": "Fast on milk and rice. Spend the entire fast day in near-silence — H12 Moon heals fastest in isolation and quiet.", "hi": "दूध और चावल पर उपवास। पूरा उपवास दिन लगभग मौन में बिताएं — H12 चंद्र एकांत और शांति में सबसे तेज ठीक होता है।", "category": "fasting"},
        8:  {"en": "Wear white. Spend at least 2 hours alone today — in meditation, prayer, or simply sitting with yourself.", "hi": "सफेद पहनें। आज कम से कम 2 घंटे अकेले बिताएं — ध्यान, प्रार्थना, या बस खुद के साथ बैठें।", "category": "meditation"},
        15: {"en": "Mid-point: make an anonymous donation — no one should know. H12 Moon gains through hidden charity.", "hi": "मध्य बिंदु: एक गुमनाम दान करें — किसी को पता नहीं होना चाहिए। H12 चंद्र छिपी दान से लाभ उठाता है।", "category": "donation"},
        21: {"en": "Three-week milestone: practice complete silence from sunrise to sunset — a day of inner pilgrimage.", "hi": "तीन सप्ताह: सूर्योदय से सूर्यास्त तक पूर्ण मौन का अभ्यास करें — आंतरिक तीर्थ का दिन।", "category": "meditation"},
        28: {"en": "Float a coconut with white flowers — offer it for liberation from all hidden fears and burdens.", "hi": "सफेद फूलों के साथ नारियल बहाएं — सभी छिपे डर और बोझ से मुक्ति के लिए अर्पित करें।", "category": "action"},
        32: {"en": "Complete fast on water and milk. Spend the day in a retreat-like state — no social media, no noise, only inner work.", "hi": "पानी और दूध पर पूर्ण उपवास। दिन एकांत-वास जैसी अवस्था में बिताएं — कोई सोशल मीडिया नहीं, कोई शोर नहीं, केवल आंतरिक कार्य।", "category": "fasting"},
        43: {"en": "Final day: Float 43 white flowers before dawn, in stillness. You have walked the path of the hidden Moon. Chandra Chalana complete!", "hi": "अंतिम दिन: भोर से पहले स्थिरता में 43 सफेद फूल बहाएं। आप छिपे चंद्र के पथ पर चले हैं। चंद्र चालना पूर्ण!", "category": "meditation"},
    },
}


def get_personalized_tasks(moon_house: int, moon_strength: str = "neutral") -> List[Dict[str, Any]]:
    """Return the 43 Chandra Chalana tasks with milestone-day overrides for the given Moon house.

    Non-milestone days are universal. Milestone days (1,5,8,15,21,28,32,43) get
    house-specific en/hi/category text so the protocol feels tailored to the chart.
    """
    tasks = copy.deepcopy(CHANDRA_CHAALANA_TASKS)
    overrides = _HOUSE_OVERRIDES.get(moon_house, {})
    if not overrides:
        return tasks
    override_map = {d: overrides[d] for d in overrides}
    for task in tasks:
        day = task["day"]
        if day in override_map:
            task["en"] = override_map[day]["en"]
            task["hi"] = override_map[day]["hi"]
            task["category"] = override_map[day]["category"]
            task["personalized"] = True
        else:
            task["personalized"] = False
    return tasks


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

