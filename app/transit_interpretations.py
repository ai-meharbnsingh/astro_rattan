"""Transit interpretation fragments — 9 planets x 12 houses x 5 areas, bilingual.

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
    # =========================================================================
    # MARS (Mangal) — Energy, courage, siblings, property, surgery, aggression
    # Natural malefic. Karaka of energy, brothers, land, blood.
    # =========================================================================
    "Mars": {
        1: {
            "general": {"en": "Mars transiting your 1st house fuels tremendous energy and assertiveness. You feel driven to take bold action and assert your identity. Physical vitality peaks but watch for impatience and aggression.", "hi": "मंगल का प्रथम भाव में गोचर जबरदस्त ऊर्जा और दृढ़ता प्रदान करता है। आप साहसिक कार्रवाई करने और अपनी पहचान स्थापित करने के लिए प्रेरित महसूस करते हैं। शारीरिक जीवन शक्ति चरम पर है लेकिन अधीरता और आक्रामकता से सावधान रहें।"},
            "love": {"en": "Passion and desire intensify in relationships. You may come across as domineering to partners. Channel the fire energy into romantic gestures rather than arguments.", "hi": "संबंधों में जुनून और इच्छा तीव्र होती है। आप साथी को दबंग लग सकते हैं। इस अग्नि ऊर्जा को विवादों के बजाय रोमांटिक भावों में प्रवाहित करें।"},
            "career": {"en": "Professional ambition soars and you push hard for results. Competitive situations favor you now. Leadership roles suit your current energy but avoid unnecessary confrontation with colleagues.", "hi": "पेशेवर महत्वाकांक्षा बढ़ती है और आप परिणामों के लिए कड़ी मेहनत करते हैं। प्रतिस्पर्धात्मक स्थितियां आपके अनुकूल हैं। नेतृत्व की भूमिकाएं उपयुक्त हैं लेकिन सहकर्मियों से अनावश्यक टकराव से बचें।"},
            "finance": {"en": "Impulse spending on sports, vehicles, or property is likely. Earnings through physical effort and competitive ventures increase. Budget consciously to avoid overspending on ego purchases.", "hi": "खेल, वाहन या संपत्ति पर आवेगपूर्ण खर्च की संभावना है। शारीरिक प्रयास और प्रतिस्पर्धी उद्यमों से आय बढ़ती है। अहंकारी खरीदारी से बचने के लिए सोच-समझकर बजट बनाएं।"},
            "health": {"en": "Energy is exceptionally high but risk of injuries, fevers, and inflammation increases. Head and face areas need extra care. Regular exercise channels this Mars energy constructively.", "hi": "ऊर्जा असाधारण रूप से उच्च है लेकिन चोट, बुखार और सूजन का जोखिम बढ़ता है। सिर और चेहरे के क्षेत्र पर विशेष ध्यान दें। नियमित व्यायाम इस मंगल ऊर्जा को रचनात्मक रूप से प्रवाहित करता है।"},
        },
        2: {
            "general": {"en": "Mars in the 2nd house brings assertive speech and determination to increase wealth. Family dynamics may become heated as you speak your mind directly. Guard against harsh words that damage close bonds.", "hi": "मंगल दूसरे भाव में दृढ़ वाणी और धन बढ़ाने का संकल्प लाता है। स्पष्ट बोलने से पारिवारिक माहौल गरम हो सकता है। कठोर शब्दों से बचें जो करीबी रिश्तों को नुकसान पहुंचाएं।"},
            "love": {"en": "Direct and passionate expression of affection marks this period. Family acceptance of relationships becomes important. Arguments over shared finances with partner are possible.", "hi": "इस अवधि में स्नेह की प्रत्यक्ष और भावुक अभिव्यक्ति होती है। रिश्तों में पारिवारिक स्वीकृति महत्वपूर्ण हो जाती है। साथी के साथ साझा वित्त पर विवाद संभव है।"},
            "career": {"en": "Aggressive pursuit of higher earnings drives career decisions. Sales, negotiation, and deal-closing abilities peak. Avoid burning bridges through overly forceful communication.", "hi": "उच्च आय की आक्रामक खोज करियर निर्णयों को प्रेरित करती है। बिक्री, बातचीत और सौदे करने की क्षमता चरम पर है। अत्यधिक बलपूर्वक संवाद से पुल न जलाएं।"},
            "finance": {"en": "Earnings potential increases through bold financial moves. Expenses on food, luxury items, and family commitments rise sharply. Real estate and property investments attract your attention.", "hi": "साहसिक वित्तीय कदमों से कमाई की संभावना बढ़ती है। भोजन, विलासिता और पारिवारिक प्रतिबद्धताओं पर खर्च तेजी से बढ़ता है। अचल संपत्ति निवेश आपका ध्यान आकर्षित करता है।"},
            "health": {"en": "Teeth, jaw, and throat areas may experience inflammation or stress. Dietary excesses lead to digestive heat. Cooling foods and mindful eating support balance during this transit.", "hi": "दांत, जबड़ा और गले के क्षेत्र में सूजन या तनाव हो सकता है। आहार की अधिकता से पाचन गर्मी होती है। शीतल भोजन और सचेत आहार इस गोचर में संतुलन का समर्थन करते हैं।"},
        },
        3: {
            "general": {"en": "Mars in the 3rd house gives exceptional courage and drive for communication. Short travels, adventures, and competitive pursuits energize you. Sibling relationships may spark with intensity.", "hi": "मंगल तीसरे भाव में असाधारण साहस और संवाद की प्रेरणा देता है। छोटी यात्राएं, साहसिक कार्य और प्रतिस्पर्धी गतिविधियां आपको ऊर्जावान बनाती हैं। भाई-बहनों के साथ संबंध तीव्र हो सकते हैं।"},
            "love": {"en": "Flirtatious and bold romantic energy flows naturally. Communication with partners becomes direct and action-oriented. Short romantic getaways or adventure dates bring excitement.", "hi": "छेड़खानी और साहसी रोमांटिक ऊर्जा स्वाभाविक रूप से प्रवाहित होती है। साथी के साथ संवाद प्रत्यक्ष और कार्योन्मुखी हो जाता है। छोटी रोमांटिक यात्राएं उत्साह लाती हैं।"},
            "career": {"en": "Writing, media, sales, and communication-based careers thrive. Initiative in projects brings swift results. Competitive presentations and pitches go in your favor.", "hi": "लेखन, मीडिया, बिक्री और संवाद-आधारित करियर फलते-फूलते हैं। परियोजनाओं में पहल से त्वरित परिणाम मिलते हैं। प्रतिस्पर्धी प्रस्तुतियां आपके पक्ष में जाती हैं।"},
            "finance": {"en": "Short-term gains through quick deals and commissions are indicated. Travel and communication expenses increase. Sibling-related financial dealings may require attention.", "hi": "त्वरित सौदों और कमीशन से अल्पकालिक लाभ संकेतित है। यात्रा और संवाद खर्च बढ़ते हैं। भाई-बहनों से संबंधित वित्तीय मामलों पर ध्यान देने की आवश्यकता हो सकती है।"},
            "health": {"en": "Hands, arms, and shoulders are active zones requiring care during physical activities. Nervous energy may cause restlessness. Channel excess energy through exercise or competitive sports.", "hi": "हाथ, बाहें और कंधे सक्रिय क्षेत्र हैं जिन्हें शारीरिक गतिविधियों में देखभाल की आवश्यकता है। तंत्रिका ऊर्जा बेचैनी का कारण बन सकती है। अतिरिक्त ऊर्जा को व्यायाम या खेल में लगाएं।"},
        },
        4: {
            "general": {"en": "Mars in the 4th house stirs domestic energy and property matters. Renovations, land disputes, or home improvements demand your attention. Inner restlessness pushes you to transform your living environment.", "hi": "मंगल चौथे भाव में घरेलू ऊर्जा और संपत्ति मामलों को उत्तेजित करता है। नवीकरण, भूमि विवाद या गृह सुधार आपका ध्यान मांगते हैं। आंतरिक बेचैनी आपको अपने रहने के वातावरण को बदलने के लिए प्रेरित करती है।"},
            "love": {"en": "Family tensions may spill into romantic life. Creating a harmonious home becomes a shared project with your partner. Mother or maternal figures may need extra attention.", "hi": "पारिवारिक तनाव रोमांटिक जीवन में आ सकता है। सामंजस्यपूर्ण घर बनाना साथी के साथ साझा परियोजना बनता है। माता या मातृ व्यक्तियों को अतिरिक्त ध्यान की आवश्यकता हो सकती है।"},
            "career": {"en": "Working from home or property-related careers get a boost. Real estate transactions and construction activities favor bold action. Authority at workplace may feel challenged.", "hi": "घर से काम करने या संपत्ति संबंधित करियर को बढ़ावा मिलता है। अचल संपत्ति लेनदेन और निर्माण गतिविधियां साहसिक कार्रवाई का समर्थन करती हैं। कार्यस्थल पर अधिकार को चुनौती मिल सकती है।"},
            "finance": {"en": "Property investments, home renovation costs, and vehicle expenses dominate the financial picture. Land and real estate dealings may prove profitable with careful negotiation.", "hi": "संपत्ति निवेश, गृह नवीकरण लागत और वाहन खर्च वित्तीय तस्वीर पर हावी हैं। सावधानीपूर्वक बातचीत से भूमि और अचल संपत्ति सौदे लाभदायक हो सकते हैं।"},
            "health": {"en": "Chest, heart area, and blood pressure need monitoring. Emotional stress affects physical wellbeing through internal heat. Cooling pranayama and calm domestic environment support health.", "hi": "छाती, हृदय क्षेत्र और रक्तचाप की निगरानी आवश्यक है। भावनात्मक तनाव आंतरिक गर्मी से शारीरिक स्वास्थ्य को प्रभावित करता है। शीतली प्राणायाम और शांत घरेलू वातावरण स्वास्थ्य का समर्थन करते हैं।"},
        },
        5: {
            "general": {"en": "Mars in the 5th house ignites creativity, romance, and competitive spirit. Children-related matters demand active involvement. Speculative ventures and bold artistic expression call to you strongly.", "hi": "मंगल पांचवें भाव में रचनात्मकता, रोमांस और प्रतिस्पर्धी भावना को प्रज्वलित करता है। संतान संबंधी मामले सक्रिय भागीदारी की मांग करते हैं। सट्टा उद्यम और साहसी कलात्मक अभिव्यक्ति आपको पुकारती है।"},
            "love": {"en": "Romantic passion burns intensely and new attractions spark easily. Existing relationships experience renewed physical chemistry. Be mindful of possessiveness or jealousy that may arise.", "hi": "रोमांटिक जुनून तीव्रता से जलता है और नए आकर्षण आसानी से पैदा होते हैं। मौजूदा संबंधों में शारीरिक रसायन नवीनीकृत होता है। अधिकारवाद या ईर्ष्या से सावधान रहें।"},
            "career": {"en": "Creative industries, sports, entertainment, and speculation-based careers flourish. Teaching and mentoring roles energize you. Bold presentations of your ideas win recognition.", "hi": "रचनात्मक उद्योग, खेल, मनोरंजन और सट्टा-आधारित करियर फलते-फूलते हैं। शिक्षण और मार्गदर्शन भूमिकाएं आपको ऊर्जावान बनाती हैं। अपने विचारों की साहसी प्रस्तुति मान्यता दिलाती है।"},
            "finance": {"en": "Speculative gains are possible but losses are equally likely without discipline. Spending on children, entertainment, and creative pursuits increases. Stock market and investment timing needs caution.", "hi": "सट्टा लाभ संभव है लेकिन अनुशासन के बिना नुकसान भी उतना ही संभव है। संतान, मनोरंजन और रचनात्मक गतिविधियों पर खर्च बढ़ता है। शेयर बाजार और निवेश समय में सावधानी आवश्यक है।"},
            "health": {"en": "Stomach and upper abdomen areas need attention. Pitta imbalance from intense activity or spicy food is common. Regular meals and cooling foods maintain digestive balance.", "hi": "पेट और ऊपरी उदर क्षेत्र पर ध्यान देने की आवश्यकता है। तीव्र गतिविधि या मसालेदार भोजन से पित्त असंतुलन आम है। नियमित भोजन और शीतल आहार पाचन संतुलन बनाए रखते हैं।"},
        },
        6: {
            "general": {"en": "Mars in the 6th house grants victory over enemies and competitors. Legal battles and disputes resolve in your favor through persistent effort. Service-oriented work and health routines benefit from martial discipline.", "hi": "मंगल छठे भाव में शत्रुओं और प्रतिस्पर्धियों पर विजय प्रदान करता है। लगातार प्रयास से कानूनी लड़ाई और विवाद आपके पक्ष में हल होते हैं। सेवा-उन्मुख कार्य और स्वास्थ्य दिनचर्या अनुशासन से लाभान्वित होती है।"},
            "love": {"en": "Service and practical support define your love language during this period. Resolving relationship conflicts becomes easier with direct action. Health of partner may need your attention.", "hi": "इस अवधि में सेवा और व्यावहारिक सहायता आपकी प्रेम भाषा को परिभाषित करती है। प्रत्यक्ष कार्रवाई से संबंध विवादों का समाधान आसान हो जाता है। साथी के स्वास्थ्य पर ध्यान देने की आवश्यकता हो सकती है।"},
            "career": {"en": "Competitive work environments bring out your best performance. Medical, military, legal, and service professions thrive. Overcoming workplace obstacles builds your professional reputation.", "hi": "प्रतिस्पर्धी कार्य वातावरण आपका सर्वश्रेष्ठ प्रदर्शन निकालते हैं। चिकित्सा, सैन्य, कानूनी और सेवा व्यवसाय फलते-फूलते हैं। कार्यस्थल बाधाओं पर विजय आपकी पेशेवर प्रतिष्ठा बनाती है।"},
            "finance": {"en": "Debts can be cleared through aggressive repayment strategies. Expenses on health treatments and legal matters are indicated. Earnings through competitive and service-related work increase.", "hi": "आक्रामक पुनर्भुगतान रणनीतियों से ऋण चुकाए जा सकते हैं। स्वास्थ्य उपचार और कानूनी मामलों पर खर्च संकेतित है। प्रतिस्पर्धी और सेवा-संबंधित कार्य से कमाई बढ़ती है।"},
            "health": {"en": "Excellent period for starting rigorous fitness regimens and overcoming chronic ailments. Surgical interventions have favorable outcomes. Immune system strengthens through disciplined habits.", "hi": "कठोर फिटनेस आहार शुरू करने और पुरानी बीमारियों को दूर करने के लिए उत्कृष्ट अवधि। शल्य चिकित्सा हस्तक्षेप के अनुकूल परिणाम होते हैं। अनुशासित आदतों से प्रतिरक्षा प्रणाली मजबूत होती है।"},
        },
        7: {
            "general": {"en": "Mars in the 7th house intensifies partnerships and public dealings. Business negotiations become forceful and results-oriented. Relationship dynamics shift toward passionate engagement or confrontation.", "hi": "मंगल सातवें भाव में साझेदारी और सार्वजनिक व्यवहार को तीव्र करता है। व्यापारिक बातचीत बलपूर्वक और परिणाम-उन्मुख हो जाती है। संबंध गतिशीलता भावुक जुड़ाव या टकराव की ओर बदलती है।"},
            "love": {"en": "Marriage and partnerships experience heightened passion but also potential conflict. Direct communication about desires and expectations is essential. New relationships start with intense attraction.", "hi": "विवाह और साझेदारी में बढ़ा हुआ जुनून लेकिन संभावित संघर्ष भी अनुभव होता है। इच्छाओं और अपेक्षाओं के बारे में सीधा संवाद आवश्यक है। नए संबंध तीव्र आकर्षण से शुरू होते हैं।"},
            "career": {"en": "Business partnerships and client relationships demand assertive handling. Contract negotiations favor bold proposals. Public-facing roles benefit from your confident energy.", "hi": "व्यावसायिक साझेदारी और ग्राहक संबंध दृढ़ प्रबंधन की मांग करते हैं। अनुबंध वार्ता में साहसिक प्रस्ताव अनुकूल होते हैं। सार्वजनिक भूमिकाएं आपकी आत्मविश्वासी ऊर्जा से लाभान्वित होती हैं।"},
            "finance": {"en": "Joint finances and partnership investments require careful negotiation. Legal settlements or business deals may involve significant sums. Spouse or partner's financial decisions affect your portfolio.", "hi": "संयुक्त वित्त और साझेदारी निवेश में सावधानीपूर्वक बातचीत आवश्यक है। कानूनी समझौतों या व्यापारिक सौदों में बड़ी राशि शामिल हो सकती है। पति/पत्नी या साथी के वित्तीय निर्णय आपके पोर्टफोलियो को प्रभावित करते हैं।"},
            "health": {"en": "Reproductive system and lower back areas need attention. Partner's health issues may cause concern. Overexertion in physical relationships or competitions needs moderation.", "hi": "प्रजनन प्रणाली और पीठ के निचले हिस्से पर ध्यान देने की आवश्यकता है। साथी की स्वास्थ्य समस्याएं चिंता का कारण हो सकती हैं। शारीरिक संबंधों या प्रतिस्पर्धाओं में अत्यधिक परिश्रम में संयम आवश्यक है।"},
        },
        8: {
            "general": {"en": "Mars in the 8th house brings transformation through crisis and intense experiences. Hidden matters surface and require courageous handling. Research, investigation, and occult studies attract your warrior spirit.", "hi": "मंगल आठवें भाव में संकट और तीव्र अनुभवों के माध्यम से परिवर्तन लाता है। छिपे मामले सतह पर आते हैं और साहसी प्रबंधन की आवश्यकता होती है। अनुसंधान, जांच और गूढ़ अध्ययन आपकी योद्धा भावना को आकर्षित करते हैं।"},
            "love": {"en": "Deep, intense emotional and physical connections define relationships. Trust and jealousy themes emerge powerfully. Transformative experiences with partners create unbreakable bonds or decisive separations.", "hi": "गहरे, तीव्र भावनात्मक और शारीरिक संबंध रिश्तों को परिभाषित करते हैं। विश्वास और ईर्ष्या के विषय शक्तिशाली रूप से उभरते हैं। साथी के साथ परिवर्तनकारी अनुभव अटूट बंधन या निर्णायक अलगाव बनाते हैं।"},
            "career": {"en": "Research, surgery, forensics, insurance, and crisis management careers thrive. Uncovering hidden information gives professional advantage. Avoid power struggles with authority figures.", "hi": "अनुसंधान, शल्य चिकित्सा, फोरेंसिक, बीमा और संकट प्रबंधन करियर फलते-फूलते हैं। छिपी जानकारी उजागर करना पेशेवर लाभ देता है। अधिकारियों के साथ सत्ता संघर्ष से बचें।"},
            "finance": {"en": "Insurance claims, inheritance matters, and joint financial dealings become active. Hidden debts or financial obligations may surface unexpectedly. Strategic financial restructuring yields positive results.", "hi": "बीमा दावे, विरासत मामले और संयुक्त वित्तीय लेनदेन सक्रिय हो जाते हैं। छिपे ऋण या वित्तीय दायित्व अप्रत्याशित रूप से सामने आ सकते हैं। रणनीतिक वित्तीय पुनर्गठन सकारात्मक परिणाम देता है।"},
            "health": {"en": "Surgical procedures have good outcomes but recovery needs patience. Reproductive and excretory system health requires vigilance. Chronic conditions may flare up but respond well to intensive treatment.", "hi": "शल्य प्रक्रियाओं के अच्छे परिणाम होते हैं लेकिन रिकवरी में धैर्य आवश्यक है। प्रजनन और उत्सर्जन प्रणाली स्वास्थ्य में सतर्कता आवश्यक है। पुरानी स्थितियां भड़क सकती हैं लेकिन गहन उपचार से अच्छी प्रतिक्रिया देती हैं।"},
        },
        9: {
            "general": {"en": "Mars in the 9th house drives passionate pursuit of higher knowledge and dharma. Long-distance travel for adventure or learning beckons strongly. Father's health or relationship with mentors may need attention.", "hi": "मंगल नौवें भाव में उच्च ज्ञान और धर्म की भावुक खोज को प्रेरित करता है। साहसिक या सीखने के लिए लंबी दूरी की यात्रा आपको पुकारती है। पिता का स्वास्थ्य या गुरुओं के साथ संबंध पर ध्यान आवश्यक हो सकता है।"},
            "love": {"en": "Philosophical and spiritual compatibility becomes important in relationships. Foreign or long-distance romance possibilities increase. Religious or cultural differences in partnerships require patient understanding.", "hi": "संबंधों में दार्शनिक और आध्यात्मिक अनुकूलता महत्वपूर्ण हो जाती है। विदेशी या लंबी दूरी के रोमांस की संभावनाएं बढ़ती हैं। साझेदारी में धार्मिक या सांस्कृतिक भिन्नताओं में धैर्यपूर्ण समझ आवश्यक है।"},
            "career": {"en": "Academic, legal, publishing, and international careers gain momentum. Bold initiatives in higher education or overseas ventures yield results. Advocating for your beliefs creates professional opportunities.", "hi": "शैक्षणिक, कानूनी, प्रकाशन और अंतरराष्ट्रीय करियर में गति आती है। उच्च शिक्षा या विदेशी उद्यमों में साहसिक पहल परिणाम देती है। अपने विश्वासों की वकालत पेशेवर अवसर बनाती है।"},
            "finance": {"en": "International trade, publishing royalties, and education-related investments attract attention. Father or guru may influence financial decisions. Long-distance financial dealings require careful documentation.", "hi": "अंतरराष्ट्रीय व्यापार, प्रकाशन रॉयल्टी और शिक्षा संबंधित निवेश ध्यान आकर्षित करते हैं। पिता या गुरु वित्तीय निर्णयों को प्रभावित कर सकते हैं। लंबी दूरी के वित्तीय लेनदेन में सावधानीपूर्वक दस्तावेज़ीकरण आवश्यक है।"},
            "health": {"en": "Hips, thighs, and liver areas need care during this transit. Overexertion during travel or sports affects the lower body. Moderate physical activity and adequate hydration support wellbeing.", "hi": "इस गोचर में कूल्हों, जांघों और यकृत क्षेत्र की देखभाल आवश्यक है। यात्रा या खेल में अत्यधिक परिश्रम निचले शरीर को प्रभावित करता है। संयमित शारीरिक गतिविधि और पर्याप्त जलयोजन स्वास्थ्य का समर्थन करते हैं।"},
        },
        10: {
            "general": {"en": "Mars in the 10th house supercharges career ambition and public action. You command attention in professional settings through decisive leadership. Government and authority dealings require courage and strategic timing.", "hi": "मंगल दसवें भाव में करियर की महत्वाकांक्षा और सार्वजनिक कार्रवाई को सुपरचार्ज करता है। निर्णायक नेतृत्व से आप पेशेवर सेटिंग में ध्यान आकर्षित करते हैं। सरकारी और अधिकारी व्यवहार में साहस और रणनीतिक समय की आवश्यकता है।"},
            "love": {"en": "Career demands may overshadow relationship time. Partner needs patience with your professional intensity. Public displays of commitment or relationship milestones are possible.", "hi": "करियर की मांगें रिश्ते के समय पर हावी हो सकती हैं। साथी को आपकी पेशेवर तीव्रता के साथ धैर्य की आवश्यकता है। प्रतिबद्धता या संबंध मील के पत्थर की सार्वजनिक अभिव्यक्ति संभव है।"},
            "career": {"en": "Peak period for career advancement and professional recognition. Executive decisions come naturally and results follow swiftly. Military, engineering, sports, and leadership positions are strongly favored.", "hi": "करियर उन्नति और पेशेवर मान्यता के लिए चरम अवधि। कार्यकारी निर्णय स्वाभाविक रूप से आते हैं और परिणाम तेजी से मिलते हैं। सैन्य, इंजीनियरिंग, खेल और नेतृत्व पद अत्यधिक अनुकूल हैं।"},
            "finance": {"en": "Professional income rises through ambitious projects and leadership bonuses. Government tenders or authority-approved ventures can be profitable. Invest earnings strategically rather than impulsively.", "hi": "महत्वाकांक्षी परियोजनाओं और नेतृत्व बोनस से पेशेवर आय बढ़ती है। सरकारी टेंडर या अधिकृत उद्यम लाभदायक हो सकते हैं। कमाई को आवेगपूर्वक नहीं बल्कि रणनीतिक रूप से निवेश करें।"},
            "health": {"en": "Knees, joints, and bones bear the stress of intense professional activity. Work-related burnout is the primary health risk. Schedule recovery time between high-performance periods.", "hi": "घुटने, जोड़ और हड्डियां तीव्र पेशेवर गतिविधि का तनाव सहती हैं। कार्य-संबंधित बर्नआउट प्राथमिक स्वास्थ्य जोखिम है। उच्च प्रदर्शन अवधि के बीच रिकवरी समय निर्धारित करें।"},
        },
        11: {
            "general": {"en": "Mars in the 11th house accelerates gains, social networking, and fulfillment of ambitious goals. Elder siblings or influential friends play a catalytic role. Group activities and team competitions bring excellent results.", "hi": "मंगल ग्यारहवें भाव में लाभ, सामाजिक नेटवर्किंग और महत्वाकांक्षी लक्ष्यों की पूर्ति को तेज करता है। बड़े भाई-बहन या प्रभावशाली मित्र उत्प्रेरक भूमिका निभाते हैं। सामूहिक गतिविधियां और टीम प्रतिस्पर्धाएं उत्कृष्ट परिणाम देती हैं।"},
            "love": {"en": "Social gatherings and group events create romantic opportunities. Friends may introduce potential partners. Shared activist causes or competitive team participation strengthens bonds.", "hi": "सामाजिक समारोह और सामूहिक आयोजन रोमांटिक अवसर बनाते हैं। मित्र संभावित साथी से परिचय करा सकते हैं। साझा सामाजिक कार्य या प्रतिस्पर्धी टीम भागीदारी बंधन मजबूत करती है।"},
            "career": {"en": "Networking aggressively opens doors to new professional opportunities. Team leadership and group project management suit your energy. Technology, engineering, and social enterprise ventures flourish.", "hi": "आक्रामक नेटवर्किंग नए पेशेवर अवसरों के द्वार खोलती है। टीम नेतृत्व और सामूहिक परियोजना प्रबंधन आपकी ऊर्जा के अनुकूल है। प्रौद्योगिकी, इंजीनियरिंग और सामाजिक उद्यम फलते-फूलते हैं।"},
            "finance": {"en": "Multiple income streams activate through networking and group ventures. Elder siblings or friends may facilitate profitable opportunities. Financial goals set during this period have high success probability.", "hi": "नेटवर्किंग और सामूहिक उद्यमों से कई आय धाराएं सक्रिय होती हैं। बड़े भाई-बहन या मित्र लाभदायक अवसर सुगम कर सकते हैं। इस अवधि में निर्धारित वित्तीय लक्ष्यों की सफलता संभावना उच्च है।"},
            "health": {"en": "Calves, ankles, and circulatory system benefit from active lifestyle but need protection during sports. Social commitments may lead to irregular schedules. Maintain consistent health routines despite busy social calendar.", "hi": "सक्रिय जीवनशैली से पिंडली, टखने और संचार प्रणाली लाभान्वित होती है लेकिन खेल में सुरक्षा आवश्यक है। सामाजिक प्रतिबद्धताएं अनियमित दिनचर्या का कारण बन सकती हैं। व्यस्त सामाजिक कार्यक्रम के बावजूद सुसंगत स्वास्थ्य दिनचर्या बनाए रखें।"},
        },
        12: {
            "general": {"en": "Mars in the 12th house channels energy toward spiritual pursuits, foreign matters, and behind-the-scenes action. Hidden enemies may become active requiring vigilance. Isolation or retreat periods prove surprisingly productive.", "hi": "मंगल बारहवें भाव में ऊर्जा को आध्यात्मिक गतिविधियों, विदेशी मामलों और पर्दे के पीछे की कार्रवाई की ओर प्रवाहित करता है। छिपे शत्रु सक्रिय हो सकते हैं जिसमें सतर्कता आवश्यक है। एकांत या वापसी की अवधि आश्चर्यजनक रूप से उत्पादक साबित होती है।"},
            "love": {"en": "Secret romantic feelings or hidden relationship dynamics surface. Emotional vulnerability can deepen intimacy if expressed safely. Foreign or long-distance connections carry strong karmic significance.", "hi": "गुप्त रोमांटिक भावनाएं या छिपी संबंध गतिशीलता सतह पर आती है। भावनात्मक कमजोरी सुरक्षित रूप से व्यक्त होने पर अंतरंगता गहरी कर सकती है। विदेशी या लंबी दूरी के संबंध मजबूत कार्मिक महत्व रखते हैं।"},
            "career": {"en": "Behind-the-scenes roles, foreign postings, and hospital or institutional work suit this transit. Undercover or confidential projects progress well. Public visibility decreases but foundational work advances.", "hi": "पर्दे के पीछे की भूमिकाएं, विदेशी पोस्टिंग और अस्पताल या संस्थागत कार्य इस गोचर के अनुकूल हैं। गोपनीय परियोजनाएं अच्छी तरह आगे बढ़ती हैं। सार्वजनिक दृश्यता कम होती है लेकिन मूलभूत कार्य आगे बढ़ता है।"},
            "finance": {"en": "Expenses on travel, hospitalization, spiritual retreats, or foreign investments increase. Hidden financial drains need identification and plugging. Charitable donations and spiritual expenditure bring inner satisfaction.", "hi": "यात्रा, अस्पताल, आध्यात्मिक एकांतवास या विदेशी निवेश पर खर्च बढ़ता है। छिपे वित्तीय नुकसान की पहचान और रोकथाम आवश्यक है। दान और आध्यात्मिक खर्च आंतरिक संतुष्टि लाते हैं।"},
            "health": {"en": "Feet, left eye, and sleep quality are vulnerable areas during this transit. Hidden health issues may surface requiring attention. Adequate rest, foot care, and stress management are essential priorities.", "hi": "इस गोचर में पैर, बाईं आंख और नींद की गुणवत्ता कमजोर क्षेत्र हैं। छिपी स्वास्थ्य समस्याएं सतह पर आ सकती हैं। पर्याप्त आराम, पैरों की देखभाल और तनाव प्रबंधन आवश्यक प्राथमिकताएं हैं।"},
        },
    },
    # =========================================================================
    # MERCURY (Budh) — Communication, business, intellect, skills, nervousness
    # Conditional benefic. Karaka of speech, trade, logic, learning.
    # =========================================================================
    "Mercury": {
        1: {
            "general": {"en": "Mercury transiting your 1st house sharpens intellect and communication skills. Quick thinking and articulate expression define your interactions. Learning new skills comes naturally during this period.", "hi": "बुध का प्रथम भाव में गोचर बुद्धि और संवाद कौशल को तेज करता है। तीव्र सोच और स्पष्ट अभिव्यक्ति आपके संवाद को परिभाषित करती है। इस अवधि में नए कौशल सीखना स्वाभाविक रूप से आता है।"},
            "love": {"en": "Witty and engaging conversations strengthen romantic connections. You express feelings through words and intellectual engagement. Communication-based bonding deepens relationships.", "hi": "चतुर और आकर्षक बातचीत रोमांटिक संबंधों को मजबूत करती है। आप भावनाओं को शब्दों और बौद्धिक जुड़ाव से व्यक्त करते हैं। संवाद-आधारित जुड़ाव रिश्तों को गहरा करता है।"},
            "career": {"en": "Writing, speaking, teaching, and analytical work excel. Job interviews and presentations go smoothly. Quick adaptation to new professional environments gives you competitive advantage.", "hi": "लेखन, भाषण, शिक्षण और विश्लेषणात्मक कार्य उत्कृष्ट होते हैं। नौकरी साक्षात्कार और प्रस्तुतियां सुचारू रूप से होती हैं। नए पेशेवर वातावरण में त्वरित अनुकूलन प्रतिस्पर्धात्मक लाभ देता है।"},
            "finance": {"en": "Business acumen sharpens and commercial transactions are favorable. Quick calculations and smart negotiations improve financial outcomes. Small trades and short-term investments show good returns.", "hi": "व्यापारिक कुशाग्रता तेज होती है और वाणिज्यिक लेनदेन अनुकूल होते हैं। त्वरित गणना और चतुर बातचीत वित्तीय परिणामों में सुधार करती है। छोटे व्यापार और अल्पकालिक निवेश अच्छे रिटर्न दिखाते हैं।"},
            "health": {"en": "Nervous system is highly active, requiring calming practices. Skin and respiratory health need attention. Overthinking and anxiety can be managed through meditation and regular breathing exercises.", "hi": "तंत्रिका तंत्र अत्यधिक सक्रिय है, शांत करने वाले अभ्यास आवश्यक हैं। त्वचा और श्वसन स्वास्थ्य पर ध्यान देने की आवश्यकता है। अत्यधिक सोच और चिंता को ध्यान और नियमित श्वास व्यायाम से प्रबंधित किया जा सकता है।"},
        },
        2: {
            "general": {"en": "Mercury in the 2nd house enhances speech eloquence and financial intelligence. Family communications improve and educational pursuits within family are supported. Your voice carries persuasive power.", "hi": "बुध दूसरे भाव में वाणी की वाक्पटुता और वित्तीय बुद्धिमत्ता बढ़ाता है। पारिवारिक संवाद सुधरता है और परिवार में शैक्षिक गतिविधियों को समर्थन मिलता है। आपकी आवाज में प्रभावशाली शक्ति होती है।"},
            "love": {"en": "Sweet words and thoughtful communication nurture family bonds. Love is expressed through practical care and intellectual sharing. Family approval of relationships comes through articulate expression.", "hi": "मधुर शब्द और विचारशील संवाद पारिवारिक बंधनों को पोषित करते हैं। प्रेम व्यावहारिक देखभाल और बौद्धिक साझेदारी से व्यक्त होता है। स्पष्ट अभिव्यक्ति से रिश्तों की पारिवारिक स्वीकृति मिलती है।"},
            "career": {"en": "Financial analysis, accounting, banking, and speech-related careers prosper. Teaching and counseling within educational institutions are favored. Documentation and record-keeping skills prove valuable.", "hi": "वित्तीय विश्लेषण, लेखांकन, बैंकिंग और वाणी-संबंधित करियर समृद्ध होते हैं। शैक्षणिक संस्थानों में शिक्षण और परामर्श अनुकूल है। दस्तावेज़ीकरण और रिकॉर्ड-कीपिंग कौशल मूल्यवान साबित होते हैं।"},
            "finance": {"en": "Excellent period for financial planning, budgeting, and commercial transactions. Multiple income sources through communication skills become available. Savings through intelligent spending decisions increase.", "hi": "वित्तीय योजना, बजट और वाणिज्यिक लेनदेन के लिए उत्कृष्ट अवधि। संवाद कौशल से आय के कई स्रोत उपलब्ध होते हैं। बुद्धिमान खर्च निर्णयों से बचत बढ़ती है।"},
            "health": {"en": "Throat, vocal cords, and oral health benefit from Mercury's positive influence here. Nervous eating habits may develop under stress. Mindful eating and vocal rest support overall wellbeing.", "hi": "बुध के यहां सकारात्मक प्रभाव से गला, स्वर तंत्र और मौखिक स्वास्थ्य लाभान्वित होता है। तनाव में नर्वस खाने की आदतें विकसित हो सकती हैं। सचेत आहार और स्वर विश्राम समग्र स्वास्थ्य का समर्थन करते हैं।"},
        },
        3: {
            "general": {"en": "Mercury in its natural 3rd house brings exceptional communication prowess. Writing, journalism, and media activities flourish brilliantly. Short travels for learning and networking are highly productive.", "hi": "बुध अपने स्वाभाविक तृतीय भाव में असाधारण संवाद कौशल लाता है। लेखन, पत्रकारिता और मीडिया गतिविधियां शानदार ढंग से फलती-फूलती हैं। सीखने और नेटवर्किंग के लिए छोटी यात्राएं अत्यधिक उत्पादक हैं।"},
            "love": {"en": "Intellectual compatibility drives romantic interest. Communication flows effortlessly with partners and potential matches. Sibling or neighbor connections may facilitate new romantic introductions.", "hi": "बौद्धिक अनुकूलता रोमांटिक रुचि को प्रेरित करती है। साथी और संभावित मिलानों के साथ संवाद सहज रूप से बहता है। भाई-बहन या पड़ोसी संबंध नए रोमांटिक परिचय सुगम कर सकते हैं।"},
            "career": {"en": "Media, marketing, sales, and digital communication careers peak. Multi-tasking ability reaches its maximum. Training programs and skill development workshops yield exceptional results.", "hi": "मीडिया, मार्केटिंग, बिक्री और डिजिटल संवाद करियर चरम पर हैं। बहु-कार्य क्षमता अधिकतम तक पहुंचती है। प्रशिक्षण कार्यक्रम और कौशल विकास कार्यशालाएं असाधारण परिणाम देती हैं।"},
            "finance": {"en": "Quick trades, commissions, and communication-based earnings multiply. Short-term investments in tech and media show promise. Sibling partnerships in business may be profitable.", "hi": "त्वरित व्यापार, कमीशन और संवाद-आधारित कमाई बहुगुणित होती है। टेक और मीडिया में अल्पकालिक निवेश आशाजनक हैं। भाई-बहनों के साथ व्यापारिक साझेदारी लाभदायक हो सकती है।"},
            "health": {"en": "Hands, nervous system, and respiratory health are in focus. Information overload may cause mental fatigue. Regular digital detox and breathing exercises restore nervous system balance.", "hi": "हाथ, तंत्रिका तंत्र और श्वसन स्वास्थ्य केंद्र में हैं। सूचना अधिभार मानसिक थकान का कारण बन सकता है। नियमित डिजिटल डिटॉक्स और श्वास व्यायाम तंत्रिका तंत्र का संतुलन बहाल करते हैं।"},
        },
        4: {
            "general": {"en": "Mercury in the 4th house stimulates intellectual activity at home and property-related planning. Academic pursuits in comfortable environments are productive. Family discussions lead to constructive decisions.", "hi": "बुध चौथे भाव में घर पर बौद्धिक गतिविधि और संपत्ति-संबंधित योजना को उत्तेजित करता है। आरामदायक वातावरण में शैक्षणिक गतिविधियां उत्पादक हैं। पारिवारिक चर्चा रचनात्मक निर्णयों की ओर ले जाती है।"},
            "love": {"en": "Emotional intelligence grows through family interactions. Home becomes a space for meaningful conversations with partners. Mother or family elders offer wise relationship advice.", "hi": "पारिवारिक संवाद से भावनात्मक बुद्धिमत्ता बढ़ती है। घर साथी के साथ सार्थक बातचीत का स्थान बनता है। माता या परिवार के बुजुर्ग बुद्धिमान संबंध सलाह देते हैं।"},
            "career": {"en": "Work-from-home productivity increases significantly. Real estate documentation and property analysis skills shine. Educational administration and home-based businesses prosper.", "hi": "घर से काम की उत्पादकता काफी बढ़ती है। अचल संपत्ति दस्तावेज़ीकरण और विश्लेषण कौशल चमकते हैं। शैक्षणिक प्रशासन और गृह-आधारित व्यवसाय समृद्ध होते हैं।"},
            "finance": {"en": "Property documentation, home office investments, and educational expenses are well-timed. Intellectual property creates value. Smart planning of household budget yields significant savings.", "hi": "संपत्ति दस्तावेज़ीकरण, गृह कार्यालय निवेश और शैक्षणिक खर्च सही समय पर हैं। बौद्धिक संपदा मूल्य बनाती है। घरेलू बजट की चतुर योजना महत्वपूर्ण बचत देती है।"},
            "health": {"en": "Mental peace at home directly supports physical health. Chest and lung health improve in well-ventilated environments. Intellectual overstimulation before sleep may cause insomnia.", "hi": "घर पर मानसिक शांति सीधे शारीरिक स्वास्थ्य का समर्थन करती है। अच्छी हवादार वातावरण में छाती और फेफड़ों का स्वास्थ्य सुधरता है। सोने से पहले बौद्धिक अत्यधिक उत्तेजना अनिद्रा का कारण बन सकती है।"},
        },
        5: {
            "general": {"en": "Mercury in the 5th house sparks creative intelligence and youthful thinking. Children's education and creative writing projects flourish. Intellectual games, puzzles, and strategic planning bring joy.", "hi": "बुध पांचवें भाव में रचनात्मक बुद्धिमत्ता और युवा सोच को प्रज्वलित करता है। बच्चों की शिक्षा और रचनात्मक लेखन परियोजनाएं फलती-फूलती हैं। बौद्धिक खेल, पहेलियां और रणनीतिक योजना आनंद लाती हैं।"},
            "love": {"en": "Romantic exchanges become witty and intellectually stimulating. Love letters, messages, and verbal expressions of affection are especially effective. Dating through educational or cultural events is favored.", "hi": "रोमांटिक आदान-प्रदान चतुर और बौद्धिक रूप से उत्तेजक हो जाते हैं। प्रेम पत्र, संदेश और स्नेह की मौखिक अभिव्यक्ति विशेष रूप से प्रभावी हैं। शैक्षणिक या सांस्कृतिक कार्यक्रमों के माध्यम से डेटिंग अनुकूल है।"},
            "career": {"en": "Creative writing, entertainment industry, education, and speculative analysis careers bloom. Teaching and mentoring bring deep satisfaction. Strategic presentation of ideas wins support.", "hi": "रचनात्मक लेखन, मनोरंजन उद्योग, शिक्षा और विश्लेषणात्मक करियर खिलते हैं। शिक्षण और मार्गदर्शन गहरी संतुष्टि लाते हैं। विचारों की रणनीतिक प्रस्तुति समर्थन जीतती है।"},
            "finance": {"en": "Speculative analysis skills improve investment decisions. Intellectual property and creative works generate income. Children's education expenses need planning but are worthwhile investments.", "hi": "सट्टा विश्लेषण कौशल निवेश निर्णयों में सुधार करते हैं। बौद्धिक संपदा और रचनात्मक कार्य आय उत्पन्न करते हैं। बच्चों के शिक्षा खर्च की योजना आवश्यक है लेकिन ये सार्थक निवेश हैं।"},
            "health": {"en": "Nervous energy from creative excitement needs grounding. Stomach and digestive system respond to mental state. Playful physical activities balance intellectual intensity.", "hi": "रचनात्मक उत्साह से तंत्रिका ऊर्जा को ग्राउंडिंग की आवश्यकता है। पेट और पाचन तंत्र मानसिक स्थिति पर प्रतिक्रिया करता है। चंचल शारीरिक गतिविधियां बौद्धिक तीव्रता को संतुलित करती हैं।"},
        },
        6: {
            "general": {"en": "Mercury in the 6th house gives analytical power to solve problems and overcome obstacles. Detailed work, debugging, and troubleshooting excel. Health management through knowledge and research is effective.", "hi": "बुध छठे भाव में समस्याओं को हल करने और बाधाओं पर विजय पाने की विश्लेषणात्मक शक्ति देता है। विस्तृत कार्य, डिबगिंग और समस्या निवारण उत्कृष्ट होते हैं। ज्ञान और अनुसंधान के माध्यम से स्वास्थ्य प्रबंधन प्रभावी है।"},
            "love": {"en": "Practical problem-solving strengthens relationships. Analyzing and addressing relationship issues rationally brings clarity. Service to partner through daily acts of care builds trust.", "hi": "व्यावहारिक समस्या-समाधान संबंधों को मजबूत करता है। संबंध समस्याओं का तर्कसंगत विश्लेषण और समाधान स्पष्टता लाता है। दैनिक देखभाल के कार्यों से साथी की सेवा विश्वास बनाती है।"},
            "career": {"en": "Data analysis, healthcare administration, accounting, and quality assurance roles shine. Problem-solving skills earn recognition from superiors. Legal documentation and dispute resolution work is favored.", "hi": "डेटा विश्लेषण, स्वास्थ्य सेवा प्रशासन, लेखांकन और गुणवत्ता आश्वासन भूमिकाएं चमकती हैं। समस्या-समाधान कौशल वरिष्ठों से मान्यता दिलाता है। कानूनी दस्तावेज़ीकरण और विवाद समाधान कार्य अनुकूल है।"},
            "finance": {"en": "Debt management and expense tracking become more efficient. Healthcare costs may arise but are manageable with planning. Income through analytical and service-based work increases steadily.", "hi": "ऋण प्रबंधन और खर्च ट्रैकिंग अधिक कुशल हो जाती है। स्वास्थ्य सेवा लागत उत्पन्न हो सकती है लेकिन योजना से प्रबंधनीय है। विश्लेषणात्मक और सेवा-आधारित कार्य से आय लगातार बढ़ती है।"},
            "health": {"en": "Excellent awareness of health issues leads to effective preventive care. Digestive and intestinal health improves through dietary intelligence. Mental stress from overwork needs conscious management.", "hi": "स्वास्थ्य समस्याओं की उत्कृष्ट जागरूकता प्रभावी निवारक देखभाल की ओर ले जाती है। आहार बुद्धिमत्ता से पाचन और आंतों का स्वास्थ्य सुधरता है। अत्यधिक कार्य से मानसिक तनाव के सचेत प्रबंधन की आवश्यकता है।"},
        },
        7: {
            "general": {"en": "Mercury in the 7th house enhances partnership communication and business negotiations. Contracts and agreements benefit from your sharp analytical eye. Public dealings require diplomatic and articulate expression.", "hi": "बुध सातवें भाव में साझेदारी संवाद और व्यापारिक बातचीत को बढ़ाता है। आपकी तीक्ष्ण विश्लेषणात्मक दृष्टि से अनुबंध और समझौते लाभान्वित होते हैं। सार्वजनिक व्यवहार में कूटनीतिक और स्पष्ट अभिव्यक्ति आवश्यक है।"},
            "love": {"en": "Intellectual compatibility becomes central to relationship satisfaction. Meaningful dialogues resolve long-standing misunderstandings. Partners who stimulate your mind attract you most.", "hi": "बौद्धिक अनुकूलता संबंध संतुष्टि का केंद्र बन जाती है। सार्थक संवाद पुरानी गलतफहमियों को हल करते हैं। जो साथी आपके मस्तिष्क को उत्तेजित करते हैं वे सबसे अधिक आकर्षित करते हैं।"},
            "career": {"en": "Contract negotiations, legal consultations, and client communications excel. Partnership-based business ventures are intellectually stimulating. Mediation and counseling roles suit your current energy.", "hi": "अनुबंध वार्ता, कानूनी परामर्श और ग्राहक संवाद उत्कृष्ट होते हैं। साझेदारी-आधारित व्यापारिक उद्यम बौद्धिक रूप से उत्तेजक हैं। मध्यस्थता और परामर्श भूमिकाएं आपकी वर्तमान ऊर्जा के अनुकूल हैं।"},
            "finance": {"en": "Business partnerships and joint ventures benefit from clear documentation. Legal settlements and contract terms work in your favor. Spouse or partner brings valuable financial insights.", "hi": "स्पष्ट दस्तावेज़ीकरण से व्यापारिक साझेदारी और संयुक्त उद्यम लाभान्वित होते हैं। कानूनी समझौते और अनुबंध शर्तें आपके पक्ष में काम करती हैं। पति/पत्नी या साथी मूल्यवान वित्तीय अंतर्दृष्टि लाते हैं।"},
            "health": {"en": "Kidney and lower back areas benefit from adequate hydration. Partner's health awareness positively influences your habits. Balanced social life supports mental and physical equilibrium.", "hi": "पर्याप्त जलयोजन से गुर्दे और पीठ के निचले हिस्से लाभान्वित होते हैं। साथी की स्वास्थ्य जागरूकता आपकी आदतों को सकारात्मक रूप से प्रभावित करती है। संतुलित सामाजिक जीवन मानसिक और शारीरिक संतुलन का समर्थन करता है।"},
        },
        8: {
            "general": {"en": "Mercury in the 8th house deepens research abilities and occult interest. Hidden information becomes accessible through intellectual investigation. Transformation through knowledge and understanding of mysteries is indicated.", "hi": "बुध आठवें भाव में अनुसंधान क्षमता और गूढ़ रुचि को गहरा करता है। बौद्धिक जांच से छिपी जानकारी सुलभ हो जाती है। ज्ञान और रहस्यों की समझ के माध्यम से परिवर्तन संकेतित है।"},
            "love": {"en": "Deep psychological understanding of partners transforms relationships. Secrets shared in trust build profound intimacy. Communication about fears and vulnerabilities creates healing bonds.", "hi": "साथियों की गहरी मनोवैज्ञानिक समझ संबंधों को बदलती है। विश्वास में साझा किए गए रहस्य गहन अंतरंगता बनाते हैं। भय और कमजोरियों के बारे में संवाद उपचारात्मक बंधन बनाता है।"},
            "career": {"en": "Research, forensics, insurance analysis, and investigation roles excel. Coding, cryptography, and data security fields attract your intellect. Uncovering hidden patterns gives professional edge.", "hi": "अनुसंधान, फोरेंसिक, बीमा विश्लेषण और जांच भूमिकाएं उत्कृष्ट होती हैं। कोडिंग, क्रिप्टोग्राफी और डेटा सुरक्षा क्षेत्र आपकी बुद्धि को आकर्षित करते हैं। छिपे पैटर्न उजागर करना पेशेवर बढ़त देता है।"},
            "finance": {"en": "Insurance, tax planning, and inheritance documentation benefit from careful analysis. Hidden financial opportunities reveal themselves through research. Joint account management requires transparent communication.", "hi": "बीमा, कर योजना और विरासत दस्तावेज़ीकरण सावधानीपूर्वक विश्लेषण से लाभान्वित होते हैं। अनुसंधान से छिपे वित्तीय अवसर प्रकट होते हैं। संयुक्त खाता प्रबंधन में पारदर्शी संवाद आवश्यक है।"},
            "health": {"en": "Nervous system sensitivity increases around hidden health concerns. Research into health conditions leads to better treatment choices. Reproductive health benefits from informed awareness.", "hi": "छिपी स्वास्थ्य चिंताओं के आसपास तंत्रिका तंत्र संवेदनशीलता बढ़ती है। स्वास्थ्य स्थितियों में अनुसंधान बेहतर उपचार विकल्पों की ओर ले जाता है। जानकारीपूर्ण जागरूकता से प्रजनन स्वास्थ्य लाभान्वित होता है।"},
        },
        9: {
            "general": {"en": "Mercury in the 9th house expands intellectual horizons through higher learning and philosophy. Foreign languages, cultures, and academic publishing attract your curious mind. Guru-disciple connections form through intellectual exchange.", "hi": "बुध नौवें भाव में उच्च शिक्षा और दर्शन के माध्यम से बौद्धिक क्षितिज का विस्तार करता है। विदेशी भाषाएं, संस्कृतियां और शैक्षणिक प्रकाशन आपके जिज्ञासु मन को आकर्षित करते हैं। बौद्धिक आदान-प्रदान से गुरु-शिष्य संबंध बनते हैं।"},
            "love": {"en": "Philosophical and intellectual depth enriches romantic conversations. Long-distance communication with lovers flows naturally. Cultural and educational activities make excellent date settings.", "hi": "दार्शनिक और बौद्धिक गहराई रोमांटिक बातचीत को समृद्ध करती है। प्रेमियों के साथ लंबी दूरी का संवाद स्वाभाविक रूप से बहता है। सांस्कृतिक और शैक्षणिक गतिविधियां उत्कृष्ट डेट सेटिंग बनाती हैं।"},
            "career": {"en": "Academic research, publishing, international consulting, and legal careers soar. Language skills open international doors. Higher certifications and advanced degrees enhance career trajectory.", "hi": "शैक्षणिक अनुसंधान, प्रकाशन, अंतरराष्ट्रीय परामर्श और कानूनी करियर ऊंचाई पर हैं। भाषा कौशल अंतरराष्ट्रीय द्वार खोलते हैं। उच्च प्रमाणपत्र और उन्नत डिग्री करियर प्रक्षेपवक्र को बढ़ाती हैं।"},
            "finance": {"en": "International transactions and export-import businesses benefit from sharp negotiation. Royalties from publications and teaching fees supplement income. Father or mentor may influence positive financial decisions.", "hi": "तीक्ष्ण बातचीत से अंतरराष्ट्रीय लेनदेन और निर्यात-आयात व्यवसाय लाभान्वित होते हैं। प्रकाशन रॉयल्टी और शिक्षण शुल्क आय का पूरक हैं। पिता या गुरु सकारात्मक वित्तीय निर्णयों को प्रभावित कर सकते हैं।"},
            "health": {"en": "Travel-related stress on nerves and hips needs attention. Higher study pressure may cause eye strain and headaches. Balance intellectual pursuit with physical movement for overall wellness.", "hi": "यात्रा-संबंधित नसों और कूल्हों पर तनाव पर ध्यान देने की आवश्यकता है। उच्च अध्ययन दबाव आंखों में तनाव और सिरदर्द का कारण बन सकता है। समग्र स्वास्थ्य के लिए बौद्धिक गतिविधि को शारीरिक गतिविधि से संतुलित करें।"},
        },
        10: {
            "general": {"en": "Mercury in the 10th house brings intellectual authority and communication-driven career success. Public speaking and professional writing gain wide recognition. Government and administrative communications are handled with skill.", "hi": "बुध दसवें भाव में बौद्धिक अधिकार और संवाद-संचालित करियर सफलता लाता है। सार्वजनिक भाषण और पेशेवर लेखन व्यापक मान्यता प्राप्त करते हैं। सरकारी और प्रशासनिक संवाद कुशलता से संभाले जाते हैं।"},
            "love": {"en": "Professional success makes you more attractive in romantic settings. Workplace connections may spark romantic interest. Maintaining work-life balance requires conscious communication with partners.", "hi": "पेशेवर सफलता रोमांटिक सेटिंग में आपको अधिक आकर्षक बनाती है। कार्यस्थल कनेक्शन रोमांटिक रुचि जगा सकते हैं। कार्य-जीवन संतुलन बनाए रखने के लिए साथी के साथ सचेत संवाद आवश्यक है।"},
            "career": {"en": "Peak period for professional communications, presentations, and strategic planning. IT, media, consulting, and advisory roles bring maximum satisfaction. Reputation as an expert grows through published work.", "hi": "पेशेवर संवाद, प्रस्तुतियों और रणनीतिक योजना के लिए चरम अवधि। आईटी, मीडिया, परामर्श और सलाहकार भूमिकाएं अधिकतम संतुष्टि लाती हैं। प्रकाशित कार्य से विशेषज्ञ के रूप में प्रतिष्ठा बढ़ती है।"},
            "finance": {"en": "Professional fees, consulting income, and intellectual property generate strong earnings. Government contracts and official documentation work yields good returns. Strategic career moves directly improve financial standing.", "hi": "पेशेवर शुल्क, परामर्श आय और बौद्धिक संपदा मजबूत कमाई उत्पन्न करती है। सरकारी अनुबंध और आधिकारिक दस्तावेज़ीकरण कार्य अच्छे रिटर्न देता है। रणनीतिक करियर कदम सीधे वित्तीय स्थिति में सुधार करते हैं।"},
            "health": {"en": "Knee and joint areas reflect professional stress accumulation. Carpal tunnel and screen fatigue are occupational risks. Ergonomic workspace and regular stretching breaks prevent chronic issues.", "hi": "घुटने और जोड़ क्षेत्र पेशेवर तनाव संचय को दर्शाते हैं। कार्पल टनल और स्क्रीन थकान व्यावसायिक जोखिम हैं। एर्गोनोमिक कार्यस्थल और नियमित स्ट्रेचिंग ब्रेक पुरानी समस्याओं को रोकते हैं।"},
        },
        11: {
            "general": {"en": "Mercury in the 11th house amplifies social networking and achievement of intellectual goals. Online communities and professional networks expand rapidly. Friend circles bring valuable information and opportunities.", "hi": "बुध ग्यारहवें भाव में सामाजिक नेटवर्किंग और बौद्धिक लक्ष्यों की प्राप्ति को बढ़ाता है। ऑनलाइन समुदाय और पेशेवर नेटवर्क तेजी से विस्तारित होते हैं। मित्र मंडली मूल्यवान जानकारी और अवसर लाती है।"},
            "love": {"en": "Friendship-based romantic connections flourish naturally. Group social settings facilitate meeting compatible people. Online dating and social media romantic interactions are favored.", "hi": "मित्रता-आधारित रोमांटिक संबंध स्वाभाविक रूप से फलते-फूलते हैं। सामूहिक सामाजिक सेटिंग अनुकूल लोगों से मिलने में सहायक होती है। ऑनलाइन डेटिंग और सोशल मीडिया रोमांटिक इंटरैक्शन अनुकूल हैं।"},
            "career": {"en": "Technology, social media management, and network-driven careers peak. Group projects and team collaborations yield outstanding outcomes. Professional associations and memberships prove strategically valuable.", "hi": "प्रौद्योगिकी, सोशल मीडिया प्रबंधन और नेटवर्क-संचालित करियर चरम पर हैं। सामूहिक परियोजनाएं और टीम सहयोग उत्कृष्ट परिणाम देते हैं। पेशेवर संघ और सदस्यताएं रणनीतिक रूप से मूल्यवान साबित होती हैं।"},
            "finance": {"en": "Multiple income channels through networks and digital platforms activate. Friends share profitable business intelligence. Crowdfunding and community-based financial initiatives succeed.", "hi": "नेटवर्क और डिजिटल प्लेटफॉर्म के माध्यम से कई आय चैनल सक्रिय होते हैं। मित्र लाभदायक व्यापारिक जानकारी साझा करते हैं। क्राउडफंडिंग और समुदाय-आधारित वित्तीय पहल सफल होती हैं।"},
            "health": {"en": "Nervous system overload from excessive social and digital engagement is likely. Calves and circulation benefit from walking meetings. Balance screen time with outdoor activities for sustained energy.", "hi": "अत्यधिक सामाजिक और डिजिटल जुड़ाव से तंत्रिका तंत्र ओवरलोड की संभावना है। वॉकिंग मीटिंग से पिंडली और रक्त संचार लाभान्वित होता है। निरंतर ऊर्जा के लिए स्क्रीन समय को बाहरी गतिविधियों से संतुलित करें।"},
        },
        12: {
            "general": {"en": "Mercury in the 12th house turns the mind inward toward contemplation, dreams, and spiritual study. Foreign communications and behind-the-scenes intellectual work thrive. Intuitive insights arise through quiet reflection.", "hi": "बुध बारहवें भाव में मन को चिंतन, स्वप्न और आध्यात्मिक अध्ययन की ओर मोड़ता है। विदेशी संवाद और पर्दे के पीछे का बौद्धिक कार्य फलता-फूलता है। शांत चिंतन से अंतर्ज्ञान अंतर्दृष्टि उत्पन्न होती है।"},
            "love": {"en": "Unspoken emotional understanding deepens romantic bonds. Secret admirers or private romantic communications emerge. Spiritual connection with partners transcends verbal expression.", "hi": "अनकही भावनात्मक समझ रोमांटिक बंधन गहरे करती है। गुप्त प्रशंसक या निजी रोमांटिक संवाद उभरते हैं। साथियों के साथ आध्यात्मिक संबंध शाब्दिक अभिव्यक्ति से परे जाता है।"},
            "career": {"en": "Research in isolation, foreign correspondence, and creative writing in solitude produce excellent work. Healthcare documentation and institutional administration roles suit this energy. Working for NGOs or spiritual organizations is fulfilling.", "hi": "एकांत में अनुसंधान, विदेशी पत्राचार और एकांत में रचनात्मक लेखन उत्कृष्ट कार्य उत्पन्न करते हैं। स्वास्थ्य सेवा दस्तावेज़ीकरण और संस्थागत प्रशासन भूमिकाएं इस ऊर्जा के अनुकूल हैं। एनजीओ या आध्यात्मिक संगठनों के लिए कार्य संतोषजनक है।"},
            "finance": {"en": "Expenses on spiritual books, meditation retreats, and foreign travel may increase. Hidden savings or forgotten financial assets may be recovered. Charitable giving brings karmic returns.", "hi": "आध्यात्मिक पुस्तकों, ध्यान एकांतवास और विदेशी यात्रा पर खर्च बढ़ सकता है। छिपी बचत या भूली हुई वित्तीय संपत्ति वसूल हो सकती है। दान कार्मिक प्रतिफल लाता है।"},
            "health": {"en": "Sleep patterns and dream quality reflect mental state. Feet and immune system need gentle care. Meditation and journaling significantly improve psychological wellbeing during this transit.", "hi": "नींद पैटर्न और स्वप्न गुणवत्ता मानसिक स्थिति को दर्शाते हैं। पैर और प्रतिरक्षा प्रणाली को कोमल देखभाल की आवश्यकता है। इस गोचर में ध्यान और जर्नलिंग मनोवैज्ञानिक स्वास्थ्य में काफी सुधार करते हैं।"},
        },
    },
    # =========================================================================
    # JUPITER (Guru/Brihaspati) — Wisdom, expansion, children, wealth, dharma
    # Great benefic. Karaka of knowledge, fortune, progeny, dharma.
    # =========================================================================
    "Jupiter": {
        1: {
            "general": {"en": "Jupiter transiting your 1st house brings expansion, optimism, and personal growth. Wisdom and generosity define your personality during this blessed period. New opportunities arrive through your magnetic presence.", "hi": "गुरु का प्रथम भाव में गोचर विस्तार, आशावाद और व्यक्तिगत विकास लाता है। इस शुभ अवधि में ज्ञान और उदारता आपके व्यक्तित्व को परिभाषित करती है। आपकी चुंबकीय उपस्थिति से नए अवसर आते हैं।"},
            "love": {"en": "Relationships blossom with warmth, generosity, and mutual growth. Your expanded outlook attracts compatible partners naturally. Marriage prospects are highly favorable during this transit.", "hi": "संबंध गर्मजोशी, उदारता और पारस्परिक विकास से खिलते हैं। आपका विस्तारित दृष्टिकोण स्वाभाविक रूप से अनुकूल साथियों को आकर्षित करता है। इस गोचर में विवाह की संभावनाएं अत्यधिक अनुकूल हैं।"},
            "career": {"en": "Professional expansion, promotions, and recognition come naturally. Teaching, consulting, and advisory roles bring deep satisfaction. Your reputation grows and doors open in new directions.", "hi": "पेशेवर विस्तार, पदोन्नति और मान्यता स्वाभाविक रूप से आती है। शिक्षण, परामर्श और सलाहकार भूमिकाएं गहरी संतुष्टि लाती हैं। आपकी प्रतिष्ठा बढ़ती है और नई दिशाओं में द्वार खुलते हैं।"},
            "finance": {"en": "Financial abundance flows through multiple channels. Wise investments and generous yet balanced spending characterize this period. Wealth grows through ethical and dharmic means.", "hi": "कई माध्यमों से वित्तीय प्रचुरता प्रवाहित होती है। बुद्धिमान निवेश और उदार लेकिन संतुलित खर्च इस अवधि की विशेषता है। नैतिक और धार्मिक साधनों से धन बढ़ता है।"},
            "health": {"en": "Overall vitality and immunity strengthen considerably. Weight gain from overindulgence is the primary health risk. Liver health benefits from moderation in rich foods and alcohol.", "hi": "समग्र जीवन शक्ति और प्रतिरक्षा काफी मजबूत होती है। अत्यधिक भोग से वजन बढ़ना प्राथमिक स्वास्थ्य जोखिम है। समृद्ध भोजन और शराब में संयम से यकृत स्वास्थ्य लाभान्वित होता है।"},
        },
        2: {
            "general": {"en": "Jupiter in the 2nd house blesses wealth, family harmony, and eloquent speech. Knowledge-based income and teaching opportunities multiply. Family traditions and values strengthen under this benevolent influence.", "hi": "गुरु दूसरे भाव में धन, पारिवारिक सद्भाव और वाक्पटु वाणी का आशीर्वाद देता है। ज्ञान-आधारित आय और शिक्षण अवसर बहुगुणित होते हैं। इस कृपालु प्रभाव में पारिवारिक परंपराएं और मूल्य मजबूत होते हैं।"},
            "love": {"en": "Family bonds strengthen and domestic harmony prevails. Married life enjoys abundance and mutual respect. Family blessings support romantic relationships and matrimonial prospects.", "hi": "पारिवारिक बंधन मजबूत होते हैं और घरेलू सद्भाव कायम रहता है। वैवाहिक जीवन प्रचुरता और पारस्परिक सम्मान का आनंद लेता है। पारिवारिक आशीर्वाद रोमांटिक संबंधों और वैवाहिक संभावनाओं का समर्थन करता है।"},
            "career": {"en": "Banking, finance, education, and food-related industries prosper. Public speaking and advisory roles elevate your professional standing. Knowledge monetization becomes a viable career path.", "hi": "बैंकिंग, वित्त, शिक्षा और खाद्य-संबंधित उद्योग समृद्ध होते हैं। सार्वजनिक भाषण और सलाहकार भूमिकाएं आपकी पेशेवर स्थिति को ऊपर उठाती हैं। ज्ञान मुद्रीकरण एक व्यवहार्य करियर मार्ग बनता है।"},
            "finance": {"en": "Wealth accumulation reaches its peak during this favorable transit. Savings, investments, and family assets grow steadily. Generous charity and dharmic spending attract more abundance.", "hi": "इस अनुकूल गोचर में धन संचय अपने चरम पर पहुंचता है। बचत, निवेश और पारिवारिक संपत्ति लगातार बढ़ती है। उदार दान और धार्मिक खर्च अधिक प्रचुरता को आकर्षित करता है।"},
            "health": {"en": "Face, eyes, and throat areas benefit from Jupiter's protective influence. Overindulgence in rich food may cause weight and sugar issues. Balanced diet with traditional foods supports optimal health.", "hi": "गुरु के सुरक्षात्मक प्रभाव से चेहरा, आंखें और गला लाभान्वित होते हैं। समृद्ध भोजन में अत्यधिक भोग वजन और शर्करा समस्याएं पैदा कर सकता है। पारंपरिक भोजन के साथ संतुलित आहार इष्टतम स्वास्थ्य का समर्थन करता है।"},
        },
        3: {
            "general": {"en": "Jupiter in the 3rd house expands communication abilities and adventurous spirit. Spiritual short journeys and learning pilgrimages are indicated. Sibling relationships improve through wisdom and generosity.", "hi": "गुरु तीसरे भाव में संवाद क्षमता और साहसिक भावना का विस्तार करता है। आध्यात्मिक छोटी यात्राएं और शिक्षण तीर्थयात्राएं संकेतित हैं। ज्ञान और उदारता से भाई-बहन संबंध सुधरते हैं।"},
            "love": {"en": "Philosophical conversations deepen romantic connections. Short romantic trips and cultural outings bring joy. Sibling support for your love life proves beneficial.", "hi": "दार्शनिक बातचीत रोमांटिक संबंधों को गहरा करती है। छोटी रोमांटिक यात्राएं और सांस्कृतिक सैर आनंद लाती हैं। आपके प्रेम जीवन के लिए भाई-बहनों का समर्थन लाभदायक साबित होता है।"},
            "career": {"en": "Publishing, journalism, media, and education careers expand. Training others becomes a source of professional growth. Courage to communicate bold ideas opens new professional paths.", "hi": "प्रकाशन, पत्रकारिता, मीडिया और शिक्षा करियर विस्तारित होते हैं। दूसरों को प्रशिक्षित करना पेशेवर विकास का स्रोत बनता है। साहसी विचारों को संप्रेषित करने का साहस नए पेशेवर मार्ग खोलता है।"},
            "finance": {"en": "Income through writing, publishing, and short-term business trips increases. Sibling financial support or joint ventures prove lucky. Small investments made with wisdom yield good returns.", "hi": "लेखन, प्रकाशन और अल्पकालिक व्यापार यात्राओं से आय बढ़ती है। भाई-बहनों का वित्तीय सहयोग या संयुक्त उद्यम शुभ साबित होते हैं। बुद्धिमत्ता से किए गए छोटे निवेश अच्छे रिटर्न देते हैं।"},
            "health": {"en": "Arms, shoulders, and respiratory system benefit from Jupiter's expansive energy. Overeating during social gatherings is the main concern. Light exercise and pranayama maintain respiratory and digestive health.", "hi": "गुरु की विस्तारक ऊर्जा से बाहें, कंधे और श्वसन तंत्र लाभान्वित होते हैं। सामाजिक समारोहों में अत्यधिक भोजन मुख्य चिंता है। हल्का व्यायाम और प्राणायाम श्वसन और पाचन स्वास्थ्य बनाए रखते हैं।"},
        },
        4: {
            "general": {"en": "Jupiter in the 4th house blesses home life with prosperity and peace. Property acquisitions and vehicle purchases are well-timed. Mother's blessings and family support create a strong foundation for all endeavors.", "hi": "गुरु चौथे भाव में गृह जीवन को समृद्धि और शांति का आशीर्वाद देता है। संपत्ति अधिग्रहण और वाहन खरीद का समय अनुकूल है। माता का आशीर्वाद और पारिवारिक सहायता सभी प्रयासों की मजबूत नींव बनाती है।"},
            "love": {"en": "Domestic bliss and emotional security define relationships. Home becomes a sanctuary of love and warmth. Family approval and blessings for relationships come naturally.", "hi": "घरेलू आनंद और भावनात्मक सुरक्षा संबंधों को परिभाषित करती है। घर प्रेम और गर्मजोशी का अभयारण्य बनता है। रिश्तों के लिए पारिवारिक अनुमोदन और आशीर्वाद स्वाभाविक रूप से आते हैं।"},
            "career": {"en": "Real estate, education, agriculture, and home-based professions flourish. Academic institutions and spiritual organizations offer opportunities. Career stability and inner satisfaction improve simultaneously.", "hi": "अचल संपत्ति, शिक्षा, कृषि और गृह-आधारित व्यवसाय फलते-फूलते हैं। शैक्षणिक संस्थान और आध्यात्मिक संगठन अवसर प्रदान करते हैं। करियर स्थिरता और आंतरिक संतुष्टि एक साथ सुधरती है।"},
            "finance": {"en": "Property values appreciate and real estate investments yield returns. Home renovation and family-related investments are well-timed. Ancestral wealth or family inheritance may become accessible.", "hi": "संपत्ति मूल्य बढ़ते हैं और अचल संपत्ति निवेश रिटर्न देते हैं। गृह नवीकरण और परिवार-संबंधित निवेश सही समय पर हैं। पैतृक संपत्ति या पारिवारिक विरासत सुलभ हो सकती है।"},
            "health": {"en": "Emotional wellbeing and mental peace improve dramatically. Chest and heart areas are protected by Jupiter's benevolent influence. Comfort-based lifestyle may lead to weight gain requiring mindful choices.", "hi": "भावनात्मक कल्याण और मानसिक शांति नाटकीय रूप से सुधरती है। गुरु के कृपालु प्रभाव से छाती और हृदय क्षेत्र सुरक्षित हैं। आराम-आधारित जीवनशैली वजन बढ़ा सकती है जिसमें सचेत विकल्प आवश्यक हैं।"},
        },
        5: {
            "general": {"en": "Jupiter in the 5th house brings immense blessings for creativity, romance, and children. Intellectual achievements and creative breakthroughs are highly probable. Past-life merit manifests as present-day good fortune.", "hi": "गुरु पांचवें भाव में रचनात्मकता, रोमांस और संतान के लिए अपार आशीर्वाद लाता है। बौद्धिक उपलब्धियां और रचनात्मक सफलता अत्यधिक संभावित हैं। पूर्व जन्म के पुण्य वर्तमान सौभाग्य के रूप में प्रकट होते हैं।"},
            "love": {"en": "Romance flourishes beautifully with deep emotional and spiritual connection. Childbirth or conception is highly favored. Existing relationships reach new heights of joy and understanding.", "hi": "गहरे भावनात्मक और आध्यात्मिक जुड़ाव के साथ रोमांस सुंदर रूप से फलता-फूलता है। संतान जन्म या गर्भधारण अत्यधिक अनुकूल है। मौजूदा संबंध आनंद और समझ की नई ऊंचाइयों तक पहुंचते हैं।"},
            "career": {"en": "Creative fields, education, speculation, and entertainment industries offer tremendous opportunities. Mentoring and teaching bring professional fulfillment. Strategic gambles in career pay off handsomely.", "hi": "रचनात्मक क्षेत्र, शिक्षा, सट्टा और मनोरंजन उद्योग जबरदस्त अवसर प्रदान करते हैं। मार्गदर्शन और शिक्षण पेशेवर पूर्णता लाते हैं। करियर में रणनीतिक जोखिम अच्छा भुगतान करते हैं।"},
            "finance": {"en": "Speculative investments under Jupiter's grace tend to be profitable. Children-related expenses are joyful investments in the future. Lottery, competition wins, and unexpected windfalls are possible.", "hi": "गुरु की कृपा में सट्टा निवेश लाभदायक होते हैं। संतान संबंधित खर्च भविष्य में आनंदमय निवेश हैं। लॉटरी, प्रतियोगिता जीत और अप्रत्याशित लाभ संभव हैं।"},
            "health": {"en": "Overall vitality and immunity are strong under this blessed transit. Upper abdomen and liver need moderation in rich food and sweets. Creative activities and joyful pursuits boost mental and physical health.", "hi": "इस शुभ गोचर में समग्र जीवन शक्ति और प्रतिरक्षा मजबूत है। ऊपरी पेट और यकृत को समृद्ध भोजन और मिठाइयों में संयम की आवश्यकता है। रचनात्मक गतिविधियां और आनंदमय गतिविधियां मानसिक और शारीरिक स्वास्थ्य को बढ़ावा देती हैं।"},
        },
        6: {
            "general": {"en": "Jupiter in the 6th house helps overcome enemies, diseases, and debts through wisdom. Service-oriented work brings spiritual growth. Legal victories and debt resolution are favored but require effort.", "hi": "गुरु छठे भाव में ज्ञान से शत्रुओं, रोगों और ऋणों पर विजय में सहायता करता है। सेवा-उन्मुख कार्य आध्यात्मिक विकास लाता है। कानूनी विजय और ऋण समाधान अनुकूल हैं लेकिन प्रयास आवश्यक है।"},
            "love": {"en": "Selfless service to partner strengthens the relationship foundation. Health challenges of loved ones bring couples closer through caregiving. Practical support matters more than romantic gestures now.", "hi": "साथी की निस्वार्थ सेवा संबंध की नींव मजबूत करती है। प्रियजनों की स्वास्थ्य चुनौतियां देखभाल के माध्यम से जोड़ों को करीब लाती हैं। अभी रोमांटिक भावों से अधिक व्यावहारिक सहायता मायने रखती है।"},
            "career": {"en": "Healthcare, legal, social service, and charitable organization careers thrive. Competitive examinations yield favorable results. Problem-solving abilities earn respect from colleagues and superiors.", "hi": "स्वास्थ्य सेवा, कानूनी, सामाजिक सेवा और धर्मार्थ संगठन करियर फलते-फूलते हैं। प्रतियोगी परीक्षाएं अनुकूल परिणाम देती हैं। समस्या-समाधान क्षमता सहकर्मियों और वरिष्ठों से सम्मान अर्जित करती है।"},
            "finance": {"en": "Debts reduce through systematic repayment plans. Healthcare expenses are manageable with insurance. Income through service and advisory roles remains steady and reliable.", "hi": "व्यवस्थित पुनर्भुगतान योजनाओं से ऋण कम होते हैं। बीमा से स्वास्थ्य सेवा खर्च प्रबंधनीय हैं। सेवा और सलाहकार भूमिकाओं से आय स्थिर और विश्वसनीय रहती है।"},
            "health": {"en": "Jupiter's protective influence helps overcome chronic health challenges. Digestive and immune system function improves through holistic approaches. Ayurvedic and traditional remedies prove especially effective.", "hi": "गुरु का सुरक्षात्मक प्रभाव पुरानी स्वास्थ्य चुनौतियों को दूर करने में मदद करता है। समग्र दृष्टिकोण से पाचन और प्रतिरक्षा तंत्र कार्य में सुधार होता है। आयुर्वेदिक और पारंपरिक उपचार विशेष रूप से प्रभावी साबित होते हैं।"},
        },
        7: {
            "general": {"en": "Jupiter in the 7th house brings auspicious developments in marriage and partnerships. Business alliances formed now have long-term growth potential. Public reputation and social standing improve through benevolent associations.", "hi": "गुरु सातवें भाव में विवाह और साझेदारी में शुभ विकास लाता है। अभी बनाए गए व्यापारिक गठबंधन में दीर्घकालिक विकास क्षमता है। परोपकारी संगठनों के माध्यम से सार्वजनिक प्रतिष्ठा और सामाजिक स्थिति में सुधार होता है।"},
            "love": {"en": "Marriage prospects are exceptionally bright and partnerships deepen with wisdom. Spouse brings good fortune and prosperity into your life. Existing marriages experience renewal of commitment and joy.", "hi": "विवाह की संभावनाएं असाधारण रूप से उज्ज्वल हैं और साझेदारी ज्ञान के साथ गहरी होती है। पति/पत्नी आपके जीवन में सौभाग्य और समृद्धि लाते हैं। मौजूदा विवाह प्रतिबद्धता और आनंद का नवीनीकरण अनुभव करते हैं।"},
            "career": {"en": "Business partnerships and client relationships expand profitably. Consulting, legal advisory, and diplomatic roles suit this transit perfectly. Joint ventures with ethical partners yield exceptional results.", "hi": "व्यापारिक साझेदारी और ग्राहक संबंध लाभदायक रूप से विस्तारित होते हैं। परामर्श, कानूनी सलाहकार और कूटनीतिक भूमिकाएं इस गोचर के लिए उपयुक्त हैं। नैतिक भागीदारों के साथ संयुक्त उद्यम असाधारण परिणाम देते हैं।"},
            "finance": {"en": "Joint financial ventures and partnership investments prosper. Spouse or business partner contributes to wealth growth. Legal settlements and contractual agreements work in your favor.", "hi": "संयुक्त वित्तीय उद्यम और साझेदारी निवेश समृद्ध होते हैं। पति/पत्नी या व्यापारिक भागीदार धन वृद्धि में योगदान करते हैं। कानूनी समझौते और अनुबंध आपके पक्ष में काम करते हैं।"},
            "health": {"en": "Partner's positive influence on health habits creates mutual wellbeing. Kidneys and lower back benefit from adequate hydration and moderate exercise. Social wellness through meaningful partnerships supports overall health.", "hi": "स्वास्थ्य आदतों पर साथी का सकारात्मक प्रभाव पारस्परिक कल्याण बनाता है। पर्याप्त जलयोजन और संयमित व्यायाम से गुर्दे और पीठ का निचला भाग लाभान्वित होता है। सार्थक साझेदारी के माध्यम से सामाजिक कल्याण समग्र स्वास्थ्य का समर्थन करता है।"},
        },
        8: {
            "general": {"en": "Jupiter in the 8th house provides protection during transformative experiences and hidden blessings. Occult knowledge, research, and inheritance matters develop favorably. Spiritual transformation through deep study and meditation is indicated.", "hi": "गुरु आठवें भाव में परिवर्तनकारी अनुभवों और छिपे आशीर्वादों के दौरान सुरक्षा प्रदान करता है। गूढ़ ज्ञान, अनुसंधान और विरासत मामले अनुकूल रूप से विकसित होते हैं। गहन अध्ययन और ध्यान के माध्यम से आध्यात्मिक परिवर्तन संकेतित है।"},
            "love": {"en": "Deep emotional transformation strengthens intimate bonds. Trust and vulnerability create profound connection with partners. Shared spiritual practices or crisis management brings couples closer.", "hi": "गहन भावनात्मक परिवर्तन अंतरंग बंधनों को मजबूत करता है। विश्वास और भेद्यता साथियों के साथ गहन संबंध बनाती है। साझा आध्यात्मिक अभ्यास या संकट प्रबंधन जोड़ों को करीब लाता है।"},
            "career": {"en": "Research, insurance, occult sciences, and transformational coaching careers benefit. Hidden professional opportunities reveal themselves. Working with other people's resources becomes profitable.", "hi": "अनुसंधान, बीमा, गूढ़ विज्ञान और परिवर्तनकारी कोचिंग करियर लाभान्वित होते हैं। छिपे पेशेवर अवसर स्वयं प्रकट होते हैं। दूसरों के संसाधनों के साथ कार्य करना लाभदायक हो जाता है।"},
            "finance": {"en": "Inheritance, insurance claims, and joint financial dealings bring unexpected gains. Tax planning and financial restructuring yield positive outcomes. Hidden wealth or forgotten assets may resurface.", "hi": "विरासत, बीमा दावे और संयुक्त वित्तीय लेनदेन अप्रत्याशित लाभ लाते हैं। कर योजना और वित्तीय पुनर्गठन सकारात्मक परिणाम देते हैं। छिपी संपत्ति या भूली हुई संपत्ति फिर से सतह पर आ सकती है।"},
            "health": {"en": "Jupiter protects against severe 8th house health challenges. Chronic conditions show improvement through alternative healing. Reproductive health and longevity benefit from this protective transit.", "hi": "गुरु गंभीर अष्टम भाव स्वास्थ्य चुनौतियों से रक्षा करता है। वैकल्पिक उपचार से पुरानी स्थितियों में सुधार दिखता है। इस सुरक्षात्मक गोचर से प्रजनन स्वास्थ्य और दीर्घायु लाभान्वित होती है।"},
        },
        9: {
            "general": {"en": "Jupiter in its own 9th house brings peak fortune, dharmic alignment, and spiritual wisdom. Long-distance travels for pilgrimage or higher education are blessed. Father and guru relationships strengthen and guide your path.", "hi": "गुरु अपने नौवें भाव में चरम सौभाग्य, धार्मिक संरेखण और आध्यात्मिक ज्ञान लाता है। तीर्थयात्रा या उच्च शिक्षा के लिए लंबी दूरी की यात्राएं आशीर्वादित हैं। पिता और गुरु संबंध मजबूत होते हैं और आपके मार्ग का मार्गदर्शन करते हैं।"},
            "love": {"en": "Spiritual and philosophical compatibility creates deepest romantic bonds. International romance or multicultural relationships are favored. Marriage blessed by religious ceremonies brings lasting happiness.", "hi": "आध्यात्मिक और दार्शनिक अनुकूलता सबसे गहरे रोमांटिक बंधन बनाती है। अंतरराष्ट्रीय रोमांस या बहुसांस्कृतिक संबंध अनुकूल हैं। धार्मिक अनुष्ठानों से आशीर्वादित विवाह स्थायी खुशी लाता है।"},
            "career": {"en": "Academic, religious, legal, and international careers reach their zenith. Higher education and advanced degrees bring career-defining opportunities. Publishing and teaching at prestigious institutions are highly indicated.", "hi": "शैक्षणिक, धार्मिक, कानूनी और अंतरराष्ट्रीय करियर अपने चरम पर पहुंचते हैं। उच्च शिक्षा और उन्नत डिग्री करियर-निर्धारक अवसर लाती हैं। प्रतिष्ठित संस्थानों में प्रकाशन और शिक्षण अत्यधिक संकेतित है।"},
            "finance": {"en": "Fortune favors financial growth through ethical and dharmic means. International business and academic earnings are especially strong. Father or guru may facilitate significant financial opportunities.", "hi": "भाग्य नैतिक और धार्मिक साधनों से वित्तीय विकास का समर्थन करता है। अंतरराष्ट्रीय व्यापार और शैक्षणिक कमाई विशेष रूप से मजबूत है। पिता या गुरु महत्वपूर्ण वित्तीय अवसर सुगम कर सकते हैं।"},
            "health": {"en": "Hips and thighs need care against weight gain from prosperity. Spiritual practices and pilgrimage travel rejuvenate body and mind. Overall health is protected by this most fortunate transit of Jupiter.", "hi": "समृद्धि से वजन बढ़ने के विरुद्ध कूल्हों और जांघों की देखभाल आवश्यक है। आध्यात्मिक अभ्यास और तीर्थ यात्रा शरीर और मन को पुनर्जीवित करती है। गुरु के इस सबसे भाग्यशाली गोचर से समग्र स्वास्थ्य सुरक्षित है।"},
        },
        10: {
            "general": {"en": "Jupiter in the 10th house brings peak career expansion and professional recognition. Authority and government favor your endeavors. Your public reputation reaches its highest point through ethical leadership.", "hi": "गुरु दसवें भाव में चरम करियर विस्तार और पेशेवर मान्यता लाता है। अधिकारी और सरकार आपके प्रयासों का समर्थन करती है। नैतिक नेतृत्व से आपकी सार्वजनिक प्रतिष्ठा अपने उच्चतम बिंदु पर पहुंचती है।"},
            "love": {"en": "Professional success enhances romantic attractiveness. Partner takes pride in your public achievements. Work-life balance requires attention but relationships benefit from your elevated status.", "hi": "पेशेवर सफलता रोमांटिक आकर्षण बढ़ाती है। साथी आपकी सार्वजनिक उपलब्धियों पर गर्व करता है। कार्य-जीवन संतुलन पर ध्यान आवश्यक है लेकिन आपकी ऊंची स्थिति से संबंध लाभान्वित होते हैं।"},
            "career": {"en": "This is THE career transit — promotions, honors, and professional milestones manifest. Government positions, judicial roles, and executive leadership are strongly favored. Your professional legacy takes shape.", "hi": "यह करियर गोचर है — पदोन्नति, सम्मान और पेशेवर मील के पत्थर प्रकट होते हैं। सरकारी पद, न्यायिक भूमिकाएं और कार्यकारी नेतृत्व अत्यधिक अनुकूल हैं। आपकी पेशेवर विरासत आकार लेती है।"},
            "finance": {"en": "Professional income reaches its peak with bonuses, promotions, and recognition rewards. Government contracts and large-scale projects bring substantial earnings. Invest wisely in this prosperity period.", "hi": "बोनस, पदोन्नति और मान्यता पुरस्कारों से पेशेवर आय अपने चरम पर पहुंचती है। सरकारी अनुबंध और बड़े पैमाने की परियोजनाएं पर्याप्त कमाई लाती हैं। इस समृद्धि काल में बुद्धिमानी से निवेश करें।"},
            "health": {"en": "Knees and bones need care despite overall strong health. Professional success may lead to sedentary lifestyle requiring conscious movement. Weight management through balanced diet supports sustained performance.", "hi": "समग्र मजबूत स्वास्थ्य के बावजूद घुटनों और हड्डियों की देखभाल आवश्यक है। पेशेवर सफलता गतिहीन जीवनशैली की ओर ले जा सकती है जिसमें सचेत गतिविधि आवश्यक है। संतुलित आहार से वजन प्रबंधन निरंतर प्रदर्शन का समर्थन करता है।"},
        },
        11: {
            "general": {"en": "Jupiter in the 11th house maximizes gains, social fulfillment, and achievement of long-cherished desires. Elder siblings and influential friends become channels of fortune. Community leadership and social impact reach their peak.", "hi": "गुरु ग्यारहवें भाव में लाभ, सामाजिक पूर्णता और पुरानी इच्छाओं की पूर्ति को अधिकतम करता है। बड़े भाई-बहन और प्रभावशाली मित्र सौभाग्य के माध्यम बनते हैं। सामुदायिक नेतृत्व और सामाजिक प्रभाव चरम पर पहुंचता है।"},
            "love": {"en": "Social circles expand bringing compatible romantic connections. Friends and community support your relationships generously. Group celebrations and social events facilitate joyful romantic moments.", "hi": "सामाजिक मंडल विस्तारित होते हैं जो अनुकूल रोमांटिक संबंध लाते हैं। मित्र और समुदाय आपके संबंधों का उदारता से समर्थन करते हैं। सामूहिक उत्सव और सामाजिक कार्यक्रम आनंदमय रोमांटिक क्षण सुगम करते हैं।"},
            "career": {"en": "Professional networking yields extraordinary opportunities. Large organizations and institutional roles expand your influence. Team achievements under your guidance bring collective recognition.", "hi": "पेशेवर नेटवर्किंग असाधारण अवसर देती है। बड़े संगठन और संस्थागत भूमिकाएं आपके प्रभाव का विस्तार करती हैं। आपके मार्गदर्शन में टीम उपलब्धियां सामूहिक मान्यता लाती हैं।"},
            "finance": {"en": "Multiple income streams flow abundantly. Investments mature and yield excellent returns. Friends and network connections facilitate profitable business opportunities.", "hi": "कई आय धाराएं प्रचुरता से प्रवाहित होती हैं। निवेश परिपक्व होते हैं और उत्कृष्ट रिटर्न देते हैं। मित्र और नेटवर्क कनेक्शन लाभदायक व्यापार अवसर सुगम करते हैं।"},
            "health": {"en": "Calves and ankles benefit from Jupiter's expansive energy supporting circulation. Social overindulgence is the main health risk during this abundant period. Gratitude practices and moderation sustain physical and mental balance.", "hi": "गुरु की विस्तारक ऊर्जा से रक्त संचार में सहायता से पिंडली और टखने लाभान्वित होते हैं। इस प्रचुर अवधि में सामाजिक अत्यधिक भोग मुख्य स्वास्थ्य जोखिम है। कृतज्ञता अभ्यास और संयम शारीरिक और मानसिक संतुलन बनाए रखते हैं।"},
        },
        12: {
            "general": {"en": "Jupiter in the 12th house blesses spiritual liberation, foreign connections, and charitable works. Moksha-oriented activities bring deep inner fulfillment. Foreign travel for spiritual purposes or higher study is indicated.", "hi": "गुरु बारहवें भाव में आध्यात्मिक मुक्ति, विदेशी संबंधों और दानार्थ कार्यों का आशीर्वाद देता है। मोक्ष-उन्मुख गतिविधियां गहरी आंतरिक पूर्णता लाती हैं। आध्यात्मिक उद्देश्यों या उच्च अध्ययन के लिए विदेश यात्रा संकेतित है।"},
            "love": {"en": "Spiritual and karmic connections define romantic relationships. Unconditional love and selfless giving strengthen bonds. Foreign or spiritually-oriented partners attract your interest.", "hi": "आध्यात्मिक और कार्मिक संबंध रोमांटिक रिश्तों को परिभाषित करते हैं। बिना शर्त प्रेम और निस्वार्थ देना बंधन मजबूत करता है। विदेशी या आध्यात्मिक रूप से उन्मुख साथी आपकी रुचि आकर्षित करते हैं।"},
            "career": {"en": "International organizations, spiritual institutions, and charitable foundations offer fulfilling career paths. Behind-the-scenes advisory and research roles bring quiet satisfaction. Hospital and healing-related professions thrive.", "hi": "अंतरराष्ट्रीय संगठन, आध्यात्मिक संस्थान और धर्मार्थ फाउंडेशन संतोषजनक करियर मार्ग प्रदान करते हैं। पर्दे के पीछे सलाहकार और अनुसंधान भूमिकाएं शांत संतुष्टि लाती हैं। अस्पताल और उपचार-संबंधित व्यवसाय फलते-फूलते हैं।"},
            "finance": {"en": "Charitable giving and spiritual expenditure bring karmic returns. Foreign investments and international income sources prove beneficial. Material wealth may decrease but spiritual wealth increases immeasurably.", "hi": "दान और आध्यात्मिक खर्च कार्मिक प्रतिफल लाते हैं। विदेशी निवेश और अंतरराष्ट्रीय आय स्रोत लाभदायक साबित होते हैं। भौतिक धन कम हो सकता है लेकिन आध्यात्मिक धन अपरिमित रूप से बढ़ता है।"},
            "health": {"en": "Feet and lymphatic system need gentle care. Sleep quality improves through spiritual practices. Jupiter protects overall health but watch for hidden conditions requiring preventive attention.", "hi": "पैर और लसीका तंत्र को कोमल देखभाल की आवश्यकता है। आध्यात्मिक अभ्यासों से नींद की गुणवत्ता सुधरती है। गुरु समग्र स्वास्थ्य की रक्षा करता है लेकिन निवारक ध्यान आवश्यक छिपी स्थितियों पर नजर रखें।"},
        },
    },
    # =========================================================================
    # VENUS (Shukra) — Love, luxury, art, marriage, vehicles, comfort
    # Natural benefic. Karaka of beauty, relationships, creativity, wealth.
    # =========================================================================
    "Venus": {
        1: {
            "general": {"en": "Venus transiting your 1st house enhances personal charm, beauty, and social grace. Artistic talents and aesthetic sensibilities are heightened. You attract positive attention and favorable social interactions effortlessly.", "hi": "शुक्र का प्रथम भाव में गोचर व्यक्तिगत आकर्षण, सौंदर्य और सामाजिक शालीनता बढ़ाता है। कलात्मक प्रतिभा और सौंदर्य संवेदनशीलता उन्नत होती है। आप सहज रूप से सकारात्मक ध्यान और अनुकूल सामाजिक संवाद आकर्षित करते हैं।"},
            "love": {"en": "Romance blooms naturally as your attractiveness peaks. New relationships start with deep mutual appreciation. Self-love and personal grooming enhance your magnetic appeal.", "hi": "आपका आकर्षण चरम पर होने से रोमांस स्वाभाविक रूप से खिलता है। नए संबंध गहरी पारस्परिक सराहना से शुरू होते हैं। आत्म-प्रेम और व्यक्तिगत सौंदर्य आपके चुंबकीय आकर्षण को बढ़ाता है।"},
            "career": {"en": "Fashion, beauty, art, entertainment, and hospitality careers flourish. Public relations and client-facing roles benefit from your enhanced charm. Creative presentations make lasting impressions.", "hi": "फैशन, सौंदर्य, कला, मनोरंजन और आतिथ्य करियर फलते-फूलते हैं। जनसंपर्क और ग्राहक-सामना भूमिकाएं आपके बढ़े हुए आकर्षण से लाभान्वित होती हैं। रचनात्मक प्रस्तुतियां स्थायी प्रभाव बनाती हैं।"},
            "finance": {"en": "Spending on personal appearance, luxury items, and comfort increases. Earnings through artistic and beauty-related work are favored. Financial diplomacy and graceful negotiation improve outcomes.", "hi": "व्यक्तिगत बाहरी आवरण, विलासिता वस्तुओं और आराम पर खर्च बढ़ता है। कलात्मक और सौंदर्य-संबंधित कार्य से कमाई अनुकूल है। वित्तीय कूटनीति और शालीन बातचीत परिणामों में सुधार करती है।"},
            "health": {"en": "Skin, complexion, and overall appearance glow with Venus energy. Overindulgence in sweets and luxury foods is the primary risk. Balance aesthetic pleasures with healthy lifestyle choices.", "hi": "शुक्र ऊर्जा से त्वचा, रंगत और समग्र रूप में चमक आती है। मिठाइयों और विलासिता भोजन में अत्यधिक भोग प्राथमिक जोखिम है। सौंदर्य आनंद को स्वस्थ जीवनशैली विकल्पों से संतुलित करें।"},
        },
        2: {
            "general": {"en": "Venus in the 2nd house brings sweet speech, family harmony, and wealth through beauty and art. Food and sensory pleasures are elevated. Family celebrations and gatherings are especially joyful.", "hi": "शुक्र दूसरे भाव में मधुर वाणी, पारिवारिक सद्भाव और सौंदर्य व कला से धन लाता है। भोजन और इंद्रिय सुख उन्नत होते हैं। पारिवारिक उत्सव और सभाएं विशेष रूप से आनंदमय होती हैं।"},
            "love": {"en": "Family warmth and domestic love create deep comfort. Cooking together and shared meals strengthen bonds. Financial generosity toward loved ones comes naturally.", "hi": "पारिवारिक गर्मजोशी और घरेलू प्रेम गहरा आराम बनाता है। साथ मिलकर खाना बनाना और साझा भोजन बंधन मजबूत करते हैं। प्रियजनों के प्रति आर्थिक उदारता स्वाभाविक रूप से आती है।"},
            "career": {"en": "Food industry, jewelry, cosmetics, banking, and luxury retail careers prosper. Your persuasive and pleasant speech wins clients. Financial advisory roles benefit from your aesthetic sensibility.", "hi": "खाद्य उद्योग, आभूषण, सौंदर्य प्रसाधन, बैंकिंग और विलासिता खुदरा करियर समृद्ध होते हैं। आपकी प्रभावशाली और मधुर वाणी ग्राहक जीतती है। वित्तीय सलाहकार भूमिकाएं आपकी सौंदर्य संवेदनशीलता से लाभान्वित होती हैं।"},
            "finance": {"en": "Wealth accumulates through beauty, art, and luxury goods trade. Family assets and savings grow steadily. Investments in precious metals, gems, or luxury items prove profitable.", "hi": "सौंदर्य, कला और विलासिता वस्तुओं के व्यापार से धन संचित होता है। पारिवारिक संपत्ति और बचत लगातार बढ़ती है। कीमती धातुओं, रत्नों या विलासिता वस्तुओं में निवेश लाभदायक साबित होता है।"},
            "health": {"en": "Throat, face, and oral health benefit from Venus in this house. Sweet cravings may lead to sugar imbalance. Enjoy culinary pleasures mindfully to maintain dental and metabolic health.", "hi": "इस भाव में शुक्र से गला, चेहरा और मौखिक स्वास्थ्य लाभान्वित होता है। मिठास की लालसा शर्करा असंतुलन का कारण बन सकती है। दंत और चयापचय स्वास्थ्य बनाए रखने के लिए पाक आनंद सचेत रूप से लें।"},
        },
        3: {
            "general": {"en": "Venus in the 3rd house beautifies communication and creative expression. Artistic writing, music, and media work bring joy. Social interactions with neighbors and siblings become harmonious and pleasant.", "hi": "शुक्र तीसरे भाव में संवाद और रचनात्मक अभिव्यक्ति को सुंदर बनाता है। कलात्मक लेखन, संगीत और मीडिया कार्य आनंद लाते हैं। पड़ोसियों और भाई-बहनों के साथ सामाजिक संवाद सामंजस्यपूर्ण और सुखद हो जाता है।"},
            "love": {"en": "Romantic messages, love letters, and creative expressions of affection delight partners. Short romantic trips and cultural dates are especially enjoyable. Siblings may facilitate romantic introductions.", "hi": "रोमांटिक संदेश, प्रेम पत्र और स्नेह की रचनात्मक अभिव्यक्ति साथियों को प्रसन्न करती है। छोटी रोमांटिक यात्राएं और सांस्कृतिक डेट विशेष रूप से आनंददायक हैं। भाई-बहन रोमांटिक परिचय सुगम कर सकते हैं।"},
            "career": {"en": "Media, advertising, fashion blogging, and creative communications thrive. Artistic collaborations with siblings or neighbors bear fruit. Sales through charm and aesthetic presentation increase.", "hi": "मीडिया, विज्ञापन, फैशन ब्लॉगिंग और रचनात्मक संवाद फलते-फूलते हैं। भाई-बहनों या पड़ोसियों के साथ कलात्मक सहयोग फल देता है। आकर्षण और सौंदर्य प्रस्तुति से बिक्री बढ़ती है।"},
            "finance": {"en": "Income through creative communication and artistic media work grows. Short business trips combine pleasure with profit. Investment in artistic tools and creative equipment is well-timed.", "hi": "रचनात्मक संवाद और कलात्मक मीडिया कार्य से आय बढ़ती है। छोटी व्यापार यात्राएं आनंद और लाभ को जोड़ती हैं। कलात्मक उपकरणों और रचनात्मक सामग्री में निवेश सही समय पर है।"},
            "health": {"en": "Arms, hands, and throat benefit from artistic and musical activities. Sensory pleasures through music and art reduce stress naturally. Avoid neck strain from prolonged creative screen work.", "hi": "कलात्मक और संगीत गतिविधियों से बाहें, हाथ और गला लाभान्वित होता है। संगीत और कला के माध्यम से इंद्रिय सुख स्वाभाविक रूप से तनाव कम करते हैं। लंबे रचनात्मक स्क्रीन कार्य से गर्दन तनाव से बचें।"},
        },
        4: {
            "general": {"en": "Venus in the 4th house creates a beautiful and luxurious home environment. Property purchases and vehicle acquisitions are favorable. Mother's love and family comfort bring deep emotional satisfaction.", "hi": "शुक्र चौथे भाव में सुंदर और विलासितापूर्ण घरेलू वातावरण बनाता है। संपत्ति खरीद और वाहन अधिग्रहण अनुकूल हैं। माता का प्रेम और पारिवारिक आराम गहरी भावनात्मक संतुष्टि लाते हैं।"},
            "love": {"en": "Home becomes the center of romantic happiness. Decorating and beautifying shared spaces with partner brings joy. Emotional security in relationships deepens naturally.", "hi": "घर रोमांटिक खुशी का केंद्र बनता है। साथी के साथ साझा स्थानों को सजाना और सुंदर बनाना आनंद लाता है। संबंधों में भावनात्मक सुरक्षा स्वाभाविक रूप से गहरी होती है।"},
            "career": {"en": "Interior design, real estate, hospitality, and home-based creative businesses flourish. Comfort-oriented workplace improvements boost productivity. Working from a beautiful home office increases satisfaction.", "hi": "इंटीरियर डिजाइन, अचल संपत्ति, आतिथ्य और गृह-आधारित रचनात्मक व्यवसाय फलते-फूलते हैं। आराम-उन्मुख कार्यस्थल सुधार उत्पादकता बढ़ाते हैं। सुंदर होम ऑफिस से काम करना संतुष्टि बढ़ाता है।"},
            "finance": {"en": "Property and vehicle investments yield excellent value. Home renovation and interior decoration expenses are justified by increased property value. Luxury home items may stretch the budget.", "hi": "संपत्ति और वाहन निवेश उत्कृष्ट मूल्य देते हैं। गृह नवीकरण और इंटीरियर सजावट खर्च बढ़ी संपत्ति मूल्य से उचित हैं। विलासिता गृह वस्तुएं बजट को खींच सकती हैं।"},
            "health": {"en": "Emotional comfort and beautiful surroundings positively impact physical health. Chest and heart areas feel lighter with emotional harmony at home. Comfort eating needs mindful attention to prevent excess.", "hi": "भावनात्मक आराम और सुंदर परिवेश शारीरिक स्वास्थ्य पर सकारात्मक प्रभाव डालते हैं। घर पर भावनात्मक सद्भाव से छाती और हृदय क्षेत्र हल्का महसूस करते हैं। अत्यधिकता को रोकने के लिए आराम भोजन पर सचेत ध्यान आवश्यक है।"},
        },
        5: {
            "general": {"en": "Venus in the 5th house creates peak romantic and creative energy. Artistic achievements and entertainment bring immense joy. Children bring happiness and creative collaborations yield beautiful results.", "hi": "शुक्र पांचवें भाव में चरम रोमांटिक और रचनात्मक ऊर्जा बनाता है। कलात्मक उपलब्धियां और मनोरंजन अपार आनंद लाते हैं। संतान खुशी लाती है और रचनात्मक सहयोग सुंदर परिणाम देते हैं।"},
            "love": {"en": "This is THE romance transit — love, passion, and creative connection peak. New relationships start with fairy-tale energy. Existing partnerships experience beautiful renewal and deepening.", "hi": "यह रोमांस गोचर है — प्रेम, जुनून और रचनात्मक संबंध चरम पर हैं। नए संबंध परी-कथा ऊर्जा से शुरू होते हैं। मौजूदा साझेदारी सुंदर नवीनीकरण और गहराई का अनुभव करती है।"},
            "career": {"en": "Entertainment, arts, fashion, music, and creative industries offer abundant opportunities. Teaching arts and mentoring creative talent brings fulfillment. Stock market and speculative ventures may favor artistic industries.", "hi": "मनोरंजन, कला, फैशन, संगीत और रचनात्मक उद्योग प्रचुर अवसर प्रदान करते हैं। कला शिक्षण और रचनात्मक प्रतिभा का मार्गदर्शन पूर्णता लाता है। शेयर बाजार और सट्टा उद्यम कलात्मक उद्योगों के पक्ष में हो सकते हैं।"},
            "finance": {"en": "Creative works generate income and intellectual property gains value. Entertainment and art investments are well-timed. Spending on children, romance, and pleasure may exceed budget without awareness.", "hi": "रचनात्मक कार्य आय उत्पन्न करते हैं और बौद्धिक संपदा का मूल्य बढ़ता है। मनोरंजन और कला निवेश सही समय पर हैं। संतान, रोमांस और आनंद पर खर्च जागरूकता के बिना बजट से अधिक हो सकता है।"},
            "health": {"en": "Creative expression and romantic fulfillment boost mental and emotional health significantly. Stomach areas need attention regarding rich food indulgence. Joy and laughter are the best medicine during this transit.", "hi": "रचनात्मक अभिव्यक्ति और रोमांटिक पूर्णता मानसिक और भावनात्मक स्वास्थ्य को काफी बढ़ावा देती है। समृद्ध भोजन भोग के संबंध में पेट क्षेत्र पर ध्यान आवश्यक है। इस गोचर में आनंद और हंसी सबसे अच्छी दवा है।"},
        },
        6: {
            "general": {"en": "Venus in the 6th house requires extra effort to maintain harmony in daily routines. Service through beauty and art helps overcome obstacles gracefully. Health improvements through aesthetic and pleasant approaches work best.", "hi": "शुक्र छठे भाव में दैनिक दिनचर्या में सामंजस्य बनाए रखने के लिए अतिरिक्त प्रयास की आवश्यकता है। सौंदर्य और कला के माध्यम से सेवा बाधाओं को शालीनता से दूर करने में मदद करती है। सौंदर्य और सुखद दृष्टिकोण से स्वास्थ्य सुधार सबसे अच्छा काम करता है।"},
            "love": {"en": "Relationships may face minor daily friction that requires patience. Showing love through practical service and daily care matters most now. Health of partner or loved ones may need attention.", "hi": "संबंधों में दैनिक मामूली घर्षण हो सकता है जिसमें धैर्य आवश्यक है। अभी व्यावहारिक सेवा और दैनिक देखभाल से प्रेम दिखाना सबसे अधिक मायने रखता है। साथी या प्रियजनों के स्वास्थ्य पर ध्यान आवश्यक हो सकता है।"},
            "career": {"en": "Beauty services, wellness industry, and healthcare aesthetics careers benefit. Workplace harmony improves through diplomatic conflict resolution. Creative problem-solving makes routine work enjoyable.", "hi": "सौंदर्य सेवाएं, कल्याण उद्योग और स्वास्थ्य सेवा सौंदर्य करियर लाभान्वित होते हैं। कूटनीतिक संघर्ष समाधान से कार्यस्थल सद्भाव सुधरता है। रचनात्मक समस्या-समाधान दिनचर्या कार्य को आनंददायक बनाता है।"},
            "finance": {"en": "Health and beauty expenses may strain the budget. Debt related to luxury purchases needs management. Income through wellness and beauty services provides steady returns.", "hi": "स्वास्थ्य और सौंदर्य खर्च बजट पर दबाव डाल सकते हैं। विलासिता खरीद से संबंधित ऋण के प्रबंधन की आवश्यकता है। कल्याण और सौंदर्य सेवाओं से आय स्थिर रिटर्न प्रदान करती है।"},
            "health": {"en": "Reproductive and urinary system health needs attention. Sugar and sweet food intake should be moderated carefully. Pleasant healing environments and aesthetic therapy support recovery from ailments.", "hi": "प्रजनन और मूत्र प्रणाली स्वास्थ्य पर ध्यान देने की आवश्यकता है। शर्करा और मीठे भोजन का सेवन सावधानीपूर्वक संयमित करना चाहिए। सुखद उपचार वातावरण और सौंदर्य चिकित्सा बीमारियों से उबरने में सहायता करती है।"},
        },
        7: {
            "general": {"en": "Venus in its natural 7th house brings peak marriage and partnership blessings. Business partnerships and public dealings are harmonious and profitable. Diplomatic skills and social grace reach their highest expression.", "hi": "शुक्र अपने स्वाभाविक सातवें भाव में चरम विवाह और साझेदारी आशीर्वाद लाता है। व्यापारिक साझेदारी और सार्वजनिक व्यवहार सामंजस्यपूर्ण और लाभदायक होते हैं। कूटनीतिक कौशल और सामाजिक शालीनता अपनी उच्चतम अभिव्यक्ति तक पहुंचती है।"},
            "love": {"en": "Marriage and committed partnership energy is at its absolute best. Wedding ceremonies and engagement during this transit are highly auspicious. Existing relationships experience deep renewal of love and commitment.", "hi": "विवाह और प्रतिबद्ध साझेदारी ऊर्जा अपने सर्वश्रेष्ठ पर है। इस गोचर में विवाह समारोह और सगाई अत्यधिक शुभ हैं। मौजूदा संबंध प्रेम और प्रतिबद्धता का गहरा नवीनीकरण अनुभव करते हैं।"},
            "career": {"en": "Partnership businesses, luxury retail, beauty industry, and diplomatic careers peak. Client relationship management excels. Contract negotiations reach favorable and harmonious outcomes.", "hi": "साझेदारी व्यवसाय, विलासिता खुदरा, सौंदर्य उद्योग और कूटनीतिक करियर चरम पर हैं। ग्राहक संबंध प्रबंधन उत्कृष्ट होता है। अनुबंध वार्ता अनुकूल और सामंजस्यपूर्ण परिणाम तक पहुंचती है।"},
            "finance": {"en": "Joint finances and partnership investments grow through mutual cooperation. Spouse or partner brings financial prosperity. Luxury purchases and shared investments are well-timed.", "hi": "पारस्परिक सहयोग से संयुक्त वित्त और साझेदारी निवेश बढ़ते हैं। पति/पत्नी या साथी वित्तीय समृद्धि लाते हैं। विलासिता खरीद और साझा निवेश सही समय पर हैं।"},
            "health": {"en": "Kidneys and reproductive health benefit from balanced hydration and harmonious relationships. Partner's positive energy supports your wellbeing. Social wellness through loving partnerships improves overall vitality.", "hi": "संतुलित जलयोजन और सामंजस्यपूर्ण संबंधों से गुर्दे और प्रजनन स्वास्थ्य लाभान्वित होता है। साथी की सकारात्मक ऊर्जा आपके कल्याण का समर्थन करती है। प्रेमपूर्ण साझेदारी के माध्यम से सामाजिक कल्याण समग्र जीवन शक्ति में सुधार करता है।"},
        },
        8: {
            "general": {"en": "Venus in the 8th house deepens intimacy and reveals hidden beauty in transformative experiences. Inheritance or partner's wealth may become available. Occult arts and mystical studies attract your aesthetic sensibility.", "hi": "शुक्र आठवें भाव में अंतरंगता को गहरा करता है और परिवर्तनकारी अनुभवों में छिपी सुंदरता प्रकट करता है। विरासत या साथी की संपत्ति उपलब्ध हो सकती है। गूढ़ कला और रहस्यमय अध्ययन आपकी सौंदर्य संवेदनशीलता को आकर्षित करते हैं।"},
            "love": {"en": "Deep, transformative emotional and physical intimacy defines this period. Trust-based vulnerability creates profound romantic bonds. Past relationship patterns may be healed through conscious awareness.", "hi": "गहरी, परिवर्तनकारी भावनात्मक और शारीरिक अंतरंगता इस अवधि को परिभाषित करती है। विश्वास-आधारित भेद्यता गहन रोमांटिक बंधन बनाती है। सचेत जागरूकता से पिछले संबंध पैटर्न ठीक हो सकते हैं।"},
            "career": {"en": "Beauty therapy, psychology, insurance, and inheritance management careers benefit. Working with shared resources and managing others' wealth suits this placement. Behind-the-scenes creative work yields value.", "hi": "सौंदर्य चिकित्सा, मनोविज्ञान, बीमा और विरासत प्रबंधन करियर लाभान्वित होते हैं। साझा संसाधनों और दूसरों की संपत्ति प्रबंधन के साथ कार्य करना इस स्थिति के अनुकूल है। पर्दे के पीछे रचनात्मक कार्य मूल्य देता है।"},
            "finance": {"en": "Partner's finances contribute to joint prosperity. Insurance and inheritance matters develop favorably. Hidden financial resources or unexpected gifts may surface pleasantly.", "hi": "साथी की वित्त संयुक्त समृद्धि में योगदान करती है। बीमा और विरासत मामले अनुकूल रूप से विकसित होते हैं। छिपे वित्तीय संसाधन या अप्रत्याशित उपहार सुखद रूप से सतह पर आ सकते हैं।"},
            "health": {"en": "Reproductive and hormonal health needs gentle attention. Detoxification and rejuvenation therapies work exceptionally well. Emotional healing through intimate connections supports physical wellness.", "hi": "प्रजनन और हार्मोनल स्वास्थ्य को कोमल ध्यान की आवश्यकता है। विषहरण और कायाकल्प चिकित्सा असाधारण रूप से अच्छी तरह काम करती है। अंतरंग संबंधों के माध्यम से भावनात्मक उपचार शारीरिक स्वास्थ्य का समर्थन करता है।"},
        },
        9: {
            "general": {"en": "Venus in the 9th house brings love of wisdom, foreign cultures, and spiritual beauty. Pilgrimages and cultural travel are deeply satisfying. Guru and father figures offer artistic and spiritual guidance.", "hi": "शुक्र नौवें भाव में ज्ञान, विदेशी संस्कृतियों और आध्यात्मिक सौंदर्य का प्रेम लाता है। तीर्थयात्रा और सांस्कृतिक यात्रा गहरी संतुष्टि देती है। गुरु और पिता तुल्य व्यक्ति कलात्मक और आध्यात्मिक मार्गदर्शन प्रदान करते हैं।"},
            "love": {"en": "Cross-cultural romance and philosophical connections flourish. Travel brings romantic adventures and meaningful encounters. Marriage ceremonies with religious or cultural significance are blessed.", "hi": "अंतर-सांस्कृतिक रोमांस और दार्शनिक संबंध फलते-फूलते हैं। यात्रा रोमांटिक रोमांच और सार्थक मुलाकातें लाती है। धार्मिक या सांस्कृतिक महत्व वाले विवाह समारोह आशीर्वादित हैं।"},
            "career": {"en": "International arts, cultural exchange, tourism, and luxury travel industries flourish. Academic positions in arts and humanities bring fulfillment. Publishing creative or spiritual works reaches wide audiences.", "hi": "अंतरराष्ट्रीय कला, सांस्कृतिक आदान-प्रदान, पर्यटन और विलासिता यात्रा उद्योग फलते-फूलते हैं। कला और मानविकी में शैक्षणिक पद पूर्णता लाते हैं। रचनात्मक या आध्यात्मिक कार्यों का प्रकाशन व्यापक दर्शकों तक पहुंचता है।"},
            "finance": {"en": "International luxury trade and cultural tourism generate income. Art investments and collectibles appreciate in value. Father or spiritual mentor may influence positive financial opportunities.", "hi": "अंतरराष्ट्रीय विलासिता व्यापार और सांस्कृतिक पर्यटन आय उत्पन्न करते हैं। कला निवेश और संग्रहणीय वस्तुओं का मूल्य बढ़ता है। पिता या आध्यात्मिक गुरु सकारात्मक वित्तीय अवसरों को प्रभावित कर सकते हैं।"},
            "health": {"en": "Travel rejuvenates body and spirit. Hips and thighs need care during long journeys. Spiritual and artistic practices provide the most effective stress relief during this transit.", "hi": "यात्रा शरीर और आत्मा को पुनर्जीवित करती है। लंबी यात्राओं में कूल्हों और जांघों की देखभाल आवश्यक है। इस गोचर में आध्यात्मिक और कलात्मक अभ्यास सबसे प्रभावी तनाव राहत प्रदान करते हैं।"},
        },
        10: {
            "general": {"en": "Venus in the 10th house enhances professional reputation through charm and creative excellence. Public image shines with grace and aesthetic appeal. Authority figures and the public respond favorably to your pleasant demeanor.", "hi": "शुक्र दसवें भाव में आकर्षण और रचनात्मक उत्कृष्टता से पेशेवर प्रतिष्ठा बढ़ाता है। सार्वजनिक छवि शालीनता और सौंदर्य आकर्षण से चमकती है। अधिकारी और जनता आपके सुखद व्यवहार पर अनुकूल प्रतिक्रिया देते हैं।"},
            "love": {"en": "Professional success and public charm attract romantic attention. Workplace romance possibilities increase. Partner takes pride in your professional achievements and public grace.", "hi": "पेशेवर सफलता और सार्वजनिक आकर्षण रोमांटिक ध्यान आकर्षित करते हैं। कार्यस्थल रोमांस की संभावनाएं बढ़ती हैं। साथी आपकी पेशेवर उपलब्धियों और सार्वजनिक शालीनता पर गर्व करता है।"},
            "career": {"en": "Fashion, entertainment, luxury brands, and creative industries peak professionally. Public relations and brand management roles excel. Government or corporate recognition for creative contributions is possible.", "hi": "फैशन, मनोरंजन, विलासिता ब्रांड और रचनात्मक उद्योग पेशेवर रूप से चरम पर हैं। जनसंपर्क और ब्रांड प्रबंधन भूमिकाएं उत्कृष्ट होती हैं। रचनात्मक योगदान के लिए सरकारी या कॉर्पोरेट मान्यता संभव है।"},
            "finance": {"en": "Professional income through creative and beauty-related fields increases. Luxury brand endorsements and artistic commissions bring premium earnings. Public-facing business ventures attract clientele.", "hi": "रचनात्मक और सौंदर्य-संबंधित क्षेत्रों से पेशेवर आय बढ़ती है। विलासिता ब्रांड एंडोर्समेंट और कलात्मक कमीशन प्रीमियम कमाई लाते हैं। सार्वजनिक-सामना व्यापार उद्यम ग्राहक आकर्षित करते हैं।"},
            "health": {"en": "Professional grace and calm demeanor support cardiovascular health. Knees and skin reflect overall wellness status. Work-life beauty balance sustains long-term professional and personal health.", "hi": "पेशेवर शालीनता और शांत व्यवहार हृदय स्वास्थ्य का समर्थन करते हैं। घुटने और त्वचा समग्र स्वास्थ्य स्थिति को दर्शाते हैं। कार्य-जीवन सौंदर्य संतुलन दीर्घकालिक पेशेवर और व्यक्तिगत स्वास्थ्य को बनाए रखता है।"},
        },
        11: {
            "general": {"en": "Venus in the 11th house brings fulfillment of desires through social connections and artistic networks. Friendships with creative and influential people enrich life beautifully. Social events and celebrations are especially enjoyable and profitable.", "hi": "शुक्र ग्यारहवें भाव में सामाजिक संबंधों और कलात्मक नेटवर्क के माध्यम से इच्छाओं की पूर्ति लाता है। रचनात्मक और प्रभावशाली लोगों की मित्रता जीवन को सुंदर रूप से समृद्ध करती है। सामाजिक कार्यक्रम और उत्सव विशेष रूप से आनंददायक और लाभदायक होते हैं।"},
            "love": {"en": "Social gatherings create perfect romantic opportunities. Friends actively support your love life and introduce compatible partners. Group celebrations and cultural events spark romantic connections.", "hi": "सामाजिक समारोह सही रोमांटिक अवसर बनाते हैं। मित्र सक्रिय रूप से आपके प्रेम जीवन का समर्थन करते हैं और अनुकूल साथियों से परिचय कराते हैं। सामूहिक उत्सव और सांस्कृतिक कार्यक्रम रोमांटिक संबंधों को प्रज्वलित करते हैं।"},
            "career": {"en": "Social media, event management, fashion networking, and artistic collaborations thrive. Professional networking through social and cultural events opens doors. Creative team projects achieve beautiful outcomes.", "hi": "सोशल मीडिया, इवेंट मैनेजमेंट, फैशन नेटवर्किंग और कलात्मक सहयोग फलते-फूलते हैं। सामाजिक और सांस्कृतिक कार्यक्रमों के माध्यम से पेशेवर नेटवर्किंग द्वार खोलती है। रचनात्मक टीम परियोजनाएं सुंदर परिणाम प्राप्त करती हैं।"},
            "finance": {"en": "Multiple income streams through artistic and social ventures activate. Friends facilitate profitable creative opportunities. Luxury goods and fashion investments yield good returns.", "hi": "कलात्मक और सामाजिक उद्यमों के माध्यम से कई आय धाराएं सक्रिय होती हैं। मित्र लाभदायक रचनात्मक अवसर सुगम करते हैं। विलासिता वस्तुओं और फैशन निवेश अच्छे रिटर्न देते हैं।"},
            "health": {"en": "Social wellness and creative fulfillment boost immunity and mood. Ankles and circulatory system benefit from dancing and social activities. Overindulgence at social events needs conscious moderation.", "hi": "सामाजिक कल्याण और रचनात्मक पूर्णता प्रतिरक्षा और मनोदशा को बढ़ावा देती है। नृत्य और सामाजिक गतिविधियों से टखने और संचार प्रणाली लाभान्वित होती है। सामाजिक कार्यक्रमों में अत्यधिक भोग के लिए सचेत संयम आवश्यक है।"},
        },
        12: {
            "general": {"en": "Venus in the 12th house brings pleasures of solitude, spiritual beauty, and foreign luxuries. Creative imagination and dream life become exceptionally vivid. Hidden romance or private pleasures mark this intimate transit.", "hi": "शुक्र बारहवें भाव में एकांत के सुख, आध्यात्मिक सौंदर्य और विदेशी विलासिता लाता है। रचनात्मक कल्पना और स्वप्न जीवन असाधारण रूप से जीवंत हो जाता है। गुप्त रोमांस या निजी सुख इस अंतरंग गोचर को चिह्नित करते हैं।"},
            "love": {"en": "Secret romantic feelings and private emotional worlds are deeply fulfilling. Spiritual love transcends physical boundaries. Foreign or long-distance romance carries special karmic significance.", "hi": "गुप्त रोमांटिक भावनाएं और निजी भावनात्मक संसार गहरी पूर्णता देते हैं। आध्यात्मिक प्रेम भौतिक सीमाओं से परे जाता है। विदेशी या लंबी दूरी का रोमांस विशेष कार्मिक महत्व रखता है।"},
            "career": {"en": "Behind-the-scenes creative work, foreign luxury industries, and spiritual arts flourish. Hospitality in foreign locations and retreat center management suit this transit. Charitable and humanitarian work brings deep satisfaction.", "hi": "पर्दे के पीछे रचनात्मक कार्य, विदेशी विलासिता उद्योग और आध्यात्मिक कला फलते-फूलते हैं। विदेशी स्थानों में आतिथ्य और रिट्रीट सेंटर प्रबंधन इस गोचर के अनुकूल है। दानार्थ और मानवतावादी कार्य गहरी संतुष्टि लाता है।"},
            "finance": {"en": "Expenses on luxury, foreign travel, and spiritual retreats increase significantly. Hidden sources of beauty-related income may emerge. Charitable donations bring karmic returns beyond material measurement.", "hi": "विलासिता, विदेशी यात्रा और आध्यात्मिक एकांतवास पर खर्च काफी बढ़ता है। सौंदर्य-संबंधित आय के छिपे स्रोत उभर सकते हैं। दान भौतिक माप से परे कार्मिक प्रतिफल लाता है।"},
            "health": {"en": "Feet and lymphatic system need pampering and care. Sleep quality improves through beauty routines and relaxation practices. Spa treatments and aesthetic healing provide exceptional therapeutic benefit.", "hi": "पैर और लसीका तंत्र को लाड़-प्यार और देखभाल की आवश्यकता है। सौंदर्य दिनचर्या और विश्राम अभ्यासों से नींद की गुणवत्ता सुधरती है। स्पा उपचार और सौंदर्य उपचार असाधारण चिकित्सीय लाभ प्रदान करते हैं।"},
        },
    },
    # =========================================================================
    # SATURN (Shani) — Discipline, delays, labor, longevity, karma
    # Great malefic. Karaka of karma, justice, servants, chronic conditions.
    # =========================================================================
    "Saturn": {
        1: {
            "general": {"en": "Saturn transiting your 1st house brings serious self-reflection, discipline, and responsibility. Physical appearance may appear more mature and authoritative. Personal growth comes through sustained effort and patience.", "hi": "शनि का प्रथम भाव में गोचर गंभीर आत्म-चिंतन, अनुशासन और जिम्मेदारी लाता है। शारीरिक रूप अधिक परिपक्व और अधिकारपूर्ण दिख सकता है। व्यक्तिगत विकास निरंतर प्रयास और धैर्य से आता है।"},
            "love": {"en": "Relationships demand maturity, commitment, and realistic expectations. Superficial connections fall away leaving only genuine bonds. Patient building of trust creates lasting relationship foundations.", "hi": "संबंध परिपक्वता, प्रतिबद्धता और यथार्थवादी अपेक्षाओं की मांग करते हैं। सतही संबंध दूर हो जाते हैं केवल वास्तविक बंधन बचते हैं। विश्वास का धैर्यपूर्ण निर्माण स्थायी संबंध नींव बनाता है।"},
            "career": {"en": "Career progress is slow but durable through disciplined effort. Authority and responsibility increase with time. Hard work during this transit builds a lasting professional legacy.", "hi": "अनुशासित प्रयास से करियर प्रगति धीमी लेकिन टिकाऊ होती है। समय के साथ अधिकार और जिम्मेदारी बढ़ती है। इस गोचर में कड़ी मेहनत एक स्थायी पेशेवर विरासत बनाती है।"},
            "finance": {"en": "Financial austerity and careful budgeting are necessary. Earnings come through hard work, not luck. Long-term savings and conservative investments prove wise during this transit.", "hi": "वित्तीय मितव्ययिता और सावधानीपूर्वक बजट आवश्यक है। कमाई भाग्य से नहीं, कड़ी मेहनत से आती है। इस गोचर में दीर्घकालिक बचत और रूढ़िवादी निवेश बुद्धिमान साबित होते हैं।"},
            "health": {"en": "Bones, joints, and teeth need extra care and regular checkups. Energy may feel low requiring adequate rest and nutrition. Chronic conditions need disciplined management through consistent routines.", "hi": "हड्डियों, जोड़ों और दांतों को अतिरिक्त देखभाल और नियमित जांच की आवश्यकता है। ऊर्जा कम महसूस हो सकती है जिसमें पर्याप्त आराम और पोषण आवश्यक है। पुरानी स्थितियों के लिए सुसंगत दिनचर्या से अनुशासित प्रबंधन आवश्यक है।"},
        },
        2: {
            "general": {"en": "Saturn in the 2nd house restricts speech and demands careful financial management. Family obligations increase and require dutiful attention. Wealth building is slow but steady through disciplined saving.", "hi": "शनि दूसरे भाव में वाणी को संयमित करता है और सावधानीपूर्वक वित्तीय प्रबंधन की मांग करता है। पारिवारिक दायित्व बढ़ते हैं और कर्तव्यपूर्ण ध्यान की आवश्यकता होती है। अनुशासित बचत से धन निर्माण धीमा लेकिन स्थिर होता है।"},
            "love": {"en": "Measured and careful expression of love replaces grand gestures. Family responsibilities may overshadow romantic time. Patient investment in relationship security builds unshakeable foundations.", "hi": "भव्य भावों के स्थान पर प्रेम की मापी और सावधान अभिव्यक्ति आती है। पारिवारिक जिम्मेदारियां रोमांटिक समय पर हावी हो सकती हैं। संबंध सुरक्षा में धैर्यपूर्ण निवेश अटल नींव बनाता है।"},
            "career": {"en": "Banking, accounting, and financial discipline-oriented careers prosper through persistence. Public speaking requires extra preparation and practice. Traditional family businesses benefit from structured management.", "hi": "बैंकिंग, लेखांकन और वित्तीय अनुशासन-उन्मुख करियर दृढ़ता से समृद्ध होते हैं। सार्वजनिक भाषण में अतिरिक्त तैयारी और अभ्यास आवश्यक है। पारंपरिक पारिवारिक व्यवसाय संरचित प्रबंधन से लाभान्वित होते हैं।"},
            "finance": {"en": "Strict budgeting and expense control are essential during this transit. Family financial obligations may feel burdensome. Long-term wealth creation through systematic investment plans works best.", "hi": "इस गोचर में सख्त बजट और खर्च नियंत्रण आवश्यक हैं। पारिवारिक वित्तीय दायित्व बोझिल लग सकते हैं। व्यवस्थित निवेश योजनाओं से दीर्घकालिक धन सृजन सबसे अच्छा काम करता है।"},
            "health": {"en": "Teeth, jaw, and throat areas may experience chronic or recurring issues. Diet needs to be nutritious but simple and easy to digest. Dental care and regular health checkups prevent compounding problems.", "hi": "दांत, जबड़ा और गले के क्षेत्र में पुरानी या आवर्ती समस्याएं हो सकती हैं। आहार पौष्टिक लेकिन सरल और पचाने में आसान होना चाहिए। दंत चिकित्सा और नियमित स्वास्थ्य जांच समस्याओं को बढ़ने से रोकती है।"},
        },
        3: {
            "general": {"en": "Saturn in the 3rd house brings disciplined communication and structured effort. Short travels may face delays but yield lasting results. Sibling relationships require patience and mature handling.", "hi": "शनि तीसरे भाव में अनुशासित संवाद और संरचित प्रयास लाता है। छोटी यात्राओं में देरी हो सकती है लेकिन स्थायी परिणाम मिलते हैं। भाई-बहन संबंधों में धैर्य और परिपक्व प्रबंधन आवश्यक है।"},
            "love": {"en": "Communication in relationships becomes more deliberate and thoughtful. Expressing feelings may feel difficult but sincerity deepens bonds. Written expressions of love carry more weight than verbal ones.", "hi": "संबंधों में संवाद अधिक सोच-विचार कर और विचारशील हो जाता है। भावनाओं को व्यक्त करना कठिन लग सकता है लेकिन ईमानदारी बंधन गहरा करती है। प्रेम की लिखित अभिव्यक्ति मौखिक से अधिक प्रभावी होती है।"},
            "career": {"en": "Technical writing, structured communication, and methodical work processes excel. Training programs and skill building require patience but yield lasting competence. Media work demands extra preparation.", "hi": "तकनीकी लेखन, संरचित संवाद और व्यवस्थित कार्य प्रक्रियाएं उत्कृष्ट होती हैं। प्रशिक्षण कार्यक्रम और कौशल निर्माण में धैर्य आवश्यक है लेकिन स्थायी योग्यता मिलती है। मीडिया कार्य में अतिरिक्त तैयारी की मांग होती है।"},
            "finance": {"en": "Communication-based income may slow temporarily. Short business trips require careful cost management. Sibling financial matters need clear boundaries and documentation.", "hi": "संवाद-आधारित आय अस्थायी रूप से धीमी हो सकती है। छोटी व्यापार यात्राओं में सावधानीपूर्वक लागत प्रबंधन आवश्यक है। भाई-बहनों के वित्तीय मामलों में स्पष्ट सीमाओं और दस्तावेज़ीकरण की आवश्यकता है।"},
            "health": {"en": "Shoulders, arms, and nervous system need protection from repetitive strain. Mental fatigue from structured work requires deliberate rest. Breathing exercises and stretching prevent chronic tension buildup.", "hi": "कंधे, बाहें और तंत्रिका तंत्र को दोहरावदार तनाव से सुरक्षा की आवश्यकता है। संरचित कार्य से मानसिक थकान में जानबूझकर आराम आवश्यक है। श्वास व्यायाम और स्ट्रेचिंग पुराने तनाव संचय को रोकते हैं।"},
        },
        4: {
            "general": {"en": "Saturn in the 4th house tests domestic stability and demands emotional maturity. Property matters may face delays or structural issues requiring repairs. Mother's health or family elderly may need dutiful care.", "hi": "शनि चौथे भाव में घरेलू स्थिरता की परीक्षा लेता है और भावनात्मक परिपक्वता की मांग करता है। संपत्ति मामलों में देरी या संरचनात्मक मुद्दे हो सकते हैं जिनमें मरम्मत आवश्यक है। माता का स्वास्थ्य या बुजुर्ग परिजनों को कर्तव्यपूर्ण देखभाल की आवश्यकता हो सकती है।"},
            "love": {"en": "Emotional walls may build up requiring patient dismantling through trust. Home environment affects relationship quality directly. Building a secure physical home together strengthens partnership bonds.", "hi": "भावनात्मक दीवारें बन सकती हैं जिन्हें विश्वास से धैर्यपूर्वक हटाने की आवश्यकता है। घरेलू वातावरण सीधे संबंध गुणवत्ता को प्रभावित करता है। साथ मिलकर सुरक्षित घर बनाना साझेदारी बंधन मजबूत करता है।"},
            "career": {"en": "Real estate, construction, agriculture, and infrastructure careers demand patience but build lasting assets. Working from home requires extra discipline. Career satisfaction comes through serving family and community.", "hi": "अचल संपत्ति, निर्माण, कृषि और बुनियादी ढांचा करियर में धैर्य की मांग है लेकिन स्थायी संपत्ति बनती है। घर से काम करने में अतिरिक्त अनुशासन आवश्यक है। परिवार और समुदाय की सेवा से करियर संतुष्टि मिलती है।"},
            "finance": {"en": "Property taxes, home repairs, and family obligations create financial pressure. Real estate investments made now will appreciate over the long term. Conservative approach to home-related spending is wise.", "hi": "संपत्ति कर, गृह मरम्मत और पारिवारिक दायित्व वित्तीय दबाव बनाते हैं। अभी किए गए अचल संपत्ति निवेश दीर्घकाल में मूल्य बढ़ाएंगे। गृह-संबंधित खर्च के लिए रूढ़िवादी दृष्टिकोण बुद्धिमान है।"},
            "health": {"en": "Chest, heart, and emotional health need careful attention. Depression or emotional heaviness may surface requiring professional support. Warm home environment and family connection support emotional healing.", "hi": "छाती, हृदय और भावनात्मक स्वास्थ्य पर सावधानीपूर्वक ध्यान देने की आवश्यकता है। अवसाद या भावनात्मक भारीपन सतह पर आ सकता है जिसमें पेशेवर सहायता आवश्यक है। गर्म घरेलू वातावरण और पारिवारिक जुड़ाव भावनात्मक उपचार का समर्थन करते हैं।"},
        },
        5: {
            "general": {"en": "Saturn in the 5th house delays creative gratification and tests patience in matters of children and romance. Structured creativity and disciplined artistic practice produce lasting works. Academic rigors yield valuable qualifications.", "hi": "शनि पांचवें भाव में रचनात्मक तृप्ति में देरी करता है और संतान और रोमांस मामलों में धैर्य की परीक्षा लेता है। संरचित रचनात्मकता और अनुशासित कलात्मक अभ्यास स्थायी कार्य उत्पन्न करते हैं। शैक्षणिक कठोरता मूल्यवान योग्यताएं देती है।"},
            "love": {"en": "Romance proceeds cautiously with realistic evaluation of compatibility. Age-gap or mature relationships may form. Building love through shared responsibilities creates deeper bonds than passion alone.", "hi": "रोमांस अनुकूलता के यथार्थवादी मूल्यांकन के साथ सावधानी से आगे बढ़ता है। आयु-अंतर या परिपक्व संबंध बन सकते हैं। साझा जिम्मेदारियों से प्रेम बनाना केवल जुनून से अधिक गहरे बंधन बनाता है।"},
            "career": {"en": "Research, structured academic work, and disciplined creative industries demand persistence. Teaching and mentoring mature students bring steady satisfaction. Long-term creative projects set during this transit endure.", "hi": "अनुसंधान, संरचित शैक्षणिक कार्य और अनुशासित रचनात्मक उद्योग दृढ़ता की मांग करते हैं। परिपक्व छात्रों को शिक्षण और मार्गदर्शन स्थिर संतुष्टि लाता है। इस गोचर में शुरू की गई दीर्घकालिक रचनात्मक परियोजनाएं टिकती हैं।"},
            "finance": {"en": "Speculative ventures are risky and should be avoided. Children's education expenses require careful long-term planning. Conservative investment in blue-chip and established assets is safest.", "hi": "सट्टा उद्यम जोखिम भरे हैं और इनसे बचना चाहिए। बच्चों के शिक्षा खर्च के लिए सावधानीपूर्वक दीर्घकालिक योजना आवश्यक है। ब्लू-चिप और स्थापित संपत्तियों में रूढ़िवादी निवेश सबसे सुरक्षित है।"},
            "health": {"en": "Stomach and upper digestive system need disciplined dietary attention. Stress from creative blocks or children's issues affects physical health. Regular meditation and structured relaxation routines are essential.", "hi": "पेट और ऊपरी पाचन तंत्र को अनुशासित आहार ध्यान की आवश्यकता है। रचनात्मक अवरोधों या संतान के मुद्दों से तनाव शारीरिक स्वास्थ्य को प्रभावित करता है। नियमित ध्यान और संरचित विश्राम दिनचर्या आवश्यक हैं।"},
        },
        6: {
            "general": {"en": "Saturn in the 6th house gives strength to overcome enemies, diseases, and debts through systematic effort. Service and duty become central themes of daily life. Legal matters resolve slowly but definitively in your favor.", "hi": "शनि छठे भाव में व्यवस्थित प्रयास से शत्रुओं, रोगों और ऋणों पर विजय की शक्ति देता है। सेवा और कर्तव्य दैनिक जीवन की केंद्रीय विषय बन जाते हैं। कानूनी मामले धीरे लेकिन निश्चित रूप से आपके पक्ष में हल होते हैं।"},
            "love": {"en": "Selfless service to partner during difficult times strengthens bonds permanently. Health challenges of loved ones require patient support. Showing love through reliable daily actions matters most.", "hi": "कठिन समय में साथी की निस्वार्थ सेवा बंधन को स्थायी रूप से मजबूत करती है। प्रियजनों की स्वास्थ्य चुनौतियों में धैर्यपूर्ण सहायता आवश्यक है। विश्वसनीय दैनिक कार्यों से प्रेम दिखाना सबसे अधिक मायने रखता है।"},
            "career": {"en": "Healthcare, law enforcement, social work, and labor-intensive industries thrive. Overcoming workplace challenges builds unshakeable professional credibility. Competitive examinations favor disciplined preparation.", "hi": "स्वास्थ्य सेवा, कानून प्रवर्तन, सामाजिक कार्य और श्रम-गहन उद्योग फलते-फूलते हैं। कार्यस्थल चुनौतियों पर विजय अटल पेशेवर विश्वसनीयता बनाती है। प्रतियोगी परीक्षाएं अनुशासित तैयारी का समर्थन करती हैं।"},
            "finance": {"en": "Debts reduce through disciplined repayment over time. Healthcare costs need insurance coverage and advance planning. Steady income from service-oriented work provides financial stability.", "hi": "समय के साथ अनुशासित पुनर्भुगतान से ऋण कम होते हैं। स्वास्थ्य सेवा लागत के लिए बीमा कवरेज और अग्रिम योजना आवश्यक है। सेवा-उन्मुख कार्य से स्थिर आय वित्तीय स्थिरता प्रदान करती है।"},
            "health": {"en": "Chronic health conditions can be managed effectively through disciplined routines. Digestive and immune system require consistent attention. Saturn rewards those who maintain strict health disciplines during this transit.", "hi": "अनुशासित दिनचर्या से पुरानी स्वास्थ्य स्थितियों को प्रभावी ढंग से प्रबंधित किया जा सकता है। पाचन और प्रतिरक्षा प्रणाली को लगातार ध्यान देने की आवश्यकता है। शनि इस गोचर में सख्त स्वास्थ्य अनुशासन बनाए रखने वालों को पुरस्कृत करता है।"},
        },
        7: {
            "general": {"en": "Saturn in the 7th house tests partnerships through responsibility and commitment. Business partnerships require formal agreements and realistic expectations. Marriage demands maturity, patience, and long-term dedication.", "hi": "शनि सातवें भाव में जिम्मेदारी और प्रतिबद्धता से साझेदारी की परीक्षा लेता है। व्यापारिक साझेदारी में औपचारिक समझौते और यथार्थवादी अपेक्षाएं आवश्यक हैं। विवाह में परिपक्वता, धैर्य और दीर्घकालिक समर्पण की मांग है।"},
            "love": {"en": "Relationships that survive Saturn's test emerge infinitely stronger. Mature, committed partnerships form during this serious transit. Unrealistic romantic expectations are replaced by genuine companionship.", "hi": "शनि की परीक्षा से बचे संबंध अनंत रूप से मजबूत होकर उभरते हैं। इस गंभीर गोचर में परिपक्व, प्रतिबद्ध साझेदारी बनती है। अवास्तविक रोमांटिक अपेक्षाओं का स्थान वास्तविक साथ लेता है।"},
            "career": {"en": "Business partnerships formalized now last decades. Legal and contractual clarity is essential in all dealings. Public responsibilities and diplomatic roles demand serious commitment.", "hi": "अभी औपचारिक की गई व्यापारिक साझेदारी दशकों तक चलती है। सभी व्यवहारों में कानूनी और अनुबंधात्मक स्पष्टता आवश्यक है। सार्वजनिक जिम्मेदारियां और कूटनीतिक भूमिकाएं गंभीर प्रतिबद्धता की मांग करती हैं।"},
            "finance": {"en": "Joint finances need clear documentation and realistic agreements. Partnership investments require conservative approach. Legal expenses related to contracts or settlements are possible.", "hi": "संयुक्त वित्त में स्पष्ट दस्तावेज़ीकरण और यथार्थवादी समझौते आवश्यक हैं। साझेदारी निवेश में रूढ़िवादी दृष्टिकोण आवश्यक है। अनुबंध या समझौतों से संबंधित कानूनी खर्च संभव हैं।"},
            "health": {"en": "Lower back, kidneys, and reproductive system need careful monitoring. Partner's health issues may create shared stress. Balanced lifestyle with adequate rest supports partnership and personal health.", "hi": "पीठ का निचला भाग, गुर्दे और प्रजनन प्रणाली की सावधानीपूर्वक निगरानी आवश्यक है। साथी की स्वास्थ्य समस्याएं साझा तनाव बना सकती हैं। पर्याप्त आराम के साथ संतुलित जीवनशैली साझेदारी और व्यक्तिगत स्वास्थ्य का समर्थन करती है।"},
        },
        8: {
            "general": {"en": "Saturn in the 8th house brings deep karmic transformation through challenging experiences. Longevity matters and chronic health need disciplined management. Hidden obstacles surface slowly requiring patient resolution over time.", "hi": "शनि आठवें भाव में चुनौतीपूर्ण अनुभवों के माध्यम से गहन कार्मिक परिवर्तन लाता है। दीर्घायु मामले और पुरानी स्वास्थ्य स्थितियों के अनुशासित प्रबंधन की आवश्यकता है। छिपी बाधाएं धीरे-धीरे सतह पर आती हैं जिनमें समय के साथ धैर्यपूर्ण समाधान आवश्यक है।"},
            "love": {"en": "Deep emotional transformation through relationship challenges builds unshakeable bonds. Trust must be earned through consistent actions over time. Shared crisis management strengthens partnerships permanently.", "hi": "संबंध चुनौतियों के माध्यम से गहन भावनात्मक परिवर्तन अटल बंधन बनाता है। विश्वास समय के साथ सुसंगत कार्यों से अर्जित करना होता है। साझा संकट प्रबंधन साझेदारी को स्थायी रूप से मजबूत करता है।"},
            "career": {"en": "Research, insurance, estate management, and crisis consulting careers demand resilience. Behind-the-scenes institutional work builds solid professional foundations. Transformation through career challenges creates lasting expertise.", "hi": "अनुसंधान, बीमा, संपत्ति प्रबंधन और संकट परामर्श करियर लचीलापन की मांग करते हैं। पर्दे के पीछे संस्थागत कार्य ठोस पेशेवर नींव बनाता है। करियर चुनौतियों के माध्यम से परिवर्तन स्थायी विशेषज्ञता बनाता है।"},
            "finance": {"en": "Inheritance and insurance matters may face delays or complications. Hidden debts or financial obligations surface requiring resolution. Long-term financial restructuring done now creates lasting security.", "hi": "विरासत और बीमा मामलों में देरी या जटिलताएं हो सकती हैं। छिपे ऋण या वित्तीय दायित्व समाधान की आवश्यकता के साथ सतह पर आते हैं। अभी किया गया दीर्घकालिक वित्तीय पुनर्गठन स्थायी सुरक्षा बनाता है।"},
            "health": {"en": "Chronic conditions require long-term management strategies. Reproductive and elimination system health needs regular monitoring. Preventive care and disciplined health routines are non-negotiable during this transit.", "hi": "पुरानी स्थितियों के लिए दीर्घकालिक प्रबंधन रणनीतियां आवश्यक हैं। प्रजनन और उत्सर्जन प्रणाली स्वास्थ्य की नियमित निगरानी आवश्यक है। इस गोचर में निवारक देखभाल और अनुशासित स्वास्थ्य दिनचर्या अपरिहार्य हैं।"},
        },
        9: {
            "general": {"en": "Saturn in the 9th house tests faith, dharma, and philosophical convictions. Higher education demands rigorous disciplined effort. Long-distance travels face delays but yield profound learning experiences.", "hi": "शनि नौवें भाव में आस्था, धर्म और दार्शनिक विश्वासों की परीक्षा लेता है। उच्च शिक्षा कठोर अनुशासित प्रयास की मांग करती है। लंबी दूरी की यात्राओं में देरी होती है लेकिन गहन सीखने के अनुभव मिलते हैं।"},
            "love": {"en": "Cross-cultural or long-distance relationships face tests of commitment. Philosophical differences with partners require mature dialogue. Religious or spiritual practices shared with partners deepen bonds.", "hi": "अंतर-सांस्कृतिक या लंबी दूरी के संबंध प्रतिबद्धता की परीक्षा का सामना करते हैं। साथियों के साथ दार्शनिक मतभेद में परिपक्व संवाद आवश्यक है। साथियों के साथ साझा धार्मिक या आध्यात्मिक अभ्यास बंधन गहरा करते हैं।"},
            "career": {"en": "Academic tenure, legal proceedings, and international postings require sustained patience. Teaching and publishing face initial obstacles but build lasting authority. Government and judicial positions reward dedication over time.", "hi": "शैक्षणिक कार्यकाल, कानूनी कार्यवाही और अंतरराष्ट्रीय पोस्टिंग में निरंतर धैर्य आवश्यक है। शिक्षण और प्रकाशन में प्रारंभिक बाधाएं आती हैं लेकिन स्थायी अधिकार बनता है। सरकारी और न्यायिक पद समय के साथ समर्पण को पुरस्कृत करते हैं।"},
            "finance": {"en": "International financial dealings face regulatory hurdles. Educational loans and academic investments require careful planning. Father or mentor may face financial challenges needing your support.", "hi": "अंतरराष्ट्रीय वित्तीय लेनदेन में नियामकीय बाधाएं आती हैं। शैक्षणिक ऋण और निवेश में सावधानीपूर्वक योजना आवश्यक है। पिता या गुरु को वित्तीय चुनौतियों का सामना हो सकता है जिनमें आपके समर्थन की आवश्यकता है।"},
            "health": {"en": "Hip joints and thigh areas need care during long journeys and extended sitting. Philosophical stress affects physical wellbeing through tension. Traditional healing practices and nature-based remedies work best.", "hi": "लंबी यात्राओं और विस्तारित बैठने में कूल्हे के जोड़ और जांघ क्षेत्र की देखभाल आवश्यक है। दार्शनिक तनाव शारीरिक स्वास्थ्य को तनाव के माध्यम से प्रभावित करता है। पारंपरिक उपचार प्रथाएं और प्रकृति-आधारित उपचार सबसे अच्छे काम करते हैं।"},
        },
        10: {
            "general": {"en": "Saturn in the 10th house brings the heaviest career responsibilities and authority. Professional achievements come slowly but carry immense lasting value. Government, administrative, and structural leadership roles demand your best.", "hi": "शनि दसवें भाव में सबसे भारी करियर जिम्मेदारियां और अधिकार लाता है। पेशेवर उपलब्धियां धीरे आती हैं लेकिन अपार स्थायी मूल्य रखती हैं। सरकारी, प्रशासनिक और संरचनात्मक नेतृत्व भूमिकाएं आपके सर्वश्रेष्ठ की मांग करती हैं।"},
            "love": {"en": "Career demands severely test relationship patience and partner understanding. Work-life balance is the crucial challenge. Partners who support your professional mission become invaluable.", "hi": "करियर की मांगें संबंध धैर्य और साथी की समझ की कड़ी परीक्षा लेती हैं। कार्य-जीवन संतुलन महत्वपूर्ण चुनौती है। आपके पेशेवर मिशन का समर्थन करने वाले साथी अमूल्य हो जाते हैं।"},
            "career": {"en": "This is Saturn's most powerful career transit — promotions earned through years of dedication manifest. Government positions, senior management, and institutional leadership roles are strongly indicated. The professional legacy you build now lasts for decades.", "hi": "यह शनि का सबसे शक्तिशाली करियर गोचर है — वर्षों के समर्पण से अर्जित पदोन्नति प्रकट होती है। सरकारी पद, वरिष्ठ प्रबंधन और संस्थागत नेतृत्व भूमिकाएं दृढ़ता से संकेतित हैं। आप अभी जो पेशेवर विरासत बनाते हैं वह दशकों तक चलती है।"},
            "finance": {"en": "Professional income is substantial but earned through tremendous effort. Conservative investment in established institutions suits this transit. Long-term retirement and security planning is essential now.", "hi": "पेशेवर आय पर्याप्त है लेकिन जबरदस्त प्रयास से अर्जित है। स्थापित संस्थानों में रूढ़िवादी निवेश इस गोचर के अनुकूल है। दीर्घकालिक सेवानिवृत्ति और सुरक्षा योजना अभी आवश्यक है।"},
            "health": {"en": "Knees, bones, and joints are Saturn's primary concern areas in this transit. Professional stress accumulates in the skeletal system. Regular orthopedic care, calcium supplementation, and structured exercise are essential.", "hi": "घुटने, हड्डियां और जोड़ इस गोचर में शनि के प्राथमिक चिंता क्षेत्र हैं। पेशेवर तनाव कंकाल प्रणाली में संचित होता है। नियमित आर्थोपेडिक देखभाल, कैल्शियम पूरक और संरचित व्यायाम आवश्यक हैं।"},
        },
        11: {
            "general": {"en": "Saturn in the 11th house brings delayed but permanent fulfillment of long-cherished goals. Social circles narrow to serious, reliable connections. Gains come through persistence, patience, and service to larger causes.", "hi": "शनि ग्यारहवें भाव में लंबे समय से संजोए लक्ष्यों की विलंबित लेकिन स्थायी पूर्ति लाता है। सामाजिक मंडल गंभीर, विश्वसनीय संबंधों तक सीमित हो जाता है। दृढ़ता, धैर्य और बड़े उद्देश्यों की सेवा से लाभ आता है।"},
            "love": {"en": "True friendships that endure form during this selective period. Social events feel more like obligations requiring careful energy management. Quality of connections matters infinitely more than quantity.", "hi": "इस चयनात्मक अवधि में सच्ची मित्रताएं बनती हैं जो टिकती हैं। सामाजिक कार्यक्रम दायित्वों जैसे लगते हैं जिनमें सावधानीपूर्वक ऊर्जा प्रबंधन आवश्यक है। संबंधों की गुणवत्ता मात्रा से अनंत रूप से अधिक मायने रखती है।"},
            "career": {"en": "Large organizations, government institutions, and NGOs offer steady growth paths. Group leadership through structure and process yields lasting results. Professional networks built now become lifetime career assets.", "hi": "बड़े संगठन, सरकारी संस्थान और एनजीओ स्थिर विकास मार्ग प्रदान करते हैं। संरचना और प्रक्रिया के माध्यम से सामूहिक नेतृत्व स्थायी परिणाम देता है। अभी बनाए गए पेशेवर नेटवर्क आजीवन करियर संपत्ति बनते हैं।"},
            "finance": {"en": "Income streams are steady but growth is gradual. Systematic investment plans and pension contributions build long-term security. Elder siblings or senior friends may need financial support.", "hi": "आय धाराएं स्थिर हैं लेकिन वृद्धि क्रमिक है। व्यवस्थित निवेश योजनाएं और पेंशन योगदान दीर्घकालिक सुरक्षा बनाते हैं। बड़े भाई-बहन या वरिष्ठ मित्रों को वित्तीय सहायता की आवश्यकता हो सकती है।"},
            "health": {"en": "Circulation in lower legs and ankles needs attention through regular movement. Social isolation or reduced networking may affect mental wellbeing. Structured social commitments and community service combat loneliness.", "hi": "नियमित गतिविधि से पैरों के निचले हिस्से और टखनों में रक्त संचार पर ध्यान देने की आवश्यकता है। सामाजिक अलगाव या कम नेटवर्किंग मानसिक स्वास्थ्य को प्रभावित कर सकती है। संरचित सामाजिक प्रतिबद्धताएं और सामुदायिक सेवा अकेलेपन से लड़ती हैं।"},
        },
        12: {
            "general": {"en": "Saturn in the 12th house brings karmic completion, spiritual discipline, and expenses on liberation. Foreign travels for serious purposes may occur despite delays. Solitude becomes productive when embraced with spiritual discipline.", "hi": "शनि बारहवें भाव में कार्मिक पूर्णता, आध्यात्मिक अनुशासन और मुक्ति पर खर्च लाता है। देरी के बावजूद गंभीर उद्देश्यों के लिए विदेश यात्रा हो सकती है। आध्यात्मिक अनुशासन से अपनाने पर एकांत उत्पादक हो जाता है।"},
            "love": {"en": "Hidden relationship patterns from the past surface for final resolution. Spiritual love and selfless giving define the highest expression of relationships. Isolation or separation tests love's endurance and depth.", "hi": "अतीत के छिपे संबंध पैटर्न अंतिम समाधान के लिए सतह पर आते हैं। आध्यात्मिक प्रेम और निस्वार्थ देना संबंधों की उच्चतम अभिव्यक्ति को परिभाषित करता है। अलगाव या विरह प्रेम की सहनशीलता और गहराई की परीक्षा लेता है।"},
            "career": {"en": "Hospital, prison, ashram, and foreign institution work demands selfless service. Behind-the-scenes roles and research in isolation produce valuable outcomes. Career satisfaction comes through spiritual purpose rather than material success.", "hi": "अस्पताल, जेल, आश्रम और विदेशी संस्थान कार्य निस्वार्थ सेवा की मांग करता है। पर्दे के पीछे की भूमिकाएं और एकांत में अनुसंधान मूल्यवान परिणाम उत्पन्न करते हैं। भौतिक सफलता के बजाय आध्यात्मिक उद्देश्य से करियर संतुष्टि मिलती है।"},
            "finance": {"en": "Expenses on hospitals, foreign travel, spiritual practices, and charitable causes increase significantly. Financial losses teach valuable lessons about attachment and impermanence. Building spiritual wealth compensates for material austerity.", "hi": "अस्पतालों, विदेश यात्रा, आध्यात्मिक अभ्यास और दानार्थ कार्यों पर खर्च काफी बढ़ता है। वित्तीय नुकसान आसक्ति और अनित्यता के बारे में मूल्यवान सबक सिखाता है। आध्यात्मिक धन बनाना भौतिक मितव्ययिता की क्षतिपूर्ति करता है।"},
            "health": {"en": "Feet, sleep quality, and immune system require vigilant care. Chronic conditions that went untreated surface demanding attention. Hospital visits for preventive checkups and holistic healing are wise investments.", "hi": "पैर, नींद की गुणवत्ता और प्रतिरक्षा प्रणाली को सतर्क देखभाल की आवश्यकता है। अनुपचारित पुरानी स्थितियां ध्यान की मांग करते हुए सतह पर आती हैं। निवारक जांच और समग्र उपचार के लिए अस्पताल का दौरा बुद्धिमान निवेश है।"},
        },
    },
    # =========================================================================
    # RAHU (North Node) — Shadow planet of obsession, illusion, foreign
    # influence, unconventional paths, technology, sudden gains/losses.
    # Always retrograde. Karaka of worldly desires, materialism, foreigners.
    # =========================================================================
    "Rahu": {
        1: {
            "general": {
                "en": "Rahu transiting your 1st house creates an intense obsession with self-image and personal identity. You project a magnetic, larger-than-life persona that attracts attention from unusual quarters. Foreign connections and unconventional lifestyle choices define this transformative period.",
                "hi": "राहु का आपके प्रथम भाव में गोचर आत्म-छवि और व्यक्तिगत पहचान के प्रति तीव्र जुनून उत्पन्न करता है। आप एक चुंबकीय, असाधारण व्यक्तित्व प्रकट करते हैं जो असामान्य दिशाओं से ध्यान आकर्षित करता है। विदेशी संबंध और अपरंपरागत जीवनशैली विकल्प इस परिवर्तनकारी अवधि को परिभाषित करते हैं।"
            },
            "love": {
                "en": "Your mysterious aura draws intense romantic interest from unexpected people. Relationships may form with those from different cultures or backgrounds. Guard against deception in matters of the heart — not everyone is who they appear to be.",
                "hi": "आपकी रहस्यमयी आभा अप्रत्याशित लोगों से तीव्र रोमांटिक रुचि आकर्षित करती है। भिन्न संस्कृतियों या पृष्ठभूमि के लोगों से संबंध बन सकते हैं। हृदय के मामलों में छल से सावधान रहें — हर कोई वैसा नहीं है जैसा दिखता है।"
            },
            "career": {
                "en": "Unconventional career paths open with striking opportunities in technology, foreign trade, or media. You may reinvent your professional identity in ways that surprise even yourself. Ambition reaches extraordinary levels but ensure ethical boundaries remain intact.",
                "hi": "प्रौद्योगिकी, विदेशी व्यापार या मीडिया में अपरंपरागत करियर मार्ग आश्चर्यजनक अवसरों के साथ खुलते हैं। आप अपनी पेशेवर पहचान ऐसे तरीकों से पुनर्निर्मित कर सकते हैं जो स्वयं आपको भी चकित करें। महत्वाकांक्षा असाधारण स्तर तक पहुंचती है लेकिन नैतिक सीमाएं बनाए रखें।"
            },
            "finance": {
                "en": "Sudden financial gains through unconventional or foreign sources are possible but come with hidden strings. Speculative investments may yield windfall profits or dramatic losses. Avoid get-rich-quick schemes that seem too good to be true.",
                "hi": "अपरंपरागत या विदेशी स्रोतों से अचानक आर्थिक लाभ संभव है लेकिन छिपी शर्तों के साथ आता है। सट्टा निवेश से अप्रत्याशित लाभ या नाटकीय हानि हो सकती है। जल्दी अमीर बनने की उन योजनाओं से बचें जो सच होने से बहुत अच्छी लगती हैं।"
            },
            "health": {
                "en": "Mysterious or hard-to-diagnose health conditions may surface during this transit. Allergies, skin sensitivities, and neurological symptoms need attention. Alternative and foreign medicine systems may provide relief where conventional methods fail.",
                "hi": "इस गोचर के दौरान रहस्यमयी या कठिन-निदान स्वास्थ्य स्थितियां सतह पर आ सकती हैं। एलर्जी, त्वचा संवेदनशीलता और तंत्रिका संबंधी लक्षणों पर ध्यान देने की आवश्यकता है। जहां पारंपरिक विधियां विफल होती हैं वहां वैकल्पिक और विदेशी चिकित्सा पद्धतियां राहत प्रदान कर सकती हैं।"
            },
        },
        2: {
            "general": {
                "en": "Rahu in the 2nd house creates an insatiable desire for wealth accumulation and material possessions. Speech becomes persuasive but may carry elements of exaggeration or half-truths. Family dynamics shift as unconventional values challenge traditional norms.",
                "hi": "राहु दूसरे भाव में धन संचय और भौतिक संपत्ति के लिए अतृप्त इच्छा उत्पन्न करता है। वाणी प्रभावशाली बनती है लेकिन इसमें अतिशयोक्ति या अर्धसत्य के तत्व हो सकते हैं। अपरंपरागत मूल्य पारंपरिक मान्यताओं को चुनौती देते हुए पारिवारिक गतिशीलता बदलती है।"
            },
            "love": {
                "en": "Words of love carry an intoxicating charm but may lack depth or sincerity. Family members may oppose your romantic choices due to cultural or social differences. Building trust requires consistent honesty over grand gestures.",
                "hi": "प्रेम के शब्दों में मादक आकर्षण होता है लेकिन गहराई या ईमानदारी की कमी हो सकती है। सांस्कृतिक या सामाजिक भिन्नताओं के कारण परिवार के सदस्य आपकी रोमांटिक पसंद का विरोध कर सकते हैं। विश्वास बनाने के लिए बड़े इशारों से अधिक निरंतर ईमानदारी आवश्यक है।"
            },
            "career": {
                "en": "Careers in banking, finance, food industry, or foreign trade receive a powerful boost. Your persuasive speech becomes a professional asset in negotiations and client dealings. Beware of making promises you cannot fulfill to advance your position.",
                "hi": "बैंकिंग, वित्त, खाद्य उद्योग या विदेशी व्यापार में करियर को शक्तिशाली बढ़ावा मिलता है। आपकी प्रभावशाली वाणी बातचीत और ग्राहक व्यवहार में पेशेवर संपत्ति बन जाती है। अपनी स्थिति बढ़ाने के लिए ऐसे वादे करने से बचें जो आप पूरे नहीं कर सकते।"
            },
            "finance": {
                "en": "Wealth may arrive through unexpected channels — foreign investments, cryptocurrency, or speculative markets. Family inheritance could involve complications or disputes. Maintain meticulous financial records as deception in money matters is possible.",
                "hi": "धन अप्रत्याशित माध्यमों से आ सकता है — विदेशी निवेश, क्रिप्टोकरेंसी या सट्टा बाजार। पारिवारिक विरासत में जटिलताएं या विवाद शामिल हो सकते हैं। धन मामलों में छल संभव है इसलिए सावधानीपूर्वक वित्तीय रिकॉर्ड बनाए रखें।"
            },
            "health": {
                "en": "Mouth, teeth, and throat issues may flare up during this transit. Food allergies or sensitivities to foreign cuisines are possible. Avoid intoxicants and processed foods — Rahu amplifies toxin accumulation in the body.",
                "hi": "इस गोचर के दौरान मुंह, दांत और गले की समस्याएं बढ़ सकती हैं। विदेशी व्यंजनों से खाद्य एलर्जी या संवेदनशीलता संभव है। नशीले पदार्थों और प्रसंस्कृत खाद्य पदार्थों से बचें — राहु शरीर में विषाक्त पदार्थों के संचय को बढ़ाता है।"
            },
        },
        3: {
            "general": {
                "en": "Rahu in the 3rd house ignites extraordinary courage and daring communication skills. Success in media, technology, and digital platforms comes naturally during this transit. Siblings may have unconventional lives or you connect with step-siblings or adopted family.",
                "hi": "राहु तीसरे भाव में असाधारण साहस और दुस्साहसी संवाद कौशल प्रज्वलित करता है। मीडिया, प्रौद्योगिकी और डिजिटल प्लेटफॉर्म में सफलता इस गोचर के दौरान स्वाभाविक रूप से आती है। भाई-बहनों का जीवन अपरंपरागत हो सकता है या आप सौतेले भाई-बहनों से जुड़ते हैं।"
            },
            "love": {
                "en": "Flirtatious and bold messaging creates exciting romantic connections, especially through social media or dating apps. Short romantic getaways bring intense but possibly fleeting experiences. Express your feelings courageously but avoid manipulation through words.",
                "hi": "छेड़खानी भरे और साहसिक संदेश रोमांचक रोमांटिक संबंध बनाते हैं, विशेषकर सोशल मीडिया या डेटिंग ऐप्स के माध्यम से। छोटी रोमांटिक यात्राएं तीव्र लेकिन संभवतः क्षणभंगुर अनुभव लाती हैं। अपनी भावनाओं को साहसपूर्वक व्यक्त करें लेकिन शब्दों से छलना से बचें।"
            },
            "career": {
                "en": "Digital marketing, content creation, journalism, and tech entrepreneurship thrive powerfully. Your fearless approach to business communication opens doors that were previously shut. Short business trips, especially abroad, yield disproportionate returns.",
                "hi": "डिजिटल मार्केटिंग, कंटेंट क्रिएशन, पत्रकारिता और टेक उद्यमशीलता शक्तिशाली रूप से फलती-फूलती है। व्यापारिक संवाद में आपका निर्भीक दृष्टिकोण उन दरवाजों को खोलता है जो पहले बंद थे। छोटी व्यापारिक यात्राएं, विशेषकर विदेश में, असमान रूप से अधिक लाभ देती हैं।"
            },
            "finance": {
                "en": "Income through writing, blogging, social media, or tech platforms increases significantly. Siblings may contribute to or complicate your financial situation. Invest in communication tools, gadgets, and digital infrastructure for long-term gains.",
                "hi": "लेखन, ब्लॉगिंग, सोशल मीडिया या टेक प्लेटफॉर्म के माध्यम से आय में उल्लेखनीय वृद्धि होती है। भाई-बहन आपकी वित्तीय स्थिति में योगदान या जटिलता ला सकते हैं। दीर्घकालिक लाभ के लिए संवाद उपकरणों, गैजेट्स और डिजिटल बुनियादी ढांचे में निवेश करें।"
            },
            "health": {
                "en": "Nervous system overstimulation from excessive screen time or information overload is the primary concern. Arms, hands, and shoulders may develop repetitive strain issues. Practice digital detox routines and breathing exercises to maintain equilibrium.",
                "hi": "अत्यधिक स्क्रीन समय या सूचना अधिभार से तंत्रिका तंत्र की अतिउत्तेजना प्राथमिक चिंता है। भुजाओं, हाथों और कंधों में दोहरावदार तनाव की समस्या विकसित हो सकती है। संतुलन बनाए रखने के लिए डिजिटल डिटॉक्स दिनचर्या और श्वास व्यायाम का अभ्यास करें।"
            },
        },
        4: {
            "general": {
                "en": "Rahu in the 4th house creates restlessness in domestic life and a constant desire for bigger or better living spaces. Foreign property acquisition or relocation to a distant place is strongly indicated. Mother's health may fluctuate or her influence takes an unconventional turn.",
                "hi": "राहु चौथे भाव में घरेलू जीवन में बेचैनी और बड़े या बेहतर रहने के स्थान की निरंतर इच्छा उत्पन्न करता है। विदेशी संपत्ति अधिग्रहण या दूर स्थान पर स्थानांतरण दृढ़ता से संकेतित है। माता के स्वास्थ्य में उतार-चढ़ाव हो सकता है या उनका प्रभाव अपरंपरागत मोड़ लेता है।"
            },
            "love": {
                "en": "Home-based romance carries an element of excitement mixed with instability. You may desire a partner who brings foreign or exotic energy into your domestic life. Creating emotional security requires conscious effort against Rahu's restless nature.",
                "hi": "घर-आधारित रोमांस में उत्तेजना का तत्व अस्थिरता के साथ मिला होता है। आप ऐसे साथी की इच्छा कर सकते हैं जो आपके घरेलू जीवन में विदेशी या विलक्षण ऊर्जा लाए। भावनात्मक सुरक्षा बनाने के लिए राहु की बेचैन प्रकृति के विरुद्ध सचेत प्रयास आवश्यक है।"
            },
            "career": {
                "en": "Real estate, automobile, interior design, and hospitality industries offer unusual success paths. Working from home or remote positions with international companies suits this transit perfectly. Property dealings may involve complex legal matters requiring expert guidance.",
                "hi": "रियल एस्टेट, ऑटोमोबाइल, इंटीरियर डिज़ाइन और आतिथ्य उद्योग असामान्य सफलता मार्ग प्रदान करते हैं। घर से काम करना या अंतरराष्ट्रीय कंपनियों के साथ दूरस्थ पद इस गोचर के लिए पूरी तरह उपयुक्त हैं। संपत्ति के सौदों में जटिल कानूनी मामले शामिल हो सकते हैं जिनमें विशेषज्ञ मार्गदर्शन आवश्यक है।"
            },
            "finance": {
                "en": "Luxury vehicle purchases, high-end property investments, or home automation spending increases. Real estate gains are possible but involve hidden complications or title disputes. Insure all major assets against unexpected loss or damage.",
                "hi": "लक्जरी वाहन खरीद, उच्च श्रेणी के संपत्ति निवेश या घरेलू स्वचालन पर खर्च बढ़ता है। रियल एस्टेट से लाभ संभव है लेकिन इसमें छिपी जटिलताएं या स्वामित्व विवाद शामिल हैं। अप्रत्याशित हानि या क्षति के विरुद्ध सभी प्रमुख संपत्तियों का बीमा करें।"
            },
            "health": {
                "en": "Chest congestion, heart palpitations, and anxiety attacks may surface from domestic stress. Sleep disturbances and recurring nightmares indicate subconscious unrest. Vastu corrections and creating a clean, organized home environment support mental health.",
                "hi": "घरेलू तनाव से सीने में जकड़न, हृदय की धड़कन बढ़ना और चिंता के दौरे सतह पर आ सकते हैं। नींद में व्यवधान और आवर्ती बुरे सपने अवचेतन अशांति को दर्शाते हैं। वास्तु सुधार और एक स्वच्छ, व्यवस्थित घरेलू वातावरण बनाना मानसिक स्वास्थ्य का समर्थन करता है।"
            },
        },
        5: {
            "general": {
                "en": "Rahu in the 5th house brings intense creativity combined with risky speculative tendencies. Romance takes an unconventional, dramatic, and often secretive turn. Children may exhibit extraordinary talents or present unusual challenges that require non-traditional approaches.",
                "hi": "राहु पांचवें भाव में जोखिम भरी सट्टा प्रवृत्तियों के साथ तीव्र रचनात्मकता लाता है। रोमांस अपरंपरागत, नाटकीय और अक्सर गुप्त मोड़ लेता है। बच्चे असाधारण प्रतिभा प्रदर्शित कर सकते हैं या असामान्य चुनौतियां प्रस्तुत कर सकते हैं जिनमें गैर-पारंपरिक दृष्टिकोण आवश्यक है।"
            },
            "love": {
                "en": "Forbidden or taboo romantic attractions gain powerful momentum during this transit. Love affairs with people from vastly different backgrounds or social stations are likely. The intoxication of romance must be balanced with realistic expectations to avoid heartbreak.",
                "hi": "इस गोचर के दौरान वर्जित या निषिद्ध रोमांटिक आकर्षण शक्तिशाली गति प्राप्त करते हैं। बहुत भिन्न पृष्ठभूमि या सामाजिक स्थिति के लोगों के साथ प्रेम संबंध संभावित हैं। दिल टूटने से बचने के लिए रोमांस के नशे को यथार्थवादी अपेक्षाओं के साथ संतुलित करना आवश्यक है।"
            },
            "career": {
                "en": "Entertainment, film, gaming, stock trading, and creative technology fields offer breakthrough opportunities. Innovative ideas that seem outlandish may actually succeed spectacularly. Academic pursuits in cutting-edge or unconventional subjects bring recognition.",
                "hi": "मनोरंजन, फिल्म, गेमिंग, शेयर ट्रेडिंग और रचनात्मक प्रौद्योगिकी क्षेत्र सफलता के अवसर प्रदान करते हैं। जो नवीन विचार विचित्र लगते हैं वे वास्तव में शानदार रूप से सफल हो सकते हैं। अत्याधुनिक या अपरंपरागत विषयों में शैक्षणिक अध्ययन मान्यता लाता है।"
            },
            "finance": {
                "en": "Stock market and speculative investments can bring sudden windfall gains or devastating losses. Gambling tendencies must be strictly controlled during this transit. Children's education or creative ventures may require significant financial investment.",
                "hi": "शेयर बाजार और सट्टा निवेश अचानक अप्रत्याशित लाभ या विनाशकारी हानि ला सकता है। इस गोचर के दौरान जुए की प्रवृत्तियों को कड़ाई से नियंत्रित करना आवश्यक है। बच्चों की शिक्षा या रचनात्मक उपक्रमों के लिए महत्वपूर्ण वित्तीय निवेश आवश्यक हो सकता है।"
            },
            "health": {
                "en": "Stomach disorders, digestive irregularities, and issues related to the solar plexus area need monitoring. Pregnancy-related complications require expert medical oversight. Avoid addictive substances as Rahu in the 5th house amplifies dependency tendencies.",
                "hi": "पेट के विकार, पाचन अनियमितताएं और सौर जाल क्षेत्र से संबंधित समस्याओं की निगरानी आवश्यक है। गर्भावस्था संबंधित जटिलताओं में विशेषज्ञ चिकित्सा देखरेख आवश्यक है। नशीले पदार्थों से बचें क्योंकि पांचवें भाव में राहु निर्भरता प्रवृत्तियों को बढ़ाता है।"
            },
        },
        6: {
            "general": {
                "en": "Rahu in the 6th house grants remarkable power to defeat enemies and overcome obstacles through cunning strategy. Legal battles are won using unconventional tactics and unexpected alliances. This is one of Rahu's strongest placements for worldly success through competition.",
                "hi": "राहु छठे भाव में चतुर रणनीति से शत्रुओं को पराजित करने और बाधाओं पर विजय पाने की उल्लेखनीय शक्ति प्रदान करता है। अपरंपरागत रणनीतियों और अप्रत्याशित गठबंधनों से कानूनी लड़ाइयां जीती जाती हैं। प्रतिस्पर्धा के माध्यम से सांसारिक सफलता के लिए यह राहु की सबसे मजबूत स्थितियों में से एक है।"
            },
            "love": {
                "en": "Serving your partner selflessly during their difficult times builds a bond that competitors cannot break. Health challenges of loved ones bring you closer through shared struggle. Romance may develop with colleagues or through workplace connections.",
                "hi": "साथी के कठिन समय में निस्वार्थ सेवा ऐसा बंधन बनाती है जो प्रतिद्वंद्वी तोड़ नहीं सकते। प्रियजनों की स्वास्थ्य चुनौतियां साझा संघर्ष के माध्यम से आपको करीब लाती हैं। सहकर्मियों के साथ या कार्यस्थल संपर्कों के माध्यम से रोमांस विकसित हो सकता है।"
            },
            "career": {
                "en": "Healthcare, alternative medicine, technology solutions for health, legal services, and competitive industries offer peak performance. You outmaneuver workplace rivals with strategic brilliance during this transit. Foreign collaborations in service industries bring extraordinary results.",
                "hi": "स्वास्थ्य सेवा, वैकल्पिक चिकित्सा, स्वास्थ्य के लिए प्रौद्योगिकी समाधान, कानूनी सेवाएं और प्रतिस्पर्धी उद्योग चरम प्रदर्शन प्रदान करते हैं। इस गोचर में आप रणनीतिक प्रतिभा से कार्यस्थल प्रतिद्वंद्वियों को मात देते हैं। सेवा उद्योगों में विदेशी सहयोग असाधारण परिणाम लाता है।"
            },
            "finance": {
                "en": "Income from competitive professions, legal settlements, or insurance claims brings unexpected gains. Medical expenses may arise through unusual health conditions but are resolved favorably. Lending money to others during this transit carries high risk of non-recovery.",
                "hi": "प्रतिस्पर्धी व्यवसायों, कानूनी समझौतों या बीमा दावों से आय अप्रत्याशित लाभ लाती है। असामान्य स्वास्थ्य स्थितियों से चिकित्सा खर्च उत्पन्न हो सकता है लेकिन अनुकूल रूप से हल होता है। इस गोचर में दूसरों को धन उधार देने में वसूली न होने का उच्च जोखिम है।"
            },
            "health": {
                "en": "Mysterious illnesses may require diagnosis from multiple specialists before being identified. Alternative healing modalities — acupuncture, Ayurvedic detox, energy healing — work particularly well. Intestinal parasites, food poisoning from exotic foods, and immune system disruptions need vigilance.",
                "hi": "रहस्यमयी बीमारियों की पहचान के लिए कई विशेषज्ञों से निदान आवश्यक हो सकता है। वैकल्पिक उपचार पद्धतियां — एक्यूपंक्चर, आयुर्वेदिक डिटॉक्स, ऊर्जा चिकित्सा — विशेष रूप से अच्छा काम करती हैं। आंतों के परजीवी, विदेशी खाद्य पदार्थों से विषाक्तता और प्रतिरक्षा प्रणाली में व्यवधान पर सतर्कता आवश्यक है।"
            },
        },
        7: {
            "general": {
                "en": "Rahu in the 7th house brings intense desire for unconventional partnerships and foreign connections. Marriage or business partnerships may involve people from different cultural, religious, or social backgrounds. Contractual matters require extreme scrutiny as deception from partners is possible.",
                "hi": "राहु सातवें भाव में अपरंपरागत साझेदारी और विदेशी संबंधों के लिए तीव्र इच्छा लाता है। विवाह या व्यावसायिक साझेदारी में भिन्न सांस्कृतिक, धार्मिक या सामाजिक पृष्ठभूमि के लोग शामिल हो सकते हैं। अनुबंध मामलों में अत्यधिक सावधानी आवश्यक है क्योंकि साझेदारों से छल संभव है।"
            },
            "love": {
                "en": "A foreign, exotic, or unconventional spouse enters your life with magnetic attraction. The relationship carries intense passion but also potential for misunderstanding due to cultural differences. Transparency and clear communication are essential to avoid deception or disappointment.",
                "hi": "विदेशी, विलक्षण या अपरंपरागत जीवनसाथी चुंबकीय आकर्षण के साथ आपके जीवन में प्रवेश करता है। संबंध में तीव्र जुनून है लेकिन सांस्कृतिक भिन्नताओं के कारण गलतफहमी की भी संभावना है। छल या निराशा से बचने के लिए पारदर्शिता और स्पष्ट संवाद आवश्यक है।"
            },
            "career": {
                "en": "International business partnerships, import-export, diplomatic services, and cross-cultural consulting flourish. Joint ventures with foreign partners can bring breakthrough success but require airtight legal agreements. Public-facing roles gain unusual popularity.",
                "hi": "अंतरराष्ट्रीय व्यावसायिक साझेदारी, आयात-निर्यात, कूटनीतिक सेवाएं और अंतर-सांस्कृतिक परामर्श फलते-फूलते हैं। विदेशी भागीदारों के साथ संयुक्त उपक्रम सफलता ला सकते हैं लेकिन कड़े कानूनी समझौतों की आवश्यकता है। जनता के सामने वाली भूमिकाओं में असामान्य लोकप्रियता मिलती है।"
            },
            "finance": {
                "en": "Joint finances with partners bring both extraordinary opportunities and hidden risks. Foreign trade and international deals can yield significant profits. Pre-nuptial or partnership agreements with clear financial terms protect against future disputes.",
                "hi": "साझेदारों के साथ संयुक्त वित्त असाधारण अवसर और छिपे जोखिम दोनों लाता है। विदेशी व्यापार और अंतरराष्ट्रीय सौदे महत्वपूर्ण लाभ दे सकते हैं। भविष्य के विवादों से सुरक्षा के लिए स्पष्ट वित्तीय शर्तों के साथ विवाह-पूर्व या साझेदारी समझौते आवश्यक हैं।"
            },
            "health": {
                "en": "Reproductive system and kidney health require careful monitoring during this transit. Partner's health issues may create shared stress affecting your wellbeing. Sexually transmitted infections or allergic reactions from unfamiliar environments need precaution.",
                "hi": "इस गोचर के दौरान प्रजनन प्रणाली और गुर्दे के स्वास्थ्य की सावधानीपूर्वक निगरानी आवश्यक है। साथी की स्वास्थ्य समस्याएं आपकी भलाई को प्रभावित करने वाला साझा तनाव बना सकती हैं। यौन संचारित संक्रमण या अपरिचित वातावरण से एलर्जी प्रतिक्रियाओं में सावधानी आवश्यक है।"
            },
        },
        8: {
            "general": {
                "en": "Rahu in the 8th house plunges you into the deepest mysteries of life — occult knowledge, tantra, and hidden dimensions of existence. Sudden inheritance or unexpected insurance payouts may arrive with complications. This transit transforms your understanding of power, death, and rebirth.",
                "hi": "राहु आठवें भाव में आपको जीवन के गहनतम रहस्यों में डुबोता है — तांत्रिक ज्ञान, तंत्र और अस्तित्व के छिपे आयाम। अचानक विरासत या अप्रत्याशित बीमा भुगतान जटिलताओं के साथ आ सकता है। यह गोचर शक्ति, मृत्यु और पुनर्जन्म की आपकी समझ को रूपांतरित करता है।"
            },
            "love": {
                "en": "Deeply transformative and intensely passionate relationships consume your emotional world. Secrets in love come to the surface demanding honest reckoning. Tantric or deeply spiritual intimacy replaces superficial romantic connections.",
                "hi": "गहन परिवर्तनकारी और अत्यंत जुनूनी संबंध आपकी भावनात्मक दुनिया को अपने में समा लेते हैं। प्रेम में रहस्य सतह पर आते हैं जो ईमानदार समझौते की मांग करते हैं। तांत्रिक या गहन आध्यात्मिक अंतरंगता सतही रोमांटिक संबंधों का स्थान लेती है।"
            },
            "career": {
                "en": "Research, forensic science, cybersecurity, insurance, occult sciences, and crisis management roles bring unexpected success. Hidden information or insider knowledge becomes a powerful professional tool. Careers involving transformation, healing, or investigation thrive.",
                "hi": "अनुसंधान, फोरेंसिक विज्ञान, साइबर सुरक्षा, बीमा, तांत्रिक विज्ञान और संकट प्रबंधन भूमिकाओं में अप्रत्याशित सफलता मिलती है। छिपी जानकारी या अंदरूनी ज्ञान शक्तिशाली पेशेवर उपकरण बन जाता है। परिवर्तन, उपचार या जांच से जुड़े करियर फलते-फूलते हैं।"
            },
            "finance": {
                "en": "Sudden inheritance, insurance claims, or windfall from hidden sources can dramatically change your financial landscape. Tax complications, joint account disputes, or financial fraud risks require vigilance. Occult or underground financial opportunities should be approached with extreme caution.",
                "hi": "अचानक विरासत, बीमा दावे या छिपे स्रोतों से अप्रत्याशित धन आपके वित्तीय परिदृश्य को नाटकीय रूप से बदल सकता है। कर जटिलताएं, संयुक्त खाता विवाद या वित्तीय धोखाधड़ी के जोखिमों में सतर्कता आवश्यक है। तांत्रिक या भूमिगत वित्तीय अवसरों को अत्यधिक सावधानी से अपनाना चाहिए।"
            },
            "health": {
                "en": "Chronic, hidden, or hard-to-diagnose diseases may surface requiring specialized investigation. Reproductive and excretory system disorders need expert attention. Avoid risky physical activities, occult experiments without guidance, and exposure to toxic environments.",
                "hi": "पुरानी, छिपी या कठिन-निदान बीमारियां सतह पर आ सकती हैं जिनमें विशेष जांच आवश्यक है। प्रजनन और उत्सर्जन प्रणाली विकारों में विशेषज्ञ ध्यान आवश्यक है। जोखिम भरी शारीरिक गतिविधियों, मार्गदर्शन के बिना तांत्रिक प्रयोगों और विषैले वातावरण के संपर्क से बचें।"
            },
        },
        9: {
            "general": {
                "en": "Rahu in the 9th house drives an obsessive quest for unconventional spirituality, foreign philosophies, and unorthodox belief systems. Higher education abroad or through non-traditional institutions is strongly favored. Father figures may have complex, unconventional, or foreign connections.",
                "hi": "राहु नौवें भाव में अपरंपरागत आध्यात्मिकता, विदेशी दर्शन और अपरंपरागत विश्वास प्रणालियों की जुनूनी खोज को प्रेरित करता है। विदेश में या गैर-पारंपरिक संस्थानों के माध्यम से उच्च शिक्षा दृढ़ता से अनुकूल है। पिता की आकृतियों के जटिल, अपरंपरागत या विदेशी संबंध हो सकते हैं।"
            },
            "love": {
                "en": "Cross-cultural romance or relationships with spiritual seekers from distant lands bring profound experiences. A guru or mentor may introduce you to your life partner in unexpected ways. Philosophical compatibility matters more than social convention in choosing a partner.",
                "hi": "अंतर-सांस्कृतिक रोमांस या दूर देशों के आध्यात्मिक साधकों के साथ संबंध गहन अनुभव लाते हैं। कोई गुरु या मार्गदर्शक अप्रत्याशित तरीकों से आपको जीवनसाथी से मिलवा सकता है। साथी चुनने में सामाजिक परंपरा से अधिक दार्शनिक अनुकूलता मायने रखती है।"
            },
            "career": {
                "en": "International education, foreign university positions, cross-border law, religious technology, and pilgrimage tourism offer extraordinary career growth. Publishing works on unconventional philosophies gains worldwide attention. Diplomatic or cultural exchange roles open new horizons.",
                "hi": "अंतरराष्ट्रीय शिक्षा, विदेशी विश्वविद्यालय पद, सीमा-पार कानून, धार्मिक प्रौद्योगिकी और तीर्थ पर्यटन असाधारण करियर वृद्धि प्रदान करते हैं। अपरंपरागत दर्शन पर प्रकाशन कार्य विश्वव्यापी ध्यान आकर्षित करता है। कूटनीतिक या सांस्कृतिक विनिमय भूमिकाएं नए क्षितिज खोलती हैं।"
            },
            "finance": {
                "en": "Foreign education investments, international publishing royalties, and cross-border business ventures bring significant returns. Pilgrimage and spiritual tourism spending increases but yields inner wealth. Father's finances may require your support or involve complex international matters.",
                "hi": "विदेशी शिक्षा निवेश, अंतरराष्ट्रीय प्रकाशन रॉयल्टी और सीमा-पार व्यापार उपक्रम महत्वपूर्ण रिटर्न लाते हैं। तीर्थयात्रा और आध्यात्मिक पर्यटन पर खर्च बढ़ता है लेकिन आंतरिक धन प्रदान करता है। पिता के वित्त में आपके समर्थन की आवश्यकता हो सकती है या जटिल अंतरराष्ट्रीय मामले शामिल हो सकते हैं।"
            },
            "health": {
                "en": "Hip joints, thighs, and liver health need attention, especially during long international journeys. Philosophical or spiritual crisis can manifest as physical fatigue and immune suppression. Yogic practices and meditation from authentic traditions provide the best healing.",
                "hi": "कूल्हे के जोड़, जांघ और यकृत स्वास्थ्य पर ध्यान देने की आवश्यकता है, विशेषकर लंबी अंतरराष्ट्रीय यात्राओं के दौरान। दार्शनिक या आध्यात्मिक संकट शारीरिक थकान और प्रतिरक्षा दमन के रूप में प्रकट हो सकता है। प्रामाणिक परंपराओं से योग अभ्यास और ध्यान सर्वोत्तम उपचार प्रदान करते हैं।"
            },
        },
        10: {
            "general": {
                "en": "Rahu in the 10th house catapults you to sudden fame, power, and public prominence through unconventional means. Political ambitions, technological leadership, and media-driven careers reach their zenith. Authority comes quickly but maintaining it requires navigating complex power dynamics.",
                "hi": "राहु दसवें भाव में आपको अपरंपरागत माध्यमों से अचानक प्रसिद्धि, शक्ति और सार्वजनिक प्रमुखता की ओर ले जाता है। राजनीतिक महत्वाकांक्षाएं, तकनीकी नेतृत्व और मीडिया-संचालित करियर अपने शिखर पर पहुंचते हैं। अधिकार तेजी से आता है लेकिन इसे बनाए रखने के लिए जटिल शक्ति गतिशीलता को नेविगेट करना आवश्यक है।"
            },
            "love": {
                "en": "Your powerful public persona attracts admirers from influential circles. Romance may intertwine with career advancement in ways that require ethical discernment. A partner who supports your ambitious public role becomes an invaluable asset.",
                "hi": "आपका शक्तिशाली सार्वजनिक व्यक्तित्व प्रभावशाली मंडलों से प्रशंसक आकर्षित करता है। रोमांस करियर की प्रगति के साथ ऐसे तरीकों से जुड़ सकता है जिनमें नैतिक विवेक आवश्यक है। आपकी महत्वाकांक्षी सार्वजनिक भूमिका का समर्थन करने वाला साथी अमूल्य संपत्ति बन जाता है।"
            },
            "career": {
                "en": "This is Rahu's most powerful career transit — rapid rise through technology, politics, media, or multinational corporations. Foreign assignments and international leadership roles bring extraordinary recognition. Maintain ethical standards as shortcuts to power carry severe long-term consequences.",
                "hi": "यह राहु का सबसे शक्तिशाली करियर गोचर है — प्रौद्योगिकी, राजनीति, मीडिया या बहुराष्ट्रीय निगमों के माध्यम से तीव्र उत्थान। विदेशी कार्यभार और अंतरराष्ट्रीय नेतृत्व भूमिकाएं असाधारण मान्यता लाती हैं। नैतिक मानक बनाए रखें क्योंकि शक्ति के शॉर्टकट गंभीर दीर्घकालिक परिणाम लाते हैं।"
            },
            "finance": {
                "en": "Income from positions of authority, technology ventures, or political connections increases dramatically. Stock options, corporate bonuses, and foreign assignments bring substantial wealth. Guard against financial scandals or tax irregularities that could accompany rapid wealth accumulation.",
                "hi": "अधिकार पदों, प्रौद्योगिकी उपक्रमों या राजनीतिक संबंधों से आय नाटकीय रूप से बढ़ती है। स्टॉक विकल्प, कॉर्पोरेट बोनस और विदेशी कार्यभार पर्याप्त धन लाते हैं। तीव्र धन संचय के साथ आने वाले वित्तीय घोटालों या कर अनियमितताओं से सावधान रहें।"
            },
            "health": {
                "en": "Knee joints, skeletal system, and skin conditions require attention under career-related stress. Public pressure and the weight of responsibility can trigger anxiety disorders. Regular health checkups and stress management routines are non-negotiable at this level of activity.",
                "hi": "करियर संबंधित तनाव में घुटने के जोड़, कंकाल प्रणाली और त्वचा की स्थितियों पर ध्यान देने की आवश्यकता है। सार्वजनिक दबाव और जिम्मेदारी का भार चिंता विकारों को ट्रिगर कर सकता है। गतिविधि के इस स्तर पर नियमित स्वास्थ्य जांच और तनाव प्रबंधन दिनचर्या अपरिहार्य हैं।"
            },
        },
        11: {
            "general": {
                "en": "Rahu in the 11th house delivers massive gains through technology-driven networks, influential contacts, and unconventional income streams. Social media influence, tech communities, and international networking bring extraordinary opportunities. Friends from foreign lands or unusual backgrounds play pivotal roles in your success.",
                "hi": "राहु ग्यारहवें भाव में प्रौद्योगिकी-संचालित नेटवर्क, प्रभावशाली संपर्कों और अपरंपरागत आय धाराओं के माध्यम से भारी लाभ प्रदान करता है। सोशल मीडिया प्रभाव, तकनीकी समुदाय और अंतरराष्ट्रीय नेटवर्किंग असाधारण अवसर लाते हैं। विदेशी या असामान्य पृष्ठभूमि के मित्र आपकी सफलता में महत्वपूर्ण भूमिका निभाते हैं।"
            },
            "love": {
                "en": "Social gatherings and tech-savvy communities introduce exciting romantic prospects. Friends may become lovers or play matchmaker roles in unexpected ways. Large social circles provide abundant romantic options but choosing wisely requires discernment beyond surface attraction.",
                "hi": "सामाजिक समारोह और तकनीक-प्रेमी समुदाय रोमांचक रोमांटिक संभावनाएं प्रस्तुत करते हैं। मित्र प्रेमी बन सकते हैं या अप्रत्याशित तरीकों से मैचमेकर की भूमिका निभा सकते हैं। बड़े सामाजिक मंडल प्रचुर रोमांटिक विकल्प प्रदान करते हैं लेकिन बुद्धिमानी से चुनने के लिए सतही आकर्षण से परे विवेक आवश्यक है।"
            },
            "career": {
                "en": "Freelancing, tech startups, social media entrepreneurship, and network-based businesses yield exceptional returns. Elder siblings or mentors in tech industries open lucrative doors. Crowdfunding, affiliate marketing, and platform-based income models thrive spectacularly.",
                "hi": "फ्रीलांसिंग, टेक स्टार्टअप, सोशल मीडिया उद्यमशीलता और नेटवर्क-आधारित व्यवसाय असाधारण रिटर्न देते हैं। तकनीकी उद्योगों में बड़े भाई-बहन या मार्गदर्शक आकर्षक अवसरों के द्वार खोलते हैं। क्राउडफंडिंग, एफिलिएट मार्केटिंग और प्लेटफॉर्म-आधारित आय मॉडल शानदार रूप से फलते-फूलते हैं।"
            },
            "finance": {
                "en": "This is Rahu's most favorable house for financial gains — income through technology, networks, and international connections multiplies. Cryptocurrency, tech stocks, and platform economy investments can yield extraordinary returns. However, unreliable friends may lead to financial betrayal if trust is given blindly.",
                "hi": "यह वित्तीय लाभ के लिए राहु का सबसे अनुकूल भाव है — प्रौद्योगिकी, नेटवर्क और अंतरराष्ट्रीय संबंधों के माध्यम से आय बहुगुणित होती है। क्रिप्टोकरेंसी, तकनीकी शेयर और प्लेटफॉर्म अर्थव्यवस्था निवेश असाधारण रिटर्न दे सकते हैं। हालांकि, अविश्वसनीय मित्र अंधा विश्वास करने पर वित्तीय विश्वासघात कर सकते हैं।"
            },
            "health": {
                "en": "Circulation issues in lower legs, varicose veins, and ankle injuries need preventive attention. Social overcommitment and networking fatigue can drain vitality. Set boundaries on social engagements and prioritize restorative solitude periodically.",
                "hi": "पैरों के निचले हिस्से में रक्त संचार समस्याएं, वैरिकाज़ वेन्स और टखने की चोटों पर निवारक ध्यान आवश्यक है। सामाजिक अति-प्रतिबद्धता और नेटवर्किंग थकान जीवन शक्ति को क्षीण कर सकती है। सामाजिक कार्यक्रमों पर सीमाएं निर्धारित करें और समय-समय पर पुनर्स्थापनात्मक एकांत को प्राथमिकता दें।"
            },
        },
        12: {
            "general": {
                "en": "Rahu in the 12th house drives an obsessive pull toward foreign lands, spiritual awakening through unconventional paths, and hidden expenditures. Foreign residence or extended stays abroad become defining life experiences. Sleep disorders, vivid dreams, and subconscious patterns demand conscious attention.",
                "hi": "राहु बारहवें भाव में विदेशी भूमि की ओर जुनूनी आकर्षण, अपरंपरागत मार्गों से आध्यात्मिक जागृति और छिपे व्यय को प्रेरित करता है। विदेशी निवास या विदेश में विस्तारित प्रवास जीवन के निर्णायक अनुभव बन जाते हैं। नींद विकार, ज्वलंत सपने और अवचेतन पैटर्न सचेत ध्यान की मांग करते हैं।"
            },
            "love": {
                "en": "Secret or long-distance relationships carry an intoxicating allure during this transit. Romantic connections formed in foreign lands or spiritual settings carry deep karmic significance. The desire for emotional escape may lead to idealized but impractical romantic fantasies.",
                "hi": "इस गोचर के दौरान गुप्त या लंबी दूरी के संबंधों में मादक आकर्षण होता है। विदेशी भूमि या आध्यात्मिक परिवेश में बने रोमांटिक संबंध गहरे कार्मिक महत्व रखते हैं। भावनात्मक पलायन की इच्छा आदर्शीकृत लेकिन अव्यावहारिक रोमांटिक कल्पनाओं की ओर ले जा सकती है।"
            },
            "career": {
                "en": "Careers in foreign countries, multinational organizations, hospitals, spiritual retreats, or behind-the-scenes roles bring fulfillment. Virtual work with international teams suits this placement perfectly. Immigration consulting, foreign diplomacy, or international NGO work aligns with Rahu's 12th house energy.",
                "hi": "विदेशों, बहुराष्ट्रीय संगठनों, अस्पतालों, आध्यात्मिक आश्रमों या पर्दे के पीछे की भूमिकाओं में करियर संतुष्टि लाता है। अंतरराष्ट्रीय टीमों के साथ वर्चुअल कार्य इस स्थिति के लिए बिल्कुल उपयुक्त है। इमिग्रेशन परामर्श, विदेशी कूटनीति या अंतरराष्ट्रीय एनजीओ कार्य राहु की बारहवें भाव की ऊर्जा से मेल खाता है।"
            },
            "finance": {
                "en": "Expenses on foreign travel, visa processing, international education, and spiritual retreats increase significantly. Hidden financial drains — subscriptions, overseas accounts, or untracked spending — need auditing. Income from foreign sources or online global platforms can offset the increased expenditure.",
                "hi": "विदेश यात्रा, वीज़ा प्रसंस्करण, अंतरराष्ट्रीय शिक्षा और आध्यात्मिक आश्रमों पर खर्च काफी बढ़ता है। छिपे वित्तीय नुकसान — सब्सक्रिप्शन, विदेशी खाते या अनट्रैक्ड खर्च — की ऑडिटिंग आवश्यक है। विदेशी स्रोतों या ऑनलाइन वैश्विक प्लेटफॉर्म से आय बढ़े हुए व्यय की भरपाई कर सकती है।"
            },
            "health": {
                "en": "Insomnia, sleep apnea, and disturbed sleep cycles are the hallmark health concerns of this transit. Feet problems, fluid retention, and immune system irregularities require monitoring. Meditation, yoga nidra, and grounding practices before sleep provide significant relief.",
                "hi": "अनिद्रा, स्लीप एपनिया और बाधित नींद चक्र इस गोचर की प्रमुख स्वास्थ्य चिंताएं हैं। पैरों की समस्याएं, द्रव प्रतिधारण और प्रतिरक्षा प्रणाली अनियमितताओं की निगरानी आवश्यक है। ध्यान, योग निद्रा और सोने से पहले ग्राउंडिंग अभ्यास महत्वपूर्ण राहत प्रदान करते हैं।"
            },
        },
    },
    # =========================================================================
    # KETU (South Node) — Shadow planet of liberation, detachment, spirituality,
    # past-life karma, sudden events. Always retrograde.
    # Karaka of moksha, occult, maternal grandfather, sudden losses leading
    # to spiritual growth.
    # =========================================================================
    "Ketu": {
        1: {
            "general": {
                "en": "Ketu transiting your 1st house creates a deeply spiritual, detached, and introspective personality. You appear mysterious and otherworldly to those around you, often seeming disinterested in worldly affairs. Past-life talents and intuitive abilities surface naturally during this period.",
                "hi": "केतु का आपके प्रथम भाव में गोचर गहन आध्यात्मिक, विरक्त और आत्मनिरीक्षणशील व्यक्तित्व बनाता है। आप अपने आसपास के लोगों को रहस्यमय और अलौकिक दिखते हैं, अक्सर सांसारिक मामलों में अरुचि प्रकट करते हैं। पूर्वजन्म की प्रतिभाएं और अंतर्ज्ञानी क्षमताएं इस अवधि में स्वाभाविक रूप से सतह पर आती हैं।"
            },
            "love": {
                "en": "A detached approach to romance may confuse partners who seek emotional intensity. Past-life karmic connections with lovers create instant but unexplainable bonds. True love during this transit requires accepting a partner who values spiritual connection over material display.",
                "hi": "रोमांस के प्रति विरक्त दृष्टिकोण उन साथियों को भ्रमित कर सकता है जो भावनात्मक तीव्रता चाहते हैं। प्रेमियों के साथ पूर्वजन्म के कार्मिक संबंध तत्काल लेकिन अव्याख्येय बंधन बनाते हैं। इस गोचर में सच्चा प्रेम ऐसे साथी को स्वीकार करना है जो भौतिक प्रदर्शन से अधिक आध्यात्मिक जुड़ाव को महत्व देता है।"
            },
            "career": {
                "en": "Careers in spirituality, metaphysics, healing arts, and research flourish as worldly ambition naturally recedes. Your intuitive problem-solving abilities impress colleagues who cannot understand your methods. Avoid positions requiring aggressive self-promotion as Ketu diminishes the ego-driven self.",
                "hi": "आध्यात्मिकता, तत्वमीमांसा, उपचार कला और अनुसंधान में करियर फलता-फूलता है क्योंकि सांसारिक महत्वाकांक्षा स्वाभाविक रूप से कम होती है। आपकी अंतर्ज्ञानी समस्या-समाधान क्षमताएं सहकर्मियों को प्रभावित करती हैं जो आपकी विधियां नहीं समझ पाते। आक्रामक आत्म-प्रचार वाले पदों से बचें क्योंकि केतु अहंकार-चालित स्वत्व को क्षीण करता है।"
            },
            "finance": {
                "en": "Material wealth holds diminishing attraction as spiritual values take precedence. Unexpected financial losses may occur but lead to profound lessons about detachment. Income from healing, spiritual counseling, or research provides modest but meaningful sustenance.",
                "hi": "आध्यात्मिक मूल्यों को प्राथमिकता मिलने से भौतिक धन का आकर्षण कम होता है। अप्रत्याशित वित्तीय हानि हो सकती है लेकिन विरक्ति के बारे में गहन सबक प्रदान करती है। उपचार, आध्यात्मिक परामर्श या अनुसंधान से आय मामूली लेकिन सार्थक जीविका प्रदान करती है।"
            },
            "health": {
                "en": "Unexplained health fluctuations, energy imbalances, and psychosomatic symptoms characterize this transit. Head-related issues, migraines, and neurological sensitivities may arise without clear medical cause. Spiritual practices, pranayama, and energy healing address root causes that conventional medicine may miss.",
                "hi": "अव्याख्येय स्वास्थ्य उतार-चढ़ाव, ऊर्जा असंतुलन और मनोदैहिक लक्षण इस गोचर की विशेषता हैं। सिर संबंधित समस्याएं, माइग्रेन और तंत्रिका संबंधी संवेदनशीलता बिना स्पष्ट चिकित्सा कारण के उत्पन्न हो सकती हैं। आध्यात्मिक अभ्यास, प्राणायाम और ऊर्जा उपचार उन मूल कारणों को संबोधित करते हैं जो पारंपरिक चिकित्सा से छूट सकते हैं।"
            },
        },
        2: {
            "general": {
                "en": "Ketu in the 2nd house brings detachment from material wealth and family attachments. Speech becomes sparse, cryptic, and spiritually inclined — you speak less but with profound impact. Food preferences shift toward simple, Sattvic, or restricted diets as sensory indulgence loses appeal.",
                "hi": "केतु दूसरे भाव में भौतिक धन और पारिवारिक आसक्तियों से विरक्ति लाता है। वाणी विरल, गूढ़ और आध्यात्मिक झुकाव वाली बन जाती है — आप कम बोलते हैं लेकिन गहन प्रभाव के साथ। इंद्रिय भोग का आकर्षण कम होने पर खाद्य प्राथमिकताएं सरल, सात्त्विक या प्रतिबंधित आहार की ओर बदलती हैं।"
            },
            "love": {
                "en": "Expressing love through words becomes challenging as Ketu restricts verbal emotional expression. Family may feel distant or emotionally unavailable despite your physical presence. Silent acts of devotion and spiritual companionship replace conventional romantic expression.",
                "hi": "केतु मौखिक भावनात्मक अभिव्यक्ति को प्रतिबंधित करने से शब्दों के माध्यम से प्रेम व्यक्त करना चुनौतीपूर्ण हो जाता है। शारीरिक उपस्थिति के बावजूद परिवार दूर या भावनात्मक रूप से अनुपलब्ध महसूस कर सकता है। मौन भक्ति और आध्यात्मिक सहचर्य पारंपरिक रोमांटिक अभिव्यक्ति का स्थान लेते हैं।"
            },
            "career": {
                "en": "Careers requiring deep knowledge, research, or spiritual expertise thrive over those demanding salesmanship. Financial advisory roles shift from aggressive wealth-building to ethical, value-based guidance. Teaching ancient wisdom, linguistics, or family counseling aligns with this transit's energy.",
                "hi": "गहन ज्ञान, अनुसंधान या आध्यात्मिक विशेषज्ञता वाले करियर बिक्रीकौशल की मांग करने वालों से बेहतर फलते हैं। वित्तीय सलाहकार भूमिकाएं आक्रामक धन-निर्माण से नैतिक, मूल्य-आधारित मार्गदर्शन की ओर बदलती हैं। प्राचीन ज्ञान, भाषाविज्ञान या पारिवारिक परामर्श का शिक्षण इस गोचर की ऊर्जा से मेल खाता है।"
            },
            "finance": {
                "en": "Sudden, unexpected financial losses teach powerful lessons about the impermanence of wealth. Family inheritance may dissolve or get distributed in unexpected ways. Savings accumulate slowly through austere living rather than aggressive earning.",
                "hi": "अचानक, अप्रत्याशित वित्तीय हानि धन की अनित्यता के बारे में शक्तिशाली सबक सिखाती है। पारिवारिक विरासत विघटित हो सकती है या अप्रत्याशित तरीकों से वितरित हो सकती है। आक्रामक कमाई के बजाय मितव्ययी जीवन के माध्यम से बचत धीरे-धीरे संचित होती है।"
            },
            "health": {
                "en": "Mouth ulcers, dental issues, and throat infections may recur during this transit. Food sensitivities and digestive issues from dietary restrictions need monitoring. Right eye health and facial skin conditions benefit from Ayurvedic remedies and clean eating.",
                "hi": "इस गोचर के दौरान मुंह के छाले, दंत समस्याएं और गले के संक्रमण बार-बार हो सकते हैं। आहार प्रतिबंधों से खाद्य संवेदनशीलता और पाचन समस्याओं की निगरानी आवश्यक है। दाहिनी आंख का स्वास्थ्य और चेहरे की त्वचा की स्थितियां आयुर्वेदिक उपचार और स्वच्छ भोजन से लाभान्वित होती हैं।"
            },
        },
        3: {
            "general": {
                "en": "Ketu in the 3rd house creates an introverted communication style with deep mystical or philosophical undertones. Siblings may feel distant or follow spiritual paths that diverge from family norms. Writing, especially on metaphysical or esoteric subjects, flows with supernatural ease.",
                "hi": "केतु तीसरे भाव में गहन रहस्यमय या दार्शनिक अर्थों के साथ अंतर्मुखी संवाद शैली बनाता है। भाई-बहन दूर महसूस कर सकते हैं या पारिवारिक मानदंडों से भिन्न आध्यात्मिक मार्गों का अनुसरण कर सकते हैं। लेखन, विशेषकर तत्वमीमांसा या गूढ़ विषयों पर, अलौकिक सहजता से प्रवाहित होता है।"
            },
            "love": {
                "en": "Romantic communication becomes subtle, intuitive, and non-verbal during this transit. Love letters or messages carry a poetic, mystical quality that deeply moves the receiver. Short romantic trips to spiritual destinations bring more fulfillment than conventional outings.",
                "hi": "इस गोचर के दौरान रोमांटिक संवाद सूक्ष्म, अंतर्ज्ञानी और अमौखिक बन जाता है। प्रेम पत्र या संदेश काव्यात्मक, रहस्यमय गुणवत्ता रखते हैं जो प्राप्तकर्ता को गहराई से प्रभावित करते हैं। आध्यात्मिक स्थलों की छोटी रोमांटिक यात्राएं पारंपरिक बाहरी गतिविधियों से अधिक संतुष्टि लाती हैं।"
            },
            "career": {
                "en": "Mystical writing, spiritual blogging, metaphysical research, and behind-the-scenes editorial work suit this transit. Courage manifests as inner spiritual strength rather than outward aggression. Short travels for spiritual retreats or meditation workshops bring career-changing insights.",
                "hi": "रहस्यमय लेखन, आध्यात्मिक ब्लॉगिंग, तत्वमीमांसा अनुसंधान और पर्दे के पीछे संपादकीय कार्य इस गोचर के लिए उपयुक्त हैं। साहस बाहरी आक्रामकता के बजाय आंतरिक आध्यात्मिक शक्ति के रूप में प्रकट होता है। आध्यात्मिक आश्रमों या ध्यान कार्यशालाओं के लिए छोटी यात्राएं करियर बदलने वाली अंतर्दृष्टि लाती हैं।"
            },
            "finance": {
                "en": "Income from writing, publishing, or media may fluctuate unpredictably during this transit. Siblings are unlikely to contribute financially and may need your spiritual support instead. Small, consistent investments in knowledge and skills yield better returns than risky ventures.",
                "hi": "इस गोचर के दौरान लेखन, प्रकाशन या मीडिया से आय में अप्रत्याशित उतार-चढ़ाव हो सकता है। भाई-बहन आर्थिक रूप से योगदान देने की संभावना कम है और इसके बजाय आपके आध्यात्मिक समर्थन की आवश्यकता हो सकती है। ज्ञान और कौशल में छोटे, सुसंगत निवेश जोखिम भरे उपक्रमों से बेहतर रिटर्न देते हैं।"
            },
            "health": {
                "en": "Nervous system sensitivity, hand tremors, and shoulder stiffness may appear intermittently. Mental restlessness alternating with deep meditative states is characteristic of this transit. Pranayama, hand mudras, and mindfulness practices stabilize the fluctuating nervous energy.",
                "hi": "तंत्रिका तंत्र संवेदनशीलता, हाथों का कंपन और कंधे की जकड़न रुक-रुक कर प्रकट हो सकती है। गहन ध्यान अवस्थाओं के साथ बदलती मानसिक बेचैनी इस गोचर की विशेषता है। प्राणायाम, हस्त मुद्राएं और माइंडफुलनेस अभ्यास उतार-चढ़ाव वाली तंत्रिका ऊर्जा को स्थिर करते हैं।"
            },
        },
        4: {
            "general": {
                "en": "Ketu in the 4th house brings profound inner peace through detachment from material comforts and worldly possessions. Home becomes a place of meditation and spiritual practice rather than material display. Mother may turn toward spirituality or experience health challenges that deepen your compassion.",
                "hi": "केतु चौथे भाव में भौतिक सुख-सुविधाओं और सांसारिक संपत्तियों से विरक्ति के माध्यम से गहन आंतरिक शांति लाता है। घर भौतिक प्रदर्शन के बजाय ध्यान और आध्यात्मिक अभ्यास का स्थान बन जाता है। माता आध्यात्मिकता की ओर मुड़ सकती हैं या स्वास्थ्य चुनौतियों का अनुभव कर सकती हैं जो आपकी करुणा को गहरा करती हैं।"
            },
            "love": {
                "en": "Domestic romance takes on a quiet, meditative quality that values silence and shared spiritual practices. Emotional detachment from household drama brings peace but may be misread as coldness by family. Creating a sacred space within the home nurtures both partnership and personal growth.",
                "hi": "घरेलू रोमांस शांत, ध्यानपूर्ण गुणवत्ता ले लेता है जो मौन और साझा आध्यात्मिक अभ्यास को महत्व देता है। घरेलू नाटक से भावनात्मक विरक्ति शांति लाती है लेकिन परिवार इसे शीतलता समझ सकता है। घर के भीतर एक पवित्र स्थान बनाना साझेदारी और व्यक्तिगत विकास दोनों का पोषण करता है।"
            },
            "career": {
                "en": "Vastu consulting, spiritual space design, ashram management, and home-based meditation teaching align perfectly. Property matters may require releasing attachment to ancestral holdings. Working from a spiritually aligned home environment enhances productivity and creativity.",
                "hi": "वास्तु परामर्श, आध्यात्मिक स्थान डिज़ाइन, आश्रम प्रबंधन और घर-आधारित ध्यान शिक्षण पूरी तरह मेल खाते हैं। संपत्ति मामलों में पैतृक जोतों से आसक्ति छोड़ने की आवश्यकता हो सकती है। आध्यात्मिक रूप से संरेखित घरेलू वातावरण से काम करना उत्पादकता और रचनात्मकता को बढ़ाता है।"
            },
            "finance": {
                "en": "Property values or real estate investments may decline or require sacrificial letting go. Home maintenance costs decrease as you embrace simplicity over luxury. Ancestral property disputes resolve through spiritual wisdom rather than legal confrontation.",
                "hi": "संपत्ति मूल्य या रियल एस्टेट निवेश में गिरावट हो सकती है या त्यागपूर्ण समर्पण की आवश्यकता हो सकती है। विलासिता के बजाय सरलता अपनाने से घरेलू रखरखाव लागत कम होती है। पैतृक संपत्ति विवाद कानूनी टकराव के बजाय आध्यात्मिक ज्ञान से हल होते हैं।"
            },
            "health": {
                "en": "Chest tightness, irregular heartbeat, and emotional heaviness connected to past memories may surface. Mother's health requires compassionate attention and may involve karmic healing processes. Meditation, heart-opening yoga poses, and spending time in nature bring deep restoration.",
                "hi": "सीने में जकड़न, अनियमित दिल की धड़कन और पिछली स्मृतियों से जुड़ा भावनात्मक भारीपन सतह पर आ सकता है। माता के स्वास्थ्य पर करुणापूर्ण ध्यान आवश्यक है और इसमें कार्मिक उपचार प्रक्रियाएं शामिल हो सकती हैं। ध्यान, हृदय खोलने वाले योग आसन और प्रकृति में समय बिताना गहन पुनर्स्थापना लाता है।"
            },
        },
        5: {
            "general": {
                "en": "Ketu in the 5th house bestows extraordinary intuitive intelligence and past-life merit that manifests as natural wisdom. Romance carries deep karmic undertones with connections that feel destined rather than chosen. Children may be spiritually gifted, unusually mature, or bring lessons about detachment.",
                "hi": "केतु पांचवें भाव में असाधारण अंतर्ज्ञानी बुद्धि और पूर्वजन्म की पुण्य प्रदान करता है जो स्वाभाविक ज्ञान के रूप में प्रकट होता है। रोमांस गहन कार्मिक अर्थ रखता है जहां संबंध चुने हुए के बजाय नियत महसूस होते हैं। बच्चे आध्यात्मिक रूप से प्रतिभाशाली, असामान्य रूप से परिपक्व हो सकते हैं या विरक्ति के सबक लाते हैं।"
            },
            "love": {
                "en": "Romantic connections feel deeply familiar as if continuing from a previous lifetime. Detachment from dramatic love stories allows a serene, spiritually mature partnership to form. Past lovers may reappear bearing karmic messages that require graceful resolution.",
                "hi": "रोमांटिक संबंध गहराई से परिचित महसूस होते हैं जैसे किसी पिछले जन्म से जारी हों। नाटकीय प्रेम कहानियों से विरक्ति एक शांत, आध्यात्मिक रूप से परिपक्व साझेदारी बनने देती है। पूर्व प्रेमी कार्मिक संदेश लेकर पुनः प्रकट हो सकते हैं जिनमें शालीन समाधान आवश्यक है।"
            },
            "career": {
                "en": "Spiritual teaching, intuitive counseling, astrology, past-life regression therapy, and children's spiritual education flourish. Creative work carries a transcendent quality that moves audiences beyond entertainment. Academic research in ancient scriptures or mystical traditions brings recognition.",
                "hi": "आध्यात्मिक शिक्षण, अंतर्ज्ञानी परामर्श, ज्योतिष, पूर्वजन्म प्रतिगमन चिकित्सा और बच्चों की आध्यात्मिक शिक्षा फलती-फूलती है। रचनात्मक कार्य दिव्य गुणवत्ता रखता है जो दर्शकों को मनोरंजन से परे ले जाता है। प्राचीन ग्रंथों या रहस्यमय परंपराओं में शैक्षणिक अनुसंधान मान्यता लाता है।"
            },
            "finance": {
                "en": "Speculative investments lose their appeal as Ketu reduces gambling tendencies. Children's education may follow unconventional or spiritual paths requiring different financial planning. Income from spiritual teaching, healing, or intuitive consulting provides meaningful sustenance.",
                "hi": "केतु जुए की प्रवृत्तियों को कम करने पर सट्टा निवेश का आकर्षण खो जाता है। बच्चों की शिक्षा अपरंपरागत या आध्यात्मिक मार्गों का अनुसरण कर सकती है जिसमें भिन्न वित्तीय योजना आवश्यक है। आध्यात्मिक शिक्षण, उपचार या अंतर्ज्ञानी परामर्श से आय सार्थक जीविका प्रदान करती है।"
            },
            "health": {
                "en": "Stomach and digestive system sensitivities increase with Ketu's purifying energy. Pregnancy may require special spiritual and medical attention with past-life karmic implications. Mantra chanting, meditation, and Sattvic diet address the subtle energy imbalances of this transit.",
                "hi": "केतु की शुद्धिकरण ऊर्जा से पेट और पाचन तंत्र की संवेदनशीलता बढ़ती है। गर्भावस्था में पूर्वजन्म कार्मिक प्रभावों के साथ विशेष आध्यात्मिक और चिकित्सा ध्यान आवश्यक हो सकता है। मंत्र जाप, ध्यान और सात्त्विक आहार इस गोचर के सूक्ष्म ऊर्जा असंतुलन को संबोधित करते हैं।"
            },
        },
        6: {
            "general": {
                "en": "Ketu in the 6th house grants swift, almost supernatural ability to defeat enemies and dissolve obstacles. Diseases resolve quickly through spiritual healing methods that complement medical treatment. This is one of Ketu's best placements — karmic debts related to service and health are rapidly cleared.",
                "hi": "केतु छठे भाव में शत्रुओं को पराजित करने और बाधाओं को विलीन करने की तीव्र, लगभग अलौकिक क्षमता प्रदान करता है। चिकित्सा उपचार के पूरक आध्यात्मिक उपचार विधियों से रोग शीघ्र ठीक होते हैं। यह केतु की सर्वश्रेष्ठ स्थितियों में से एक है — सेवा और स्वास्थ्य से संबंधित कार्मिक ऋण तेजी से मुक्त होते हैं।"
            },
            "love": {
                "en": "Selfless service to your partner during health challenges creates an unbreakable spiritual bond. Enemies of your relationship dissolve as karmic protection surrounds your partnership. Healing together — physically and spiritually — becomes the foundation of lasting love.",
                "hi": "स्वास्थ्य चुनौतियों के दौरान साथी की निस्वार्थ सेवा अटूट आध्यात्मिक बंधन बनाती है। कार्मिक सुरक्षा आपकी साझेदारी को घेरने पर आपके संबंध के शत्रु विलीन हो जाते हैं। शारीरिक और आध्यात्मिक रूप से एक साथ उपचार करना स्थायी प्रेम की नींव बनता है।"
            },
            "career": {
                "en": "Spiritual healing, alternative medicine, veterinary care, and charitable service organizations bring deep professional satisfaction. Workplace conflicts resolve mysteriously as Ketu removes adversaries from your path. Competitive examinations benefit from intuitive preparation and past-life knowledge.",
                "hi": "आध्यात्मिक उपचार, वैकल्पिक चिकित्सा, पशु चिकित्सा और धर्मार्थ सेवा संगठन गहन पेशेवर संतुष्टि लाते हैं। केतु आपके मार्ग से विरोधियों को हटाने पर कार्यस्थल संघर्ष रहस्यमय ढंग से हल होते हैं। प्रतियोगी परीक्षाएं अंतर्ज्ञानी तैयारी और पूर्वजन्म ज्ञान से लाभान्वित होती हैं।"
            },
            "finance": {
                "en": "Debts dissolve faster than expected through karmic grace and unexpected resolutions. Medical expenses may arise but resolve affordably through alternative healing modalities. Charitable donations during this transit bring manifold spiritual and material returns.",
                "hi": "कार्मिक कृपा और अप्रत्याशित समाधानों के माध्यम से ऋण अपेक्षा से तेजी से विलीन होते हैं। चिकित्सा खर्च उत्पन्न हो सकते हैं लेकिन वैकल्पिक उपचार विधियों से किफायती रूप से हल होते हैं। इस गोचर के दौरान दान बहुगुणित आध्यात्मिक और भौतिक लाभ लाता है।"
            },
            "health": {
                "en": "Sudden, unexplained health recoveries are the hallmark of Ketu in the 6th house. Chronic conditions that defied treatment may respond to spiritual healing, fasting, or Ayurvedic detox. Intestinal health improves through simplified diet and elimination of processed foods.",
                "hi": "अचानक, अव्याख्येय स्वास्थ्य सुधार छठे भाव में केतु की विशेषता है। उपचार से अनसुलझी पुरानी स्थितियां आध्यात्मिक उपचार, उपवास या आयुर्वेदिक डिटॉक्स से ठीक हो सकती हैं। सरलीकृत आहार और प्रसंस्कृत खाद्य पदार्थों के उन्मूलन से आंतों का स्वास्थ्य सुधरता है।"
            },
        },
        7: {
            "general": {
                "en": "Ketu in the 7th house brings karmic partnerships that feel destined and carry deep past-life significance. Marriage may involve a spiritually evolved partner who teaches detachment from worldly expectations. Business partnerships dissolve naturally if they lack spiritual alignment or higher purpose.",
                "hi": "केतु सातवें भाव में नियत महसूस होने वाली और गहन पूर्वजन्म महत्व रखने वाली कार्मिक साझेदारी लाता है। विवाह में आध्यात्मिक रूप से विकसित साथी शामिल हो सकता है जो सांसारिक अपेक्षाओं से विरक्ति सिखाता है। आध्यात्मिक संरेखण या उच्च उद्देश्य की कमी वाली व्यावसायिक साझेदारी स्वाभाविक रूप से विघटित होती है।"
            },
            "love": {
                "en": "A partner from a previous lifetime reconnects bringing both comfort and unresolved karma. Spiritual marriage based on soul-level understanding transcends conventional romantic expectations. Detachment does not mean disinterest — it means loving without possessiveness or fear.",
                "hi": "पिछले जन्म का साथी पुनः जुड़ता है जो सुख और अनसुलझे कर्म दोनों लाता है। आत्मा स्तर की समझ पर आधारित आध्यात्मिक विवाह पारंपरिक रोमांटिक अपेक्षाओं से ऊपर उठता है। विरक्ति का अर्थ अरुचि नहीं — इसका अर्थ है अधिकार भावना या भय के बिना प्रेम करना।"
            },
            "career": {
                "en": "Spiritual counseling for couples, meditation retreat partnerships, and karmic healing collaborations flourish. Public-facing roles may diminish as Ketu pulls you toward behind-the-scenes work with partners. Joint ventures succeed only when aligned with dharmic purpose rather than pure profit.",
                "hi": "जोड़ों के लिए आध्यात्मिक परामर्श, ध्यान आश्रम साझेदारी और कार्मिक उपचार सहयोग फलते-फूलते हैं। केतु आपको साझेदारों के साथ पर्दे के पीछे काम की ओर खींचने पर सार्वजनिक भूमिकाएं कम हो सकती हैं। संयुक्त उपक्रम केवल तब सफल होते हैं जब शुद्ध लाभ के बजाय धार्मिक उद्देश्य से संरेखित हों।"
            },
            "finance": {
                "en": "Joint finances may experience unexpected reductions or require sacrificial adjustments. Partner's financial situation may be modest but spiritually enriching. Legal settlements resolve through spiritual wisdom and mediation rather than aggressive litigation.",
                "hi": "संयुक्त वित्त में अप्रत्याशित कमी हो सकती है या त्यागपूर्ण समायोजन की आवश्यकता हो सकती है। साथी की वित्तीय स्थिति मामूली हो सकती है लेकिन आध्यात्मिक रूप से समृद्ध। कानूनी समझौते आक्रामक मुकदमेबाजी के बजाय आध्यात्मिक ज्ञान और मध्यस्थता से हल होते हैं।"
            },
            "health": {
                "en": "Reproductive health and kidney function may fluctuate requiring holistic attention. Partner's health challenges become shared spiritual lessons in compassion and service. Lower back care through yoga and Ayurvedic massage maintains the physical vessel during this karmic transit.",
                "hi": "प्रजनन स्वास्थ्य और गुर्दे की कार्यप्रणाली में उतार-चढ़ाव हो सकता है जिसमें समग्र ध्यान आवश्यक है। साथी की स्वास्थ्य चुनौतियां करुणा और सेवा में साझा आध्यात्मिक सबक बनती हैं। इस कार्मिक गोचर के दौरान योग और आयुर्वेदिक मालिश से पीठ के निचले हिस्से की देखभाल भौतिक शरीर को बनाए रखती है।"
            },
        },
        8: {
            "general": {
                "en": "Ketu in the 8th house unlocks profound mystical insight, deep meditative states, and moksha yoga potential. Sudden transformative experiences strip away illusions and reveal ultimate spiritual truths. Past-life occult knowledge resurfaces naturally, granting abilities in healing, astrology, and tantra.",
                "hi": "केतु आठवें भाव में गहन रहस्यमय अंतर्दृष्टि, गहन ध्यान अवस्थाओं और मोक्ष योग की संभावना को खोलता है। अचानक परिवर्तनकारी अनुभव भ्रम को दूर करते हैं और परम आध्यात्मिक सत्य प्रकट करते हैं। पूर्वजन्म का तांत्रिक ज्ञान स्वाभाविक रूप से पुनः प्रकट होता है, उपचार, ज्योतिष और तंत्र में क्षमताएं प्रदान करता है।"
            },
            "love": {
                "en": "Relationships undergo deep alchemical transformation that burns away superficiality. Tantric intimacy and soul-level connection replace purely physical attraction. Shared near-death experiences, crisis, or spiritual awakening bonds partners at the deepest possible level.",
                "hi": "संबंध गहन रसायनी परिवर्तन से गुजरते हैं जो सतहीपन को जला देता है। तांत्रिक अंतरंगता और आत्मा-स्तर का जुड़ाव शुद्ध शारीरिक आकर्षण का स्थान लेता है। साझा संकट या आध्यात्मिक जागृति साझेदारों को सबसे गहरे संभव स्तर पर बांधती है।"
            },
            "career": {
                "en": "Occult sciences, past-life regression, forensic investigation of ancient mysteries, and transformative healing arts thrive. Research into death, dying, and consciousness studies yields groundbreaking insights. Insurance and estate matters resolve through surrender rather than struggle.",
                "hi": "तांत्रिक विज्ञान, पूर्वजन्म प्रतिगमन, प्राचीन रहस्यों की फोरेंसिक जांच और परिवर्तनकारी उपचार कलाएं फलती-फूलती हैं। मृत्यु और चेतना अध्ययन में अनुसंधान अभूतपूर्व अंतर्दृष्टि प्रदान करता है। बीमा और संपत्ति मामले संघर्ष के बजाय समर्पण से हल होते हैं।"
            },
            "finance": {
                "en": "Sudden loss of inherited wealth or insurance complications teach powerful lessons about impermanence. Hidden financial matters surface and resolve through spiritual acceptance rather than legal battle. Donations to spiritual causes during this transit accelerate karmic debt clearance.",
                "hi": "विरासत में मिली संपत्ति का अचानक नुकसान या बीमा जटिलताएं अनित्यता के बारे में शक्तिशाली सबक सिखाती हैं। छिपे वित्तीय मामले सतह पर आते हैं और कानूनी लड़ाई के बजाय आध्यात्मिक स्वीकृति से हल होते हैं। इस गोचर में आध्यात्मिक कार्यों के लिए दान कार्मिक ऋण मुक्ति को तेज करता है।"
            },
            "health": {
                "en": "Chronic reproductive or excretory system conditions may reach a turning point — either healing or requiring intervention. Near-death experiences or surgical procedures carry karmic significance and lead to spiritual awakening. Kundalini practices under qualified guidance can unlock extraordinary healing during this transit.",
                "hi": "पुराने प्रजनन या उत्सर्जन प्रणाली की स्थितियां एक मोड़ पर पहुंच सकती हैं — या तो उपचार या हस्तक्षेप की आवश्यकता। मृत्यु-समीप अनुभव या शल्य प्रक्रियाएं कार्मिक महत्व रखती हैं और आध्यात्मिक जागृति की ओर ले जाती हैं। योग्य मार्गदर्शन में कुंडलिनी अभ्यास इस गोचर में असाधारण उपचार को खोल सकता है।"
            },
        },
        9: {
            "general": {
                "en": "Ketu in the 9th house bestows intuitive spiritual wisdom that transcends formal religious education. Dharma is felt and lived rather than studied from texts — your spiritual path is deeply personal and unconventional. Father figures may be spiritually inclined or experience events that shift your philosophical worldview.",
                "hi": "केतु नौवें भाव में अंतर्ज्ञानी आध्यात्मिक ज्ञान प्रदान करता है जो औपचारिक धार्मिक शिक्षा से परे है। धर्म ग्रंथों से पढ़ने के बजाय अनुभव और जिया जाता है — आपका आध्यात्मिक मार्ग गहन व्यक्तिगत और अपरंपरागत है। पिता आध्यात्मिक झुकाव वाले हो सकते हैं या ऐसी घटनाएं अनुभव कर सकते हैं जो आपके दार्शनिक विश्वदृष्टिकोण को बदल दें।"
            },
            "love": {
                "en": "A partner who shares your spiritual values at the soul level brings the deepest satisfaction. Cross-cultural or interfaith relationships work only when grounded in shared spiritual practice. Pilgrimages and spiritual journeys undertaken together cement the bond beyond worldly attachments.",
                "hi": "आत्मा स्तर पर आपके आध्यात्मिक मूल्यों को साझा करने वाला साथी सबसे गहरी संतुष्टि लाता है। अंतर-सांस्कृतिक या अंतर-धर्म संबंध केवल साझा आध्यात्मिक अभ्यास पर आधारित होने पर ही काम करते हैं। एक साथ की गई तीर्थयात्राएं और आध्यात्मिक यात्राएं बंधन को सांसारिक आसक्तियों से परे सुदृढ़ करती हैं।"
            },
            "career": {
                "en": "Spiritual teaching, ashram leadership, philosophical writing, and pilgrimage guidance become natural vocations. Academic positions in philosophy or religion carry an authenticity that comes from lived experience. International spiritual missions and dharma propagation bring deep professional fulfillment.",
                "hi": "आध्यात्मिक शिक्षण, आश्रम नेतृत्व, दार्शनिक लेखन और तीर्थयात्रा मार्गदर्शन स्वाभाविक व्यवसाय बनते हैं। दर्शन या धर्म में शैक्षणिक पद जीवित अनुभव से आने वाली प्रामाणिकता रखते हैं। अंतरराष्ट्रीय आध्यात्मिक मिशन और धर्म प्रचार गहन पेशेवर संतुष्टि लाते हैं।"
            },
            "finance": {
                "en": "Financial investment in spiritual education, retreats, and pilgrimage yields immeasurable inner returns. Father's financial situation may be modest or require your support. Income from spiritual teaching and dharmic activities provides sufficient sustenance aligned with a purposeful life.",
                "hi": "आध्यात्मिक शिक्षा, आश्रम और तीर्थयात्रा में वित्तीय निवेश अनमोल आंतरिक लाभ देता है। पिता की वित्तीय स्थिति मामूली हो सकती है या आपके समर्थन की आवश्यकता हो सकती है। आध्यात्मिक शिक्षण और धार्मिक गतिविधियों से आय उद्देश्यपूर्ण जीवन के अनुरूप पर्याप्त जीविका प्रदान करती है।"
            },
            "health": {
                "en": "Hip and thigh area health fluctuates with the intensity of spiritual practices undertaken. Liver detoxification through fasting and Ayurvedic cleansing works exceptionally well during this transit. Walking pilgrimages and nature immersion provide both physical exercise and spiritual nourishment.",
                "hi": "कूल्हे और जांघ क्षेत्र का स्वास्थ्य किए गए आध्यात्मिक अभ्यासों की तीव्रता के साथ उतार-चढ़ाव करता है। उपवास और आयुर्वेदिक शोधन से यकृत विषहरण इस गोचर में असाधारण रूप से अच्छा काम करता है। पैदल तीर्थयात्राएं और प्रकृति में विसर्जन शारीरिक व्यायाम और आध्यात्मिक पोषण दोनों प्रदान करते हैं।"
            },
        },
        10: {
            "general": {
                "en": "Ketu in the 10th house brings detachment from worldly career ambitions and a shift toward spiritually meaningful work. Sudden, unexpected career changes or resignations may occur as material success loses its motivating power. Authority comes through spiritual wisdom rather than organizational hierarchy.",
                "hi": "केतु दसवें भाव में सांसारिक करियर महत्वाकांक्षाओं से विरक्ति और आध्यात्मिक रूप से सार्थक कार्य की ओर बदलाव लाता है। भौतिक सफलता अपनी प्रेरक शक्ति खोने पर अचानक, अप्रत्याशित करियर परिवर्तन या त्यागपत्र हो सकता है। अधिकार संगठनात्मक पदानुक्रम के बजाय आध्यात्मिक ज्ञान से आता है।"
            },
            "love": {
                "en": "Career detachment allows more time and energy for nurturing relationships. A partner who values spiritual growth over material achievement becomes the ideal companion. Public recognition for your partnership's spiritual contributions replaces conventional social status.",
                "hi": "करियर विरक्ति संबंधों के पोषण के लिए अधिक समय और ऊर्जा प्रदान करती है। भौतिक उपलब्धि से अधिक आध्यात्मिक विकास को महत्व देने वाला साथी आदर्श सहचर बनता है। आपकी साझेदारी के आध्यात्मिक योगदान के लिए सार्वजनिक मान्यता पारंपरिक सामाजिक प्रतिष्ठा का स्थान लेती है।"
            },
            "career": {
                "en": "Spiritual leadership, non-profit management, monastic life, or humanitarian work replaces corporate ambition. Past professional expertise is redirected toward service-oriented purposes. Unexpected resignation from prestigious positions leads to more fulfilling spiritual vocations.",
                "hi": "आध्यात्मिक नेतृत्व, गैर-लाभकारी प्रबंधन, मठवासी जीवन या मानवतावादी कार्य कॉर्पोरेट महत्वाकांक्षा का स्थान लेता है। पिछली पेशेवर विशेषज्ञता सेवा-उन्मुख उद्देश्यों की ओर पुनर्निर्देशित होती है। प्रतिष्ठित पदों से अप्रत्याशित त्यागपत्र अधिक संतुष्टिपूर्ण आध्यात्मिक व्यवसायों की ओर ले जाता है।"
            },
            "finance": {
                "en": "Income may decrease temporarily as career priorities shift from earning to serving. Professional investments yield diminishing returns as worldly focus weakens. Financial security comes through simplifying needs rather than increasing earnings.",
                "hi": "करियर प्राथमिकताओं के कमाई से सेवा की ओर बदलने पर आय अस्थायी रूप से कम हो सकती है। सांसारिक ध्यान कमजोर होने पर पेशेवर निवेश से घटते रिटर्न मिलते हैं। आय बढ़ाने के बजाय आवश्यकताओं को सरल बनाने से वित्तीय सुरक्षा आती है।"
            },
            "health": {
                "en": "Knee joint issues, bone density concerns, and career-related stress manifest physically during this transit. Skin conditions connected to emotional detachment from professional identity may surface. Grounding yoga practices, bone-strengthening exercises, and regular sunlight exposure maintain structural health.",
                "hi": "घुटने के जोड़ की समस्याएं, हड्डी घनत्व चिंताएं और करियर संबंधित तनाव इस गोचर में शारीरिक रूप से प्रकट होते हैं। पेशेवर पहचान से भावनात्मक विरक्ति से जुड़ी त्वचा की स्थितियां सतह पर आ सकती हैं। ग्राउंडिंग योग अभ्यास, हड्डी मजबूत करने वाले व्यायाम और नियमित धूप संरचनात्मक स्वास्थ्य बनाए रखते हैं।"
            },
        },
        11: {
            "general": {
                "en": "Ketu in the 11th house prioritizes spiritual gains over material accumulation and narrows social circles to spiritually aligned connections. Elder siblings may follow renunciation paths or experience events that catalyze your own spiritual growth. Selective networking with quality over quantity defines your social strategy.",
                "hi": "केतु ग्यारहवें भाव में भौतिक संचय से अधिक आध्यात्मिक लाभ को प्राथमिकता देता है और सामाजिक मंडल को आध्यात्मिक रूप से संरेखित संबंधों तक सीमित करता है। बड़े भाई-बहन त्याग के मार्ग अपना सकते हैं या ऐसी घटनाओं का अनुभव कर सकते हैं जो आपके अपने आध्यात्मिक विकास को उत्प्रेरित करती हैं। गुणवत्ता पर मात्रा से अधिक ध्यान देने वाला चयनात्मक नेटवर्किंग आपकी सामाजिक रणनीति को परिभाषित करता है।"
            },
            "love": {
                "en": "Spiritual friendships that blossom into deep love carry the most meaningful connections. Large social gatherings feel draining — intimate spiritual circles nourish romantic possibility. A lover who is also a spiritual companion creates the most fulfilling partnership.",
                "hi": "गहन प्रेम में खिलने वाली आध्यात्मिक मित्रताएं सबसे सार्थक संबंध रखती हैं। बड़े सामाजिक समारोह थकाने वाले लगते हैं — अंतरंग आध्यात्मिक मंडल रोमांटिक संभावना का पोषण करते हैं। जो प्रेमी आध्यात्मिक साथी भी हो वह सबसे संतोषजनक साझेदारी बनाता है।"
            },
            "career": {
                "en": "Satsang communities, spiritual networks, non-profit organizations, and dharmic social enterprises align with Ketu's 11th house energy. Technology-driven spiritual outreach and online meditation communities bring unexpected professional growth. Elder mentors from spiritual traditions guide career toward service.",
                "hi": "सत्संग समुदाय, आध्यात्मिक नेटवर्क, गैर-लाभकारी संगठन और धार्मिक सामाजिक उद्यम केतु की ग्यारहवें भाव की ऊर्जा से मेल खाते हैं। प्रौद्योगिकी-संचालित आध्यात्मिक पहुंच और ऑनलाइन ध्यान समुदाय अप्रत्याशित पेशेवर वृद्धि लाते हैं। आध्यात्मिक परंपराओं के वरिष्ठ मार्गदर्शक करियर को सेवा की ओर निर्देशित करते हैं।"
            },
            "finance": {
                "en": "Material gains plateau as Ketu redirects energy from accumulation to distribution. Elder siblings may need financial support or withdraw from shared financial obligations. Wealth shared with spiritual communities generates karmic merit that protects long-term prosperity.",
                "hi": "संचय से वितरण की ओर ऊर्जा पुनर्निर्देशित करने पर भौतिक लाभ स्थिर होता है। बड़े भाई-बहनों को वित्तीय सहायता की आवश्यकता हो सकती है या साझा वित्तीय दायित्वों से पीछे हट सकते हैं। आध्यात्मिक समुदायों के साथ साझा की गई संपत्ति कार्मिक पुण्य उत्पन्न करती है जो दीर्घकालिक समृद्धि की रक्षा करता है।"
            },
            "health": {
                "en": "Lower leg circulation and ankle health require consistent attention during this transit. Social withdrawal, while spiritually beneficial, should not lead to complete isolation affecting mental health. Walking meditation, community service, and balanced social engagement maintain both physical and emotional wellbeing.",
                "hi": "इस गोचर के दौरान पैरों के निचले हिस्से का रक्त संचार और टखने के स्वास्थ्य पर लगातार ध्यान आवश्यक है। सामाजिक वापसी, आध्यात्मिक रूप से लाभकारी होते हुए भी, मानसिक स्वास्थ्य को प्रभावित करने वाले पूर्ण अलगाव की ओर नहीं ले जानी चाहिए। चलित ध्यान, सामुदायिक सेवा और संतुलित सामाजिक भागीदारी शारीरिक और भावनात्मक दोनों कल्याण बनाए रखती है।"
            },
        },
        12: {
            "general": {
                "en": "Ketu in the 12th house is the ultimate moksha indicator — liberation, spiritual enlightenment, and dissolution of worldly attachments reach their pinnacle. Foreign spiritual journeys, ashram life, and deep meditation become defining experiences. This is the most powerful transit for spiritual seekers aspiring toward final liberation.",
                "hi": "केतु बारहवें भाव में परम मोक्ष सूचक है — मुक्ति, आध्यात्मिक ज्ञान और सांसारिक आसक्तियों का विलय अपने शिखर पर पहुंचता है। विदेशी आध्यात्मिक यात्राएं, आश्रम जीवन और गहन ध्यान निर्णायक अनुभव बनते हैं। अंतिम मुक्ति की आकांक्षा रखने वाले आध्यात्मिक साधकों के लिए यह सबसे शक्तिशाली गोचर है।"
            },
            "love": {
                "en": "Unconditional, selfless love that asks nothing in return characterizes romantic expression during this transit. Relationships become vehicles for spiritual liberation rather than emotional dependency. A partner who meditates, serves, and seeks truth alongside you creates the highest form of partnership.",
                "hi": "बदले में कुछ न मांगने वाला बिना शर्त, निस्वार्थ प्रेम इस गोचर में रोमांटिक अभिव्यक्ति की विशेषता है। संबंध भावनात्मक निर्भरता के बजाय आध्यात्मिक मुक्ति के वाहन बन जाते हैं। जो साथी आपके साथ ध्यान करता है, सेवा करता है और सत्य की खोज करता है, वह साझेदारी का उच्चतम रूप बनाता है।"
            },
            "career": {
                "en": "Monastery work, ashram service, foreign spiritual missions, hospice care, and prison chaplaincy align with Ketu's 12th house purpose. Behind-the-scenes spiritual work that requires no recognition brings the deepest satisfaction. Immigration to spiritually significant lands for permanent practice is strongly indicated.",
                "hi": "मठ कार्य, आश्रम सेवा, विदेशी आध्यात्मिक मिशन, धर्मशाला देखभाल और कारागार पुरोहिती केतु के बारहवें भाव के उद्देश्य से मेल खाती है। पर्दे के पीछे का आध्यात्मिक कार्य जिसमें किसी मान्यता की आवश्यकता नहीं, सबसे गहरी संतुष्टि लाता है। स्थायी अभ्यास के लिए आध्यात्मिक रूप से महत्वपूर्ण भूमि पर प्रवास दृढ़ता से संकेतित है।"
            },
            "finance": {
                "en": "Material expenses for spiritual purposes — donations, retreats, pilgrimages, and charitable trusts — increase significantly. Financial detachment accelerates as the soul prepares for liberation from material cycles. What is given away freely during this transit returns multiplied in spiritual currency.",
                "hi": "आध्यात्मिक उद्देश्यों के लिए भौतिक व्यय — दान, आश्रम, तीर्थयात्रा और धर्मार्थ ट्रस्ट — में उल्लेखनीय वृद्धि होती है। भौतिक चक्रों से मुक्ति के लिए आत्मा तैयार होने पर वित्तीय विरक्ति तेज होती है। इस गोचर में जो स्वेच्छा से दिया जाता है वह आध्यात्मिक मुद्रा में बहुगुणित होकर लौटता है।"
            },
            "health": {
                "en": "Sleep becomes the gateway to spiritual experiences — lucid dreaming, astral projection, and deep meditative sleep states intensify. Feet health, lymphatic system, and immune function require mindful attention. Complete fasting, silence retreats, and yogic sleep practices provide the most profound healing during this transit.",
                "hi": "नींद आध्यात्मिक अनुभवों का द्वार बन जाती है — सचेत स्वप्न, सूक्ष्म शरीर यात्रा और गहन ध्यानात्मक नींद की अवस्थाएं तीव्र होती हैं। पैरों का स्वास्थ्य, लसीका प्रणाली और प्रतिरक्षा कार्य पर सजग ध्यान आवश्यक है। पूर्ण उपवास, मौन आश्रम और योगिक नींद अभ्यास इस गोचर में सबसे गहन उपचार प्रदान करते हैं।"
            },
        },
    },
    # =========================================================================
    # RAHU (North Node) — obsession, illusion, foreign influence, technology
    # Shadow planet. Natural malefic. Amplifies desire and brings sudden turns.
    # =========================================================================
    "Rahu": {
        1: {
            "general": {"en": "Rahu in your 1st house intensifies self-focus and the urge to reinvent your identity. You may feel unusually ambitious, magnetic, and restless. Avoid impulsive image changes and exaggerated claims.", "hi": "पहले भाव में राहु आत्म-केंद्रितता और पहचान बदलने की तीव्र इच्छा बढ़ाता है। आप असामान्य रूप से महत्वाकांक्षी, आकर्षक और बेचैन महसूस कर सकते हैं। आवेगी छवि परिवर्तन और बढ़ा-चढ़ाकर बोलने से बचें।"},
            "love": {"en": "Unconventional attractions and sudden chemistry can arise quickly. Keep boundaries clear and avoid manipulative dynamics. Honest intent prevents confusion in romance.", "hi": "अपरंपरागत आकर्षण और अचानक केमिस्ट्री तेजी से बन सकती है। सीमाएं स्पष्ट रखें और चालाकी भरे व्यवहार से बचें। साफ नीयत प्रेम में भ्रम को रोकती है।"},
            "career": {"en": "Visibility increases and you may get bold roles involving media, technology, or foreign links. Use ambition strategically rather than chasing attention. A strong personal brand helps when backed by real work.", "hi": "दृश्यता बढ़ती है और मीडिया, तकनीक या विदेशी संपर्क वाले काम मिल सकते हैं। ध्यान के पीछे भागने के बजाय महत्वाकांक्षा को रणनीति से चलाएं। वास्तविक काम के साथ मजबूत व्यक्तिगत ब्रांड लाभ देता है।"},
            "finance": {"en": "Risk-taking impulses rise; avoid speculative bets made to prove status. Focus on transparent deals and documented income sources. Short-term gains are possible, but volatility is high.", "hi": "जोखिम लेने की प्रवृत्ति बढ़ती है; प्रतिष्ठा दिखाने के लिए सट्टा दांव से बचें। पारदर्शी सौदों और दस्तावेज़ी आय स्रोतों पर ध्यान दें। अल्पकालिक लाभ संभव है, पर अस्थिरता अधिक रहती है।"},
            "health": {"en": "Nervous energy and irregular routines can disturb sleep and digestion. Reduce stimulants and screen time, especially at night. Grounding practices help calm anxiety.", "hi": "नसों की ऊर्जा और अनियमित दिनचर्या से नींद और पाचन प्रभावित हो सकते हैं। खासकर रात में उत्तेजक पदार्थ और स्क्रीन समय कम करें। ग्राउंडिंग अभ्यास चिंता को शांत करते हैं।"},
        },
        2: {
            "general": {"en": "Rahu in the 2nd house magnifies focus on money, possessions, and speech. Family dynamics can feel intense or political. Speak carefully and avoid shortcuts in wealth-building.", "hi": "दूसरे भाव में राहु धन, संपत्ति और वाणी पर अत्यधिक ध्यान बढ़ाता है। पारिवारिक माहौल तीव्र या राजनीतिक लग सकता है। सोच-समझकर बोलें और धन निर्माण में शॉर्टकट से बचें।"},
            "love": {"en": "Desire for security can make you possessive. Practice reassurance without controlling behavior. Shared values matter more than flashy gestures.", "hi": "सुरक्षा की चाह आपको अधिकारपूर्ण बना सकती है। नियंत्रण के बिना भरोसा दें। दिखावे से अधिक साझा मूल्यों का महत्व रहेगा।"},
            "career": {"en": "Negotiation and persuasion skills can bring benefits, especially in sales or public roles. Keep ethics strong; reputation can swing quickly. Document agreements in writing.", "hi": "बातचीत और मनवाने की क्षमता से लाभ हो सकता है, खासकर बिक्री या सार्वजनिक भूमिकाओं में। नैतिकता मजबूत रखें; प्रतिष्ठा तेजी से बदल सकती है। समझौते लिखित में रखें।"},
            "finance": {"en": "Income opportunities appear, but so do temptations for dubious schemes. Avoid lending without paperwork. Build savings steadily to counter sudden expenses.", "hi": "आय के अवसर दिखते हैं, पर संदिग्ध योजनाओं का लालच भी बढ़ता है। बिना कागजात के उधार देने से बचें। अचानक खर्चों के लिए बचत धीरे-धीरे बनाएं।"},
            "health": {"en": "Throat, teeth, and dietary habits need attention. Overeating or sugary cravings can increase. A disciplined meal schedule improves stability.", "hi": "गला, दांत और खानपान पर ध्यान दें। अधिक खाने या मीठे की चाह बढ़ सकती है। अनुशासित भोजन समय स्थिरता लाता है।"},
        },
        3: {
            "general": {"en": "Rahu in the 3rd house boosts courage, hustle, and persuasive communication. You may feel driven to travel, network, and experiment. Verify facts before acting on rumors.", "hi": "तीसरे भाव में राहु साहस, मेहनत और प्रभावशाली संवाद बढ़ाता है। यात्रा, नेटवर्किंग और प्रयोग की तीव्र प्रेरणा हो सकती है। अफवाहों पर नहीं, तथ्यों की जांच कर के कदम उठाएं।"},
            "love": {"en": "Flirtation and playful messaging increase, but mixed signals can create drama. Keep communication clean and consistent. Avoid secretive triangles.", "hi": "फ्लर्ट और संदेशों में चंचलता बढ़ती है, पर मिश्रित संकेत नाटक पैदा कर सकते हैं। संवाद साफ और स्थिर रखें। गुप्त त्रिकोणों से बचें।"},
            "career": {"en": "Good for marketing, content, tech, and entrepreneurial moves. Short projects can scale fast if you stay disciplined. Avoid cutting corners under pressure.", "hi": "मार्केटिंग, कंटेंट, तकनीक और उद्यमिता के लिए अच्छा समय है। अनुशासन रहे तो छोटे प्रोजेक्ट तेजी से बढ़ सकते हैं। दबाव में भी शॉर्टकट न लें।"},
            "finance": {"en": "Side income through skills, media, or online work can rise. Track spending on gadgets and travel. Small but frequent expenses add up quickly.", "hi": "कौशल, मीडिया या ऑनलाइन काम से अतिरिक्त आय बढ़ सकती है। गैजेट्स और यात्रा पर खर्च ट्रैक करें। छोटे-छोटे खर्च जल्दी बढ़ जाते हैं।"},
            "health": {"en": "Arms, shoulders, and nerves may feel tense from overwork and screen use. Stretching and breathwork reduce restlessness. Drive carefully during short trips.", "hi": "अधिक काम और स्क्रीन से हाथ, कंधे और नसों में तनाव हो सकता है। स्ट्रेचिंग और श्वास अभ्यास बेचैनी घटाते हैं। छोटी यात्राओं में सावधानी से वाहन चलाएं।"},
        },
        4: {
            "general": {"en": "Rahu in the 4th house brings restlessness at home and a desire to upgrade property, vehicles, or comforts. Domestic politics can surface. Keep decisions practical and avoid emotional spending.", "hi": "चौथे भाव में राहु घर में बेचैनी और संपत्ति, वाहन या सुख-सुविधा बढ़ाने की चाह लाता है। घरेलू राजनीति उभर सकती है। निर्णय व्यावहारिक रखें और भावनात्मक खर्च से बचें।"},
            "love": {"en": "Family expectations may interfere with romance. Create privacy and reduce outside opinions. Emotional reassurance prevents misunderstandings.", "hi": "परिवार की अपेक्षाएं प्रेम पर असर डाल सकती हैं। निजी स्थान बनाएं और बाहरी राय कम करें। भावनात्मक भरोसा गलतफहमी रोकता है।"},
            "career": {"en": "Remote work, real-estate, hospitality, or home-based business can benefit. Avoid office politics carried into home life. A stable routine improves productivity.", "hi": "रिमोट वर्क, रियल-एस्टेट, हॉस्पिटैलिटी या घर से जुड़े व्यवसाय में लाभ हो सकता है। ऑफिस की राजनीति घर में न लाएं। स्थिर दिनचर्या उत्पादकता बढ़ाती है।"},
            "finance": {"en": "Spending on home repairs, decor, or vehicles may rise. Prefer transparent deals and verified paperwork in property matters. Avoid rushed purchases.", "hi": "घर की मरम्मत, सजावट या वाहन पर खर्च बढ़ सकता है। संपत्ति मामलों में पारदर्शी सौदे और कागजात की जांच करें। जल्दबाजी में खरीद से बचें।"},
            "health": {"en": "Chest, lungs, and sleep can be sensitive when mental stress rises. Keep your living space clean and ventilated. Calming evening routines help.", "hi": "मानसिक तनाव बढ़ने पर छाती, फेफड़े और नींद संवेदनशील हो सकती है। रहने की जगह साफ और हवादार रखें। शांत शाम की दिनचर्या मदद करती है।"},
        },
        5: {
            "general": {"en": "Rahu in the 5th house amplifies creativity, romance, and speculative appetite. Brilliant ideas can appear suddenly. Double-check decisions around children and investments.", "hi": "पांचवें भाव में राहु रचनात्मकता, प्रेम और सट्टा प्रवृत्ति बढ़ाता है। शानदार विचार अचानक आ सकते हैं। बच्चों और निवेश से जुड़े निर्णयों की दोबारा जांच करें।"},
            "love": {"en": "Romantic excitement increases, but illusions are also stronger. Avoid secret affairs and keep intentions clear. Attraction can be intense yet unstable.", "hi": "प्रेम में रोमांच बढ़ता है, पर भ्रम भी बढ़ता है। गुप्त संबंधों से बचें और नीयत स्पष्ट रखें। आकर्षण तीव्र पर अस्थिर हो सकता है।"},
            "career": {"en": "Good for entertainment, creative work, trading, or tech innovation. Present ideas with structure, not hype. Mentorship helps refine raw talent.", "hi": "मनोरंजन, रचनात्मक काम, ट्रेडिंग या तकनीकी नवाचार के लिए अच्छा समय। विचारों को दिखावे के बजाय संरचना के साथ प्रस्तुत करें। मार्गदर्शन से प्रतिभा निखरती है।"},
            "finance": {"en": "Speculation can tempt you; set risk limits and avoid gambling. Gains are possible through smart strategy, but losses can be sudden. Prefer diversified investing.", "hi": "सट्टा लुभा सकता है; जोखिम सीमा तय करें और जुए से बचें। रणनीति सही हो तो लाभ संभव है, पर नुकसान भी अचानक हो सकता है। विविध निवेश बेहतर है।"},
            "health": {"en": "Stomach and stress-related issues can rise with excitement and irregular eating. Reduce late-night snacking. Creative outlets reduce mental pressure.", "hi": "उत्साह और अनियमित भोजन से पेट और तनाव-जनित समस्याएं बढ़ सकती हैं। देर रात स्नैकिंग कम करें। रचनात्मक गतिविधियां मानसिक दबाव घटाती हैं।"},
        },
        6: {
            "general": {"en": "Rahu in the 6th house can bring victories over competitors and sudden problem-solving ability. You may expose hidden opponents. Keep routines clean to avoid health fluctuations.", "hi": "छठे भाव में राहु प्रतिस्पर्धियों पर विजय और अचानक समाधान क्षमता दे सकता है। छिपे विरोधी उजागर हो सकते हैं। स्वास्थ्य उतार-चढ़ाव से बचने के लिए दिनचर्या साफ रखें।"},
            "love": {"en": "Minor conflicts can arise due to suspicion or overthinking. Avoid spying or testing your partner. Practical support strengthens relationships.", "hi": "शंका या अधिक सोच के कारण छोटे विवाद हो सकते हैं। साथी की जांच-पड़ताल से बचें। व्यावहारिक सहयोग रिश्ते मजबूत करता है।"},
            "career": {"en": "Excellent for litigation, competitive exams, research, and crisis roles. You can outperform rivals through strategy. Avoid unethical tactics; backlash can be severe.", "hi": "कानूनी मामलों, प्रतियोगी परीक्षाओं, शोध और संकट-प्रबंधन भूमिकाओं के लिए उत्तम समय। रणनीति से प्रतिद्वंद्वियों पर बढ़त मिलती है। अनैतिक तरीकों से बचें; प्रतिक्रिया भारी हो सकती है।"},
            "finance": {"en": "Debt management improves if you stay disciplined. Avoid hidden liabilities and read contracts carefully. Unexpected gains through disputes are possible.", "hi": "अनुशासन रहे तो ऋण प्रबंधन सुधरता है। छिपी देनदारियों से बचें और अनुबंध ध्यान से पढ़ें। विवादों से अचानक लाभ संभव है।"},
            "health": {"en": "Allergies, toxins, and stress-related issues may flare. Keep hygiene high and avoid risky substances. Regular checkups help catch problems early.", "hi": "एलर्जी, विषाक्तता और तनाव से जुड़ी समस्याएं उभर सकती हैं। स्वच्छता बनाए रखें और नशे/जोखिम भरी चीजों से बचें। नियमित जांच मदद करती है।"},
        },
        7: {
            "general": {"en": "Rahu in the 7th house brings intense focus on partnerships, contracts, and public image. New alliances can form quickly, especially with foreign or unconventional people. Vet commitments carefully before locking them in.", "hi": "सातवें भाव में राहु साझेदारी, अनुबंध और सार्वजनिक छवि पर तीव्र ध्यान लाता है। खासकर विदेशी या अपरंपरागत लोगों के साथ नए गठबंधन तेजी से बन सकते हैं। प्रतिबद्धता से पहले अच्छी तरह जांच-पड़ताल करें।"},
            "love": {"en": "Attraction can be strong and sudden, but clarity is essential. Avoid relationships based on fantasy or convenience. Honest communication prevents trust issues.", "hi": "आकर्षण तीव्र और अचानक हो सकता है, पर स्पष्टता जरूरी है। कल्पना या सुविधा पर आधारित रिश्तों से बचें। ईमानदार संवाद भरोसे की समस्या रोकता है।"},
            "career": {"en": "Business partnerships and client-facing roles expand. Choose collaborators with clean reputations. Written agreements protect you from misunderstandings.", "hi": "व्यापार साझेदारी और ग्राहक-सामना भूमिकाओं में विस्तार हो सकता है। साफ प्रतिष्ठा वाले सहयोगी चुनें। लिखित समझौते गलतफहमी से बचाते हैं।"},
            "finance": {"en": "Shared finances and contracts require transparency. Avoid risky joint ventures without due diligence. Gains can come via partnerships, but leakage is possible too.", "hi": "साझा वित्त और अनुबंधों में पारदर्शिता जरूरी है। जांच के बिना जोखिम भरे संयुक्त उपक्रम से बचें। साझेदारी से लाभ भी संभव है, पर नुकसान/लीकेज भी हो सकता है।"},
            "health": {"en": "Stress can manifest through skin issues or hormonal imbalance. Balance social obligations with rest. Avoid overindulgence that affects vitality.", "hi": "तनाव त्वचा समस्याओं या हार्मोन असंतुलन के रूप में दिख सकता है। सामाजिक दायित्वों और आराम में संतुलन रखें। अतिशय भोग से बचें जो ऊर्जा घटाता है।"},
        },
        8: {
            "general": {"en": "Rahu in the 8th house brings sudden transformations, secrets, and deep psychological themes. Interest in occult subjects may increase. Avoid risky behavior and keep insurance and paperwork updated.", "hi": "आठवें भाव में राहु अचानक परिवर्तन, रहस्य और गहरे मानसिक विषय लाता है। गूढ़ विषयों में रुचि बढ़ सकती है। जोखिम भरे व्यवहार से बचें और बीमा व कागजात अपडेट रखें।"},
            "love": {"en": "Intimacy can deepen, but trust must be earned. Avoid jealousy and hidden games. Healing conversations strengthen bonds.", "hi": "निकटता गहरी हो सकती है, पर भरोसा कमाना जरूरी है। ईर्ष्या और गुप्त खेलों से बचें। उपचारक बातचीत संबंध मजबूत करती है।"},
            "career": {"en": "Good for research, investigation, cybersecurity, and crisis management. Hidden opportunities appear through confidential work. Maintain strict ethics with sensitive data.", "hi": "शोध, जांच, साइबर सुरक्षा और संकट प्रबंधन के लिए अच्छा समय। गोपनीय काम से छिपे अवसर मिल सकते हैं। संवेदनशील डेटा के साथ कड़ी नैतिकता रखें।"},
            "finance": {"en": "Be cautious with loans, taxes, and shared assets. Sudden gains or losses are possible; avoid leverage. Keep compliance clean to prevent penalties.", "hi": "ऋण, कर और साझा संपत्ति में सावधानी रखें। अचानक लाभ या नुकसान संभव है; लीवरेज से बचें। दंड से बचने के लिए अनुपालन साफ रखें।"},
            "health": {"en": "Reproductive health, chronic issues, and stress need attention. Avoid extreme detox or unverified therapies. Grounding and steady routines support recovery.", "hi": "प्रजनन स्वास्थ्य, पुरानी समस्याएं और तनाव पर ध्यान दें। अत्यधिक डिटॉक्स या बिना जांच उपचार से बचें। स्थिर दिनचर्या और ग्राउंडिंग स्वास्थ्य में मदद करते हैं।"},
        },
        9: {
            "general": {"en": "Rahu in the 9th house challenges beliefs and pushes you toward new philosophies, travel, and unconventional teachers. Question dogma, but avoid arrogance. Learn through direct experience and verified guidance.", "hi": "नौवें भाव में राहु विश्वासों को चुनौती देता है और नई विचारधाराओं, यात्रा तथा अपरंपरागत गुरुओं की ओर ले जाता है। रूढ़ि पर प्रश्न करें, पर अहंकार से बचें। प्रत्यक्ष अनुभव और सत्यापित मार्गदर्शन से सीखें।"},
            "love": {"en": "Cross-cultural or long-distance connections may develop. Shared worldview matters more than excitement alone. Avoid moral conflicts by aligning values early.", "hi": "भिन्न संस्कृति या लंबी दूरी के संबंध बन सकते हैं। सिर्फ रोमांच नहीं, साझा दृष्टि जरूरी है। मूल्यों को पहले मिलाकर नैतिक टकराव से बचें।"},
            "career": {"en": "Good for higher education, publishing, legal work, and international roles. Mentors help, but verify credentials. Opportunities come via travel or global networks.", "hi": "उच्च शिक्षा, प्रकाशन, कानून और अंतरराष्ट्रीय भूमिकाओं के लिए अच्छा समय। मार्गदर्शक मदद करेंगे, पर योग्यता जांचें। यात्रा या वैश्विक नेटवर्क से अवसर आते हैं।"},
            "finance": {"en": "Expenses on travel, courses, and certifications increase. Avoid risky investments justified by ideology. Focus on skills that convert to stable income.", "hi": "यात्रा, कोर्स और प्रमाणपत्रों पर खर्च बढ़ता है। विचारधारा के नाम पर जोखिम भरे निवेश से बचें। ऐसे कौशल पर ध्यान दें जो स्थिर आय में बदलें।"},
            "health": {"en": "Hips and liver area can be sensitive if lifestyle becomes excessive. Moderate indulgence and maintain movement. Spiritual practices can reduce mental stress.", "hi": "जीवनशैली अति हो जाए तो कूल्हे और यकृत क्षेत्र संवेदनशील हो सकते हैं। संयम रखें और नियमित गतिविधि करें। आध्यात्मिक अभ्यास मानसिक तनाव घटाते हैं।"},
        },
        10: {
            "general": {"en": "Rahu in the 10th house fuels ambition, public visibility, and desire for power. Rapid career shifts or fame can occur. Build credibility patiently to avoid reputation shocks.", "hi": "दसवें भाव में राहु महत्वाकांक्षा, सार्वजनिक दृश्यता और शक्ति की चाह बढ़ाता है। करियर में तेज बदलाव या प्रसिद्धि संभव है। प्रतिष्ठा के झटके से बचने के लिए धीरे-धीरे विश्वसनीयता बनाएं।"},
            "love": {"en": "Work can dominate priorities, causing relationship imbalance. Set clear time boundaries. Appreciation and presence matter more than grand promises.", "hi": "काम प्राथमिकता बनकर रिश्तों में असंतुलन ला सकता है। समय सीमाएं स्पष्ट करें। बड़े वादों से ज्यादा उपस्थिति और सराहना मायने रखती है।"},
            "career": {"en": "Excellent for politics, corporate growth, tech leadership, and unconventional industries. Promotions may come suddenly. Avoid conflicts with authority and keep compliance tight.", "hi": "राजनीति, कॉर्पोरेट वृद्धि, तकनीकी नेतृत्व और अपरंपरागत उद्योगों के लिए उत्तम समय। पदोन्नति अचानक मिल सकती है। अधिकारियों से टकराव से बचें और अनुपालन मजबूत रखें।"},
            "finance": {"en": "Income can rise with status, but expenses also increase. Avoid flashy spending that drains savings. Keep taxes and documentation accurate.", "hi": "पद के साथ आय बढ़ सकती है, पर खर्च भी बढ़ता है। दिखावे के खर्च से बचें जो बचत घटाए। कर और दस्तावेज़ सही रखें।"},
            "health": {"en": "Stress and blood pressure can rise with ambition and workload. Prioritize sleep and routine exercise. Detox digital overload to reduce burnout.", "hi": "महत्वाकांक्षा और कार्यभार से तनाव व रक्तचाप बढ़ सकता है। नींद और नियमित व्यायाम प्राथमिक रखें। डिजिटल ओवरलोड कम करके बर्नआउट घटाएं।"},
        },
        11: {
            "general": {"en": "Rahu in the 11th house expands networks, gains, and access to influential circles. Sudden opportunities can come through friends or online communities. Choose associations wisely to avoid scandals.", "hi": "ग्यारहवें भाव में राहु नेटवर्क, लाभ और प्रभावशाली लोगों तक पहुंच बढ़ाता है। मित्रों या ऑनलाइन समुदाय से अचानक अवसर मिल सकते हैं। बदनामी से बचने के लिए संगति सोच-समझकर चुनें।"},
            "love": {"en": "Romance can emerge through social circles or friendships. Avoid mixing love with group politics. Keep intentions clear in public settings.", "hi": "सामाजिक दायरे या मित्रता से प्रेम संबंध बन सकते हैं। प्रेम को समूह राजनीति से अलग रखें। सार्वजनिक माहौल में नीयत स्पष्ट रखें।"},
            "career": {"en": "Big organizations, tech platforms, and collaborations bring growth. Leadership in communities increases your reach. Focus on long-term alliances, not quick wins.", "hi": "बड़े संगठन, तकनीकी प्लेटफॉर्म और सहयोग से वृद्धि होती है। समुदायों में नेतृत्व से प्रभाव बढ़ता है। त्वरित लाभ नहीं, दीर्घकालिक गठबंधनों पर ध्यान दें।"},
            "finance": {"en": "Gains improve but can be irregular. Diversify income streams and avoid risky speculation with friends. Separate money from friendships with clear terms.", "hi": "लाभ बढ़ते हैं पर अनियमित हो सकते हैं। आय के स्रोत विविध बनाएं और मित्रों के साथ जोखिम भरे सट्टे से बचें। धन और मित्रता को स्पष्ट शर्तों के साथ अलग रखें।"},
            "health": {"en": "Over-socializing can disturb sleep and routines. Manage screen time and late nights. Balanced social life supports mental well-being.", "hi": "अत्यधिक मेलजोल से नींद और दिनचर्या बिगड़ सकती है। स्क्रीन समय और देर रात कम करें। संतुलित सामाजिक जीवन मानसिक स्वास्थ्य को सहारा देता है।"},
        },
        12: {
            "general": {"en": "Rahu in the 12th house highlights foreign lands, isolation, hidden desires, and subconscious patterns. Travel or relocation may be tempting. Avoid escapism and keep spiritual discipline.", "hi": "बारहवें भाव में राहु विदेश, एकांत, छिपी इच्छाएं और अवचेतन पैटर्न उभारता है। यात्रा या स्थान परिवर्तन का आकर्षण बढ़ सकता है। पलायनवाद से बचें और आध्यात्मिक अनुशासन रखें।"},
            "love": {"en": "Secret attractions or long-distance dynamics can emerge. Avoid deception and be transparent about commitments. Compassionate honesty prevents regret.", "hi": "गुप्त आकर्षण या दूरस्थ संबंध उभर सकते हैं। धोखे से बचें और प्रतिबद्धता में पारदर्शिता रखें। करुणामय ईमानदारी पछतावा रोकती है।"},
            "career": {"en": "Work with foreign clients, hospitals, research labs, or behind-the-scenes teams can progress. Maintain confidentiality and clear documentation. Quiet effort brings results.", "hi": "विदेशी ग्राहक, अस्पताल, शोध प्रयोगशाला या पर्दे के पीछे की टीमों में काम आगे बढ़ सकता है। गोपनीयता और दस्तावेज़ स्पष्ट रखें। शांत प्रयास से परिणाम मिलते हैं।"},
            "finance": {"en": "Expenses increase on travel, health, and comforts. Watch subscriptions and hidden charges. Build a safety buffer to avoid anxiety.", "hi": "यात्रा, स्वास्थ्य और सुख-सुविधा पर खर्च बढ़ सकता है। सब्सक्रिप्शन और छिपे शुल्क पर नजर रखें। चिंता कम करने के लिए सुरक्षा निधि बनाएं।"},
            "health": {"en": "Sleep quality and mental health need protection. Meditation and reduced stimulants help. Avoid addictive habits that drain vitality.", "hi": "नींद की गुणवत्ता और मानसिक स्वास्थ्य की रक्षा जरूरी है। ध्यान और उत्तेजक पदार्थ कम करना मदद करता है। ऊर्जा घटाने वाली आदतों से बचें।"},
        },
    },
    # =========================================================================
    # KETU (South Node) — detachment, moksha, intuition, past-life karma
    # Shadow planet. Natural malefic. Cuts attachment and deepens insight.
    # =========================================================================
    "Ketu": {
        1: {
            "general": {"en": "Ketu in your 1st house brings introspection and a desire to withdraw from superficial identity concerns. You may feel less interested in approval and more focused on meaning. Avoid neglecting basic responsibilities while seeking solitude.", "hi": "पहले भाव में केतु आत्मचिंतन और सतही पहचान की चिंता से दूरी लाता है। आप प्रशंसा से कम और अर्थ से अधिक जुड़ सकते हैं। एकांत खोजते हुए बुनियादी जिम्मेदारियों की उपेक्षा न करें।"},
            "love": {"en": "Emotional distance can appear if you retreat too much. Practice gentle communication and presence. A spiritual or mindful connection feels more satisfying than drama.", "hi": "अधिक पीछे हटने पर भावनात्मक दूरी आ सकती है। कोमल संवाद और उपस्थित रहना जरूरी है। नाटक के बजाय आध्यात्मिक या सजग जुड़ाव अधिक संतोष देता है।"},
            "career": {"en": "You may prefer independent work and deeper mastery rather than showy roles. Good for research, healing, and behind-the-scenes efforts. Avoid disappearing from important commitments.", "hi": "दिखावटी भूमिकाओं के बजाय स्वतंत्र काम और गहरी महारत की इच्छा हो सकती है। शोध, उपचार और पर्दे के पीछे के प्रयासों के लिए अच्छा समय। महत्वपूर्ण प्रतिबद्धताओं से गायब न हों।"},
            "finance": {"en": "Material motivation may dip; maintain budgeting discipline anyway. Avoid careless spending due to indifference. Focus on essential expenses and long-term security.", "hi": "भौतिक प्रेरणा घट सकती है; फिर भी बजट अनुशासन रखें। उदासीनता में लापरवाह खर्च से बचें। आवश्यक खर्च और दीर्घकालिक सुरक्षा पर ध्यान दें।"},
            "health": {"en": "Energy may fluctuate with mental withdrawal. Support the nervous system through sleep and simple routines. Meditation helps, but keep the body grounded.", "hi": "मानसिक अलगाव से ऊर्जा उतार-चढ़ाव हो सकता है। नींद और सरल दिनचर्या से नसों को सहारा दें। ध्यान मदद करता है, पर शरीर को जमीन से जुड़ा रखें।"},
        },
        2: {
            "general": {"en": "Ketu in the 2nd house reduces attachment to wealth and can make speech more blunt or detached. Family patterns from the past may surface. Speak with kindness and keep financial basics in order.", "hi": "दूसरे भाव में केतु धन से आसक्ति कम करता है और वाणी को रूखा या अलग-थलग बना सकता है। परिवार के पुराने पैटर्न उभर सकते हैं। दयालुता से बोलें और वित्तीय आधार व्यवस्थित रखें।"},
            "love": {"en": "You may value simplicity over romance theatrics. Express affection through care rather than words alone. Avoid withdrawing when family pressure increases.", "hi": "आप दिखावे से ज्यादा सरलता को महत्व दे सकते हैं। केवल शब्द नहीं, देखभाल से स्नेह जताएं। पारिवारिक दबाव बढ़े तो पीछे न हटें।"},
            "career": {"en": "Work involving analysis, data, or minimalistic communication suits you. Be careful with negotiations; detached tone can be misread. Maintain professionalism with clients.", "hi": "विश्लेषण, डेटा या संक्षिप्त संवाद वाला काम अनुकूल रहेगा। बातचीत में सावधानी रखें; आपका अलग-थलग स्वर गलत समझा जा सकता है। ग्राहकों के साथ पेशेवर रहें।"},
            "finance": {"en": "Avoid ignoring savings and documentation. Sudden expenses can arise through family or dental matters. Keep an emergency buffer.", "hi": "बचत और कागजात की अनदेखी न करें। परिवार या दंत समस्याओं से अचानक खर्च हो सकता है। आपात निधि रखें।"},
            "health": {"en": "Teeth, throat, and digestion may need care if diet becomes irregular. Prefer simple, sattvic meals. Hydration and routine improve stability.", "hi": "आहार अनियमित होने पर दांत, गला और पाचन पर असर पड़ सकता है। सरल, सात्विक भोजन चुनें। पानी और दिनचर्या स्थिरता बढ़ाते हैं।"},
        },
        3: {
            "general": {"en": "Ketu in the 3rd house brings quiet courage and preference for solitary effort. You may communicate less but with depth. Avoid misunderstandings with siblings due to silence.", "hi": "तीसरे भाव में केतु शांत साहस और एकांत प्रयास की प्रवृत्ति लाता है। आप कम बोलेंगे पर गहराई से। मौन के कारण भाई-बहनों से गलतफहमी से बचें।"},
            "love": {"en": "You may avoid casual flirting and prefer meaningful conversation. Share feelings directly instead of disappearing. Small acts of service express love well.", "hi": "आप हल्के फ्लर्ट से बचकर अर्थपूर्ण बातचीत पसंद कर सकते हैं। गायब होने के बजाय भाव सीधे साझा करें। छोटे सेवा-भाव के काम प्रेम दिखाते हैं।"},
            "career": {"en": "Good for writing, research, coding, and skill-building in isolation. Short travel reduces; focus improves. Keep collaboration channels open to avoid being overlooked.", "hi": "लेखन, शोध, कोडिंग और एकांत में कौशल निर्माण के लिए अच्छा समय। छोटी यात्राएं कम हो सकती हैं; फोकस बढ़ता है। अनदेखे होने से बचने के लिए सहयोग चैनल खुले रखें।"},
            "finance": {"en": "Spending on tools for learning can be useful. Avoid impulsive gadget buys; buy only what supports your craft. Side income can come from niche skills.", "hi": "सीखने के उपकरणों पर खर्च उपयोगी हो सकता है। आवेगी गैजेट खरीद से बचें; वही लें जो काम में सहायक हो। निचे कौशल से अतिरिक्त आय संभव है।"},
            "health": {"en": "Neck and shoulder tension can rise with long focused work. Take breaks and stretch. Calm breathing reduces mental overload.", "hi": "लंबे फोकस काम से गर्दन और कंधे में तनाव बढ़ सकता है। विराम लें और स्ट्रेच करें। शांत श्वास मानसिक दबाव घटाती है।"},
        },
        4: {
            "general": {"en": "Ketu in the 4th house creates detachment from home comforts and can bring relocations or changes in living arrangements. Emotional patterns from childhood may surface. Build inner security rather than chasing external comfort.", "hi": "चौथे भाव में केतु घर के सुख से दूरी और रहने के स्थान में बदलाव/स्थानांतरण ला सकता है। बचपन की भावनात्मक आदतें उभर सकती हैं। बाहरी सुविधा के बजाय अंदरूनी सुरक्षा बनाएं।"},
            "love": {"en": "You may need more private time, which partners can misunderstand. Explain your need for space gently. Nurturing routines at home support harmony.", "hi": "आपको अधिक निजी समय चाहिए हो सकता है, जिसे साथी गलत समझ सकते हैं। जगह की जरूरत को कोमलता से समझाएं। घर की पोषणकारी दिनचर्या सामंजस्य बढ़ाती है।"},
            "career": {"en": "Home-based work, study, and introspective projects progress well. Avoid being too isolated from teams. Clear updates keep trust intact.", "hi": "घर से काम, अध्ययन और आत्ममंथन वाले प्रोजेक्ट अच्छे चलते हैं। टीम से अत्यधिक अलग न हों। स्पष्ट अपडेट भरोसा बनाए रखते हैं।"},
            "finance": {"en": "Avoid over-investing in decor or property upgrades to fill emotional gaps. Spend on essentials and maintenance. Simple living reduces stress.", "hi": "भावनात्मक खालीपन भरने के लिए सजावट या प्रॉपर्टी अपग्रेड पर अधिक निवेश न करें। आवश्यक और रखरखाव पर खर्च करें। सरल जीवन तनाव घटाता है।"},
            "health": {"en": "Chest and emotional stress can affect breathing and sleep. Keep the home airy and calm. Meditation and gentle walking help regulation.", "hi": "छाती और भावनात्मक तनाव से श्वास और नींद प्रभावित हो सकती है। घर को शांत और हवादार रखें। ध्यान और हल्की सैर सहायक है।"},
        },
        5: {
            "general": {"en": "Ketu in the 5th house heightens intuition, past-life creativity, and interest in mantras or spiritual study. You may feel detached from applause. Balance inner focus with responsibilities toward children and projects.", "hi": "पांचवें भाव में केतु अंतर्ज्ञान, पूर्व-जन्म की रचनात्मकता और मंत्र/आध्यात्मिक अध्ययन की रुचि बढ़ाता है। प्रशंसा से दूरी महसूस हो सकती है। बच्चों और प्रोजेक्ट की जिम्मेदारी के साथ अंदरूनी फोकस संतुलित रखें।"},
            "love": {"en": "Romance becomes more contemplative; you may dislike games. Express warmth intentionally. Avoid emotional withdrawal that looks like coldness.", "hi": "प्रेम अधिक चिंतनशील हो सकता है; आपको खेल पसंद नहीं आएंगे। जान-बूझकर गर्मजोशी दिखाएं। भावनात्मक दूरी को ठंडापन न बनने दें।"},
            "career": {"en": "Good for teaching, research, and creative work with depth. Avoid risky speculation; prefer mastery. Mentoring juniors brings karmic satisfaction.", "hi": "गहराई वाले शिक्षण, शोध और रचनात्मक काम के लिए अच्छा समय। जोखिम भरे सट्टे से बचें; महारत चुनें। कनिष्ठों को मार्गदर्शन से संतोष मिलता है।"},
            "finance": {"en": "Speculative impulses reduce, which is good. Keep investment plans simple and long-term. Expenses may go toward learning or spiritual practices.", "hi": "सट्टा प्रवृत्ति कम होती है, जो अच्छा है। निवेश योजनाएं सरल और दीर्घकालिक रखें। सीखने या आध्यात्मिक अभ्यास पर खर्च हो सकता है।"},
            "health": {"en": "Stomach sensitivity can rise when stress is suppressed. Eat simple and avoid late meals. Creative expression helps emotional digestion.", "hi": "तनाव दबाने पर पेट संवेदनशील हो सकता है। सरल भोजन करें और देर से खाना न खाएं। रचनात्मक अभिव्यक्ति भावनात्मक पाचन में मदद करती है।"},
        },
        6: {
            "general": {"en": "Ketu in the 6th house gives sharp discernment to defeat enemies and overcome obstacles quietly. You may prefer serving without recognition. Avoid neglecting health signals due to stoicism.", "hi": "छठे भाव में केतु शत्रुओं पर शांत तरीके से विजय और बाधाएं पार करने की सूझ देता है। आप बिना पहचान के सेवा करना पसंद कर सकते हैं। कठोरता में स्वास्थ्य संकेतों की अनदेखी न करें।"},
            "love": {"en": "You may become overly practical in relationships. Balance duty with affection. Avoid judging your partner for emotional needs.", "hi": "रिश्तों में आप अत्यधिक व्यावहारिक हो सकते हैं। कर्तव्य और स्नेह में संतुलन रखें। साथी की भावनात्मक जरूरतों को आंकने से बचें।"},
            "career": {"en": "Good for healing work, problem-solving, and technical service roles. Quiet competence earns respect over time. Avoid workplace isolation; communicate progress.", "hi": "उपचार, समस्या समाधान और तकनीकी सेवा भूमिकाओं के लिए अच्छा समय। शांत दक्षता समय के साथ सम्मान दिलाती है। कार्यस्थल पर अलगाव से बचें; प्रगति साझा करें।"},
            "finance": {"en": "Debt repayment and expense reduction improve if you stay disciplined. Avoid hidden fees and unclear medical spending. Keep receipts and records.", "hi": "अनुशासन रहे तो ऋण चुकाने और खर्च घटाने में मदद मिलती है। छिपे शुल्क और अस्पष्ट चिकित्सा खर्च से बचें। रसीदें और रिकॉर्ड रखें।"},
            "health": {"en": "Digestive sensitivity and skin issues can flare if stress is internalized. Prefer clean food and simple routines. Regular checkups help.", "hi": "तनाव अंदर दबाने पर पाचन संवेदनशीलता और त्वचा समस्या उभर सकती है। साफ भोजन और सरल दिनचर्या रखें। नियमित जांच सहायक है।"},
        },
        7: {
            "general": {"en": "Ketu in the 7th house brings detachment and karmic tests in partnerships. You may question relationship expectations and seek depth. Avoid coldness; clarity and compassion keep bonds steady.", "hi": "सातवें भाव में केतु साझेदारी में अलगाव और कार्मिक परीक्षाएं लाता है। आप रिश्तों की अपेक्षाओं पर प्रश्न कर सकते हैं और गहराई चाहेंगे। ठंडापन न लाएं; स्पष्टता और करुणा संबंध स्थिर रखती है।"},
            "love": {"en": "You may crave spiritual companionship over surface romance. Old karmic partners can reappear. Set boundaries and avoid silent withdrawal.", "hi": "आप सतही रोमांस से ज्यादा आध्यात्मिक संग चाहते हैं। पुराने कार्मिक साथी लौट सकते हैं। सीमाएं तय करें और मौन में पीछे न हटें।"},
            "career": {"en": "Partnership work requires patience and explicit roles. Avoid vague contracts. Strong outcomes come from principled collaboration.", "hi": "साझेदारी वाले काम में धैर्य और स्पष्ट भूमिकाएं जरूरी हैं। अस्पष्ट अनुबंध से बचें। सिद्धांत-आधारित सहयोग से अच्छे परिणाम मिलते हैं।"},
            "finance": {"en": "Shared finances need transparency and minimal complexity. Avoid entanglement in unclear joint debts. Keep accounts separated where possible.", "hi": "साझा धन में पारदर्शिता और कम जटिलता जरूरी है। अस्पष्ट संयुक्त ऋण में फंसने से बचें। संभव हो तो खाते अलग रखें।"},
            "health": {"en": "Hormonal balance and stress require steady routines. Emotional suppression can show up as fatigue. Gentle movement and honest dialogue help.", "hi": "हार्मोन संतुलन और तनाव के लिए स्थिर दिनचर्या आवश्यक है। भाव दबाने से थकान हो सकती है। हल्की गतिविधि और ईमानदार संवाद मदद करते हैं।"},
        },
        8: {
            "general": {"en": "Ketu in the 8th house supports deep spiritual transformation, occult study, and research. You may detach from old fears. Avoid careless risk; move with mindfulness.", "hi": "आठवें भाव में केतु गहरा आध्यात्मिक परिवर्तन, गूढ़ अध्ययन और शोध को सहारा देता है। पुराने डर से दूरी बन सकती है। लापरवाह जोखिम से बचें; सजगता से चलें।"},
            "love": {"en": "Intimacy becomes profound but quiet. Avoid secrecy that damages trust. Healing honesty deepens bonds.", "hi": "निकटता गहरी पर शांत हो सकती है। भरोसा तोड़ने वाली गोपनीयता से बचें। उपचारक ईमानदारी रिश्ते गहरे करती है।"},
            "career": {"en": "Excellent for investigation, forensics, data security, and research roles. Hidden knowledge becomes your advantage. Keep compliance strong with sensitive matters.", "hi": "जांच, फॉरेंसिक, डेटा सुरक्षा और शोध भूमिकाओं के लिए उत्तम। छिपा ज्ञान आपकी बढ़त बनता है। संवेदनशील मामलों में अनुपालन मजबूत रखें।"},
            "finance": {"en": "Be conservative with loans and taxes. Avoid speculative leverage. Savings and insurance planning bring peace.", "hi": "ऋण और कर में सावधानी रखें। सट्टा लीवरेज से बचें। बचत और बीमा योजना शांति देती है।"},
            "health": {"en": "Chronic issues may need holistic attention. Avoid extremes and listen to subtle signals. Rest, meditation, and steady routines support healing.", "hi": "पुरानी समस्याओं पर समग्र ध्यान जरूरी हो सकता है। अति से बचें और सूक्ष्म संकेत सुनें। आराम, ध्यान और स्थिर दिनचर्या उपचार में सहायक है।"},
        },
        9: {
            "general": {"en": "Ketu in the 9th house increases spiritual seeking and detachment from rigid belief systems. You may find unusual teachers or paths. Respect tradition but follow direct realization.", "hi": "नौवें भाव में केतु आध्यात्मिक खोज बढ़ाता है और कठोर विश्वास प्रणालियों से दूरी लाता है। आपको अनोखे गुरु या मार्ग मिल सकते हैं। परंपरा का सम्मान करें पर प्रत्यक्ष अनुभूति का अनुसरण करें।"},
            "love": {"en": "Shared dharma and values become central in relationships. You may avoid superficial matches. Speak openly about principles to prevent silent distance.", "hi": "रिश्तों में साझा धर्म और मूल्य केंद्र बनते हैं। आप सतही मेल से बच सकते हैं। सिद्धांतों पर खुलकर बात करें ताकि मौन दूरी न बने।"},
            "career": {"en": "Good for teaching, spiritual work, publishing, and advisory roles. Credentials matter, but inner integrity matters more. Avoid arrogance in debates.", "hi": "शिक्षण, आध्यात्मिक काम, प्रकाशन और सलाहकारी भूमिकाओं के लिए अच्छा समय। प्रमाणपत्र जरूरी हैं, पर भीतर की ईमानदारी अधिक महत्वपूर्ण है। बहस में अहंकार से बचें।"},
            "finance": {"en": "Spend on learning and pilgrimage only with planning. Avoid risky investments driven by ideology. Simple, stable income strategies work best.", "hi": "सीखने और तीर्थ पर खर्च योजना से करें। विचारधारा के कारण जोखिम भरे निवेश से बचें। सरल, स्थिर आय रणनीति श्रेष्ठ है।"},
            "health": {"en": "Hips and sciatic area may need care if you sit too long. Walking and gentle yoga help. Spiritual practice reduces mental agitation.", "hi": "लंबे समय बैठने से कूल्हे और सायटिका क्षेत्र पर असर हो सकता है। सैर और हल्का योग मदद करता है। आध्यात्मिक अभ्यास मानसिक बेचैनी घटाता है।"},
        },
        10: {
            "general": {"en": "Ketu in the 10th house can reduce attachment to status and make career feel less fulfilling. You may seek purpose over titles. Keep responsibilities intact while recalibrating direction.", "hi": "दसवें भाव में केतु पद-प्रतिष्ठा से आसक्ति कम करता है और करियर कम संतोषजनक लग सकता है। आप पद से ज्यादा उद्देश्य चाहेंगे। दिशा बदलते हुए भी जिम्मेदारी निभाएं।"},
            "love": {"en": "Work-related detachment can spill into relationships. Share your inner process with your partner. Consistent presence prevents misunderstandings.", "hi": "काम से जुड़ा अलगाव रिश्तों में भी आ सकता है। अपने भीतर की प्रक्रिया साथी से साझा करें। स्थिर उपस्थिति गलतफहमी रोकती है।"},
            "career": {"en": "Good for research, consulting, and roles that reward expertise over show. Avoid abrupt resignations; plan transitions. Quiet excellence builds long-term respect.", "hi": "शोध, परामर्श और ऐसी भूमिकाओं के लिए अच्छा समय जहां दिखावे से ज्यादा विशेषज्ञता महत्व रखती है। अचानक नौकरी छोड़ने से बचें; बदलाव की योजना बनाएं। शांत उत्कृष्टता दीर्घकालिक सम्मान बनाती है।"},
            "finance": {"en": "Income may be steady but motivation to chase more reduces. Maintain savings habits. Avoid neglecting taxes and paperwork.", "hi": "आय स्थिर हो सकती है पर अधिक पाने की दौड़ कम हो सकती है। बचत की आदत बनाए रखें। कर और कागजात की अनदेखी न करें।"},
            "health": {"en": "Stress can show as fatigue if you suppress dissatisfaction. Balance work with restorative practices. Sunlight, routine, and movement help.", "hi": "असंतोष दबाने पर तनाव थकान बन सकता है। काम और पुनर्स्थापन अभ्यास में संतुलन रखें। धूप, दिनचर्या और गतिविधि मदद करती है।"},
        },
        11: {
            "general": {"en": "Ketu in the 11th house makes you selective about friends and networks. Gains come through meaningful alliances rather than crowds. Avoid withdrawing without explanation from social circles.", "hi": "ग्यारहवें भाव में केतु मित्रों और नेटवर्क में चयनात्मकता लाता है। भीड़ के बजाय अर्थपूर्ण संबंधों से लाभ मिलता है। सामाजिक दायरे से बिना बताए दूरी न बनाएं।"},
            "love": {"en": "Love may arise from friendship, but you prefer sincerity over hype. Avoid confusing signals by being direct. Quality time matters.", "hi": "मित्रता से प्रेम हो सकता है, पर आप दिखावे से ज्यादा सच्चाई चाहेंगे। सीधे रहें ताकि संकेत भ्रमित न हों। गुणवत्तापूर्ण समय महत्वपूर्ण है।"},
            "career": {"en": "You may step back from corporate politics and focus on craft. Niche communities support growth. Avoid burning bridges; leave networks gracefully.", "hi": "आप कॉर्पोरेट राजनीति से हटकर कौशल पर ध्यान दे सकते हैं। निचे समुदाय वृद्धि में सहायक है। संबंध तोड़े बिना सम्मान से आगे बढ़ें।"},
            "finance": {"en": "Gains may be moderate but stable when you avoid overexpansion. Avoid risky schemes pitched by friends. Keep financial goals simple.", "hi": "अति विस्तार से बचें तो लाभ मध्यम पर स्थिर रह सकता है। मित्रों द्वारा सुझाई जोखिम भरी योजनाओं से बचें। वित्तीय लक्ष्य सरल रखें।"},
            "health": {"en": "Social withdrawal can affect mood; maintain light community engagement. Walking and sunlight help regulate energy. Avoid excessive isolation.", "hi": "सामाजिक दूरी से मनोदशा प्रभावित हो सकती है; हल्का समुदाय जुड़ाव रखें। सैर और धूप ऊर्जा संतुलित करती है। अत्यधिक एकांत से बचें।"},
        },
        12: {
            "general": {"en": "Ketu in the 12th house supports meditation, liberation, and letting go of old attachments. Solitude can be deeply restorative. Avoid neglecting practical life while pursuing spiritual escape.", "hi": "बारहवें भाव में केतु ध्यान, मुक्ति और पुरानी आसक्ति छोड़ने में सहायक है। एकांत गहराई से पुनर्स्थापनकारी हो सकता है। आध्यात्मिक पलायन में व्यावहारिक जीवन की उपेक्षा न करें।"},
            "love": {"en": "You may prefer quiet, compassionate love and may withdraw from noisy relationships. Share needs gently. Spiritual practices as a couple bring closeness.", "hi": "आप शांत, करुणामय प्रेम पसंद कर सकते हैं और शोर वाले रिश्तों से दूरी बन सकती है। जरूरतें कोमलता से बताएं। साथ में आध्यात्मिक अभ्यास निकटता बढ़ाते हैं।"},
            "career": {"en": "Good for work in hospitals, ashrams, research labs, and foreign institutions. Behind-the-scenes roles suit you. Keep boundaries to avoid exploitation.", "hi": "अस्पताल, आश्रम, शोध प्रयोगशाला और विदेशी संस्थानों के काम के लिए अच्छा समय। पर्दे के पीछे की भूमिकाएं अनुकूल हैं। शोषण से बचने के लिए सीमाएं रखें।"},
            "finance": {"en": "Expenses may rise on travel, charity, and healing. Keep budgets and avoid leaks through subscriptions. Simplicity protects peace.", "hi": "यात्रा, दान और उपचार पर खर्च बढ़ सकता है। बजट रखें और सब्सक्रिप्शन से होने वाले लीकेज से बचें। सरलता शांति बचाती है।"},
            "health": {"en": "Sleep, immunity, and mental peace need attention. Meditation helps, but also keep nutrition and routine steady. Avoid escapist habits.", "hi": "नींद, प्रतिरक्षा और मानसिक शांति पर ध्यान दें। ध्यान मदद करता है, पर पोषण और दिनचर्या भी स्थिर रखें। पलायनवादी आदतों से बचें।"},
        },
    },
}

# =========================================================================
# DIGNITY MODIFIERS — prefix/suffix phrases for planet dignity states
# =========================================================================
DIGNITY_MODIFIERS: Dict[str, Dict[str, Dict[str, str]]] = {
    "exalted": {
        "prefix": {"en": "With exceptional strength, ", "hi": "असाधारण बल के साथ, "},
        "suffix": {"en": " Results are amplified and highly favorable.", "hi": " परिणाम प्रबलित और अत्यंत अनुकूल हैं।"},
    },
    "debilitated": {
        "prefix": {"en": "With diminished strength, ", "hi": "क्षीण बल के साथ, "},
        "suffix": {"en": " Extra effort is needed to realize benefits.", "hi": " लाभ प्राप्त करने के लिए अतिरिक्त प्रयास आवश्यक है।"},
    },
    "own_sign": {
        "prefix": {"en": "Comfortably placed, ", "hi": "स्वगृही होकर, "},
        "suffix": {"en": " Natural strengths are expressed freely.", "hi": " स्वाभाविक शक्तियां स्वतंत्र रूप से प्रकट होती हैं।"},
    },
    "retrograde": {
        "prefix": {"en": "In retrograde motion, ", "hi": "वक्री गति में, "},
        "suffix": {"en": " Review and revision of past matters is indicated.", "hi": " पुराने मामलों की समीक्षा और पुनर्विचार संकेतित है।"},
    },
    "combust": {
        "prefix": {"en": "Being combust near the Sun, ", "hi": "सूर्य के निकट अस्त होने से, "},
        "suffix": {"en": " Effects may be subdued or internalized.", "hi": " प्रभाव दबे हुए या आंतरिक हो सकते हैं।"},
    },
}
