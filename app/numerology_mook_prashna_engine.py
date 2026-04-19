"""
numerology_mook_prashna_engine.py — Mook Prashna & Khoyi Vastu
===============================================================
Ancient Indian numerology technique from "Saral Ank Jyotish".

METHOD:
  1. Person writes 9 numbers spontaneously (no thinking)
  2. Sum all 9 → add 3 → final number (range: 3–84)
  3. Look up in table:
     - MOOK PRASHNA: reveals what topic the person is thinking about
     - KHOYI VASTU:  reveals where a lost item is located

Reference: Chapter "Mook Prashna Gyan" from Saral Ank Jyotish.
Attributed to Sepharial ("Kabala of Numbers") who learned from an Indian Swami.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# TABLE 1: MOOK PRASHNA — Question Topics (numbers 3–84)
# Each entry: what the questioner is thinking about (without speaking)
# ---------------------------------------------------------------------------
MOOK_PRASHNA_TOPICS: dict[int, dict] = {
    3:  {
        "topic": "Self / Illness / Anger / Quarrel",
        "topic_hi": "स्वयं के बारे में / बीमारी, ज्वर, रोग / क्रोध या झगड़ा",
        "detail": "You are thinking about yourself — health issues, fever, disease, anger, or a fight/conflict.",
        "detail_hi": "आप अपने बारे में सोच रहे हैं। किसी बीमारी, ज्वर, रोग, क्रोध या झगड़े के बारे में सोच रहे हैं।",
        "category": "Health & Self",
    },
    4:  {
        "topic": "Family / Love / Heart's Desire",
        "topic_hi": "परिवार / प्रेम / मन की गहरी इच्छा",
        "detail": "A domestic or family matter, love, joy, or something deeply desired from the heart.",
        "detail_hi": "आप किसी घरेलू विषय पर सोच रहे हैं। परिवार, प्रेम, आनन्द, मौज-मस्ती या किसी तीव्र हृदय इच्छा के बारे में।",
        "category": "Family & Love",
    },
    5:  {
        "topic": "Marriage / Partnership / Peace",
        "topic_hi": "विवाह / साझेदारी / शान्ति और सुलह",
        "detail": "Marriage, a contract, partnership, peace, harmony, unity, or reconciling others.",
        "detail_hi": "विवाह, अनुबंध, साझेदारी, शान्ति, एकता और मेल-मिलाप, या दूसरों में सुलह कराने के बारे में।",
        "category": "Relationships",
    },
    6:  {
        "topic": "News / Siblings / Communication / Travel",
        "topic_hi": "समाचार / भाई-बहन / संचार / यात्रा",
        "detail": "News or information, siblings, communication, postal matters, or short travel.",
        "detail_hi": "किसी समाचार, भाई, यात्रा, संचार के साधन, डाक से आने-जाने वाली वस्तु के विषय में।",
        "category": "Communication",
    },
    7:  {
        "topic": "House / Land / Water / Relocation",
        "topic_hi": "मकान / जमीन / जल / स्थानान्तरण",
        "detail": "House, land, underground property, the ocean, a large water body, change, or relocation.",
        "detail_hi": "मकान, जमीन, भूमिगत वस्तु, समुद्र, अपार जल राशि, परिवर्तन या स्थानान्तरण के बारे में।",
        "category": "Property",
    },
    8:  {
        "topic": "Antiques / Foreign / Ancient Things",
        "topic_hi": "प्राचीन वस्तुएं / विदेश / पूर्व दिशा",
        "detail": "Ancient things, antiques, foreign country or objects, east direction, or ancient Indian civilization.",
        "detail_hi": "प्राचीनता, पुरानी वस्तुएं, विदेश या विदेशी वस्तुओं, पूर्व दिशा या प्राचीन भारतीय सभ्यता के बारे में।",
        "category": "Foreign & Ancient",
    },
    9:  {
        "topic": "Death / Business Loss / Wrong Deal",
        "topic_hi": "मृत्यु / व्यापारिक घाटा / गलत अनुबंध",
        "detail": "Someone's death, business loss, damage, or a bad deal and how to fix it.",
        "detail_hi": "किसी की मृत्यु, व्यापारिक घाटा, हानि, नुकसान, या गलत अनुबंध और उसे कैसे ठीक किया जाए।",
        "category": "Loss & Difficulty",
    },
    10: {
        "topic": "Harmful Friendship / Bad Contract / Dispute",
        "topic_hi": "हानिकारक मित्रता / बुरा अनुबंध / झगड़ा",
        "detail": "An unfortunate, harmful friendship, agreement causing loss, or an ongoing dispute.",
        "detail_hi": "दुर्भाग्यपूर्ण, कष्टदायक मित्रता, हानि की संभावना वाला अनुबंध, या हो गया झगड़ा।",
        "category": "Conflict",
    },
    11: {
        "topic": "Mine / Property Valuation / Land",
        "topic_hi": "खान / सम्पत्ति मूल्यांकन / जायदाद",
        "detail": "A mine, house, land, property, or estate valuation.",
        "detail_hi": "किसी खान, मकान, जमीन, जायदाद, सम्पत्ति के मूल्य निर्धारण के बारे में।",
        "category": "Property",
    },
    12: {
        "topic": "Celebration / Party / Luxury",
        "topic_hi": "उत्सव / पार्टी / विलासिता",
        "detail": "A pleasant atmosphere, celebration, party, luxury, fine clothes, or social event.",
        "detail_hi": "खुशनुमा वातावरण, जलसा, उत्सव, आराम, विलासिता की वस्तुएं, उत्तम वस्त्र या पार्टी।",
        "category": "Celebration",
    },
    13: {
        "topic": "Money / Lottery / Urgent Financial Gain",
        "topic_hi": "धन / लॉटरी / तत्काल आर्थिक लाभ",
        "detail": "Money matters, urgent financial gain, gambling, or lottery.",
        "detail_hi": "रुपये पैसे, तत्काल धन लाभ, सट्टा या लॉटरी के बारे में।",
        "category": "Finance",
    },
    14: {
        "topic": "Female Relatives / Short Journey / Overseas News",
        "topic_hi": "स्त्री संबंधी / छोटी यात्रा / विदेश से समाचार",
        "detail": "Female relatives (sister, aunt, grandmother), a short journey, or news from a faraway country.",
        "detail_hi": "किसी स्त्री संबंधी — बहन, चाची, ताई, मामी, दादी, नानी; छोटी यात्रा या विदेश से आने वाले संवाद।",
        "category": "Family & Travel",
    },
    15: {
        "topic": "Death / Bad News / Loss / Misfortune",
        "topic_hi": "मृत्यु / बुरी खबर / हानि / दुर्भाग्य",
        "detail": "Death or sorrow news, distressing information, financial loss, or misfortune.",
        "detail_hi": "किसी की मृत्यु, दुःख का समाचार, कष्टप्रद खबर, घाटा, हानि या दुर्भाग्य।",
        "category": "Loss & Difficulty",
    },
    16: {
        "topic": "Good News / Beneficial Agreement / Wife",
        "topic_hi": "शुभ समाचार / लाभदायक अनुबंध / पत्नी",
        "detail": "Good auspicious news, a beneficial contact or agreement, or matters concerning your wife.",
        "detail_hi": "शुभ समाचार, लाभप्रद सम्पर्क, अच्छा सुखदायक अनुबंध, समझौता या पत्नी के बाबत।",
        "category": "Good Fortune",
    },
    17: {
        "topic": "Disease / Servant / Happy Journey / Family",
        "topic_hi": "रोग / नौकर / हर्षदायक यात्रा / कुटुम्ब",
        "detail": "Disease, hardship, servant matters, OR a happy journey, love, desired message, family work.",
        "detail_hi": "किसी रोग, तकलीफ, नौकर; या किसी हर्षदायक यात्रा, प्रेम, इच्छित संदेश प्राप्ति, कुटुम्ब कार्य।",
        "category": "Health & Family",
    },
    18: {
        "topic": "Happy Journey / Love / Desired Message / Gold",
        "topic_hi": "हर्षदायक यात्रा / प्रेम / इच्छित संदेश / सुवर्ण",
        "detail": "A happy journey, love, joy, receiving a desired message, gold/salary, or family work.",
        "detail_hi": "हर्षदायक यात्रा, प्रेम, हर्ष, इच्छित संदेश प्राप्ति, सुवर्ण भाता या कुटुम्ब कार्य।",
        "category": "Joy & Travel",
    },
    19: {
        "topic": "Work Obstruction / Hospital / Jail / Lost Child",
        "topic_hi": "कार्य में रुकावट / अस्पताल / जेल / बच्चा",
        "detail": "Work stoppage, solitude, hospital/nursing home stay, jail, punishment, or a lost child.",
        "detail_hi": "काम में रुकावट, एकान्तवास, अस्पताल या नर्सिंग होम, जेल, सजा या किसी बचे के बारे में।",
        "category": "Difficulty",
    },
    20: {
        "topic": "Journey / Letter / Transport / Road",
        "topic_hi": "यात्रा / पत्र / परिवहन / रास्ता",
        "detail": "A journey, letter, correspondence, transporting items, or a road-related question.",
        "detail_hi": "यात्रा, पत्र, पत्र व्यवहार, वस्तु के लाने-ले जाने या रास्ते से संबंधित प्रश्न।",
        "category": "Travel & Communication",
    },
    21: {
        "topic": "Financial Gain / Silver / White Items",
        "topic_hi": "आर्थिक लाभ / चाँदी / सफेद वस्तु",
        "detail": "Some financial gain, money, items in your possession, silver objects, or white things.",
        "detail_hi": "आर्थिक लाभ, रुपया-पैसा, अपने पास होने वाली वस्तुओं, चाँदी की चीज या सफेद वस्तु के बारे में।",
        "category": "Finance",
    },
    22: {
        "topic": "Unwanted Marriage / Sick Partner / Enemy",
        "topic_hi": "अनिच्छित विवाह / बीमार साथी / शत्रु",
        "detail": "An unwanted or adverse marriage, sick partner/husband/wife, enemy, or difficult contract.",
        "detail_hi": "इच्छा के प्रतिकूल विवाह, बीमार साझेदार या पति-पत्नी, शत्रु, कठिनाइयाँ या प्रतिकूल अनुबंध।",
        "category": "Relationships",
    },
    23: {
        "topic": "Good Living / Fine Clothes / Health / Comfort",
        "topic_hi": "सुखद जीवन / अच्छे वस्त्र / स्वास्थ्य / आराम",
        "detail": "Good affluent living, fine clothes, good food, loyal servants, good position, or good health.",
        "detail_hi": "अच्छी सम्पन्न स्थिति, अच्छे कपड़े, उत्तम भोजन, स्वामिभक्त नौकर, अच्छा पद, आराम, यश, स्वास्थ्य।",
        "category": "Comfort & Prosperity",
    },
    24: {
        "topic": "Unstable Situation / Family Quarrel / Children / Secret Love",
        "topic_hi": "डाँवाडोल स्थिति / कुटुम्ब कलह / बच्चे / गुप्त प्रेम",
        "detail": "An unstable situation, family quarrel, a new venture with obstacles, children, or secret love.",
        "detail_hi": "डाँवाडोल स्थिति, कुटुम्ब की कलह, बाधाओं वाला नया काम, बच्चों के बारे में या गुप्त प्रेम।",
        "category": "Family",
    },
    25: {
        "topic": "Excessive Profit / Gold / Sun / Wealth",
        "topic_hi": "अत्यधिक लाभ / सुवर्ण / सूर्य / सम्पत्ति",
        "detail": "Excessive profit, abundant wealth, gold, the sun, or shiny objects.",
        "detail_hi": "अत्यधिक लाभ, प्रचुर सम्पत्ति, सुवर्ण, धन दौलत, सूर्य या किसी चमकीली वस्तु के बारे में।",
        "category": "Wealth",
    },
    26: {
        "topic": "Peaceful Rights / Good Property / Plot / House",
        "topic_hi": "शान्तिपूर्वक अधिकार / अच्छी जायदाद / मकान / प्लॉट",
        "detail": "Peacefully gaining rights to something, good property, house, foundation, flat ground, or plot.",
        "detail_hi": "शान्तिपूर्वक अधिकार प्राप्त करना, अच्छी जायदाद, मकान, बुनियाद, समतल भूमि, प्लॉट।",
        "category": "Property",
    },
    27: {
        "topic": "Closed Room / Boat Journey / Brother / Letter / New Moon",
        "topic_hi": "बन्द कमरा / नाव यात्रा / भाई / पत्र / नया चन्द्रमा",
        "detail": "A closed room, short boat journey, brother or close relative, letter/correspondence, silver object, or new moon.",
        "detail_hi": "बन्द कमरा, नाव यात्रा, भाई या निकट संबंधी, पत्र, सफेद/चाँदी वस्तु, या नया चन्द्रमा।",
        "category": "Travel & Family",
    },
    28: {
        "topic": "Imagination / New Moon / White/Silver Objects",
        "topic_hi": "कल्पना / नया चन्द्रमा / सफेद-चाँदी वस्तु",
        "detail": "Imagination, a new moon phase, white cloth, cup-shaped objects, or silver items.",
        "detail_hi": "अपनी कल्पना, सफेद कपड़ा, प्यालानुमा वस्तु, चाँदी की वस्तु या नये चन्द्रमा के बारे में।",
        "category": "Spiritual",
    },
    29: {
        "topic": "Poor Health / Poverty / Blood Disorder / Struggle",
        "topic_hi": "खराब स्वास्थ्य / गरीबी / रक्त विकार / संघर्ष",
        "detail": "Poor health, poverty, difficult circumstances, blood disorder, disease, or a struggling life.",
        "detail_hi": "अस्वास्थ्य, खराब तन्दुरुस्ती, गरीबी, कठिनाइयाँ, रक्त विकार, बीमारी या संघर्षमय जीवन।",
        "category": "Health & Difficulty",
    },
    30: {
        "topic": "Children's Joy / Inheritance / Reunion",
        "topic_hi": "बच्चों की खुशी / विरासत / मेलमिलाप",
        "detail": "Children's happiness, joyful experience, good dowry, inherited wealth, reunion, or organization.",
        "detail_hi": "बच्चों की प्रसन्नता, आनन्ददायक अनुभव, अच्छा दहेज या विरासत में धन, मेलमिलाप या संघ।",
        "category": "Family & Joy",
    },
    31: {
        "topic": "Underground Things / Reptiles in House / Foreign",
        "topic_hi": "भूमिगत वस्तु / घर में जीव-जन्तु / विदेश",
        "detail": "Underground things, snakes/scorpions/animals in the house, or foreign matters.",
        "detail_hi": "जमीन के नीचे भूगर्भ में वस्तु, मकान में सर्प, बिच्छू या अन्य जानवर, या विदेश के बारे में।",
        "category": "Foreign & Hidden",
    },
    32: {
        "topic": "King / Government / Gold Investment / Personality",
        "topic_hi": "राजा / सरकार / सुवर्ण निवेश / व्यक्तित्व",
        "detail": "A king, ruler, government, gold or good investment, or your own personality and character.",
        "detail_hi": "बादशाह, राजा या सरकार, स्वर्ण या अच्छी जगह धन लगाना, या अपने व्यक्तित्व व चरित्र से संबंधित।",
        "category": "Authority & Wealth",
    },
    33: {
        "topic": "Happy News / Good Position / Achievement / Brother",
        "topic_hi": "हर्षदायक समाचार / अच्छा पद / उपलब्धि / भाई",
        "detail": "Happy news, a good position, a specific achievement or accomplishment, or a brother.",
        "detail_hi": "हर्षदायक समाचार, अच्छे पद या स्थिति, किसी विशिष्ट उपलब्धि या किसी भाई के विषय में।",
        "category": "Success",
    },
    34: {
        "topic": "Financial Gain / Food / Daily Necessities / Purchase",
        "topic_hi": "आर्थिक लाभ / भोजन / दैनिक आवश्यकताएं / खरीद",
        "detail": "Financial gain, food, grain, daily necessities, a purchase, or physical/material benefit.",
        "detail_hi": "आर्थिक लाभ, भोजन, अन्न, रोजमर्रा की जरूरतें, खरीद या किसी शारीरिक-भौतिक लाभ के बारे में।",
        "category": "Finance & Daily Life",
    },
    35: {
        "topic": "Woman / Child Birth / Secret Plan / Solitude",
        "topic_hi": "स्त्री / बालक का जन्म / गुप्त योजना / एकान्तवास",
        "detail": "A woman, child birth (boy or girl), a secret plan or conspiracy, or your own secret/solitude.",
        "detail_hi": "किसी स्त्री, बालक का जन्म (लड़का या लड़की), गुप्त योजना या षड्यन्त्र, या अपनी गुप्त बात/एकान्तवास।",
        "category": "Family & Secrets",
    },
    36: {
        "topic": "Gambling Loss / Sick Child / Family Suffering",
        "topic_hi": "सट्टे में हानि / बीमार बच्चा / परिवार का दुःख",
        "detail": "Loss in gambling or job, sick child, a sad family situation, suffering, or difficulties.",
        "detail_hi": "सट्टे या रोजगार में हानि, बीमार बच्चा, दुःखदायक घरेलू स्थिति, दुःख, कष्ट और कठिनाइयाँ।",
        "category": "Difficulty",
    },
    37: {
        "topic": "Failed Contract / Unhappy Marriage / Property",
        "topic_hi": "असफल अनुबंध / दुखी विवाह / मकान-जायदाद",
        "detail": "A contract with bad outcome, an unsuccessful marriage or unhappy married life, house or property.",
        "detail_hi": "बुरे परिणाम वाला अनुबंध, खराब परिणाम वाला विवाह, सुखी वैवाहिक जीवन न रहना, मकान या जायदाद।",
        "category": "Relationships & Property",
    },
    38: {
        "topic": "Fever / Illness / Nearby Water Body / Sister",
        "topic_hi": "बुखार / मलेरिया / निकट जलाशय / बहन",
        "detail": "Fever, malaria, illness, death, a nearby water body, receiving news/travel, or a sister.",
        "detail_hi": "बुखार, मलेरिया, शारीरिक कष्ट या मृत्यु, पास के तालाब या जलाशय, यात्रा, संवाद या बहन।",
        "category": "Health",
    },
    39: {
        "topic": "Closed Place / Temple / Going Out / Eviction",
        "topic_hi": "बन्द जगह / मन्दिर / बाहर जाना / निष्कासन",
        "detail": "A closed place or temple, palace, cinema, glittering building, going out, eviction, or travel.",
        "detail_hi": "बन्द जगह या मन्दिर, राज-भवन, सिनेमा, चमकीला भवन, बाहर जाना, निष्कासन या प्रवास।",
        "category": "Travel & Spiritual",
    },
    40: {
        "topic": "Valuables / Jewelry / Clothes / Grain Prices",
        "topic_hi": "बहुमूल्य वस्तुएं / जेवलरी / वस्त्र / अन्न मूल्य",
        "detail": "Valuable items, jewelry, clothes, money, or grain/food prices.",
        "detail_hi": "बहुमूल्य वस्तुओं, जवाहरात, जेवलरी, पहनने के वस्त्र, धन या अन्न के मूल्यों के बारे में।",
        "category": "Wealth & Possessions",
    },
    41: {
        "topic": "Self — Dress / Food / Reputation / Fame",
        "topic_hi": "स्वयं — पोशाक / भोजन / प्रतिष्ठा / नेकनामी",
        "detail": "About yourself — your dress, food, current position, reputation, good or bad fame.",
        "detail_hi": "अपने स्वयं के बारे में — पोशाक, भोजन, स्थिति, नेकनामी, बदनामी, साख या प्रतिष्ठा।",
        "category": "Self",
    },
    42: {
        "topic": "High-Position Woman / Official's Favor / Large Crowd",
        "topic_hi": "उच्च पदस्थ महिला / अधिकारी की कृपा / जनसमूह",
        "detail": "A friend or high-position woman, a high official's favor, a large crowd, fair, or gathering.",
        "detail_hi": "किसी मित्र या उच्च पद की महिला, उच्च पदाधिकारी की अनुकंपा, विशाल जनसमूह, मेला या सभा।",
        "category": "Social & Authority",
    },
    43: {
        "topic": "Ancestral Property / Old Building / Minerals / Elder",
        "topic_hi": "पैतृक सम्पत्ति / पुरानी इमारत / खनिज / वृद्ध पुरुष",
        "detail": "Ancestral property, old building, crematorium, mine, minerals, or an elderly man.",
        "detail_hi": "पैतृक सम्पत्ति, पुरानी इमारत, शमशान, खान, खनिज पदार्थ या किसी वृद्ध पुरुष के बारे में।",
        "category": "Property & Elders",
    },
    44: {
        "topic": "Brother / Health / Religious Texts / Overseas Letter",
        "topic_hi": "भाई / स्वास्थ्य / धार्मिक ग्रन्थ / विदेश से पत्र",
        "detail": "A brother, health, comfort items, religious texts, scriptures, or a letter from overseas.",
        "detail_hi": "भाई, स्वास्थ्य, आराम की वस्तुएं, धार्मिक ग्रन्थ, शास्त्र या समुद्रपार से आने वाला पत्र।",
        "category": "Family & Spiritual",
    },
    45: {
        "topic": "Marriage / Fraud / Injustice / Cheap Items",
        "topic_hi": "विवाह / धोखाधड़ी / अन्याय / कम मूल्य की वस्तु",
        "detail": "Marriage, profit/loss, fraud, bias, injustice, or a low-value item.",
        "detail_hi": "विवाह, लाभ-हानि, धोखाधड़ी, पक्षपात, असमानता, अन्याय या किसी कम मूल्य की वस्तु।",
        "category": "Relationships",
    },
    46: {
        "topic": "Friend / High Official / Gold / Jewelry / Valuables",
        "topic_hi": "मित्र / उच्च पदाधिकारी / सोना / जेवलरी / बहुमूल्य वस्तु",
        "detail": "A friend or high official, gold items, a ring, jewelry, or any valuable item.",
        "detail_hi": "किसी मित्र या उच्च पदाधिकारी, सोने की वस्तु, अंगूठी, जवाहरात या बहुमूल्य वस्तु के बारे में।",
        "category": "Wealth & Social",
    },
    47: {
        "topic": "Self / Justice / Lawsuit / Peace / Death",
        "topic_hi": "स्वयं / न्याय / मुकदमा / शान्ति / मृत्यु",
        "detail": "About yourself — justice, a lawsuit, measurement, satisfaction, peace, comfort, or death.",
        "detail_hi": "स्वयं के बारे में — न्याय, मुकदमा, नाप-तौल, संतोष, आराम या मृत्यु के बारे में।",
        "category": "Self & Justice",
    },
    48: {
        "topic": "Inner Rooms / Hidden Servant / Woman's Health / Distant Message",
        "topic_hi": "घर के भीतरी हिस्से / छिपे नौकर / महिला स्वास्थ्य / दूर से संवाद",
        "detail": "Clothing, beauty parlor, inner rooms of the house, a hidden servant, woman's health, or a distant message.",
        "detail_hi": "पोशाक, श्रृंगार गृह, भवन के अन्दरुनी हिस्से, छिपे या भागे नौकर, महिला स्वास्थ्य, या दूर से संवाद।",
        "category": "Home & Health",
    },
    49: {
        "topic": "Change of Position / Mother / Queen / High-Position Woman",
        "topic_hi": "पद/स्थान परिवर्तन / माता / रानी / उच्चपदस्थ महिला",
        "detail": "Change of position or place, your mother, a specific object, a queen, or high-position woman.",
        "detail_hi": "पद परिवर्तन या स्थान परिवर्तन, अपनी माता, किसी विशिष्ट वस्तु, रानी या उच्च पदस्थ महिला।",
        "category": "Change & Women",
    },
    50: {
        "topic": "Difficult Journey / Distressed Sister / Sad News",
        "topic_hi": "कष्टदायक यात्रा / कष्ट में बहन / दुखद समाचार",
        "detail": "A difficult journey, a sister in distress, duty call, summons, or sad news.",
        "detail_hi": "कष्टदायक यात्रा, कष्ट में पड़ी बहन, कर्तव्य की पुकार, बुलावा या दुखद समाचार।",
        "category": "Difficulty & Family",
    },
    51: {
        "topic": "Abundant Financial Gain / Lottery / Children / Money from Afar",
        "topic_hi": "प्रचुर आर्थिक लाभ / सट्टा-लॉटरी / बच्चे / दूर से धन",
        "detail": "Abundant financial gain, a bet, lottery, job, children, or money coming from a distance.",
        "detail_hi": "प्रचुर आर्थिक लाभ, शर्त, सट्टा, लॉटरी, रोजगार, बच्चों के बारे में या दूर से आने वाला धन।",
        "category": "Wealth & Family",
    },
    52: {
        "topic": "Disease / Death / Hidden Item / Doctor / Tantra / Reptiles",
        "topic_hi": "रोग/मृत्यु / छिपी वस्तु / डॉक्टर / तन्त्र / सर्पादि",
        "detail": "Physical disease, death, a lost/hidden item, servant, red cloth, doctor, tantric matters, or reptiles.",
        "detail_hi": "शारीरिक रोग, मृत्यु, खोई-छिपी वस्तु, नौकर, लाल कपड़ा, डॉक्टर, तन्त्र-योग विद्या, सर्प या रेंगने वाले जीव।",
        "category": "Health & Hidden",
    },
    53: {
        "topic": "High Position / Job / King / Lost Gold",
        "topic_hi": "उच्च पद / नौकरी / राजा / खोया सोना",
        "detail": "A high position, job, king or high official, a dead king, or lost gold.",
        "detail_hi": "उच्च पद, नौकरी, राजा या उच्च पदाधिकारी, मृत सिंह या खोये हुए सोने के बारे में।",
        "category": "Authority & Wealth",
    },
    54: {
        "topic": "Infectious Disease / Distressed Woman / Promise / Contract",
        "topic_hi": "संक्रामक रोग / कष्ट में महिला / वायदा / अनुबंध",
        "detail": "Infectious disease, a woman in distress, wife, daughter, a promise, contract, or enclosed space.",
        "detail_hi": "संक्रामक रोग, कष्ट में महिला, पत्नी, कन्या, वायदा, अनुबंध या चार दीवारों के बारे में।",
        "category": "Health & Relationships",
    },
    55: {
        "topic": "Death / Lost Documents / Young Girl / Crowd",
        "topic_hi": "मृत्यु / खोए कागज / नई लड़की / जनसमूह",
        "detail": "Death, lost papers/documents, a misdirected message, a young girl, a crowd, or a friend.",
        "detail_hi": "मृत्यु, खोये कागज या दस्तावेज, गलत जगह संदेश, नई उम्र की लड़की, जनसमूह या मित्र।",
        "category": "Loss",
    },
    56: {
        "topic": "Overseas / Sea Voyage / Religious Conference / Shakti",
        "topic_hi": "विदेश / समुद्रयात्रा / धार्मिक सम्मेलन / शक्ति",
        "detail": "Overseas/foreign matters, sea voyage, religious conference, publication, ship, ghost, or Shakti (Durga, Kali).",
        "detail_hi": "समुद्रपार, विदेश, समुद्रयात्रा, धार्मिक सम्मेलन, प्रकाशन, जहाज, भूत या शक्ति (दुर्गा, काली)।",
        "category": "Spiritual & Foreign",
    },
    57: {
        "topic": "Treasure / Inheritance / Pension / Male Relative",
        "topic_hi": "खजाना / विरासत / पेंशन / पुरुष संबंधी",
        "detail": "A treasure, store, received money, inheritance, pension, or a male relative.",
        "detail_hi": "खजाने, भंडार, प्राप्त धन राशि, विरासत, पेंशन या किसी पुरुष संबंधी के बारे में।",
        "category": "Wealth & Family",
    },
    58: {
        "topic": "Lawyer / Judge / Guru / Scripture / Personal Property",
        "topic_hi": "वकील / जज / गुरु / शास्त्र / व्यक्तिगत जायदाद",
        "detail": "A lawyer, judge, guru, priest, scripture/Veda, personal property, influence, or personal gain.",
        "detail_hi": "वकील, जज, गुरु, पुरोहित, शास्त्र, वेद, ब्राह्मण, व्यक्तिगत जायदाद, प्रभाव या व्यक्तिगत प्राप्ति।",
        "category": "Legal & Spiritual",
    },
    59: {
        "topic": "Hospital / House Fire / Adventure / Industry",
        "topic_hi": "अस्पताल / घर में आग / साहसिक कार्य / उद्योग",
        "detail": "A death house, hospital, patient's room, child, house fire, adventurous work, or industry.",
        "detail_hi": "मृत्यु गृह, अस्पताल, रोगी का कमरा, बच्चा, घर में जलती अग्नि, साहसिक कार्य या उद्योग।",
        "category": "Health & Adventure",
    },
    60: {
        "topic": "Fire Ritual / Sage / God / Time / Foreign King",
        "topic_hi": "हवन / ऋषि / ईश्वर / काल / विदेशी राजा",
        "detail": "A fire worshipper, religious ritual, foreign king, sage, meditative state, Brahma, sky/sun, God, or Time.",
        "detail_hi": "पारसी, अग्नि पूजक, हवनकर्ता, धार्मिक संस्कार, विदेशी राजा, ऋषि, समाधि, ब्रह्मा, आकाश-सूर्य, ईश्वर या काल।",
        "category": "Spiritual & Divine",
    },
    61: {
        "topic": "Food / Trade / Fine Clothes / Market / Brahmin",
        "topic_hi": "भोजन / व्यापार / उत्तम वस्त्र / बाजार / ब्राह्मण",
        "detail": "Food/grain, trade, fine clothes, a male person, friend, market/shop, servant, or Vaishnav Brahmin.",
        "detail_hi": "भोजन, खाद्य पदार्थ, व्यापार, उत्तम वस्त्र, पुरुष, मित्र, व्यापार स्थान, बाजार, नौकर या वैष्णव ब्राह्मण।",
        "category": "Trade & Food",
    },
    62: {
        "topic": "Contract / Legal Action / Property / Father",
        "topic_hi": "अनुबंध / कानूनी कार्यवाही / जायदाद / पिता",
        "detail": "An article or contract, promise, legal action, a position, property, or father-related matters.",
        "detail_hi": "किसी लेख या अनुबंध, वायदे, कानूनी कार्यवाही, पद, जायदाद या पिता से संबंधित प्रश्न।",
        "category": "Legal & Family",
    },
    63: {
        "topic": "Dead Woman / Lost Property / Waning Moon / Dowry",
        "topic_hi": "मृत स्त्री / खोई जायदाद / क्षीण चन्द्रमा / स्त्री-धन",
        "detail": "A dead woman, lost property, shroud, waning moon, woman's dowry/wealth, or bathing.",
        "detail_hi": "मृत स्त्री, खोई जायदाद या वस्तु, कफन, क्षीण चन्द्रमा, स्त्री का दहेज, स्त्री-धन या स्नान।",
        "category": "Grief & Loss",
    },
    64: {
        "topic": "Own Position / Inherited Property / Old Man / Deal / Time",
        "topic_hi": "अपना पद / विरासत / वृद्ध व्यक्ति / सौदा / समय",
        "detail": "Your position, acquired property, inheritance, an old man, a deal/exchange, or a time period.",
        "detail_hi": "अपने पद व स्थिति, प्राप्त जायदाद, विरासत, वृद्ध मनुष्य, सौदा, वस्तुओं की अदला-बदली, समय की अवधि।",
        "category": "Self & Property",
    },
    65: {
        "topic": "Short Journey / Sister / Secret Counsel / Closed Room",
        "topic_hi": "छोटी यात्रा / बहन / गुप्त मंत्रणा / बन्द कमरा",
        "detail": "A short journey and return, coming/going, walking, closed room, pleasant room, sister, mantra, or secret counsel.",
        "detail_hi": "छोटी यात्रा और वापसी, जाना-आना, पैदल यात्रा, बन्द कमरा, बहन, मन्त्र या गुप्त मन्त्रणा।",
        "category": "Travel & Secrets",
    },
    66: {
        "topic": "Crematorium / Mountain / Minerals / Burning House / Sand",
        "topic_hi": "श्मशान / पर्वत / खनिज / जलता घर / रेत",
        "detail": "A crematorium, mountain/hill, mineral, doctor/healer, friend, burning house, dry land, or sand.",
        "detail_hi": "श्मशान, पर्वतीय स्थान, खनिज पदार्थ, वैद्य, मित्र, जलता घर, सूखी भूमि या रेत।",
        "category": "Dark & Earth",
    },
    67: {
        "topic": "Dead King / Lost Gold / Woman's Dowry / Sick Child",
        "topic_hi": "मृत राजा / खोया सोना / स्त्री का दहेज / बीमार बच्चा",
        "detail": "A dead king, lost gold, woman's dowry or waist ornament (mekhala), or a sick child.",
        "detail_hi": "मृत राजा, खोया सोना, स्त्री का दहेज, करधनी (मेखला) या बीमार बच्चे के बारे में।",
        "category": "Grief & Family",
    },
    68: {
        "topic": "Young Girl / Family / Trustworthy Position / Bail",
        "topic_hi": "छोटी उम्र की कन्या / कुटुम्ब / विश्वास योग्य पद / जमानत",
        "detail": "A young girl, family matters, a trustworthy position, or bail/guarantee.",
        "detail_hi": "छोटी, कम उम्र की कन्या, कुटुम्ब संबंधी, विश्वास योग्य पद या जमानत संबंधी प्रश्न।",
        "category": "Family",
    },
    69: {
        "topic": "Clothes / Boat / Merchant Goods / Trade / Science",
        "topic_hi": "वस्त्र / नौका / सौदागरी सामान / व्यापार / विज्ञान",
        "detail": "Clothes, boat/ship, merchant's goods, food items, trade, Vedanga, or science.",
        "detail_hi": "वस्त्र, नौका, जहाज, सौदागरी का सामान, भोजन की वस्तुएं, व्यापार, वेदांग या विज्ञान की वस्तु।",
        "category": "Trade & Travel",
    },
    70: {
        "topic": "Wife / Contract / Public Gathering / Full Moon",
        "topic_hi": "पत्नी / अनुबंध / जनसमूह / पूर्णिमा",
        "detail": "Your wife, a contract, a public gathering place, the full moon, or Purnima.",
        "detail_hi": "पत्नी, अनुबंध, जनता के एकत्र होने का स्थान, पूर्ण चन्द्र या पूर्णमासी के बारे में।",
        "category": "Relationships & Spiritual",
    },
    71: {
        "topic": "Water Pot / Old Familiar Place / Friend / Social Contact",
        "topic_hi": "जलपात्र / पुराना जाना-पहचाना स्थान / मित्र / सम्पर्क",
        "detail": "A water pot, pitcher, an old familiar place or friend, or contacts with other people.",
        "detail_hi": "जलपात्र, कुम्भ, घड़ा, किसी पुराने परिचित स्थान या मित्र, या अन्य लोगों से अपने सम्पर्क।",
        "category": "Social",
    },
    72: {
        "topic": "Money / Rich Friend / Religious Conference / Paired Items",
        "topic_hi": "धन / अमीर मित्र / धार्मिक सम्मेलन / जोड़े वाली वस्तु",
        "detail": "Money, a rich friend, Brahmin, religious conference, or paired items (shoes, scissors, pajama, sandals).",
        "detail_hi": "धन, अमीर मित्र, ब्राह्मण, धार्मिक सम्मेलन, खड़ाऊँ या जोड़े से पूर्ण वस्तु जैसे जूता, कैंची, पाजामा।",
        "category": "Wealth & Spiritual",
    },
    73: {
        "topic": "Brother / Quick Journey / Angry Message / Inheritance / Writing",
        "topic_hi": "भाई / शीघ्र यात्रा / क्रोधयुक्त संदेश / उत्तराधिकार / लेखन",
        "detail": "Brother, a position, ruler's death, quick journey, angry message, honor, inheritance, or writing.",
        "detail_hi": "भाई, पद, शासक की मृत्यु, शीघ्र यात्रा, क्रोधयुक्त संदेश, सम्मान, उत्तराधिकार या लेखन।",
        "category": "Family & Communication",
    },
    74: {
        "topic": "Shining Sun / Proud Wife / Powerful Enemy / Eyes / Shiny Object",
        "topic_hi": "चमकता सूर्य / गर्वीली पत्नी / शक्तिशाली शत्रु / आँखें / चमकीला पदार्थ",
        "detail": "The shining sun, a proud wife, a powerful enemy, hunting, eyesight, or a shiny/glittering substance.",
        "detail_hi": "चमकते सूर्य, गर्विता पत्नी, शक्ति सम्पन्न शत्रु, आखेट-शिकार, आँखों की ज्योति या चमकीले पदार्थ।",
        "category": "Power & Conflict",
    },
    75: {
        "topic": "Pleasant Place / Landlordship / Salvation / Buried Money / Cattle",
        "topic_hi": "खुशनुमा जगह / जमींदारी / मोक्ष / गड़ा धन / पशु",
        "detail": "A pleasant place, landlordship, salvation/moksha, buried money, cattle, or animals.",
        "detail_hi": "खुशनुमा जगह, जमींदारी, मोक्ष, गड़ा धन, मवेशी या पशुओं के बारे में।",
        "category": "Wealth & Spiritual",
    },
    76: {
        "topic": "Son / School / Newly Married Bride / Celibate Youth",
        "topic_hi": "पुत्र / पाठशाला / नव परिणीता वधू / ब्रह्मचारी युवा",
        "detail": "A son, educational institution, school, newly married bride, new daughter-in-law, or celibate youth.",
        "detail_hi": "पुत्र, विद्या स्थान, पाठशाला, स्कूल, नव परिणीता वधू, नई बहू या ब्रह्मचारी कुमार-कुमारी।",
        "category": "Family & Education",
    },
    77: {
        "topic": "Dhoti / Turban / Maid / Medicine / Water / Drinks",
        "topic_hi": "धोती / पगड़ी / नौकरानी / औषधि / जल / पीना-पिलाना",
        "detail": "Dhoti, turban, scarf, a maid, medicine, water, or drinking/beverages.",
        "detail_hi": "धोती, पगड़ी, साफा, नौकरानी, औषधि, जल या पीने-पिलाने के बारे में।",
        "category": "Daily Life",
    },
    78: {
        "topic": "Old Friend / Hospital / Jail / Imprisoned Person",
        "topic_hi": "वृद्ध मित्र / अस्पताल / जेल / बन्धन में व्यक्ति",
        "detail": "An old friend, organization, ancient relationships, hospital, jail, prison, or an imprisoned person.",
        "detail_hi": "वृद्ध मित्र, संस्था, प्राचीन संबंध, अस्पताल, जेल, कारागार या बन्धन में पड़े व्यक्ति।",
        "category": "Difficulty & Social",
    },
    79: {
        "topic": "Self-Growth / Footwear / Prosperity / Judge / Intelligence",
        "topic_hi": "स्वयं की वृद्धि / खड़ाऊँ / उन्नति / जज / बुद्धि",
        "detail": "Self-growth, prosperity, footwear, stairs, advancement, ultimate limit of a thing, judge/lawyer, or intelligence.",
        "detail_hi": "स्वयं की वृद्धि-समृद्धि, पदशक्ति, चरण, खड़ाऊँ, उन्नति-सुख, वस्तु की अन्तिम सीमा, जज, वकील या बुद्धि-ज्ञान।",
        "category": "Growth & Success",
    },
    80: {
        "topic": "Profit-Loss Fear / Fire Damage / Death Abroad / Sea Voyage",
        "topic_hi": "लाभ-हानि की आशंका / अग्नि हानि / विदेश में मृत्यु / समुद्र यात्रा",
        "detail": "Concern about profit/loss, fire damage, foreign land, death far away, or a sea voyage.",
        "detail_hi": "लाभ-हानि की आशंका, अग्नि से हानि, विदेश भूमि, दूर देश में मृत्यु या समुद्र यात्रा।",
        "category": "Risk & Travel",
    },
    81: {
        "topic": "Wealthy Relative / Gold Ornaments / Personal Health / Ripe Fruits",
        "topic_hi": "धनवान रिश्तेदार / सोने के आभूषण / स्वास्थ्य / पके फल",
        "detail": "A wealthy relative, fine clothes, gold ornaments, personal health, or ripe fruits.",
        "detail_hi": "किसी धनवान रिश्तेदार, उत्तम वस्त्र, सोने के आभूषण, व्यक्तिगत स्वास्थ्य या पके फलों के बारे में।",
        "category": "Wealth & Health",
    },
    82: {
        "topic": "Peaceful End / Valuable Dowry / Happy News / Car / Sister",
        "topic_hi": "शान्तिपूर्ण अन्तिम समय / बहुमूल्य दहेज / हर्षदायक समाचार / सवारी / बहन",
        "detail": "Peaceful end times, valuable dowry, happy news, riding an elephant or car, a journey for profit, or a sister.",
        "detail_hi": "शान्तिपूर्ण अन्तिम समय, बहुमूल्य दहेज, हर्षदायक समाचार, हाथी या कार की सवारी, लाभ की यात्रा, या बहन।",
        "category": "Joy & Family",
    },
    83: {
        "topic": "Business Deal / Property Rental / Road / New Daughter-in-law / Engagement",
        "topic_hi": "व्यापार / जायदाद किराया / रास्ता / नई बहू / सगाई",
        "detail": "Business, a deal/contract, property lease or rental, road or gate, new daughter-in-law, or engagement.",
        "detail_hi": "व्यापार, सन्धि, अनुबंध, जायदाद का ठेका या किराया, रास्ता या फाटक, नई बहू या सगाई।",
        "category": "Business & Family",
    },
    84: {
        "topic": "Girl / Pond / Public Festival / Durga / Holiday / Dear Friend",
        "topic_hi": "कन्या / तालाब / जन महोत्सव / दुर्गापूजा / अवकाश / प्रिय मित्र",
        "detail": "A girl/daughter, pond or bathing place, public festival, Durga worship, a holiday, clean cloth, or a dear friend.",
        "detail_hi": "कन्या, तालाब या स्नान स्थान, जन महोत्सव, दुर्गादेवी पूजा, अवकाश, साफ कपड़ा या प्रिय मित्र।",
        "category": "Joy & Spiritual",
    },
}

# ---------------------------------------------------------------------------
# TABLE 2: KHOYI VASTU — Lost Item Locations (numbers 3–84)
# Same number derivation — where to find the lost item
# ---------------------------------------------------------------------------
KHOYI_VASTU_LOCATIONS: dict[int, dict] = {
    3:  {
        "location": "In a corridor, gallery, alleyway, or among papers",
        "location_hi": "रास्ते, गैलरी, गलियारे में या कागजों के मध्य में",
        "hint": "Check passageways and document piles.",
        "hint_hi": "गलियारों और कागजों के ढेर की जाँच करें।",
    },
    4:  {
        "location": "Item is NOT lost — it is in your own possession",
        "location_hi": "वस्तु खोई नहीं है — आपके ही कब्जे में है",
        "hint": "Look more carefully in your own belongings first.",
        "hint_hi": "पहले अपनी चीजों में ध्यान से देखें।",
    },
    5:  {
        "location": "Will be found with a little effort — look under hat, cap, or turban",
        "location_hi": "थोड़ी खोज से मिल जाएगी — टोपी, साफा, पगड़ी, हैट के नीचे देखें",
        "hint": "Check headgear or nearby headwear storage.",
        "hint_hi": "सिर के वस्त्रों के पास या नीचे देखें।",
    },
    6:  {
        "location": "Near shoe rack, exit path — check shelf, sofa, rack, or almirah compartment",
        "location_hi": "चप्पल-जूते रखने की जगह, निकलने के रास्ते में — आले, सोफे, रैक या आलमारी में",
        "hint": "Check near the main door exit area.",
        "hint_hi": "मुख्य द्वार के पास की जगह देखें।",
    },
    7:  {
        "location": "Ask your servant or maid — they know where it is",
        "location_hi": "अपने नौकर या नौकरानी से पता लगाएं",
        "hint": "Your domestic helper has information about this item.",
        "hint_hi": "आपके घर के नौकर को इस वस्तु की जानकारी है।",
    },
    8:  {
        "location": "On top of almirah or balcony — ask a carpenter, artisan, or laborer",
        "location_hi": "आलमारी के ऊपर या बालकनी में — नौकर, कारीगर, मजदूर से तलाश करें",
        "hint": "Check high-up places and ask skilled workers.",
        "hint_hi": "ऊंचे स्थानों पर देखें और कुशल कामगारों से पूछें।",
    },
    9:  {
        "location": "Check in a child's or teenager's clothes or pocket",
        "location_hi": "किसी बालक या किशोर के पास, उसके कपड़े या जेब में देखें",
        "hint": "A child at home has picked it up or knows where it is.",
        "hint_hi": "घर के किसी बच्चे ने इसे उठाया है या उसे पता है।",
    },
    10: {
        "location": "It is in your main room or sitting room",
        "location_hi": "आपके प्रमुख कमरे या बैठक में है",
        "hint": "Search the living/drawing room thoroughly.",
        "hint_hi": "बैठक या ड्राइंग रूम में ध्यान से खोजें।",
    },
    11: {
        "location": "Go near a pond, lake, or water body to search — item is safe",
        "location_hi": "तालाब, जलाशय या पानी के पास जाकर तलाश करें — वस्तु सुरक्षित है",
        "hint": "Also check your workplace, office, books, or papers.",
        "hint_hi": "अपने काम के स्थान, दफ्तर, किताबों या कागजों में भी देखें।",
    },
    12: {
        "location": "Check in office, books, or papers — also where you keep clothes",
        "location_hi": "दफ्तर, किताबों या कागजों में देखें — जहाँ कपड़े रखते हैं वहाँ भी देखें",
        "hint": "Look in work documents and in your clothing storage.",
        "hint_hi": "काम के दस्तावेज और कपड़ों की जगह देखें।",
    },
    13: {
        "location": "Where you keep clothes, shawl, overcoat — also check drain or sewer area",
        "location_hi": "जहाँ कपड़े, शॉल, ओवरकोट रखते हैं — नाली या सीवर भी देखें",
        "hint": "Check clothing storage and outdoor drainage areas.",
        "hint_hi": "कपड़ों की जगह और बाहरी नाली के पास देखें।",
    },
    14: {
        "location": "Under turban/hat/cap — or near a toilet, drain, or sewer",
        "location_hi": "पगड़ी, हैट, टोपी या साफे के नीचे — संडास, नाली, सीवर के पास",
        "hint": "Check headgear and plumbing areas.",
        "hint_hi": "सिर के वस्त्रों के नीचे और पानी-निकासी की जगहों पर देखें।",
    },
    15: {
        "location": "Ask your husband or wife — check garage or stable",
        "location_hi": "पति या पत्नी से पूछें — गैरेज या अस्तबल में देखें",
        "hint": "Your spouse knows or it is in the vehicle storage area.",
        "hint_hi": "आपके जीवनसाथी को पता है या यह गाड़ी रखने की जगह पर है।",
    },
    16: {
        "location": "Ask the cook — check in the kitchen",
        "location_hi": "रसोईया से पता करें — रसोई घर में देखें",
        "hint": "The kitchen or the person who manages it holds the answer.",
        "hint_hi": "रसोई या रसोइया के पास जवाब है।",
    },
    17: {
        "location": "Check in an almirah compartment, rack, safe, or near artistic items",
        "location_hi": "आलमारी या रैक के खाने में, सेफ में, या कलात्मक वस्तुओं के पास देखें",
        "hint": "Look in storage compartments and decorative item areas.",
        "hint_hi": "भंडारण के खानों और सजावटी वस्तुओं के पास देखें।",
    },
    18: {
        "location": "Item is at home and will be found in clothes — also look in a lane or alley",
        "location_hi": "चीज घर में है और कपड़ों में मिलेगी — पगडंडी या गली में भी देखें",
        "hint": "Check your clothes thoroughly and nearby outdoor pathways.",
        "hint_hi": "कपड़ों में ध्यान से देखें और पास की गली में भी देखें।",
    },
    19: {
        "location": "A little far, on dry sandy ground — or forgot where kept; near water or good clothes",
        "location_hi": "थोड़ी दूर सूखी रेतीली जमीन पर — खोई नहीं है; जल के पास या बढ़िया कपड़ों के पास",
        "hint": "Not truly lost — check sandy/dry areas and near good clothing.",
        "hint_hi": "खोई नहीं है — सूखी जगह और अच्छे कपड़ों के पास देखें।",
    },
    20: {
        "location": "Not lost — forgot where you kept it; near water or near good clothes",
        "location_hi": "खोई नहीं है — कहीं रखकर भूल गए हैं; जल के पास या बढ़िया कपड़ों के पास मिलेगी",
        "hint": "Think carefully — you placed it somewhere safe and forgot.",
        "hint_hi": "ध्यान से सोचें — आपने इसे किसी सुरक्षित जगह रखकर भूल गए।",
    },
    21: {
        "location": "Item is with you — check in a box, case, tin, attaché case, or folded container",
        "location_hi": "चीज आपके पास ही है — बक्से, केस, डिब्बे, अटैची, ब्रीफकेस या मोड़कर बन्द डिब्बे में",
        "hint": "Check closed containers in your immediate area.",
        "hint_hi": "अपने आसपास के बन्द बर्तनों और डिब्बों में देखें।",
    },
    22: {
        "location": "On top of an almirah or shelved rack — will be found soon",
        "location_hi": "किसी आलमारी या खानेदार रैक के ऊपर है — जल्दी मिलनी चाहिए",
        "hint": "Check the top surfaces of storage furniture.",
        "hint_hi": "भंडारण के फर्नीचर की ऊपरी सतह देखें।",
    },
    23: {
        "location": "It is nearby — in the room where you keep clothes",
        "location_hi": "पास में है — दूसरे कमरे में जहाँ कपड़े रखते हों वहाँ देखें",
        "hint": "Check your bedroom or dressing room.",
        "hint_hi": "शयन कक्ष या कपड़े रखने के कमरे में देखें।",
    },
    24: {
        "location": "Item is with you — it is not lost",
        "location_hi": "चीज आपके पास ही है — खोई नहीं है",
        "hint": "Search more carefully in your own belongings.",
        "hint_hi": "अपनी चीजों में और ध्यान से देखें।",
    },
    25: {
        "location": "Look in your own belongings — inside a white, round object",
        "location_hi": "अपनी ही चीजों में देखें — किसी सफेद और गोल वस्तु के अन्दर है",
        "hint": "Check inside white containers, bowls, or round items.",
        "hint_hi": "सफेद रंग के गोल बर्तनों या वस्तुओं के अन्दर देखें।",
    },
    26: {
        "location": "Ask an elderly person in the house — they have kept it safely",
        "location_hi": "घर के वयोवृद्ध बुजुर्ग से पूछें — उन्होंने संभाल कर रख दी है",
        "hint": "An older family member has safely stored it for you.",
        "hint_hi": "परिवार के बड़े-बुजुर्ग ने इसे संभालकर रखा है।",
    },
    27: {
        "location": "Search the cowshed, stable, garage, or servant's quarters",
        "location_hi": "गौशाला, घुड़साल, गैरेज में या नौकरों के निवास में खोज करें",
        "hint": "Check outbuildings and domestic worker areas.",
        "hint_hi": "बाहरी कमरों और नौकरों के रहने की जगह देखें।",
    },
    28: {
        "location": "Finding the item is NOT possible — give up hope",
        "location_hi": "खोई वस्तु मिलना संभव नहीं है — आशा छोड़ दें",
        "hint": "The item is permanently lost. Accept it and move forward.",
        "hint_hi": "वस्तु स्थायी रूप से खो गई है। स्वीकार करें और आगे बढ़ें।",
    },
    29: {
        "location": "An elderly person or servant will tell you where it is",
        "location_hi": "किसी वृद्ध पुरुष या नौकर से पता मिलेगा",
        "hint": "Ask older household members or domestic help.",
        "hint_hi": "घर के बड़े सदस्यों या नौकरों से पूछें।",
    },
    30: {
        "location": "Ask children or students — lost during play",
        "location_hi": "बच्चों से या विद्यार्थियों से पूछने से पता मिलेगा — खेल में खोई है",
        "hint": "A child picked it up while playing.",
        "hint_hi": "खेल के दौरान किसी बच्चे ने इसे उठाया है।",
    },
    31: {
        "location": "In a secret room or closed drain — may be found with luck or effort",
        "location_hi": "गुप्त कोठरी या बन्द नाली में है — सौभाग्य से या परिश्रम से मिल सकती है",
        "hint": "Check hidden spaces and closed plumbing areas.",
        "hint_hi": "छिपी जगहों और बन्द नालियों में देखें।",
    },
    32: {
        "location": "Nearby in veranda, on a rock, raised ground, or a rectangular object",
        "location_hi": "पास ही बरामदे में, चट्टान पर, उभरी जमीन पर या आयताकार पदार्थ पर",
        "hint": "Check outdoor seating areas and flat-topped surfaces.",
        "hint_hi": "बाहरी बैठक की जगह और समतल सतहों पर देखें।",
    },
    33: {
        "location": "Item is with you",
        "location_hi": "चीज आपके पास है",
        "hint": "Search your own belongings more carefully.",
        "hint_hi": "अपनी चीजों में और ध्यान से खोजें।",
    },
    34: {
        "location": "Near fire, stove, furnace, or oven — or in main room near fireplace",
        "location_hi": "अग्नि, अंगीठी, चूल्हा, भट्टी, ओवन के पास — या मुख्य कमरे में आग जलाने के स्थान पर",
        "hint": "Item is close by — check kitchen and main room heating areas.",
        "hint_hi": "वस्तु नजदीक है — रसोई और मुख्य कमरे में ताप के स्थान देखें।",
    },
    35: {
        "location": "Near water in a hidden spot, or in husband-wife's private room or near washbasin",
        "location_hi": "पानी के पास छिपे स्थान में, गुप्त स्थान में — पति-पत्नी का निजी कमरा या वाश बेसिन",
        "hint": "Check private bathroom areas and near water sources.",
        "hint_hi": "निजी बाथरूम और पानी के स्रोत के पास देखें।",
    },
    36: {
        "location": "Will be obtained through a nanny, caretaker, or guardian",
        "location_hi": "किसी आया, धाय या अभिभावक के द्वारा प्राप्त होगी",
        "hint": "Ask a caretaker or child's guardian — they have it.",
        "hint_hi": "बच्चों की देखभाल करने वाले से पूछें — उनके पास है।",
    },
    37: {
        "location": "In a holy place — temple, pilgrimage site, or near house compound walls",
        "location_hi": "पवित्र स्थान, मन्दिर, तीर्थ, देवालय, समाधि में — या घर की चारदीवारी के पास",
        "hint": "Check sacred spaces at home or nearby temple areas.",
        "hint_hi": "घर के पवित्र स्थान या पास के मन्दिर में देखें।",
    },
    38: {
        "location": "Where drinking water is stored",
        "location_hi": "पीने का पानी जहाँ रखा जाता है वहाँ मिलेगी",
        "hint": "Check water storage area — matka, water filter, cooler.",
        "hint_hi": "पानी रखने की जगह — मटका, वाटर फिल्टर, कूलर के पास देखें।",
    },
    39: {
        "location": "Consider permanently lost — or will be found in damaged condition",
        "location_hi": "हमेशा के लिये खो गई समझो — या क्षत-विक्षत हालत में मिलेगी",
        "hint": "Very low chance of recovery; if found, may be damaged.",
        "hint_hi": "मिलने की बहुत कम संभावना; मिले तो खराब हालत में होगी।",
    },
    40: {
        "location": "In a two-part container or box",
        "location_hi": "किसी दो भागों वाले पात्र में या बक्से में मिलेगी",
        "hint": "Check dual-compartment containers, tiffin boxes, or divided storage.",
        "hint_hi": "दो भागों वाले डिब्बे, टिफिन या विभाजित भंडारण में देखें।",
    },
    41: {
        "location": "Near a holy bathing place — river, lake, pond, or its surroundings",
        "location_hi": "धार्मिक स्नान स्थल, पवित्र नदी, सरोवर, जलाशय या उसके आसपास",
        "hint": "Check near any water body used for ritual purposes.",
        "hint_hi": "धार्मिक उद्देश्य से उपयोग होने वाले जल निकाय के पास देखें।",
    },
    42: {
        "location": "Check with your partner or spouse — item has changed hands",
        "location_hi": "साझेदार या पति-पत्नी से पता करें — वस्तु एक हाथ से दूसरे हाथ में पहुँच चुकी है",
        "hint": "A family member or partner has it or knows its location.",
        "hint_hi": "परिवार का कोई सदस्य या साथी के पास है या जानता है।",
    },
    43: {
        "location": "Servant has it — will return when asked, explained, or pressured",
        "location_hi": "नौकर के पास है — पूछने, समझाने या दबाव डालने पर लौटा देगा",
        "hint": "A domestic helper accidentally or intentionally took it.",
        "hint_hi": "घरेलू नौकर ने गलती से या जानबूझकर ले लिया है।",
    },
    44: {
        "location": "Among family — search more in children's belongings",
        "location_hi": "घर परिवार के बीच किसी के पास — बच्चों की चीजों में ज्यादा तलाश करें",
        "hint": "A family member (especially a child) has it.",
        "hint_hi": "परिवार के किसी सदस्य (विशेषकर बच्चे) के पास है।",
    },
    45: {
        "location": "Near house wall or compound wall — by rainwater drain, pipe, or water",
        "location_hi": "मकान की दीवार या चारदीवारी के पास — बरसात की नाली, मोरी या पाइप के पास",
        "hint": "Check outdoor walls and drainage pipe areas of the house.",
        "hint_hi": "घर की बाहरी दीवारें और पानी निकासी के पाइप के पास देखें।",
    },
    46: {
        "location": "Where you were or stayed before — go there and search",
        "location_hi": "थोड़ी दूर पर जहाँ आप पहले ठहरे थे — वहाँ जाकर तलाश करें",
        "hint": "Retrace your steps to your previous location.",
        "hint_hi": "अपने पिछले स्थान पर वापस जाकर खोजें।",
    },
    47: {
        "location": "Check near your bag, pockets, tools, instrument, or walking stick",
        "location_hi": "थैले, जेबों, औजार, यन्त्र या छड़ी रखने के स्थान के पास देखें",
        "hint": "Check your everyday carry items and tool storage.",
        "hint_hi": "अपनी रोज की चीजें और औजार रखने की जगह देखें।",
    },
    48: {
        "location": "Under two people's control — hard to get; may already be used or spent",
        "location_hi": "दो व्यक्तियों के अधिकार में — कठिनाई से मिलेगी; खर्च हो चुकी है या उपयोग में",
        "hint": "Two people share custody — difficult recovery; may be already consumed.",
        "hint_hi": "दो लोगों के पास है — मिलना मुश्किल; शायद खर्च हो गई या उपयोग में आ गई।",
    },
    49: {
        "location": "With an old/elderly servant — may be inside food/flour — or hidden by servant",
        "location_hi": "पुराने या वृद्ध नौकर के पास — रोटी, आटे, केक जैसी वस्तु के अन्दर, या नौकर ने छिपाया",
        "hint": "Check food storage areas and ask elderly domestic helpers.",
        "hint_hi": "खाने की जगहें देखें और पुराने नौकरों से पूछें।",
    },
    50: {
        "location": "No hope of finding",
        "location_hi": "मिलने की कोई आशा नहीं है",
        "hint": "Item is permanently gone. Accept the loss.",
        "hint_hi": "वस्तु स्थायी रूप से चली गई है। हानि स्वीकार करें।",
    },
    51: {
        "location": "In the lower part of the house — near shoes, slippers, socks, or drain",
        "location_hi": "घर के नीचे के भाग में — जूते, चप्पल, मोजे, पजामा, पानी की नाली के पास",
        "hint": "Check the ground floor and entryway areas.",
        "hint_hi": "भूतल और प्रवेश द्वार के पास देखें।",
    },
    52: {
        "location": "Gone by hand — will NOT be found",
        "location_hi": "हाथ से गई — नहीं मिलेगी",
        "hint": "Item has left your possession permanently.",
        "hint_hi": "वस्तु हमेशा के लिए चली गई है।",
    },
    53: {
        "location": "You have it — in an old dark place or old junk pile",
        "location_hi": "आपके ही पास है — पुरानी अँधेरी जगह में या पुराने कबाड़ में पड़ी है",
        "hint": "Search old storage areas, attic, or junk collection.",
        "hint_hi": "पुराने भंडारण, अटारी या कबाड़ की जगह में खोजें।",
    },
    54: {
        "location": "In your possession — forgotten; check dark corners or high-up places",
        "location_hi": "आपके कब्जे में — इधर-उधर रखकर भूले; अँधेरे कोनों में और ऊँचे स्थानों पर देखें",
        "hint": "You placed it somewhere high or in a corner and forgot.",
        "hint_hi": "आपने इसे ऊंची जगह या किसी कोने में रखकर भूल गए।",
    },
    55: {
        "location": "Has left your possession — if found, through someone else's help",
        "location_hi": "आपके पास से चली गई है — मिले तो किसी दूसरे की मदद से मिलेगी",
        "hint": "Ask friends or contacts — someone else will locate it.",
        "hint_hi": "मित्रों से पूछें — कोई और इसे ढूंढने में मदद करेगा।",
    },
    56: {
        "location": "Gone due to servants' conspiracy — hard to find; investigate guilty servant",
        "location_hi": "दो नौकरों के षड्यन्त्र से गई — मिलना कठिन; दोषी नौकर की तहकीकात करें",
        "hint": "Likely taken by household staff. Investigate carefully.",
        "hint_hi": "घरेलू कर्मचारियों द्वारा ले जाई गई। सावधानी से जाँच करें।",
    },
    57: {
        "location": "With help of a young person or child — they will find it",
        "location_hi": "किसी नवयुवक या बच्चे की सहायता से मिलेगी",
        "hint": "Ask a young person at home — they know or can help.",
        "hint_hi": "घर के किसी युवा या बच्चे से पूछें — वे जानते हैं या मदद कर सकते हैं।",
    },
    58: {
        "location": "On the roof or upper part of the house — servant will help retrieve it",
        "location_hi": "घर की छत पर या ऊपर के भाग में — नौकर के द्वारा प्राप्त होगी",
        "hint": "Check the terrace and upper floors; a servant has placed it there.",
        "hint_hi": "छत और ऊपरी मंजिल देखें; नौकर ने वहाँ रखा है।",
    },
    59: {
        "location": "Near where you were when you discovered the loss — or near a relative or cup/vessel",
        "location_hi": "जहाँ खोने का पता लगा वहाँ या उसके पास — किसी संबंधी द्वारा या प्याले के पास",
        "hint": "Return to the spot where you first noticed it missing.",
        "hint_hi": "उस जगह पर वापस जाएं जहाँ पहले पता चला कि खो गई है।",
    },
    60: {
        "location": "Where water is stored — look around that area",
        "location_hi": "जहाँ पानी रखा जाता है — वहीं आस-पास देखने से मिल जाएगी",
        "hint": "Check water storage, cooler, matka, or refrigerator area.",
        "hint_hi": "पानी रखने की जगह — कूलर, मटका या फ्रिज के पास देखें।",
    },
    61: {
        "location": "Stand where item was lost — look around — it is right at your feet",
        "location_hi": "जहाँ खोई है वहीं खड़े होकर आसपास देखो — पैरों के पास ही है",
        "hint": "Go back to where you last had it — it's right there.",
        "hint_hi": "जहाँ आखिरी बार था वहाँ जाएं — वहीं है।",
    },
    62: {
        "location": "In a water pot, pitcher, or jug — in your own home",
        "location_hi": "पानी के घड़े, सुराही, जग के पास — आपके ही घर में आपके अधिकार में",
        "hint": "Check water vessels and containers in your home.",
        "hint_hi": "घर के पानी के बर्तनों और घड़ों में देखें।",
    },
    63: {
        "location": "After police investigation it will be found",
        "location_hi": "पुलिस की तहकीकात के बाद मिल जाएगी",
        "hint": "File a complaint — official investigation will recover it.",
        "hint_hi": "शिकायत दर्ज करें — आधिकारिक जाँच से मिलेगी।",
    },
    64: {
        "location": "Your faithful servant will track it down",
        "location_hi": "आपका वफादार नौकर उसका पता लगा देगा",
        "hint": "Trust your most loyal household helper to find it.",
        "hint_hi": "अपने सबसे विश्वासपात्र नौकर पर भरोसा करें — वह ढूंढेगा।",
    },
    65: {
        "location": "In young people's or children's hands — will be found in damaged condition",
        "location_hi": "नवयुवकों या बालकों के हाथ में — क्षत-विक्षत हालत में मिलेगी",
        "hint": "Young people have it; recovery possible but may be damaged.",
        "hint_hi": "युवाओं के पास है; मिल सकती है लेकिन क्षतिग्रस्त हो सकती है।",
    },
    66: {
        "location": "At home in kitchen/storehouse where spices and flour are stored",
        "location_hi": "घर में ही — जहाँ मसाले, आटा आदि रखे जाते हैं, रसोई भंडारगृह में",
        "hint": "Check kitchen storage and pantry shelves.",
        "hint_hi": "रसोई और भंडारगृह की अलमारियाँ देखें।",
    },
    67: {
        "location": "A little far — some servant will bring it to you",
        "location_hi": "कुछ दूर पर है — कोई नौकर उसे लेकर आपके पास आएगा",
        "hint": "Wait — a household helper will bring it back to you.",
        "hint_hi": "प्रतीक्षा करें — कोई नौकर इसे आपके पास लेकर आएगा।",
    },
    68: {
        "location": "A little far near cattle (cows/bulls) — low hope; may be destroyed",
        "location_hi": "कुछ दूर पर गाय-बैलों के पास — मिलने की आशा कम; नष्ट हो सकती है",
        "hint": "Check livestock areas; recovery is uncertain.",
        "hint_hi": "पशुओं के पास देखें; मिलना अनिश्चित है।",
    },
    69: {
        "location": "In your home, in iron or steel vessels",
        "location_hi": "आपके घर में — लोहे या स्टील के पात्रों में",
        "hint": "Check steel/iron containers, pots, or boxes in your home.",
        "hint_hi": "घर में लोहे या स्टील के बर्तनों और डिब्बों में देखें।",
    },
    70: {
        "location": "In your clothes or covering — will be found",
        "location_hi": "पहनने, ओढ़ने के कपड़ों में — मिल जाएगी",
        "hint": "Check your clothes, blankets, or bed sheets carefully.",
        "hint_hi": "कपड़ों, कम्बल और चादरों में ध्यान से देखें।",
    },
    71: {
        "location": "In the kitchen dining area — ask the cook and keep watch",
        "location_hi": "रसोई में खाना खाने के स्थान पर — रसोईये से पूछो, निगाह रखो",
        "hint": "Check the dining area and kitchen — ask the cook.",
        "hint_hi": "भोजन स्थल और रसोई देखें — रसोइया से पूछें।",
    },
    72: {
        "location": "A young unmarried girl will locate it — she is nearby with it",
        "location_hi": "कुमारी कन्या या नवयुवती पता लगाकर देगी — उसके पास में है",
        "hint": "A young woman at home knows where it is.",
        "hint_hi": "घर की कोई युवती जानती है — उससे पूछें।",
    },
    73: {
        "location": "At home in a box, trunk, case, or two-part container like tiffin carrier",
        "location_hi": "घर में ही — बक्से, संदूक, केस, डिब्बे में या दो भागों वाले पात्र, टिफिन कैरियर में",
        "hint": "Check trunks, closed boxes, and tiffin-style containers.",
        "hint_hi": "बक्से, संदूक और टिफिन जैसे बन्द बर्तनों में देखें।",
    },
    74: {
        "location": "Your faithful servant will track it down",
        "location_hi": "आपका वफादार नौकर उसका पता लगा देगा",
        "hint": "Trust your most loyal household helper — they will find it.",
        "hint_hi": "सबसे विश्वासपात्र नौकर पर भरोसा करें — वह ढूंढेगा।",
    },
    75: {
        "location": "In young people's or children's hands — found in damaged condition",
        "location_hi": "नवयुवकों या बालकों के हाथ में — क्षत-विक्षत हालत में मिलेगी",
        "hint": "Young people have it; may be damaged when recovered.",
        "hint_hi": "युवाओं के पास है; मिलेगी लेकिन क्षतिग्रस्त हो सकती है।",
    },
    76: {
        "location": "At home where spices and flour are stored — kitchen storehouse",
        "location_hi": "घर में जहाँ मसाले, आटा रखे जाते हैं — रसोई भंडारगृह में",
        "hint": "Search kitchen pantry and dry goods storage.",
        "hint_hi": "रसोई का भंडारगृह और सूखे सामान की जगह देखें।",
    },
    77: {
        "location": "A little far — some servant will bring it to you",
        "location_hi": "कुछ दूर पर — कोई नौकर उसे लेकर आपके पास आएगा",
        "hint": "It will return to you through a helper.",
        "hint_hi": "यह किसी सहायक के माध्यम से आपके पास आएगी।",
    },
    78: {
        "location": "A little far near cattle — very low hope of finding; may be destroyed",
        "location_hi": "कुछ दूर पर गाय-बैलों के पास — मिलने की आशा नहीं; नष्ट हो चुकी है",
        "hint": "Recovery is very unlikely. Accept the loss.",
        "hint_hi": "मिलने की संभावना बहुत कम। हानि स्वीकार करें।",
    },
    79: {
        "location": "In your home, in iron or steel vessels",
        "location_hi": "आपके घर में — लोहे या स्टील के पात्रों में",
        "hint": "Check metal containers, iron boxes, or steel pots.",
        "hint_hi": "धातु के डिब्बे, लोहे के बक्से या स्टील के बर्तनों में देखें।",
    },
    80: {
        "location": "In clothes or covering — in two-shelf box, case, shoes, or socks",
        "location_hi": "पहनने-ओढ़ने के कपड़ों में — दो खानों वाले बक्से, केस, जूते, मोजे में",
        "hint": "Check two-compartment storage and clothing items.",
        "hint_hi": "दो खानों वाले भंडारण और कपड़ों की चीजों में देखें।",
    },
    81: {
        "location": "In the kitchen where food is eaten — ask the cook; keep watch",
        "location_hi": "रसोई में खाना खाने के स्थान पर — रसोईये से पूछो; निगाह रखो",
        "hint": "The dining/kitchen area holds the answer — ask the cook.",
        "hint_hi": "भोजन स्थल या रसोई में जवाब है — रसोइये से पूछें।",
    },
    82: {
        "location": "A young unmarried girl or young woman will locate it — she has it",
        "location_hi": "कुमारी कन्या या नवयुवती पता लगाएगी — उसके पास में है",
        "hint": "Ask a young woman in your household — she knows.",
        "hint_hi": "घर की युवती से पूछें — वह जानती है।",
    },
    83: {
        "location": "At home in a box, trunk, case — or near a water-filled pit; in two-part vessel",
        "location_hi": "घर में बक्से, संदूक, केस में — या पानी से भरे गड्ढे के पास; दो भागों वाले पात्र में",
        "hint": "Check storage boxes and water storage areas.",
        "hint_hi": "भंडारण के बक्सों और पानी रखने की जगहों में देखें।",
    },
    84: {
        "location": "At home in a box/trunk/case — or near a water-filled pit",
        "location_hi": "घर में बक्से, संदूक, केस में — या किसी तालाब या पानी से भरे गड्ढे के पास",
        "hint": "Check closed storage boxes and any water pit or pond nearby.",
        "hint_hi": "बन्द भंडारण बक्से और पास के तालाब या पानी के गड्ढे के पास देखें।",
    },
}


# ---------------------------------------------------------------------------
# CORE COMPUTE FUNCTION
# ---------------------------------------------------------------------------

def compute_mook_number(numbers: list[int]) -> int:
    """
    Sum the 9 numbers written by the person and add 3.
    Result is always in range 3–84.
    """
    total = sum(numbers) + 3
    return max(3, min(84, total))


def calculate_mook_prashna(numbers: list[int]) -> dict:
    """
    Given 9 numbers, compute the mook prashna result.

    Returns:
        dict with derived_number, question_topic, and lost_item_location
    """
    if len(numbers) != 9:
        raise ValueError("Exactly 9 numbers are required")
    if any(not (0 <= n <= 9) for n in numbers):
        raise ValueError("Each number must be between 0 and 9")

    num = compute_mook_number(numbers)
    topic = MOOK_PRASHNA_TOPICS.get(num, MOOK_PRASHNA_TOPICS[9])
    location = KHOYI_VASTU_LOCATIONS.get(num, KHOYI_VASTU_LOCATIONS[9])

    return {
        "numbers_entered": numbers,
        "sum": sum(numbers),
        "derived_number": num,
        "question_topic": topic,
        "lost_item_location": location,
        "method": "Sum of 9 numbers + 3",
        "method_hi": "9 अंकों का योग + 3",
    }
