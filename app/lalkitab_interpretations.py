"""
lalkitab_interpretations.py — Lal Kitab House-by-House Planet Interpretations
==============================================================================
Contains VALIDATED per-house interpretations for all 9 planets (108 total)
plus a validated remedy system with specific procedural remedies.

Sources:
  - Lal Kitab (1941 original text)
  - Lal Kitab Ke Farmaan (Pt. Roop Chand Joshi)
  - AstroSage Lal Kitab ebook
  - Audio lecture transcriptions (Advance series)
"""

from typing import Any, Dict, List, Optional

# ============================================================
# PLANET-HOUSE INTERPRETATIONS (9 planets x 12 houses = 108)
# ============================================================

LK_PLANET_HOUSE_INTERPRETATIONS: Dict[str, Dict[int, Dict[str, Any]]] = {

    # ─────────────────────────────────────────────────────────
    # JUPITER (Brihaspati / Guru) — Planet of Kismat
    # ─────────────────────────────────────────────────────────
    "Jupiter": {
        1: {
            "nature": "raja_or_fakir",
            "effect_en": "Jupiter in House 1 makes the native illustrious as a king. Good looking, learned, fond of wearing good clothes and sweet foods. Succeeds over enemies. Must pursue higher education to activate fortune.",
            "effect_hi": "बृहस्पति प्रथम भाव में हो तो जातक राजा के समान प्रतापी होता है। विद्वान, सुंदर, मीठे भोजन का शौकीन। शत्रुओं पर विजय। उच्च शिक्षा से किस्मत जागती है।",
            "conditions": "Must pursue graduation/degree to activate fortune. If afflicted, behaves like a fakir instead.",
            "keywords": ["kismat", "raja", "vidya", "degree"],
        },
        2: {
            "nature": "raja",
            "effect_en": "Jupiter in House 2 creates a 'Jagat Guru' — if good, will uplift the world. Wealth accumulates, speech becomes golden. Family prospers across generations.",
            "effect_hi": "बृहस्पति दूसरे भाव में 'जगत गुरु' बनाता है। धन संचय, वाणी प्रभावशाली। परिवार पीढ़ियों तक फलता-फूलता है।",
            "conditions": "If afflicted, entire family (khandan) suffers instead.",
            "keywords": ["jagat_guru", "dhan", "khandan", "vaani"],
        },
        3: {
            "nature": "mixed",
            "effect_en": "Jupiter in House 3 gets strongly affected by Mercury's influence. The native may have fluctuating fortune tied to siblings and short travels. Chandra-based remedies work best to stabilize this placement.",
            "effect_hi": "बृहस्पति तीसरे भाव में बुध के प्रभाव से प्रभावित होता है। भाई-बहनों और छोटी यात्राओं से किस्मत जुड़ी रहती है। चंद्रमा आधारित उपाय सबसे अच्छे काम करते हैं।",
            "conditions": "Mercury's condition directly impacts Jupiter here. Strengthen Moon for best results.",
            "keywords": ["budh", "chandra", "bhai", "yatra"],
        },
        4: {
            "nature": "raja_or_fakir",
            "effect_en": "Jupiter in House 4 is exalted (Uchcha). Like Raja Indra or Vikramaditya — enormous power, property, vehicles, mother's blessings. BUT if afflicted, leads to self-destruction. Never assume automatically great.",
            "effect_hi": "बृहस्पति चौथे भाव में उच्च का है। राजा इंद्र/विक्रमादित्य जैसा — अपार शक्ति, संपत्ति, वाहन, माता का आशीर्वाद। लेकिन पीड़ित हो तो आत्म-विनाश। स्वतः अच्छा न मानें।",
            "conditions": "Exalted position but enemies in 2/5/9/12 can destroy it completely. Check for Budh, Shukra, Rahu, Ketu, Shani in those houses.",
            "keywords": ["uchcha", "raja_indra", "vikramaditya", "maa"],
        },
        5: {
            "nature": "mixed",
            "effect_en": "Jupiter in House 5 means fortune changes from the day a child is born. If a son is born on Thursday, fortune may reverse. Speculative gains possible but risky. Education and children define luck.",
            "effect_hi": "बृहस्पति पांचवें भाव में हो तो किस्मत बच्चे के जन्म के दिन से बदलती है। गुरुवार को पुत्र जन्म हो तो किस्मत पलट सकती है। सट्टे से लाभ संभव पर जोखिम भी। शिक्षा और संतान से भाग्य तय।",
            "conditions": "If afflicted, birth complications or children bring misfortune. Son born on Thursday = fortune reversal.",
            "keywords": ["santaan", "thursday", "vidya", "satta"],
        },
        6: {
            "nature": "manda",
            "effect_en": "Jupiter in House 6 is manda (weak). The native must work extremely hard for everything. Rarely born rich — struggles with enemies, debts, and health. Service to others is the path.",
            "effect_hi": "बृहस्पति छठे भाव में मंदा (कमज़ोर) है। जातक को हर चीज़ के लिए अत्यधिक मेहनत करनी पड़ती है। शायद ही अमीर घर में जन्म — शत्रु, कर्ज़, स्वास्थ्य से संघर्ष। सेवा ही मार्ग है।",
            "conditions": "Must serve others to activate any fortune. Avoid arrogance completely.",
            "keywords": ["manda", "mehnat", "seva", "karz"],
        },
        7: {
            "nature": "mixed",
            "effect_en": "Jupiter in House 7 makes the native head of dharmic or religious work. Marriage brings fortune. CRITICAL: never reveal financial struggles publicly. If suffering is displayed publicly, more pain follows.",
            "effect_hi": "बृहस्पति सातवें भाव में जातक को धार्मिक/धर्म कार्य का प्रमुख बनाता है। विवाह से भाग्य आता है। महत्वपूर्ण: आर्थिक संघर्ष कभी सार्वजनिक न करें। दुख दिखाओगे तो और दुख आएगा।",
            "conditions": "Never display suffering publicly — brings more suffering. Keep financial problems private.",
            "keywords": ["dharma", "vivah", "gupt", "izzat"],
        },
        8: {
            "nature": "mixed",
            "effect_en": "Jupiter in House 8: 'Sone ki Lanka takka daani' (donor of golden Lanka). Inherited wealth is useless — must earn independently. Never work with father or grandfather's business. Self-made success only.",
            "effect_hi": "बृहस्पति आठवें भाव में: 'सोने की लंका टक्का दानी'। विरासत में मिला धन बेकार — स्वयं कमाना होगा। पिता/दादा के व्यापार में कभी काम न करें। केवल स्वनिर्मित सफलता।",
            "conditions": "Inherited wealth useless. Must work independently. Don't join father/grandfather's business.",
            "keywords": ["sone_ki_lanka", "swanirbhar", "virasat", "ashtam"],
        },
        9: {
            "nature": "raja",
            "effect_en": "Jupiter in House 9 brings fortune through father's blessings. Religious pilgrimages bring wealth and prosperity. The native is naturally lucky, spiritually inclined, and respected by society.",
            "effect_hi": "बृहस्पति नौवें भाव में पिता के आशीर्वाद से भाग्य। धार्मिक तीर्थयात्रा से धन-समृद्धि। जातक स्वाभाविक रूप से भाग्यशाली, आध्यात्मिक और समाज में सम्मानित।",
            "conditions": "If afflicted, father's ill health or strained father relationship. Pilgrimages still help.",
            "keywords": ["pita", "tirth", "bhagya", "dharma"],
        },
        10: {
            "nature": "mixed",
            "effect_en": "Jupiter in House 10 is debilitated BUT 'Jis kadar bhi teda chale, mitti sona degi' (however crookedly you walk, earth gives gold). Not necessarily bad — career brings fortune if no malefic aspects.",
            "effect_hi": "बृहस्पति दसवें भाव में नीच है लेकिन 'जिस कदर भी टेढ़ा चले, मिट्टी सोना देगी'। ज़रूरी नहीं कि बुरा हो — कैरियर से भाग्य आता है अगर कोई पापी दृष्टि न हो।",
            "conditions": "Debilitated but compensated by karma. Not bad if no malefic aspect. Hard work always pays.",
            "keywords": ["neech", "karma", "mitti_sona", "career"],
        },
        11: {
            "nature": "raja",
            "effect_en": "Jupiter in House 11: 'Saap bhi sajda kare' (even snakes bow). Enormous gains and social respect. CONDITION: must maintain family ties. Day family bonds break = everything collapses.",
            "effect_hi": "बृहस्पति ग्यारहवें भाव में: 'सांप भी सजदा करे'। अपार लाभ और सामाजिक सम्मान। शर्त: परिवार से संबंध बनाए रखने होंगे। जिस दिन परिवार से नाता टूटा = सब बर्बाद।",
            "conditions": "Must maintain family ties. If family bonds break, everything collapses. Remedy: donate kafan.",
            "keywords": ["saap_sajda", "labh", "parivar", "kafan"],
        },
        12: {
            "nature": "manda",
            "effect_en": "Jupiter in House 12 brings poverty and hardship cycle. Connection to pataal (underworld energy). Air/breath weakens — respiratory issues possible. Spiritual inclination but material suffering.",
            "effect_hi": "बृहस्पति बारहवें भाव में गरीबी और कष्ट का चक्र। पाताल से संबंध। हवा/सांस कमज़ोर — श्वसन समस्या संभव। आध्यात्मिक रुझान लेकिन भौतिक कष्ट।",
            "conditions": "Poverty cycle. Breath/air element weakens. Spiritual gains but material losses.",
            "keywords": ["pataal", "gareebi", "saans", "vyay"],
        },
    },

    # ─────────────────────────────────────────────────────────
    # MOON (Chandra) — Planet of Mind & Mother
    # ─────────────────────────────────────────────────────────
    "Moon": {
        1: {
            "nature": "raja",
            "effect_en": "Moon in House 1 gives a royal and attractive personality. The native is imaginative, emotionally strong, popular among people. Mother's influence shapes destiny. Wealth through public dealings.",
            "effect_hi": "चंद्रमा प्रथम भाव में राजसी और आकर्षक व्यक्तित्व देता है। जातक कल्पनाशील, भावनात्मक रूप से मज़बूत, लोगों में लोकप्रिय। माता का प्रभाव भाग्य गढ़ता है। जनता से धन।",
            "conditions": "Good for public dealing and government work. Mother must be respected.",
            "keywords": ["maa", "lokpriya", "jan_sampark", "akarshak"],
        },
        2: {
            "nature": "raja",
            "effect_en": "Moon in House 2 blesses with sweet and influential speech. Family wealth accumulates through mother's side. Silver and dairy products bring luck. Fond of good food and comforts.",
            "effect_hi": "चंद्रमा दूसरे भाव में मधुर और प्रभावशाली वाणी देता है। मातृपक्ष से पारिवारिक धन बढ़ता है। चांदी और दूध के उत्पाद शुभ। अच्छे भोजन और आराम का शौक।",
            "conditions": "Keep silver with you. Respect mother for wealth to flow.",
            "keywords": ["vaani", "chandi", "doodh", "maa_paksh"],
        },
        3: {
            "nature": "mixed",
            "effect_en": "Moon in House 3 makes the native courageous but emotionally unstable with siblings. Short travels bring mood swings. Writing and communication skills are good but inconsistent.",
            "effect_hi": "चंद्रमा तीसरे भाव में जातक को साहसी लेकिन भाई-बहनों से भावनात्मक रूप से अस्थिर बनाता है। छोटी यात्राओं से मन बदलता रहता है। लेखन कला अच्छी लेकिन असंगत।",
            "conditions": "Emotional instability with siblings. Keep water at bedside.",
            "keywords": ["sahas", "bhai", "yatra", "lekhan"],
        },
        4: {
            "nature": "raja",
            "effect_en": "Moon in House 4 is exalted. Mother prospers, emotional stability, property gains. The native enjoys vehicles, land, and domestic happiness. Heart is pure and mind is peaceful.",
            "effect_hi": "चंद्रमा चौथे भाव में उच्च का है। माता की समृद्धि, भावनात्मक स्थिरता, संपत्ति लाभ। जातक वाहन, भूमि, और घरेलू सुख भोगता है। हृदय शुद्ध, मन शांत।",
            "conditions": "Mother's health and happiness directly linked to native's fortune. Keep home near water.",
            "keywords": ["uchcha", "maa", "sampatti", "grih_sukh"],
        },
        5: {
            "nature": "mixed",
            "effect_en": "Moon in House 5 gives intelligent and emotionally perceptive children. Speculative gains through intuition. Romance and love affairs are emotional. Education in arts and creative fields.",
            "effect_hi": "चंद्रमा पांचवें भाव में बुद्धिमान और भावनात्मक रूप से संवेदनशील संतान देता है। अंतर्ज्ञान से सट्टे में लाभ। प्रेम संबंध भावनात्मक। कला और रचनात्मक क्षेत्रों में शिक्षा।",
            "conditions": "Intuition strong but emotional decisions in speculation can backfire.",
            "keywords": ["santaan", "kalpana", "prem", "kala"],
        },
        6: {
            "nature": "manda",
            "effect_en": "Moon in House 6 creates mental health vulnerabilities. Enemies use emotional manipulation. Mother may face health issues. The native serves others but gets little appreciation. Digestive troubles.",
            "effect_hi": "चंद्रमा छठे भाव में मानसिक स्वास्थ्य कमज़ोरी पैदा करता है। शत्रु भावनात्मक छल करते हैं। माता के स्वास्थ्य में समस्या। जातक सेवा करता है लेकिन सराहना कम मिलती है। पाचन दोष।",
            "conditions": "Mental health needs attention. Mother's health linked. Avoid emotional enemies.",
            "keywords": ["manda", "man", "shatru", "maa_swasthya"],
        },
        7: {
            "nature": "mixed",
            "effect_en": "Moon in House 7 gives an emotional and caring spouse. Marriage brings prosperity if Moon is strong. The native is popular in partnerships and public dealings. Trade and business partnerships favoured.",
            "effect_hi": "चंद्रमा सातवें भाव में भावनात्मक और देखभाल करने वाला जीवनसाथी देता है। चंद्र बलवान हो तो विवाह से समृद्धि। साझेदारी और जन-संपर्क में लोकप्रिय। व्यापार साझेदारी शुभ।",
            "conditions": "Spouse is emotional. If Moon is weak, marriage suffers from mood swings.",
            "keywords": ["vivah", "saajhedaari", "lokpriya", "vyapar"],
        },
        8: {
            "nature": "manda",
            "effect_en": "Moon in House 8 brings sudden emotional upheavals and inheritance-related troubles. Secret fears and anxieties. Mother's health becomes a concern. Night-time disturbances and restless sleep.",
            "effect_hi": "चंद्रमा आठवें भाव में अचानक भावनात्मक उथल-पुथल और विरासत संबंधी परेशानी। गुप्त भय और चिंता। माता के स्वास्थ्य की चिंता। रात की नींद में बाधा और बेचैनी।",
            "conditions": "Sleep disturbances. Keep silver and water at bedside. Avoid darkness-related fears.",
            "keywords": ["ashtam", "neend", "bhay", "virasat"],
        },
        9: {
            "nature": "raja",
            "effect_en": "Moon in House 9 blesses with spiritual intuition and pilgrimages bring fortune. Mother is deeply religious. Travels over water bring luck. Father and mother both influence destiny positively.",
            "effect_hi": "चंद्रमा नौवें भाव में आध्यात्मिक अंतर्ज्ञान और तीर्थयात्रा से भाग्य। माता अत्यंत धार्मिक। जल यात्रा से भाग्य। पिता और माता दोनों भाग्य को सकारात्मक प्रभावित करते हैं।",
            "conditions": "Pilgrimages especially to water bodies bring great fortune.",
            "keywords": ["tirth", "jal", "maa_dharma", "bhagya"],
        },
        10: {
            "nature": "mixed",
            "effect_en": "Moon in House 10 gives career in public service, hospitality, or liquid-related businesses. Fame comes in waves — sometimes up, sometimes down. Government favours possible but unstable.",
            "effect_hi": "चंद्रमा दसवें भाव में जन सेवा, आतिथ्य, या तरल पदार्थ संबंधी व्यवसाय में कैरियर। प्रसिद्धि लहरों में — कभी ऊपर, कभी नीचे। सरकारी कृपा संभव लेकिन अस्थिर।",
            "conditions": "Career fluctuates with Moon cycles. Keep stability through discipline.",
            "keywords": ["career", "jan_seva", "sarkaar", "asthir"],
        },
        11: {
            "nature": "raja",
            "effect_en": "Moon in House 11 gives large social circle, gains through women, and fulfilment of desires. Elder siblings are supportive. Income from multiple sources. Silver brings added luck.",
            "effect_hi": "चंद्रमा ग्यारहवें भाव में बड़ा सामाजिक दायरा, स्त्रियों से लाभ, और इच्छापूर्ति। बड़े भाई-बहन सहायक। कई स्रोतों से आय। चांदी से अतिरिक्त भाग्य।",
            "conditions": "Keep silver on person. Respect elder women in family.",
            "keywords": ["labh", "stri", "ichha_purti", "chandi"],
        },
        12: {
            "nature": "manda",
            "effect_en": "Moon in House 12 brings nighttime troubles, disturbed sleep, and restlessness. Destructive tidal force within. +Ketu in House 2 = dignity lost and in-laws damaged. +Ketu in House 4 = entire male lineage becomes worthless. +Mars in House 7 = excellent married life, 'ask for water, get milk'.",
            "effect_hi": "चंद्रमा बारहवें भाव में रात को परेशानी, नींद में बाधा, बेचैनी। अंदर विनाशकारी ज्वार। +केतु दूसरे भाव में = इज़्ज़त गई, ससुराल का नुकसान। +केतु चौथे भाव में = पूरा पुरुष वंश बर्बाद। +मंगल सातवें भाव में = उत्तम वैवाहिक जीवन, 'पानी मांगो दूध मिले'।",
            "conditions": "Check Ketu in 2 or 4 (destroys). Mars in 7 reverses negativity completely. Sleep with milk/water at bedside.",
            "keywords": ["neend", "raat", "ketu_combo", "mangal_combo"],
        },
    },

    # ─────────────────────────────────────────────────────────
    # MARS (Mangal / Kuja) — Planet of Courage & Blood
    # ─────────────────────────────────────────────────────────
    "Mars": {
        1: {
            "nature": "raja",
            "effect_en": "Mars in House 1 makes the native fearless, athletic, and commanding. Natural leader with red complexion or marks on face. Quick temper but brave. Government or military success. Manglik dosha active.",
            "effect_hi": "मंगल प्रथम भाव में जातक को निडर, खिलाड़ी, और प्रभावशाली बनाता है। जन्मजात नेता, चेहरे पर लालिमा या निशान। जल्दी गुस्सा लेकिन बहादुर। सरकार या सेना में सफलता। मांगलिक दोष सक्रिय।",
            "conditions": "Manglik dosha active. Must channel anger constructively. Red coral helps.",
            "keywords": ["nidar", "neta", "manglik", "sena"],
        },
        2: {
            "nature": "mixed",
            "effect_en": "Mars in House 2 gives harsh or commanding speech. Wealth through property, land, or physical labour. Family disputes over property common. Eyes may be affected. Red lentils and copper bring fortune.",
            "effect_hi": "मंगल दूसरे भाव में कठोर या आदेशात्मक वाणी देता है। संपत्ति, भूमि, या शारीरिक श्रम से धन। परिवार में संपत्ति विवाद आम। आंखों पर प्रभाव। मसूर दाल और तांबा भाग्यशाली।",
            "conditions": "Control speech. Property disputes likely. Keep copper on person.",
            "keywords": ["vaani", "sampatti", "tamba", "masoor"],
        },
        3: {
            "nature": "raja",
            "effect_en": "Mars in House 3 makes the native brave, courageous, and good for siblings if alone. Excellent for writing, communication, and short travels. Physically strong and active. Brothers are either very helpful or very conflicting.",
            "effect_hi": "मंगल तीसरे भाव में जातक को बहादुर, साहसी बनाता है, अकेला हो तो भाई-बहनों के लिए अच्छा। लेखन, संचार और छोटी यात्राओं के लिए उत्कृष्ट। शारीरिक रूप से मज़बूत और सक्रिय।",
            "conditions": "If alone in house 3, siblings prosper. If with malefics, sibling rivalry intense.",
            "keywords": ["sahas", "bhai", "lekhan", "bal"],
        },
        4: {
            "nature": "manda",
            "effect_en": "Mars in House 4 creates domestic unrest and property disputes. Mother's health may suffer. The native is restless at home. Vehicles bring accidents if Mars is afflicted. Land-related legal issues.",
            "effect_hi": "मंगल चौथे भाव में घरेलू अशांति और संपत्ति विवाद। माता का स्वास्थ्य प्रभावित। जातक घर में बेचैन। पीड़ित मंगल से वाहन दुर्घटना। भूमि संबंधी कानूनी मसले।",
            "conditions": "Mother's health needs care. Avoid hasty property decisions. Keep sweet food at home.",
            "keywords": ["grih", "maa", "vaahan", "bhumi_vivad"],
        },
        5: {
            "nature": "mixed",
            "effect_en": "Mars in House 5 gives brave and athletic children. Risk in speculation and gambling. Love affairs are passionate but short. Education in technical/engineering fields. Children born after difficulty.",
            "effect_hi": "मंगल पांचवें भाव में बहादुर और खिलाड़ी संतान। सट्टे और जुए में जोखिम। प्रेम संबंध जोशपूर्ण लेकिन अल्पकालिक। तकनीकी/इंजीनियरिंग शिक्षा। संतान कठिनाई के बाद।",
            "conditions": "Avoid gambling. Children come after struggles. Technical education suits.",
            "keywords": ["santaan", "satta", "josh", "takneeki"],
        },
        6: {
            "nature": "raja",
            "effect_en": "Mars in House 6 destroys enemies and wins competitions. Excellent for military, police, or legal careers. Health is strong but watch for blood pressure. The native dominates opponents easily.",
            "effect_hi": "मंगल छठे भाव में शत्रुओं का विनाश और प्रतियोगिता में विजय। सेना, पुलिस, या कानूनी कैरियर के लिए उत्कृष्ट। स्वास्थ्य मज़बूत लेकिन रक्तचाप सावधानी। विरोधियों पर आसानी से वर्चस्व।",
            "conditions": "Good for competitive fields. Watch blood pressure. Donate blood periodically.",
            "keywords": ["shatru_nash", "vijay", "sena", "rakt"],
        },
        7: {
            "nature": "mixed",
            "effect_en": "Mars in House 7 makes marriage fiery — passionate but argumentative. Spouse is strong-willed. Business partnerships need careful selection. Manglik dosha strongly active. If with Moon in 12, married life is excellent — 'ask for water, get milk'.",
            "effect_hi": "मंगल सातवें भाव में विवाह उग्र — जोशपूर्ण लेकिन विवादास्पद। जीवनसाथी दृढ़ इरादे वाला। व्यापार साझेदारी सावधानी से चुनें। मांगलिक दोष अत्यंत सक्रिय। चंद्र 12वें भाव में हो तो वैवाहिक जीवन उत्तम — 'पानी मांगो दूध मिले'।",
            "conditions": "Manglik dosha active. Marry manglik spouse for harmony. Moon in 12 reverses negativity.",
            "keywords": ["manglik", "vivah", "josh", "chandra_combo"],
        },
        8: {
            "nature": "manda",
            "effect_en": "Mars in House 8 brings blood disease risk. Never exploit a widow — kismat permanently destroyed. Never good relationship with younger brothers (separate by age 8). +Mercury/Ketu in House 2 = paralysis risk. Surgeries and accidents possible.",
            "effect_hi": "मंगल आठवें भाव में रक्त रोग का खतरा। कभी विधवा का शोषण न करें — किस्मत हमेशा के लिए नष्ट। छोटे भाइयों से कभी अच्छा संबंध नहीं (8 वर्ष की उम्र से अलग)। +बुध/केतु दूसरे भाव में = लकवे का खतरा।",
            "conditions": "CRITICAL: Never exploit widows. Separate from younger brothers by age 8. Check Mercury/Ketu in House 2 for paralysis risk.",
            "keywords": ["rakt_rog", "vidhwa", "bhai", "lakva"],
        },
        9: {
            "nature": "mixed",
            "effect_en": "Mars in House 9 gives courage in religious pursuits. Father may be strict or military-background. Pilgrimages to Mars temples bring fortune. Property through father. Can be aggressive in dharmic matters.",
            "effect_hi": "मंगल नौवें भाव में धार्मिक कार्यों में साहस। पिता कठोर या सैनिक पृष्ठभूमि के हो सकते हैं। मंगल मंदिरों की तीर्थयात्रा से भाग्य। पिता से संपत्ति। धार्मिक मामलों में आक्रामक हो सकता है।",
            "conditions": "Father is strict but supportive. Visit Hanuman temples regularly.",
            "keywords": ["pita", "dharma", "hanuman", "bhumi"],
        },
        10: {
            "nature": "raja",
            "effect_en": "Mars in House 10 gives powerful career in engineering, military, police, surgery, or real estate. Commands authority at workplace. Rapid career rise but through conflict and competition. Property from career earnings.",
            "effect_hi": "मंगल दसवें भाव में इंजीनियरिंग, सेना, पुलिस, सर्जरी, या रियल एस्टेट में शक्तिशाली कैरियर। कार्यस्थल पर अधिकार। तीव्र कैरियर उन्नति लेकिन संघर्ष और प्रतिस्पर्धा से। कैरियर की कमाई से संपत्ति।",
            "conditions": "Career through authority and competition. Avoid office politics through honesty.",
            "keywords": ["career", "adhikaar", "sena", "sampatti"],
        },
        11: {
            "nature": "raja",
            "effect_en": "Mars in House 11 fulfils desires through courage and effort. Gains from brothers, property deals, and technical work. Social circle includes military and police connections. Elder brother is supportive.",
            "effect_hi": "मंगल ग्यारहवें भाव में साहस और प्रयास से इच्छापूर्ति। भाइयों, संपत्ति सौदों, और तकनीकी कार्य से लाभ। सामाजिक दायरे में सैनिक और पुलिस कनेक्शन। बड़ा भाई सहायक।",
            "conditions": "Gains through property and brothers. Keep relationships with elder siblings strong.",
            "keywords": ["labh", "bhai", "sampatti", "sahas"],
        },
        12: {
            "nature": "raja",
            "effect_en": "Mars in House 12 is STRONGEST position. Traditionally considered 51% strong. Long life, miraculous survivals, unsolicited helpers arrive. 'Diya meetha logon, kami zar na dolat' (give sweets, no shortage of wealth). Condition: House 3 must be empty or have 2+ planets. Best remedy: Tuesday Hanuman halwa with milk.",
            "effect_hi": "मंगल बारहवें भाव में सबसे मज़बूत स्थिति। परंपरागत रूप से 51% बलवान। लंबी उम्र, चमत्कारी बचाव, बिन बुलाए सहायक आते हैं। 'दिया मीठा लोगों, कमी ज़र ना दौलत'। शर्त: तीसरा भाव खाली या 2+ ग्रह। उत्तम उपाय: मंगलवार हनुमान हलवा दूध से।",
            "conditions": "STRONGEST Mars. House 3 must be empty or have 2+ planets. Give sweets = wealth never lacks. Tuesday Hanuman halwa with milk is best remedy.",
            "keywords": ["sabse_mazboot", "lambi_umar", "hanuman", "meetha"],
        },
    },

    # ─────────────────────────────────────────────────────────
    # SATURN (Shani) — Planet of Karma & Justice
    # ─────────────────────────────────────────────────────────
    "Saturn": {
        1: {
            "nature": "mixed",
            "effect_en": "Saturn in House 1 makes the native hardworking, disciplined, and serious from a young age. Life starts with struggles but improves with age. Dark complexion or thin build. Success comes after 36.",
            "effect_hi": "शनि प्रथम भाव में जातक को बचपन से मेहनती, अनुशासित, और गंभीर बनाता है। जीवन संघर्ष से शुरू लेकिन उम्र के साथ सुधरता है। सांवला रंग या पतला शरीर। 36 के बाद सफलता।",
            "conditions": "Early life struggles. Success after 36. Avoid alcohol. Serve the elderly.",
            "keywords": ["mehnat", "anushasan", "sangharsh", "der_se_safalta"],
        },
        2: {
            "nature": "mixed",
            "effect_en": "Saturn in House 2 restricts speech and family wealth initially. Delayed accumulation but eventually stable. Family responsibilities are heavy. The native speaks less but effectively. Teeth and eye problems possible.",
            "effect_hi": "शनि दूसरे भाव में वाणी और पारिवारिक धन को शुरू में बाधित करता है। विलंबित लेकिन अंततः स्थिर संचय। पारिवारिक ज़िम्मेदारियां भारी। कम बोलता है लेकिन प्रभावशाली। दांत और आंख समस्या।",
            "conditions": "Family wealth delayed. Teeth/eye care needed. Speak truth always.",
            "keywords": ["vaani", "vilamb", "dhan", "daant"],
        },
        3: {
            "nature": "raja",
            "effect_en": "Saturn in House 3 makes the native extremely brave, long-lived, and successful in technical or mechanical work. Younger siblings may cause worry. Writing and communication bring lasting results.",
            "effect_hi": "शनि तीसरे भाव में जातक को अत्यंत बहादुर, दीर्घायु, और तकनीकी/यांत्रिक कार्य में सफल बनाता है। छोटे भाई-बहन चिंता का कारण। लेखन और संचार से स्थायी परिणाम।",
            "conditions": "Long life and bravery. Technical skills are the path. Care for younger siblings.",
            "keywords": ["sahas", "dirghaayu", "takneeki", "bhai"],
        },
        4: {
            "nature": "manda",
            "effect_en": "Saturn in House 4 delays property acquisition and creates distance from mother. Domestic life is challenging until middle age. Old homes or ancestral properties cause problems. Heart remains heavy.",
            "effect_hi": "शनि चौथे भाव में संपत्ति अधिग्रहण में देरी और माता से दूरी। मध्य आयु तक घरेलू जीवन चुनौतीपूर्ण। पुराने घर या पैतृक संपत्ति समस्या। हृदय भारी रहता है।",
            "conditions": "Mother's distance or health issues. Property delayed but comes. Serve mother.",
            "keywords": ["maa", "sampatti", "vilamb", "grih_kashta"],
        },
        5: {
            "nature": "manda",
            "effect_en": "Saturn in House 5 delays children or creates distance from them. Education is slow but thorough. No luck in speculation. Romance comes late in life. Children born after age 30 bring fortune.",
            "effect_hi": "शनि पांचवें भाव में संतान में देरी या उनसे दूरी। शिक्षा धीमी लेकिन गहन। सट्टे में भाग्य नहीं। प्रेम देर से आता है। 30 की उम्र के बाद जन्मी संतान भाग्यशाली।",
            "conditions": "Children delayed. No speculation. Late love. Education through discipline.",
            "keywords": ["santaan_vilamb", "shiksha", "prem_der", "anushasan"],
        },
        6: {
            "nature": "raja",
            "effect_en": "Saturn in House 6 destroys enemies through patience and persistence. Excellent for service and government work. Health is strong despite initial appearance. Wins long legal battles. Debts get cleared over time.",
            "effect_hi": "शनि छठे भाव में धैर्य और दृढ़ता से शत्रु नाश। सेवा और सरकारी काम के लिए उत्कृष्ट। शुरुआती दिखावट के बावजूद स्वास्थ्य मज़बूत। लंबी कानूनी लड़ाई जीतता है। कर्ज़ समय से साफ़।",
            "conditions": "Patience is the weapon. Government service suits. Legal battles won.",
            "keywords": ["shatru_nash", "dhairya", "sarkaar", "karz_mukti"],
        },
        7: {
            "nature": "mixed",
            "effect_en": "Saturn in House 7 delays marriage or brings an older/mature spouse. Business partnerships are slow but stable. The native is loyal in marriage. Second half of life is better than first.",
            "effect_hi": "शनि सातवें भाव में विवाह में देरी या बड़ी उम्र/परिपक्व जीवनसाथी। व्यापार साझेदारी धीमी लेकिन स्थिर। जातक विवाह में वफ़ादार। जीवन का दूसरा भाग पहले से बेहतर।",
            "conditions": "Late marriage is better. Choose mature partner. Business partnerships need patience.",
            "keywords": ["vivah_vilamb", "paripakv", "wafadaar", "dhairya"],
        },
        8: {
            "nature": "raja",
            "effect_en": "Saturn in House 8 is in its own house. Very strong but tests heavily through suffering. Long life through endurance. Inheritance comes with conditions. Occult knowledge and deep research ability.",
            "effect_hi": "शनि आठवें भाव में अपने ही घर में है। बहुत मज़बूत लेकिन कष्ट से कठोर परीक्षा। सहनशक्ति से लंबी उम्र। विरासत शर्तों के साथ। तांत्रिक ज्ञान और गहन शोध क्षमता।",
            "conditions": "Own house — very strong. Long life but through suffering. Occult knowledge comes naturally.",
            "keywords": ["apna_ghar", "lambi_umar", "kashta", "tantrik"],
        },
        9: {
            "nature": "mixed",
            "effect_en": "Saturn in House 9 makes father strict or causes father-related difficulties. Fortune comes through hard work, not luck. Religious discipline suits — structured spiritual practice. Pilgrimages bring karmic relief.",
            "effect_hi": "शनि नौवें भाव में पिता कठोर या पिता संबंधी कठिनाई। भाग्य मेहनत से, किस्मत से नहीं। धार्मिक अनुशासन अनुकूल — संरचित साधना। तीर्थयात्रा से कार्मिक राहत।",
            "conditions": "Father relationship strained. Fortune through effort only. Structured worship.",
            "keywords": ["pita", "mehnat", "anushasan", "tirth"],
        },
        10: {
            "nature": "manda",
            "effect_en": "Saturn in House 10 is debilitated. Career struggles, delayed success, and authority issues. Boss or government creates obstacles. BUT persistent effort eventually brings recognition. Avoid shortcuts.",
            "effect_hi": "शनि दसवें भाव में नीच है। कैरियर संघर्ष, विलंबित सफलता, और अधिकार समस्याएं। बॉस या सरकार बाधा डालती है। लेकिन निरंतर प्रयास अंततः मान्यता दिलाता है। शॉर्टकट से बचें।",
            "conditions": "Debilitated — career struggles. Avoid shortcuts. Hard work ALWAYS pays eventually.",
            "keywords": ["neech", "career", "sangharsh", "vilamb"],
        },
        11: {
            "nature": "raja",
            "effect_en": "Saturn in House 11 gives slow but massive gains. Elder siblings are karmic connections. Income through service, labour, or government increases with age. Social circle includes mature, wise people.",
            "effect_hi": "शनि ग्यारहवें भाव में धीमा लेकिन विशाल लाभ। बड़े भाई-बहन कार्मिक संबंध। सेवा, श्रम, या सरकार से आय उम्र के साथ बढ़ती है। सामाजिक दायरे में परिपक्व, बुद्धिमान लोग।",
            "conditions": "Gains increase with age. Government connections fruitful. Serve elderly.",
            "keywords": ["labh", "dhima", "sarkaar", "bade_log"],
        },
        12: {
            "nature": "mixed",
            "effect_en": "Saturn in House 12 brings expenditure on hospitals, prisons, or spiritual retreats. Foreign residence possible but with karmic purpose. Sleep disorders and leg/feet problems. Salvation through service.",
            "effect_hi": "शनि बारहवें भाव में अस्पताल, जेल, या आध्यात्मिक आश्रम पर खर्च। विदेश निवास संभव लेकिन कार्मिक उद्देश्य से। नींद विकार और पैर की समस्या। सेवा से मुक्ति।",
            "conditions": "Foreign land possible. Hospital expenses. Serve poor for spiritual relief. Feet health.",
            "keywords": ["vyay", "videsh", "hospital", "mukti"],
        },

        # Nishaniyan of afflicted Saturn (cross-reference)
        "_nishaniyan": {
            "signs_en": "Roof collapse, vehicle problems after purchase, eyesight weakening, paternal uncle illness.",
            "signs_hi": "छत गिरना, खरीदने के बाद वाहन समस्या, दृष्टि कमज़ोर होना, चाचा की बीमारी।",
        },
    },

    # ─────────────────────────────────────────────────────────
    # SUN (Surya) — Planet of Authority & Father
    # ─────────────────────────────────────────────────────────
    "Sun": {
        1: {
            "nature": "raja",
            "effect_en": "Sun in House 1 gives commanding personality, government favour, and father's blessings. The native is authoritative, health-conscious, and respected. Leadership roles come naturally. Wheat and copper bring luck.",
            "effect_hi": "सूर्य प्रथम भाव में प्रभावशाली व्यक्तित्व, सरकारी कृपा, और पिता का आशीर्वाद। जातक अधिकारपूर्ण, स्वास्थ्य-सचेत, और सम्मानित। नेतृत्व स्वाभाविक। गेहूं और तांबा शुभ।",
            "conditions": "Government connections strong. Father supportive. Offer water to Sun at sunrise.",
            "keywords": ["adhikaar", "sarkaar", "pita", "neta"],
        },
        2: {
            "nature": "raja",
            "effect_en": "Sun in House 2 gives authoritative speech and family wealth through government or father. Eyes are sharp but may weaken with age. Gold brings fortune. Family commands respect in society.",
            "effect_hi": "सूर्य दूसरे भाव में अधिकारपूर्ण वाणी और सरकार या पिता से पारिवारिक धन। आंखें तेज़ लेकिन उम्र से कमज़ोर। सोना भाग्यशाली। परिवार समाज में सम्मान पाता है।",
            "conditions": "Eyes need care. Gold ornaments bring luck. Father helps with wealth.",
            "keywords": ["vaani", "sona", "ankh", "pita_dhan"],
        },
        3: {
            "nature": "raja",
            "effect_en": "Sun in House 3 gives courage, good siblings, and success in communication. Government letters and official documents bring good news. Younger brothers benefit from the native. Short travels are productive.",
            "effect_hi": "सूर्य तीसरे भाव में साहस, अच्छे भाई-बहन, और संचार में सफलता। सरकारी पत्र और आधिकारिक दस्तावेज़ शुभ समाचार लाते हैं। छोटे भाई जातक से लाभान्वित। छोटी यात्राएं उत्पादक।",
            "conditions": "Brothers prosper. Official work succeeds. Write and communicate boldly.",
            "keywords": ["sahas", "bhai", "sarkaar", "sanchar"],
        },
        4: {
            "nature": "mixed",
            "effect_en": "Sun in House 4 can create tension with mother and domestic issues. The native desires property and vehicles but faces delays. Father and mother's relationship affects destiny. Heart health needs attention.",
            "effect_hi": "सूर्य चौथे भाव में माता से तनाव और घरेलू समस्याएं। संपत्ति और वाहन की इच्छा लेकिन देरी। पिता-माता का संबंध भाग्य को प्रभावित। हृदय स्वास्थ्य ध्यान मांगता है।",
            "conditions": "Mother-father tension affects home. Heart care needed. Build own house for peace.",
            "keywords": ["maa", "grih", "hriday", "sampatti"],
        },
        5: {
            "nature": "raja",
            "effect_en": "Sun in House 5 blesses with intelligent children and success in education. Government jobs for children. Speculative gains through father's guidance. Romance brings status. Creative fields are lucky.",
            "effect_hi": "सूर्य पांचवें भाव में बुद्धिमान संतान और शिक्षा में सफलता। बच्चों को सरकारी नौकरी। पिता के मार्गदर्शन से सट्टे में लाभ। प्रेम से प्रतिष्ठा। रचनात्मक क्षेत्र भाग्यशाली।",
            "conditions": "Children are government-connected. Father's guidance essential. Creative work suits.",
            "keywords": ["santaan", "vidya", "sarkaar", "rachna"],
        },
        6: {
            "nature": "raja",
            "effect_en": "Sun in House 6 defeats enemies through authority. Government work and legal battles are won. Health is robust except for heat-related issues. The native serves with dignity and commands even in service.",
            "effect_hi": "सूर्य छठे भाव में अधिकार से शत्रुओं की पराजय। सरकारी काम और कानूनी लड़ाई जीत। गर्मी संबंधी समस्या छोड़ स्वास्थ्य मज़बूत। सेवा में भी गरिमा और आदेश।",
            "conditions": "Enemies defeated. Government legal matters won. Avoid excessive heat.",
            "keywords": ["shatru_vijay", "sarkaar", "garmi", "adhikaar"],
        },
        7: {
            "nature": "mixed",
            "effect_en": "Sun in House 7 gives a proud or government-connected spouse. Marriage brings social status. Business partnerships with government officials prosper. The native may be dominating in relationships.",
            "effect_hi": "सूर्य सातवें भाव में गर्वीला या सरकार से जुड़ा जीवनसाथी। विवाह से सामाजिक प्रतिष्ठा। सरकारी अधिकारियों के साथ व्यापार साझेदारी फलती है। जातक संबंधों में प्रभावशाली।",
            "conditions": "Spouse has authority. Don't be dominating. Partnership with government works.",
            "keywords": ["vivah", "pratishttha", "sarkaar", "sajhedaari"],
        },
        8: {
            "nature": "manda",
            "effect_en": "Sun in House 8 weakens father's influence and creates inheritance disputes. Government opposes the native. Eye and bone problems. Secret enemies from authority positions. Father's health is a concern.",
            "effect_hi": "सूर्य आठवें भाव में पिता का प्रभाव कमज़ोर और विरासत विवाद। सरकार विरोध करती है। आंख और हड्डी समस्या। अधिकार पदों से गुप्त शत्रु। पिता के स्वास्थ्य की चिंता।",
            "conditions": "Father's health concern. Government opposition. Keep copper. Avoid inheritance disputes.",
            "keywords": ["pita_kashta", "virasat", "sarkaar_virodh", "gupt_shatru"],
        },
        9: {
            "nature": "raja",
            "effect_en": "Sun in House 9 is one of the best placements. Father is highly respected and brings fortune. Religious authority and pilgrimage bring wealth. Government recognition for dharmic work. Foreign travel is productive.",
            "effect_hi": "सूर्य नौवें भाव में श्रेष्ठतम स्थितियों में से एक। पिता अत्यंत सम्मानित और भाग्यशाली। धार्मिक अधिकार और तीर्थयात्रा से धन। धर्म कार्य में सरकारी मान्यता। विदेश यात्रा उत्पादक।",
            "conditions": "Father is key to fortune. Pilgrimages essential. Government honours possible.",
            "keywords": ["pita_bhagya", "tirth", "sarkaar_maan", "dharma"],
        },
        10: {
            "nature": "raja",
            "effect_en": "Sun in House 10 gives powerful government career, authority, and social status. The native is a natural administrator. Father supports career. Name and fame through profession. Kings and rulers have this placement.",
            "effect_hi": "सूर्य दसवें भाव में शक्तिशाली सरकारी कैरियर, अधिकार, और सामाजिक प्रतिष्ठा। जातक जन्मजात प्रशासक। पिता कैरियर में सहायक। पेशे से नाम और प्रसिद्धि। राजाओं की यही स्थिति।",
            "conditions": "Career in government/administration. Father's blessings essential. Offer water to Sun.",
            "keywords": ["sarkaar", "adhikaar", "prashasan", "naam"],
        },
        11: {
            "nature": "raja",
            "effect_en": "Sun in House 11 gives gains through government, father, and authority. Elder siblings are influential. Income increases steadily. Social circle includes powerful and respected people. Desires are fulfilled.",
            "effect_hi": "सूर्य ग्यारहवें भाव में सरकार, पिता, और अधिकार से लाभ। बड़े भाई-बहन प्रभावशाली। आय निरंतर बढ़ती है। सामाजिक दायरे में शक्तिशाली और सम्मानित लोग। इच्छाएं पूर्ण।",
            "conditions": "Father and government bring gains. Elder siblings supportive. Keep gold.",
            "keywords": ["labh", "sarkaar", "pita", "ichha_purti"],
        },
        12: {
            "nature": "manda",
            "effect_en": "Sun in House 12 weakens authority and father's support. Government opposes or ignores. Expenditure on father's health. Eye problems and sleep disturbances. Foreign land may help but father suffers.",
            "effect_hi": "सूर्य बारहवें भाव में अधिकार और पिता का सहारा कमज़ोर। सरकार विरोध या उपेक्षा करती है। पिता के स्वास्थ्य पर खर्च। आंख और नींद की समस्या। विदेश सहायक लेकिन पिता को कष्ट।",
            "conditions": "Father suffers. Government opposes. Eye care essential. Offer wheat on Sundays.",
            "keywords": ["pita_kashta", "vyay", "ankh", "videsh"],
        },
    },

    # ─────────────────────────────────────────────────────────
    # MERCURY (Budh) — Planet of Intelligence & Trade
    # ─────────────────────────────────────────────────────────
    "Mercury": {
        1: {
            "nature": "raja",
            "effect_en": "Mercury in House 1 gives sharp intellect, youthful appearance, and excellent communication skills. Business acumen from birth. Good for trade, media, and education. Sisters and daughters bring luck.",
            "effect_hi": "बुध प्रथम भाव में तीक्ष्ण बुद्धि, युवा रूप, और उत्कृष्ट संचार कौशल। जन्म से व्यापार कुशलता। व्यापार, मीडिया, और शिक्षा के लिए अच्छा। बहनें और बेटियां भाग्यशाली।",
            "conditions": "Sisters/daughters bring luck. Business from young age. Green colour auspicious.",
            "keywords": ["buddhi", "vyapar", "sanchar", "behen"],
        },
        2: {
            "nature": "raja",
            "effect_en": "Mercury in House 2 gives sweet, persuasive speech and wealth through trade or writing. Family is educated and articulate. Banking and accounting skills. Green vegetables and moong dal bring fortune.",
            "effect_hi": "बुध दूसरे भाव में मधुर, प्रभावशाली वाणी और व्यापार या लेखन से धन। परिवार शिक्षित और वाक्पटु। बैंकिंग और लेखा कौशल। हरी सब्ज़ियां और मूंग दाल भाग्यशाली।",
            "conditions": "Speech is the weapon. Banking/accounting suits. Donate green things on Wednesdays.",
            "keywords": ["vaani", "vyapar", "lekhan", "banking"],
        },
        3: {
            "nature": "raja",
            "effect_en": "Mercury in House 3 is in its own house. Excellent for communication, writing, teaching, and media. Siblings are intellectual. Short travels bring profit. Publishing and journalism succeed. Kanya Pujan stabilizes this Mercury.",
            "effect_hi": "बुध तीसरे भाव में अपने घर में है। संचार, लेखन, शिक्षण, और मीडिया के लिए उत्कृष्ट। भाई-बहन बौद्धिक। छोटी यात्राओं से लाभ। प्रकाशन और पत्रकारिता सफल। कन्या पूजन बुध को स्थिर करता है।",
            "conditions": "Own house — very strong. Kanya Pujan stabilizes further. Writing and media are destiny.",
            "keywords": ["apna_ghar", "lekhan", "sanchar", "kanya_pujan"],
        },
        4: {
            "nature": "mixed",
            "effect_en": "Mercury in House 4 gives education-focused home and intelligent mother. Property through intellectual work. Home office or study room brings fortune. Green plants in home are essential for mental peace.",
            "effect_hi": "बुध चौथे भाव में शिक्षा-केंद्रित घर और बुद्धिमान माता। बौद्धिक कार्य से संपत्ति। गृह कार्यालय या अध्ययन कक्ष भाग्यशाली। घर में हरे पौधे मानसिक शांति के लिए आवश्यक।",
            "conditions": "Keep green plants at home. Mother is intellectual. Home office brings fortune.",
            "keywords": ["shiksha", "maa_buddhi", "grih", "hara"],
        },
        5: {
            "nature": "raja",
            "effect_en": "Mercury in House 5 gives highly intelligent children and success in education. Creative writing, astrology, and speculative gains through analysis. Daughters are especially bright. Teaching brings fulfilment.",
            "effect_hi": "बुध पांचवें भाव में अत्यंत बुद्धिमान संतान और शिक्षा में सफलता। रचनात्मक लेखन, ज्योतिष, और विश्लेषण से सट्टे में लाभ। बेटियां विशेष रूप से प्रतिभाशाली। शिक्षण से संतुष्टि।",
            "conditions": "Children are brilliant. Astrology as interest. Daughters bring luck.",
            "keywords": ["santaan_buddhi", "vidya", "jyotish", "beti"],
        },
        6: {
            "nature": "mixed",
            "effect_en": "Mercury in House 6 defeats enemies through intelligence and legal wit. Good for accounting, auditing, and detective work. Nerves and skin may be affected. Sisters may face challenges.",
            "effect_hi": "बुध छठे भाव में बुद्धि और कानूनी चतुराई से शत्रुओं की पराजय। लेखा, ऑडिट, और जासूसी कार्य के लिए अच्छा। नसें और त्वचा प्रभावित। बहनों को चुनौतियां।",
            "conditions": "Intelligence defeats enemies. Skin/nerve care needed. Support sisters.",
            "keywords": ["shatru", "buddhi", "lekha", "nas"],
        },
        7: {
            "nature": "mixed",
            "effect_en": "Mercury in House 7 gives an intelligent, youthful spouse. Business partnerships based on intellect prosper. The native is skilled in negotiations. Trade and commerce thrive through marriage connections.",
            "effect_hi": "बुध सातवें भाव में बुद्धिमान, युवा जीवनसाथी। बुद्धि पर आधारित व्यापार साझेदारी सफल। जातक वार्ता में कुशल। विवाह के संपर्कों से व्यापार फलता है।",
            "conditions": "Spouse is intellectual. Business through marriage connections. Negotiations are strength.",
            "keywords": ["vivah", "buddhi", "vyapar", "vaarta"],
        },
        8: {
            "nature": "manda",
            "effect_en": "Mercury in House 8 creates nervousness, anxiety, and hidden fears. Inheritance disputes involve legal complications. Skin diseases and nervous disorders. Research into occult brings knowledge but fear.",
            "effect_hi": "बुध आठवें भाव में घबराहट, चिंता, और छिपे भय। विरासत विवाद में कानूनी जटिलताएं। त्वचा रोग और तंत्रिका विकार। तांत्रिक शोध से ज्ञान लेकिन भय।",
            "conditions": "Nervous health needs care. Legal complications in inheritance. Avoid occult extremes.",
            "keywords": ["chinta", "nas", "virasat", "bhay"],
        },
        9: {
            "nature": "raja",
            "effect_en": "Mercury in House 9 blesses with analytical mind for religion and philosophy. Father is educated. Foreign education brings fortune. Publishing religious or educational texts succeeds. Pilgrimage with learning purpose.",
            "effect_hi": "बुध नौवें भाव में धर्म और दर्शन के लिए विश्लेषणात्मक बुद्धि। पिता शिक्षित। विदेशी शिक्षा भाग्यशाली। धार्मिक या शैक्षिक ग्रंथों का प्रकाशन सफल। शिक्षा उद्देश्य से तीर्थयात्रा।",
            "conditions": "Father is scholarly. Foreign education brings fortune. Publish and teach.",
            "keywords": ["pita_vidya", "dharma", "videsh_shiksha", "prakashan"],
        },
        10: {
            "nature": "raja",
            "effect_en": "Mercury in House 10 gives career in trade, communication, accounting, or media. Dual career possible. Quick promotions through intelligence. Green colour in workplace brings luck.",
            "effect_hi": "बुध दसवें भाव में व्यापार, संचार, लेखा, या मीडिया में कैरियर। दोहरा कैरियर संभव। बुद्धि से तीव्र पदोन्नति। कार्यस्थल में हरा रंग भाग्यशाली।",
            "conditions": "Dual income sources. Intelligence drives career. Keep green at workplace.",
            "keywords": ["career", "vyapar", "sanchar", "buddhi"],
        },
        11: {
            "nature": "raja",
            "effect_en": "Mercury in House 11 gives gains through intelligence, trade, and sisters. Social circle is educated and influential. Multiple income streams from intellectual work. Elder sisters bring fortune.",
            "effect_hi": "बुध ग्यारहवें भाव में बुद्धि, व्यापार, और बहनों से लाभ। सामाजिक दायरा शिक्षित और प्रभावशाली। बौद्धिक कार्य से कई आय स्रोत। बड़ी बहनें भाग्यशाली।",
            "conditions": "Sisters bring gains. Multiple income streams. Educated social circle.",
            "keywords": ["labh", "behen", "vyapar", "buddhi"],
        },
        12: {
            "nature": "manda",
            "effect_en": "Mercury in House 12 brings expenditure through wrong decisions and poor communication. Foreign land may help but mental peace is lost. Sisters face difficulties. Nervousness and insomnia.",
            "effect_hi": "बुध बारहवें भाव में गलत फ़ैसलों और खराब संचार से खर्च। विदेश सहायक लेकिन मानसिक शांति खोती है। बहनों को कठिनाई। घबराहट और अनिद्रा।",
            "conditions": "Wrong decisions cause losses. Sisters suffer. Mental peace lost. Green things help.",
            "keywords": ["vyay", "galat_nirnay", "behen_kashta", "anidra"],
        },
    },

    # ─────────────────────────────────────────────────────────
    # VENUS (Shukra) — Planet of Luxury & Marriage
    # ─────────────────────────────────────────────────────────
    "Venus": {
        1: {
            "nature": "raja",
            "effect_en": "Venus in House 1 gives attractive personality, love for luxury, and artistic talent. Marriage is early and happy. Women are helpful throughout life. White clothes and silver bring luck. Generous nature.",
            "effect_hi": "शुक्र प्रथम भाव में आकर्षक व्यक्तित्व, विलासिता का शौक, और कलात्मक प्रतिभा। विवाह जल्दी और सुखी। जीवन भर स्त्रियां सहायक। सफ़ेद कपड़े और चांदी शुभ। उदार स्वभाव।",
            "conditions": "Women help throughout life. White colour auspicious. Art and beauty are destiny.",
            "keywords": ["akarshak", "kala", "vivah", "stri_sahay"],
        },
        2: {
            "nature": "raja",
            "effect_en": "Venus in House 2 gives melodious voice, family wealth, and love for fine food. Wife brings fortune. Beauty and aesthetics in home. Banking and luxury goods trade prosper. Diamonds bring extra luck.",
            "effect_hi": "शुक्र दूसरे भाव में मधुर स्वर, पारिवारिक धन, और स्वादिष्ट भोजन का शौक। पत्नी भाग्य लाती है। घर में सुंदरता और सौंदर्य। बैंकिंग और विलासिता व्यापार फलता है। हीरा अतिरिक्त भाग्य।",
            "conditions": "Wife brings fortune. Home must be beautiful. Diamond suits this placement.",
            "keywords": ["vaani", "patni_bhagya", "saundarya", "heera"],
        },
        3: {
            "nature": "mixed",
            "effect_en": "Venus in House 3 gives artistic communication skills. Sisters are beautiful and helpful. Short travels for pleasure and art. Writing about beauty, fashion, and relationships succeeds. Creative media work.",
            "effect_hi": "शुक्र तीसरे भाव में कलात्मक संचार कौशल। बहनें सुंदर और सहायक। आनंद और कला के लिए छोटी यात्राएं। सौंदर्य, फैशन, और संबंधों पर लेखन सफल। रचनात्मक मीडिया कार्य।",
            "conditions": "Sisters are key. Creative communication. Art-related travels bring joy.",
            "keywords": ["kala", "behen", "lekhan", "fashion"],
        },
        4: {
            "nature": "raja",
            "effect_en": "Venus in House 4 blesses with beautiful home, luxury vehicles, and domestic happiness. Mother is beautiful and cultured. Property brings fortune. White marble and flowers in home are auspicious.",
            "effect_hi": "शुक्र चौथे भाव में सुंदर घर, विलासिता वाहन, और घरेलू सुख। माता सुंदर और सुसंस्कृत। संपत्ति भाग्यशाली। घर में सफ़ेद संगमरमर और फूल शुभ।",
            "conditions": "Home must be beautiful. Mother is cultured. White flowers at home.",
            "keywords": ["grih_sukh", "vaahan", "maa_sundar", "sampatti"],
        },
        5: {
            "nature": "raja",
            "effect_en": "Venus in House 5 gives love marriage and beautiful, talented children. Creative arts, music, and cinema bring success. Speculative gains through artistic ventures. Romance is central to life.",
            "effect_hi": "शुक्र पांचवें भाव में प्रेम विवाह और सुंदर, प्रतिभाशाली संतान। रचनात्मक कला, संगीत, और सिनेमा से सफलता। कलात्मक उद्यमों से सट्टे में लाभ। प्रेम जीवन का केंद्र।",
            "conditions": "Love marriage likely. Children are talented. Arts and music are destiny.",
            "keywords": ["prem_vivah", "santaan", "sangeet", "kala"],
        },
        6: {
            "nature": "manda",
            "effect_en": "Venus in House 6 creates health issues for wife or through women. Luxury spending becomes debt. Beauty fades through stress. Kidney and urinary tract issues. Service to women brings relief.",
            "effect_hi": "शुक्र छठे भाव में पत्नी या स्त्रियों से स्वास्थ्य समस्या। विलासिता खर्च कर्ज़ बन जाता है। तनाव से सौंदर्य घटता है। गुर्दा और मूत्र पथ समस्या। स्त्रियों की सेवा से राहत।",
            "conditions": "Wife's health concern. Control luxury spending. Kidney care needed.",
            "keywords": ["patni_rog", "karz", "gurda", "vilasita"],
        },
        7: {
            "nature": "raja",
            "effect_en": "Venus in House 7 gives beautiful, loving spouse and excellent married life. Business partnerships with women thrive. The native is charming in public. Luxury goods trade succeeds. Marriage is the turning point.",
            "effect_hi": "शुक्र सातवें भाव में सुंदर, प्रेमपूर्ण जीवनसाथी और उत्कृष्ट वैवाहिक जीवन। स्त्रियों के साथ व्यापार साझेदारी फलती है। जातक सार्वजनिक रूप से आकर्षक। विलासिता व्यापार सफल। विवाह जीवन का मोड़।",
            "conditions": "Marriage is destiny. Spouse brings fortune. Luxury trade thrives.",
            "keywords": ["vivah", "sundar_patni", "vyapar", "vilasita"],
        },
        8: {
            "nature": "mixed",
            "effect_en": "Venus in House 8 gives deep, transformative love and inherited wealth through spouse. Secret relationships possible. Sexual energy strong. Wife's family brings fortune or trouble. Beauty-related health issues.",
            "effect_hi": "शुक्र आठवें भाव में गहरा, परिवर्तनकारी प्रेम और जीवनसाथी से विरासती धन। गुप्त संबंध संभव। यौन ऊर्जा प्रबल। पत्नी का परिवार भाग्य या कष्ट लाता है। सौंदर्य संबंधी स्वास्थ्य।",
            "conditions": "Spouse family brings fortune or trouble. Avoid secret relationships. Deep love.",
            "keywords": ["gupt_prem", "virasat", "youn", "patni_parivar"],
        },
        9: {
            "nature": "raja",
            "effect_en": "Venus in House 9 blesses with fortune through wife, art, and beauty. Religious art and temple decoration bring merit. Wife is deeply spiritual. Foreign travel for pleasure brings fortune. Father supports marriage.",
            "effect_hi": "शुक्र नौवें भाव में पत्नी, कला, और सौंदर्य से भाग्य। धार्मिक कला और मंदिर सजावट से पुण्य। पत्नी अत्यंत आध्यात्मिक। आनंद हेतु विदेश यात्रा भाग्यशाली। पिता विवाह का समर्थन।",
            "conditions": "Wife brings spiritual fortune. Temple decoration brings merit. Foreign travel lucky.",
            "keywords": ["patni_bhagya", "kala", "dharma", "videsh"],
        },
        10: {
            "nature": "raja",
            "effect_en": "Venus in House 10 gives career in arts, fashion, entertainment, hospitality, or luxury goods. Fame through beauty and charm. Women in workplace are helpful. Career brings luxurious lifestyle.",
            "effect_hi": "शुक्र दसवें भाव में कला, फैशन, मनोरंजन, आतिथ्य, या विलासिता सामान में कैरियर। सौंदर्य और आकर्षण से प्रसिद्धि। कार्यस्थल में स्त्रियां सहायक। कैरियर से विलासिता भरा जीवन।",
            "conditions": "Beauty-related career. Women help at work. Fame through charm.",
            "keywords": ["career", "kala", "fashion", "stri_sahay"],
        },
        11: {
            "nature": "raja",
            "effect_en": "Venus in House 11 gives gains through women, art, and luxury goods. Social circle is glamorous. Elder sisters bring fortune. Multiple income streams from beauty and entertainment. Desires are fulfilled lavishly.",
            "effect_hi": "शुक्र ग्यारहवें भाव में स्त्रियों, कला, और विलासिता सामान से लाभ। सामाजिक दायरा आकर्षक। बड़ी बहनें भाग्यशाली। सौंदर्य और मनोरंजन से कई आय स्रोत। इच्छाएं भव्य रूप से पूर्ण।",
            "conditions": "Women bring gains. Glamorous social circle. Elder sisters are lucky.",
            "keywords": ["labh", "stri", "kala", "vilasita"],
        },
        12: {
            "nature": "mixed",
            "effect_en": "Venus in House 12 gives expenditure on luxury, women, and pleasure. Bed pleasures are strong. Foreign residence is luxurious. Wife may have health issues. Secret relationships drain wealth. Spiritual love transcends.",
            "effect_hi": "शुक्र बारहवें भाव में विलासिता, स्त्रियों, और आनंद पर खर्च। शय्या सुख प्रबल। विदेश निवास विलासिता। पत्नी को स्वास्थ्य समस्या। गुप्त संबंध धन क्षय। आध्यात्मिक प्रेम ऊपर।",
            "conditions": "Luxury expenditure high. Foreign luxury. Wife health concern. Avoid secret affairs.",
            "keywords": ["vyay", "vilasita", "videsh", "gupt_sambandh"],
        },
    },

    # ─────────────────────────────────────────────────────────
    # RAHU — Shadow Planet of Illusion & Foreign
    # ─────────────────────────────────────────────────────────
    "Rahu": {
        1: {
            "nature": "mixed",
            "effect_en": "Rahu in House 1 gives unusual personality and unconventional thinking. Foreign connections are strong. The native is ambitious beyond measure. Deception from others is common. Keep silver and fennel for protection.",
            "effect_hi": "राहु प्रथम भाव में असामान्य व्यक्तित्व और अपरंपरागत सोच। विदेशी संबंध मज़बूत। जातक असीमित महत्वाकांक्षी। दूसरों से धोखा आम। सुरक्षा के लिए चांदी और सौंफ रखें।",
            "conditions": "Keep silver and fennel (saunf). Foreign connections help. Guard against deception.",
            "keywords": ["videshi", "mahatvakaanksha", "dhokha", "chandi"],
        },
        2: {
            "nature": "manda",
            "effect_en": "Rahu in House 2 creates confusion in family and speech becomes misleading. Wealth comes from unusual or foreign sources but leaves suddenly. Family secrets and hidden wealth. In-laws create troubles.",
            "effect_hi": "राहु दूसरे भाव में परिवार में भ्रम और वाणी भ्रामक। असामान्य या विदेशी स्रोतों से धन लेकिन अचानक चला जाता है। पारिवारिक रहस्य और छिपा धन। ससुराल समस्या।",
            "conditions": "Family confusion. Wealth unstable. Keep coal/iron piece in home safe.",
            "keywords": ["vaani_bhram", "videshi_dhan", "parivar_rahasya", "sasural"],
        },
        3: {
            "nature": "raja",
            "effect_en": "Rahu in House 3 gives extraordinary courage and success in technology, media, and foreign communication. Siblings may have unusual lives. Travel abroad for work succeeds. Occult writing gains fame.",
            "effect_hi": "राहु तीसरे भाव में असाधारण साहस और तकनीक, मीडिया, विदेशी संचार में सफलता। भाई-बहनों का जीवन असामान्य। विदेश में काम के लिए यात्रा सफल। तांत्रिक लेखन से प्रसिद्धि।",
            "conditions": "Technology and foreign media suit. Brothers have unusual lives. Courage is extreme.",
            "keywords": ["sahas", "takneek", "videsh", "media"],
        },
        4: {
            "nature": "manda",
            "effect_en": "Rahu in House 4 creates instability at home and mental confusion. Mother may have unusual personality. Property through unconventional means. Electricity-related problems in home. Keep home clean and uncluttered.",
            "effect_hi": "राहु चौथे भाव में घर में अस्थिरता और मानसिक भ्रम। माता का व्यक्तित्व असामान्य। अपरंपरागत साधनों से संपत्ति। घर में बिजली संबंधी समस्या। घर साफ़ और व्यवस्थित रखें।",
            "conditions": "Home instability. Mother unusual. Keep home clean. Electrical issues common.",
            "keywords": ["grih_asthir", "maa", "bhram", "bijli"],
        },
        5: {
            "nature": "mixed",
            "effect_en": "Rahu in House 5 gives clever but manipulative intelligence. Children may be unconventional or born through difficulty. Speculative gains through foreign investments. Love affairs have deception element.",
            "effect_hi": "राहु पांचवें भाव में चतुर लेकिन छलपूर्ण बुद्धि। संतान अपरंपरागत या कठिनाई से जन्म। विदेशी निवेश से सट्टे में लाभ। प्रेम संबंधों में धोखे का तत्व।",
            "conditions": "Children unconventional. Foreign investments suit. Avoid deception in love.",
            "keywords": ["santaan", "satta", "videshi", "chhal"],
        },
        6: {
            "nature": "raja",
            "effect_en": "Rahu in House 6 crushes enemies through unconventional means. Excellent for technology-based service and foreign employment. Health is unusual — ailments are hard to diagnose. Legal tricks work in favour.",
            "effect_hi": "राहु छठे भाव में अपरंपरागत साधनों से शत्रु नाश। तकनीक आधारित सेवा और विदेशी रोज़गार के लिए उत्कृष्ट। स्वास्थ्य असामान्य — रोग का निदान कठिन। कानूनी चालें अनुकूल।",
            "conditions": "Enemies defeated through tricks. Foreign job suits. Mysterious health issues.",
            "keywords": ["shatru_nash", "takneek", "videsh_naukri", "rahasya_rog"],
        },
        7: {
            "nature": "mixed",
            "effect_en": "Rahu in House 7 gives foreign or unconventional spouse. Marriage may be inter-caste or inter-religion. Business partnerships with foreigners succeed. The native is charming but deceptive in relationships.",
            "effect_hi": "राहु सातवें भाव में विदेशी या अपरंपरागत जीवनसाथी। अंतर्जातीय या अंतर्धार्मिक विवाह। विदेशियों के साथ व्यापार साझेदारी सफल। जातक आकर्षक लेकिन संबंधों में छलपूर्ण।",
            "conditions": "Unusual marriage. Foreign spouse possible. Guard against deception in partnerships.",
            "keywords": ["vivah_videshi", "antar_jaati", "vyapar", "chhal"],
        },
        8: {
            "nature": "manda",
            "effect_en": "Rahu in House 8 brings sudden and mysterious transformations. Inheritance from foreign or unusual sources. Hidden enemies from unexpected places. Occult powers develop naturally. Poisoning or intoxication risk.",
            "effect_hi": "राहु आठवें भाव में अचानक और रहस्यमय परिवर्तन। विदेशी या असामान्य स्रोतों से विरासत। अप्रत्याशित स्थानों से गुप्त शत्रु। तांत्रिक शक्ति स्वाभाविक। विषाक्तता या नशे का खतरा।",
            "conditions": "Sudden transformations. Occult powers. Avoid intoxicants. Keep coconut for protection.",
            "keywords": ["achinak", "rahasya", "tantrik", "vish"],
        },
        9: {
            "nature": "mixed",
            "effect_en": "Rahu in House 9 gives fortune through foreign lands and unconventional religion. Father may be from different culture or have unusual beliefs. Pilgrimages to foreign lands bring fortune. Technology-based dharma work.",
            "effect_hi": "राहु नौवें भाव में विदेशी भूमि और अपरंपरागत धर्म से भाग्य। पिता भिन्न संस्कृति या असामान्य विश्वास वाले। विदेश तीर्थयात्रा भाग्यशाली। तकनीक आधारित धर्म कार्य।",
            "conditions": "Foreign lands bring fortune. Father unusual. Technology in dharma suits.",
            "keywords": ["videsh_bhagya", "pita", "takneek", "dharma"],
        },
        10: {
            "nature": "raja",
            "effect_en": "Rahu in House 10 gives powerful career in politics, technology, or foreign companies. The native rises rapidly but through unconventional means. Fame is sudden. Government connections through diplomacy.",
            "effect_hi": "राहु दसवें भाव में राजनीति, तकनीक, या विदेशी कंपनियों में शक्तिशाली कैरियर। अपरंपरागत साधनों से तीव्र उन्नति। प्रसिद्धि अचानक। कूटनीति से सरकारी संबंध।",
            "conditions": "Rapid career rise. Foreign companies suit. Politics possible. Fame sudden.",
            "keywords": ["career", "rajneeti", "takneek", "achinak_prasiddhi"],
        },
        11: {
            "nature": "raja",
            "effect_en": "Rahu in House 11 gives massive gains through foreign connections, technology, and unconventional means. Social circle is international. Elder siblings live abroad. Desires fulfilled through unexpected channels.",
            "effect_hi": "राहु ग्यारहवें भाव में विदेशी संबंधों, तकनीक, और अपरंपरागत साधनों से विशाल लाभ। सामाजिक दायरा अंतर्राष्ट्रीय। बड़े भाई-बहन विदेश में। अप्रत्याशित मार्गों से इच्छापूर्ति।",
            "conditions": "Foreign connections bring wealth. Technology is the vehicle. International network.",
            "keywords": ["labh", "videsh", "takneek", "antarrashtriya"],
        },
        12: {
            "nature": "mixed",
            "effect_en": "Rahu in House 12 gives foreign settlement and expenditure in distant lands. Spiritual confusion — attracted to multiple paths. Dreams are vivid and prophetic. Hidden enemies from foreign places. Sleep disturbances.",
            "effect_hi": "राहु बारहवें भाव में विदेश बसावट और दूर देशों में खर्च। आध्यात्मिक भ्रम — कई मार्गों से आकर्षण। स्वप्न स्पष्ट और भविष्यवाणी वाले। विदेशी स्थानों से गुप्त शत्रु। नींद बाधित।",
            "conditions": "Foreign settlement. Vivid dreams. Spiritual confusion. Keep fennel under pillow.",
            "keywords": ["videsh", "sapna", "bhram", "gupt_shatru"],
        },
    },

    # ─────────────────────────────────────────────────────────
    # KETU — Shadow Planet of Spirituality & Detachment
    # ─────────────────────────────────────────────────────────
    "Ketu": {
        1: {
            "nature": "mixed",
            "effect_en": "Ketu in House 1 gives a mysterious, spiritual personality. The native appears detached and otherworldly. Health is unpredictable with mysterious ailments. Spiritual growth from young age. Saffron and dogs bring luck.",
            "effect_hi": "केतु प्रथम भाव में रहस्यमय, आध्यात्मिक व्यक्तित्व। जातक विरक्त और अलौकिक दिखता है। स्वास्थ्य अप्रत्याशित, रहस्यमय बीमारियां। बचपन से आध्यात्मिक विकास। केसर और कुत्ते शुभ।",
            "conditions": "Feed stray dogs. Keep saffron. Spiritual path from birth. Mysterious health.",
            "keywords": ["adhyaatmik", "virakti", "rahasya_rog", "kesar"],
        },
        2: {
            "nature": "manda",
            "effect_en": "Ketu in House 2 disrupts family harmony and speech. Wealth is unstable — comes and goes mysteriously. Family has spiritual or unusual tendencies. Vision problems possible. Avoid harsh speech.",
            "effect_hi": "केतु दूसरे भाव में पारिवारिक सामंजस्य और वाणी बाधित। धन अस्थिर — रहस्यमय ढंग से आता-जाता है। परिवार में आध्यात्मिक या असामान्य प्रवृत्तियां। दृष्टि समस्या। कठोर वाणी से बचें।",
            "conditions": "Family instability. Wealth mysterious. Vision care. Feed dogs. Donate blankets.",
            "keywords": ["parivar", "dhan_asthir", "drishti", "vaani"],
        },
        3: {
            "nature": "raja",
            "effect_en": "Ketu in House 3 gives extraordinary spiritual courage and mystical communication abilities. Brothers have spiritual inclinations. Occult writing and psychic research succeed. Travels to spiritual places.",
            "effect_hi": "केतु तीसरे भाव में असाधारण आध्यात्मिक साहस और रहस्यमय संचार क्षमता। भाइयों में आध्यात्मिक रुझान। तांत्रिक लेखन और मानसिक शोध सफल। आध्यात्मिक स्थलों की यात्रा।",
            "conditions": "Spiritual courage. Occult research. Brothers are spiritual. Travel to holy places.",
            "keywords": ["sahas", "tantrik", "bhai", "adhyaatmik_yatra"],
        },
        4: {
            "nature": "manda",
            "effect_en": "Ketu in House 4 detaches from home and mother. Property issues from unknown causes. Domestic peace disturbed by spiritual or supernatural events. Mother may be ill or distant. Secret room or space at home helps.",
            "effect_hi": "केतु चौथे भाव में घर और माता से विरक्ति। अज्ञात कारणों से संपत्ति समस्या। आध्यात्मिक या अलौकिक घटनाओं से घरेलू शांति बाधित। माता बीमार या दूर। घर में गुप्त कमरा या स्थान सहायक।",
            "conditions": "Mother's distance. Home unrest. Keep saffron at worship place. Dogs in home help.",
            "keywords": ["maa_virakti", "grih", "alaukik", "kesar"],
        },
        5: {
            "nature": "mixed",
            "effect_en": "Ketu in House 5 gives spiritually inclined children or delays/difficulties with children. Education in occult or spiritual sciences. Speculative losses. Past-life connections surface in love. Intuition is extremely strong.",
            "effect_hi": "केतु पांचवें भाव में आध्यात्मिक रुझान वाली संतान या संतान में देरी/कठिनाई। तांत्रिक या आध्यात्मिक विज्ञान में शिक्षा। सट्टे में हानि। प्रेम में पूर्व-जन्म संबंध। अंतर्ज्ञान अत्यंत प्रबल।",
            "conditions": "Children delayed or spiritual. No speculation. Past-life love connections. Trust intuition.",
            "keywords": ["santaan", "adhyaatmik", "satta_hani", "poorv_janm"],
        },
        6: {
            "nature": "mixed",
            "effect_en": "Ketu in House 6 can defeat enemies through spiritual means or create mysterious health problems. Dogs as pets bring protection. Hidden enemies are from spiritual circles. Service to animals brings relief.",
            "effect_hi": "केतु छठे भाव में आध्यात्मिक साधनों से शत्रु नाश या रहस्यमय स्वास्थ्य समस्या। पालतू कुत्ते सुरक्षा लाते हैं। आध्यात्मिक मंडलियों से गुप्त शत्रु। जानवरों की सेवा से राहत।",
            "conditions": "Feed and care for dogs. Mysterious diseases. Spiritual enemies. Animal service.",
            "keywords": ["shatru", "kutta", "rahasya_rog", "pashu_seva"],
        },
        7: {
            "nature": "manda",
            "effect_en": "Ketu in House 7 creates detachment in marriage and partnerships. Spouse may be spiritual or otherworldly. Marriage faces mysterious challenges. Business partnerships dissolve unexpectedly. Past-life spouse connection.",
            "effect_hi": "केतु सातवें भाव में विवाह और साझेदारी में विरक्ति। जीवनसाथी आध्यात्मिक या अलौकिक। विवाह रहस्यमय चुनौतियां। व्यापार साझेदारी अप्रत्याशित रूप से टूटती है। पूर्व-जन्म का साथी।",
            "conditions": "Marriage detachment. Spiritual spouse. Past-life connection. Feed dogs together.",
            "keywords": ["vivah_virakti", "adhyaatmik_patni", "poorv_janm", "sajhedaari"],
        },
        8: {
            "nature": "raja",
            "effect_en": "Ketu in House 8 gives deep occult knowledge and moksha potential. Sudden spiritual awakenings. Inheritance from unexpected sources. Death is peaceful and spiritually significant. Research into mysteries succeeds.",
            "effect_hi": "केतु आठवें भाव में गहरा तांत्रिक ज्ञान और मोक्ष की संभावना। अचानक आध्यात्मिक जागृति। अप्रत्याशित स्रोतों से विरासत। मृत्यु शांत और आध्यात्मिक रूप से महत्वपूर्ण। रहस्यों की खोज सफल।",
            "conditions": "Moksha potential. Occult mastery. Peaceful death. Research mysteries.",
            "keywords": ["moksha", "tantrik", "jagruti", "rahasya"],
        },
        9: {
            "nature": "raja",
            "effect_en": "Ketu in House 9 gives deep spiritual wisdom and past-life religious merit. The native is a natural mystic. Father may be spiritually evolved or detached. Pilgrimages to ancient sites bring liberation. Teaching spirituality succeeds.",
            "effect_hi": "केतु नौवें भाव में गहरा आध्यात्मिक ज्ञान और पूर्व-जन्म का धार्मिक पुण्य। जातक जन्मजात रहस्यवादी। पिता आध्यात्मिक रूप से विकसित या विरक्त। प्राचीन स्थलों की तीर्थयात्रा से मुक्ति। अध्यात्म शिक्षण सफल।",
            "conditions": "Natural mystic. Father spiritual. Ancient pilgrimages. Teaching dharma.",
            "keywords": ["adhyaatmik_gyan", "pita", "tirth", "moksha"],
        },
        10: {
            "nature": "mixed",
            "effect_en": "Ketu in House 10 creates unusual career path — either spiritual vocation or frequent career changes. The native achieves fame through unconventional work. Technology and spirituality combine in career. Detachment from worldly ambition.",
            "effect_hi": "केतु दसवें भाव में असामान्य कैरियर मार्ग — आध्यात्मिक व्यवसाय या बार-बार कैरियर बदलाव। अपरंपरागत कार्य से प्रसिद्धि। तकनीक और अध्यात्म का कैरियर में मेल। सांसारिक महत्वाकांक्षा से विरक्ति।",
            "conditions": "Unusual career. Frequent changes. Spirituality in work. Detachment from ambition.",
            "keywords": ["career_asaman", "adhyaatmik", "badlaav", "virakti"],
        },
        11: {
            "nature": "mixed",
            "effect_en": "Ketu in House 11 gives gains through spiritual or mystical work. Social circle includes healers and mystics. Elder siblings have spiritual tendencies. Desires are fulfilled unexpectedly. Non-material wishes come true.",
            "effect_hi": "केतु ग्यारहवें भाव में आध्यात्मिक या रहस्यमय कार्य से लाभ। सामाजिक दायरे में उपचारक और रहस्यवादी। बड़े भाई-बहन में आध्यात्मिक प्रवृत्ति। इच्छाएं अप्रत्याशित रूप से पूर्ण। अभौतिक इच्छाएं सच।",
            "conditions": "Spiritual gains. Mystic social circle. Non-material wishes fulfilled.",
            "keywords": ["labh", "adhyaatmik", "rahasya", "ichha_purti"],
        },
        12: {
            "nature": "raja",
            "effect_en": "Ketu in House 12 is one of the best placements for moksha. Deep meditation comes naturally. Foreign ashrams or spiritual retreats call. Expenditure on spiritual pursuits is actually investment. Dreams are prophetic.",
            "effect_hi": "केतु बारहवें भाव में मोक्ष के लिए श्रेष्ठतम स्थितियों में से एक। गहरा ध्यान स्वाभाविक। विदेशी आश्रम या आध्यात्मिक रिट्रीट बुलाते हैं। आध्यात्मिक कार्यों पर खर्च वास्तव में निवेश। स्वप्न भविष्यवाणी वाले।",
            "conditions": "Moksha placement. Meditation is natural. Foreign ashrams call. Prophetic dreams.",
            "keywords": ["moksha", "dhyan", "videsh_ashram", "sapna"],
        },
    },
}


# ============================================================
# VALIDATED REMEDIES SYSTEM
# ============================================================

LK_VALIDATED_REMEDIES: Dict[str, Dict[str, Any]] = {
    "mitti_ka_kuja": {
        "name_en": "Earthen Pot (Mitti ka Kuja)",
        "name_hi": "मिट्टी का कूजा",
        "for_planet": "Saturn",
        "condition": None,
        "procedure_en": (
            "Fill an earthen pot with mustard oil. Seal it airtight with cement/araldite "
            "so no air remains. Bury it in the ground near a river or pond on Amavasya "
            "(new moon night). Continue for 40-43 days."
        ),
        "procedure_hi": (
            "मिट्टी के कूजे में सरसों का तेल भरें। सीमेंट/अरालडाइट से वायुरोधी सील करें। "
            "अमावस्या की रात नदी या तालाब के पास ज़मीन में गाड़ दें। 40-43 दिन तक करें।"
        ),
        "validated": True,
    },
    "kanya_pujan": {
        "name_en": "Kanya Pujan (Worship of Young Girls)",
        "name_hi": "कन्या पूजन",
        "for_planet": "Mercury",
        "condition": None,
        "procedure_en": (
            "Serve 9 girls (under age of puberty). Offer red saree, freshly cooked halwa "
            "with black chana on Ashtami or Navami. This stabilizes Mercury in House 3 "
            "and indirectly benefits Jupiter and Saturn."
        ),
        "procedure_hi": (
            "9 कन्याओं (अविवाहित) की सेवा करें। लाल साड़ी, ताज़ा बना हलवा और काले चने "
            "अष्टमी या नवमी पर अर्पित करें। यह बुध को तीसरे भाव में स्थिर करता है।"
        ),
        "validated": True,
    },
    "tuesday_hanuman_halwa": {
        "name_en": "Tuesday Hanuman Halwa",
        "name_hi": "मंगलवार हनुमान हलवा",
        "for_planet": "Mars",
        "condition": None,
        "procedure_en": (
            "Every Tuesday, visit Hanuman temple. Offer halwa made from suji (semolina) "
            "with milk. Also offer Boondi Ladoo. This remedy also controls Rahu regardless "
            "of its position. Keep rice or silver on person."
        ),
        "procedure_hi": (
            "हर मंगलवार हनुमान मंदिर जाएं। सूजी का हलवा दूध से बनाकर अर्पित करें। बूंदी "
            "लड्डू भी चढ़ाएं। यह उपाय राहु को भी नियंत्रित करता है। चावल या चांदी साथ रखें।"
        ),
        "validated": True,
    },
    "mars_12_meetha": {
        "name_en": "Mars 12th House Sweets Remedy",
        "name_hi": "मंगल बारहवें भाव मीठा उपाय",
        "for_planet": "Mars",
        "condition": "Mars in House 12",
        "procedure_en": (
            "Eat sweets yourself and offer sweets to others. This increases wealth. "
            "Specifically, milk-based halwa eaten and distributed brings prosperity."
        ),
        "procedure_hi": (
            "स्वयं मिठाई खाएं और दूसरों को खिलाएं। इससे धन में वृद्धि होती है। विशेष रूप "
            "से दूध से बना हलवा खाने और बांटने से समृद्धि आती है।"
        ),
        "validated": True,
    },
    "chandra_universal_booster": {
        "name_en": "Moon as Universal Remedy Booster",
        "name_hi": "चंद्र सार्वभौमिक उपाय सहायक",
        "for_planet": "Any",
        "condition": None,
        "procedure_en": (
            "For any planet's affliction, add Moon items to the remedy: milk, white sweets "
            "(barfi), silver, white flowers, rice, white cloth. Donate silver in flowing "
            "water. Keep water/milk pot at headboard while sleeping, pour on Peepal tree "
            "in morning."
        ),
        "procedure_hi": (
            "किसी भी ग्रह की पीड़ा के लिए चंद्र की वस्तुएं उपाय में जोड़ें: दूध, सफेद मिठाई "
            "(बर्फी), चांदी, सफेद फूल, चावल, सफेद कपड़ा। बहते पानी में चांदी प्रवाहित करें।"
        ),
        "validated": "partial",
    },
    "jupiter_education_remedy": {
        "name_en": "Jupiter Education Activation",
        "name_hi": "बृहस्पति शिक्षा सक्रियण",
        "for_planet": "Jupiter",
        "condition": "Jupiter in House 1",
        "procedure_en": (
            "Pursue and complete higher education (graduation or above). Jupiter in House 1 "
            "activates fortune only after formal education. Donate turmeric and chana dal "
            "at temple on Thursdays."
        ),
        "procedure_hi": (
            "उच्च शिक्षा (स्नातक या उससे ऊपर) पूरी करें। बृहस्पति प्रथम भाव में औपचारिक "
            "शिक्षा के बाद ही किस्मत सक्रिय करता है। गुरुवार को मंदिर में हल्दी और चना दाल दान करें।"
        ),
        "validated": True,
    },
    "jupiter_11_kafan_daan": {
        "name_en": "Jupiter 11th House Kafan Donation",
        "name_hi": "बृहस्पति ग्यारहवें भाव कफ़न दान",
        "for_planet": "Jupiter",
        "condition": "Jupiter in House 11",
        "procedure_en": (
            "When family bonds feel strained, donate a white cloth (kafan) to a needy "
            "person or at a cremation ground. This preserves the family unity that Jupiter "
            "in House 11 absolutely requires."
        ),
        "procedure_hi": (
            "जब पारिवारिक संबंध तनावपूर्ण लगें, ज़रूरतमंद या शमशान में सफ़ेद कपड़ा (कफ़न) दान "
            "करें। यह पारिवारिक एकता को बनाए रखता है जो ग्यारहवें भाव के बृहस्पति के लिए अनिवार्य है।"
        ),
        "validated": True,
    },
    "saturn_mustard_oil_iron": {
        "name_en": "Saturn Mustard Oil & Iron Remedy",
        "name_hi": "शनि सरसों तेल और लोहा उपाय",
        "for_planet": "Saturn",
        "condition": None,
        "procedure_en": (
            "On Saturday, pour mustard oil on a piece of iron. See your reflection in the "
            "oil, then donate both the oil and iron to a needy person. Feed crows with "
            "cooked rice mixed with sesame oil."
        ),
        "procedure_hi": (
            "शनिवार को लोहे के टुकड़े पर सरसों का तेल डालें। तेल में अपना प्रतिबिंब देखें, फिर "
            "तेल और लोहा दोनों ज़रूरतमंद को दान करें। कौवों को तिल के तेल में मिला चावल खिलाएं।"
        ),
        "validated": True,
    },
    "rahu_coconut_remedy": {
        "name_en": "Rahu Coconut Flowing Water Remedy",
        "name_hi": "राहु नारियल बहते पानी उपाय",
        "for_planet": "Rahu",
        "condition": None,
        "procedure_en": (
            "Float a whole coconut in flowing water (river or stream) on Saturday. "
            "Keep a solid silver square piece in your pocket and fennel (saunf) "
            "under your pillow while sleeping."
        ),
        "procedure_hi": (
            "शनिवार को बहते पानी (नदी या नाले) में पूरा नारियल प्रवाहित करें। "
            "जेब में चांदी का ठोस चौकोर टुकड़ा रखें और सोते समय सौंफ तकिए के "
            "नीचे रखें।"
        ),
        "validated": True,
    },
    "ketu_dog_feeding": {
        "name_en": "Ketu Dog Feeding Remedy",
        "name_hi": "केतु कुत्ता भोजन उपाय",
        "for_planet": "Ketu",
        "condition": None,
        "procedure_en": (
            "Feed stray dogs regularly, especially with sweet roti or biscuits. Keep "
            "saffron at your place of worship. Donate a black and white blanket to a "
            "temple. Apply saffron tilak daily."
        ),
        "procedure_hi": (
            "नियमित रूप से आवारा कुत्तों को खिलाएं, विशेषकर मीठी रोटी या बिस्कुट। पूजा स्थान "
            "पर केसर रखें। मंदिर में काला-सफ़ेद कंबल दान करें। रोज़ केसर तिलक लगाएं।"
        ),
        "validated": True,
    },
    "sun_water_offering": {
        "name_en": "Sun Sunrise Water Offering",
        "name_hi": "सूर्य को सूर्योदय जल अर्पण",
        "for_planet": "Sun",
        "condition": None,
        "procedure_en": (
            "Every morning at sunrise, face east and offer water to the Sun from a copper "
            "vessel. Add red flowers or jaggery to the water. Chant Surya mantra 11 times. "
            "Wear a copper ring or keep a copper square piece."
        ),
        "procedure_hi": (
            "हर सुबह सूर्योदय पर पूर्व दिशा की ओर मुंह करके तांबे के बर्तन से सूर्य को जल अर्पित "
            "करें। जल में लाल फूल या गुड़ डालें। सूर्य मंत्र 11 बार जाप करें। तांबे की अंगूठी या "
            "चौकोर तांबा रखें।"
        ),
        "validated": True,
    },
    "venus_white_donation": {
        "name_en": "Venus White Cloth & Ghee Donation",
        "name_hi": "शुक्र सफ़ेद कपड़ा और घी दान",
        "for_planet": "Venus",
        "condition": None,
        "procedure_en": (
            "On Friday, donate white clothes, white rice, and ghee at a Devi temple. "
            "Offer white flowers. Use perfume or fragrance regularly. Keep a silver "
            "square piece at home."
        ),
        "procedure_hi": (
            "शुक्रवार को देवी मंदिर में सफ़ेद कपड़े, सफ़ेद चावल, और घी दान करें। सफ़ेद फूल अर्पित "
            "करें। नियमित रूप से इत्र या सुगंध प्रयोग करें। घर में चांदी का चौकोर टुकड़ा रखें।"
        ),
        "validated": True,
    },
    "moon_silver_peepal": {
        "name_en": "Moon Silver & Peepal Tree Remedy",
        "name_hi": "चंद्र चांदी और पीपल वृक्ष उपाय",
        "for_planet": "Moon",
        "condition": None,
        "procedure_en": (
            "Keep fresh water by bedside at night, pour it on a Peepal tree root in "
            "the morning. Wear a pearl in silver on the little finger on Monday. "
            "Drink water from a silver glass. Donate white rice and milk on Mondays."
        ),
        "procedure_hi": (
            "रात को सिरहाने पर ताज़ा पानी रखें, सुबह पीपल के पेड़ की जड़ में डालें। सोमवार को "
            "चांदी में मोती छोटी उंगली में पहनें। चांदी के गिलास से पानी पिएं। सोमवार को सफ़ेद "
            "चावल और दूध दान करें।"
        ),
        "validated": True,
    },
}


# ============================================================
# PUBLIC API FUNCTIONS
# ============================================================

def get_lk_house_interpretation(planet: str, house: int) -> Dict[str, Any]:
    """
    Return the full interpretation for a planet in a specific house.

    Args:
        planet: Planet name (e.g. "Jupiter", "Moon", "Mars")
        house: LK house number (1-12)

    Returns:
        Dict with nature, effect_en, effect_hi, conditions, keywords.
        Empty dict if planet/house not found.
    """
    planet_data = LK_PLANET_HOUSE_INTERPRETATIONS.get(planet, {})
    interpretation = planet_data.get(house, {})
    if interpretation:
        return {
            "planet": planet,
            "house": house,
            "nature": interpretation.get("nature", "mixed"),
            "effect_en": interpretation.get("effect_en", ""),
            "effect_hi": interpretation.get("effect_hi", ""),
            "conditions": interpretation.get("conditions", ""),
            "keywords": interpretation.get("keywords", []),
        }
    return {}


def get_all_interpretations_for_chart(
    planet_positions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Return all house interpretations for a given chart's planet positions.

    Args:
        planet_positions: list of {"planet": "Jupiter", "house": 4} dicts

    Returns:
        List of interpretation dicts for each planet in its house.
    """
    from app.lalkitab_source_tags import source_of
    src = source_of("get_all_interpretations_for_chart")  # LK_CANONICAL
    results = []
    for pos in planet_positions:
        planet = pos.get("planet", "")
        house = pos.get("house", 0)
        interp = get_lk_house_interpretation(planet, house)
        if interp:
            interp.setdefault("source", src)
            results.append(interp)
    return results


def get_lk_validated_remedies(
    planet_positions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Return all applicable validated remedies based on planet positions.

    Args:
        planet_positions: list of {"planet": "Jupiter", "house": 4} dicts

    Returns:
        List of applicable remedy dicts with name, procedure, validation status.
    """
    # Build a quick lookup: planet -> house
    planet_house_map: Dict[str, int] = {}
    planet_set: set = set()
    for pos in planet_positions:
        p = pos.get("planet", "")
        h = pos.get("house", 0)
        planet_house_map[p] = h
        planet_set.add(p)

    applicable: List[Dict[str, Any]] = []

    for remedy_key, remedy in LK_VALIDATED_REMEDIES.items():
        target_planet = remedy["for_planet"]
        condition = remedy.get("condition")

        # Check if remedy applies
        should_include = False

        if target_planet == "Any":
            # Universal remedies always included
            should_include = True
        elif target_planet in planet_set:
            if condition is None:
                # General remedy for this planet — always include
                should_include = True
            else:
                # Condition-specific remedy (e.g. "Mars in House 12")
                # Parse condition: "<Planet> in House <N>"
                parts = condition.split()
                if len(parts) >= 4 and parts[1] == "in" and parts[2] == "House":
                    try:
                        cond_house = int(parts[3])
                        cond_planet = parts[0]
                        if planet_house_map.get(cond_planet) == cond_house:
                            should_include = True
                    except (ValueError, IndexError):
                        pass

        if should_include:
            applicable.append({
                "key": remedy_key,
                "name_en": remedy["name_en"],
                "name_hi": remedy["name_hi"],
                "for_planet": target_planet,
                "condition": condition,
                "procedure_en": remedy["procedure_en"],
                "procedure_hi": remedy["procedure_hi"],
                "validated": remedy["validated"],
            })

    return applicable
