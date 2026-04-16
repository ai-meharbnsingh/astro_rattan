"""Transit interpretation fragments — 7 planets x 12 houses x 5 areas, bilingual.

This is the core interpretation matrix for the Vedic astrology horoscope app.
Each planet-house-area combination provides culturally authentic bilingual text
following classical Jyotish principles.
"""
from typing import Dict

# TRANSIT_FRAGMENTS[planet][house_number][area] = {"en": "...", "hi": "..."}
TRANSIT_FRAGMENTS: Dict[str, Dict[int, Dict[str, Dict[str, str]]]] = {
    # =========================================================================
    # SUN (Surya) — Authority, ego, father, government, vitality, soul
    # Natural malefic. Karaka of soul, power, government.
    # =========================================================================
    "Sun": {
        1: {
            "general": {
                "en": "Sun transiting your 1st house illuminates your personality and boosts confidence. This is an excellent period for personal initiatives and self-expression. Leadership qualities come to the fore naturally.",
                "hi": "सूर्य का आपके प्रथम भाव में गोचर आपके व्यक्तित्व को प्रकाशित करता है और आत्मविश्वास बढ़ाता है। यह व्यक्तिगत पहल और आत्म-अभिव्यक्ति के लिए उत्कृष्ट समय है। नेतृत्व के गुण स्वाभाविक रूप से सामने आते हैं।"
            },
            "love": {
                "en": "Your magnetic personality draws admirers during this transit. You radiate warmth and confidence in romantic matters. However, guard against excessive self-focus that may overshadow your partner's needs.",
                "hi": "इस गोचर के दौरान आपका आकर्षक व्यक्तित्व प्रशंसकों को खींचता है। प्रेम मामलों में आप उष्णता और आत्मविश्वास बिखेरते हैं। हालांकि, अत्यधिक आत्मकेंद्रितता से बचें जो साथी की भावनाओं को दबा सकती है।"
            },
            "career": {
                "en": "Professional visibility increases significantly with Sun in your ascendant. Authority figures notice your work and leadership potential. Take charge of projects and demonstrate your capabilities boldly.",
                "hi": "लग्न में सूर्य के आने से व्यावसायिक दृश्यता काफी बढ़ जाती है। अधिकारी आपके कार्य और नेतृत्व क्षमता को पहचानते हैं। परियोजनाओं की कमान संभालें और अपनी योग्यता का साहसपूर्वक प्रदर्शन करें।"
            },
            "finance": {
                "en": "Financial independence is highlighted as the Sun energizes your self-worth. Income through personal effort and government-related channels may increase. Avoid impulsive spending driven by ego or status.",
                "hi": "सूर्य आपकी आत्म-मूल्य की भावना को ऊर्जा देता है, जिससे आर्थिक स्वतंत्रता पर प्रकाश पड़ता है। व्यक्तिगत प्रयास और सरकारी माध्यमों से आय बढ़ सकती है। अहंकार या प्रतिष्ठा से प्रेरित आवेगी खर्च से बचें।"
            },
            "health": {
                "en": "Vitality and physical energy reach a peak during this transit. Your constitution strengthens and immunity improves. Be mindful of heat-related issues, headaches, and eye strain.",
                "hi": "इस गोचर के दौरान जीवन शक्ति और शारीरिक ऊर्जा चरम पर पहुंचती है। आपकी शारीरिक संरचना मजबूत होती है और रोग प्रतिरोधक क्षमता बढ़ती है। गर्मी संबंधित समस्याओं, सिरदर्द और आंखों के तनाव से सावधान रहें।"
            },
        },
        2: {
            "general": {
                "en": "Sun in your 2nd house focuses attention on wealth, family matters, and speech. You may take a more authoritative role within your family. Financial dealings with government or authority figures are highlighted.",
                "hi": "दूसरे भाव में सूर्य धन, पारिवारिक मामलों और वाणी पर ध्यान केंद्रित करता है। परिवार में आप अधिक अधिकारपूर्ण भूमिका निभा सकते हैं। सरकार या अधिकारियों से वित्तीय लेन-देन प्रमुख रहता है।"
            },
            "love": {
                "en": "Family dynamics influence your romantic life during this period. Your speech carries authority which can either attract or intimidate partners. Warmth in expressing feelings to loved ones strengthens bonds.",
                "hi": "इस अवधि में पारिवारिक गतिशीलता आपके प्रेम जीवन को प्रभावित करती है। आपकी वाणी में अधिकार होता है जो साथी को आकर्षित या भयभीत कर सकता है। प्रियजनों के प्रति भावनाओं में उष्णता रिश्तों को मजबूत करती है।"
            },
            "career": {
                "en": "Your professional speech and presentation skills are enhanced. Careers involving banking, finance, or government treasury benefit greatly. Focus on building valuable assets through your work.",
                "hi": "आपकी व्यावसायिक वाणी और प्रस्तुति कौशल में वृद्धि होती है। बैंकिंग, वित्त या सरकारी कोषागार से जुड़े करियर को विशेष लाभ मिलता है। अपने कार्य के माध्यम से मूल्यवान संपत्ति बनाने पर ध्यान दें।"
            },
            "finance": {
                "en": "Accumulated wealth comes under scrutiny and reorganization. Income from family business or inherited sources may increase. Be cautious about overcommitting resources to maintain status.",
                "hi": "संचित धन की जांच और पुनर्गठन होता है। पारिवारिक व्यवसाय या विरासत के स्रोतों से आय बढ़ सकती है। प्रतिष्ठा बनाए रखने के लिए संसाधनों को अधिक वचनबद्ध करने से सावधान रहें।"
            },
            "health": {
                "en": "Pay attention to your diet and oral health during this transit. The right eye and face area may need extra care. Consuming warm, Sattvic foods helps maintain balance.",
                "hi": "इस गोचर के दौरान अपने आहार और मौखिक स्वास्थ्य पर ध्यान दें। दाहिनी आंख और चेहरे के क्षेत्र को अतिरिक्त देखभाल की आवश्यकता हो सकती है। गर्म, सात्त्विक भोजन का सेवन संतुलन बनाए रखने में मदद करता है।"
            },
        },
        3: {
            "general": {
                "en": "Sun transiting your 3rd house ignites courage and communication abilities. Short travels and interactions with siblings become significant. Your willpower and determination strengthen considerably.",
                "hi": "तीसरे भाव में सूर्य का गोचर साहस और संवाद क्षमताओं को प्रज्वलित करता है। छोटी यात्राएं और भाई-बहनों के साथ बातचीत महत्वपूर्ण हो जाती है। आपका संकल्प और दृढ़ता काफी मजबूत होती है।"
            },
            "love": {
                "en": "Communication in relationships becomes more direct and assertive. Romantic connections through siblings or neighbors are possible. Express your feelings with clarity but temper authority with tenderness.",
                "hi": "रिश्तों में संवाद अधिक प्रत्यक्ष और दृढ़ हो जाता है। भाई-बहनों या पड़ोसियों के माध्यम से रोमांटिक संबंध संभव हैं। अपनी भावनाओं को स्पष्टता से व्यक्त करें पर अधिकार को कोमलता से मिलाएं।"
            },
            "career": {
                "en": "Writing, media, and communication-based careers flourish under this transit. Your bold initiatives in the workplace earn recognition. Short business trips prove highly productive.",
                "hi": "लेखन, मीडिया और संवाद-आधारित करियर इस गोचर में फलते-फूलते हैं। कार्यस्थल पर आपकी साहसिक पहल को मान्यता मिलती है। छोटी व्यावसायिक यात्राएं अत्यधिक उत्पादक सिद्ध होती हैं।"
            },
            "finance": {
                "en": "Gains through communication, publishing, or media ventures are indicated. Siblings may play a role in your financial growth. Investments in technology and communication tools yield returns.",
                "hi": "संवाद, प्रकाशन या मीडिया उपक्रमों से लाभ संकेतित है। भाई-बहन आपकी वित्तीय वृद्धि में भूमिका निभा सकते हैं। प्रौद्योगिकी और संवाद उपकरणों में निवेश लाभकारी रहता है।"
            },
            "health": {
                "en": "Hands, arms, and shoulders require attention during this period. Nervous energy may lead to restlessness or insomnia. Channel excess energy into physical activities like sports or exercise.",
                "hi": "इस अवधि में हाथ, भुजाओं और कंधों पर ध्यान देने की आवश्यकता है। तंत्रिका ऊर्जा बेचैनी या अनिद्रा का कारण बन सकती है। अतिरिक्त ऊर्जा को खेल या व्यायाम जैसी शारीरिक गतिविधियों में लगाएं।"
            },
        },
        4: {
            "general": {
                "en": "Sun in your 4th house brings focus to home, mother, and inner happiness. Matters of property and vehicles come to attention. There may be a desire to renovate your living space or establish authority at home.",
                "hi": "चौथे भाव में सूर्य घर, माता और आंतरिक सुख पर ध्यान लाता है। संपत्ति और वाहन के मामले ध्यान में आते हैं। अपने रहने की जगह का नवीनीकरण करने या घर में अधिकार स्थापित करने की इच्छा हो सकती है।"
            },
            "love": {
                "en": "Domestic harmony becomes a priority in your relationships. Romantic moments at home bring special joy. Balance your authoritative nature with nurturing warmth for best results in love.",
                "hi": "रिश्तों में घरेलू सामंजस्य प्राथमिकता बन जाता है। घर पर रोमांटिक पल विशेष आनंद लाते हैं। प्रेम में सर्वोत्तम परिणामों के लिए अपनी अधिकारपूर्ण प्रकृति को पोषण देने वाली गर्मजोशी से संतुलित करें।"
            },
            "career": {
                "en": "Work from home or real estate ventures gain momentum. Government dealings related to property may arise. Your career may temporarily take a backseat as domestic matters demand attention.",
                "hi": "घर से काम या अचल संपत्ति उपक्रमों को गति मिलती है। संपत्ति से संबंधित सरकारी कार्यवाही हो सकती है। घरेलू मामलों पर ध्यान देने की आवश्यकता से करियर अस्थायी रूप से पीछे रह सकता है।"
            },
            "finance": {
                "en": "Investments in property and real estate are favored but require careful analysis. Expenses on home improvement or family comfort may increase. Government grants or subsidies for housing could benefit you.",
                "hi": "संपत्ति और अचल संपत्ति में निवेश अनुकूल है परंतु सावधानीपूर्वक विश्लेषण आवश्यक है। गृह सुधार या पारिवारिक आराम पर खर्च बढ़ सकता है। आवास के लिए सरकारी अनुदान या सब्सिडी से लाभ हो सकता है।"
            },
            "health": {
                "en": "Chest area and heart health need monitoring during this transit. Emotional stress from family matters may affect your wellbeing. Spending time in peaceful home environments supports healing.",
                "hi": "इस गोचर में छाती और हृदय स्वास्थ्य की निगरानी आवश्यक है। पारिवारिक मामलों से भावनात्मक तनाव आपकी सेहत को प्रभावित कर सकता है। शांतिपूर्ण घरेलू वातावरण में समय बिताना उपचार में सहायक है।"
            },
        },
        5: {
            "general": {
                "en": "Sun in your 5th house brings a brilliant period for creativity, romance, and intellectual pursuits. Children may bring pride and joy. Past merits manifest as new opportunities and recognition.",
                "hi": "पांचवें भाव में सूर्य रचनात्मकता, प्रेम और बौद्धिक गतिविधियों के लिए शानदार समय लाता है। संतान गर्व और आनंद का कारण बन सकती है। पूर्व पुण्य नए अवसरों और मान्यता के रूप में प्रकट होते हैं।"
            },
            "love": {
                "en": "Romance takes center stage with passionate and expressive energy. New love interests may emerge through creative or educational settings. Existing relationships deepen with warmth and playful affection.",
                "hi": "उत्साही और अभिव्यक्तिपूर्ण ऊर्जा के साथ प्रेम केंद्र में आ जाता है। रचनात्मक या शैक्षिक परिवेश से नए प्रेम संबंध उभर सकते हैं। मौजूदा रिश्ते गर्मजोशी और खिलवाड़ भरे स्नेह से गहरे होते हैं।"
            },
            "career": {
                "en": "Creative professions, entertainment, and education sectors thrive during this transit. Speculative ventures guided by intelligence can succeed. Your creative vision earns appreciation from superiors.",
                "hi": "रचनात्मक व्यवसाय, मनोरंजन और शिक्षा क्षेत्र इस गोचर में फलते-फूलते हैं। बुद्धि द्वारा निर्देशित सट्टा उपक्रम सफल हो सकते हैं। आपकी रचनात्मक दृष्टि को वरिष्ठों से सराहना मिलती है।"
            },
            "finance": {
                "en": "Speculative investments and stock markets may bring gains if approached wisely. Income through creative or educational work increases. Avoid gambling or excessive risk-taking despite feeling confident.",
                "hi": "सट्टा निवेश और शेयर बाजार बुद्धिमानी से संपर्क करने पर लाभ दे सकते हैं। रचनात्मक या शैक्षिक कार्य से आय बढ़ती है। आत्मविश्वास होने के बावजूद जुआ या अत्यधिक जोखिम लेने से बचें।"
            },
            "health": {
                "en": "Stomach and digestive system require attention. Mental overexertion from creative or intellectual work can cause fatigue. Balance productive activity with adequate rest and recreation.",
                "hi": "पेट और पाचन तंत्र पर ध्यान देने की आवश्यकता है। रचनात्मक या बौद्धिक कार्य से मानसिक अत्यधिक परिश्रम थकान का कारण बन सकता है। उत्पादक गतिविधि को पर्याप्त विश्राम और मनोरंजन से संतुलित करें।"
            },
        },
        6: {
            "general": {
                "en": "Sun transiting your 6th house empowers you to overcome enemies, diseases, and obstacles. Competition brings out your best fighting spirit. Service-oriented activities and daily routines gain structure.",
                "hi": "छठे भाव में सूर्य का गोचर आपको शत्रुओं, रोगों और बाधाओं पर विजय पाने में सशक्त करता है। प्रतिस्पर्धा आपकी सर्वश्रेष्ठ लड़ाकू भावना को प्रकट करती है। सेवा-उन्मुख गतिविधियों और दैनिक दिनचर्या में संरचना आती है।"
            },
            "love": {
                "en": "Relationships may face minor conflicts or ego clashes during this period. Service to your partner and practical demonstrations of love work best. Avoid letting work stress spill into romantic life.",
                "hi": "इस अवधि में रिश्तों में छोटे-मोटे संघर्ष या अहंकार के टकराव हो सकते हैं। साथी की सेवा और प्रेम के व्यावहारिक प्रदर्शन सबसे अच्छे रहते हैं। कार्य तनाव को प्रेम जीवन में आने से रोकें।"
            },
            "career": {
                "en": "Excellent period for competitive exams, legal matters, and overcoming workplace rivals. Healthcare, law enforcement, and service careers see progress. Your diligence and discipline earn respect from colleagues.",
                "hi": "प्रतियोगी परीक्षाओं, कानूनी मामलों और कार्यस्थल प्रतिद्वंद्वियों पर विजय के लिए उत्कृष्ट समय। स्वास्थ्य सेवा, कानून प्रवर्तन और सेवा करियर में प्रगति होती है। आपकी लगन और अनुशासन सहकर्मियों से सम्मान अर्जित करते हैं।"
            },
            "finance": {
                "en": "Debts can be cleared and financial disputes resolved favorably. Income from service-oriented work or healthcare increases. Budget carefully to avoid unnecessary expenses on health remedies.",
                "hi": "ऋण चुकाए जा सकते हैं और वित्तीय विवाद अनुकूल रूप से हल हो सकते हैं। सेवा-उन्मुख कार्य या स्वास्थ्य सेवा से आय बढ़ती है। स्वास्थ्य उपचारों पर अनावश्यक खर्चों से बचने के लिए सावधानी से बजट बनाएं।"
            },
            "health": {
                "en": "Digestive ailments and inflammatory conditions may surface temporarily. This transit favors starting new health routines and overcoming chronic issues. Regular exercise and disciplined eating bring remarkable improvements.",
                "hi": "पाचन संबंधी बीमारियां और सूजन की स्थिति अस्थायी रूप से सामने आ सकती है। यह गोचर नई स्वास्थ्य दिनचर्या शुरू करने और पुरानी समस्याओं को दूर करने में सहायक है। नियमित व्यायाम और अनुशासित भोजन उल्लेखनीय सुधार लाता है।"
            },
        },
        7: {
            "general": {
                "en": "Sun in your 7th house illuminates partnerships and public dealings. Marriage and business partnerships demand attention and adjustment. You may encounter influential people who shape your path.",
                "hi": "सातवें भाव में सूर्य साझेदारी और सार्वजनिक व्यवहार को प्रकाशित करता है। विवाह और व्यावसायिक साझेदारी पर ध्यान और समायोजन की मांग होती है। आप प्रभावशाली लोगों से मिल सकते हैं जो आपके मार्ग को आकार देते हैं।"
            },
            "love": {
                "en": "Marriage and committed relationships come into sharp focus. A dominant partner or power dynamics in the relationship may surface. Finding balance between independence and togetherness is the key lesson.",
                "hi": "विवाह और प्रतिबद्ध संबंध तीव्र ध्यान में आते हैं। रिश्ते में प्रभावशाली साथी या शक्ति गतिशीलता सामने आ सकती है। स्वतंत्रता और एकजुटता के बीच संतुलन खोजना मुख्य सीख है।"
            },
            "career": {
                "en": "Business partnerships and client relationships take precedence. Legal agreements and contracts require careful attention. Public-facing roles and diplomacy skills are tested and strengthened.",
                "hi": "व्यावसायिक साझेदारी और ग्राहक संबंध प्राथमिकता लेते हैं। कानूनी समझौतों और अनुबंधों पर सावधानीपूर्वक ध्यान देने की आवश्यकता है। सार्वजनिक भूमिकाओं और कूटनीति कौशल की परीक्षा होती है और वे मजबूत होते हैं।"
            },
            "finance": {
                "en": "Joint finances and partnership income are highlighted. Business deals with government entities may prove lucrative. Ensure transparency in all financial partnerships to avoid disputes.",
                "hi": "संयुक्त वित्त और साझेदारी से आय प्रमुख रहती है। सरकारी संस्थाओं के साथ व्यापारिक सौदे लाभकारी सिद्ध हो सकते हैं। विवादों से बचने के लिए सभी वित्तीय साझेदारियों में पारदर्शिता सुनिश्चित करें।"
            },
            "health": {
                "en": "Lower back and kidney area may need care during this transit. Relationship stress can manifest as physical ailments. Maintain work-life balance and practice stress management techniques.",
                "hi": "इस गोचर में पीठ के निचले हिस्से और गुर्दे के क्षेत्र को देखभाल की आवश्यकता हो सकती है। रिश्तों का तनाव शारीरिक बीमारियों के रूप में प्रकट हो सकता है। कार्य-जीवन संतुलन बनाए रखें और तनाव प्रबंधन तकनीकों का अभ्यास करें।"
            },
        },
        8: {
            "general": {
                "en": "Sun transiting your 8th house brings transformation and encounters with hidden matters. Sudden changes in status or identity may occur. Research, occult studies, and investigation work are favored.",
                "hi": "आठवें भाव में सूर्य का गोचर परिवर्तन और छिपे मामलों से सामना लाता है। स्थिति या पहचान में अचानक परिवर्तन हो सकते हैं। अनुसंधान, गूढ़ अध्ययन और जांच कार्य अनुकूल रहते हैं।"
            },
            "love": {
                "en": "Deep emotional transformations in relationships are likely. Intimacy and trust issues may come to the surface for healing. Relationships that survive this transit emerge stronger and more authentic.",
                "hi": "रिश्तों में गहरे भावनात्मक परिवर्तन की संभावना है। अंतरंगता और विश्वास के मुद्दे उपचार के लिए सतह पर आ सकते हैं। इस गोचर से बचकर निकलने वाले रिश्ते अधिक मजबूत और प्रामाणिक बनते हैं।"
            },
            "career": {
                "en": "Behind-the-scenes work and research-based roles gain prominence. Insurance, taxation, and inheritance-related careers benefit. Power dynamics in the workplace require careful navigation.",
                "hi": "पर्दे के पीछे का काम और शोध-आधारित भूमिकाएं प्रमुखता पाती हैं। बीमा, कराधान और विरासत संबंधित करियर को लाभ मिलता है। कार्यस्थल में शक्ति गतिशीलता के लिए सावधानीपूर्वक नेविगेशन आवश्यक है।"
            },
            "finance": {
                "en": "Inheritance, insurance payouts, or unexpected financial windfalls are possible. Joint finances with spouse undergo restructuring. Avoid risky investments and be cautious with others' money.",
                "hi": "विरासत, बीमा भुगतान या अप्रत्याशित वित्तीय लाभ संभव हैं। जीवनसाथी के साथ संयुक्त वित्त का पुनर्गठन होता है। जोखिमपूर्ण निवेश से बचें और दूसरों के धन के साथ सतर्क रहें।"
            },
            "health": {
                "en": "Chronic health issues may flare up and demand attention. Reproductive and elimination system health needs monitoring. This transit favors undergoing therapeutic treatments and deep healing modalities.",
                "hi": "पुरानी स्वास्थ्य समस्याएं भड़क सकती हैं और ध्यान देने की मांग कर सकती हैं। प्रजनन और उत्सर्जन तंत्र के स्वास्थ्य की निगरानी आवश्यक है। यह गोचर चिकित्सीय उपचार और गहन उपचार पद्धतियों के लिए अनुकूल है।"
            },
        },
        9: {
            "general": {
                "en": "Sun in your 9th house activates fortune, higher wisdom, and spiritual growth. Long-distance travel and connections with mentors are highlighted. Your father or guru figures play a significant role.",
                "hi": "नवम भाव में सूर्य भाग्य, उच्च ज्ञान और आध्यात्मिक विकास को सक्रिय करता है। लंबी दूरी की यात्रा और गुरु जनों से संपर्क प्रमुख रहता है। आपके पिता या गुरु तुल्य व्यक्ति महत्वपूर्ण भूमिका निभाते हैं।"
            },
            "love": {
                "en": "Romantic connections may form through educational or spiritual pursuits. Love gains a philosophical dimension and deeper meaning. Cross-cultural relationships or long-distance romance is possible.",
                "hi": "शैक्षिक या आध्यात्मिक गतिविधियों के माध्यम से रोमांटिक संबंध बन सकते हैं। प्रेम को दार्शनिक आयाम और गहरा अर्थ मिलता है। अंतर-सांस्कृतिक संबंध या लंबी दूरी का प्रेम संभव है।"
            },
            "career": {
                "en": "Academic careers, legal professions, and religious vocations flourish. International opportunities and collaborations emerge. Your moral authority and ethical stance enhance professional reputation.",
                "hi": "शैक्षणिक करियर, कानूनी पेशे और धार्मिक व्यवसाय फलते-फूलते हैं। अंतर्राष्ट्रीय अवसर और सहयोग उभरते हैं। आपका नैतिक अधिकार और नैतिक रुख व्यावसायिक प्रतिष्ठा को बढ़ाता है।"
            },
            "finance": {
                "en": "Fortune favors you with gains through foreign connections or higher education. Father's support or paternal inheritance may bring financial benefit. Charitable giving during this period multiplies blessings.",
                "hi": "विदेशी संपर्कों या उच्च शिक्षा के माध्यम से लाभ के साथ भाग्य आपके अनुकूल है। पिता का सहयोग या पैतृक विरासत वित्तीय लाभ ला सकती है। इस अवधि में दान-पुण्य आशीर्वाद को गुणा करता है।"
            },
            "health": {
                "en": "Thighs and hips may need attention during this period. Long travels could cause fatigue if not planned well. Spiritual practices like yoga and meditation significantly boost overall wellbeing.",
                "hi": "इस अवधि में जांघों और कूल्हों पर ध्यान देने की आवश्यकता हो सकती है। लंबी यात्राएं ठीक से योजना न बनाने पर थकान का कारण बन सकती हैं। योग और ध्यान जैसे आध्यात्मिक अभ्यास समग्र स्वास्थ्य को महत्वपूर्ण रूप से बढ़ावा देते हैं।"
            },
        },
        10: {
            "general": {
                "en": "Sun transiting your 10th house is a powerful placement for career and public recognition. Authority, status, and ambition reach their peak. Government dealings and interactions with powerful people are favored.",
                "hi": "दसवें भाव में सूर्य का गोचर करियर और सार्वजनिक मान्यता के लिए शक्तिशाली स्थान है। अधिकार, प्रतिष्ठा और महत्वाकांक्षा अपने चरम पर पहुंचती है। सरकारी कार्य और शक्तिशाली लोगों से बातचीत अनुकूल रहती है।"
            },
            "love": {
                "en": "Your professional success enhances your attractiveness in romantic matters. However, career ambitions may overshadow relationship needs. Find time for love despite professional demands to maintain harmony.",
                "hi": "आपकी व्यावसायिक सफलता प्रेम मामलों में आपके आकर्षण को बढ़ाती है। हालांकि, करियर की महत्वाकांक्षाएं रिश्तों की जरूरतों पर भारी पड़ सकती हैं। सामंजस्य बनाए रखने के लिए व्यावसायिक मांगों के बावजूद प्रेम के लिए समय निकालें।"
            },
            "career": {
                "en": "This is the most powerful transit for career advancement and public honors. Promotions, awards, and recognition from authority figures are likely. Take bold steps in your profession and showcase leadership.",
                "hi": "करियर में उन्नति और सार्वजनिक सम्मान के लिए यह सबसे शक्तिशाली गोचर है। पदोन्नति, पुरस्कार और अधिकारियों से मान्यता की संभावना है। अपने पेशे में साहसिक कदम उठाएं और नेतृत्व का प्रदर्शन करें।"
            },
            "finance": {
                "en": "Income from profession and government sources peaks during this transit. Career-related investments and professional development pay dividends. Use this period to negotiate better compensation.",
                "hi": "इस गोचर के दौरान पेशे और सरकारी स्रोतों से आय चरम पर होती है। करियर-संबंधित निवेश और व्यावसायिक विकास लाभांश देता है। बेहतर मुआवजे के लिए बातचीत करने हेतु इस अवधि का उपयोग करें।"
            },
            "health": {
                "en": "Knees and joints may experience strain from the pressures of ambition. Work-related stress requires conscious management. Maintain a disciplined health routine despite a demanding schedule.",
                "hi": "महत्वाकांक्षा के दबाव से घुटनों और जोड़ों में तनाव हो सकता है। कार्य-संबंधित तनाव के लिए सचेत प्रबंधन आवश्यक है। मांगलिक कार्यक्रम के बावजूद अनुशासित स्वास्थ्य दिनचर्या बनाए रखें।"
            },
        },
        11: {
            "general": {
                "en": "Sun in your 11th house brings excellent results for income, social networking, and fulfillment of desires. Elder siblings and influential friends support your goals. Recognition within your social circle increases.",
                "hi": "ग्यारहवें भाव में सूर्य आय, सामाजिक नेटवर्किंग और इच्छाओं की पूर्ति के लिए उत्कृष्ट परिणाम लाता है। बड़े भाई-बहन और प्रभावशाली मित्र आपके लक्ष्यों का समर्थन करते हैं। सामाजिक दायरे में मान्यता बढ़ती है।"
            },
            "love": {
                "en": "Social gatherings and friend circles become avenues for romantic connections. Love blossoms through shared ideals and group activities. Friendships may transform into deeper romantic relationships.",
                "hi": "सामाजिक समारोह और मित्र मंडल रोमांटिक संबंधों के मार्ग बन जाते हैं। साझा आदर्शों और सामूहिक गतिविधियों से प्रेम पल्लवित होता है। मित्रता गहरे रोमांटिक रिश्तों में बदल सकती है।"
            },
            "career": {
                "en": "Professional networking yields remarkable opportunities during this transit. Large organizations and government networks open doors. Team leadership and collaborative projects bring recognition.",
                "hi": "इस गोचर के दौरान व्यावसायिक नेटवर्किंग उल्लेखनीय अवसर प्रदान करती है। बड़े संगठन और सरकारी नेटवर्क द्वार खोलते हैं। टीम नेतृत्व और सहयोगी परियोजनाएं मान्यता दिलाती हैं।"
            },
            "finance": {
                "en": "Multiple income streams and gains from various sources are indicated. Investments in large-cap stocks and government securities perform well. Friends and networks contribute to financial opportunities.",
                "hi": "विविध स्रोतों से कई आय धाराएं और लाभ संकेतित हैं। लार्ज-कैप शेयरों और सरकारी प्रतिभूतियों में निवेश अच्छा प्रदर्शन करता है। मित्र और नेटवर्क वित्तीय अवसरों में योगदान करते हैं।"
            },
            "health": {
                "en": "Ankles and calves may be vulnerable during this period. Circulatory health benefits from regular physical activity. Social engagements bring positive energy that supports mental wellbeing.",
                "hi": "इस अवधि में टखने और पिंडलियां संवेदनशील हो सकती हैं। नियमित शारीरिक गतिविधि से रक्त संचार स्वास्थ्य को लाभ मिलता है। सामाजिक संलग्नता सकारात्मक ऊर्जा लाती है जो मानसिक स्वास्थ्य का समर्थन करती है।"
            },
        },
        12: {
            "general": {
                "en": "Sun transiting your 12th house directs energy toward spiritual liberation, foreign connections, and inner reflection. Worldly recognition temporarily diminishes as inner growth takes priority. This is an excellent period for meditation and retreat.",
                "hi": "बारहवें भाव में सूर्य का गोचर आध्यात्मिक मुक्ति, विदेशी संपर्कों और आंतरिक चिंतन की ओर ऊर्जा निर्देशित करता है। आंतरिक विकास की प्राथमिकता से सांसारिक मान्यता अस्थायी रूप से कम होती है। यह ध्यान और एकांतवास के लिए उत्कृष्ट समय है।"
            },
            "love": {
                "en": "Love takes on a more spiritual and selfless quality during this period. Secret attractions or hidden aspects of relationships may surface. Practice unconditional giving in love without expectations.",
                "hi": "इस अवधि में प्रेम अधिक आध्यात्मिक और निस्वार्थ गुण धारण करता है। गुप्त आकर्षण या रिश्तों के छिपे पहलू सामने आ सकते हैं। बिना अपेक्षाओं के प्रेम में निःशर्त समर्पण का अभ्यास करें।"
            },
            "career": {
                "en": "Careers in foreign lands, hospitals, or spiritual organizations are favored. Behind-the-scenes contributions outweigh public visibility. Use this quiet period for planning your next career move strategically.",
                "hi": "विदेशों, अस्पतालों या आध्यात्मिक संगठनों में करियर अनुकूल है। पर्दे के पीछे का योगदान सार्वजनिक दृश्यता से अधिक महत्वपूर्ण रहता है। अपने अगले करियर कदम की रणनीतिक योजना बनाने के लिए इस शांत अवधि का उपयोग करें।"
            },
            "finance": {
                "en": "Expenses may increase, particularly on travel, hospitals, or spiritual pursuits. Foreign income sources or overseas investments gain relevance. Practice mindful spending and build savings for future stability.",
                "hi": "खर्च बढ़ सकते हैं, विशेषकर यात्रा, अस्पताल या आध्यात्मिक गतिविधियों पर। विदेशी आय स्रोत या विदेशी निवेश प्रासंगिक होते हैं। सावधानीपूर्वक खर्च करें और भविष्य की स्थिरता के लिए बचत करें।"
            },
            "health": {
                "en": "Feet and sleep patterns need attention during this transit. Energy levels may feel lower than usual, making rest essential. Spiritual practices, hydrotherapy, and foot massage provide excellent remedies.",
                "hi": "इस गोचर में पैरों और नींद के पैटर्न पर ध्यान देने की आवश्यकता है। ऊर्जा का स्तर सामान्य से कम महसूस हो सकता है, जिससे विश्राम आवश्यक हो जाता है। आध्यात्मिक अभ्यास, जल चिकित्सा और पैरों की मालिश उत्कृष्ट उपचार प्रदान करते हैं।"
            },
        },
    },
    # =========================================================================
    # MOON (Chandra) — Mind, emotions, mother, public, fluids, comfort
    # Conditional benefic. Karaka of mind, mother, emotions.
    # =========================================================================
    "Moon": {
        1: {
            "general": {
                "en": "Moon transiting your 1st house heightens emotional sensitivity and intuition. Public interactions increase as your approachable nature draws people in. Mental clarity fluctuates with the Moon's phase.",
                "hi": "चंद्रमा का प्रथम भाव में गोचर भावनात्मक संवेदनशीलता और अंतर्ज्ञान को बढ़ाता है। आपका मिलनसार स्वभाव लोगों को आकर्षित करता है और सार्वजनिक संपर्क बढ़ता है। मानसिक स्पष्टता चंद्रमा की कला के साथ उतार-चढ़ाव करती है।"
            },
            "love": {
                "en": "Emotional availability makes you highly attractive to potential partners. Your nurturing nature draws romantic attention naturally. Be mindful of mood swings that could create unnecessary misunderstandings.",
                "hi": "भावनात्मक उपलब्धता आपको संभावित साथियों के लिए अत्यधिक आकर्षक बनाती है। आपका पोषणकारी स्वभाव स्वाभाविक रूप से रोमांटिक ध्यान आकर्षित करता है। मनोदशा में उतार-चढ़ाव से अनावश्यक गलतफहमी पैदा हो सकती है।"
            },
            "career": {
                "en": "Public-facing roles and careers involving people management thrive. Your empathetic approach wins client trust and team loyalty. Creative and hospitality industries see particular benefit.",
                "hi": "जनसंपर्क भूमिकाएं और लोगों के प्रबंधन से जुड़े करियर फलते-फूलते हैं। आपका सहानुभूतिपूर्ण दृष्टिकोण ग्राहक विश्वास और टीम निष्ठा जीतता है। रचनात्मक और आतिथ्य उद्योगों को विशेष लाभ मिलता है।"
            },
            "finance": {
                "en": "Income from public-related work and the hospitality sector increases. Emotional spending tendencies need conscious management. Liquid assets and short-term investments are more suitable now.",
                "hi": "जनसंपर्क कार्य और आतिथ्य क्षेत्र से आय बढ़ती है। भावनात्मक खर्च की प्रवृत्तियों के लिए सचेत प्रबंधन आवश्यक है। तरल संपत्ति और अल्पकालिक निवेश अभी अधिक उपयुक्त हैं।"
            },
            "health": {
                "en": "Water retention and fluid imbalance may occur during this transit. Mental health requires nurturing through rest and emotional expression. Stay hydrated and pay attention to your body's natural rhythms.",
                "hi": "इस गोचर के दौरान जल प्रतिधारण और तरल असंतुलन हो सकता है। विश्राम और भावनात्मक अभिव्यक्ति के माध्यम से मानसिक स्वास्थ्य का पोषण आवश्यक है। पर्याप्त जल पिएं और शरीर की प्राकृतिक लय पर ध्यान दें।"
            },
        },
        2: {
            "general": {
                "en": "Moon in your 2nd house brings emotional attachment to family and possessions. Speech becomes sweet and emotionally charged. Food habits and dietary preferences may shift during this period.",
                "hi": "दूसरे भाव में चंद्रमा परिवार और संपत्ति के प्रति भावनात्मक लगाव लाता है। वाणी मधुर और भावनात्मक रूप से प्रभावित हो जाती है। इस अवधि में खान-पान की आदतें और आहार प्राथमिकताएं बदल सकती हैं।"
            },
            "love": {
                "en": "Love is expressed through nurturing and providing for family. Comfort food shared together strengthens romantic bonds. Your gentle, caring speech melts hearts and deepens emotional connections.",
                "hi": "प्रेम परिवार के पोषण और देखभाल के माध्यम से व्यक्त होता है। साथ मिलकर भोजन करना रोमांटिक बंधनों को मजबूत करता है। आपकी कोमल, देखभाल भरी वाणी दिलों को पिघलाती है और भावनात्मक जुड़ाव गहरा करती है।"
            },
            "career": {
                "en": "Careers in food, hospitality, and family businesses gain momentum. Your persuasive and sweet communication style wins deals. Financial advisory and wealth management roles suit you well now.",
                "hi": "खाद्य, आतिथ्य और पारिवारिक व्यवसायों में करियर को गति मिलती है। आपकी प्रेरक और मधुर संवाद शैली सौदे जीतती है। वित्तीय सलाहकार और धन प्रबंधन भूमिकाएं अभी आपके लिए उपयुक्त हैं।"
            },
            "finance": {
                "en": "Savings and accumulated wealth fluctuate with emotional spending patterns. Family resources and inherited wealth bring comfort. Investments in food, dairy, or silver may prove beneficial.",
                "hi": "बचत और संचित धन भावनात्मक खर्च पैटर्न के साथ उतार-चढ़ाव करता है। पारिवारिक संसाधन और विरासत में मिली संपत्ति आराम प्रदान करती है। खाद्य, डेयरी या चांदी में निवेश लाभदायक सिद्ध हो सकता है।"
            },
            "health": {
                "en": "Face, throat, and mouth areas may experience sensitivity. Comfort eating could lead to weight fluctuations. Focus on nourishing, home-cooked meals and maintain regular eating schedules.",
                "hi": "चेहरे, गले और मुंह के क्षेत्र में संवेदनशीलता हो सकती है। भावनात्मक भोजन वजन में उतार-चढ़ाव का कारण बन सकता है। पौष्टिक, घर के बने भोजन पर ध्यान दें और नियमित भोजन समय बनाए रखें।"
            },
        },
        3: {
            "general": {
                "en": "Moon transiting your 3rd house stimulates emotional intelligence in communication. Short journeys bring mental refreshment and new connections. Siblings and neighbors become sources of emotional support.",
                "hi": "तीसरे भाव में चंद्रमा का गोचर संवाद में भावनात्मक बुद्धिमत्ता को उत्तेजित करता है। छोटी यात्राएं मानसिक ताजगी और नए संपर्क लाती हैं। भाई-बहन और पड़ोसी भावनात्मक सहारे का स्रोत बनते हैं।"
            },
            "love": {
                "en": "Heartfelt communication strengthens romantic relationships. Love letters, messages, and emotional expression flow easily. Short romantic getaways bring wonderful rejuvenation to your love life.",
                "hi": "हृदयस्पर्शी संवाद रोमांटिक रिश्तों को मजबूत करता है। प्रेम पत्र, संदेश और भावनात्मक अभिव्यक्ति सहजता से प्रवाहित होती है। छोटी रोमांटिक यात्राएं आपके प्रेम जीवन में अद्भुत ताजगी लाती हैं।"
            },
            "career": {
                "en": "Writing, blogging, and emotional storytelling resonate powerfully with audiences. Sales and marketing benefit from your intuitive communication. Collaborative projects with siblings or close associates flourish.",
                "hi": "लेखन, ब्लॉगिंग और भावनात्मक कहानी सुनाना दर्शकों के साथ शक्तिशाली रूप से गूंजता है। बिक्री और विपणन को आपके सहज संवाद से लाभ मिलता है। भाई-बहनों या करीबी सहयोगियों के साथ सहयोगी परियोजनाएं फलती-फूलती हैं।"
            },
            "finance": {
                "en": "Small but consistent gains from communication and media work are likely. Travel expenses increase but bring proportional returns. Collaborative ventures with siblings yield moderate financial benefits.",
                "hi": "संवाद और मीडिया कार्य से छोटे लेकिन निरंतर लाभ की संभावना है। यात्रा खर्च बढ़ते हैं लेकिन आनुपातिक रिटर्न लाते हैं। भाई-बहनों के साथ सहयोगी उपक्रम मध्यम वित्तीय लाभ देते हैं।"
            },
            "health": {
                "en": "Arms, shoulders, and nervous system may feel sensitive during this transit. Mental restlessness can be channeled through creative writing or art. Short walks in nature calm the mind effectively.",
                "hi": "इस गोचर में भुजाओं, कंधों और तंत्रिका तंत्र में संवेदनशीलता महसूस हो सकती है। मानसिक बेचैनी को रचनात्मक लेखन या कला के माध्यम से प्रसारित किया जा सकता है। प्रकृति में छोटी सैर मन को प्रभावी रूप से शांत करती है।"
            },
        },
        4: {
            "general": {
                "en": "Moon in your 4th house is powerfully placed, bringing deep emotional fulfillment and domestic happiness. Connection with mother strengthens and home feels like a sanctuary. Inner peace and contentment prevail.",
                "hi": "चौथे भाव में चंद्रमा शक्तिशाली स्थिति में है, गहरी भावनात्मक पूर्ति और घरेलू सुख लाता है। माता से जुड़ाव मजबूत होता है और घर एक अभयारण्य जैसा लगता है। आंतरिक शांति और संतोष की अनुभूति होती है।"
            },
            "love": {
                "en": "Romantic life is deeply nurturing and emotionally satisfying during this transit. Creating a cozy home environment together strengthens your bond. Emotional security in relationships reaches its highest point.",
                "hi": "इस गोचर के दौरान प्रेम जीवन गहराई से पोषणकारी और भावनात्मक रूप से संतोषजनक होता है। साथ मिलकर एक आरामदायक घरेलू वातावरण बनाना आपके बंधन को मजबूत करता है। रिश्तों में भावनात्मक सुरक्षा अपने उच्चतम बिंदु पर पहुंचती है।"
            },
            "career": {
                "en": "Real estate, interior design, and home-based businesses are especially favored. Nurturing roles in education and childcare bring satisfaction. Work-from-home arrangements prove unusually productive.",
                "hi": "अचल संपत्ति, इंटीरियर डिजाइन और घर-आधारित व्यवसाय विशेष रूप से अनुकूल हैं। शिक्षा और बाल देखभाल में पोषणकारी भूमिकाएं संतोष देती हैं। घर से काम करने की व्यवस्था असामान्य रूप से उत्पादक सिद्ध होती है।"
            },
            "finance": {
                "en": "Property investments and home-related purchases are well-timed. Mother may contribute to your financial wellbeing. Emotional decisions about money should be balanced with practical wisdom.",
                "hi": "संपत्ति निवेश और घर-संबंधित खरीदारी का सही समय है। माता आपकी वित्तीय स्थिति में योगदान दे सकती हैं। धन के बारे में भावनात्मक निर्णयों को व्यावहारिक बुद्धि से संतुलित करना चाहिए।"
            },
            "health": {
                "en": "Chest, lungs, and emotional heart center need gentle care. Comfort at home directly influences your physical wellbeing. Warm milk with turmeric before sleep and peaceful domestic routines support healing.",
                "hi": "छाती, फेफड़े और भावनात्मक हृदय केंद्र को कोमल देखभाल की आवश्यकता है। घर में आराम सीधे आपकी शारीरिक सेहत को प्रभावित करता है। सोने से पहले हल्दी वाला गर्म दूध और शांतिपूर्ण घरेलू दिनचर्या उपचार में सहायक है।"
            },
        },
        5: {
            "general": {
                "en": "Moon transiting your 5th house enhances creativity, romance, and emotional joy. Connection with children deepens and brings happiness. Artistic inspiration flows freely and imagination reaches new heights.",
                "hi": "पांचवें भाव में चंद्रमा का गोचर रचनात्मकता, प्रेम और भावनात्मक आनंद को बढ़ाता है। बच्चों से जुड़ाव गहरा होता है और सुख प्रदान करता है। कलात्मक प्रेरणा स्वतंत्र रूप से बहती है और कल्पना नई ऊंचाइयों तक पहुंचती है।"
            },
            "love": {
                "en": "This is one of the most romantic transits for emotional connection and playful love. Hearts open wide and feelings are expressed with poetic beauty. New romances begin with deep emotional resonance.",
                "hi": "भावनात्मक जुड़ाव और खिलवाड़ भरे प्रेम के लिए यह सबसे रोमांटिक गोचरों में से एक है। हृदय खुलकर प्रकट होते हैं और भावनाएं काव्यात्मक सुंदरता से व्यक्त होती हैं। नए प्रेम संबंध गहरे भावनात्मक अनुनाद से शुरू होते हैं।"
            },
            "career": {
                "en": "Creative arts, entertainment, and education careers receive a powerful emotional boost. Teaching and mentoring roles bring deep fulfillment. Performance arts and emotional storytelling captivate audiences.",
                "hi": "रचनात्मक कला, मनोरंजन और शिक्षा करियर को शक्तिशाली भावनात्मक बल मिलता है। शिक्षण और मार्गदर्शन भूमिकाएं गहरी पूर्ति लाती हैं। प्रदर्शन कला और भावनात्मक कथा-कथन दर्शकों को मोहित करता है।"
            },
            "finance": {
                "en": "Emotional investments in creative projects may yield returns. Avoid speculative decisions based purely on gut feelings. Children-related expenses bring joy despite the financial outlay.",
                "hi": "रचनात्मक परियोजनाओं में भावनात्मक निवेश लाभ दे सकता है। केवल आंतरिक भावनाओं पर आधारित सट्टा निर्णयों से बचें। बच्चों से संबंधित खर्च वित्तीय व्यय के बावजूद आनंद प्रदान करते हैं।"
            },
            "health": {
                "en": "Stomach and digestive health are influenced by emotional states. Joy and laughter serve as powerful medicine during this transit. Creative expression through dance or music provides therapeutic benefits.",
                "hi": "पेट और पाचन स्वास्थ्य भावनात्मक स्थितियों से प्रभावित होते हैं। इस गोचर में हंसी और खुशी शक्तिशाली औषधि का काम करती है। नृत्य या संगीत के माध्यम से रचनात्मक अभिव्यक्ति चिकित्सीय लाभ प्रदान करती है।"
            },
        },
        6: {
            "general": {
                "en": "Moon in your 6th house creates emotional turbulence through conflicts and health concerns. Daily routines feel emotionally draining and service to others becomes necessary. Mental resilience is tested through everyday challenges.",
                "hi": "छठे भाव में चंद्रमा संघर्षों और स्वास्थ्य चिंताओं के माध्यम से भावनात्मक उथल-पुथल पैदा करता है। दैनिक दिनचर्या भावनात्मक रूप से थकाऊ लगती है और दूसरों की सेवा आवश्यक हो जाती है। रोजमर्रा की चुनौतियों से मानसिक लचीलेपन की परीक्षा होती है।"
            },
            "love": {
                "en": "Emotional conflicts in relationships require patience and understanding. Serving your partner with care heals existing wounds. Avoid projecting workplace frustrations onto your romantic life.",
                "hi": "रिश्तों में भावनात्मक संघर्षों के लिए धैर्य और समझ आवश्यक है। देखभाल के साथ साथी की सेवा मौजूदा घावों को भरती है। कार्यस्थल की निराशाओं को प्रेम जीवन पर प्रक्षेपित करने से बचें।"
            },
            "career": {
                "en": "Healthcare, nursing, and social service careers resonate deeply during this transit. Emotional intelligence helps navigate workplace conflicts. Daily work routines may need restructuring for mental wellbeing.",
                "hi": "स्वास्थ्य सेवा, नर्सिंग और सामाजिक सेवा करियर इस गोचर में गहराई से गूंजते हैं। भावनात्मक बुद्धिमत्ता कार्यस्थल संघर्षों को नेविगेट करने में मदद करती है। मानसिक स्वास्थ्य के लिए दैनिक कार्य दिनचर्या का पुनर्गठन आवश्यक हो सकता है।"
            },
            "finance": {
                "en": "Medical expenses or costs related to daily necessities may increase. Lending money based on emotional appeals should be avoided. Structured budgeting helps manage the financial drain of this period.",
                "hi": "चिकित्सा खर्च या दैनिक आवश्यकताओं से संबंधित लागत बढ़ सकती है। भावनात्मक अपील पर आधारित उधार देने से बचना चाहिए। व्यवस्थित बजट बनाना इस अवधि के वित्तीय बोझ को प्रबंधित करने में मदद करता है।"
            },
            "health": {
                "en": "Digestive disturbances linked to emotional stress are common during this transit. Anxiety and worry weaken immunity and overall vitality. Establish calming routines including warm baths and herbal teas.",
                "hi": "इस गोचर में भावनात्मक तनाव से जुड़ी पाचन गड़बड़ी आम है। चिंता और व्याकुलता रोग प्रतिरोधक क्षमता और समग्र जीवन शक्ति को कमजोर करती है। गर्म स्नान और हर्बल चाय सहित शांत करने वाली दिनचर्या स्थापित करें।"
            },
        },
        7: {
            "general": {
                "en": "Moon in your 7th house brings emotional focus on partnerships and marriage. Public dealings increase with greater sensitivity to others' needs. Emotional bonds with your spouse or partner deepen significantly.",
                "hi": "सातवें भाव में चंद्रमा साझेदारी और विवाह पर भावनात्मक ध्यान लाता है। दूसरों की जरूरतों के प्रति अधिक संवेदनशीलता के साथ सार्वजनिक व्यवहार बढ़ता है। जीवनसाथी या साथी के साथ भावनात्मक बंधन काफी गहरा होता है।"
            },
            "love": {
                "en": "Emotional intimacy in relationships reaches beautiful depths during this transit. Your empathetic nature creates deep romantic fulfillment. Marriage proposals and commitments carry strong emotional significance.",
                "hi": "इस गोचर के दौरान रिश्तों में भावनात्मक अंतरंगता सुंदर गहराई तक पहुंचती है। आपका सहानुभूतिपूर्ण स्वभाव गहरी रोमांटिक पूर्ति पैदा करता है। विवाह प्रस्ताव और प्रतिबद्धताएं मजबूत भावनात्मक महत्व रखती हैं।"
            },
            "career": {
                "en": "Client-facing roles and partnership-based businesses benefit from emotional intelligence. Negotiations succeed through empathy and understanding. Counseling and relationship-oriented professions are especially rewarding.",
                "hi": "ग्राहक-सम्मुख भूमिकाओं और साझेदारी-आधारित व्यवसायों को भावनात्मक बुद्धिमत्ता से लाभ मिलता है। सहानुभूति और समझ के माध्यम से बातचीत सफल होती है। परामर्श और रिश्ता-उन्मुख पेशे विशेष रूप से पुरस्कृत होते हैं।"
            },
            "finance": {
                "en": "Spouse's income and joint finances gain prominence. Business partnerships based on emotional trust can be profitable. Avoid making major financial decisions during highly emotional states.",
                "hi": "जीवनसाथी की आय और संयुक्त वित्त प्रमुखता प्राप्त करते हैं। भावनात्मक विश्वास पर आधारित व्यावसायिक साझेदारी लाभदायक हो सकती है। अत्यधिक भावनात्मक अवस्थाओं में बड़े वित्तीय निर्णय लेने से बचें।"
            },
            "health": {
                "en": "Kidneys and lower back need attention, especially regarding fluid balance. Relationship harmony directly impacts your physical health now. Partner-based activities like couples yoga support mutual wellbeing.",
                "hi": "गुर्दे और पीठ के निचले हिस्से पर ध्यान देने की आवश्यकता है, विशेषकर तरल संतुलन के संबंध में। रिश्तों का सामंजस्य अभी सीधे आपके शारीरिक स्वास्थ्य को प्रभावित करता है। कपल योग जैसी साझा गतिविधियां पारस्परिक स्वास्थ्य का समर्थन करती हैं।"
            },
        },
        8: {
            "general": {
                "en": "Moon transiting your 8th house brings emotional intensity and encounters with hidden fears. Transformation through emotional crisis leads to profound inner growth. Psychic sensitivity and intuitive dreams increase.",
                "hi": "आठवें भाव में चंद्रमा का गोचर भावनात्मक तीव्रता और छिपे भय से सामना लाता है। भावनात्मक संकट के माध्यम से परिवर्तन गहन आंतरिक विकास की ओर ले जाता है। मानसिक संवेदनशीलता और सहज ज्ञान युक्त स्वप्न बढ़ते हैं।"
            },
            "love": {
                "en": "Emotional depth in relationships intensifies, revealing hidden layers. Trust issues and vulnerability become central themes in love. Allowing yourself to be truly seen creates transformative intimacy.",
                "hi": "रिश्तों में भावनात्मक गहराई तीव्र होती है, छिपी परतों को प्रकट करती है। विश्वास के मुद्दे और भेद्यता प्रेम में केंद्रीय विषय बन जाते हैं। अपने आप को वास्तव में देखने देना परिवर्तनकारी अंतरंगता पैदा करता है।"
            },
            "career": {
                "en": "Research, psychology, and healing professions gain emotional depth and insight. Insurance and financial investigation work benefits from enhanced intuition. Avoid emotional decision-making in high-stakes professional matters.",
                "hi": "अनुसंधान, मनोविज्ञान और उपचार पेशों को भावनात्मक गहराई और अंतर्दृष्टि मिलती है। बीमा और वित्तीय जांच कार्य को बढ़ी हुई अंतर्ज्ञान से लाभ मिलता है। उच्च-दांव व्यावसायिक मामलों में भावनात्मक निर्णय लेने से बचें।"
            },
            "finance": {
                "en": "Unexpected financial shifts may cause emotional distress. Inheritance or insurance matters carry emotional weight alongside financial significance. Guard against impulsive financial decisions triggered by fear or anxiety.",
                "hi": "अप्रत्याशित वित्तीय बदलाव भावनात्मक कष्ट का कारण बन सकते हैं। विरासत या बीमा मामले वित्तीय महत्व के साथ भावनात्मक भार भी वहन करते हैं। भय या चिंता से प्रेरित आवेगी वित्तीय निर्णयों से सावधान रहें।"
            },
            "health": {
                "en": "Reproductive health and hormonal balance require attention during this transit. Emotional suppression can manifest as chronic physical conditions. Deep breathing, meditation, and emotional release therapies provide relief.",
                "hi": "इस गोचर में प्रजनन स्वास्थ्य और हार्मोनल संतुलन पर ध्यान देने की आवश्यकता है। भावनात्मक दमन पुरानी शारीरिक स्थितियों के रूप में प्रकट हो सकता है। गहरी सांस, ध्यान और भावनात्मक विमोचन चिकित्सा राहत प्रदान करती है।"
            },
        },
        9: {
            "general": {
                "en": "Moon in your 9th house creates emotional connection to spiritual and philosophical pursuits. Long journeys bring peace of mind and emotional renewal. The relationship with your mother and guru deepens.",
                "hi": "नवम भाव में चंद्रमा आध्यात्मिक और दार्शनिक गतिविधियों से भावनात्मक जुड़ाव पैदा करता है। लंबी यात्राएं मन की शांति और भावनात्मक नवीनीकरण लाती हैं। माता और गुरु के साथ संबंध गहरा होता है।"
            },
            "love": {
                "en": "Love finds expression through shared spiritual values and pilgrimages together. Cross-cultural romantic connections carry deep emotional meaning. Philosophy and wisdom in love create lasting emotional bonds.",
                "hi": "साझा आध्यात्मिक मूल्यों और एक साथ तीर्थ यात्राओं के माध्यम से प्रेम अभिव्यक्ति पाता है। अंतर-सांस्कृतिक रोमांटिक संबंध गहरा भावनात्मक अर्थ रखते हैं। प्रेम में दर्शन और ज्ञान स्थायी भावनात्मक बंधन बनाते हैं।"
            },
            "career": {
                "en": "Teaching, counseling, and spiritual guidance careers resonate with emotional authenticity. International work brings emotional fulfillment. Publishing and academic pursuits benefit from intuitive insights.",
                "hi": "शिक्षण, परामर्श और आध्यात्मिक मार्गदर्शन करियर भावनात्मक प्रामाणिकता से गूंजते हैं। अंतर्राष्ट्रीय कार्य भावनात्मक पूर्ति लाता है। प्रकाशन और शैक्षणिक गतिविधियों को सहज अंतर्दृष्टि से लाभ मिलता है।"
            },
            "finance": {
                "en": "Financial blessings come through spiritual practices and acts of compassion. Foreign investments guided by intuition may prove rewarding. Charitable donations during this period generate positive karmic returns.",
                "hi": "आध्यात्मिक अभ्यास और करुणा के कार्यों से वित्तीय आशीर्वाद मिलता है। अंतर्ज्ञान द्वारा निर्देशित विदेशी निवेश पुरस्कृत सिद्ध हो सकते हैं। इस अवधि में दान सकारात्मक कर्मफल उत्पन्न करता है।"
            },
            "health": {
                "en": "Thighs and liver need gentle care during this transit period. Pilgrimage and spiritual retreats provide profound healing for body and mind. Faith and positive emotions significantly strengthen your immune system.",
                "hi": "इस गोचर अवधि में जांघों और यकृत को कोमल देखभाल की आवश्यकता है। तीर्थयात्रा और आध्यात्मिक एकांतवास शरीर और मन के लिए गहन उपचार प्रदान करते हैं। विश्वास और सकारात्मक भावनाएं आपकी प्रतिरक्षा प्रणाली को महत्वपूर्ण रूप से मजबूत करती हैं।"
            },
        },
        10: {
            "general": {
                "en": "Moon transiting your 10th house brings emotional investment in career and public image. Your nurturing qualities earn public appreciation and recognition. Reputation is influenced by how emotionally connected you appear.",
                "hi": "दसवें भाव में चंद्रमा का गोचर करियर और सार्वजनिक छवि में भावनात्मक निवेश लाता है। आपके पोषणकारी गुण सार्वजनिक प्रशंसा और मान्यता अर्जित करते हैं। प्रतिष्ठा इस बात से प्रभावित होती है कि आप कितने भावनात्मक रूप से जुड़े दिखते हैं।"
            },
            "love": {
                "en": "Your public success and emotional warmth make you especially attractive now. Work-life balance challenges may strain romantic relationships. A partner who supports your career ambitions strengthens the bond immensely.",
                "hi": "आपकी सार्वजनिक सफलता और भावनात्मक गर्मजोशी अभी आपको विशेष रूप से आकर्षक बनाती है। कार्य-जीवन संतुलन की चुनौतियां रोमांटिक रिश्तों पर दबाव डाल सकती हैं। करियर महत्वाकांक्षाओं का समर्थन करने वाला साथी बंधन को बेहद मजबूत करता है।"
            },
            "career": {
                "en": "Public visibility peaks as your emotional authenticity resonates with people. Careers in public service, healthcare management, and hospitality shine. Let your genuine care for others guide professional decisions.",
                "hi": "आपकी भावनात्मक प्रामाणिकता लोगों के साथ गूंजने से सार्वजनिक दृश्यता चरम पर होती है। सार्वजनिक सेवा, स्वास्थ्य प्रबंधन और आतिथ्य में करियर चमकता है। दूसरों के लिए आपकी सच्ची देखभाल को व्यावसायिक निर्णयों का मार्गदर्शन करने दें।"
            },
            "finance": {
                "en": "Professional income benefits from public approval and emotional connection with clients. Government or institutional support for your work may materialize. Invest in building your professional reputation as a long-term asset.",
                "hi": "सार्वजनिक अनुमोदन और ग्राहकों के साथ भावनात्मक जुड़ाव से व्यावसायिक आय को लाभ मिलता है। आपके कार्य के लिए सरकारी या संस्थागत सहायता मिल सकती है। अपनी व्यावसायिक प्रतिष्ठा को दीर्घकालिक संपत्ति के रूप में बनाने में निवेश करें।"
            },
            "health": {
                "en": "Knees and skeletal system may feel the strain of emotional pressures at work. Public scrutiny can cause anxiety affecting physical health. Set clear boundaries between professional obligations and personal rest.",
                "hi": "कार्य पर भावनात्मक दबाव से घुटनों और कंकाल तंत्र पर तनाव महसूस हो सकता है। सार्वजनिक जांच चिंता पैदा कर सकती है जो शारीरिक स्वास्थ्य को प्रभावित करती है। व्यावसायिक दायित्वों और व्यक्तिगत विश्राम के बीच स्पष्ट सीमाएं निर्धारित करें।"
            },
        },
        11: {
            "general": {
                "en": "Moon in your 11th house brings emotional fulfillment through social connections and group activities. Desires and wishes find emotional support from friends. Elder siblings provide nurturing guidance during this period.",
                "hi": "ग्यारहवें भाव में चंद्रमा सामाजिक संपर्कों और सामूहिक गतिविधियों के माध्यम से भावनात्मक पूर्ति लाता है। इच्छाओं और कामनाओं को मित्रों से भावनात्मक सहयोग मिलता है। बड़े भाई-बहन इस अवधि में पोषणकारी मार्गदर्शन प्रदान करते हैं।"
            },
            "love": {
                "en": "Friendships may blossom into romantic relationships with emotional depth. Social events create opportunities for meaningful romantic encounters. Love shared within community contexts feels particularly fulfilling.",
                "hi": "मित्रता भावनात्मक गहराई के साथ रोमांटिक रिश्तों में खिल सकती है। सामाजिक कार्यक्रम सार्थक रोमांटिक मुलाकातों के अवसर पैदा करते हैं। सामुदायिक संदर्भ में साझा प्रेम विशेष रूप से संतोषजनक लगता है।"
            },
            "career": {
                "en": "Networking and team-based projects bring both emotional satisfaction and professional gains. Social media and community management roles thrive. Your ability to emotionally connect with large groups creates opportunities.",
                "hi": "नेटवर्किंग और टीम-आधारित परियोजनाएं भावनात्मक संतुष्टि और व्यावसायिक लाभ दोनों लाती हैं। सोशल मीडिया और सामुदायिक प्रबंधन भूमिकाएं फलती-फूलती हैं। बड़े समूहों से भावनात्मक रूप से जुड़ने की आपकी क्षमता अवसर पैदा करती है।"
            },
            "finance": {
                "en": "Income through social networks and group ventures increases. Friends may introduce profitable financial opportunities. Emotional satisfaction from gains matters as much as the monetary value itself.",
                "hi": "सामाजिक नेटवर्क और सामूहिक उपक्रमों से आय बढ़ती है। मित्र लाभदायक वित्तीय अवसरों से परिचय करा सकते हैं। लाभ से भावनात्मक संतुष्टि मौद्रिक मूल्य जितनी ही महत्वपूर्ण है।"
            },
            "health": {
                "en": "Calves and circulatory system benefit from group physical activities. Social support networks directly enhance your mental wellbeing. Laughter with friends proves to be the best medicine during this transit.",
                "hi": "सामूहिक शारीरिक गतिविधियों से पिंडलियों और रक्त संचार तंत्र को लाभ मिलता है। सामाजिक सहायता नेटवर्क सीधे आपकी मानसिक सेहत को बढ़ाते हैं। इस गोचर में मित्रों के साथ हंसी सबसे अच्छी दवा सिद्ध होती है।"
            },
        },
        12: {
            "general": {
                "en": "Moon transiting your 12th house heightens spiritual sensitivity and need for solitude. Dreams become vivid and emotionally significant. This is a period of emotional release, healing, and preparation for renewal.",
                "hi": "बारहवें भाव में चंद्रमा का गोचर आध्यात्मिक संवेदनशीलता और एकांत की आवश्यकता को बढ़ाता है। स्वप्न ज्वलंत और भावनात्मक रूप से महत्वपूर्ण हो जाते हैं। यह भावनात्मक विमोचन, उपचार और नवीनीकरण की तैयारी का समय है।"
            },
            "love": {
                "en": "Love takes on a deeply spiritual and selfless dimension. Hidden emotions or secret attractions may surface for resolution. Unconditional compassion and forgiveness transform your romantic relationships.",
                "hi": "प्रेम गहराई से आध्यात्मिक और निस्वार्थ आयाम धारण करता है। छिपी भावनाएं या गुप्त आकर्षण समाधान के लिए सामने आ सकते हैं। निःशर्त करुणा और क्षमा आपके रोमांटिक रिश्तों को रूपांतरित करती है।"
            },
            "career": {
                "en": "Careers in hospitals, ashrams, and foreign lands bring emotional peace. Creative work done in solitude yields profound results. Take time for introspection before making major career decisions.",
                "hi": "अस्पतालों, आश्रमों और विदेशों में करियर भावनात्मक शांति लाता है। एकांत में किया गया रचनात्मक कार्य गहन परिणाम देता है। बड़े करियर निर्णय लेने से पहले आत्मनिरीक्षण के लिए समय लें।"
            },
            "finance": {
                "en": "Expenses on comfort, sleep aids, and spiritual retreats may increase. Foreign earnings or hidden sources of income may surface. Practice detachment from material outcomes while maintaining practical financial discipline.",
                "hi": "आराम, नींद सहायता और आध्यात्मिक एकांतवास पर खर्च बढ़ सकता है। विदेशी आय या आय के छिपे स्रोत सामने आ सकते हैं। व्यावहारिक वित्तीय अनुशासन बनाए रखते हुए भौतिक परिणामों से वैराग्य का अभ्यास करें।"
            },
            "health": {
                "en": "Sleep quality and feet health require careful attention during this transit. Emotional exhaustion can manifest as physical fatigue and lethargy. Warm foot soaks, adequate sleep, and gentle meditation support complete healing.",
                "hi": "इस गोचर में नींद की गुणवत्ता और पैरों के स्वास्थ्य पर सावधानीपूर्वक ध्यान देने की आवश्यकता है। भावनात्मक थकान शारीरिक थकान और सुस्ती के रूप में प्रकट हो सकती है। गर्म पैर स्नान, पर्याप्त नींद और कोमल ध्यान पूर्ण उपचार का समर्थन करते हैं।"
            },
        },
    },
}
