"""
database_seed_lalkitab.py — Idempotent seed data for Lal Kitab DB tables.

Tables seeded:
  1. nishaniyan_master  — physical/environmental signs for 9 planets × 12 houses (108 rows)
  2. lal_kitab_debts    — 8 karmic debts (Rin) with Hindi text
  3. lk_interpretations — planet-in-house interpretation texts (108 rows)

All inserts use ON CONFLICT DO NOTHING — safe to call multiple times.
"""

import logging

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# TABLE 1: NISHANIYAN MASTER  (9 planets × 12 houses = 108)
# Columns: planet, house, nishani_text, nishani_text_en, category, severity
# ─────────────────────────────────────────────────────────────

LK_NISHANIYAN = [
    # SUN (सूर्य)
    ("sun", 1,  "क्रोधी स्वभाव का होगा। सिर के बाल कम होंगे। बहुत ज़्यादा हिम्मती होगा। पत्नी हमेशा बीमार रहेगी या दब कर रहेगी।",
     "Short-tempered by nature. Hair tends to be sparse. Very courageous. Wife will often be unwell or subdued.", "physical", "moderate"),
    ("sun", 2,  "जातक के परिवार में 2 शादियाँ होंगी। भाई का तलाक़ हो जाता है। परिवार में औरतों की कमी रहेगी।",
     "Two marriages will occur in the family. Brother's marriage may end in divorce. Women will be fewer in the family.", "family", "strong"),
    ("sun", 3,  "पड़ोस का घर उजड़ा होगा या पड़ोसी परेशान होगा। भाइयों और दोस्तों से अनबन रहती है।",
     "Neighbor's house will be empty or neighbor will be in trouble. Disagreements with brothers and friends persist.", "home", "moderate"),
    ("sun", 4,  "जातक मीठे का शौकीन होगा। घर में गच्चक, गुड़, चॉकलेट आएगा।",
     "Native is fond of sweets. Jaggery, gachak, and chocolates frequently come to the home.", "physical", "mild"),
    ("sun", 5,  "पेट हमेशा ख़राब ही रहता है। परिवार में दो शादियाँ ज़रूर होंगी।",
     "Stomach is frequently disturbed. Two marriages will certainly occur in the family.", "physical", "moderate"),
    ("sun", 6,  "जातक का जन्म नानके में होता है या नानके निसर्ग होम के पैसे भरते हैं। गुप्त शत्रु ज़्यादा बनते हैं।",
     "Native is born at maternal grandparents' home or they bear the delivery expenses. Many hidden enemies.", "family", "moderate"),
    ("sun", 7,  "घर में गुड़, गच्चक, चॉकलेट गिफ़्ट आती है। प्रेम विवाह करने के योग।",
     "Jaggery, gachak, chocolates come as gifts at home. Chances of a love marriage.", "home", "moderate"),
    ("sun", 8,  "जातक की पत्नी घर के भेद बाहर बताएगी। मुकदमे में बार बार हार होती है।",
     "Wife will reveal family secrets to others. Repeated defeats in court cases.", "family", "strong"),
    ("sun", 9,  "घर में पीतल के बड़े बर्तन खाली पड़े होंगे। जब भी मकान बदलेगा खुद पे या पिता पे कष्ट आएगा।",
     "Large brass utensils will lie empty at home. Whenever the house changes, hardship comes to self or father.", "home", "moderate"),
    ("sun", 10, "घर में खोटे सिक्के पड़े होंगे। जहाँ काम कम पैसों में हो सकता है यह ज़्यादा पैसे दे के आएगा।",
     "Counterfeit coins will be found at home. Will pay more for work that could be done cheaply.", "home", "moderate"),
    ("sun", 11, "जातक का ससुर जीवित नहीं रहेगा। नेकी करेगा तो बदनामी मिलेगी।",
     "Father-in-law will not survive long. Acts of kindness will bring disrepute.", "family", "strong"),
    ("sun", 12, "जातक को मोबाइल गिफ़्ट मिलता है। उच्च रक्तचाप रहेगा।",
     "Native receives a mobile phone as a gift. High blood pressure is likely.", "physical", "moderate"),

    # MOON (चंद्र)
    ("moon", 1,  "नज़ला जुकाम बहुत जल्दी होता है। घर में एंटीबायऑटिक दवाई होती है। हरी सब्जियाँ खाने का शौकीन।",
     "Prone to colds and sinus issues. Antibiotics often found at home. Fond of eating green vegetables.", "physical", "mild"),
    ("moon", 2,  "भगवान शंकर की मूर्तियाँ और शंख, सर्प, शिवलिंग होंगे। नशे या नींद की दवाई खाता होगा। जली हुई प्रेस या खराब मिक्सी होगी।",
     "Shiva idols, conch shells, and Shivalingas will be in the home. May use intoxicants or sleep medication. A burnt iron or broken mixer in the house.", "home", "moderate"),
    ("moon", 3,  "कमज़ोर दिल का होगा। रिश्तेदारों और भाइयों से अनबन रहती है। माता को नसों की परेशानी होगी।",
     "Emotionally sensitive. Disagreements with relatives and brothers persist. Mother will have nerve-related issues.", "family", "moderate"),
    ("moon", 4,  "बनियान फटी हुई होगी। माता का अपमान करता है। कंजूस होता है।",
     "Undershirt will often be torn. Disrespects mother. Tends to be miserly.", "physical", "strong"),
    ("moon", 5,  "संतान प्रिय होगा। बच्चे धार्मिक और आज्ञाकारी होंगे। पेट में गड़बड़ी होने के योग।",
     "Affectionate toward children. Children will be religious and obedient. Chances of digestive disturbances.", "family", "mild"),
    ("moon", 6,  "माता की सेहत कमज़ोर रहेगी। शत्रु गुप्त होंगे। मानसिक अशांति रहेगी।",
     "Mother's health will be weak. Enemies will be hidden. Mental restlessness will persist.", "physical", "moderate"),
    ("moon", 7,  "पत्नी सुंदर और भावुक होगी। वैवाहिक जीवन में उतार चढ़ाव। पत्नी की सेहत ध्यान देने योग्य।",
     "Wife will be beautiful and emotional. Ups and downs in married life. Wife's health needs attention.", "family", "moderate"),
    ("moon", 8,  "माता को कष्ट होने के योग। अचानक धन लाभ या हानि। गुप्त बातें दूसरों को पता चलेंगी।",
     "Mother may face hardship. Sudden financial gain or loss. Secret matters will become known to others.", "family", "strong"),
    ("moon", 9,  "भाग्य माता के आशीर्वाद पर निर्भर। धार्मिक यात्राओं से लाभ। विदेश से धन आने के योग।",
     "Fortune depends on mother's blessings. Gains from religious travel. Chances of money coming from abroad.", "events", "mild"),
    ("moon", 10, "माता की तरह दयालु और नर्म दिल। व्यापार में उतार चढ़ाव। जनता में लोकप्रियता।",
     "Compassionate and soft-hearted like mother. Fluctuations in business. Popular among the masses.", "physical", "mild"),
    ("moon", 11, "मित्रों से सहायता मिलती रहेगी। बड़ी बहन का योग। पानी और दूध से व्यापार शुभ।",
     "Friends will continue to help. Likely to have an elder sister. Business in water and milk is auspicious.", "events", "mild"),
    ("moon", 12, "विदेश यात्रा के योग। अकेलापन महसूस होगा। खर्च पर नियंत्रण ज़रूरी।",
     "Chances of foreign travel. Will feel loneliness. Expenditure control is necessary.", "events", "moderate"),

    # VENUS (शुक्र)
    ("venus", 1,  "पत्नी बीमार रहती है। जिसपे दिल आ गया उसके लिए जान कुर्बान कर देगा। दिन में भी प्रेम के सपने देखने वाला।",
     "Wife remains unwell. Will sacrifice everything for someone they fall in love with. Daydreams about romance constantly.", "physical", "moderate"),
    ("venus", 2,  "घर शेरमुखी होगा। पत्नी घर की बॉस होगी। नीली जींस और सफेद शर्ट पहनने की आदत या शौकीन।",
     "House will be triangular or sher-mukhi shaped. Wife will be the boss at home. Fond of wearing blue jeans and white shirt.", "home", "moderate"),
    ("venus", 3,  "कला का पुजारी होगा। शत्रुओं से डरने वाला। घर की नौकरानी या पड़ोसन से अत्यधिक नजदीकी।",
     "A devotee of the arts. Tends to fear enemies. Excessive closeness with household help or neighbor.", "physical", "strong"),
    ("venus", 4,  "दो पत्नियों के योग। सुख सुविधाओं का शौकीन। शादी के 4 वर्ष बाद भाग्य उदय होता है।",
     "Chances of two marriages. Very fond of comforts and luxuries. Fortune rises 4 years after marriage.", "family", "strong"),
    ("venus", 5,  "रोमांटिक स्वभाव। संतान सुंदर और गुणी होगी। कला और संगीत में रुचि।",
     "Romantic by nature. Children will be beautiful and virtuous. Interest in arts and music.", "physical", "mild"),
    ("venus", 6,  "स्वास्थ्य में परेशानी। ऋण लेने के योग। विरोधियों से सतर्क रहना होगा।",
     "Health troubles. Prone to taking on debt. Must be cautious of opponents.", "physical", "moderate"),
    ("venus", 7,  "सुंदर और संस्कारी पत्नी। वैवाहिक जीवन सुखद। व्यापारिक साझेदारी से लाभ।",
     "Beautiful and cultured wife. Happy married life. Gains from business partnerships.", "family", "mild"),
    ("venus", 8,  "ससुराल से धन लाभ। गुप्त संबंध बनने के योग। दुर्घटना का भय।",
     "Financial gain from in-laws. Chances of secret relationships. Fear of accidents.", "events", "moderate"),
    ("venus", 9,  "भाग्यशाली। धार्मिक कार्यों में रुचि। विदेश यात्रा से लाभ।",
     "Lucky. Interest in religious activities. Gains from foreign travel.", "events", "mild"),
    ("venus", 10, "कला, फिल्म, फैशन के क्षेत्र में सफलता। सरकार से लाभ। व्यापार में उन्नति।",
     "Success in arts, film, or fashion. Benefits from government. Growth in business.", "events", "mild"),
    ("venus", 11, "मित्रों से सहायता। बड़ी बहन होगी। धन संचय के योग।",
     "Support from friends. Will have an elder sister. Chances of wealth accumulation.", "events", "mild"),
    ("venus", 12, "विदेश में स्थायी निवास का योग। गुप्त प्रेम संबंध। खर्च अधिक होगा।",
     "Chances of permanent settlement abroad. Secret love affairs. Expenditure will be high.", "events", "moderate"),

    # MARS (मंगल)
    ("mars", 1,  "परिवार में कोई यूनीफॉर्म पहन कर काम करने वाला होता है। शरीर को चुस्त दरुस्त रखने वाला। जातक के सिर या माथे पे चोट का निशान होता है।",
     "Someone in the family works in uniform. Physically fit and active. Scar on head or forehead.", "physical", "moderate"),
    ("mars", 2,  "मसालेदार, फास्ट फूड तंदूरी खाने का शौकीन। मीठा बनकर दूसरों को ठगने वाला। सच का साथ देने वाला और सच बोलने वाला।",
     "Fond of spicy, fast food, and tandoori food. Pretends to be sweet-natured while deceiving others. Stands by truth and speaks honestly.", "physical", "moderate"),
    ("mars", 3,  "भाइयों के साथ झगड़े होंगे। साहसी और निडर होगा। दुर्घटनाओं का खतरा रहेगा।",
     "Disputes with brothers. Courageous and fearless. Risk of accidents.", "family", "strong"),
    ("mars", 4,  "माता के साथ झगड़े। घर में आग लगने का खतरा। संपत्ति विवाद के योग।",
     "Disputes with mother. Fire hazard at home. Property dispute chances.", "home", "strong"),
    ("mars", 5,  "पहला बच्चा लड़का होने के योग। संतान सुख में कमी। जुआ सट्टे में नुकसान।",
     "First child likely to be a boy. Less happiness from children. Losses from gambling or speculation.", "family", "moderate"),
    ("mars", 6,  "शत्रुओं पर विजय। शरीर में रक्त संबंधी रोग। सेना, पुलिस में सेवा योग।",
     "Victory over enemies. Blood-related disorders in the body. Good prospects for army or police service.", "physical", "moderate"),
    ("mars", 7,  "मंगली योग। पति-पत्नी में झगड़े। विवाह में देरी या परेशानी।",
     "Manglik yoga. Disputes between husband and wife. Delay or trouble in marriage.", "family", "strong"),
    ("mars", 8,  "अचानक आघात का भय। पैतृक संपत्ति को लेकर विवाद। 28 वर्ष के बाद उन्नति।",
     "Fear of sudden trauma. Dispute over ancestral property. Progress after age 28.", "events", "strong"),
    ("mars", 9,  "पिता के साथ विचार नहीं मिलते। धर्म के प्रति संशय। विदेश यात्रा में बाधाएं।",
     "Does not agree with father. Skeptical about religion. Obstacles in foreign travel.", "family", "moderate"),
    ("mars", 10, "कार्यक्षेत्र में प्रतिस्पर्धा। सरकारी काम में सफलता। इंजीनियरिंग, सेना में करियर।",
     "Competition in the workplace. Success in government work. Career in engineering or armed forces.", "events", "mild"),
    ("mars", 11, "बड़े भाई से विरोध। मित्र विश्वासघात करेंगे। धन लाभ संघर्ष के बाद।",
     "Opposition from elder brother. Friends will betray. Financial gain after struggle.", "family", "moderate"),
    ("mars", 12, "गुप्त शत्रु अधिक। खर्च अनियंत्रित। विदेश में संघर्ष।",
     "Many hidden enemies. Uncontrolled expenses. Struggles abroad.", "events", "strong"),

    # MERCURY (बुध)
    ("mercury", 1,  "परिवार में कोई गायक होगा या खुद बाथरूम सिंगर होगा। जुबान का कच्चा होगा। चापलूस और शरारती होगा।",
     "Someone in the family is a singer or is a bathroom singer. Loose-tongued. Flattering and mischievous.", "physical", "moderate"),
    ("mercury", 2,  "घर में बंद घड़ियाँ, पुराने चश्मे, हरी बोतलें होंगी। दाँत टेढ़े-मेढ़े या एक दूसरे के ऊपर चढ़े हुए होंगे। टूटे हेडफोन या चार्जिंग केबल बेड बॉक्स में होंगी।",
     "Stopped clocks, old spectacles, green bottles found at home. Crooked or overlapping teeth. Broken headphones or charging cables in the bedside drawer.", "home", "moderate"),
    ("mercury", 3,  "पढ़ने-लिखने में कुशल। व्यापारिक बुद्धि तीव्र। भाई-बहनों के साथ मधुर संबंध।",
     "Skilled in reading and writing. Sharp business mind. Harmonious relations with siblings.", "physical", "mild"),
    ("mercury", 4,  "माता पढ़ी-लिखी और बुद्धिमान होगी। घर में किताबें और पढ़ाई का माहौल। संपत्ति को लेकर तर्क-वितर्क।",
     "Mother is educated and intelligent. Books and study atmosphere at home. Arguments over property.", "home", "mild"),
    ("mercury", 5,  "संतान बुद्धिमान और पढ़ी-लिखी होगी। लेखन, शिक्षा, गणित में रुचि। अटकलों से नुकसान।",
     "Children will be intelligent and well-educated. Interest in writing, education, mathematics. Losses from speculation.", "family", "mild"),
    ("mercury", 6,  "बुद्धि से शत्रुओं को हराएगा। चालाकी से काम लेगा। स्वास्थ्य में पेट और त्वचा की परेशानी।",
     "Will defeat enemies with intelligence. Uses cleverness at work. Health issues related to stomach and skin.", "physical", "moderate"),
    ("mercury", 7,  "पत्नी बुद्धिमान और व्यापारिक। साझेदारी में धोखे का भय। विवाह में चालाकी से काम।",
     "Wife is intelligent and business-minded. Risk of betrayal in partnerships. Uses cleverness in marriage matters.", "family", "moderate"),
    ("mercury", 8,  "गुप्त ज्ञान में रुचि। पैतृक संपत्ति में विवाद। जीवनकाल में अचानक परिवर्तन।",
     "Interest in occult knowledge. Dispute over ancestral property. Sudden changes during lifetime.", "events", "moderate"),
    ("mercury", 9,  "लेखन, अध्यापन, ज्योतिष में सफलता। धार्मिक बुद्धि तीव्र। विदेश से ज्ञान प्राप्ति।",
     "Success in writing, teaching, and astrology. Sharp religious intellect. Acquiring knowledge from abroad.", "events", "mild"),
    ("mercury", 10, "व्यापार में सफलता। लेखक, पत्रकार, वकील बनने के योग। बुद्धि से उच्च पद।",
     "Success in business. Chances of becoming writer, journalist, or lawyer. High position through intellect.", "events", "mild"),
    ("mercury", 11, "व्यापारिक मित्र फायदेमंद। बहन का विशेष सहयोग। आय के अनेक स्रोत।",
     "Business-minded friends are beneficial. Special support from sister. Multiple sources of income.", "events", "mild"),
    ("mercury", 12, "विदेश में बसने के योग। गुप्त अध्ययन में रुचि। खर्च पर नियंत्रण ज़रूरी।",
     "Chances of settling abroad. Interest in secret studies. Expenditure control is necessary.", "events", "mild"),

    # JUPITER (बृहस्पति)
    ("jupiter", 1,  "जातक अमीर बनाता है। शिक्षा भले ही कम हो फिर भी पड़े लिखों का बाप होगा। जातक स्वस्थ रहेगा और दुश्मनों से कभी नहीं डरेगा।",
     "Native becomes wealthy. Even with less education will be wiser than the educated. Healthy and fearless of enemies.", "physical", "mild"),
    ("jupiter", 2,  "घर के बाहर सड़क टूटी होगी या गटर का ढक्कन होगा। घर की दीवारें रंग बिरंगी या पपड़ियाँ उतरी हुई होंगी। गुरु गंटाल योग के बाद भोग या भोग के बाद योग करने वाला।",
     "Road outside home will be broken or have a drain cover. Walls will be multicolored or with peeling paint. Alternates between worldly pleasures and spiritual practice.", "home", "moderate"),
    ("jupiter", 3,  "गद्दे-बिस्तरे को आग लगी हुई या कार की सीट जली हुई। एक ही दिशा में तीन दरवाज़े या तीन खिड़कियाँ। घर में तीन कुकर या पतीले।",
     "Mattress or car seat will be burnt or scorched. Three doors or windows in one direction. Three pressure cookers or pots in the home.", "home", "moderate"),
    ("jupiter", 4,  "घर में किश्ती की फ़ोटो या स्टैचू होगा। घर का कोई बुजुर्ग सन्यासी होगा। माता का चेहरा गोल और तेजवान होगा।",
     "A boat photo or statuette will be in the home. An elderly family member will be a renunciant. Mother's face will be round and radiant.", "home", "mild"),
    ("jupiter", 5,  "दाँत पीले होंगे। घर में कोई टीचर या टीचिंग क्लास देने वाला होगा। कोई ज्योतिषी या धार्मिक इंसान मित्र होगा।",
     "Teeth will be yellowish. A teacher or coaching instructor will be in the family. A friend will be an astrologer or religious person.", "physical", "mild"),
    ("jupiter", 6,  "घर के पास कोई धार्मिक स्थान होगा। जातक शत्रुओं पर भारी रहेगा। गुरु अशुभ हो तो पेट की बीमारियाँ होंगी।",
     "A religious place will be near the home. Will overcome enemies. If Jupiter is malefic, digestive ailments will arise.", "home", "moderate"),
    ("jupiter", 7,  "शादी के बाद किस्मत खुलेगी। पत्नी धार्मिक और संस्कारी होगी। ससुराल में बड़ा मकान या जमीन होगी।",
     "Fortune opens after marriage. Wife will be religious and cultured. In-laws will have a large house or land.", "family", "mild"),
    ("jupiter", 8,  "पारिवारिक संपत्ति विरासत में मिलेगी। 42 साल के बाद उन्नति होगी। गुप्त विद्याओं में रुचि होगी।",
     "Ancestral property will be inherited. Progress after age 42. Interest in occult sciences.", "events", "moderate"),
    ("jupiter", 9,  "भाग्य उज्ज्वल होगा। धार्मिक यात्राओं से लाभ। बड़े लोगों का आशीर्वाद मिलता रहेगा।",
     "Fortune will be bright. Gain from religious travel. Blessings of elders will continue.", "events", "mild"),
    ("jupiter", 10, "सरकारी या बड़े पद पर होगा। यश और कीर्ति मिलेगी। पिता का व्यवसाय आगे बढ़ाएगा।",
     "Will hold government or senior position. Fame and renown. Will carry forward father's business.", "events", "mild"),
    ("jupiter", 11, "बड़े भाई या बहन की मदद से उन्नति होगी। मित्रों का दायरा बड़ा होगा। लाभ के अनेक स्रोत होंगे।",
     "Progress with help of elder sibling. Wide circle of friends. Multiple sources of income.", "events", "mild"),
    ("jupiter", 12, "विदेश यात्रा का योग। आध्यात्मिक जीवन की ओर झुकाव। खर्च अधिक होगा लेकिन धर्म के काम में।",
     "Chance of foreign travel. Inclination toward spiritual life. High expenses but in religious work.", "events", "mild"),

    # SATURN (शनि)
    ("saturn", 1,  "घर में शराब रखी होगी। नज़र कमज़ोर और क्रोधी स्वभाव का होगा। अपने राज़ किसी को आसानी से न बतायेगा।",
     "Alcohol will be kept at home. Weak eyesight and irritable temperament. Will not easily reveal personal secrets.", "home", "strong"),
    ("saturn", 2,  "अधूरी पढ़ाई। पत्नी चालाक होगी। छत से गिरने या सिर पे चोट लगने के योग।",
     "Incomplete education. Wife will be cunning. Chances of falling from roof or head injury.", "physical", "strong"),
    ("saturn", 3,  "भाइयों से विरोध। कड़ी मेहनत के बाद सफलता। यात्राओं में बाधाएं।",
     "Opposition from brothers. Success only after hard work. Obstacles in journeys.", "family", "moderate"),
    ("saturn", 4,  "माता को कष्ट। मकान में देरी। पुराना मकान या जमीन होगी।",
     "Hardship to mother. Delay in owning a home. Old house or land will be there.", "home", "strong"),
    ("saturn", 5,  "संतान सुख में विलंब। पहली संतान कष्ट में। शिक्षा में रुकावट।",
     "Late child happiness. First child in distress. Obstacles in education.", "family", "strong"),
    ("saturn", 6,  "शत्रुओं पर विजय देर से मिलेगी। दीर्घकालीन रोग। नौकरों से परेशानी।",
     "Victory over enemies will come late. Chronic illness. Troubles from servants.", "physical", "moderate"),
    ("saturn", 7,  "विवाह में देरी। पत्नी बड़ी उम्र की। वैवाहिक जीवन में संघर्ष।",
     "Late marriage. Wife will be older. Struggle in married life.", "family", "strong"),
    ("saturn", 8,  "दीर्घायु। पैतृक संपत्ति में विवाद। 36 वर्ष के बाद उन्नति।",
     "Long life. Dispute over ancestral property. Progress after age 36.", "events", "moderate"),
    ("saturn", 9,  "पिता को कष्ट। धर्म के प्रति उदासीनता। किस्मत देर से जागेगी।",
     "Hardship to father. Indifferent toward religion. Fortune will awaken late.", "family", "strong"),
    ("saturn", 10, "उच्च पद देर से मिलेगा। कड़ी मेहनत से सफलता। पदावनति का भय।",
     "Senior position will come late. Success through hard work. Fear of demotion.", "events", "moderate"),
    ("saturn", 11, "बड़े भाई को कष्ट। मित्रों से धोखे का भय। धन संचय धीरे-धीरे।",
     "Elder brother in difficulty. Risk of betrayal by friends. Wealth accumulation is slow.", "family", "moderate"),
    ("saturn", 12, "जेल, अस्पताल, विदेश का योग। एकांतवास की इच्छा। गुप्त शत्रु अधिक।",
     "Chances of prison, hospital, or foreign country. Desire for seclusion. Many hidden enemies.", "events", "strong"),

    # RAHU (राहु)
    ("rahu", 1,  "कभी एक जगह टिक के काम नहीं करेगा। दो शादियों के योग। बहुत ज़्यादा और खामखां बोलने वाला।",
     "Will never settle in one place for long. Chances of two marriages. Talks excessively and unnecessarily.", "physical", "strong"),
    ("rahu", 2,  "घर से एक बार ज़रूर भागेगा। घर में दिन में चोरी हो सकती है। नेत्र रोगी और माता या बीवी का अपमान करने वाला।",
     "Will run away from home at least once. Day-time theft can happen at home. Suffers from eye disease; disrespects mother or wife.", "events", "strong"),
    ("rahu", 3,  "भाइयों से अनबन। झूठ बोलने की आदत। यात्राओं से धन हानि।",
     "Disputes with brothers. Habit of lying. Financial losses from travel.", "family", "strong"),
    ("rahu", 4,  "माता का अचानक स्वास्थ्य बिगड़ना। घर में बार-बार परिवर्तन। संपत्ति विवाद।",
     "Mother's health may deteriorate suddenly. Frequent changes in home. Property disputes.", "home", "strong"),
    ("rahu", 5,  "संतान को कष्ट। जुआ-सट्टे में नुकसान। प्रेम संबंधों में धोखा।",
     "Children face hardship. Losses in gambling and speculation. Betrayal in love relationships.", "family", "strong"),
    ("rahu", 6,  "गुप्त शत्रु। चर्म रोग या नशे की लत। कर्ज से परेशानी।",
     "Hidden enemies. Skin disease or addiction. Troubles from debt.", "physical", "strong"),
    ("rahu", 7,  "विवाह में देरी या परेशानी। साझेदार से धोखा। पत्नी का स्वास्थ्य ठीक नहीं।",
     "Delay or trouble in marriage. Betrayal by partner. Wife's health not good.", "family", "strong"),
    ("rahu", 8,  "अचानक धन हानि। दुर्घटना का भय। गुप्त शत्रु जानलेवा।",
     "Sudden financial loss. Fear of accidents. Hidden enemies are dangerous.", "events", "strong"),
    ("rahu", 9,  "पिता को कष्ट। धर्म के प्रति भ्रम। विदेश यात्रा में बाधाएं।",
     "Hardship to father. Confusion about religion. Obstacles in foreign travel.", "family", "moderate"),
    ("rahu", 10, "करियर में अचानक उठान या पतन। सरकारी कामों में बाधाएं। झूठ से काम चलाएगा।",
     "Sudden rise or fall in career. Obstacles in government work. Will use deception to manage.", "events", "strong"),
    ("rahu", 11, "मित्र विश्वासघाती। धन अचानक मिलेगा और जाएगा। बड़े भाई को कष्ट।",
     "Treacherous friends. Money will come and go suddenly. Elder brother in hardship.", "family", "moderate"),
    ("rahu", 12, "विदेश में बसने के योग लेकिन परेशानी। गुप्त शत्रु। खर्च बेहद अधिक।",
     "Chances of settling abroad but with hardship. Hidden enemies. Very high expenditure.", "events", "strong"),

    # KETU (केतु)
    ("ketu", 1,  "वात रोग सर दर्द और विधवा स्त्री से झगड़ा करने वाला। परिवार में किसी को शुगर हो सकती है। रिश्तेदारों से अनबन रहेगी।",
     "Vata disorders and headaches; quarrelsome with widows. Someone in family may have diabetes. Disputes with relatives.", "physical", "moderate"),
    ("ketu", 2,  "परिवार में कोई बहुत सड़े मिज़ाज का होगा। जातक खुद या परिवार में किसी को किसी और ने पाला होगा। पतंग की डोर, केबल के गुच्छे, ऊन के गोले घर में होंगे।",
     "Someone in family will be very ill-tempered. Native or family member was raised by someone else. Kite strings, cable bundles, or wool balls found in the house.", "home", "strong"),
    ("ketu", 3,  "भाई-बहनों के साथ तनाव। साहस की कमी। धार्मिक यात्राओं में बाधाएं।",
     "Tension with siblings. Lack of courage. Obstacles in religious journeys.", "family", "moderate"),
    ("ketu", 4,  "माता को कष्ट। पुराने घर में रहने के योग। माता की सेहत चिंताजनक।",
     "Hardship to mother. Likely to live in an old house. Mother's health is concerning.", "family", "strong"),
    ("ketu", 5,  "संतान कम। पहला बच्चा कष्ट में। आध्यात्मिक संतान होगी।",
     "Few children. First child faces hardship. Children will be spiritually inclined.", "family", "strong"),
    ("ketu", 6,  "रोग जल्दी ठीक होंगे। गुप्त शत्रु नष्ट होंगे। पेट के रोगों से सावधानी।",
     "Diseases will heal quickly. Hidden enemies will be destroyed. Caution regarding stomach ailments.", "physical", "moderate"),
    ("ketu", 7,  "विवाह में परेशानी। पति-पत्नी में दूरी। साझेदार से झगड़ा।",
     "Trouble in marriage. Distance between husband and wife. Disputes with partner.", "family", "strong"),
    ("ketu", 8,  "दीर्घायु। पैतृक संपत्ति में हानि। रहस्यमयी जीवन।",
     "Long life. Loss in ancestral property. Mysterious life.", "events", "moderate"),
    ("ketu", 9,  "पिता का साथ नहीं मिलेगा। धर्म में संशय। भाग्य साथ नहीं देगा।",
     "Will not receive father's support. Doubt about religion. Fortune will not be supportive.", "family", "strong"),
    ("ketu", 10, "करियर में रुकावटें। ध्यान भटकेगा। आध्यात्मिक कार्यों से सफलता।",
     "Obstacles in career. Mind will wander. Success through spiritual work.", "events", "moderate"),
    ("ketu", 11, "मित्रों से लाभ कम। बड़े भाई की परेशानी। धन संचय कठिन।",
     "Less benefit from friends. Elder brother's hardship. Wealth accumulation is difficult.", "events", "moderate"),
    ("ketu", 12, "मोक्ष की साधना करेगा। विदेश में सुख। एकांतवास में रुचि।",
     "Will seek spiritual liberation. Happiness abroad. Interest in solitude.", "events", "mild"),
]

# ─────────────────────────────────────────────────────────────
# TABLE 2: LAL KITAB DEBTS  (8 karmic debts / Rin)
# Columns: debt_type, planet, description, indication, remedy
# Note: DB columns are description/indication/remedy (single text each)
#       We expose _hi / _en variants in the Python dict for test validation
#       and combine them for DB insert.
# ─────────────────────────────────────────────────────────────

LK_DEBTS = [
    {
        "debt_type": "पितृ ऋण",
        "planet": "sun",
        "description_hi": "पिता या पितृ पक्ष के प्रति कर्तव्यों की अनदेखी से उत्पन्न ऋण।",
        "description_en": "Debt arising from neglect of duties towards father and paternal lineage.",
        "indication_hi": "पिता से अनबन, नौकरी में बाधा, सरकारी काम में परेशानी, आँखों की समस्या।",
        "indication_en": "Conflict with father, career obstacles, government-related troubles, eye problems.",
        "remedy_hi": "रविवार को गेहूं और गुड़ दान करें। सूर्य को जल अर्पण करें। तांबे के बर्तन में गंगाजल रखें।",
        "remedy_en": "Donate wheat and jaggery on Sundays. Offer water to the Sun at sunrise. Keep Gangajal in a copper vessel.",
    },
    {
        "debt_type": "मातृ ऋण",
        "planet": "moon",
        "description_hi": "माता या मातृ पक्ष के प्रति उपेक्षा से उत्पन्न ऋण।",
        "description_en": "Debt arising from neglect of mother and maternal lineage.",
        "indication_hi": "माता से अनबन, मानसिक तनाव, चंद्रमा से संबंधित पीड़ाएं, नींद में कठिनाई।",
        "indication_en": "Conflict with mother, mental stress, Moon-related afflictions, sleep difficulties.",
        "remedy_hi": "सोमवार को चावल और दूध दान करें। माता की सेवा करें। चाँदी का चौकोर टुकड़ा रखें।",
        "remedy_en": "Donate rice and milk on Mondays. Serve your mother. Keep a square piece of silver.",
    },
    {
        "debt_type": "भ्रातृ ऋण",
        "planet": "mercury",
        "description_hi": "भाई-बहनों के प्रति अन्याय या उपेक्षा से उत्पन्न ऋण।",
        "description_en": "Debt from injustice or neglect toward siblings.",
        "indication_hi": "बुध खराब हो, भाई-बहनों से झगड़े, शिक्षा में बाधा, व्यापार में नुकसान।",
        "indication_en": "Mercury afflicted, disputes with siblings, obstacles in education, business losses.",
        "remedy_hi": "बुधवार को हरी मूंग दान करें। भाई-बहन का सम्मान करें। पन्ना धारण करें।",
        "remedy_en": "Donate green moong on Wednesdays. Respect your siblings. Wear an emerald.",
    },
    {
        "debt_type": "देव ऋण",
        "planet": "jupiter",
        "description_hi": "देवताओं या गुरु के प्रति श्रद्धा न रखने से उत्पन्न ऋण।",
        "description_en": "Debt from lack of devotion toward deities or Guru.",
        "indication_hi": "गुरु खराब हो, संतान संबंधी समस्याएं, धर्म में अरुचि, शिक्षा में व्यवधान।",
        "indication_en": "Jupiter afflicted, issues related to children, disinterest in religion, disruptions in education.",
        "remedy_hi": "गुरुवार को पीपल की पूजा करें। ब्राह्मण को भोजन कराएं। पीला पुखराज धारण करें।",
        "remedy_en": "Worship the Peepal tree on Thursdays. Feed a Brahmin. Wear a yellow topaz.",
    },
    {
        "debt_type": "स्त्री ऋण",
        "planet": "venus",
        "description_hi": "स्त्रियों के प्रति अपमान या शोषण से उत्पन्न ऋण।",
        "description_en": "Debt from disrespect or exploitation of women.",
        "indication_hi": "शुक्र खराब हो, वैवाहिक समस्याएं, पत्नी का अस्वस्थ रहना, धन व्यय।",
        "indication_en": "Venus afflicted, marital problems, wife's ill health, financial expenditure.",
        "remedy_hi": "शुक्रवार को गाय की सेवा करें। पत्नी का सम्मान करें। हीरा या ओपल धारण करें।",
        "remedy_en": "Serve a cow on Fridays. Respect your wife. Wear a diamond or opal.",
    },
    {
        "debt_type": "शत्रु ऋण",
        "planet": "mars",
        "description_hi": "भाइयों या शत्रुओं के साथ किए गए अन्याय से उत्पन्न ऋण।",
        "description_en": "Debt arising from injustice done to brothers or enemies.",
        "indication_hi": "मंगल खराब हो, भाइयों से झगड़े, रक्त संबंधी रोग, दुर्घटनाओं का भय।",
        "indication_en": "Mars afflicted, disputes with brothers, blood-related diseases, fear of accidents.",
        "remedy_hi": "मंगलवार को लाल मसूर दाल दान करें। हनुमान जी को सिंदूर चढ़ाएं। मूंगा धारण करें।",
        "remedy_en": "Donate red lentils on Tuesdays. Offer sindoor to Hanuman ji. Wear coral.",
    },
    {
        "debt_type": "पितामह ऋण",
        "planet": "saturn",
        "description_hi": "दादा-परदादा या पूर्वजों के प्रति कर्तव्यहीनता से उत्पन्न ऋण।",
        "description_en": "Debt from neglect of duties toward grandfather and ancestors.",
        "indication_hi": "शनि खराब हो, जीवन में देरी से सफलता, शारीरिक पीड़ा, एकाकीपन।",
        "indication_en": "Saturn afflicted, delayed success in life, physical pain, loneliness.",
        "remedy_hi": "शनिवार को तेल दान करें। काले कुत्ते को रोटी खिलाएं। नीलम या काले घोड़े की नाल की अंगूठी।",
        "remedy_en": "Donate oil on Saturdays. Feed black dogs bread. Wear a sapphire or horseshoe ring.",
    },
    {
        "debt_type": "प्रपितामह ऋण",
        "planet": "rahu",
        "description_hi": "नाना-परनाना या मातृ पितामह के प्रति की गई उपेक्षा से उत्पन्न ऋण।",
        "description_en": "Debt from neglect of maternal grandfather and his lineage.",
        "indication_hi": "राहु खराब हो, गुप्त शत्रु, नशे की लत, अचानक धन हानि।",
        "indication_en": "Rahu afflicted, hidden enemies, addiction, sudden financial loss.",
        "remedy_hi": "400 ग्राम सीसा बहते पानी में डालें। गले में चाँदी पहनें। नाना का सम्मान करें।",
        "remedy_en": "Throw 400 grams of lead into flowing water. Wear silver around the neck. Respect your maternal grandfather.",
    },
]

# ─────────────────────────────────────────────────────────────
# TABLE 3: LK_INTERPRETATIONS  (9 planets × 12 houses = 108)
# Columns: planet, house, interpretation_hi, interpretation_en, category
# ─────────────────────────────────────────────────────────────

LK_INTERPRETATIONS = [
    # SUN (सूर्य)
    {"planet": "sun", "house": 1,  "interpretation_hi": "सूर्य प्रथम भाव में — व्यक्तित्व प्रबल, सरकारी क्षेत्र में सफलता, नेतृत्व गुण। पिता का प्रभाव जीवन पर गहरा।", "interpretation_en": "Sun in House 1 — Strong personality, success in government sector, leadership qualities. Father's influence is deep.", "category": "personality"},
    {"planet": "sun", "house": 2,  "interpretation_hi": "सूर्य द्वितीय भाव में — परिवार में दो विवाह। वाणी प्रभावशाली। धन संचय में उतार-चढ़ाव।", "interpretation_en": "Sun in House 2 — Two marriages in family. Powerful speech. Fluctuations in wealth accumulation.", "category": "wealth"},
    {"planet": "sun", "house": 3,  "interpretation_hi": "सूर्य तृतीय भाव में — भाई-बहनों से अनबन। साहस और पराक्रम उच्च। पड़ोस में अशांति।", "interpretation_en": "Sun in House 3 — Discord with siblings. High courage and valor. Unrest in neighborhood.", "category": "siblings"},
    {"planet": "sun", "house": 4,  "interpretation_hi": "सूर्य चतुर्थ भाव में — मकान और वाहन सुख। माता पे दबाव। मीठे का शौक।", "interpretation_en": "Sun in House 4 — Happiness from house and vehicle. Pressure on mother. Fondness for sweets.", "category": "home"},
    {"planet": "sun", "house": 5,  "interpretation_hi": "सूर्य पंचम भाव में — संतान में समस्याएं। पेट की बीमारी। प्रेम संबंध अस्थिर।", "interpretation_en": "Sun in House 5 — Problems with children. Stomach ailments. Unstable love relationships.", "category": "children"},
    {"planet": "sun", "house": 6,  "interpretation_hi": "सूर्य षष्ठ भाव में — गुप्त शत्रु। नाना पक्ष से सहायता। कर्ज का भय।", "interpretation_en": "Sun in House 6 — Hidden enemies. Help from maternal side. Fear of debt.", "category": "enemies"},
    {"planet": "sun", "house": 7,  "interpretation_hi": "सूर्य सप्तम भाव में — प्रेम विवाह के योग। व्यापारिक साझेदार से लाभ। पत्नी का स्वास्थ्य कमज़ोर।", "interpretation_en": "Sun in House 7 — Chances of love marriage. Gains from business partners. Wife's health weak.", "category": "marriage"},
    {"planet": "sun", "house": 8,  "interpretation_hi": "सूर्य अष्टम भाव में — पारिवारिक रहस्य उजागर होंगे। मुकदमेबाज़ी। आयु लंबी किंतु संघर्षपूर्ण।", "interpretation_en": "Sun in House 8 — Family secrets will be revealed. Litigation. Long life but with struggles.", "category": "longevity"},
    {"planet": "sun", "house": 9,  "interpretation_hi": "सूर्य नवम भाव में — पिता पे कष्ट। धार्मिक यात्राएं। भाग्य उज्ज्वल लेकिन देर से।", "interpretation_en": "Sun in House 9 — Hardship on father. Religious travels. Fortune bright but delayed.", "category": "fortune"},
    {"planet": "sun", "house": 10, "interpretation_hi": "सूर्य दशम भाव में — सरकारी नौकरी में सफलता। समाज में प्रतिष्ठा। कार्यक्षेत्र में नेतृत्व।", "interpretation_en": "Sun in House 10 — Success in government job. Prestige in society. Leadership in career.", "category": "career"},
    {"planet": "sun", "house": 11, "interpretation_hi": "सूर्य एकादश भाव में — बड़े भाई से संघर्ष। मित्रों से सहायता। नेकी से बदनामी।", "interpretation_en": "Sun in House 11 — Conflict with elder brother. Help from friends. Goodness brings infamy.", "category": "gains"},
    {"planet": "sun", "house": 12, "interpretation_hi": "सूर्य द्वादश भाव में — खर्च अधिक। विदेश यात्रा के योग। उच्च रक्तचाप का भय।", "interpretation_en": "Sun in House 12 — High expenditure. Chances of foreign travel. Fear of high blood pressure.", "category": "expenditure"},

    # MOON (चंद्र)
    {"planet": "moon", "house": 1,  "interpretation_hi": "चंद्र प्रथम भाव में — धनवान और स्वस्थ। माता की छाया जीवन पर। जुकाम और नज़ले की प्रवृत्ति।", "interpretation_en": "Moon in House 1 — Wealthy and healthy. Mother's shadow on life. Prone to colds and sinus.", "category": "personality"},
    {"planet": "moon", "house": 2,  "interpretation_hi": "चंद्र द्वितीय भाव में — घर में धार्मिक वस्तुएं। वाणी मधुर। शिवलिंग और शंख का प्रभाव।", "interpretation_en": "Moon in House 2 — Religious items in home. Sweet speech. Influence of Shivalinga and conch.", "category": "wealth"},
    {"planet": "moon", "house": 3,  "interpretation_hi": "चंद्र तृतीय भाव में — भावुक और संवेदनशील। भाइयों से अनबन। माता को नसों की परेशानी।", "interpretation_en": "Moon in House 3 — Emotional and sensitive. Discord with siblings. Mother has nerve problems.", "category": "siblings"},
    {"planet": "moon", "house": 4,  "interpretation_hi": "चंद्र चतुर्थ भाव में — माता का सुख, गृह सुख, मानसिक शांति, संपत्ति लाभ। माता का सम्मान अनिवार्य।", "interpretation_en": "Moon in House 4 — Happiness from mother, domestic comfort, mental peace, property gains. Respect for mother is essential.", "category": "home"},
    {"planet": "moon", "house": 5,  "interpretation_hi": "चंद्र पंचम भाव में — संतान प्रिय। बच्चे आज्ञाकारी। पेट में गड़बड़ी के योग।", "interpretation_en": "Moon in House 5 — Fond of children. Children will be obedient. Chances of stomach disturbances.", "category": "children"},
    {"planet": "moon", "house": 6,  "interpretation_hi": "चंद्र षष्ठ भाव में — माता की सेहत कमज़ोर। मानसिक अशांति। गुप्त शत्रु।", "interpretation_en": "Moon in House 6 — Mother's health weak. Mental restlessness. Hidden enemies.", "category": "enemies"},
    {"planet": "moon", "house": 7,  "interpretation_hi": "चंद्र सप्तम भाव में — पत्नी सुंदर और भावुक। वैवाहिक जीवन में उतार-चढ़ाव।", "interpretation_en": "Moon in House 7 — Wife beautiful and emotional. Ups and downs in married life.", "category": "marriage"},
    {"planet": "moon", "house": 8,  "interpretation_hi": "चंद्र अष्टम भाव में — अचानक धन लाभ या हानि। माता को कष्ट। गुप्त बातें उजागर।", "interpretation_en": "Moon in House 8 — Sudden financial gain or loss. Hardship to mother. Secrets revealed.", "category": "longevity"},
    {"planet": "moon", "house": 9,  "interpretation_hi": "चंद्र नवम भाव में — माता के आशीर्वाद से भाग्य। धार्मिक यात्राओं से लाभ।", "interpretation_en": "Moon in House 9 — Fortune through mother's blessings. Gains from religious travels.", "category": "fortune"},
    {"planet": "moon", "house": 10, "interpretation_hi": "चंद्र दशम भाव में — जनता में लोकप्रियता। व्यापार में उतार-चढ़ाव। दयालु स्वभाव।", "interpretation_en": "Moon in House 10 — Popular among masses. Fluctuations in business. Compassionate nature.", "category": "career"},
    {"planet": "moon", "house": 11, "interpretation_hi": "चंद्र एकादश भाव में — मित्रों से लाभ। बड़ी बहन का योग। दूध-पानी से व्यापार शुभ।", "interpretation_en": "Moon in House 11 — Gains from friends. Likely to have elder sister. Business in milk and water auspicious.", "category": "gains"},
    {"planet": "moon", "house": 12, "interpretation_hi": "चंद्र द्वादश भाव में — विदेश यात्रा। अकेलापन। खर्च पर नियंत्रण ज़रूरी।", "interpretation_en": "Moon in House 12 — Foreign travel. Loneliness. Expenditure control necessary.", "category": "expenditure"},

    # VENUS (शुक्र)
    {"planet": "venus", "house": 1,  "interpretation_hi": "शुक्र प्रथम भाव में — पत्नी बीमार रहेगी। प्रेम के लिए जान कुर्बान। रोमांटिक स्वभाव।", "interpretation_en": "Venus in House 1 — Wife will remain unwell. Will sacrifice for love. Romantic nature.", "category": "personality"},
    {"planet": "venus", "house": 2,  "interpretation_hi": "शुक्र द्वितीय भाव में — घर शेरमुखी। पत्नी का प्रभुत्व। फैशनेबल स्वभाव।", "interpretation_en": "Venus in House 2 — Sher-mukhi house. Wife's dominance. Fashionable nature.", "category": "wealth"},
    {"planet": "venus", "house": 3,  "interpretation_hi": "शुक्र तृतीय भाव में — कला प्रेमी। शत्रुओं से भय। घरेलू सहायकों से अत्यधिक निकटता।", "interpretation_en": "Venus in House 3 — Art lover. Fear of enemies. Excessive closeness with household help.", "category": "siblings"},
    {"planet": "venus", "house": 4,  "interpretation_hi": "शुक्र चतुर्थ भाव में — दो विवाह के योग। विलासिता का शौक। शादी के बाद भाग्य उदय।", "interpretation_en": "Venus in House 4 — Two marriages possible. Fondness for luxuries. Fortune rises after marriage.", "category": "home"},
    {"planet": "venus", "house": 5,  "interpretation_hi": "शुक्र पंचम भाव में — संतान सुंदर और गुणी। कला-संगीत में रुचि। रोमांटिक स्वभाव।", "interpretation_en": "Venus in House 5 — Beautiful and virtuous children. Interest in arts and music. Romantic nature.", "category": "children"},
    {"planet": "venus", "house": 6,  "interpretation_hi": "शुक्र षष्ठ भाव में — स्वास्थ्य में परेशानी। ऋण का भय। विरोधियों से सावधानी।", "interpretation_en": "Venus in House 6 — Health troubles. Fear of debt. Be cautious of opponents.", "category": "enemies"},
    {"planet": "venus", "house": 7,  "interpretation_hi": "शुक्र सप्तम भाव में — सुंदर और संस्कारी पत्नी। वैवाहिक जीवन सुखद। साझेदारी से लाभ।", "interpretation_en": "Venus in House 7 — Beautiful and cultured wife. Happy married life. Gains from partnerships.", "category": "marriage"},
    {"planet": "venus", "house": 8,  "interpretation_hi": "शुक्र अष्टम भाव में — ससुराल से धन लाभ। गुप्त संबंध। दुर्घटना का भय।", "interpretation_en": "Venus in House 8 — Gains from in-laws. Secret relationships. Fear of accidents.", "category": "longevity"},
    {"planet": "venus", "house": 9,  "interpretation_hi": "शुक्र नवम भाव में — भाग्यशाली। धार्मिक कार्यों में रुचि। विदेश यात्रा से लाभ।", "interpretation_en": "Venus in House 9 — Lucky. Interest in religious activities. Gains from foreign travel.", "category": "fortune"},
    {"planet": "venus", "house": 10, "interpretation_hi": "शुक्र दशम भाव में — कला-फिल्म-फैशन में सफलता। सरकार से लाभ। व्यापार में उन्नति।", "interpretation_en": "Venus in House 10 — Success in arts, film, fashion. Benefits from government. Business growth.", "category": "career"},
    {"planet": "venus", "house": 11, "interpretation_hi": "शुक्र एकादश भाव में — मित्रों से सहायता। बड़ी बहन का योग। धन संचय के अवसर।", "interpretation_en": "Venus in House 11 — Support from friends. Elder sister likely. Opportunities for wealth accumulation.", "category": "gains"},
    {"planet": "venus", "house": 12, "interpretation_hi": "शुक्र द्वादश भाव में — विदेश में स्थायी निवास। गुप्त प्रेम संबंध। खर्च अधिक।", "interpretation_en": "Venus in House 12 — Permanent settlement abroad. Secret love affairs. High expenditure.", "category": "expenditure"},

    # MARS (मंगल)
    {"planet": "mars", "house": 1,  "interpretation_hi": "मंगल प्रथम भाव में — सिर या माथे पर चोट का निशान। परिवार में वर्दीधारी। शारीरिक शक्ति उच्च।", "interpretation_en": "Mars in House 1 — Scar on head or forehead. Someone in family wears uniform. High physical strength.", "category": "personality"},
    {"planet": "mars", "house": 2,  "interpretation_hi": "मंगल द्वितीय भाव में — मसालेदार खाने का शौक। वाणी कठोर। सत्यवादी।", "interpretation_en": "Mars in House 2 — Fond of spicy food. Harsh speech. Truthful.", "category": "wealth"},
    {"planet": "mars", "house": 3,  "interpretation_hi": "मंगल तृतीय भाव में — भाइयों से झगड़े। साहसी और निडर। दुर्घटना का खतरा।", "interpretation_en": "Mars in House 3 — Fights with brothers. Courageous and fearless. Accident risk.", "category": "siblings"},
    {"planet": "mars", "house": 4,  "interpretation_hi": "मंगल चतुर्थ भाव में — माता से विवाद। घर में आग का खतरा। संपत्ति विवाद।", "interpretation_en": "Mars in House 4 — Disputes with mother. Fire hazard at home. Property disputes.", "category": "home"},
    {"planet": "mars", "house": 5,  "interpretation_hi": "मंगल पंचम भाव में — पहला बच्चा लड़का। संतान सुख में कमी। जुए में नुकसान।", "interpretation_en": "Mars in House 5 — First child likely a boy. Reduced happiness from children. Gambling losses.", "category": "children"},
    {"planet": "mars", "house": 6,  "interpretation_hi": "मंगल षष्ठ भाव में — शत्रुओं पर विजय। रक्त संबंधी रोग। सेना-पुलिस में सेवा योग।", "interpretation_en": "Mars in House 6 — Victory over enemies. Blood-related diseases. Career in army or police.", "category": "enemies"},
    {"planet": "mars", "house": 7,  "interpretation_hi": "मंगल सप्तम भाव में — मंगली योग। दांपत्य में कलह। विवाह में देरी।", "interpretation_en": "Mars in House 7 — Manglik dosha. Marital conflicts. Delay in marriage.", "category": "marriage"},
    {"planet": "mars", "house": 8,  "interpretation_hi": "मंगल अष्टम भाव में — अचानक आघात का भय। पैतृक संपत्ति विवाद। 28 के बाद उन्नति।", "interpretation_en": "Mars in House 8 — Fear of sudden trauma. Ancestral property dispute. Progress after age 28.", "category": "longevity"},
    {"planet": "mars", "house": 9,  "interpretation_hi": "मंगल नवम भाव में — पिता से मतभेद। धर्म में संशय। विदेश यात्रा में बाधा।", "interpretation_en": "Mars in House 9 — Disagreement with father. Doubt about religion. Obstacles in foreign travel.", "category": "fortune"},
    {"planet": "mars", "house": 10, "interpretation_hi": "मंगल दशम भाव में — सरकारी काम में सफलता। इंजीनियरिंग-सेना में करियर। प्रतिस्पर्धी।", "interpretation_en": "Mars in House 10 — Success in government work. Career in engineering or army. Competitive.", "category": "career"},
    {"planet": "mars", "house": 11, "interpretation_hi": "मंगल एकादश भाव में — बड़े भाई से विरोध। मित्रों से विश्वासघात। संघर्ष के बाद धन लाभ।", "interpretation_en": "Mars in House 11 — Opposition from elder brother. Betrayal by friends. Gains after struggle.", "category": "gains"},
    {"planet": "mars", "house": 12, "interpretation_hi": "मंगल द्वादश भाव में — गुप्त शत्रु अधिक। खर्च बेकाबू। विदेश में संघर्ष।", "interpretation_en": "Mars in House 12 — Many hidden enemies. Uncontrolled expenses. Struggles abroad.", "category": "expenditure"},

    # MERCURY (बुध)
    {"planet": "mercury", "house": 1,  "interpretation_hi": "बुध प्रथम भाव में — बुद्धिमान और वाचाल। चापलूस स्वभाव। परिवार में गायक या कलाकार।", "interpretation_en": "Mercury in House 1 — Intelligent and talkative. Flattering nature. Singer or artist in family.", "category": "personality"},
    {"planet": "mercury", "house": 2,  "interpretation_hi": "बुध द्वितीय भाव में — घर में पुरानी वस्तुएं। टेढ़े दाँत। वाणी चतुर।", "interpretation_en": "Mercury in House 2 — Old items in home. Crooked teeth. Clever speech.", "category": "wealth"},
    {"planet": "mercury", "house": 3,  "interpretation_hi": "बुध तृतीय भाव में — पढ़ने-लिखने में कुशल। व्यापारिक बुद्धि। भाई-बहनों से मधुर संबंध।", "interpretation_en": "Mercury in House 3 — Skilled in reading and writing. Business acumen. Harmonious relations with siblings.", "category": "siblings"},
    {"planet": "mercury", "house": 4,  "interpretation_hi": "बुध चतुर्थ भाव में — माता पढ़ी-लिखी। घर में पढ़ाई का माहौल। संपत्ति को लेकर तर्क।", "interpretation_en": "Mercury in House 4 — Mother educated. Academic atmosphere at home. Arguments over property.", "category": "home"},
    {"planet": "mercury", "house": 5,  "interpretation_hi": "बुध पंचम भाव में — संतान बुद्धिमान। शिक्षा में रुचि। अटकलों से नुकसान।", "interpretation_en": "Mercury in House 5 — Intelligent children. Interest in education. Losses from speculation.", "category": "children"},
    {"planet": "mercury", "house": 6,  "interpretation_hi": "बुध षष्ठ भाव में — बुद्धि से शत्रुओं पर विजय। पेट और त्वचा की समस्या।", "interpretation_en": "Mercury in House 6 — Victory over enemies through intellect. Stomach and skin problems.", "category": "enemies"},
    {"planet": "mercury", "house": 7,  "interpretation_hi": "बुध सप्तम भाव में — बुद्धिमान पत्नी। साझेदारी में धोखे का भय।", "interpretation_en": "Mercury in House 7 — Intelligent wife. Risk of betrayal in partnerships.", "category": "marriage"},
    {"planet": "mercury", "house": 8,  "interpretation_hi": "बुध अष्टम भाव में — गुप्त ज्ञान में रुचि। संपत्ति विवाद। जीवन में अचानक परिवर्तन।", "interpretation_en": "Mercury in House 8 — Interest in occult. Property dispute. Sudden changes in life.", "category": "longevity"},
    {"planet": "mercury", "house": 9,  "interpretation_hi": "बुध नवम भाव में — लेखन-अध्यापन में सफलता। धार्मिक बुद्धि। विदेश से ज्ञान।", "interpretation_en": "Mercury in House 9 — Success in writing and teaching. Religious intellect. Knowledge from abroad.", "category": "fortune"},
    {"planet": "mercury", "house": 10, "interpretation_hi": "बुध दशम भाव में — व्यापार में सफलता। लेखक-पत्रकार-वकील बनने के योग।", "interpretation_en": "Mercury in House 10 — Business success. Chances of becoming writer, journalist, or lawyer.", "category": "career"},
    {"planet": "mercury", "house": 11, "interpretation_hi": "बुध एकादश भाव में — व्यापारिक मित्र फायदेमंद। बहन का सहयोग। आय के अनेक स्रोत।", "interpretation_en": "Mercury in House 11 — Business-minded friends beneficial. Sister's support. Multiple income sources.", "category": "gains"},
    {"planet": "mercury", "house": 12, "interpretation_hi": "बुध द्वादश भाव में — विदेश में बसने के योग। गुप्त अध्ययन। खर्च पर नियंत्रण।", "interpretation_en": "Mercury in House 12 — Settling abroad possible. Secret studies. Control expenditure.", "category": "expenditure"},

    # JUPITER (बृहस्पति)
    {"planet": "jupiter", "house": 1,  "interpretation_hi": "बृहस्पति प्रथम भाव में — राजा के समान प्रतापी। विद्वान, सुंदर, दुश्मनों पर विजय। उच्च शिक्षा से किस्मत।", "interpretation_en": "Jupiter in House 1 — Majestic like a king. Learned, handsome, victory over enemies. Fortune through higher education.", "category": "personality"},
    {"planet": "jupiter", "house": 2,  "interpretation_hi": "बृहस्पति द्वितीय भाव में — जगत गुरु बनने के योग। धन संचय। वाणी सुनहरी।", "interpretation_en": "Jupiter in House 2 — Potential to become a world teacher. Wealth accumulation. Golden speech.", "category": "wealth"},
    {"planet": "jupiter", "house": 3,  "interpretation_hi": "बृहस्पति तृतीय भाव में — भाई-बहनों से जुड़ी किस्मत। बुध का प्रभाव। चंद्र उपाय लाभकारी।", "interpretation_en": "Jupiter in House 3 — Fortune tied to siblings. Mercury's influence. Moon remedies most beneficial.", "category": "siblings"},
    {"planet": "jupiter", "house": 4,  "interpretation_hi": "बृहस्पति चतुर्थ भाव में — उच्च स्थिति। संपत्ति, वाहन, माता का आशीर्वाद। पीड़ित हो तो आत्म-विनाश।", "interpretation_en": "Jupiter in House 4 — Exalted position. Property, vehicle, mother's blessings. If afflicted, self-destruction.", "category": "home"},
    {"planet": "jupiter", "house": 5,  "interpretation_hi": "बृहस्पति पंचम भाव में — संतान से किस्मत का संबंध। गुरुवार को पुत्र जन्म शुभ। शिक्षा महत्वपूर्ण।", "interpretation_en": "Jupiter in House 5 — Fortune linked to children. Son born on Thursday is auspicious. Education important.", "category": "children"},
    {"planet": "jupiter", "house": 6,  "interpretation_hi": "बृहस्पति षष्ठ भाव में — मंदा ग्रह। अत्यधिक मेहनत। सेवा से ही भाग्य।", "interpretation_en": "Jupiter in House 6 — Weak planet. Requires extreme hard work. Fortune only through service.", "category": "enemies"},
    {"planet": "jupiter", "house": 7,  "interpretation_hi": "बृहस्पति सप्तम भाव में — विवाह से भाग्य। धर्म कार्य का प्रमुख। आर्थिक संघर्ष छुपाएं।", "interpretation_en": "Jupiter in House 7 — Fortune through marriage. Leader in religious work. Hide financial struggles.", "category": "marriage"},
    {"planet": "jupiter", "house": 8,  "interpretation_hi": "बृहस्पति अष्टम भाव में — विरासती धन बेकार। स्वयं कमाएं। पिता का व्यापार छोड़ें।", "interpretation_en": "Jupiter in House 8 — Inherited wealth useless. Must earn independently. Avoid father's business.", "category": "longevity"},
    {"planet": "jupiter", "house": 9,  "interpretation_hi": "बृहस्पति नवम भाव में — भाग्य उज्ज्वल। धार्मिक यात्राओं से लाभ। बड़ों का आशीर्वाद।", "interpretation_en": "Jupiter in House 9 — Bright fortune. Gains from religious travel. Elders' blessings.", "category": "fortune"},
    {"planet": "jupiter", "house": 10, "interpretation_hi": "बृहस्पति दशम भाव में — सरकारी या उच्च पद। यश-कीर्ति। पिता का व्यवसाय आगे बढ़ाए।", "interpretation_en": "Jupiter in House 10 — Government or senior position. Fame and renown. Continue father's business.", "category": "career"},
    {"planet": "jupiter", "house": 11, "interpretation_hi": "बृहस्पति एकादश भाव में — बड़े भाई-बहन से उन्नति। मित्रों का बड़ा दायरा। लाभ के अनेक स्रोत।", "interpretation_en": "Jupiter in House 11 — Progress with elder siblings. Wide friend circle. Multiple income sources.", "category": "gains"},
    {"planet": "jupiter", "house": 12, "interpretation_hi": "बृहस्पति द्वादश भाव में — विदेश यात्रा। आध्यात्मिक जीवन। खर्च धर्म में।", "interpretation_en": "Jupiter in House 12 — Foreign travel. Spiritual life. Expenses in religious work.", "category": "expenditure"},

    # SATURN (शनि)
    {"planet": "saturn", "house": 1,  "interpretation_hi": "शनि प्रथम भाव में — घर में शराब। कमज़ोर आँखें और क्रोधी स्वभाव। राज़ नहीं बताने वाला।", "interpretation_en": "Saturn in House 1 — Alcohol at home. Weak eyes and irritable temperament. Keeps secrets.", "category": "personality"},
    {"planet": "saturn", "house": 2,  "interpretation_hi": "शनि द्वितीय भाव में — अधूरी पढ़ाई। चालाक पत्नी। सिर पर चोट का योग।", "interpretation_en": "Saturn in House 2 — Incomplete education. Cunning wife. Risk of head injury.", "category": "wealth"},
    {"planet": "saturn", "house": 3,  "interpretation_hi": "शनि तृतीय भाव में — भाइयों से विरोध। कड़ी मेहनत के बाद सफलता। यात्राओं में बाधाएं।", "interpretation_en": "Saturn in House 3 — Opposition from brothers. Success after hard work. Obstacles in journeys.", "category": "siblings"},
    {"planet": "saturn", "house": 4,  "interpretation_hi": "शनि चतुर्थ भाव में — माता को कष्ट। मकान में देरी। पुराना मकान या जमीन।", "interpretation_en": "Saturn in House 4 — Hardship to mother. Delay in getting a house. Old property.", "category": "home"},
    {"planet": "saturn", "house": 5,  "interpretation_hi": "शनि पंचम भाव में — संतान सुख में देरी। पहली संतान कष्ट में। शिक्षा में रुकावट।", "interpretation_en": "Saturn in House 5 — Delayed happiness from children. First child in distress. Education obstacles.", "category": "children"},
    {"planet": "saturn", "house": 6,  "interpretation_hi": "शनि षष्ठ भाव में — शत्रु पर विजय देर से। दीर्घकालीन रोग। नौकरों से परेशानी।", "interpretation_en": "Saturn in House 6 — Victory over enemies is delayed. Chronic illness. Troubles from servants.", "category": "enemies"},
    {"planet": "saturn", "house": 7,  "interpretation_hi": "शनि सप्तम भाव में — विवाह में देरी। बड़ी उम्र की पत्नी। वैवाहिक जीवन संघर्षपूर्ण।", "interpretation_en": "Saturn in House 7 — Delayed marriage. Older wife. Struggle in married life.", "category": "marriage"},
    {"planet": "saturn", "house": 8,  "interpretation_hi": "शनि अष्टम भाव में — दीर्घायु। पैतृक संपत्ति विवाद। 36 के बाद उन्नति।", "interpretation_en": "Saturn in House 8 — Long life. Ancestral property dispute. Progress after age 36.", "category": "longevity"},
    {"planet": "saturn", "house": 9,  "interpretation_hi": "शनि नवम भाव में — पिता को कष्ट। धर्म में उदासीनता। किस्मत देर से।", "interpretation_en": "Saturn in House 9 — Hardship to father. Indifference to religion. Fortune comes late.", "category": "fortune"},
    {"planet": "saturn", "house": 10, "interpretation_hi": "शनि दशम भाव में — उच्च पद देर से मिलेगा। कड़ी मेहनत से सफलता। पदावनति का भय।", "interpretation_en": "Saturn in House 10 — Senior position comes late. Success through hard work. Fear of demotion.", "category": "career"},
    {"planet": "saturn", "house": 11, "interpretation_hi": "शनि एकादश भाव में — बड़े भाई को कष्ट। मित्रों से धोखे का भय। धन संचय धीमा।", "interpretation_en": "Saturn in House 11 — Elder brother in hardship. Risk of betrayal by friends. Slow wealth accumulation.", "category": "gains"},
    {"planet": "saturn", "house": 12, "interpretation_hi": "शनि द्वादश भाव में — जेल, अस्पताल, विदेश का योग। एकांतवास की इच्छा। गुप्त शत्रु।", "interpretation_en": "Saturn in House 12 — Chances of prison, hospital, or abroad. Desire for seclusion. Hidden enemies.", "category": "expenditure"},

    # RAHU (राहु)
    {"planet": "rahu", "house": 1,  "interpretation_hi": "राहु प्रथम भाव में — कभी स्थिर नहीं। दो शादियों के योग। अत्यधिक बोलने वाला।", "interpretation_en": "Rahu in House 1 — Never stable. Two marriages possible. Talks excessively.", "category": "personality"},
    {"planet": "rahu", "house": 2,  "interpretation_hi": "राहु द्वितीय भाव में — घर से भागेगा। दिन में चोरी का भय। आँखों की बीमारी।", "interpretation_en": "Rahu in House 2 — Will flee from home once. Risk of daytime theft. Eye disease.", "category": "wealth"},
    {"planet": "rahu", "house": 3,  "interpretation_hi": "राहु तृतीय भाव में — भाइयों से अनबन। झूठ की आदत। यात्राओं से हानि।", "interpretation_en": "Rahu in House 3 — Discord with brothers. Habit of lying. Losses from travel.", "category": "siblings"},
    {"planet": "rahu", "house": 4,  "interpretation_hi": "राहु चतुर्थ भाव में — माता का अचानक बीमार होना। घर में बार-बार परिवर्तन। संपत्ति विवाद।", "interpretation_en": "Rahu in House 4 — Mother suddenly falls ill. Frequent changes in home. Property disputes.", "category": "home"},
    {"planet": "rahu", "house": 5,  "interpretation_hi": "राहु पंचम भाव में — संतान को कष्ट। जुए में नुकसान। प्रेम संबंधों में धोखा।", "interpretation_en": "Rahu in House 5 — Children face hardship. Gambling losses. Betrayal in love.", "category": "children"},
    {"planet": "rahu", "house": 6,  "interpretation_hi": "राहु षष्ठ भाव में — गुप्त शत्रु। चर्म रोग या नशे की लत। कर्ज से परेशानी।", "interpretation_en": "Rahu in House 6 — Hidden enemies. Skin disease or addiction. Debt troubles.", "category": "enemies"},
    {"planet": "rahu", "house": 7,  "interpretation_hi": "राहु सप्तम भाव में — विवाह में देरी। साझेदार से धोखा। पत्नी का स्वास्थ्य कमज़ोर।", "interpretation_en": "Rahu in House 7 — Delayed marriage. Betrayal by partner. Wife's health weak.", "category": "marriage"},
    {"planet": "rahu", "house": 8,  "interpretation_hi": "राहु अष्टम भाव में — अचानक धन हानि। दुर्घटना का भय। जानलेवा गुप्त शत्रु।", "interpretation_en": "Rahu in House 8 — Sudden financial loss. Accident risk. Dangerous hidden enemies.", "category": "longevity"},
    {"planet": "rahu", "house": 9,  "interpretation_hi": "राहु नवम भाव में — पिता को कष्ट। धर्म में भ्रम। विदेश यात्रा में बाधाएं।", "interpretation_en": "Rahu in House 9 — Hardship to father. Confusion about religion. Obstacles in foreign travel.", "category": "fortune"},
    {"planet": "rahu", "house": 10, "interpretation_hi": "राहु दशम भाव में — करियर में अचानक उठान या पतन। सरकारी कामों में बाधाएं।", "interpretation_en": "Rahu in House 10 — Sudden career rise or fall. Obstacles in government work.", "category": "career"},
    {"planet": "rahu", "house": 11, "interpretation_hi": "राहु एकादश भाव में — विश्वासघाती मित्र। धन अचानक आएगा-जाएगा। बड़े भाई को कष्ट।", "interpretation_en": "Rahu in House 11 — Treacherous friends. Money comes and goes suddenly. Elder brother in hardship.", "category": "gains"},
    {"planet": "rahu", "house": 12, "interpretation_hi": "राहु द्वादश भाव में — विदेश में बसने के योग पर परेशानी। गुप्त शत्रु। बहुत अधिक खर्च।", "interpretation_en": "Rahu in House 12 — Settling abroad but with hardship. Hidden enemies. Very high expenses.", "category": "expenditure"},

    # KETU (केतु)
    {"planet": "ketu", "house": 1,  "interpretation_hi": "केतु प्रथम भाव में — वात रोग और सर दर्द। परिवार में शुगर। रिश्तेदारों से अनबन।", "interpretation_en": "Ketu in House 1 — Vata disorders and headaches. Diabetes in family. Discord with relatives.", "category": "personality"},
    {"planet": "ketu", "house": 2,  "interpretation_hi": "केतु द्वितीय भाव में — परिवार में कोई अत्यधिक क्रोधी। किसी और ने पाला होगा। घर में पतंग की डोर।", "interpretation_en": "Ketu in House 2 — Someone in family very ill-tempered. Raised by someone else. Kite string in house.", "category": "wealth"},
    {"planet": "ketu", "house": 3,  "interpretation_hi": "केतु तृतीय भाव में — भाई-बहनों से तनाव। साहस की कमी। धार्मिक यात्राओं में बाधाएं।", "interpretation_en": "Ketu in House 3 — Tension with siblings. Lack of courage. Obstacles in religious journeys.", "category": "siblings"},
    {"planet": "ketu", "house": 4,  "interpretation_hi": "केतु चतुर्थ भाव में — माता को कष्ट। पुराने घर में रहने के योग। माता की सेहत चिंताजनक।", "interpretation_en": "Ketu in House 4 — Hardship to mother. May live in old house. Mother's health concerning.", "category": "home"},
    {"planet": "ketu", "house": 5,  "interpretation_hi": "केतु पंचम भाव में — संतान कम। पहला बच्चा कष्ट में। आध्यात्मिक संतान।", "interpretation_en": "Ketu in House 5 — Few children. First child in hardship. Spiritually inclined children.", "category": "children"},
    {"planet": "ketu", "house": 6,  "interpretation_hi": "केतु षष्ठ भाव में — रोग जल्दी ठीक होंगे। गुप्त शत्रु नष्ट। पेट रोगों से सावधानी।", "interpretation_en": "Ketu in House 6 — Diseases heal quickly. Hidden enemies destroyed. Caution for stomach ailments.", "category": "enemies"},
    {"planet": "ketu", "house": 7,  "interpretation_hi": "केतु सप्तम भाव में — विवाह में परेशानी। पति-पत्नी में दूरी। साझेदार से झगड़ा।", "interpretation_en": "Ketu in House 7 — Trouble in marriage. Distance between spouses. Disputes with partner.", "category": "marriage"},
    {"planet": "ketu", "house": 8,  "interpretation_hi": "केतु अष्टम भाव में — दीर्घायु। पैतृक संपत्ति में हानि। रहस्यमयी जीवन।", "interpretation_en": "Ketu in House 8 — Long life. Loss in ancestral property. Mysterious life.", "category": "longevity"},
    {"planet": "ketu", "house": 9,  "interpretation_hi": "केतु नवम भाव में — पिता का साथ नहीं मिलेगा। धर्म में संशय। भाग्य का साथ नहीं।", "interpretation_en": "Ketu in House 9 — Father's support absent. Doubt about religion. Fortune unsupportive.", "category": "fortune"},
    {"planet": "ketu", "house": 10, "interpretation_hi": "केतु दशम भाव में — करियर में रुकावटें। ध्यान भटकेगा। आध्यात्मिक कार्यों से सफलता।", "interpretation_en": "Ketu in House 10 — Career obstacles. Mind wanders. Success through spiritual work.", "category": "career"},
    {"planet": "ketu", "house": 11, "interpretation_hi": "केतु एकादश भाव में — मित्रों से लाभ कम। बड़े भाई की परेशानी। धन संचय कठिन।", "interpretation_en": "Ketu in House 11 — Less gains from friends. Elder brother's hardship. Wealth accumulation difficult.", "category": "gains"},
    {"planet": "ketu", "house": 12, "interpretation_hi": "केतु द्वादश भाव में — मोक्ष की साधना। विदेश में सुख। एकांतवास में रुचि।", "interpretation_en": "Ketu in House 12 — Spiritual liberation. Happiness abroad. Interest in seclusion.", "category": "expenditure"},
]


# ─────────────────────────────────────────────────────────────
# SEED FUNCTION
# ─────────────────────────────────────────────────────────────

def seed_lalkitab_tables(db) -> None:
    """
    Idempotent seed of all three Lal Kitab DB tables.
    Uses ON CONFLICT DO NOTHING — safe to call multiple times.

    :param db: PgConnection (or any object with .execute() and .commit())
    """
    _seed_nishaniyan(db)
    _seed_debts(db)
    _seed_lk_interpretations(db)
    try:
        db.commit()
    except Exception:
        pass  # autocommit contexts don't need explicit commit
    logger.info("[seed_lalkitab] All three LK tables seeded successfully.")


def _seed_nishaniyan(db) -> None:
    """Seed nishaniyan_master. Handles both 5-column and 6-column (with nishani_text_en) schemas."""
    # Check if nishani_text_en column exists
    try:
        db.execute("SELECT nishani_text_en FROM nishaniyan_master LIMIT 1")
        has_en_col = True
    except Exception:
        has_en_col = False
        try:
            db.rollback()
        except Exception:
            pass

    if has_en_col:
        sql = """
            INSERT INTO nishaniyan_master (planet, house, nishani_text, nishani_text_en, category, severity)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        for row in LK_NISHANIYAN:
            planet, house, nishani_hi, nishani_en, category, severity = row
            try:
                db.execute(sql, (planet, house, nishani_hi, nishani_en, category, severity))
            except Exception as e:
                logger.debug("[seed_nishaniyan] skip row %s/%s: %s", planet, house, e)
                try:
                    db.rollback()
                except Exception:
                    pass
    else:
        sql = """
            INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        for row in LK_NISHANIYAN:
            planet, house, nishani_hi, _nishani_en, category, severity = row
            try:
                db.execute(sql, (planet, house, nishani_hi, category, severity))
            except Exception as e:
                logger.debug("[seed_nishaniyan] skip row %s/%s: %s", planet, house, e)
                try:
                    db.rollback()
                except Exception:
                    pass

    logger.info("[seed_lalkitab] nishaniyan_master seeded (%d rows).", len(LK_NISHANIYAN))


def _seed_debts(db) -> None:
    """Seed lal_kitab_debts. DB columns: debt_type, planet, description, indication, remedy."""
    sql = """
        INSERT INTO lal_kitab_debts (debt_type, planet, description, indication, remedy)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """
    for debt in LK_DEBTS:
        # Combine Hindi + English for the single DB text columns
        description = f"{debt['description_hi']} / {debt['description_en']}"
        indication = f"{debt['indication_hi']} / {debt['indication_en']}"
        remedy = f"{debt['remedy_hi']} / {debt['remedy_en']}"
        try:
            db.execute(sql, (debt["debt_type"], debt["planet"], description, indication, remedy))
        except Exception as e:
            logger.debug("[seed_debts] skip debt %s: %s", debt.get("debt_type"), e)
            try:
                db.rollback()
            except Exception:
                pass

    logger.info("[seed_lalkitab] lal_kitab_debts seeded (%d rows).", len(LK_DEBTS))


def _seed_lk_interpretations(db) -> None:
    """Seed lk_interpretations table (created by migration if not yet present)."""
    # Ensure table exists
    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS lk_interpretations (
                id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
                planet TEXT NOT NULL,
                house INTEGER NOT NULL CHECK (house BETWEEN 1 AND 12),
                interpretation_hi TEXT NOT NULL,
                interpretation_en TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'general',
                UNIQUE (planet, house)
            )
        """)
        try:
            db.commit()
        except Exception:
            pass
    except Exception as e:
        logger.warning("[seed_lk_interpretations] table creation warning: %s", e)
        try:
            db.rollback()
        except Exception:
            pass

    sql = """
        INSERT INTO lk_interpretations (planet, house, interpretation_hi, interpretation_en, category)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (planet, house) DO NOTHING
    """
    for interp in LK_INTERPRETATIONS:
        try:
            db.execute(sql, (
                interp["planet"],
                interp["house"],
                interp["interpretation_hi"],
                interp["interpretation_en"],
                interp["category"],
            ))
        except Exception as e:
            logger.debug("[seed_lk_interp] skip %s/%s: %s", interp.get("planet"), interp.get("house"), e)
            try:
                db.rollback()
            except Exception:
                pass

    logger.info("[seed_lalkitab] lk_interpretations seeded (%d rows).", len(LK_INTERPRETATIONS))
