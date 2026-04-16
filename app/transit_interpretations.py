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
}
