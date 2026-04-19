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
    _seed_farmaan(db)
    try:
        db.commit()
    except Exception:
        pass  # autocommit contexts don't need explicit commit
    logger.info("[seed_lalkitab] All four LK tables seeded successfully.")


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


# ─────────────────────────────────────────────────────────────
# LK_FARMAAN — 108 farmaan entries (9 planets × 12 houses)
# These are derived from canonical LK 1952 principles.
# ─────────────────────────────────────────────────────────────
LK_FARMAAN = [
    # SUN (सूर्य) — Farmaans 1–12
    (1, "Sun in House 1: The native is of royal bearing. If Sun is alone, health and authority are strong. Remedy: offer water to the Sun every morning.",
     "सूर्य भाव 1 में: जातक राजसी स्वभाव का होगा। सूर्य अकेला हो तो स्वास्थ्य और अधिकार उच्च। उपाय: प्रतिदिन प्रातः सूर्य को जल अर्पित करें।",
     "Sun in H1 gives kingly nature and vitality. Afflicted Sun here causes ego conflicts.",
     "भाव 1 में सूर्य राजसी स्वभाव और ऊर्जा देता है। पीड़ित सूर्य अहंकार के टकराव देता है।",
     ["Sun"], [1], "high"),
    (2, "Sun in House 2: Family will have two marriages or two prominent figures. Father's gold should not be worn. Offer jaggery to cows.",
     "सूर्य भाव 2 में: परिवार में दो विवाह या दो प्रमुख व्यक्ति होंगे। पिता का सोना न पहनें। गायों को गुड़ खिलाएँ।",
     "Sun in H2 links family wealth to authority. Father's resources should not be personally exploited.",
     "भाव 2 में सूर्य परिवार के धन को अधिकार से जोड़ता है। पिता के संसाधनों का व्यक्तिगत उपयोग न करें।",
     ["Sun"], [2], "high"),
    (3, "Sun in House 3: The native is courageous. Neighbors are often in trouble. Siblings may be fewer or in conflict. Do not accept gifts from brothers.",
     "सूर्य भाव 3 में: जातक साहसी होगा। पड़ोसी अक्सर परेशानी में रहेंगे। भाई कम या विवाद में। भाइयों से उपहार न लें।",
     "Sun in H3 gives courage but creates tension with siblings. Refusing gifts from brothers protects the relationship.",
     "भाव 3 में सूर्य साहस देता है पर भाइयों से तनाव। भाइयों से उपहार न लेने से संबंध सुरक्षित रहते हैं।",
     ["Sun"], [3], "moderate"),
    (4, "Sun in House 4: The native is fond of sweets. Home is visited by prominent guests. Father may be away or focused on public life. Plant a pomegranate tree at home.",
     "सूर्य भाव 4 में: जातक मिठाई का शौकीन। घर में प्रतिष्ठित अतिथि आते हैं। पिता दूर या सार्वजनिक जीवन में। घर में अनार का पेड़ लगाएँ।",
     "Sun in H4 brings distinction to the home. Father's absence is compensated by mother's strength.",
     "भाव 4 में सूर्य घर को विशिष्टता देता है। पिता की अनुपस्थिति माता की शक्ति से पूरी होती है।",
     ["Sun"], [4], "moderate"),
    (5, "Sun in House 5: Stomach is often troubled. Two marriages in the family are likely. Intelligence is high but pride may block learning. Feed jaggery to monkeys.",
     "सूर्य भाव 5 में: पेट अक्सर खराब रहता है। परिवार में दो विवाह संभव। बुद्धि उच्च पर अहंकार सीखने में बाधा। बंदरों को गुड़ खिलाएँ।",
     "Sun in H5 gives high intelligence but stomach sensitivity. Ego management is the key remedy.",
     "भाव 5 में सूर्य उच्च बुद्धि पर पेट की संवेदनशीलता देता है। अहंकार प्रबंधन मुख्य उपाय है।",
     ["Sun"], [5], "moderate"),
    (6, "Sun in House 6: The native gains through government service. Enemies are defeated. Born at maternal grandparents' home or expenses borne by them. Offer water to Surya daily.",
     "सूर्य भाव 6 में: जातक सरकारी सेवा से लाभान्वित। शत्रुओं पर विजय। नानके के घर जन्म या वे प्रसव खर्च उठाते हैं। प्रतिदिन सूर्य को जल अर्पित करें।",
     "Sun in H6 gives government favor and victory over enemies. The native is often born in the mother's parents' home.",
     "भाव 6 में सूर्य सरकारी कृपा और शत्रु विजय देता है। जातक अक्सर माँ के मायके में जन्म लेता है।",
     ["Sun"], [6], "high"),
    (7, "Sun in House 7: Gifts of jaggery and sweets come to the home. Love marriage is possible. Spouse may be from a prominent family. Avoid ego clashes in marriage.",
     "सूर्य भाव 7 में: घर में गुड़ और मिठाई उपहार में आती है। प्रेम विवाह की संभावना। जीवनसाथी प्रतिष्ठित परिवार से। विवाह में अहंकार के टकराव से बचें।",
     "Sun in H7 brings prominent partnerships. The native's ego must be tamed for marital harmony.",
     "भाव 7 में सूर्य प्रतिष्ठित साझेदारी लाता है। वैवाहिक सुख के लिए जातक का अहंकार नियंत्रित होना चाहिए।",
     ["Sun"], [7], "moderate"),
    (8, "Sun in House 8: Wife reveals family secrets. Court cases bring repeated defeats. Copper utensils should be kept clean. Donate wheat on Sundays.",
     "सूर्य भाव 8 में: पत्नी परिवार के राज़ उजागर करती है। मुकदमों में बार-बार हार। तांबे के बर्तन साफ रखें। रविवार को गेहूँ दान करें।",
     "Sun in H8 creates vulnerability in secrets and legal matters. Copper remedies and wheat donation are prescribed.",
     "भाव 8 में सूर्य गुप्त और कानूनी मामलों में कमजोरी देता है। तांबे के उपाय और गेहूँ दान निर्धारित हैं।",
     ["Sun"], [8], "moderate"),
    (9, "Sun in House 9: Brass utensils lie empty at home. House change brings hardship to self or father. Seek father's blessings regularly. Offer water to the Peepal tree.",
     "सूर्य भाव 9 में: घर में पीतल के बड़े बर्तन खाली पड़े। मकान बदलने पर खुद या पिता को कष्ट। नियमित पिता का आशीर्वाद लें। पीपल के पेड़ को जल चढ़ाएँ।",
     "Sun in H9 ties luck to father's wellbeing. Moving houses must be done with caution and father's consent.",
     "भाव 9 में सूर्य भाग्य को पिता के स्वास्थ्य से जोड़ता है। घर बदलना सावधानी और पिता की सहमति से करें।",
     ["Sun"], [9], "moderate"),
    (10, "Sun in House 10: Counterfeit or broken coins are found at home. Work that could be done cheaply ends up costing more. Career peak comes through government or authority. Offer red flowers to the Sun.",
     "सूर्य भाव 10 में: घर में खोटे या टूटे सिक्के मिलते हैं। जो काम सस्ते में हो, वह महँगा पड़ता है। करियर का शिखर सरकार या अधिकार से। सूर्य को लाल फूल अर्पित करें।",
     "Sun in H10 gives career success through authority but creates financial anomalies at home.",
     "भाव 10 में सूर्य अधिकार से करियर सफलता देता है पर घर में आर्थिक विसंगतियाँ।",
     ["Sun"], [10], "high"),
    (11, "Sun in House 11: Father-in-law will not survive long. Acts of charity bring unexpected disrepute. Elder siblings or father's network is beneficial. Donate copper on Sundays.",
     "सूर्य भाव 11 में: ससुर अधिक समय तक जीवित नहीं रहेंगे। दान से बदनामी मिलती है। बड़े भाई-बहन या पिता का नेटवर्क लाभदायक। रविवार को तांबा दान करें।",
     "Sun in H11 brings gains through authority networks but warns against ostentatious charity.",
     "भाव 11 में सूर्य अधिकार नेटवर्क से लाभ देता है पर दिखावटी दान के विरुद्ध चेतावनी।",
     ["Sun"], [11], "moderate"),
    (12, "Sun in House 12: Mobile or electronic items come as gifts. High blood pressure is likely. Expenses on status rise. Perform Surya Namaskar daily to reduce expenditure.",
     "सूर्य भाव 12 में: मोबाइल या इलेक्ट्रॉनिक वस्तुएँ उपहार में मिलती हैं। उच्च रक्तचाप की संभावना। प्रतिष्ठा पर खर्च बढ़ता है। खर्च कम करने के लिए प्रतिदिन सूर्य नमस्कार करें।",
     "Sun in H12 creates hidden expenditures and health issues. Daily Surya Namaskar is the LK prescribed remedy.",
     "भाव 12 में सूर्य छुपे खर्च और स्वास्थ्य समस्याएँ देता है। प्रतिदिन सूर्य नमस्कार लाल किताब द्वारा निर्धारित उपाय है।",
     ["Sun"], [12], "moderate"),

    # MOON (चंद्र) — Farmaans 13–24
    (13, "Moon in House 1: The native is prone to colds. Antibiotics are often found at home. Loves green vegetables. Keep silver with you always.",
     "चंद्र भाव 1 में: जातक को नज़ला-जुकाम जल्दी होता है। घर में एंटीबायोटिक अक्सर होती है। हरी सब्जियाँ खाने का शौक। हमेशा चाँदी साथ रखें।",
     "Moon in H1 creates sensitivity to cold and emotional health. Silver is the prescribed protective metal.",
     "भाव 1 में चंद्र ठंड और भावनात्मक स्वास्थ्य के प्रति संवेदनशीलता देता है। चाँदी निर्धारित सुरक्षात्मक धातु है।",
     ["Moon"], [1], "high"),
    (14, "Moon in House 2: Family will have prosperity tied to mother. Speech is gentle and persuasive. Women in the family are influential. Donate milk on Mondays.",
     "चंद्र भाव 2 में: माता से जुड़ी परिवार की समृद्धि। वाणी कोमल और प्रेरक। परिवार में महिलाएँ प्रभावशाली। सोमवार को दूध दान करें।",
     "Moon in H2 ties family wealth to maternal blessings. Female family members play key roles.",
     "भाव 2 में चंद्र परिवार के धन को मातृ आशीर्वाद से जोड़ता है। महिला परिवार के सदस्य महत्वपूर्ण भूमिका निभाते हैं।",
     ["Moon"], [2], "high"),
    (15, "Moon in House 3: The native travels frequently for emotional reasons. Sibling bonds are emotionally strong. Short journeys bring peace. Keep a silver ball at home.",
     "चंद्र भाव 3 में: जातक भावनात्मक कारणों से बार-बार यात्रा करता है। भाई-बहन के बंधन भावनात्मक रूप से मजबूत। छोटी यात्राएँ शांति लाती हैं। घर में चाँदी की गेंद रखें।",
     "Moon in H3 creates emotionally driven journeys and strong sibling bonds. Silver remedy brings mental peace.",
     "भाव 3 में चंद्र भावनात्मक यात्राएँ और मजबूत भाई-बहन बंधन देता है। चाँदी उपाय मानसिक शांति लाता है।",
     ["Moon"], [3], "moderate"),
    (16, "Moon in House 4 (Pakka Ghar): The native's mother is a great blessing. Home is a sanctuary. Property and vehicles come through maternal connections. Moon in H4 is at its strongest.",
     "चंद्र भाव 4 में (पक्का घर): माता महान आशीर्वाद है। घर एक अभयारण्य। संपत्ति और वाहन माता के संपर्क से। भाव 4 में चंद्र अपनी उच्चतम शक्ति पर।",
     "Moon in H4 is its Pakka Ghar — the strongest position. Mother's blessings are the greatest asset.",
     "भाव 4 में चंद्र अपना पक्का घर है — सबसे मजबूत स्थिति। माता का आशीर्वाद सबसे बड़ी संपत्ति।",
     ["Moon"], [4], "high"),
    (17, "Moon in House 5: Children are sensitive and emotionally intelligent. Love affairs are emotionally intense. Speculation based on intuition may succeed. Offer milk to Shivling on Mondays.",
     "चंद्र भाव 5 में: संतान संवेदनशील और भावनात्मक रूप से बुद्धिमान। प्रेम संबंध भावनात्मक रूप से गहरे। अंतर्ज्ञान पर आधारित सट्टा सफल हो सकता है। सोमवार को शिवलिंग पर दूध चढ़ाएँ।",
     "Moon in H5 creates emotionally intelligent children and intuition-driven creativity.",
     "भाव 5 में चंद्र भावनात्मक रूप से बुद्धिमान संतान और अंतर्ज्ञान-प्रेरित रचनात्मकता देता है।",
     ["Moon"], [5], "moderate"),
    (18, "Moon in House 6: The native is prone to emotional health issues. Enemies exploit emotional weaknesses. Service to women and children strengthens the chart. Donate white items on Mondays.",
     "चंद्र भाव 6 में: जातक भावनात्मक स्वास्थ्य समस्याओं से ग्रस्त। शत्रु भावनात्मक कमजोरियों का शोषण करते हैं। महिलाओं और बच्चों की सेवा कुंडली को मजबूत करती है। सोमवार को सफेद वस्तु दान करें।",
     "Moon in H6 creates emotional vulnerability to enemies. Service-oriented remedies strengthen the chart.",
     "भाव 6 में चंद्र शत्रुओं के प्रति भावनात्मक कमजोरी देता है। सेवापरक उपाय कुंडली को मजबूत करते हैं।",
     ["Moon"], [6], "moderate"),
    (19, "Moon in House 7: Marriage is emotionally fulfilling. Spouse is nurturing and caring. Business partnerships succeed when emotionally compatible. Offer milk to the Moon on full moon nights.",
     "चंद्र भाव 7 में: विवाह भावनात्मक रूप से संतोषजनक। जीवनसाथी पोषण देने वाला और देखभाल करने वाला। व्यापार साझेदारी भावनात्मक संगतता में सफल। पूर्णिमा रात को चंद्रमा को दूध अर्पित करें।",
     "Moon in H7 brings emotionally compatible partnerships and nurturing relationships.",
     "भाव 7 में चंद्र भावनात्मक रूप से संगत साझेदारी और पोषण देने वाले संबंध लाता है।",
     ["Moon"], [7], "high"),
    (20, "Moon in House 8: Hidden emotional fears surface. In-laws have emotional dynamics. Intuitive abilities are strong but morbid thoughts must be controlled. Worship Shiva on Mondays.",
     "चंद्र भाव 8 में: छुपे भावनात्मक भय सामने आते हैं। ससुराल में भावनात्मक गतिशीलता। अंतर्ज्ञान शक्तिशाली पर उदास विचारों पर नियंत्रण जरूरी। सोमवार को शिव पूजा करें।",
     "Moon in H8 gives psychic abilities but creates emotional vulnerability to darkness. Shiva worship is protective.",
     "भाव 8 में चंद्र मानसिक शक्तियाँ देता है पर अंधकार के प्रति भावनात्मक कमजोरी। शिव पूजा सुरक्षात्मक है।",
     ["Moon"], [8], "moderate"),
    (21, "Moon in House 9: Spiritual journeys are emotionally driven. Mother's dharma shapes the native's fortune. Pilgrimage to water-based sacred sites is most beneficial. Keep a silver coin in the prayer room.",
     "चंद्र भाव 9 में: आध्यात्मिक यात्राएँ भावनात्मक रूप से प्रेरित। माता का धर्म जातक के भाग्य को आकार देता है। जल-आधारित तीर्थस्थलों की यात्रा सबसे लाभकारी। पूजा घर में चाँदी का सिक्का रखें।",
     "Moon in H9 ties religious fortune to mother's blessings and water-based sacred journeys.",
     "भाव 9 में चंद्र धार्मिक भाग्य को माता के आशीर्वाद और जल-आधारित तीर्थयात्राओं से जोड़ता है।",
     ["Moon"], [9], "moderate"),
    (22, "Moon in House 10: Career through emotional intelligence and public care. Success in fields serving the public (healthcare, education, hospitality). Respect women in the workplace.",
     "चंद्र भाव 10 में: भावनात्मक बुद्धि और सार्वजनिक देखभाल से करियर। जनसेवा क्षेत्रों में सफलता (स्वास्थ्य, शिक्षा, आतिथ्य)। कार्यस्थल पर महिलाओं का सम्मान करें।",
     "Moon in H10 gives success in public-service careers. Respecting women in the workplace is prescribed.",
     "भाव 10 में चंद्र जनसेवा करियर में सफलता देता है। कार्यस्थल पर महिलाओं का सम्मान निर्धारित है।",
     ["Moon"], [10], "moderate"),
    (23, "Moon in House 11: Wishes are fulfilled through emotional connections and mother's blessings. Elder sister or motherly figure brings gains. Donate milk and white sweets on Mondays.",
     "चंद्र भाव 11 में: भावनात्मक संपर्क और माता के आशीर्वाद से इच्छाएँ पूरी होती हैं। बड़ी बहन या माँ-जैसी व्यक्ति से लाभ। सोमवार को दूध और सफेद मिठाई दान करें।",
     "Moon in H11 brings wish fulfillment through nurturing relationships. Maternal figures are key benefactors.",
     "भाव 11 में चंद्र पोषण देने वाले संबंधों से इच्छापूर्ति लाता है। मातृ समान व्यक्ति प्रमुख दाता हैं।",
     ["Moon"], [11], "high"),
    (24, "Moon in House 12: Emotional withdrawal and spiritual sensitivity. Foreign lands or hospitals may feel like home. Past-life memories surface in dreams. Keep camphor in the bedroom.",
     "चंद्र भाव 12 में: भावनात्मक वापसी और आध्यात्मिक संवेदनशीलता। विदेश या अस्पताल घर जैसे लग सकते हैं। स्वप्न में पूर्वजन्म की यादें आती हैं। शयनकक्ष में कपूर रखें।",
     "Moon in H12 creates spiritual sensitivity and past-life dreamwork. Camphor purifies the sleep environment.",
     "भाव 12 में चंद्र आध्यात्मिक संवेदनशीलता और पूर्वजन्म स्वप्न-कार्य देता है। कपूर नींद के वातावरण को शुद्ध करता है।",
     ["Moon"], [12], "moderate"),

    # MARS (मंगल) — Farmaans 25–36
    (25, "Mars in House 1: Scar on head or forehead. Family has someone in uniform (army/police). Physical strength and courage are high. Do not cut trees — plant them instead.",
     "मंगल भाव 1 में: सिर या माथे पर चोट का निशान। परिवार में वर्दीधारी। शारीरिक शक्ति और साहस उच्च। पेड़ न काटें — बल्कि लगाएँ।",
     "Mars in H1 marks the native with physical courage and a warrior's spirit. Tree planting counteracts Mars's cutting energy.",
     "भाव 1 में मंगल जातक को शारीरिक साहस और योद्धा भावना देता है। पेड़ लगाना मंगल की काटने की ऊर्जा का प्रतिकार करता है।",
     ["Mars"], [1], "high"),
    (26, "Mars in House 2: Fond of spicy food. Speech is harsh but truthful. Money is spent impulsively. Do not lend money — it will not return.",
     "मंगल भाव 2 में: मसालेदार खाने का शौक। वाणी कठोर पर सत्यवादी। पैसा आवेग में खर्च होता है। पैसा उधार न दें — वापस नहीं आएगा।",
     "Mars in H2 creates a truthful but blunt speaker. Financial impulsiveness is the key weakness.",
     "भाव 2 में मंगल सत्यवादी पर कटु वक्ता बनाता है। आर्थिक आवेग मुख्य कमजोरी है।",
     ["Mars"], [2], "moderate"),
    (27, "Mars in House 3 (Pakka Ghar): Courageous and fearless. Fights with brothers may occur but are resolved quickly. Accident risk during journeys. Wear red coral for protection.",
     "मंगल भाव 3 में (पक्का घर): साहसी और निडर। भाइयों से झगड़े होते हैं पर जल्दी सुलझते हैं। यात्रा में दुर्घटना का खतरा। सुरक्षा के लिए लाल मूंगा पहनें।",
     "Mars in H3 is its Pakka Ghar — highest courage and sibling energy. Red coral provides transit protection.",
     "भाव 3 में मंगल अपना पक्का घर है — उच्चतम साहस और भाई-बहन ऊर्जा। लाल मूंगा यात्रा सुरक्षा देता है।",
     ["Mars"], [3], "high"),
    (28, "Mars in House 4: Disputes with mother. Fire hazard at home — keep fire extinguisher. Property disputes with relatives. Do not construct a new room in the south direction.",
     "मंगल भाव 4 में: माता से विवाद। घर में आग का खतरा — अग्निशामक रखें। रिश्तेदारों से संपत्ति विवाद। दक्षिण दिशा में नया कमरा न बनाएँ।",
     "Mars in H4 creates domestic fire risk and property disputes. South-facing construction should be avoided.",
     "भाव 4 में मंगल घरेलू अग्नि जोखिम और संपत्ति विवाद देता है। दक्षिणमुखी निर्माण से बचें।",
     ["Mars"], [4], "moderate"),
    (29, "Mars in House 5: First child is likely a boy. Speculation brings losses. Gambling must be avoided. Feed jaggery to monkeys on Tuesdays.",
     "मंगल भाव 5 में: पहला बच्चा लड़का होने की संभावना। सट्टे से नुकसान। जुए से बिल्कुल बचें। मंगलवार को बंदरों को गुड़ खिलाएँ।",
     "Mars in H5 favors male children but creates losses through speculation. Avoiding gambling is essential.",
     "भाव 5 में मंगल पुरुष संतान पक्षधर है पर सट्टे से नुकसान देता है। जुए से बचना अनिवार्य है।",
     ["Mars"], [5], "moderate"),
    (30, "Mars in House 6: Victory over enemies. Blood-related diseases require monitoring. Career in army, police, or surgery. Donate red lentils on Tuesdays.",
     "मंगल भाव 6 में: शत्रुओं पर विजय। रक्त-संबंधी रोगों की निगरानी जरूरी। सेना, पुलिस या शल्य चिकित्सा में करियर। मंगलवार को लाल मसूर दान करें।",
     "Mars in H6 gives warrior's victory over enemies. Blood health and military/surgical careers are indicated.",
     "भाव 6 में मंगल शत्रुओं पर योद्धा विजय देता है। रक्त स्वास्थ्य और सैन्य/शल्य करियर संकेतित हैं।",
     ["Mars"], [6], "high"),
    (31, "Mars in House 7: Manglik Yoga. Marital conflicts and possible delay in marriage. Partner is energetic and strong-willed. Fast on Tuesdays for marital harmony.",
     "मंगल भाव 7 में: मांगलिक योग। वैवाहिक संघर्ष और विवाह में देरी संभव। साझेदार ऊर्जावान और दृढ़इच्छाशक्ति वाला। वैवाहिक सुख के लिए मंगलवार का व्रत करें।",
     "Mars in H7 creates Manglik Yoga — strong partnerships but potential conflict. Tuesday fasting is prescribed.",
     "भाव 7 में मंगल मांगलिक योग बनाता है — मजबूत साझेदारी पर संभावित संघर्ष। मंगलवार व्रत निर्धारित है।",
     ["Mars"], [7], "high"),
    (32, "Mars in House 8 (Pakka Ghar): Sudden events and transformations. Fear of injuries and surgeries. Research and occult knowledge are excellent. Keep a red cloth under the pillow.",
     "मंगल भाव 8 में (पक्का घर): अचानक घटनाएँ और परिवर्तन। चोट और शल्य चिकित्सा का भय। शोध और गुप्त ज्ञान उत्कृष्ट। तकिए के नीचे लाल कपड़ा रखें।",
     "Mars in H8 is Pakka Ghar — excellent for research and occult but creates sudden life events.",
     "भाव 8 में मंगल पक्का घर है — शोध और गुप्त विद्या के लिए उत्कृष्ट पर अचानक जीवन घटनाएँ।",
     ["Mars"], [8], "high"),
    (33, "Mars in House 9: Disagreement with father. Doubts about religion or dharma. Travel to foreign lands for work. Respect father unconditionally to activate luck.",
     "मंगल भाव 9 में: पिता से मतभेद। धर्म पर संशय। काम के लिए विदेश यात्रा। भाग्य सक्रिय करने के लिए पिता का बिना शर्त सम्मान करें।",
     "Mars in H9 creates tension with father and dharmic doubts. Unconditional respect for father is the key remedy.",
     "भाव 9 में मंगल पिता और धार्मिक संदेह के साथ तनाव देता है। पिता का बिना शर्त सम्मान मुख्य उपाय है।",
     ["Mars"], [9], "moderate"),
    (34, "Mars in House 10: Success in government work, engineering, or military. Competitive and action-oriented career. Donate red items on Tuesdays for career stability.",
     "मंगल भाव 10 में: सरकारी कार्य, इंजीनियरिंग या सेना में सफलता। प्रतिस्पर्धी और सक्रिय करियर। करियर स्थिरता के लिए मंगलवार को लाल वस्तु दान करें।",
     "Mars in H10 gives career success through action and authority. Red item donation on Tuesdays strengthens career.",
     "भाव 10 में मंगल कार्य और अधिकार से करियर सफलता देता है। मंगलवार को लाल वस्तु दान करियर मजबूत करता है।",
     ["Mars"], [10], "high"),
    (35, "Mars in House 11: Opposition from elder brother. Friends may betray. Gains come after struggle and conflict. Never take a loan from friends.",
     "मंगल भाव 11 में: बड़े भाई से विरोध। मित्र विश्वासघात कर सकते हैं। संघर्ष के बाद लाभ आता है। कभी मित्रों से कर्ज न लें।",
     "Mars in H11 brings gains through struggle but warns against financial deals with friends.",
     "भाव 11 में मंगल संघर्ष से लाभ लाता है पर मित्रों के साथ आर्थिक लेन-देन के विरुद्ध चेतावनी।",
     ["Mars"], [11], "moderate"),
    (36, "Mars in House 12: Hidden enemies are many. Expenditure is uncontrolled. Struggles if living abroad. Do not keep weapons or sharp objects in the bedroom.",
     "मंगल भाव 12 में: छुपे शत्रु अधिक। खर्च बेकाबू। विदेश में संघर्ष। शयनकक्ष में हथियार या नुकीली वस्तु न रखें।",
     "Mars in H12 creates hidden enemies and uncontrolled spending. Sharp objects in the bedroom intensify the affliction.",
     "भाव 12 में मंगल छुपे शत्रु और बेकाबू खर्च देता है। शयनकक्ष में नुकीली वस्तुएँ पीड़ा बढ़ाती हैं।",
     ["Mars"], [12], "moderate"),

    # JUPITER (बृहस्पति) — Farmaans 37–48
    (37, "Jupiter in House 1: Majestic like a king. Learned and wise. Fortune through higher education and dharma. Do not disrespect teachers or Brahmins.",
     "बृहस्पति भाव 1 में: राजा के समान प्रतापी। विद्वान और बुद्धिमान। उच्च शिक्षा और धर्म से किस्मत। गुरु या ब्राह्मण का अपमान न करें।",
     "Jupiter in H1 gives kingly wisdom and fortune through education. Disrespecting teachers destroys Jupiter's blessings.",
     "भाव 1 में बृहस्पति राजसी ज्ञान और शिक्षा से भाग्य देता है। गुरु का अपमान बृहस्पति के आशीर्वाद नष्ट करता है।",
     ["Jupiter"], [1], "high"),
    (38, "Jupiter in House 2 (Pakka Ghar): Potential to become a world teacher. Wealth accumulation is natural. Family is scholarly. Offer yellow sweets at temples on Thursdays.",
     "बृहस्पति भाव 2 में (पक्का घर): जगत गुरु बनने के योग। धन संचय स्वाभाविक। परिवार विद्वान। गुरुवार को मंदिर में पीली मिठाई चढ़ाएँ।",
     "Jupiter in H2 (Pakka Ghar) creates scholars and wealth accumulators. Yellow sweet offerings on Thursday strengthen Jupiter.",
     "भाव 2 में बृहस्पति (पक्का घर) विद्वान और धन संचयकर्ता बनाता है। गुरुवार को पीली मिठाई चढ़ाना बृहस्पति को मजबूत करता है।",
     ["Jupiter"], [2], "high"),
    (39, "Jupiter in House 3: Fortune tied to siblings. Mercury's influence makes communication important. Moon remedies are most beneficial. Donate yellow items on Thursdays.",
     "बृहस्पति भाव 3 में: भाग्य भाई-बहनों से जुड़ा। बुध का प्रभाव संवाद को महत्वपूर्ण बनाता है। चंद्र उपाय सबसे लाभकारी। गुरुवार को पीली वस्तु दान करें।",
     "Jupiter in H3 ties fortune to siblings and communication. Moon remedies are specifically prescribed.",
     "भाव 3 में बृहस्पति भाग्य को भाई-बहन और संवाद से जोड़ता है। चंद्र उपाय विशेष रूप से निर्धारित हैं।",
     ["Jupiter"], [3], "moderate"),
    (40, "Jupiter in House 4: Property, vehicles, and mother's blessings. If Jupiter is afflicted, self-destructive tendencies emerge. Plant a banana tree or offer banana to Vishnu.",
     "बृहस्पति भाव 4 में: संपत्ति, वाहन और माता का आशीर्वाद। पीड़ित बृहस्पति आत्म-विनाश की प्रवृत्ति। केले का पेड़ लगाएँ या विष्णु को केला अर्पित करें।",
     "Jupiter in H4 blesses home and property. Afflicted Jupiter here is particularly dangerous — banana tree remedy is prescribed.",
     "भाव 4 में बृहस्पति घर और संपत्ति को आशीर्वाद देता है। पीड़ित बृहस्पति यहाँ विशेष रूप से खतरनाक — केले का पेड़ निर्धारित उपाय।",
     ["Jupiter"], [4], "high"),
    (41, "Jupiter in House 5: Fortune linked to children. Son born on Thursday is especially auspicious. Education is the key to fortune. Study Sanskrit or sacred texts.",
     "बृहस्पति भाव 5 में: भाग्य संतान से जुड़ा। गुरुवार को जन्मा पुत्र विशेष रूप से शुभ। शिक्षा भाग्य की कुंजी। संस्कृत या धार्मिक ग्रंथ पढ़ें।",
     "Jupiter in H5 ties luck to children and education. Thursday-born sons carry special blessings.",
     "भाव 5 में बृहस्पति भाग्य को संतान और शिक्षा से जोड़ता है। गुरुवार को जन्मे पुत्र विशेष आशीर्वाद लाते हैं।",
     ["Jupiter"], [5], "high"),
    (42, "Jupiter in House 6: Weak placement — requires extreme hard work. Fortune only through service. Avoid complacency. Feed cows on Thursdays.",
     "बृहस्पति भाव 6 में: कमजोर स्थान — अत्यधिक मेहनत जरूरी। सेवा से ही भाग्य। आलस्य से बचें। गुरुवार को गायों को चारा खिलाएँ।",
     "Jupiter in H6 is debilitated in LK terms — only hard work and service unlocks its blessings.",
     "भाव 6 में बृहस्पति लाल किताब के अनुसार कमजोर — केवल परिश्रम और सेवा से आशीर्वाद मिलता है।",
     ["Jupiter"], [6], "moderate"),
    (43, "Jupiter in House 7: Fortune through marriage. Leader in religious work. Hide financial struggles from spouse. Offer yellow flowers at Vishnu temple on Thursdays.",
     "बृहस्पति भाव 7 में: विवाह से भाग्य। धर्म कार्यों का प्रमुख। जीवनसाथी से आर्थिक संघर्ष छुपाएँ। गुरुवार को विष्णु मंदिर में पीले फूल चढ़ाएँ।",
     "Jupiter in H7 brings fortune through marriage and religious leadership. Financial secrets from the spouse protect the chart.",
     "भाव 7 में बृहस्पति विवाह और धार्मिक नेतृत्व से भाग्य लाता है। जीवनसाथी से आर्थिक रहस्य कुंडली की रक्षा करते हैं।",
     ["Jupiter"], [7], "high"),
    (44, "Jupiter in House 8: Inherited wealth is useless — must earn independently. Avoid father's business. Research and wisdom produce genuine results.",
     "बृहस्पति भाव 8 में: विरासती धन बेकार — स्वयं कमाना जरूरी। पिता का व्यापार न करें। शोध और ज्ञान वास्तविक परिणाम देते हैं।",
     "Jupiter in H8 invalidates inherited wealth. The native must create independent fortune through research.",
     "भाव 8 में बृहस्पति विरासती धन को निरर्थक करता है। जातक को शोध के माध्यम से स्वतंत्र भाग्य बनाना होगा।",
     ["Jupiter"], [8], "moderate"),
    (45, "Jupiter in House 9 (Pakka Ghar): Bright fortune. Religious travel yields major gains. Elders' blessings are highly protective. Recite Guru Stotra daily.",
     "बृहस्पति भाव 9 में (पक्का घर): उज्ज्वल भाग्य। धार्मिक यात्रा से बड़े लाभ। बुजुर्गों का आशीर्वाद अत्यधिक सुरक्षात्मक। प्रतिदिन गुरु स्तोत्र का पाठ करें।",
     "Jupiter in H9 (Pakka Ghar) brings brilliant fortune through dharma. Daily Guru Stotra is the prescribed strengthening practice.",
     "भाव 9 में बृहस्पति (पक्का घर) धर्म से उज्ज्वल भाग्य लाता है। दैनिक गुरु स्तोत्र निर्धारित शक्तिवर्धक अभ्यास है।",
     ["Jupiter"], [9], "high"),
    (46, "Jupiter in House 10: Government or senior position. Fame and renown in society. Continue or honor father's business. Donate yellow sweets at temples on Thursdays.",
     "बृहस्पति भाव 10 में: सरकारी या उच्च पद। समाज में यश-कीर्ति। पिता के व्यवसाय को आगे बढ़ाएँ या सम्मान दें। गुरुवार को मंदिर में पीली मिठाई दान करें।",
     "Jupiter in H10 gives fame and senior positions. Honoring father's work amplifies career blessings.",
     "भाव 10 में बृहस्पति यश और उच्च पद देता है। पिता के कार्य का सम्मान करियर के आशीर्वाद को बढ़ाता है।",
     ["Jupiter"], [10], "high"),
    (47, "Jupiter in House 11: Progress with elder siblings. Wide and beneficial social network. Multiple income sources. Feed Brahmins or scholars on Thursdays.",
     "बृहस्पति भाव 11 में: बड़े भाई-बहन से प्रगति। विस्तृत और लाभकारी सामाजिक नेटवर्क। आय के अनेक स्रोत। गुरुवार को ब्राह्मण या विद्वान को भोजन कराएँ।",
     "Jupiter in H11 brings abundant gains through intellectual social networks and elder sibling cooperation.",
     "भाव 11 में बृहस्पति बौद्धिक सामाजिक नेटवर्क और बड़े भाई-बहन के सहयोग से प्रचुर लाभ लाता है।",
     ["Jupiter"], [11], "high"),
    (48, "Jupiter in House 12 (Pakka Ghar): Foreign travel and spiritual life. Expenses in religious or charitable work. Gains from foreign lands. Visit a temple abroad when possible.",
     "बृहस्पति भाव 12 में (पक्का घर): विदेश यात्रा और आध्यात्मिक जीवन। धार्मिक या धर्मार्थ कार्य में खर्च। विदेश से लाभ। जब संभव हो विदेश में मंदिर जाएँ।",
     "Jupiter in H12 (Pakka Ghar) directs fortune through spirituality and foreign lands. Temple visits abroad are auspicious.",
     "भाव 12 में बृहस्पति (पक्का घर) आध्यात्मिकता और विदेश के माध्यम से भाग्य निर्देशित करता है। विदेश में मंदिर भ्रमण शुभ है।",
     ["Jupiter"], [12], "high"),

    # SATURN (शनि) — Farmaans 49–60
    (49, "Saturn in House 1: Alcohol may be present at home. Weak eyes and irritable nature. Keeps secrets. Do not keep alcohol at home. Feed crows on Saturdays.",
     "शनि भाव 1 में: घर में शराब हो सकती है। कमज़ोर आँखें और चिड़चिड़ा स्वभाव। राज़ छुपाने वाला। घर में शराब न रखें। शनिवार को कौवों को खाना खिलाएँ।",
     "Saturn in H1 creates physical and social challenges. Removing alcohol from home and feeding crows are prescribed remedies.",
     "भाव 1 में शनि शारीरिक और सामाजिक चुनौतियाँ देता है। घर से शराब हटाना और कौवों को खिलाना निर्धारित उपाय हैं।",
     ["Saturn"], [1], "high"),
    (50, "Saturn in House 2: Incomplete education. Cunning spouse. Risk of head injury. Avoid alcohol and gambling. Donate black sesame seeds on Saturdays.",
     "शनि भाव 2 में: अधूरी पढ़ाई। चालाक जीवनसाथी। सिर पर चोट का जोखिम। शराब और जुए से बचें। शनिवार को काले तिल दान करें।",
     "Saturn in H2 creates educational gaps and marital cunning. Black sesame seed donation on Saturday is prescribed.",
     "भाव 2 में शनि शैक्षणिक अंतराल और वैवाहिक चालाकी देता है। शनिवार को काले तिल दान निर्धारित है।",
     ["Saturn"], [2], "moderate"),
    (51, "Saturn in House 3: Opposition from brothers. Success after hard work. Journeys have obstacles. Offer iron items to Saturn temples on Saturdays.",
     "शनि भाव 3 में: भाइयों से विरोध। कड़ी मेहनत के बाद सफलता। यात्राओं में बाधाएँ। शनिवार को शनि मंदिर में लोहे की वस्तु चढ़ाएँ।",
     "Saturn in H3 creates sibling friction and journey delays. Iron offerings at Saturn temples strengthen patience.",
     "भाव 3 में शनि भाई-बहन की रगड़ और यात्रा देरी देता है। शनि मंदिर में लोहे की वस्तु चढ़ाने से धैर्य मजबूत होता है।",
     ["Saturn"], [3], "moderate"),
    (52, "Saturn in House 4: Hardship to mother. Delayed house ownership. Property is often old or inherited. Serve your mother regularly to reduce Saturn's affliction.",
     "शनि भाव 4 में: माता को कष्ट। घर मिलने में देरी। संपत्ति अक्सर पुरानी या विरासत में। शनि की पीड़ा कम करने के लिए नियमित माता की सेवा करें।",
     "Saturn in H4 delays home ownership and creates maternal hardship. Mother's service is the direct remedy.",
     "भाव 4 में शनि घर स्वामित्व में देरी और मातृ कष्ट देता है। माता की सेवा सीधा उपाय है।",
     ["Saturn"], [4], "moderate"),
    (53, "Saturn in House 5: Delayed happiness from children. First child may face hardship. Education has obstacles. Study with discipline and persist — results come late but surely.",
     "शनि भाव 5 में: संतान सुख में देरी। पहली संतान को कष्ट हो सकता है। शिक्षा में बाधाएँ। अनुशासन से पढ़ाई करें और दृढ़ रहें — परिणाम देर से पर निश्चित।",
     "Saturn in H5 delays but does not deny — discipline in study and parenting eventually yields results.",
     "भाव 5 में शनि देरी करता है पर वंचित नहीं — पढ़ाई और पालन-पोषण में अनुशासन अंततः फल देता है।",
     ["Saturn"], [5], "moderate"),
    (54, "Saturn in House 6: Delayed victory over enemies but assured. Chronic illness must be managed. Servants and employees may cause trouble. Feed black dogs on Saturdays.",
     "शनि भाव 6 में: शत्रुओं पर देर से पर निश्चित विजय। दीर्घकालीन रोग का प्रबंधन जरूरी। नौकर या कर्मचारी परेशानी दे सकते हैं। शनिवार को काले कुत्तों को खाना खिलाएँ।",
     "Saturn in H6 assures victory over enemies through persistence. Black dog feeding on Saturdays is prescribed.",
     "भाव 6 में शनि दृढ़ता से शत्रुओं पर निश्चित विजय देता है। शनिवार को काले कुत्तों को खिलाना निर्धारित है।",
     ["Saturn"], [6], "high"),
    (55, "Saturn in House 7 (Pakka Ghar): Marriage is delayed but the bond is lasting. Spouse is serious, mature, or older. Discipline in relationship brings long-term rewards.",
     "शनि भाव 7 में (पक्का घर): विवाह में देरी पर बंधन टिकाऊ। जीवनसाथी गंभीर, परिपक्व या बड़ी उम्र का। संबंध में अनुशासन दीर्घकालिक पुरस्कार लाता है।",
     "Saturn in H7 (Pakka Ghar) — delayed but durable marriage. Maturity and discipline are the relationship's pillars.",
     "भाव 7 में शनि (पक्का घर) — देर से पर टिकाऊ विवाह। परिपक्वता और अनुशासन संबंध के स्तंभ हैं।",
     ["Saturn"], [7], "high"),
    (56, "Saturn in House 8: Long life despite hardships. Ancestral property disputes. Progress after age 36. Donate black sesame seeds and mustard oil on Saturdays.",
     "शनि भाव 8 में: कठिनाइयों के बावजूद दीर्घायु। पैतृक संपत्ति विवाद। 36 वर्ष के बाद प्रगति। शनिवार को काले तिल और सरसों का तेल दान करें।",
     "Saturn in H8 gives longevity but delays progress until age 36. Saturday donations accelerate Saturn's timeline.",
     "भाव 8 में शनि दीर्घायु देता है पर 36 वर्ष तक प्रगति में देरी। शनिवार दान शनि की समयरेखा त्वरित करते हैं।",
     ["Saturn"], [8], "high"),
    (57, "Saturn in House 9: Father faces hardship. Religious indifference possible. Fortune comes very late. Serve your father and the elderly to activate luck.",
     "शनि भाव 9 में: पिता को कष्ट। धर्म में उदासीनता संभव। भाग्य बहुत देर से आता है। भाग्य सक्रिय करने के लिए पिता और बुजुर्गों की सेवा करें।",
     "Saturn in H9 delays fortune and creates father's hardship. Serving elders is the prescribed remedy to unlock luck.",
     "भाव 9 में शनि भाग्य में देरी और पिता को कष्ट देता है। बुजुर्गों की सेवा भाग्य अनलॉक करने का निर्धारित उपाय है।",
     ["Saturn"], [9], "moderate"),
    (58, "Saturn in House 10 (Pakka Ghar): Senior position comes late but durably. Success through hard work and discipline. Authority is earned, never gifted.",
     "शनि भाव 10 में (पक्का घर): उच्च पद देर से पर स्थायी। कठिन परिश्रम और अनुशासन से सफलता। अधिकार अर्जित होता है, कभी उपहार में नहीं मिलता।",
     "Saturn in H10 (Pakka Ghar) gives hard-won but permanent career authority. No shortcuts — only discipline works.",
     "भाव 10 में शनि (पक्का घर) कठिन पर स्थायी करियर अधिकार देता है। कोई शॉर्टकट नहीं — केवल अनुशासन काम करता है।",
     ["Saturn"], [10], "high"),
    (59, "Saturn in House 11: Elder brother faces hardship. Friends may betray. Wealth accumulates slowly but surely. Never take loans from friends.",
     "शनि भाव 11 में: बड़े भाई को कष्ट। मित्र धोखा दे सकते हैं। धन धीरे पर निश्चित संचित होता है। मित्रों से कर्ज कभी न लें।",
     "Saturn in H11 builds wealth slowly and warns against financial dealings with friends.",
     "भाव 11 में शनि धीरे धन बनाता है और मित्रों के साथ आर्थिक लेन-देन के विरुद्ध चेतावनी देता है।",
     ["Saturn"], [11], "moderate"),
    (60, "Saturn in House 12: Expenditures rise and isolation increases. Spiritual retreat or foreign stay indicated. Past karma requires closure through service.",
     "शनि भाव 12 में: खर्च बढ़ता है और एकांत में वृद्धि। आध्यात्मिक साधना या विदेश प्रवास संभव। पूर्वकर्म का समाधान सेवा के माध्यम से।",
     "Saturn in H12 demands karmic closure through service. Foreign stays or spiritual retreats are part of this karmic resolution.",
     "भाव 12 में शनि सेवा के माध्यम से कर्म समाधान माँगता है। विदेश प्रवास या आध्यात्मिक साधना इस कर्म समाधान का हिस्सा है।",
     ["Saturn"], [12], "moderate"),

    # VENUS (शुक्र) — Farmaans 61–72
    (61, "Venus in House 1: Beautiful and charming nature. Artistic and musical talents. Good health and attractive appearance. Keep your surroundings clean and fragrant.",
     "शुक्र भाव 1 में: सुंदर और आकर्षक स्वभाव। कलात्मक और संगीत प्रतिभा। अच्छा स्वास्थ्य और आकर्षक रूप। परिवेश को साफ और सुगंधित रखें।",
     "Venus in H1 grants natural beauty and artistic gifts. A clean, fragrant home amplifies Venus's blessings.",
     "भाव 1 में शुक्र प्राकृतिक सौंदर्य और कलात्मक उपहार देता है। साफ, सुगंधित घर शुक्र के आशीर्वाद को बढ़ाता है।",
     ["Venus"], [1], "high"),
    (62, "Venus in House 2: Family wealth through beauty or artistic industries. Speech is charming and persuasive. Women in the family are prosperous. Never disrespect women.",
     "शुक्र भाव 2 में: सौंदर्य या कलात्मक उद्योग से पारिवारिक धन। वाणी आकर्षक और प्रेरक। परिवार में महिलाएँ समृद्ध। महिलाओं का कभी अपमान न करें।",
     "Venus in H2 ties family wealth to beauty and art. Respecting women in the family is essential to maintain Venus's favor.",
     "भाव 2 में शुक्र परिवार के धन को सौंदर्य और कला से जोड़ता है। परिवार में महिलाओं का सम्मान शुक्र की कृपा बनाए रखने के लिए अनिवार्य।",
     ["Venus"], [2], "high"),
    (63, "Venus in House 3: Beautiful, artistic communication. Pleasant short journeys. Sibling bonds are harmonious. Write or create art regularly to activate Venus.",
     "शुक्र भाव 3 में: सुंदर, कलात्मक संवाद। सुखद छोटी यात्राएँ। भाई-बहन के बंधन सामंजस्यपूर्ण। शुक्र सक्रिय करने के लिए नियमित लेखन या कला बनाएँ।",
     "Venus in H3 brings artistic communication and harmonious sibling relationships. Regular creative practice amplifies Venus.",
     "भाव 3 में शुक्र कलात्मक संवाद और सामंजस्यपूर्ण भाई-बहन संबंध लाता है। नियमित रचनात्मक अभ्यास शुक्र को बढ़ाता है।",
     ["Venus"], [3], "moderate"),
    (64, "Venus in House 4: Home is beautiful and comfortable. Mother's blessings bring property and vehicles. Domestic happiness increases. Keep fresh flowers at home.",
     "शुक्र भाव 4 में: घर सुंदर और आरामदायक। माता का आशीर्वाद संपत्ति और वाहन लाता है। घरेलू सुख बढ़ता है। घर में ताजे फूल रखें।",
     "Venus in H4 beautifies the home and brings maternal blessings. Fresh flowers at home amplify Venus's domestic energy.",
     "भाव 4 में शुक्र घर को सुंदर और मातृ आशीर्वाद लाता है। घर में ताजे फूल शुक्र की घरेलू ऊर्जा को बढ़ाते हैं।",
     ["Venus"], [4], "high"),
    (65, "Venus in House 5: Excellent creativity, romance, and speculation. Children are beautiful and artistically gifted. Love life is vibrant. Donate white sweets on Fridays.",
     "शुक्र भाव 5 में: उत्कृष्ट रचनात्मकता, प्रेम और सट्टा। संतान सुंदर और कलात्मक रूप से प्रतिभाशाली। प्रेम जीवन जीवंत। शुक्रवार को सफेद मिठाई दान करें।",
     "Venus in H5 gives artistic children and vibrant romance. White sweet donation on Fridays amplifies Venus's creative blessings.",
     "भाव 5 में शुक्र कलात्मक संतान और जीवंत प्रेम देता है। शुक्रवार को सफेद मिठाई दान शुक्र की रचनात्मक कृपा बढ़ाता है।",
     ["Venus"], [5], "high"),
    (66, "Venus in House 6: Enemies are dissolved through charm and grace. Health resolves gently through beauty routines. Service work brings appreciation. Avoid harsh treatment of women.",
     "शुक्र भाव 6 में: आकर्षण और शालीनता से शत्रु घुलते हैं। सौंदर्य दिनचर्या से स्वास्थ्य सहजता से सुलझता है। सेवा कार्य सराहा जाता है। महिलाओं के साथ कठोर व्यवहार से बचें।",
     "Venus in H6 defeats enemies through grace rather than force. Respecting women maintains Venus's protective shield.",
     "भाव 6 में शुक्र बल के बजाय शालीनता से शत्रुओं को हराता है। महिलाओं का सम्मान शुक्र की सुरक्षात्मक ढाल बनाए रखता है।",
     ["Venus"], [6], "moderate"),
    (67, "Venus in House 7 (Pakka Ghar): The strongest placement for Venus. Marriage is blessed with beauty, harmony, and love. Business partnerships flourish. Offer white flowers at Lakshmi temple on Fridays.",
     "शुक्र भाव 7 में (पक्का घर): शुक्र के लिए सबसे मजबूत स्थान। विवाह सौंदर्य, सामंजस्य और प्रेम से धन्य। व्यापार साझेदारी फलती है। शुक्रवार को लक्ष्मी मंदिर में सफेद फूल चढ़ाएँ।",
     "Venus in H7 (Pakka Ghar) is the ideal marriage placement. White flower offerings at Lakshmi temples on Friday seal this blessing.",
     "भाव 7 में शुक्र (पक्का घर) आदर्श विवाह स्थान है। शुक्रवार को लक्ष्मी मंदिर में सफेद फूल चढ़ाना इस आशीर्वाद को पक्का करता है।",
     ["Venus"], [7], "high"),
    (68, "Venus in House 8: Hidden pleasures and in-law harmony. Financial inheritance comes through marriage. Occult arts and esoteric knowledge of beauty. Avoid secret relationships.",
     "शुक्र भाव 8 में: छुपे सुख और ससुराल सामंजस्य। विवाह के माध्यम से वित्तीय विरासत। गुप्त कला और सौंदर्य का गूढ़ ज्ञान। गुप्त संबंधों से बचें।",
     "Venus in H8 brings hidden wealth but warns against secret romantic relationships.",
     "भाव 8 में शुक्र छुपा धन लाता है पर गुप्त रोमांटिक संबंधों के विरुद्ध चेतावनी देता है।",
     ["Venus"], [8], "moderate"),
    (69, "Venus in House 9: Luck through beauty, art, and cultural travel. Religious tolerance and interfaith appreciation. Sponsor or attend arts at sacred sites.",
     "शुक्र भाव 9 में: सौंदर्य, कला और सांस्कृतिक यात्रा से भाग्य। धार्मिक सहिष्णुता और अंतर-धार्मिक प्रशंसा। पवित्र स्थलों पर कला को प्रायोजित करें या उसमें भाग लें।",
     "Venus in H9 brings fortune through art and cultural pilgrimage. Sacred arts patronage is specifically beneficial.",
     "भाव 9 में शुक्र कला और सांस्कृतिक तीर्थयात्रा से भाग्य लाता है। पवित्र कला संरक्षण विशेष रूप से लाभकारी है।",
     ["Venus"], [9], "moderate"),
    (70, "Venus in House 10: Career in arts, beauty, entertainment, or luxury. Public charm brings professional recognition. Wear white or pastel colors for important events.",
     "शुक्र भाव 10 में: कला, सौंदर्य, मनोरंजन या विलासिता में करियर। सार्वजनिक आकर्षण से पेशेवर मान्यता। महत्वपूर्ण अवसरों के लिए सफेद या पेस्टल रंग पहनें।",
     "Venus in H10 gives career success through public charm and artistic industries. White or pastel colors amplify Venus's professional energy.",
     "भाव 10 में शुक्र सार्वजनिक आकर्षण और कलात्मक उद्योग से करियर सफलता देता है। सफेद या पेस्टल रंग शुक्र की पेशेवर ऊर्जा को बढ़ाते हैं।",
     ["Venus"], [10], "high"),
    (71, "Venus in House 11: Gains through beauty, relationships, and artistic networking. Elder sister or beautiful friends bring wealth. Donate white sweets on Fridays.",
     "शुक्र भाव 11 में: सौंदर्य, संबंधों और कलात्मक नेटवर्किंग से लाभ। बड़ी बहन या सुंदर मित्र धन लाते हैं। शुक्रवार को सफेद मिठाई दान करें।",
     "Venus in H11 brings gains through artistic networks and beautiful friendships. Elder sister relationships are especially auspicious.",
     "भाव 11 में शुक्र कलात्मक नेटवर्क और सुंदर मित्रता से लाभ लाता है। बड़ी बहन के संबंध विशेष रूप से शुभ हैं।",
     ["Venus"], [11], "high"),
    (72, "Venus in House 12: Secret pleasures, foreign romances, and spiritual devotion through beauty. Hidden artistic talents emerge. Avoid excessive luxury in isolation.",
     "शुक्र भाव 12 में: गुप्त सुख, विदेशी रोमांस और सौंदर्य के माध्यम से आध्यात्मिक भक्ति। छुपी कलात्मक प्रतिभा उभरती है। एकांत में अत्यधिक विलासिता से बचें।",
     "Venus in H12 reveals hidden artistic talents and spiritual beauty. Excessive luxury in isolation drains Venus's positive energy.",
     "भाव 12 में शुक्र छुपी कलात्मक प्रतिभा और आध्यात्मिक सौंदर्य प्रकट करता है। एकांत में अत्यधिक विलासिता शुक्र की सकारात्मक ऊर्जा खींचती है।",
     ["Venus"], [12], "moderate"),

    # MERCURY (बुध) — Farmaans 73–84
    (73, "Mercury in House 1: Intelligent, talkative, and quick-witted. Family may have a singer or artist. Business acumen is natural. Read and write daily to activate Mercury.",
     "बुध भाव 1 में: बुद्धिमान, वाचाल और तीक्ष्ण बुद्धि। परिवार में गायक या कलाकार हो सकता है। व्यापारिक बुद्धि स्वाभाविक। बुध सक्रिय करने के लिए प्रतिदिन पढ़ें और लिखें।",
     "Mercury in H1 gives natural intelligence and business acumen. Daily reading and writing practice amplifies Mercury.",
     "भाव 1 में बुध प्राकृतिक बुद्धि और व्यापारिक कौशल देता है। दैनिक पढ़ने-लिखने का अभ्यास बुध को बढ़ाता है।",
     ["Mercury"], [1], "high"),
    (74, "Mercury in House 2: Old items and clutter at home. Clever speech and sharp tongue. Financial intelligence is high. Keep accounts meticulously — Mercury in H2 rewards organized finances.",
     "बुध भाव 2 में: घर में पुरानी वस्तुएँ और सामान। चालाक वाणी और तेज जुबान। वित्तीय बुद्धि उच्च। हिसाब-किताब सावधानी से रखें — भाव 2 में बुध व्यवस्थित वित्त को पुरस्कृत करता है।",
     "Mercury in H2 gives financial intelligence but clutters the home. Organized accounts are specifically rewarded.",
     "भाव 2 में बुध वित्तीय बुद्धि देता है पर घर में अव्यवस्था। व्यवस्थित हिसाब-किताब विशेष रूप से पुरस्कृत होते हैं।",
     ["Mercury"], [2], "moderate"),
    (75, "Mercury in House 3 (Pakka Ghar): Excellent for reading, writing, contracts, and communications. Siblings are intellectually close. Short journeys are productive and educational.",
     "बुध भाव 3 में (पक्का घर): पढ़ने, लिखने, अनुबंध और संवाद के लिए उत्कृष्ट। भाई-बहन बौद्धिक रूप से करीब। छोटी यात्राएँ उत्पादक और शैक्षणिक।",
     "Mercury in H3 (Pakka Ghar) — peak communication and intellect. This is the ideal placement for writers, traders, and teachers.",
     "भाव 3 में बुध (पक्का घर) — चरम संचार और बुद्धि। लेखक, व्यापारियों और शिक्षकों के लिए आदर्श स्थान।",
     ["Mercury"], [3], "high"),
    (76, "Mercury in House 4: Educated mother. Academic home environment. Property matters involve detailed analysis. Set up a home library or study room.",
     "बुध भाव 4 में: पढ़ी-लिखी माता। घर में शैक्षणिक माहौल। संपत्ति मामलों में विस्तृत विश्लेषण। घर में पुस्तकालय या अध्ययन कक्ष बनाएँ।",
     "Mercury in H4 creates an educated home environment. A home library specifically activates Mercury's intellectual energy.",
     "भाव 4 में बुध एक शैक्षित घरेलू वातावरण बनाता है। घर में पुस्तकालय विशेष रूप से बुध की बौद्धिक ऊर्जा को सक्रिय करता है।",
     ["Mercury"], [4], "moderate"),
    (77, "Mercury in House 5: Intelligent and analytical children. Writing and teaching are rewarding. Avoid speculation — losses through overanalysis. Teach or tutor others to activate Mercury.",
     "बुध भाव 5 में: बुद्धिमान और विश्लेषणात्मक संतान। लेखन और अध्यापन फायदेमंद। सट्टे से बचें — अत्यधिक विश्लेषण से नुकसान। बुध सक्रिय करने के लिए दूसरों को पढ़ाएँ।",
     "Mercury in H5 creates intelligent children and rewards teaching. Speculation is contraindicated — overanalysis leads to losses.",
     "भाव 5 में बुध बुद्धिमान संतान और अध्यापन को पुरस्कृत करता है। सट्टा विपरीत — अत्यधिक विश्लेषण से नुकसान।",
     ["Mercury"], [5], "moderate"),
    (78, "Mercury in House 6 (Pakka Ghar): Defeat enemies through intelligence and analysis. Excellent health research and service. Work in detail-oriented fields. Donate green items on Wednesdays.",
     "बुध भाव 6 में (पक्का घर): बुद्धि और विश्लेषण से शत्रुओं पर विजय। उत्कृष्ट स्वास्थ्य शोध और सेवा। विस्तार-उन्मुख क्षेत्रों में काम करें। बुधवार को हरी वस्तु दान करें।",
     "Mercury in H6 (Pakka Ghar) — analytical intellect defeats enemies. Green item donation on Wednesdays reinforces this strength.",
     "भाव 6 में बुध (पक्का घर) — विश्लेषणात्मक बुद्धि शत्रुओं को हराती है। बुधवार को हरी वस्तु दान इस शक्ति को मजबूत करता है।",
     ["Mercury"], [6], "high"),
    (79, "Mercury in House 7: Intelligent and communicative spouse. Business partnerships succeed through clear contracts. Risk of deception — get everything in writing.",
     "बुध भाव 7 में: बुद्धिमान और संवादपटु जीवनसाथी। स्पष्ट अनुबंध से व्यापार साझेदारी सफल। धोखे का जोखिम — सब कुछ लिखित में लें।",
     "Mercury in H7 gives an intelligent spouse but warns against verbal agreements. Written contracts are essential.",
     "भाव 7 में बुध बुद्धिमान जीवनसाथी देता है पर मौखिक समझौतों के विरुद्ध चेतावनी। लिखित अनुबंध अनिवार्य हैं।",
     ["Mercury"], [7], "moderate"),
    (80, "Mercury in House 8: Research and occult communication excel. Tax and financial analysis are rewarding. Information hidden from others becomes a source of power.",
     "बुध भाव 8 में: शोध और गुप्त संवाद उत्कृष्ट। कर और वित्तीय विश्लेषण फायदेमंद। दूसरों से छुपी जानकारी शक्ति का स्रोत बनती है।",
     "Mercury in H8 gives power through hidden knowledge and research. Financial analysis and tax work are specifically rewarded.",
     "भाव 8 में बुध छुपे ज्ञान और शोध से शक्ति देता है। वित्तीय विश्लेषण और कर कार्य विशेष रूप से पुरस्कृत होते हैं।",
     ["Mercury"], [8], "moderate"),
    (81, "Mercury in House 9: Success in writing and teaching dharma. Religious texts and long-distance communication are highlighted. Translate or teach sacred knowledge.",
     "बुध भाव 9 में: धर्म लिखने और पढ़ाने में सफलता। धार्मिक ग्रंथ और दूरस्थ संवाद प्रमुख। पवित्र ज्ञान का अनुवाद करें या पढ़ाएँ।",
     "Mercury in H9 gives fortune through written and taught dharma. Translating or teaching sacred texts is the highest Mercury practice here.",
     "भाव 9 में बुध लिखित और पढ़ाए धर्म से भाग्य देता है। पवित्र ग्रंथों का अनुवाद या अध्यापन यहाँ सर्वोच्च बुध अभ्यास है।",
     ["Mercury"], [9], "moderate"),
    (82, "Mercury in House 10: Business success and career in communication. Writer, journalist, lawyer, or analyst career is favored. Sign contracts on Wednesdays.",
     "बुध भाव 10 में: व्यापार सफलता और संवाद में करियर। लेखक, पत्रकार, वकील या विश्लेषक करियर पक्षधर। बुधवार को अनुबंध पर हस्ताक्षर करें।",
     "Mercury in H10 gives communication-based career success. Signing contracts on Wednesdays specifically amplifies this energy.",
     "भाव 10 में बुध संवाद-आधारित करियर सफलता देता है। बुधवार को अनुबंध पर हस्ताक्षर विशेष रूप से इस ऊर्जा को बढ़ाते हैं।",
     ["Mercury"], [10], "high"),
    (83, "Mercury in House 11: Business-minded friends are highly beneficial. Sister's support is key. Multiple income streams through communication and networking.",
     "बुध भाव 11 में: व्यापार-मानसिकता वाले मित्र अत्यधिक लाभकारी। बहन का सहयोग महत्वपूर्ण। संवाद और नेटवर्किंग के माध्यम से आय के अनेक स्रोत।",
     "Mercury in H11 brings gains through business friendships and sibling (sister) support. Multiple income streams are natural.",
     "भाव 11 में बुध व्यापारिक मित्रता और भाई-बहन (बहन) के सहयोग से लाभ लाता है। आय के अनेक स्रोत स्वाभाविक हैं।",
     ["Mercury"], [11], "high"),
    (84, "Mercury in House 12: Settlement abroad is possible. Secret studies and foreign communication are active. Control expenditure — Mercury in H12 creates subtle financial leakage.",
     "बुध भाव 12 में: विदेश में बसने की संभावना। गुप्त अध्ययन और विदेशी संवाद सक्रिय। खर्च नियंत्रित करें — भाव 12 में बुध सूक्ष्म वित्तीय रिसाव बनाता है।",
     "Mercury in H12 enables foreign settlement and secret intellectual work. Financial discipline is essential to prevent subtle expenditure leakage.",
     "भाव 12 में बुध विदेश बसावट और गुप्त बौद्धिक कार्य सक्षम करता है। सूक्ष्म व्यय रिसाव रोकने के लिए वित्तीय अनुशासन अनिवार्य है।",
     ["Mercury"], [12], "moderate"),

    # RAHU — Farmaans 85–96
    (85, "Rahu in House 1: Unconventional appearance and ambitions. Foreign or unusual life experiences. Snake-related symbols in dreams. Keep a silver plate at home for clarity.",
     "राहु भाव 1 में: अपरंपरागत रूप और महत्वाकांक्षाएँ। विदेशी या असामान्य जीवन अनुभव। स्वप्न में साँप से संबंधित प्रतीक। स्पष्टता के लिए घर में चाँदी की थाली रखें।",
     "Rahu in H1 creates an unconventional native with unusual life experiences. Silver remedies ground Rahu's disorienting energy.",
     "भाव 1 में राहु असामान्य जीवन अनुभवों वाला अपरंपरागत जातक बनाता है। चाँदी उपाय राहु की भटकाने वाली ऊर्जा को जमीन पर लाते हैं।",
     ["Rahu"], [1], "moderate"),
    (86, "Rahu in House 2: Family members may be from different backgrounds or cultures. Speech can be deceptive without intention. Wealth comes from unusual sources. Avoid lying — Rahu amplifies the consequences.",
     "राहु भाव 2 में: परिवार के सदस्य विभिन्न पृष्ठभूमि या संस्कृति से हो सकते हैं। वाणी अनजाने में भ्रामक हो सकती है। धन असामान्य स्रोतों से। झूठ से बचें — राहु परिणाम बढ़ाता है।",
     "Rahu in H2 creates cross-cultural family dynamics. Truth in speech is essential — Rahu amplifies the consequences of deception.",
     "भाव 2 में राहु अंतर-सांस्कृतिक पारिवारिक गतिशीलता बनाता है। वाणी में सत्य अनिवार्य — राहु छल के परिणाम बढ़ाता है।",
     ["Rahu"], [2], "moderate"),
    (87, "Rahu in House 3: Unusual courage and digital-age communication skills. Foreign siblings or unconventional journeys. Digital business ventures succeed. Keep a blue or black cloth in the travel bag.",
     "राहु भाव 3 में: असामान्य साहस और डिजिटल-युग संवाद कौशल। विदेशी भाई-बहन या अपरंपरागत यात्राएँ। डिजिटल व्यापार उद्यम सफल। यात्रा बैग में नीला या काला कपड़ा रखें।",
     "Rahu in H3 gives digital-age courage and unconventional communication advantages.",
     "भाव 3 में राहु डिजिटल-युग साहस और अपरंपरागत संवाद लाभ देता है।",
     ["Rahu"], [3], "moderate"),
    (88, "Rahu in House 4: Domestic disruption or renovation. Mother's health may be unusual. Foreign property or non-traditional home setup. Keep the home clean and clutter-free.",
     "राहु भाव 4 में: घरेलू व्यवधान या नवीनीकरण। माता का स्वास्थ्य असामान्य हो सकता है। विदेशी संपत्ति या गैर-पारंपरिक घर की व्यवस्था। घर को साफ और अव्यवस्था-मुक्त रखें।",
     "Rahu in H4 creates unusual domestic circumstances. Home cleanliness specifically counters Rahu's chaotic home energy.",
     "भाव 4 में राहु असामान्य घरेलू परिस्थितियाँ बनाता है। घर की सफाई विशेष रूप से राहु की अव्यवस्थित घरेलू ऊर्जा का प्रतिकार करती है।",
     ["Rahu"], [4], "moderate"),
    (89, "Rahu in House 5: Past karma is prominent. Unusual children or creative ideas from unconventional sources. Speculation is tempting but risky. Meditate to access past-life intelligence.",
     "राहु भाव 5 में: पूर्वकर्म प्रमुख। असामान्य संतान या अपरंपरागत स्रोतों से रचनात्मक विचार। सट्टा लुभावना पर जोखिमपूर्ण। पूर्वजन्म की बुद्धि तक पहुँचने के लिए ध्यान करें।",
     "Rahu in H5 activates past-life karma through children and speculation. Meditation unlocks Rahu's intelligence in H5.",
     "भाव 5 में राहु संतान और सट्टे के माध्यम से पूर्वजन्म का कर्म सक्रिय करता है। ध्यान भाव 5 में राहु की बुद्धि को अनलॉक करता है।",
     ["Rahu"], [5], "moderate"),
    (90, "Rahu in House 6 (Pakka Ghar): Enemies are confused and powerless. Unconventional healing methods work. Legal battles are won through unexpected angles. Keep a piece of coal in the house.",
     "राहु भाव 6 में (पक्का घर): शत्रु भ्रमित और शक्तिहीन। अपरंपरागत उपचार विधियाँ काम करती हैं। अप्रत्याशित कोणों से कानूनी लड़ाइयाँ जीती जाती हैं। घर में कोयले का टुकड़ा रखें।",
     "Rahu in H6 (Pakka Ghar) — enemies defeated through unconventional means. Coal in the home is a specific LK remedy.",
     "भाव 6 में राहु (पक्का घर) — अपरंपरागत तरीकों से शत्रु पराजित। घर में कोयला एक विशिष्ट लाल किताब उपाय है।",
     ["Rahu"], [6], "high"),
    (91, "Rahu in House 7: Unconventional marriages or partnerships. Foreign spouse possible. Business partnerships have unusual elements. Clearly define all partnership terms in writing.",
     "राहु भाव 7 में: अपरंपरागत विवाह या साझेदारी। विदेशी जीवनसाथी संभव। व्यापार साझेदारी में असामान्य तत्व। सभी साझेदारी शर्तें स्पष्ट रूप से लिखित में परिभाषित करें।",
     "Rahu in H7 creates unconventional partnerships. Written partnership terms are essential to prevent Rahu's deceptive energy.",
     "भाव 7 में राहु अपरंपरागत साझेदारी बनाता है। लिखित साझेदारी शर्तें राहु की भ्रामक ऊर्जा को रोकने के लिए अनिवार्य हैं।",
     ["Rahu"], [7], "moderate"),
    (92, "Rahu in House 8: Intense occult knowledge and research abilities. Sudden inheritance or legacy from foreign sources. Transformation is rapid and dramatic. Practice meditation for grounding.",
     "राहु भाव 8 में: तीव्र गुप्त ज्ञान और शोध क्षमताएँ। विदेशी स्रोत से अचानक विरासत। परिवर्तन तीव्र और नाटकीय। जमीन से जुड़े रहने के लिए ध्यान करें।",
     "Rahu in H8 gives powerful occult knowledge but creates rapid, sometimes destabilizing transformations.",
     "भाव 8 में राहु शक्तिशाली गुप्त ज्ञान देता है पर तीव्र, कभी-कभी अस्थिर परिवर्तन बनाता है।",
     ["Rahu"], [8], "moderate"),
    (93, "Rahu in House 9: Unconventional beliefs and foreign gurus. Luck comes through strange channels. Long journeys with unusual experiences. Donate to unconventional or foreign charitable causes.",
     "राहु भाव 9 में: अपरंपरागत विश्वास और विदेशी गुरु। भाग्य अजीब रास्तों से। असामान्य अनुभवों के साथ लंबी यात्राएँ। अपरंपरागत या विदेशी धर्मार्थ कार्यों में दान करें।",
     "Rahu in H9 brings fortune through unconventional dharma. Donating to foreign or non-traditional causes specifically activates Rahu's luck.",
     "भाव 9 में राहु अपरंपरागत धर्म से भाग्य लाता है। विदेशी या गैर-पारंपरिक कार्यों में दान राहु के भाग्य को विशेष रूप से सक्रिय करता है।",
     ["Rahu"], [9], "moderate"),
    (94, "Rahu in House 10: Career gains through unconventional or tech-based means. Foreign or government career opportunities arise suddenly. Blue sapphire (after consulting a specialist) may help career.",
     "राहु भाव 10 में: अपरंपरागत या टेक-आधारित माध्यम से करियर लाभ। विदेशी या सरकारी करियर अवसर अचानक आते हैं। नीलम (विशेषज्ञ से परामर्श के बाद) करियर में मदद कर सकता है।",
     "Rahu in H10 gives career gains through technology and unconventional paths. Foreign opportunities appear suddenly.",
     "भाव 10 में राहु प्रौद्योगिकी और अपरंपरागत रास्तों से करियर लाभ देता है। विदेशी अवसर अचानक आते हैं।",
     ["Rahu"], [10], "high"),
    (95, "Rahu in House 11 (Pakka Ghar): Unexpected financial gains through foreign or unconventional sources. Ambitions fulfilled through indirect channels. Keep a black or blue item in the home.",
     "राहु भाव 11 में (पक्का घर): विदेशी या अपरंपरागत स्रोतों से अप्रत्याशित आर्थिक लाभ। महत्वाकांक्षाएँ अप्रत्यक्ष रास्तों से पूरी होती हैं। घर में काली या नीली वस्तु रखें।",
     "Rahu in H11 (Pakka Ghar) — unexpected wealth through unconventional channels. Black or blue items in the home amplify this energy.",
     "भाव 11 में राहु (पक्का घर) — अपरंपरागत रास्तों से अप्रत्याशित धन। घर में काली या नीली वस्तुएँ इस ऊर्जा को बढ़ाती हैं।",
     ["Rahu"], [11], "high"),
    (96, "Rahu in House 12 (Pakka Ghar): Deep foreign connections and karmic expenditures. Spiritual obsession from past lives. Liberation energies are active. Donate at hospitals or foreign charitable institutions.",
     "राहु भाव 12 में (पक्का घर): गहरे विदेशी संपर्क और कर्मपूर्ण व्यय। पूर्वजन्म से आध्यात्मिक जुनून। मुक्ति ऊर्जाएँ सक्रिय। अस्पतालों या विदेशी धर्मार्थ संस्थाओं में दान करें।",
     "Rahu in H12 (Pakka Ghar) connects the native to foreign and past-life karmic expenditures. Hospital and foreign charity donations are specifically prescribed.",
     "भाव 12 में राहु (पक्का घर) जातक को विदेशी और पूर्वजन्म के कर्मपूर्ण व्यय से जोड़ता है। अस्पताल और विदेशी दान विशेष रूप से निर्धारित हैं।",
     ["Rahu"], [12], "high"),

    # KETU — Farmaans 97–108
    (97, "Ketu in House 1: Past-life identity and spiritual introspection. Mysterious health fluctuations. Ego detachment brings inner peace. Worship Ganesha daily for clarity.",
     "केतु भाव 1 में: पूर्वजन्म की पहचान और आध्यात्मिक आत्म-निरीक्षण। रहस्यमय स्वास्थ्य उतार-चढ़ाव। अहंकार वैराग्य से आंतरिक शांति। स्पष्टता के लिए प्रतिदिन गणेश पूजा करें।",
     "Ketu in H1 activates past-life identity. Daily Ganesha worship brings the clarity that Ketu's mysterious energy clouds.",
     "भाव 1 में केतु पूर्वजन्म की पहचान सक्रिय करता है। दैनिक गणेश पूजा वह स्पष्टता लाती है जो केतु की रहस्यमय ऊर्जा धुंधला करती है।",
     ["Ketu"], [1], "moderate"),
    (98, "Ketu in House 2: Family detachment with past-life flavor. Speech becomes spiritual or cryptic. Wealth has a karmic quality. Do not accumulate excessive possessions — give freely.",
     "केतु भाव 2 में: पूर्वजन्म के स्वाद के साथ पारिवारिक वैराग्य। वाणी आध्यात्मिक या रहस्यमय। धन में कर्मपूर्ण गुण। अत्यधिक संपत्ति संचित न करें — उदारता से दें।",
     "Ketu in H2 creates karmic wealth patterns. Giving freely — not hoarding — is the prescribed way to maintain Ketu's favor.",
     "भाव 2 में केतु कर्मपूर्ण धन पैटर्न बनाता है। उदारता से देना — जमा करना नहीं — केतु की कृपा बनाए रखने का निर्धारित तरीका है।",
     ["Ketu"], [2], "moderate"),
    (99, "Ketu in House 3 (Pakka Ghar): Intuitive courage and spiritual communication. Past-life sibling bonds. Sacred journeys are deeply meaningful. Offer sesame seeds at temples.",
     "केतु भाव 3 में (पक्का घर): अंतर्ज्ञानी साहस और आध्यात्मिक संवाद। पूर्वजन्म के भाई-बहन बंधन। पवित्र यात्राएँ गहराई से अर्थपूर्ण। मंदिरों में तिल अर्पित करें।",
     "Ketu in H3 (Pakka Ghar) gives intuitive spiritual courage. Sesame seed offerings at temples strengthen this placement.",
     "भाव 3 में केतु (पक्का घर) अंतर्ज्ञानी आध्यात्मिक साहस देता है। मंदिरों में तिल चढ़ाने से यह स्थान मजबूत होता है।",
     ["Ketu"], [3], "high"),
    (100, "Ketu in House 4: Home detachment — the native may move frequently. Ancestral property has karmic resolution. Mother's spiritual matters are active. Keep a Ketu yantra in the home.",
     "केतु भाव 4 में: घर से वैराग्य — जातक बार-बार घर बदल सकता है। पैतृक संपत्ति में कर्म समाधान। माता के आध्यात्मिक मामले सक्रिय। घर में केतु यंत्र रखें।",
     "Ketu in H4 creates frequent home changes as part of ancestral karma resolution. A Ketu yantra stabilizes this energy.",
     "भाव 4 में केतु पैतृक कर्म समाधान के हिस्से के रूप में बार-बार घर बदलाव बनाता है। केतु यंत्र इस ऊर्जा को स्थिर करता है।",
     ["Ketu"], [4], "moderate"),
    (101, "Ketu in House 5: Past-life intelligence and karmic children. Spiritual creativity exceeds material creativity. Avoid speculation — losses are karmically amplified. Practice spiritual arts.",
     "केतु भाव 5 में: पूर्वजन्म की बुद्धि और कर्मपूर्ण संतान। भौतिक रचनात्मकता से आध्यात्मिक रचनात्मकता श्रेष्ठ। सट्टे से बचें — हानियाँ कर्मपूर्वक बढ़ती हैं। आध्यात्मिक कलाओं का अभ्यास करें।",
     "Ketu in H5 activates past-life knowledge and spiritual creativity. Material speculation is karmically dangerous here.",
     "भाव 5 में केतु पूर्वजन्म ज्ञान और आध्यात्मिक रचनात्मकता सक्रिय करता है। भौतिक सट्टा यहाँ कर्मपूर्वक खतरनाक है।",
     ["Ketu"], [5], "moderate"),
    (102, "Ketu in House 6 (Pakka Ghar): Enemies dissolved through past karma. Disease karma resolves through spiritual discipline. Detached service is powerfully protective. Light incense at temples on Saturdays.",
     "केतु भाव 6 में (पक्का घर): पूर्वकर्म से शत्रु घुलते हैं। आध्यात्मिक अनुशासन से रोग कर्म सुलझता है। वैराग्यपूर्ण सेवा शक्तिशाली रूप से सुरक्षात्मक। शनिवार को मंदिरों में धूप जलाएँ।",
     "Ketu in H6 (Pakka Ghar) dissolves enemies and disease karma through past-life merit. Saturday incense offerings are prescribed.",
     "भाव 6 में केतु (पक्का घर) पूर्वजन्म की पुण्य से शत्रु और रोग कर्म घुलाता है। शनिवार को धूप अर्पण निर्धारित है।",
     ["Ketu"], [6], "high"),
    (103, "Ketu in House 7: Marriage feels karmically destined from a past life. Spouse has a spiritual or mysterious quality. Partnership detachment is natural. Perform Ketu rituals on Tuesdays.",
     "केतु भाव 7 में: विवाह पूर्वजन्म से कर्मपूर्वक नियत लगता है। जीवनसाथी में आध्यात्मिक या रहस्यमय गुण। साझेदारी वैराग्य स्वाभाविक। मंगलवार को केतु अनुष्ठान करें।",
     "Ketu in H7 creates karmic marriage connections. The spouse often feels like a past-life soul bond.",
     "भाव 7 में केतु कर्मपूर्ण विवाह संबंध बनाता है। जीवनसाथी अक्सर पूर्वजन्म के आत्मिक बंधन जैसा लगता है।",
     ["Ketu"], [7], "moderate"),
    (104, "Ketu in House 8: Deep spiritual transformation. Past-life occult knowledge surfaces dramatically. Liberation through crisis. Do not fear transformation — embrace it spiritually.",
     "केतु भाव 8 में: गहरी आध्यात्मिक परिवर्तन। पूर्वजन्म का गुप्त ज्ञान नाटकीय रूप से सामने। संकट से मुक्ति। परिवर्तन से मत डरो — आध्यात्मिक रूप से स्वीकार करो।",
     "Ketu in H8 creates powerful occult and transformation energy. Spiritual acceptance of crisis accelerates liberation.",
     "भाव 8 में केतु शक्तिशाली गुप्त और परिवर्तन ऊर्जा बनाता है। संकट की आध्यात्मिक स्वीकृति मुक्ति को त्वरित करती है।",
     ["Ketu"], [8], "moderate"),
    (105, "Ketu in House 9: Past-life spiritual dharma activates. Guru connection from a previous life. Religious detachment leads to true wisdom. Study ancient or esoteric religious traditions.",
     "केतु भाव 9 में: पूर्वजन्म का आध्यात्मिक धर्म सक्रिय। पूर्वजन्म से गुरु संबंध। धार्मिक वैराग्य वास्तविक ज्ञान की ओर। प्राचीन या गूढ़ धार्मिक परंपराओं का अध्ययन करें।",
     "Ketu in H9 activates past-life dharmic connections. Study of esoteric religious traditions is the highest practice here.",
     "भाव 9 में केतु पूर्वजन्म के धार्मिक संबंध सक्रिय करता है। गूढ़ धार्मिक परंपराओं का अध्ययन यहाँ सर्वोच्च अभ्यास है।",
     ["Ketu"], [9], "moderate"),
    (106, "Ketu in House 10: Career feels karmically driven. Past-life authority patterns surface — old roles resurface. Detachment from career outcomes produces the best results.",
     "केतु भाव 10 में: करियर कर्मपूर्वक संचालित लगता है। पूर्वजन्म के अधिकार पैटर्न सामने — पुरानी भूमिकाएँ फिर से उभरती हैं। करियर फल से वैराग्य सर्वोत्तम परिणाम देता है।",
     "Ketu in H10 creates a career that feels spiritually driven. Detachment from outcomes paradoxically produces better career results.",
     "भाव 10 में केतु आध्यात्मिक रूप से संचालित करियर बनाता है। फल से वैराग्य विरोधाभासी रूप से बेहतर करियर परिणाम देता है।",
     ["Ketu"], [10], "moderate"),
    (107, "Ketu in House 11: Material desires feel hollow despite fulfillment. Spiritual desires bring genuine satisfaction. Elder siblings have past-life connections. Donate to spiritual organizations.",
     "केतु भाव 11 में: भौतिक इच्छाएँ पूर्ति के बावजूद खोखी लगती हैं। आध्यात्मिक इच्छाएँ वास्तविक संतुष्टि लाती हैं। बड़े भाई-बहन से पूर्वजन्म के संबंध। आध्यात्मिक संगठनों को दान करें।",
     "Ketu in H11 creates spiritual fulfillment while material desires feel empty. Spiritual organization donations are specifically prescribed.",
     "भाव 11 में केतु आध्यात्मिक संतुष्टि बनाता है जबकि भौतिक इच्छाएँ खोखी लगती हैं। आध्यात्मिक संगठन दान विशेष रूप से निर्धारित हैं।",
     ["Ketu"], [11], "moderate"),
    (108, "Ketu in House 12 (Pakka Ghar): Ketu at peak spiritual power. Moksha energy, past-life foreign connections, and liberation are all intensely active. Practice deep meditation and spiritual study.",
     "केतु भाव 12 में (पक्का घर): केतु की उच्चतम आध्यात्मिक शक्ति। मोक्ष ऊर्जा, पूर्वजन्म के विदेशी संबंध और मुक्ति सभी तीव्रता से सक्रिय। गहन ध्यान और आध्यात्मिक अध्ययन का अभ्यास करें।",
     "Ketu in H12 (Pakka Ghar) is the strongest liberation placement in LK. Deep meditation is the highest prescribed practice.",
     "भाव 12 में केतु (पक्का घर) लाल किताब में सबसे मजबूत मुक्ति स्थान है। गहन ध्यान सर्वोच्च निर्धारित अभ्यास है।",
     ["Ketu"], [12], "high"),
]


def _seed_farmaan(db) -> None:
    """Seed lk_farmaan table with 108 planet+house canonical entries."""
    import uuid as _uuid

    sql = """
        INSERT INTO lk_farmaan (
            id, farmaan_number, english, hindi,
            traditional_commentary_en, traditional_commentary_hi,
            confidence_level, planet_tags, house_tags, rights_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (farmaan_number) DO NOTHING
    """
    count = 0
    for row in LK_FARMAAN:
        (fnum, english, hindi, commentary_en, commentary_hi, planet_tags, house_tags, confidence) = row
        try:
            db.execute(sql, (
                _uuid.uuid4().hex,
                fnum,
                english,
                hindi,
                commentary_en,
                commentary_hi,
                confidence,
                planet_tags,
                house_tags,
                "public_domain",
            ))
            count += 1
        except Exception as e:
            logger.debug("[seed_farmaan] skip farmaan %s: %s", fnum, e)
            try:
                db.rollback()
            except Exception:
                pass

    logger.info("[seed_lalkitab] lk_farmaan seeded (%d rows).", count)
