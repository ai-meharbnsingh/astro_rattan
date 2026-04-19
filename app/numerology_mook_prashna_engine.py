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
        "detail": "Your mind is focused on yourself right now — your health, your body, or your inner state. This could be a worry about a fever, an ongoing illness, or a physical symptom that needs attention. It may also point to suppressed anger, a recent argument, or a conflict that is still unresolved. Reflect on which of these feels most relevant: your body's signals or the friction in a relationship.",
        "detail_hi": "आपका मन अभी अपने आप पर केंद्रित है — आपका स्वास्थ्य, शरीर, या आंतरिक स्थिति। यह किसी बुखार, चल रही बीमारी या शारीरिक लक्षण की चिंता हो सकती है। इसका अर्थ दबा हुआ क्रोध, हाल का झगड़ा या अनसुलझा विवाद भी हो सकता है। सोचें — कौन सा विषय अधिक प्रासंगिक लगता है: शरीर की पुकार या रिश्ते में तनाव।",
        "category": "Health & Self",
    },
    4:  {
        "topic": "Family / Love / Heart's Desire",
        "topic_hi": "परिवार / प्रेम / मन की गहरी इच्छा",
        "detail": "Your heart is thinking about home, family, or a deep personal desire. This number reveals feelings of love, joy, comfort, and the people closest to you. You may be longing for something — a reunion, emotional security, a relationship, or domestic happiness. Trust what your heart truly wants; this is the time to act on that quiet inner wish.",
        "detail_hi": "आपका हृदय घर, परिवार या किसी गहरी व्यक्तिगत इच्छा के बारे में सोच रहा है। यह अंक प्रेम, आनन्द, आराम और निकट जनों की भावनाओं को प्रकट करता है। आप किसी मिलन, भावनात्मक सुरक्षा, रिश्ते या घरेलू सुख की चाह रख सकते हैं। अपने हृदय की सच्ची चाह पर भरोसा करें।",
        "category": "Family & Love",
    },
    5:  {
        "topic": "Marriage / Partnership / Peace",
        "topic_hi": "विवाह / साझेदारी / शान्ति और सुलह",
        "detail": "Your mind is dwelling on a relationship, agreement, or the question of harmony and peace. This may concern a marriage proposal, a business partnership, a contract to sign, or resolving a dispute. You may be the one who can bring two opposing sides together. Focus on balance, fairness, and mutual benefit in whatever situation you are navigating.",
        "detail_hi": "आपका मन किसी रिश्ते, समझौते या सुलह के सवाल पर केंद्रित है। यह किसी विवाह प्रस्ताव, व्यापारिक साझेदारी, अनुबंध या विवाद सुलझाने से संबंधित हो सकता है। आप दो विपरीत पक्षों को एक साथ ला सकते हैं। संतुलन, निष्पक्षता और आपसी लाभ पर ध्यान दें।",
        "category": "Relationships",
    },
    6:  {
        "topic": "News / Siblings / Communication / Travel",
        "topic_hi": "समाचार / भाई-बहन / संचार / यात्रा",
        "detail": "You are waiting for news, a message, or a reply — or you are thinking about a sibling or close relative. There may be a letter, call, or email that is on your mind. A short journey may also be involved, or you are thinking about how to communicate something important. Be patient; the information you are waiting for will arrive soon.",
        "detail_hi": "आप किसी समाचार, संदेश या उत्तर की प्रतीक्षा कर रहे हैं — या किसी भाई-बहन या निकट संबंधी के बारे में सोच रहे हैं। कोई पत्र, कॉल या संदेश आपके मन में है। एक छोटी यात्रा भी संभव है, या आप कुछ महत्वपूर्ण कहने का तरीका सोच रहे हैं। धैर्य रखें; जो जानकारी आप चाहते हैं, वह शीघ्र आएगी।",
        "category": "Communication",
    },
    7:  {
        "topic": "House / Land / Water / Relocation",
        "topic_hi": "मकान / जमीन / जल / स्थानान्तरण",
        "detail": "Your thoughts are circling around property — a house, a plot of land, or a significant change of location. You may be contemplating buying, selling, or renting property, or thinking about relocating to a new city or country. Water and deep foundations are symbolic here — this is about where you plant your roots. Think carefully before making any major move.",
        "detail_hi": "आपके विचार संपत्ति के इर्द-गिर्द घूम रहे हैं — एक मकान, जमीन का टुकड़ा, या स्थान में बड़ा बदलाव। आप संपत्ति खरीदने, बेचने या किराये पर लेने, या किसी नए शहर/देश में जाने के बारे में सोच सकते हैं। जल और गहरी नींव यहाँ प्रतीक हैं — यह वह जगह है जहाँ आप अपनी जड़ें जमाते हैं। कोई भी बड़ा कदम उठाने से पहले ध्यान से सोचें।",
        "category": "Property",
    },
    8:  {
        "topic": "Antiques / Foreign / Ancient Things",
        "topic_hi": "प्राचीन वस्तुएं / विदेश / पूर्व दिशा",
        "detail": "Your mind is on something old, distant, or foreign — antique objects, heritage, history, or matters involving another country. You may be thinking about an item of ancestral value, a connection to foreign lands, or knowledge from ancient traditions. The east direction holds significance. Look to the past or to faraway sources for the answer you seek.",
        "detail_hi": "आपका मन किसी पुरानी, दूर की या विदेशी चीज पर है — प्राचीन वस्तुएं, विरासत, इतिहास, या किसी दूसरे देश से संबंधित मामले। पूर्व दिशा यहाँ महत्वपूर्ण है। अपने पूर्वजों की विरासत या दूरदराज के स्रोतों में उत्तर खोजें।",
        "category": "Foreign & Ancient",
    },
    9:  {
        "topic": "Death / Business Loss / Wrong Deal",
        "topic_hi": "मृत्यु / व्यापारिक घाटा / गलत अनुबंध",
        "detail": "A heavy or difficult matter weighs on your mind — possibly the passing of someone, a significant financial loss, or a business deal that went wrong. You may be wondering how to recover from damage or how to exit a bad agreement. This is not a time for new risks; focus on damage control, settling debts, and healing what has been harmed.",
        "detail_hi": "कोई भारी या कठिन विषय आपके मन पर है — शायद किसी की मृत्यु, बड़ा आर्थिक नुकसान, या गलत व्यापारिक सौदा। आप यह सोच रहे होंगे कि नुकसान से कैसे उबरें या बुरे समझौते से कैसे निकलें। यह नए जोखिम उठाने का समय नहीं है; नुकसान नियंत्रण और उपचार पर ध्यान दें।",
        "category": "Loss & Difficulty",
    },
    10: {
        "topic": "Harmful Friendship / Bad Contract / Dispute",
        "topic_hi": "हानिकारक मित्रता / बुरा अनुबंध / झगड़ा",
        "detail": "Your mind is troubled by a friendship or partnership that may not be serving you well. A contract or agreement may have hidden risks, or you are caught in an ongoing dispute with someone. Examine the people and agreements in your life carefully — not everything that appears friendly is truly beneficial. Resolve conflicts calmly before they escalate further.",
        "detail_hi": "आपका मन किसी मित्रता या साझेदारी से परेशान है जो शायद आपके हित में नहीं है। किसी अनुबंध में छिपे जोखिम हो सकते हैं, या आप किसी विवाद में फंसे हैं। अपने जीवन के लोगों और समझौतों की सावधानी से जांच करें। विवाद बढ़ने से पहले शांति से सुलझाएं।",
        "category": "Conflict",
    },
    11: {
        "topic": "Mine / Property Valuation / Land",
        "topic_hi": "खान / सम्पत्ति मूल्यांकन / जायदाद",
        "detail": "Your question is rooted in property — its value, ownership, or potential. This may involve getting a house or land assessed, resolving a dispute over inherited property, or exploring a mine or resource-rich land. Financial decisions around immovable assets are on your mind. Seek expert valuation before making any major property transaction.",
        "detail_hi": "आपका प्रश्न संपत्ति — उसके मूल्य, स्वामित्व या संभावना से जुड़ा है। इसमें मकान या जमीन का मूल्यांकन, पैतृक संपत्ति के विवाद को सुलझाना, या संसाधन-समृद्ध भूमि की खोज शामिल हो सकती है। किसी भी बड़े संपत्ति लेनदेन से पहले विशेषज्ञ मूल्यांकन लें।",
        "category": "Property",
    },
    12: {
        "topic": "Celebration / Party / Luxury",
        "topic_hi": "उत्सव / पार्टी / विलासिता",
        "detail": "Your heart is drawn toward celebration, pleasure, and the finer things in life. You may be planning or attending a social gathering, a party, or a festive occasion. Fine clothes, luxury items, comfort, and enjoyment are themes here. Allow yourself to embrace the joy around you — social connections made now carry positive energy.",
        "detail_hi": "आपका मन उत्सव, आनंद और जीवन की बेहतर चीजों की ओर खिंचा है। आप किसी सामाजिक समारोह, पार्टी या उत्सव की योजना बना सकते हैं या उसमें भाग ले सकते हैं। अच्छे वस्त्र, विलासिता, आराम और आनंद यहाँ प्रमुख विषय हैं। अपने आसपास की खुशी को अपनाएं।",
        "category": "Celebration",
    },
    13: {
        "topic": "Money / Lottery / Urgent Financial Gain",
        "topic_hi": "धन / लॉटरी / तत्काल आर्थिक लाभ",
        "detail": "Money is firmly on your mind — an urgent financial need, an unexpected windfall, or a gamble of some kind. You may be hoping for a lottery win, a quick return on investment, or relief from financial pressure. This number often indicates that money is both the question and the answer. Be cautious about impulsive financial decisions; think twice before risking what you have.",
        "detail_hi": "धन आपके मन पर है — कोई तत्काल आर्थिक जरूरत, अप्रत्याशित लाभ या कोई जोखिम। आप लॉटरी, जल्दी लाभ या आर्थिक दबाव से राहत की उम्मीद कर सकते हैं। आवेग में आकर आर्थिक फैसले न करें।",
        "category": "Finance",
    },
    14: {
        "topic": "Female Relatives / Short Journey / Overseas News",
        "topic_hi": "स्त्री संबंधी / छोटी यात्रा / विदेश से समाचार",
        "detail": "A woman in your family — a sister, aunt, grandmother, or mother-figure — is at the center of your thoughts. Alternatively, you are anticipating news from a distant place or planning a short trip. There may be a message or correspondence coming from abroad. This is a good time to reach out to the women in your family; they have something important to share.",
        "detail_hi": "परिवार की कोई महिला — बहन, चाची, दादी, माँ — आपके विचारों के केंद्र में है। या आप किसी दूरदराज के समाचार की प्रतीक्षा कर रहे हैं। विदेश से कोई संदेश आ सकता है। परिवार की महिलाओं से संपर्क करें — उनके पास कुछ महत्वपूर्ण है।",
        "category": "Family & Travel",
    },
    15: {
        "topic": "Death / Bad News / Loss / Misfortune",
        "topic_hi": "मृत्यु / बुरी खबर / हानि / दुर्भाग्य",
        "detail": "Your mind is burdened by something painful — the fear of bad news, a recent loss, or a streak of misfortune. This could be the passing of someone you know, a financial setback, or an emotional blow. Grief and loss are natural parts of life; allow yourself time to process. Seek support from those around you rather than carrying this weight alone.",
        "detail_hi": "आपका मन किसी दर्दनाक बात से दबा है — बुरी खबर का डर, हाल का नुकसान, या दुर्भाग्य की लहर। यह किसी परिचित की मृत्यु, आर्थिक झटका, या भावनात्मक चोट हो सकती है। दुःख जीवन का हिस्सा है; अकेले बोझ न उठाएं, अपनों से सहारा लें।",
        "category": "Loss & Difficulty",
    },
    16: {
        "topic": "Good News / Beneficial Agreement / Wife",
        "topic_hi": "शुभ समाचार / लाभदायक अनुबंध / पत्नी",
        "detail": "Something positive is on the horizon — you are thinking about good news that is about to arrive, a beneficial agreement, or a contact that will bring advantage. Matters related to your wife or a close female partner may also be in focus. This is a favourable number; move forward with confidence in negotiations and expect auspicious developments soon.",
        "detail_hi": "कुछ सकारात्मक क्षितिज पर है — आप आने वाले शुभ समाचार, लाभकारी समझौते या फायदेमंद संपर्क के बारे में सोच रहे हैं। पत्नी या किसी करीबी महिला साथी से जुड़े मामले भी चर्चा में हो सकते हैं। यह अनुकूल अंक है — वार्ता में आत्मविश्वास से आगे बढ़ें।",
        "category": "Good Fortune",
    },
    17: {
        "topic": "Disease / Servant / Happy Journey / Family",
        "topic_hi": "रोग / नौकर / हर्षदायक यात्रा / कुटुम्ब",
        "detail": "This number carries a dual energy — on one side there is concern about health, a servant's behaviour, or a domestic difficulty; on the other, there is the promise of a happy journey, a joyful message, or fulfilling family work. Read the context of your life right now: if things feel heavy, focus on health and household; if they feel light, embrace the travel or good news coming your way.",
        "detail_hi": "यह अंक दोहरी ऊर्जा रखता है — एक ओर स्वास्थ्य, नौकर या घरेलू कठिनाई की चिंता है; दूसरी ओर हर्षदायक यात्रा, खुशखबरी या परिवार का काम है। अपने जीवन का संदर्भ पढ़ें: यदि भारी लगे तो स्वास्थ्य पर ध्यान दें; यदि हल्का लगे तो आने वाली खुशी को अपनाएं।",
        "category": "Health & Family",
    },
    18: {
        "topic": "Happy Journey / Love / Desired Message / Gold",
        "topic_hi": "हर्षदायक यात्रा / प्रेम / इच्छित संदेश / सुवर्ण",
        "detail": "Joy and movement are in the air — your mind is set on a happy trip, a romantic connection, or a longed-for message finally arriving. There may be financial reward, a salary, or gold involved. Family activities bring warmth. This is one of the more fortunate numbers; whatever you have been hoping to hear or receive is likely on its way to you.",
        "detail_hi": "खुशी और गति हवा में है — आपका मन एक सुखद यात्रा, प्रेम संबंध, या प्रतीक्षित संदेश पर है। वित्तीय पुरस्कार, वेतन या सोना शामिल हो सकता है। परिवारिक गतिविधियाँ उष्णता लाती हैं। यह भाग्यशाली अंकों में से एक है — जो सुनना या पाना चाहते थे वह आने वाला है।",
        "category": "Joy & Travel",
    },
    19: {
        "topic": "Work Obstruction / Hospital / Jail / Lost Child",
        "topic_hi": "कार्य में रुकावट / अस्पताल / जेल / बच्चा",
        "detail": "A serious blockage has entered your thoughts — work that has stopped, a forced period of isolation, or concern about someone confined in a hospital or institution. You may be worried about a child who is lost, ill, or facing punishment. This number calls for patience and compassion. Work through the obstacle step by step rather than forcing a breakthrough.",
        "detail_hi": "कोई गंभीर बाधा आपके विचारों में है — रुका हुआ काम, अनिवार्य एकांत, या किसी के अस्पताल/संस्था में बंद होने की चिंता। कोई बच्चा खोया हुआ, बीमार या सजा का सामना कर रहा हो सकता है। यह अंक धैर्य और करुणा की माँग करता है। बाधा को धीरे-धीरे पार करें।",
        "category": "Difficulty",
    },
    20: {
        "topic": "Journey / Letter / Transport / Road",
        "topic_hi": "यात्रा / पत्र / परिवहन / रास्ता",
        "detail": "Movement and communication are your primary concerns — a journey you need to make, a letter or message you are waiting for, or the logistics of transporting something from one place to another. A road, route, or path is also symbolically significant here. Check your correspondence and plan your travel; things will begin to move once you take the first step.",
        "detail_hi": "गतिविधि और संचार आपकी प्राथमिक चिंताएं हैं — कोई यात्रा जो करनी है, कोई पत्र जिसका इंतजार है, या किसी वस्तु के परिवहन की व्यवस्था। रास्ता या मार्ग यहाँ प्रतीकात्मक रूप से महत्वपूर्ण है। अपना पत्र व्यवहार जांचें और यात्रा की योजना बनाएं।",
        "category": "Travel & Communication",
    },
    21: {
        "topic": "Financial Gain / Silver / White Items",
        "topic_hi": "आर्थिक लाभ / चाँदी / सफेद वस्तु",
        "detail": "Money, possessions, and material gain are on your mind. You may be thinking about an amount owed to you, a purchase you want to make, or silver and white-coloured objects that hold value. There is a gentle optimism here — some financial benefit is within reach. Take stock of what you already own before seeking more; the gain may already be in your possession.",
        "detail_hi": "धन, संपत्ति और भौतिक लाभ आपके मन पर है। आप किसी देय राशि, खरीदारी, या चाँदी व सफेद वस्तुओं के बारे में सोच रहे हैं। यहाँ हल्की आशावादिता है — कुछ आर्थिक लाभ पहुँच में है। अधिक खोजने से पहले जो पास है उसका मूल्यांकन करें।",
        "category": "Finance",
    },
    22: {
        "topic": "Unwanted Marriage / Sick Partner / Enemy",
        "topic_hi": "अनिच्छित विवाह / बीमार साथी / शत्रु",
        "detail": "There is tension in a key relationship — a marriage or partnership that feels forced or mismatched, a partner who is unwell, or an enemy whose actions are affecting you. A difficult contract or agreement may also be weighing heavily. This is a time to address relationship problems honestly rather than avoiding them. Identify who is truly on your side and who is not.",
        "detail_hi": "किसी मुख्य रिश्ते में तनाव है — एक विवाह या साझेदारी जो मजबूरी से हुई हो, एक बीमार साथी, या कोई शत्रु जिसके कार्य आपको प्रभावित कर रहे हैं। रिश्ते की समस्याओं को ईमानदारी से संबोधित करें। पहचानें कि वास्तव में आपके साथ कौन है और कौन नहीं।",
        "category": "Relationships",
    },
    23: {
        "topic": "Good Living / Fine Clothes / Health / Comfort",
        "topic_hi": "सुखद जीवन / अच्छे वस्त्र / स्वास्थ्य / आराम",
        "detail": "Your mind is on comfort, quality, and the good life — fine clothes, nutritious food, good health, a respected position, or loyal people around you. This is one of the most positive numbers and suggests you are thinking about how to elevate your quality of life. You deserve good things; focus on maintaining your health and reputation, and the comfort you seek will naturally follow.",
        "detail_hi": "आपका मन आराम, गुणवत्ता और अच्छे जीवन पर है — अच्छे वस्त्र, पौष्टिक भोजन, अच्छा स्वास्थ्य, प्रतिष्ठित पद। यह सबसे सकारात्मक अंकों में से एक है। स्वास्थ्य और प्रतिष्ठा बनाए रखने पर ध्यान दें।",
        "category": "Comfort & Prosperity",
    },
    24: {
        "topic": "Unstable Situation / Family Quarrel / Children / Secret Love",
        "topic_hi": "डाँवाडोल स्थिति / कुटुम्ब कलह / बच्चे / गुप्त प्रेम",
        "detail": "The ground beneath you feels unsteady — a family quarrel, a new project meeting unexpected resistance, or a domestic situation that refuses to settle. Children may be involved, or there may be a secret love connection you are nurturing quietly. Stability will return, but it requires honest conversation and patience. Do not start new ventures until the current turbulence calms.",
        "detail_hi": "आपके पैरों तले जमीन अस्थिर लगती है — पारिवारिक झगड़ा, कोई नया काम जो बाधाओं से घिरा है, या घरेलू स्थिति जो शांत नहीं हो रही। बच्चे शामिल हो सकते हैं, या कोई गुप्त प्रेम। ईमानदार बातचीत और धैर्य से स्थिरता लौटेगी।",
        "category": "Family",
    },
    25: {
        "topic": "Excessive Profit / Gold / Sun / Wealth",
        "topic_hi": "अत्यधिक लाभ / सुवर्ण / सूर्य / सम्पत्ति",
        "detail": "Abundant wealth and shining success are in your thoughts — gold, a major financial gain, or the radiance of the sun itself. You may be thinking about a big investment, an opportunity to multiply your money, or celebrating prosperity that has already arrived. This is a powerful wealth number; act on your ambitions boldly but avoid greed, which can turn fortune into loss.",
        "detail_hi": "प्रचुर धन और चमकती सफलता आपके विचारों में है — सोना, बड़ा आर्थिक लाभ, या सूर्य की आभा। आप बड़े निवेश या धन बढ़ाने के अवसर के बारे में सोच रहे हैं। यह शक्तिशाली धन अंक है; साहस से काम करें लेकिन लालच से बचें।",
        "category": "Wealth",
    },
    26: {
        "topic": "Peaceful Rights / Good Property / Plot / House",
        "topic_hi": "शान्तिपूर्वक अधिकार / अच्छी जायदाद / मकान / प्लॉट",
        "detail": "Your thoughts are on securing what is rightfully yours — a house, a plot of land, or property that should belong to you. The key word here is 'peaceful': this number favours gaining rights through calm, lawful means rather than conflict. Foundation, stability, and solid ground are highlighted. This is a good time to formalise ownership or draft a legal agreement around property.",
        "detail_hi": "आपके विचार वह पाने पर हैं जो वैध रूप से आपका है — मकान, जमीन, या संपत्ति। मुख्य बात 'शांतिपूर्ण' है: यह अंक शांत, कानूनी तरीकों से अधिकार पाने का समर्थन करता है। संपत्ति के स्वामित्व को औपचारिक बनाने का यह अच्छा समय है।",
        "category": "Property",
    },
    27: {
        "topic": "Closed Room / Boat Journey / Brother / Letter / New Moon",
        "topic_hi": "बन्द कमरा / नाव यात्रा / भाई / पत्र / नया चन्द्रमा",
        "detail": "Your mind is in an enclosed, reflective space — a closed room, a boat on water, or the quiet stillness of a new moon phase. A brother or male relative may be at the centre of your concern. A letter or piece of correspondence is expected. Silver and white objects carry symbolic weight here. Use this introspective period to plan carefully before acting.",
        "detail_hi": "आपका मन एक बंद, चिंतनशील जगह में है — एक बंद कमरा, पानी पर नाव, या नए चंद्रमा की शांत स्थिरता। कोई भाई या पुरुष संबंधी आपकी चिंता के केंद्र में हो सकता है। पत्र या पत्राचार की प्रतीक्षा है। इस चिंतन काल का उपयोग सावधानी से योजना बनाने में करें।",
        "category": "Travel & Family",
    },
    28: {
        "topic": "Imagination / New Moon / White/Silver Objects",
        "topic_hi": "कल्पना / नया चन्द्रमा / सफेद-चाँदी वस्तु",
        "detail": "Your mind is wandering in the realm of imagination, intuition, and subtle energies. A new moon phase suggests new beginnings that are not yet visible — seeds planted in the dark. White cloth, silver objects, and cup-shaped vessels carry meaning. Trust your instincts and inner visions right now; what you imagine has a real chance of becoming reality if you act with intention.",
        "detail_hi": "आपका मन कल्पना, अंतर्ज्ञान और सूक्ष्म ऊर्जाओं के क्षेत्र में भटक रहा है। नया चंद्रमा नई शुरुआत का संकेत है जो अभी दिखाई नहीं दे रही। सफेद वस्त्र और चाँदी की वस्तुएं अर्थपूर्ण हैं। अभी अपनी प्रवृत्ति और आंतरिक दृष्टि पर भरोसा करें।",
        "category": "Spiritual",
    },
    29: {
        "topic": "Poor Health / Poverty / Blood Disorder / Struggle",
        "topic_hi": "खराब स्वास्थ्य / गरीबी / रक्त विकार / संघर्ष",
        "detail": "A difficult period is weighing on your mind — poor health, financial struggle, or a feeling of being stuck in difficult circumstances. Blood-related health concerns or chronic illness may be a worry. This number is a call to take your body and finances seriously. Seek proper medical advice, avoid wasteful spending, and build slowly rather than seeking quick fixes.",
        "detail_hi": "एक कठिन दौर आपके मन पर भारी है — खराब स्वास्थ्य, आर्थिक संघर्ष, या कठिन परिस्थितियों में फंसे होने का एहसास। रक्त संबंधी स्वास्थ्य चिंताएं हो सकती हैं। इस अंक का संदेश है: शरीर और वित्त को गंभीरता से लें। उचित चिकित्सा सलाह लें और धीरे-धीरे निर्माण करें।",
        "category": "Health & Difficulty",
    },
    30: {
        "topic": "Children's Joy / Inheritance / Reunion",
        "topic_hi": "बच्चों की खुशी / विरासत / मेलमिलाप",
        "detail": "Joy and togetherness fill your thoughts — the happiness of children, an inheritance or valuable dowry, or the reunion of people who have been apart. You may be thinking about a social group, an organisation, or a joyful family gathering. This number brings warmth and unity. Use this energy to mend broken relationships and share what you have with those you love.",
        "detail_hi": "खुशी और एकजुटता आपके विचारों में भरी है — बच्चों की खुशी, कोई विरासत, या अलग हुए लोगों का पुनर्मिलन। आप किसी सामाजिक समूह, संगठन, या खुशनुमा पारिवारिक मेल के बारे में सोच रहे हैं। इस ऊर्जा का उपयोग टूटे रिश्ते ठीक करने में करें।",
        "category": "Family & Joy",
    },
    31: {
        "topic": "Underground Things / Reptiles in House / Foreign",
        "topic_hi": "भूमिगत वस्तु / घर में जीव-जन्तु / विदेश",
        "detail": "Your thoughts are in hidden or underground territory — something buried, concealed, or not yet in the open. There may be a concern about snakes, scorpions, or pests entering the home. Foreign connections or matters from abroad are also significant here. Investigate what lies beneath the surface before making decisions; all is not as visible as it appears.",
        "detail_hi": "आपके विचार छिपे या भूमिगत क्षेत्र में हैं — कुछ दबा हुआ, छिपा हुआ, या अभी सामने नहीं आया। घर में सर्प, बिच्छू या कीट की चिंता हो सकती है। विदेशी संपर्क भी यहाँ महत्वपूर्ण हैं। निर्णय करने से पहले सतह के नीचे की जाँच करें।",
        "category": "Foreign & Hidden",
    },
    32: {
        "topic": "King / Government / Gold Investment / Personality",
        "topic_hi": "राजा / सरकार / सुवर्ण निवेश / व्यक्तित्व",
        "detail": "Power, authority, and leadership are on your mind — a king-like figure, a government body, or someone with great influence. You may be thinking about a wise investment in gold or a high-value asset, or reflecting deeply on your own character and reputation. This is a time to think and act like a leader: be decisive, act with integrity, and invest wisely in things of lasting value.",
        "detail_hi": "शक्ति, अधिकार और नेतृत्व आपके मन पर है — कोई प्रभावशाली व्यक्ति, सरकारी संस्था, या महान प्रभाव वाला कोई। सोने में निवेश या अपने चरित्र पर गहरा चिंतन भी हो सकता है। नेता की तरह सोचें और कार्य करें: निर्णायक रहें, ईमानदारी से काम करें।",
        "category": "Authority & Wealth",
    },
    33: {
        "topic": "Happy News / Good Position / Achievement / Brother",
        "topic_hi": "हर्षदायक समाचार / अच्छा पद / उपलब्धि / भाई",
        "detail": "Success and recognition are on your mind — a promotion, an achievement, an award, or simply the relief of receiving very good news. A brother or male companion may play a central role in this positive development. This is an auspicious number indicating that your efforts are being noticed. Take pride in what you have built and share your success generously with those who supported you.",
        "detail_hi": "सफलता और पहचान आपके मन पर है — पदोन्नति, उपलब्धि, पुरस्कार, या बहुत अच्छी खबर मिलने की राहत। कोई भाई या पुरुष साथी इस सकारात्मक घटनाक्रम में केंद्रीय भूमिका निभा सकता है। यह शुभ अंक है — अपनी मेहनत पर गर्व करें।",
        "category": "Success",
    },
    34: {
        "topic": "Financial Gain / Food / Daily Necessities / Purchase",
        "topic_hi": "आर्थिक लाभ / भोजन / दैनिक आवश्यकताएं / खरीद",
        "detail": "Your thoughts are grounded in the practical and material — food, grain, money, daily household needs, or a purchase you are planning. Financial gain of a tangible, everyday kind is indicated. This number is less about grand wealth and more about reliable, steady provision. Focus on managing your daily finances well, stocking up on essentials, and making sound practical purchases.",
        "detail_hi": "आपके विचार व्यावहारिक और भौतिक में आधारित हैं — भोजन, अन्न, धन, दैनिक घरेलू जरूरतें, या योजनाबद्ध खरीदारी। ठोस, रोजमर्रा के प्रकार का वित्तीय लाभ संकेतित है। दैनिक वित्त अच्छे से संभालें, जरूरी चीजें एकत्र करें।",
        "category": "Finance & Daily Life",
    },
    35: {
        "topic": "Woman / Child Birth / Secret Plan / Solitude",
        "topic_hi": "स्त्री / बालक का जन्म / गुप्त योजना / एकान्तवास",
        "detail": "A woman holds a central place in your thoughts — or you are thinking about the birth of a child, a secret plan you are crafting, or a period of solitude and inner reflection. There may be a conspiracy or hidden scheme around you that needs careful attention. If planning something privately, ensure your intentions are pure. New life and new beginnings are also strongly indicated here.",
        "detail_hi": "कोई महिला आपके विचारों में केंद्रीय स्थान रखती है — या आप किसी बच्चे के जन्म, गुप्त योजना, या एकांत और आंतरिक चिंतन की अवधि के बारे में सोच रहे हैं। यदि निजी योजना बना रहे हैं, तो सुनिश्चित करें कि इरादे शुद्ध हों।",
        "category": "Family & Secrets",
    },
    36: {
        "topic": "Gambling Loss / Sick Child / Family Suffering",
        "topic_hi": "सट्टे में हानि / बीमार बच्चा / परिवार का दुःख",
        "detail": "Pain within the family weighs heavily on your mind — a child who is unwell, a domestic situation filled with sorrow, or the aftermath of a risky gamble or failed employment. This is a time for compassion rather than criticism. Attend to the health and emotional needs of those around you, and step away from any form of speculation or financial risk until the situation stabilises.",
        "detail_hi": "परिवार का दर्द आपके मन पर भारी है — कोई बीमार बच्चा, दुःख से भरी घरेलू स्थिति, या किसी जोखिम भरे सट्टे का परिणाम। यह आलोचना के बजाय करुणा का समय है। जब तक स्थिति स्थिर न हो, सट्टे या वित्तीय जोखिम से दूर रहें।",
        "category": "Difficulty",
    },
    37: {
        "topic": "Failed Contract / Unhappy Marriage / Property",
        "topic_hi": "असफल अनुबंध / दुखी विवाह / मकान-जायदाद",
        "detail": "An agreement or relationship that has not fulfilled its promise is on your mind. A contract that brought poor results, a marriage that is not going smoothly, or a property dispute may be causing stress. Review the terms of any active agreements and be honest about what needs to change. Property matters may also require legal attention — do not delay addressing what is clearly not working.",
        "detail_hi": "कोई समझौता या रिश्ता जो अपना वादा पूरा नहीं कर सका, आपके मन पर है। खराब परिणाम वाला अनुबंध, असुखी विवाह, या संपत्ति विवाद तनाव का कारण हो सकता है। किसी भी सक्रिय समझौते की शर्तों की समीक्षा करें और ईमानदार रहें।",
        "category": "Relationships & Property",
    },
    38: {
        "topic": "Fever / Illness / Nearby Water Body / Sister",
        "topic_hi": "बुखार / मलेरिया / निकट जलाशय / बहन",
        "detail": "A health concern — fever, malaria, or physical discomfort — is at the forefront of your mind, or you are thinking about a sister or female relative. A nearby pond, lake, or water body has relevance. You may be expecting a message or preparing for a short journey. Attend promptly to any health symptoms and check in on female relatives who may need your support.",
        "detail_hi": "एक स्वास्थ्य चिंता — बुखार, मलेरिया, या शारीरिक असुविधा — आपके मन में सबसे आगे है, या आप किसी बहन या महिला संबंधी के बारे में सोच रहे हैं। पास का तालाब या जलाशय प्रासंगिक है। स्वास्थ्य लक्षणों पर तुरंत ध्यान दें।",
        "category": "Health",
    },
    39: {
        "topic": "Closed Place / Temple / Going Out / Eviction",
        "topic_hi": "बन्द जगह / मन्दिर / बाहर जाना / निष्कासन",
        "detail": "Your thoughts are about departure, sacred spaces, or a forced change of location. You may be drawn to visit a temple, a grand building, or a place of spiritual significance. Alternatively, you may be facing eviction, a transfer, or the need to leave somewhere that has been home. If the departure is chosen, embrace it; if forced, seek legal counsel and know your rights.",
        "detail_hi": "आपके विचार प्रस्थान, पवित्र स्थानों, या जबरन स्थान परिवर्तन के बारे में हैं। आप किसी मंदिर, भव्य भवन, या आध्यात्मिक स्थान जाने के लिए आकर्षित हो सकते हैं। यदि प्रस्थान स्वैच्छिक है तो अपनाएं; यदि मजबूरी है तो कानूनी सलाह लें।",
        "category": "Travel & Spiritual",
    },
    40: {
        "topic": "Valuables / Jewelry / Clothes / Grain Prices",
        "topic_hi": "बहुमूल्य वस्तुएं / जेवलरी / वस्त्र / अन्न मूल्य",
        "detail": "Material possessions and their worth are on your mind — jewelry, precious stones, fine clothing, or the rising and falling prices of food commodities. You may be considering buying or selling valuables, or tracking the market for household essentials. Guard your possessions carefully. This is also a good time to appreciate the value of what you already own rather than chasing new acquisitions.",
        "detail_hi": "भौतिक संपत्ति और उनका मूल्य आपके मन पर है — जेवलरी, कीमती पत्थर, अच्छे कपड़े, या खाद्य वस्तुओं के बढ़ते-घटते मूल्य। जो आपके पास पहले से है उसकी कदर करें; नई चीजें खोजने की जल्दबाजी न करें।",
        "category": "Wealth & Possessions",
    },
    41: {
        "topic": "Self — Dress / Food / Reputation / Fame",
        "topic_hi": "स्वयं — पोशाक / भोजन / प्रतिष्ठा / नेकनामी",
        "detail": "This number brings your focus squarely back to yourself — how you present yourself to the world, what you eat, your current standing in society, and your reputation. Are you proud of how others see you? Is your name associated with good deeds or controversy? This is a moment for honest self-reflection. Invest in your appearance, your diet, and your public character.",
        "detail_hi": "यह अंक आपका ध्यान पूरी तरह खुद पर वापस लाता है — आप दुनिया के सामने खुद को कैसे प्रस्तुत करते हैं, क्या खाते हैं, समाज में आपकी स्थिति, और आपकी प्रतिष्ठा। ईमानदार आत्म-चिंतन का यह क्षण है। अपनी उपस्थिति, आहार और सार्वजनिक चरित्र में निवेश करें।",
        "category": "Self",
    },
    42: {
        "topic": "High-Position Woman / Official's Favor / Large Crowd",
        "topic_hi": "उच्च पदस्थ महिला / अधिकारी की कृपा / जनसमूह",
        "detail": "You are thinking about people in power — a high-ranking woman, a government official, or someone whose approval you need. A large public gathering, a fair, or a social event may also be on your mind. Their favour can open doors for you. Be respectful, well-prepared, and approach authority figures with confidence; this is a good time to make your case to those who can help you.",
        "detail_hi": "आप शक्ति में बैठे लोगों के बारे में सोच रहे हैं — कोई उच्च पदस्थ महिला, सरकारी अधिकारी, या जिसकी स्वीकृति आपको चाहिए। उनकी कृपा आपके लिए दरवाजे खोल सकती है। सम्मान के साथ, तैयार होकर अधिकारी के पास जाएं।",
        "category": "Social & Authority",
    },
    43: {
        "topic": "Ancestral Property / Old Building / Minerals / Elder",
        "topic_hi": "पैतृक सम्पत्ति / पुरानी इमारत / खनिज / वृद्ध पुरुष",
        "detail": "Your thoughts are rooted in the past — ancestral property, an old family home or crumbling building, mineral resources buried in land, or the wisdom of an elderly man. There may be an inheritance dispute, a renovation project, or the need to reconnect with your roots. Honour the elders around you; their experience holds the key to resolving what you are facing.",
        "detail_hi": "आपके विचार अतीत में जड़े हैं — पैतृक संपत्ति, पुराना पारिवारिक घर, भूमि में दबे खनिज संसाधन, या किसी वृद्ध पुरुष की बुद्धिमत्ता। विरासत विवाद या नवीनीकरण परियोजना हो सकती है। अपने आसपास के बुजुर्गों का सम्मान करें; उनका अनुभव आपकी समस्या की चाबी है।",
        "category": "Property & Elders",
    },
    44: {
        "topic": "Brother / Health / Religious Texts / Overseas Letter",
        "topic_hi": "भाई / स्वास्थ्य / धार्मिक ग्रन्थ / विदेश से पत्र",
        "detail": "A brother is prominent in your thoughts, or you are reflecting on your health and personal comfort. Sacred texts, scriptures, or spiritual knowledge may be calling your attention. There may also be a letter or communication coming from someone overseas. This is a good time to deepen your knowledge through reading and to strengthen bonds with siblings.",
        "detail_hi": "कोई भाई आपके विचारों में प्रमुख है, या आप अपने स्वास्थ्य और व्यक्तिगत आराम पर विचार कर रहे हैं। पवित्र ग्रंथ या आध्यात्मिक ज्ञान आपका ध्यान आकर्षित कर सकता है। विदेश से कोई पत्र आ सकता है। भाई-बहनों के साथ संबंध मजबूत करने का यह अच्छा समय है।",
        "category": "Family & Spiritual",
    },
    45: {
        "topic": "Marriage / Fraud / Injustice / Cheap Items",
        "topic_hi": "विवाह / धोखाधड़ी / अन्याय / कम मूल्य की वस्तु",
        "detail": "Your mind is wrestling with fairness — a marriage that may involve compromise, a situation of fraud or deception, or an injustice that has been done to you. Low-value items or transactions may also be involved. Be vigilant about who you trust with your money and your heart. If you sense something is biased or dishonest, trust that instinct and investigate further before committing.",
        "detail_hi": "आपका मन निष्पक्षता से जूझ रहा है — एक विवाह जिसमें समझौता हो सकता है, धोखाधड़ी की स्थिति, या आपके साथ हुआ अन्याय। जिस पर पैसा और दिल भरोसा करते हैं उसके बारे में सतर्क रहें। अगर कुछ पक्षपाती लगे तो प्रतिबद्ध होने से पहले जाँच करें।",
        "category": "Relationships",
    },
    46: {
        "topic": "Friend / High Official / Gold / Jewelry / Valuables",
        "topic_hi": "मित्र / उच्च पदाधिकारी / सोना / जेवलरी / बहुमूल्य वस्तु",
        "detail": "A trusted friend or a high-ranking official is at the centre of your thoughts, and their involvement brings with it the energy of gold, jewelry, and valuable things. You may be thinking about gifting, purchasing, or receiving something precious. This is a favourable number for making connections with powerful people. Nurture the friendship or professional relationship — it can bring lasting material benefit.",
        "detail_hi": "कोई विश्वसनीय मित्र या उच्च पदस्थ अधिकारी आपके विचारों के केंद्र में है, और उनकी भागीदारी सोने, जेवलरी और मूल्यवान चीजों की ऊर्जा लाती है। यह प्रभावशाली लोगों के साथ संपर्क बनाने के लिए अनुकूल अंक है। यह दोस्ती या पेशेवर रिश्ते को पोषित करें।",
        "category": "Wealth & Social",
    },
    47: {
        "topic": "Self / Justice / Lawsuit / Peace / Death",
        "topic_hi": "स्वयं / न्याय / मुकदमा / शान्ति / मृत्यु",
        "detail": "Deep and weighty matters concerning yourself are on your mind — a question of justice, an active lawsuit, the need to measure or weigh a situation carefully, or thoughts about mortality and peace. This number asks you to be truthful with yourself above all else. If a legal matter is pending, get proper counsel. If it is peace you seek, it begins within you.",
        "detail_hi": "आपसे जुड़े गहरे और भारी मामले आपके मन पर हैं — न्याय का सवाल, कोई मुकदमा, किसी स्थिति का सावधानी से मूल्यांकन, या मृत्यु और शांति के विचार। यह अंक मांग करता है कि आप सबसे पहले खुद के साथ सच्चे रहें। यदि कानूनी मामला लंबित है, उचित सलाह लें।",
        "category": "Self & Justice",
    },
    48: {
        "topic": "Inner Rooms / Hidden Servant / Woman's Health / Distant Message",
        "topic_hi": "घर के भीतरी हिस्से / छिपे नौकर / महिला स्वास्थ्य / दूर से संवाद",
        "detail": "Your focus is on the hidden and domestic — the inner rooms of your home, clothing and personal presentation, a servant or helper who may have gone missing or is behaving secretively. A woman's health is also a concern. A message from a distant place is on its way. Pay attention to what is happening quietly behind the scenes in your household.",
        "detail_hi": "आपका ध्यान छिपे और घरेलू पर है — घर के भीतरी कमरे, पोशाक और व्यक्तिगत प्रस्तुति, एक नौकर जो गायब हो गया हो या गुप्त व्यवहार कर रहा हो। किसी महिला का स्वास्थ्य भी चिंता का विषय है। दूर से एक संदेश आने वाला है। अपने घर में पर्दे के पीछे जो हो रहा है उस पर ध्यान दें।",
        "category": "Home & Health",
    },
    49: {
        "topic": "Change of Position / Mother / Queen / High-Position Woman",
        "topic_hi": "पद/स्थान परिवर्तन / माता / रानी / उच्चपदस्थ महिला",
        "detail": "A significant change in your role, position, or physical location is on your mind. Your mother or a mother-figure holds great importance right now, or you are dealing with a powerful woman in authority. This number signals transition — something is shifting in your life. Embrace the change rather than resisting it; the new position or place will bring opportunities the old one could not.",
        "detail_hi": "आपकी भूमिका, पद, या स्थान में महत्वपूर्ण बदलाव आपके मन पर है। आपकी माँ या माँ जैसी कोई शख्सियत अभी बहुत महत्वपूर्ण है। यह अंक संक्रमण का संकेत देता है — जीवन में कुछ बदल रहा है। बदलाव को स्वीकार करें; नया स्थान या पद नए अवसर लाएगा।",
        "category": "Change & Women",
    },
    50: {
        "topic": "Difficult Journey / Distressed Sister / Sad News",
        "topic_hi": "कष्टदायक यात्रा / कष्ट में बहन / दुखद समाचार",
        "detail": "Something painful and unwelcome is on its way — a difficult journey you must take out of duty, a sister or female relative who is in distress and needs your help, or sad news that will arrive soon. You may feel summoned to a situation that you would rather avoid. Answer the call with courage; your presence and support can make a real difference to someone who is struggling.",
        "detail_hi": "कुछ दर्दनाक और अनचाहा आने वाला है — एक कठिन यात्रा जो कर्तव्य से करनी होगी, कोई बहन या महिला संबंधी जो कष्ट में है, या दुखद खबर। साहस के साथ बुलावे का जवाब दें; आपकी उपस्थिति और समर्थन किसी संघर्षरत व्यक्ति के लिए वास्तविक फर्क ला सकता है।",
        "category": "Difficulty & Family",
    },
    51: {
        "topic": "Abundant Financial Gain / Lottery / Children / Money from Afar",
        "topic_hi": "प्रचुर आर्थिक लाभ / सट्टा-लॉटरी / बच्चे / दूर से धन",
        "detail": "A windfall of wealth is on your mind — whether from a lottery, a big bet, a new job, or money arriving from a distant source. Children may also play a joyful role in what you are thinking about. The financial energy here is abundant and optimistic. However, good fortune rewards the prepared: have a plan for how you will use or invest any money that comes your way.",
        "detail_hi": "धन की झोली आपके मन में है — लॉटरी, बड़ी शर्त, नौकरी, या दूर से आने वाले धन से। बच्चे भी खुशनुमा भूमिका निभा सकते हैं। वित्तीय ऊर्जा यहाँ प्रचुर और आशावादी है। लेकिन सौभाग्य तैयार लोगों को पुरस्कृत करता है: जो भी धन आए उसके उपयोग की योजना रखें।",
        "category": "Wealth & Family",
    },
    52: {
        "topic": "Disease / Death / Hidden Item / Doctor / Tantra / Reptiles",
        "topic_hi": "रोग/मृत्यु / छिपी वस्तु / डॉक्टर / तन्त्र / सर्पादि",
        "detail": "Dark or hidden energies are on your mind — a serious illness, the fear of death, a lost or concealed item, or matters involving doctors and medical treatment. Tantric practices, occult knowledge, or reptiles in or near the home may also be of concern. Face what is hidden rather than avoiding it. Seek medical attention promptly if health is the concern; do not delay.",
        "detail_hi": "अंधेरी या छिपी ऊर्जाएं आपके मन पर हैं — गंभीर बीमारी, मृत्यु का डर, खोई या छिपी वस्तु, या डॉक्टरों और चिकित्सा से जुड़े मामले। तंत्र विद्या या घर के पास सर्पादि जीव भी चिंता का कारण हो सकते हैं। छिपे को टालने के बजाय सामना करें। स्वास्थ्य चिंता है तो तुरंत चिकित्सा लें।",
        "category": "Health & Hidden",
    },
    53: {
        "topic": "High Position / Job / King / Lost Gold",
        "topic_hi": "उच्च पद / नौकरी / राजा / खोया सोना",
        "detail": "Ambition and authority are in your thoughts — a coveted position, a job you are hoping to get or keep, or the power and influence of a king-like figure. Lost gold or valuable possessions may also be on your mind. This is a time to assert yourself professionally and pursue positions of leadership. Do not undersell your abilities; step forward with confidence.",
        "detail_hi": "महत्वाकांक्षा और अधिकार आपके विचारों में हैं — एक प्रतिष्ठित पद, वह नौकरी जो पाना चाहते हैं, या राजा जैसी किसी शख्सियत की शक्ति। खोया हुआ सोना भी मन में हो सकता है। व्यावसायिक रूप से आगे बढ़ें और नेतृत्व के पदों का पीछा करें।",
        "category": "Authority & Wealth",
    },
    54: {
        "topic": "Infectious Disease / Distressed Woman / Promise / Contract",
        "topic_hi": "संक्रामक रोग / कष्ट में महिला / वायदा / अनुबंध",
        "detail": "A contagious illness, a woman in pain, or a promise that has been broken — these are the themes weighing on you. Your wife, daughter, or another important woman in your life may need your attention and care. There may also be a contract or enclosed agreement that requires review. Keep your promises and attend to the health and wellbeing of the women in your circle.",
        "detail_hi": "एक संक्रामक बीमारी, कष्ट में महिला, या टूटा हुआ वादा — ये आप पर भारी विषय हैं। आपकी पत्नी, बेटी, या कोई महत्वपूर्ण महिला को आपके ध्यान और देखभाल की जरूरत हो सकती है। अपने वादे रखें और अपने घेरे की महिलाओं के स्वास्थ्य का ध्यान रखें।",
        "category": "Health & Relationships",
    },
    55: {
        "topic": "Death / Lost Documents / Young Girl / Crowd",
        "topic_hi": "मृत्यु / खोए कागज / नई लड़की / जनसमूह",
        "detail": "Loss looms large in your thoughts — the death of someone, important papers or documents that have gone missing, a message that did not reach its destination, or a young girl who is a focus of concern. A large crowd or social gathering may also be relevant. Search carefully for what has been misplaced, and be gentle in your dealings with the young and vulnerable around you.",
        "detail_hi": "नुकसान आपके विचारों में बड़ा है — किसी की मृत्यु, गुम हुए महत्वपूर्ण दस्तावेज, गलत जगह पहुंचा संदेश, या कोई युवा लड़की जो चिंता का केंद्र है। जो खो गया है उसे सावधानी से खोजें और अपने आसपास के युवा और कमजोर लोगों के साथ कोमल रहें।",
        "category": "Loss",
    },
    56: {
        "topic": "Overseas / Sea Voyage / Religious Conference / Shakti",
        "topic_hi": "विदेश / समुद्रयात्रा / धार्मिक सम्मेलन / शक्ति",
        "detail": "Your thoughts stretch across oceans and spiritual realms — a foreign land, a sea voyage, a religious gathering or conference, or the fierce and protective energy of the Goddess (Durga, Kali, Shakti). You may be drawn to publish something, set sail literally or metaphorically, or connect with divine feminine power. This is a powerful, expansive number; act with courage and faith.",
        "detail_hi": "आपके विचार समुद्रों और आध्यात्मिक क्षेत्रों में फैले हैं — विदेश, समुद्रयात्रा, धार्मिक सम्मेलन, या देवी (दुर्गा, काली, शक्ति) की उग्र और रक्षात्मक ऊर्जा। साहस और विश्वास के साथ कार्य करें; यह शक्तिशाली, विस्तारशील अंक है।",
        "category": "Spiritual & Foreign",
    },
    57: {
        "topic": "Treasure / Inheritance / Pension / Male Relative",
        "topic_hi": "खजाना / विरासत / पेंशन / पुरुष संबंधी",
        "detail": "Stored or inherited wealth is on your mind — a treasure, a stockpile of resources, an expected inheritance, or a pension that is due. A male relative — father, uncle, or older brother — may be connected to this financial matter. This is a number of accumulated wealth rather than sudden gains. Be patient; what is owed to you will eventually reach your hands.",
        "detail_hi": "संचित या विरासत में मिली संपत्ति आपके मन पर है — खजाना, संसाधनों का भंडार, प्रत्याशित विरासत, या देय पेंशन। कोई पुरुष संबंधी — पिता, चाचा, या बड़ा भाई — इस वित्तीय मामले से जुड़ा हो सकता है। धैर्य रखें; जो आपका है वह अंततः आपके पास आएगा।",
        "category": "Wealth & Family",
    },
    58: {
        "topic": "Lawyer / Judge / Guru / Scripture / Personal Property",
        "topic_hi": "वकील / जज / गुरु / शास्त्र / व्यक्तिगत जायदाद",
        "detail": "Your mind is engaged with authority, wisdom, and law — a lawyer whose advice you need, a judge whose decision will affect you, a guru or spiritual teacher, or sacred scriptures that hold answers. Personal property and its legal protection are also highlighted. Seek knowledgeable counsel before making any major legal or property decision; wisdom is your greatest asset right now.",
        "detail_hi": "आपका मन अधिकार, बुद्धिमत्ता और कानून में लगा है — जिस वकील की सलाह चाहिए, जिस जज का फैसला प्रभावित करेगा, कोई गुरु या पवित्र ग्रंथ। व्यक्तिगत संपत्ति और उसकी कानूनी सुरक्षा भी महत्वपूर्ण है। कोई बड़ा कानूनी या संपत्ति निर्णय लेने से पहले जानकार की सलाह लें।",
        "category": "Legal & Spiritual",
    },
    59: {
        "topic": "Hospital / House Fire / Adventure / Industry",
        "topic_hi": "अस्पताल / घर में आग / साहसिक कार्य / उद्योग",
        "detail": "Your thoughts oscillate between danger and daring — a hospital room, a fire in the home, a risky or adventurous project, or an industrial venture. A child may be involved in one of these situations. Fire as a symbol here represents both destruction and transformation. If pursuing an ambitious industrial or adventurous goal, proceed with caution and strong safety measures.",
        "detail_hi": "आपके विचार खतरे और साहस के बीच झूल रहे हैं — अस्पताल का कमरा, घर में आग, एक जोखिम भरा उद्यम, या औद्योगिक प्रयास। अग्नि यहाँ विनाश और परिवर्तन दोनों का प्रतीक है। यदि महत्वाकांक्षी लक्ष्य का पीछा कर रहे हैं, तो सावधानी और मजबूत सुरक्षा उपायों के साथ आगे बढ़ें।",
        "category": "Health & Adventure",
    },
    60: {
        "topic": "Fire Ritual / Sage / God / Time / Foreign King",
        "topic_hi": "हवन / ऋषि / ईश्वर / काल / विदेशी राजा",
        "detail": "The highest, most sacred energies are on your mind — a fire ritual (havan), a saintly sage, the concept of God, the flow of cosmic time, or a foreign king or dignitary. You may be seeking divine guidance or contemplating life's deepest questions. This is a deeply spiritual number; meditate, pray, and surrender what you cannot control. The universe has a plan that is larger than what you can currently see.",
        "detail_hi": "सर्वोच्च, सबसे पवित्र ऊर्जाएं आपके मन पर हैं — हवन, कोई संत ऋषि, ईश्वर की अवधारणा, ब्रह्मांडीय समय का प्रवाह, या कोई विदेशी राजा। आप दिव्य मार्गदर्शन मांग रहे हों या जीवन के गहरे प्रश्नों पर विचार कर रहे हों। ध्यान करें, प्रार्थना करें; ब्रह्मांड की एक योजना है।",
        "category": "Spiritual & Divine",
    },
    61: {
        "topic": "Food / Trade / Fine Clothes / Market / Brahmin",
        "topic_hi": "भोजन / व्यापार / उत्तम वस्त्र / बाजार / ब्राह्मण",
        "detail": "Commerce, nourishment, and social networks are on your mind — buying and selling in the marketplace, food and grain trade, fine clothing, or a friendship with a learned or spiritually elevated person. The market and the merchant hold the answers you seek. This is a good time to pursue trade, stock up on provisions, and connect with people of wisdom or commerce.",
        "detail_hi": "व्यापार, पोषण और सामाजिक नेटवर्क आपके मन पर है — बाजार में खरीद-बिक्री, भोजन और अनाज व्यापार, अच्छे कपड़े, या किसी विद्वान व्यक्ति के साथ मित्रता। यह व्यापार करने, आपूर्ति संग्रहित करने और बुद्धिमान लोगों से जुड़ने का अच्छा समय है।",
        "category": "Trade & Food",
    },
    62: {
        "topic": "Contract / Legal Action / Property / Father",
        "topic_hi": "अनुबंध / कानूनी कार्यवाही / जायदाद / पिता",
        "detail": "Legal and formal matters dominate your thinking — a written article, contract, promise, or an ongoing legal dispute. Property and its ownership are at the heart of it, and your father or a father-figure may be directly involved. Before signing anything, read every clause carefully. Your father's guidance, or advice modelled on fatherly wisdom, will serve you well here.",
        "detail_hi": "कानूनी और औपचारिक मामले आपके विचारों पर हावी हैं — कोई लिखित लेख, अनुबंध, वादा, या चल रहा कानूनी विवाद। संपत्ति और उसका स्वामित्व इसके केंद्र में है, और आपके पिता या पिता जैसी शख्सियत सीधे शामिल हो सकती है। कुछ भी हस्ताक्षर करने से पहले हर धारा ध्यान से पढ़ें।",
        "category": "Legal & Family",
    },
    63: {
        "topic": "Dead Woman / Lost Property / Waning Moon / Dowry",
        "topic_hi": "मृत स्त्री / खोई जायदाद / क्षीण चन्द्रमा / स्त्री-धन",
        "detail": "Grief, endings, and loss are present in your thoughts — the death of a woman, property that has gone missing, the fading light of a waning moon, or matters around a woman's dowry or personal wealth. This number asks you to process loss with dignity and not cling to what has passed. Complete what needs to be completed, conduct the final rites, and allow closure to come.",
        "detail_hi": "दुःख, अंत, और नुकसान आपके विचारों में मौजूद हैं — किसी महिला की मृत्यु, गुम हुई संपत्ति, क्षीण चंद्रमा, या महिला के दहेज या व्यक्तिगत संपत्ति के मामले। यह अंक आपसे गरिमा के साथ नुकसान को स्वीकार करने को कहता है। जो जाना है उसे जाने दें।",
        "category": "Grief & Loss",
    },
    64: {
        "topic": "Own Position / Inherited Property / Old Man / Deal / Time",
        "topic_hi": "अपना पद / विरासत / वृद्ध व्यक्ति / सौदा / समय",
        "detail": "Your standing in the world and what you have built or inherited occupy your mind. An old man — possibly a grandfather or elderly relative — holds significance, or there is a deal, an exchange, or a time-sensitive matter to resolve. This number asks you to value time itself as a precious resource. Make your decisions now rather than postponing, because time is moving on.",
        "detail_hi": "दुनिया में आपकी स्थिति और जो आपने बनाया या विरासत में पाया, वह आपके मन में है। एक बुजुर्ग पुरुष — दादा या वृद्ध संबंधी — महत्वपूर्ण है, या कोई सौदा या समय-संवेदनशील मामला है। अभी निर्णय लें, टालने से काम नहीं चलेगा।",
        "category": "Self & Property",
    },
    65: {
        "topic": "Short Journey / Sister / Secret Counsel / Closed Room",
        "topic_hi": "छोटी यात्रा / बहन / गुप्त मंत्रणा / बन्द कमरा",
        "detail": "Movement and private conversation are at the heart of your thoughts — a short trip you need to take and come back from, a sister who needs your presence, or a confidential meeting where important decisions will be made. A closed room or private space holds significance. Trust the people you are meeting privately, but be careful about what you reveal to the wider world.",
        "detail_hi": "गतिविधि और निजी बातचीत आपके विचारों के केंद्र में है — एक छोटी यात्रा, कोई बहन जिसे आपकी उपस्थिति चाहिए, या एक गोपनीय बैठक जहाँ महत्वपूर्ण निर्णय होंगे। जिनसे निजी तौर पर मिल रहे हैं उन पर भरोसा करें, लेकिन व्यापक दुनिया को क्या बताते हैं इसमें सावधान रहें।",
        "category": "Travel & Secrets",
    },
    66: {
        "topic": "Crematorium / Mountain / Minerals / Burning House / Sand",
        "topic_hi": "श्मशान / पर्वत / खनिज / जलता घर / रेत",
        "detail": "Heavy, elemental energies fill your thoughts — death, the crematorium, a mountain or rocky terrain, minerals underground, a healer or doctor, or the image of fire consuming a home. Dry land and sand are also present. This number often signals the need to face mortality or impermanence honestly. Seek healing, get medical help if needed, and let go of what can no longer be saved.",
        "detail_hi": "भारी, मूलभूत ऊर्जाएं आपके विचारों में भरी हैं — मृत्यु, श्मशान, पहाड़ी भूभाग, भूमिगत खनिज, कोई वैद्य, या अग्नि से जलता घर। यह अंक अक्सर नश्वरता का ईमानदारी से सामना करने का संकेत देता है। चिकित्सा सहायता लें और जो बचाया नहीं जा सकता उसे जाने दें।",
        "category": "Dark & Earth",
    },
    67: {
        "topic": "Dead King / Lost Gold / Woman's Dowry / Sick Child",
        "topic_hi": "मृत राजा / खोया सोना / स्त्री का दहेज / बीमार बच्चा",
        "detail": "Loss in positions of power and loss of precious things are your twin concerns — the fall of a leader, gold that has been lost or stolen, a woman's dowry that is at risk, or a child who is unwell and needs care. This number calls for grief and practical response in equal measure. Protect what remains and focus your energy on the vulnerable — the child who needs you most.",
        "detail_hi": "शक्ति के पदों में हानि और कीमती चीजों की हानि आपकी दोहरी चिंता है — एक नेता का पतन, खोया या चोरी हुआ सोना, जोखिम में महिला का दहेज, या बीमार बच्चा। दुःख और व्यावहारिक प्रतिक्रिया दोनों की जरूरत है। जो बचा है उसकी रक्षा करें और बच्चे पर ध्यान दें।",
        "category": "Grief & Family",
    },
    68: {
        "topic": "Young Girl / Family / Trustworthy Position / Bail",
        "topic_hi": "छोटी उम्र की कन्या / कुटुम्ब / विश्वास योग्य पद / जमानत",
        "detail": "A young girl — perhaps a daughter, niece, or a young woman in your care — holds the centre of your attention, or a family matter requires immediate resolution. You may be seeking a trustworthy position or person you can rely on completely, or there is a bail or guarantee situation involving someone close to you. Act as the responsible guardian figure your loved ones need right now.",
        "detail_hi": "एक युवा लड़की — शायद बेटी, भतीजी, या आपकी देखभाल में कोई युवती — आपके ध्यान के केंद्र में है, या एक पारिवारिक मामले को तत्काल हल की जरूरत है। जमानत या गारंटी की स्थिति हो सकती है। अभी अपने प्रियजनों के लिए जिम्मेदार संरक्षक की तरह कार्य करें।",
        "category": "Family",
    },
    69: {
        "topic": "Clothes / Boat / Merchant Goods / Trade / Science",
        "topic_hi": "वस्त्र / नौका / सौदागरी सामान / व्यापार / विज्ञान",
        "detail": "Commerce, knowledge, and movement across water are prominent themes — clothes and textiles, a merchant's goods being transported by boat or ship, food-related trade, or the study of a science or Vedic discipline. You may be considering a trading venture or an intellectual pursuit. Both require preparation and the right vessel — whether a ship or a disciplined mind.",
        "detail_hi": "व्यापार, ज्ञान और पानी के पार गतिविधि प्रमुख विषय हैं — वस्त्र और वस्त्र उद्योग, नाव या जहाज से माल परिवहन, भोजन संबंधी व्यापार, या किसी विज्ञान या वैदिक अनुशासन का अध्ययन। दोनों के लिए तैयारी और सही साधन — चाहे जहाज हो या अनुशासित मन — की जरूरत है।",
        "category": "Trade & Travel",
    },
    70: {
        "topic": "Wife / Contract / Public Gathering / Full Moon",
        "topic_hi": "पत्नी / अनुबंध / जनसमूह / पूर्णिमा",
        "detail": "Your wife or a close female partner sits at the heart of your current thoughts, or there is a formal agreement that needs to be signed. A public gathering, a large assembly, or the full moon's auspicious energy may also be significant. The full moon is a time of completion and illumination; whatever you have been building will reach its fullness now. Honour your commitments.",
        "detail_hi": "आपकी पत्नी या कोई करीबी महिला साथी आपके वर्तमान विचारों के केंद्र में है, या कोई औपचारिक समझौता है जिस पर हस्ताक्षर होने हैं। पूर्णिमा की शुभ ऊर्जा महत्वपूर्ण है; जो आप बना रहे थे वह अब पूर्णता तक पहुंचेगा। अपनी प्रतिबद्धताओं का सम्मान करें।",
        "category": "Relationships & Spiritual",
    },
    71: {
        "topic": "Water Pot / Old Familiar Place / Friend / Social Contact",
        "topic_hi": "जलपात्र / पुराना जाना-पहचाना स्थान / मित्र / सम्पर्क",
        "detail": "Nostalgia and social connections are stirring in your mind — an old friend you haven't spoken to in a while, a familiar place you long to return to, or the simple image of a water vessel filled and ready. Human connections made in the past hold great value right now. Reach out to old contacts; a reunion or renewed friendship could bring unexpected benefit and comfort.",
        "detail_hi": "पुरानी यादें और सामाजिक संबंध आपके मन में जाग रहे हैं — कोई पुराना मित्र, कोई जाना-पहचाना स्थान जहाँ जाना चाहते हैं। पुराने संपर्कों को पुनर्जीवित करें; पुराने मित्र से मुलाकात अप्रत्याशित लाभ और आराम ला सकती है।",
        "category": "Social",
    },
    72: {
        "topic": "Money / Rich Friend / Religious Conference / Paired Items",
        "topic_hi": "धन / अमीर मित्र / धार्मिक सम्मेलन / जोड़े वाली वस्तु",
        "detail": "Wealth and spiritual community are intertwined in your thoughts — a wealthy friend or Brahmin whose support would be valuable, a religious conference or gathering, or paired objects like shoes, scissors, or sandals. Financial matters and spiritual matters reinforce each other here. Attend the gathering or reach out to the wealthy contact; generosity and devotion both lead to abundance.",
        "detail_hi": "धन और आध्यात्मिक समुदाय आपके विचारों में जुड़े हैं — एक धनी मित्र या ब्राह्मण जिसका समर्थन मूल्यवान होगा, एक धार्मिक सम्मेलन। आर्थिक और आध्यात्मिक मामले यहाँ एक-दूसरे को मजबूत करते हैं। उदारता और भक्ति दोनों समृद्धि की ओर ले जाते हैं।",
        "category": "Wealth & Spiritual",
    },
    73: {
        "topic": "Brother / Quick Journey / Angry Message / Inheritance / Writing",
        "topic_hi": "भाई / शीघ्र यात्रा / क्रोधयुक्त संदेश / उत्तराधिकार / लेखन",
        "detail": "Speed and urgency characterise this number — a quick journey that must be made, an angry or emotionally charged message that needs a measured response, inheritance matters that cannot wait, or something you need to put into writing. A brother is central. Do not reply impulsively to any heated message; take a breath, choose your words carefully, and respond with composure.",
        "detail_hi": "गति और तात्कालिकता इस अंक की विशेषता है — एक शीघ्र यात्रा, एक क्रोधित संदेश जिसे संयमित प्रतिक्रिया की जरूरत है, विरासत के मामले जो प्रतीक्षा नहीं कर सकते। किसी भी गर्म संदेश का आवेग में जवाब न दें; शांत होकर सावधानी से शब्द चुनें।",
        "category": "Family & Communication",
    },
    74: {
        "topic": "Shining Sun / Proud Wife / Powerful Enemy / Eyes / Shiny Object",
        "topic_hi": "चमकता सूर्य / गर्वीली पत्नी / शक्तिशाली शत्रु / आँखें / चमकीला पदार्थ",
        "detail": "Brilliance and confrontation are your themes — the radiance of the sun, a wife or female partner who carries herself with pride and confidence, or a powerful enemy whose strength you must not underestimate. Eyesight and clarity of vision are also symbolically present. This is a time to shine yourself while keeping a watchful eye on those who oppose you. Stay sharp and well-prepared.",
        "detail_hi": "चमक और टकराव आपके विषय हैं — सूर्य की आभा, एक गर्वीली और आत्मविश्वासी पत्नी, या एक शक्तिशाली शत्रु जिसे कम न आंकें। दृष्टि और स्पष्टता यहाँ प्रतीकात्मक रूप से मौजूद हैं। खुद चमकें और विरोधियों पर नजर रखें।",
        "category": "Power & Conflict",
    },
    75: {
        "topic": "Pleasant Place / Landlordship / Salvation / Buried Money / Cattle",
        "topic_hi": "खुशनुमा जगह / जमींदारी / मोक्ष / गड़ा धन / पशु",
        "detail": "Your mind stretches between the worldly and the spiritual — a beautiful place of comfort, landownership, cattle and agricultural wealth, buried or hidden money, or the ultimate aspiration of spiritual liberation (moksha). You may be balancing material ambition with a deeper spiritual longing. Both are valid; do not abandon either. Build your material foundation while nurturing your inner life.",
        "detail_hi": "आपका मन सांसारिक और आध्यात्मिक के बीच फैला है — एक सुंदर आरामदायक जगह, भू-स्वामित्व, पशु और कृषि संपदा, दबा हुआ धन, या मोक्ष की परम आकांक्षा। भौतिक आधार बनाएं और अपने आंतरिक जीवन को पोषित करें।",
        "category": "Wealth & Spiritual",
    },
    76: {
        "topic": "Son / School / Newly Married Bride / Celibate Youth",
        "topic_hi": "पुत्र / पाठशाला / नव परिणीता वधू / ब्रह्मचारी युवा",
        "detail": "Young life and new beginnings are at the heart of your thoughts — a son's future, an educational institution, the arrival of a new bride into the family, or a young person at the threshold of their journey. This number carries freshness and potential. Invest in education, welcome the new additions to your family circle warmly, and support the young people around you.",
        "detail_hi": "युवा जीवन और नई शुरुआत आपके विचारों के केंद्र में है — एक बेटे का भविष्य, एक शैक्षणिक संस्थान, परिवार में नई बहू का आगमन, या एक युवा व्यक्ति। शिक्षा में निवेश करें, परिवार में नए सदस्यों का स्वागत करें, अपने आसपास के युवाओं का समर्थन करें।",
        "category": "Family & Education",
    },
    77: {
        "topic": "Dhoti / Turban / Maid / Medicine / Water / Drinks",
        "topic_hi": "धोती / पगड़ी / नौकरानी / औषधि / जल / पीना-पिलाना",
        "detail": "Simple, essential things of daily domestic life occupy your thoughts — clothing, headwear, a maidservant, medicine, water, and what is drunk or offered to others. These are not grand matters but profoundly important ones; the daily acts of care, nourishment, and domestic routine are what hold a home together. Pay attention to health remedies and the small acts of service around you.",
        "detail_hi": "रोजमर्रा की घरेलू जीवन की सरल और आवश्यक चीजें आपके विचारों में हैं — वस्त्र, सिर के कपड़े, नौकरानी, दवाई, जल। ये बड़े मामले नहीं हैं लेकिन गहरे महत्वपूर्ण हैं; देखभाल, पोषण और घरेलू दिनचर्या घर को एक साथ रखती है।",
        "category": "Daily Life",
    },
    78: {
        "topic": "Old Friend / Hospital / Jail / Imprisoned Person",
        "topic_hi": "वृद्ध मित्र / अस्पताल / जेल / बन्धन में व्यक्ति",
        "detail": "Long-standing bonds and confined situations are on your mind — an old and dear friend, an institution of healing or punishment, or someone who is literally or metaphorically imprisoned and unable to move freely. Ancient relationships deserve renewed attention. If someone you care about is in a hospital or jail, your visit or your advocacy may mean more to them than you realise.",
        "detail_hi": "पुराने रिश्ते और बंधन की स्थितियां आपके मन पर हैं — एक पुराना प्रिय मित्र, कोई अस्पताल या जेल में व्यक्ति। पुराने रिश्तों पर नए सिरे से ध्यान दें। अगर कोई प्रिय अस्पताल या जेल में है, तो आपकी उपस्थिति या पैरवी उनके लिए अनमोल होगी।",
        "category": "Difficulty & Social",
    },
    79: {
        "topic": "Self-Growth / Footwear / Prosperity / Judge / Intelligence",
        "topic_hi": "स्वयं की वृद्धि / खड़ाऊँ / उन्नति / जज / बुद्धि",
        "detail": "Personal advancement and the limits of what you can achieve are on your mind. You may be thinking about how far you have come, how much further you can go, or the legal and intellectual resources that will help you get there — a judge, a lawyer, or your own sharp intelligence. Footwear and feet symbolise where you stand and where you are going. Stand firmly, think clearly, and keep moving forward.",
        "detail_hi": "व्यक्तिगत उन्नति और आप क्या हासिल कर सकते हैं, इसकी सीमाएं आपके मन पर हैं। आप सोच रहे होंगे कि कितना आगे आए हैं और कितना और जाना है। मजबूती से खड़े रहें, स्पष्ट सोचें और आगे बढ़ते रहें।",
        "category": "Growth & Success",
    },
    80: {
        "topic": "Profit-Loss Fear / Fire Damage / Death Abroad / Sea Voyage",
        "topic_hi": "लाभ-हानि की आशंका / अग्नि हानि / विदेश में मृत्यु / समुद्र यात्रा",
        "detail": "Risk and uncertainty dominate your thinking — the fear of losing what you have gained, damage caused by fire, the death of someone in a distant land, or the dangers of a sea voyage. This is not a number that encourages recklessness. Get insurance, take precautions against fire and risk, and if someone is travelling far, ensure they have what they need for safety.",
        "detail_hi": "जोखिम और अनिश्चितता आपके विचारों पर हावी है — जो कमाया उसे खोने का डर, आग से नुकसान, दूर देश में किसी की मृत्यु, या समुद्र यात्रा के खतरे। यह अपरिपक्वता को प्रोत्साहित करने वाला अंक नहीं है। बीमा लें, आग और जोखिम के खिलाफ सावधानी बरतें।",
        "category": "Risk & Travel",
    },
    81: {
        "topic": "Wealthy Relative / Gold Ornaments / Personal Health / Ripe Fruits",
        "topic_hi": "धनवान रिश्तेदार / सोने के आभूषण / स्वास्थ्य / पके फल",
        "detail": "Richness in its many forms fills your mind — a wealthy relative whose help could be significant, gold ornaments that carry both monetary and sentimental value, the ripeness of fruit as a symbol of good health and harvest, and your own personal vitality. This is a number of readiness and maturity. Things that have been growing are now ripe; act before the moment passes.",
        "detail_hi": "समृद्धि अपने कई रूपों में आपके मन को भरती है — एक धनी रिश्तेदार, सोने के आभूषण, अच्छे स्वास्थ्य और फसल के प्रतीक पके फल, और आपकी अपनी जीवन शक्ति। यह परिपक्वता और तत्परता का अंक है। जो बढ़ रहा था वह अब पका है; क्षण गुजरने से पहले कार्य करें।",
        "category": "Wealth & Health",
    },
    82: {
        "topic": "Peaceful End / Valuable Dowry / Happy News / Car / Sister",
        "topic_hi": "शान्तिपूर्ण अन्तिम समय / बहुमूल्य दहेज / हर्षदायक समाचार / सवारी / बहन",
        "detail": "Your thoughts are moving toward a peaceful and dignified conclusion — a matter that is drawing to a graceful close, a valuable dowry arrangement, happy news that brings the family together, or a comfortable journey (by car, vehicle, or even elephant in the classical sense). A sister holds special significance. This is a number of auspicious completions; trust that things are ending well.",
        "detail_hi": "आपके विचार एक शांतिपूर्ण और सम्मानजनक निष्कर्ष की ओर बढ़ रहे हैं — एक मामला जो सुंदर तरीके से समाप्त हो रहा है, एक मूल्यवान दहेज व्यवस्था, परिवार को एक साथ लाने वाली खुशखबरी। बहन का विशेष महत्व है। यह शुभ समापन का अंक है; विश्वास करें कि चीजें अच्छी तरह समाप्त हो रही हैं।",
        "category": "Joy & Family",
    },
    83: {
        "topic": "Business Deal / Property Rental / Road / New Daughter-in-law / Engagement",
        "topic_hi": "व्यापार / जायदाद किराया / रास्ता / नई बहू / सगाई",
        "detail": "Commerce and new family chapters are intertwined in your thoughts — a business deal being negotiated, a property being leased or rented, a road or pathway that opens new possibilities, or the joyful arrival of a new daughter-in-law or an engagement being planned. Both the contract and the celebration deserve your full attention; make sure legal details are solid before the festivities begin.",
        "detail_hi": "व्यापार और परिवार के नए अध्याय आपके विचारों में जुड़े हैं — कोई व्यापारिक सौदा, संपत्ति का पट्टा या किराया, नई संभावनाओं को खोलने वाला रास्ता, या नई बहू का आगमन या सगाई। अनुबंध और उत्सव दोनों पर पूरा ध्यान दें।",
        "category": "Business & Family",
    },
    84: {
        "topic": "Girl / Pond / Public Festival / Durga / Holiday / Dear Friend",
        "topic_hi": "कन्या / तालाब / जन महोत्सव / दुर्गापूजा / अवकाश / प्रिय मित्र",
        "detail": "Joy, purity, and celebration are the energies of this number — a young girl or daughter who brings light into your life, a serene pond or bathing place where you find peace, a grand public festival, the divine grace of Goddess Durga, a well-deserved holiday, or a dear friend whose company refreshes your spirit. This is one of the most uplifting numbers. Celebrate life; you have earned this joy.",
        "detail_hi": "आनंद, पवित्रता और उत्सव इस अंक की ऊर्जाएं हैं — एक युवा बेटी जो जीवन में रोशनी लाती है, एक शांत तालाब, एक भव्य जन महोत्सव, देवी दुर्गा की दिव्य कृपा, एक सुखद अवकाश, या एक प्रिय मित्र। यह सबसे उत्साहजनक अंकों में से एक है। जीवन का जश्न मनाएं; आपने यह आनंद अर्जित किया है।",
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
        "hint": "Walk through every corridor and passageway in your home or office. Check piles of papers, files, and stacked documents carefully — the item may have slipped between sheets. Also look in narrow spaces between furniture and walls.",
        "hint_hi": "घर या दफ्तर के हर गलियारे और रास्ते में चलकर देखें। कागजों, फाइलों और दस्तावेजों के ढेर में सावधानी से जाँच करें — वस्तु शायद पन्नों के बीच फंसी हो। फर्नीचर और दीवारों के बीच संकरी जगहें भी देखें।",
    },
    4:  {
        "location": "Item is NOT lost — it is in your own possession",
        "location_hi": "वस्तु खोई नहीं है — आपके ही कब्जे में है",
        "hint": "Stop searching elsewhere — the item has not left your possession. Check your own bags, pockets, and shelves more carefully before assuming it is gone. It is right with you, probably in a place you checked too quickly.",
        "hint_hi": "और जगह तलाश करना बंद करें — वस्तु आपके पास से गई नहीं है। अपने बैग, जेबें और अलमारियां और ध्यान से जांचें। यह आपके ही पास है, शायद किसी ऐसी जगह जो आपने जल्दी में देखी।",
    },
    5:  {
        "location": "Will be found with a little effort — look under hat, cap, or turban",
        "location_hi": "थोड़ी खोज से मिल जाएगी — टोपी, साफा, पगड़ी, हैट के नीचे देखें",
        "hint": "Check under or inside any headwear — caps, hats, turbans, scarves. Also look in the area where headgear is stored or hung. The item is close and will be recovered with a small but focused effort.",
        "hint_hi": "टोपी, हैट, पगड़ी, दुपट्टे के नीचे या अंदर देखें। सिर के वस्त्र जहाँ रखे या टांगे जाते हैं वहाँ भी देखें। वस्तु पास है और थोड़े केंद्रित प्रयास से मिल जाएगी।",
    },
    6:  {
        "location": "Near shoe rack, exit path — check shelf, sofa, rack, or almirah compartment",
        "location_hi": "चप्पल-जूते रखने की जगह, निकलने के रास्ते में — आले, सोफे, रैक या आलमारी में",
        "hint": "Focus on the main entrance and exit areas of your home — shoe racks, the area behind the front door, sofas near the entrance, and the nearest almirah compartment. The item was likely set down here while you were coming or going.",
        "hint_hi": "घर के मुख्य प्रवेश और निकास क्षेत्रों पर ध्यान दें — जूते रखने की जगह, मुख्य दरवाजे के पीछे का क्षेत्र, प्रवेश के पास सोफे और निकटतम आलमारी का खाना। वस्तु शायद आते-जाते यहीं रखी गई।",
    },
    7:  {
        "location": "Ask your servant or maid — they know where it is",
        "location_hi": "अपने नौकर या नौकरानी से पता लगाएं",
        "hint": "Your domestic helper moved, cleaned around, or placed the item somewhere while doing their work. Ask them directly and calmly — do not accuse. They will remember where they last saw it or where they placed it while cleaning.",
        "hint_hi": "घरेलू सहायक ने काम करते समय वस्तु को हिलाया, साफ किया, या कहीं रखा होगा। उनसे सीधे और शांति से पूछें — आरोप न लगाएं। वे याद करेंगे कि इसे आखिरी बार कहाँ देखा या सफाई करते समय कहाँ रखा।",
    },
    8:  {
        "location": "On top of almirah or balcony — ask a carpenter, artisan, or laborer",
        "location_hi": "आलमारी के ऊपर या बालकनी में — नौकर, कारीगर, मजदूर से तलाश करें",
        "hint": "Look on top of almirahs, cabinets, and high shelves — places you would not normally check. Also search the balcony or terrace. If any renovation or repair work was done recently, ask the carpenter or worker who was in the house.",
        "hint_hi": "आलमारियों, अलमारियों और ऊंची शेल्फ के ऊपर देखें — ऐसी जगहें जो आम तौर पर नहीं देखते। बालकनी या छत भी देखें। यदि हाल ही में कोई मरम्मत या नवीनीकरण कार्य हुआ है, तो घर में आए बढ़ई या मजदूर से पूछें।",
    },
    9:  {
        "location": "Check in a child's or teenager's clothes or pocket",
        "location_hi": "किसी बालक या किशोर के पास, उसके कपड़े या जेब में देखें",
        "hint": "A child in the house picked up the item out of curiosity or during play. Check their clothes pockets, school bag, toy box, and under their bed. Ask them gently — children often remember exactly what they touched.",
        "hint_hi": "घर में किसी बच्चे ने जिज्ञासावश या खेल के दौरान वस्तु उठाई होगी। उनके कपड़ों की जेब, स्कूल बैग, खिलौने के डिब्बे और उनके बिस्तर के नीचे देखें। उनसे धीरे से पूछें — बच्चे अक्सर ठीक याद रखते हैं कि उन्होंने क्या छुआ।",
    },
    10: {
        "location": "It is in your main room or sitting room",
        "location_hi": "आपके प्रमुख कमरे या बैठक में है",
        "hint": "Do a systematic search of your living room or main hall — behind cushions, under the sofa, on the centre table, inside magazines or books lying around. The item is definitely in this room; look methodically rather than randomly.",
        "hint_hi": "अपने बैठक या मुख्य हॉल में व्यवस्थित तरीके से खोजें — कुशन के पीछे, सोफे के नीचे, सेंटर टेबल पर, पड़ी पत्रिकाओं या किताबों के अंदर। वस्तु निश्चित रूप से इसी कमरे में है; बेतरतीब नहीं बल्कि क्रमबद्ध तरीके से खोजें।",
    },
    11: {
        "location": "Go near a pond, lake, or water body to search — item is safe",
        "location_hi": "तालाब, जलाशय या पानी के पास जाकर तलाश करें — वस्तु सुरक्षित है",
        "hint": "Search near any water body close to where the item was last seen — a pond, a tap area, a bathroom, or a water storage spot. Also check your workplace, office, or study area including books and stacked papers. The item is safe and has not been damaged.",
        "hint_hi": "जहाँ वस्तु आखिरी बार देखी गई उसके पास किसी भी जल स्रोत के पास खोजें — तालाब, नल क्षेत्र, बाथरूम, या पानी रखने की जगह। कार्यस्थल, दफ्तर या अध्ययन क्षेत्र में किताबों और कागजों में भी देखें। वस्तु सुरक्षित है, क्षतिग्रस्त नहीं हुई।",
    },
    12: {
        "location": "Check in office, books, or papers — also where you keep clothes",
        "location_hi": "दफ्तर, किताबों या कागजों में देखें — जहाँ कपड़े रखते हैं वहाँ भी देखें",
        "hint": "Flip through books and papers on your desk or study table — the item may be used as a bookmark or have slipped between pages. Also check inside folded clothes in the wardrobe. These two locations are your best leads.",
        "hint_hi": "अपनी मेज या पढ़ाई की टेबल पर किताबों और कागजों को पलटें — वस्तु बुकमार्क के रूप में या पन्नों के बीच फंसी हो सकती है। अलमारी में मुड़े कपड़ों के अंदर भी देखें। ये दोनों जगहें आपकी सबसे अच्छी संभावनाएं हैं।",
    },
    13: {
        "location": "Where you keep clothes, shawl, overcoat — also check drain or sewer area",
        "location_hi": "जहाँ कपड़े, शॉल, ओवरकोट रखते हैं — नाली या सीवर भी देखें",
        "hint": "Check your heavy clothing storage — winter coats, shawls, and overcoats hanging in the wardrobe or folded in trunks. Also check near outdoor drains or the sewer area if the item could have been near there. The clothing storage area is the stronger bet.",
        "hint_hi": "भारी कपड़ों का भंडारण जाँचें — अलमारी में टंगे या संदूक में मुड़े सर्दी के कोट, शॉल और ओवरकोट। बाहरी नालियों के पास भी देखें। कपड़ों का भंडारण क्षेत्र अधिक संभावित है।",
    },
    14: {
        "location": "Under turban/hat/cap — or near a toilet, drain, or sewer",
        "location_hi": "पगड़ी, हैट, टोपी या साफे के नीचे — संडास, नाली, सीवर के पास",
        "hint": "Lift and check under all headgear — inside caps, under folded turbans, and in headwear storage. If not found there, check the bathroom, toilet area, and nearby drainage points. The item may have fallen near plumbing.",
        "hint_hi": "सभी सिर के वस्त्रों के नीचे जाँचें — टोपी के अंदर, मुड़ी पगड़ी के नीचे। यदि वहाँ नहीं मिला, तो बाथरूम, शौचालय क्षेत्र और पास के पानी निकासी बिंदुओं की जाँच करें।",
    },
    15: {
        "location": "Ask your husband or wife — check garage or stable",
        "location_hi": "पति या पत्नी से पूछें — गैरेज या अस्तबल में देखें",
        "hint": "Your spouse either moved the item or knows its current location — ask them specifically. If they are unsure, search the garage, vehicle storage area, or any outbuilding. The item is connected to someone very close to you.",
        "hint_hi": "आपके जीवनसाथी ने या तो वस्तु को हिलाया है या उसकी वर्तमान जगह जानते हैं — उनसे विशेष रूप से पूछें। यदि वे अनिश्चित हैं, तो गैरेज, वाहन भंडारण क्षेत्र की तलाश करें।",
    },
    16: {
        "location": "Ask the cook — check in the kitchen",
        "location_hi": "रसोईया से पता करें — रसोई घर में देखें",
        "hint": "Go directly to the kitchen and search systematically — on counters, inside drawers, behind jars and canisters, on shelves above the stove. Ask the person who cooks most often in your home; they saw what happened in that space.",
        "hint_hi": "सीधे रसोई में जाएं और व्यवस्थित रूप से खोजें — काउंटर पर, दराजों के अंदर, जार और डिब्बों के पीछे, चूल्हे के ऊपर शेल्फ पर। घर में जो सबसे अधिक खाना बनाते हैं उनसे पूछें।",
    },
    17: {
        "location": "Check in an almirah compartment, rack, safe, or near artistic items",
        "location_hi": "आलमारी या रैक के खाने में, सेफ में, या कलात्मक वस्तुओं के पास देखें",
        "hint": "Open each compartment and shelf of your almirah systematically. Check the safe or lockbox if you have one. Also look near decorative objects, photo frames, and artistic items — the item may have been placed there temporarily.",
        "hint_hi": "अपनी आलमारी के हर खाने और शेल्फ को व्यवस्थित रूप से खोलें। यदि सेफ या लॉकबॉक्स है तो जाँचें। सजावटी वस्तुओं, फोटो फ्रेम और कलात्मक वस्तुओं के पास भी देखें।",
    },
    18: {
        "location": "Item is at home and will be found in clothes — also look in a lane or alley",
        "location_hi": "चीज घर में है और कपड़ों में मिलेगी — पगडंडी या गली में भी देखें",
        "hint": "Go through your laundry, folded clothes, and clothes that are hanging — the item is tucked into or among clothing. If not found there, walk the nearby lane or alley outside your home and search the path you took recently.",
        "hint_hi": "अपने धुले, मुड़े और टंगे कपड़ों को ध्यान से देखें — वस्तु कपड़ों में या उनके बीच फंसी है। यदि वहाँ नहीं मिली, तो घर के पास की गली में चलकर हाल ही में लिए गए रास्ते पर देखें।",
    },
    19: {
        "location": "A little far, on dry sandy ground — or forgot where kept; near water or good clothes",
        "location_hi": "थोड़ी दूर सूखी रेतीली जमीन पर — खोई नहीं है; जल के पास या बढ़िया कपड़ों के पास",
        "hint": "The item is not truly lost — you placed it somewhere specific and forgot. Check near any water source (tap, filter, cooler) or in the area where you keep your best clothes. If you went outdoors recently, check dry sandy or garden soil areas.",
        "hint_hi": "वस्तु वास्तव में खोई नहीं है — आपने इसे किसी विशेष जगह रखा और भूल गए। किसी भी जल स्रोत (नल, फिल्टर, कूलर) के पास या जहाँ आप अपने अच्छे कपड़े रखते हैं वहाँ देखें।",
    },
    20: {
        "location": "Not lost — forgot where you kept it; near water or near good clothes",
        "location_hi": "खोई नहीं है — कहीं रखकर भूल गए हैं; जल के पास या बढ़िया कपड़ों के पास मिलेगी",
        "hint": "Sit quietly and retrace your steps mentally — where were you when you last used this item? It is in your home, placed by your own hand in a safe spot. Check near water (bathroom shelf, kitchen counter) and in your good clothing storage.",
        "hint_hi": "शांत बैठें और मानसिक रूप से अपने कदमों को याद करें — जब आपने आखिरी बार इस वस्तु का उपयोग किया तब आप कहाँ थे? यह घर में ही है, आपके हाथों से किसी सुरक्षित जगह रखी गई। पानी के पास और अच्छे कपड़ों के भंडार में देखें।",
    },
    21: {
        "location": "Item is with you — check in a box, case, tin, attaché case, or folded container",
        "location_hi": "चीज आपके पास ही है — बक्से, केस, डिब्बे, अटैची, ब्रीफकेस या मोड़कर बन्द डिब्बे में",
        "hint": "Check every closed container in your home and bag — tins, boxes, briefcases, attaché cases, and any container that closes or folds shut. The item is definitely within your reach. Try each container one by one.",
        "hint_hi": "घर और बैग में हर बंद बर्तन जाँचें — डिब्बे, बक्से, ब्रीफकेस, अटैची, और कोई भी बर्तन जो बंद होता है। वस्तु निश्चित रूप से आपकी पहुँच में है। हर बर्तन एक-एक करके आजमाएं।",
    },
    22: {
        "location": "On top of an almirah or shelved rack — will be found soon",
        "location_hi": "किसी आलमारी या खानेदार रैक के ऊपर है — जल्दी मिलनी चाहिए",
        "hint": "Stand on a stool and look at the top surface of almirahs and tall shelves — things placed there tend to get pushed back and hidden from sight. Also check the top of the refrigerator or any tall furniture. The item will be found very soon.",
        "hint_hi": "स्टूल पर खड़े होकर आलमारियों और ऊंची शेल्फ की ऊपरी सतह देखें — वहाँ रखी चीजें अंदर धकेल दी जाती हैं। फ्रिज के ऊपर या किसी ऊंचे फर्नीचर के ऊपर भी देखें। वस्तु जल्द ही मिलेगी।",
    },
    23: {
        "location": "It is nearby — in the room where you keep clothes",
        "location_hi": "पास में है — दूसरे कमरे में जहाँ कपड़े रखते हों वहाँ देखें",
        "hint": "Go to your bedroom or dressing room and search thoroughly — inside the wardrobe, on the dressing table, under clothing, and in the drawers. The item is close by; it just requires a focused search in this specific room.",
        "hint_hi": "अपने शयन कक्ष या ड्रेसिंग रूम में जाएं और अच्छी तरह खोजें — अलमारी के अंदर, ड्रेसिंग टेबल पर, कपड़ों के नीचे, और दराजों में। वस्तु नजदीक ही है; बस इस कमरे में केंद्रित खोज की जरूरत है।",
    },
    24: {
        "location": "Item is with you — it is not lost",
        "location_hi": "चीज आपके पास ही है — खोई नहीं है",
        "hint": "The item has not gone anywhere. Empty your bag completely, check all your pockets one by one, and re-examine every shelf or drawer you use regularly. You will find it — it is right in your possession, just overlooked.",
        "hint_hi": "वस्तु कहीं नहीं गई है। अपना बैग पूरी तरह खाली करें, सभी जेबें एक-एक करके जाँचें, और जो शेल्फ या दराज आप नियमित रूप से उपयोग करते हैं उन्हें फिर से देखें। यह आपके ही पास है।",
    },
    25: {
        "location": "Look in your own belongings — inside a white, round object",
        "location_hi": "अपनी ही चीजों में देखें — किसी सफेद और गोल वस्तु के अन्दर है",
        "hint": "Think of every white, round, or cylindrical container in your home — a white bowl, a round tin, a white cup, a container with a lid. Open and check inside each one. The item slipped or was placed inside something white and round.",
        "hint_hi": "घर में हर सफेद, गोल या बेलनाकार बर्तन के बारे में सोचें — सफेद कटोरा, गोल डिब्बा, सफेद कप, ढक्कनदार बर्तन। हर एक को खोलकर अंदर देखें। वस्तु किसी सफेद और गोल चीज के अंदर रखी या फिसली है।",
    },
    26: {
        "location": "Ask an elderly person in the house — they have kept it safely",
        "location_hi": "घर के वयोवृद्ध बुजुर्ग से पूछें — उन्होंने संभाल कर रख दी है",
        "hint": "The oldest person in your home — grandparent, elderly relative, or elder — deliberately put the item away for safekeeping. They have not forgotten; simply ask them directly and warmly where they kept it.",
        "hint_hi": "घर का सबसे बुजुर्ग व्यक्ति — दादा-दादी, नाना-नानी या वृद्ध संबंधी — ने जानबूझकर वस्तु सुरक्षित रख दी है। उन्हें याद है; बस सीधे और गर्मजोशी से पूछें कि उन्होंने इसे कहाँ रखा।",
    },
    27: {
        "location": "Search the cowshed, stable, garage, or servant's quarters",
        "location_hi": "गौशाला, घुड़साल, गैरेज में या नौकरों के निवास में खोज करें",
        "hint": "The item has moved to an outbuilding or working area — garage, shed, stable, or the room where your domestic help stays. These are easy places to overlook in a standard search. Do a careful physical check of these spaces.",
        "hint_hi": "वस्तु किसी बाहरी इमारत या कार्य क्षेत्र में चली गई है — गैरेज, शेड, अस्तबल, या घरेलू सहायक के कमरे में। ये जगहें आमतौर पर खोज में अनदेखी रह जाती हैं। इन स्थानों की सावधानीपूर्वक जाँच करें।",
    },
    28: {
        "location": "Finding the item is NOT possible — give up hope",
        "location_hi": "खोई वस्तु मिलना संभव नहीं है — आशा छोड़ दें",
        "hint": "Despite your best efforts, this item will not be recovered. Accept the loss gracefully and move on without dwelling on it. Use this as an opportunity to replace the item with something even better — what is lost was perhaps meant to leave.",
        "hint_hi": "अपने सर्वोत्तम प्रयासों के बावजूद, यह वस्तु वापस नहीं मिलेगी। हानि को शालीनता से स्वीकार करें और आगे बढ़ें। इसे उस वस्तु को और बेहतर चीज से बदलने के अवसर के रूप में उपयोग करें।",
    },
    29: {
        "location": "An elderly person or servant will tell you where it is",
        "location_hi": "किसी वृद्ध पुरुष या नौकर से पता मिलेगा",
        "hint": "Do not search alone — ask the oldest person in the household or the most experienced domestic helper. They either witnessed where it was placed or moved it themselves. A calm and respectful inquiry will bring the answer quickly.",
        "hint_hi": "अकेले मत खोजें — घर के सबसे बुजुर्ग व्यक्ति या सबसे अनुभवी घरेलू सहायक से पूछें। उन्होंने या तो देखा कि वस्तु कहाँ रखी गई या खुद हिलाई। शांत और सम्मानजनक पूछताछ जल्दी जवाब देगी।",
    },
    30: {
        "location": "Ask children or students — lost during play",
        "location_hi": "बच्चों से या विद्यार्थियों से पूछने से पता मिलेगा — खेल में खोई है",
        "hint": "A child in the household picked up the item during play and put it in an unexpected place. Ask each child gently and without anger — they will tell you exactly where it is. Also check children's play areas, under beds, and inside toy boxes.",
        "hint_hi": "घर के बच्चे ने खेल के दौरान वस्तु उठाई और किसी अप्रत्याशित जगह रख दी। हर बच्चे से धीरे और बिना गुस्से के पूछें — वे बताएंगे कि वह कहाँ है। बच्चों के खेल क्षेत्र, बिस्तर के नीचे और खिलौने के डिब्बों में भी देखें।",
    },
    31: {
        "location": "In a secret room or closed drain — may be found with luck or effort",
        "location_hi": "गुप्त कोठरी या बन्द नाली में है — सौभाग्य से या परिश्रम से मिल सकती है",
        "hint": "Search hidden or rarely opened spaces — a store room, locked cabinet, or space under the stairs. Also check any covered or blocked drainage areas in and around the house. Recovery is possible but requires persistent effort rather than a quick glance.",
        "hint_hi": "छिपी या कम खुलने वाली जगहें खोजें — स्टोर रूम, बंद अलमारी, या सीढ़ियों के नीचे की जगह। घर के अंदर और बाहर किसी भी ढके या बंद नाली क्षेत्र की भी जाँच करें। मिल सकती है लेकिन लगातार प्रयास चाहिए।",
    },
    32: {
        "location": "Nearby in veranda, on a rock, raised ground, or a rectangular object",
        "location_hi": "पास ही बरामदे में, चट्टान पर, उभरी जमीन पर या आयताकार पदार्थ पर",
        "hint": "Check your veranda, front porch, or any outdoor seating area. Look on flat stone surfaces, raised platforms, or on top of rectangular objects like a brick, a step, or a ledge. The item is just outside your immediate indoor search zone.",
        "hint_hi": "अपने बरामदे, सामने के पोर्च या किसी बाहरी बैठने की जगह की जाँच करें। सपाट पत्थर की सतहों, ऊंचे प्लेटफार्मों, या ईंट, सीढ़ी, या किसी सतह जैसी आयताकार वस्तुओं के ऊपर देखें।",
    },
    33: {
        "location": "Item is with you",
        "location_hi": "चीज आपके पास है",
        "hint": "The item never left your immediate possession or your home. Take a few deep breaths and go through your belongings one item at a time, slowly and patiently. You are missing it due to a momentary lapse of attention — it will reappear the moment you search calmly.",
        "hint_hi": "वस्तु कभी आपके तत्काल कब्जे या घर से नहीं गई। कुछ गहरी साँसें लें और अपनी चीजों को एक-एक करके, धीरे-धीरे और धैर्यपूर्वक देखें। आप इसे ध्यान की क्षणिक चूक के कारण छोड़ रहे हैं।",
    },
    34: {
        "location": "Near fire, stove, furnace, or oven — or in main room near fireplace",
        "location_hi": "अग्नि, अंगीठी, चूल्हा, भट्टी, ओवन के पास — या मुख्य कमरे में आग जलाने के स्थान पर",
        "hint": "Search systematically around every heat source in your home — the kitchen stove, the oven, the gas burner, and any space heater or fireplace in the main room. Items placed near warmth are often pushed aside or knocked behind appliances. Check under and behind these appliances as well as on the surfaces immediately around them.",
        "hint_hi": "घर में हर ताप स्रोत के आसपास व्यवस्थित रूप से खोजें — रसोई का चूल्हा, ओवन, गैस बर्नर और मुख्य कमरे में कोई हीटर। इन उपकरणों के पीछे और नीचे, तथा आसपास की सतहों पर भी देखें।",
    },
    35: {
        "location": "Near water in a hidden spot, or in husband-wife's private room or near washbasin",
        "location_hi": "पानी के पास छिपे स्थान में, गुप्त स्थान में — पति-पत्नी का निजी कमरा या वाश बेसिन",
        "hint": "Go directly to the master bedroom and search it thoroughly — on the nightstands, under the bed, in the bedside drawers, and around the washbasin or en-suite bathroom. Water proximity is significant: check the bathroom shelf, the counter by the sink, and any damp or hidden corner near plumbing.",
        "hint_hi": "सीधे शयन कक्ष में जाएं और अच्छी तरह खोजें — नाइटस्टैंड पर, बिस्तर के नीचे, बेडसाइड दराजों में, और वॉशबेसिन के पास। बाथरूम की शेल्फ, सिंक के पास की सतह और पाइपलाइन के पास के छिपे कोने देखें।",
    },
    36: {
        "location": "Will be obtained through a nanny, caretaker, or guardian",
        "location_hi": "किसी आया, धाय या अभिभावक के द्वारा प्राप्त होगी",
        "hint": "The item is in the hands of the person who cares for the children — a nanny, babysitter, daytime caretaker, or older guardian. They either picked it up during their duties or a child handed it to them for safekeeping. Ask them directly and calmly; they will have it or know exactly where it is.",
        "hint_hi": "वस्तु उस व्यक्ति के पास है जो बच्चों की देखभाल करता है — आया, बेबीसिटर, दिन का देखभालकर्ता या बड़े अभिभावक। उनसे सीधे और शांति से पूछें; उनके पास होगी या वे ठीक बताएंगे।",
    },
    37: {
        "location": "In a holy place — temple, pilgrimage site, or near house compound walls",
        "location_hi": "पवित्र स्थान, मन्दिर, तीर्थ, देवालय, समाधि में — या घर की चारदीवारी के पास",
        "hint": "Search your home's prayer room or puja corner first — around the deity idols, on the altar shelf, or near incense holders. Then check the perimeter of your house compound near the boundary walls. If you visited a temple or pilgrimage site recently, contact the venue or retrace your steps there.",
        "hint_hi": "सबसे पहले घर के पूजा स्थान में खोजें — देवताओं की मूर्तियों के पास, वेदी की शेल्फ पर, या अगरबत्ती के पास। फिर घर की चारदीवारी के पास देखें। हाल ही में किसी मंदिर या तीर्थ स्थान गए थे तो वहाँ भी खोजें।",
    },
    38: {
        "location": "Where drinking water is stored",
        "location_hi": "पीने का पानी जहाँ रखा जाता है वहाँ मिलेगी",
        "hint": "Check every place where drinking water is stored or kept in your home — the earthen matka, the water filter unit, the water cooler, the refrigerator's water tray, and any vessels used for drinking water. Look on the shelf above, the surface below, and inside the storage area around these containers.",
        "hint_hi": "घर में जहाँ-जहाँ पीने का पानी रखा जाता है वहाँ देखें — मटका, वाटर फिल्टर, वाटर कूलर, फ्रिज की पानी की ट्रे। इन बर्तनों के ऊपर की शेल्फ, नीचे की सतह और आसपास के भंडारण क्षेत्र में भी देखें।",
    },
    39: {
        "location": "Consider permanently lost — or will be found in damaged condition",
        "location_hi": "हमेशा के लिये खो गई समझो — या क्षत-विक्षत हालत में मिलेगी",
        "hint": "The chances of full recovery are very slim for this item. If it does turn up, expect it to be in a damaged, broken, or deteriorated state. Make peace with the loss and consider replacing it; continuing to search will likely be an exercise in frustration rather than resolution.",
        "hint_hi": "इस वस्तु के पूरी तरह मिलने की संभावना बहुत कम है। यदि मिले तो टूटी, खराब या बिगड़ी हुई हालत में होगी। हानि को शांति से स्वीकार करें और नई वस्तु लेने पर विचार करें।",
    },
    40: {
        "location": "In a two-part container or box",
        "location_hi": "किसी दो भागों वाले पात्र में या बक्से में मिलेगी",
        "hint": "Think of every container in your home that has two sections, compartments, or halves — a tiffin carrier, a divided lunch box, a hinged tin, a briefcase with two pockets, or a storage box with a removable tray. Open each one and look inside both compartments carefully; the item is tucked in one of these divided spaces.",
        "hint_hi": "घर में हर उस बर्तन के बारे में सोचें जिसके दो भाग या खाने हों — टिफिन कैरियर, विभाजित लंच बॉक्स, कब्जेदार डिब्बा, दो जेब वाला ब्रीफकेस। हर एक खोलकर दोनों खानों में ध्यान से देखें।",
    },
    41: {
        "location": "Near a holy bathing place — river, lake, pond, or its surroundings",
        "location_hi": "धार्मिक स्नान स्थल, पवित्र नदी, सरोवर, जलाशय या उसके आसपास",
        "hint": "If you have recently visited a river, lake, pond, or sacred bathing ghat, retrace your steps there and search carefully along the bank or path. At home, check your bathroom — especially the bathing area, the rim of the tub or bucket area, and the shelf beside the water source. Sacred water and bathing spots hold the key.",
        "hint_hi": "हाल ही में किसी नदी, झील, तालाब या पवित्र घाट पर गए थे तो वहाँ जाकर किनारे पर सावधानी से खोजें। घर पर बाथरूम में — स्नान क्षेत्र, बाल्टी के पास और जल स्रोत के पास की शेल्फ — देखें।",
    },
    42: {
        "location": "Check with your partner or spouse — item has changed hands",
        "location_hi": "साझेदार या पति-पत्नी से पता करें — वस्तु एक हाथ से दूसरे हाथ में पहुँच चुकी है",
        "hint": "The item has been picked up or moved by your spouse, partner, or a close family member — it did not simply fall somewhere. Ask them directly whether they used it, put it away, or saw where it went. If they are unsure, search together through their belongings; the answer is in a conversation, not a solo search.",
        "hint_hi": "वस्तु आपके जीवनसाथी, साथी या किसी करीबी परिवार के सदस्य ने उठाई या हिलाई है। उनसे सीधे पूछें कि क्या उन्होंने इसे उपयोग किया, रखा, या देखा। यदि वे अनिश्चित हैं, तो मिलकर उनके सामान में खोजें।",
    },
    43: {
        "location": "Servant has it — will return when asked, explained, or pressured",
        "location_hi": "नौकर के पास है — पूछने, समझाने या दबाव डालने पर लौटा देगा",
        "hint": "A domestic helper in your household has the item — either accidentally picked up while doing chores or taken deliberately. Approach them calmly but clearly, explaining that you know the item has not left the house. A gentle inquiry first; if that does not work, a firm but non-aggressive follow-up will bring it back.",
        "hint_hi": "घर का कोई नौकर या काम करने वाला इस वस्तु को ले गया है — काम करते समय गलती से या जानबूझकर। शांतिपूर्वक लेकिन स्पष्ट रूप से बात करें। पहले विनम्र पूछताछ; यदि काम न आए, तो दृढ़ लेकिन शांत अनुवर्ती वार्ता वस्तु वापस लाएगी।",
    },
    44: {
        "location": "Among family — search more in children's belongings",
        "location_hi": "घर परिवार के बीच किसी के पास — बच्चों की चीजों में ज्यादा तलाश करें",
        "hint": "The item is within the family and has not left the house. Start with the children — check their school bags, toy boxes, pockets, and under their beds. Then broaden to other family members' rooms. The item is safe; someone picked it up without realising its importance to you.",
        "hint_hi": "वस्तु परिवार के अंदर ही है और घर से नहीं निकली। पहले बच्चों से शुरू करें — उनके स्कूल बैग, खिलौने के डिब्बे, जेबें और बिस्तर के नीचे जाँचें। फिर अन्य परिवार के सदस्यों के कमरों में देखें।",
    },
    45: {
        "location": "Near house wall or compound wall — by rainwater drain, pipe, or water",
        "location_hi": "मकान की दीवार या चारदीवारी के पास — बरसात की नाली, मोरी या पाइप के पास",
        "hint": "Walk the perimeter of your house along the outer walls and compound boundary. Check near every drainage pipe, rainwater outlet, and external water pipe. Items dropped near the exterior often end up lodged against a wall or beside a drainage channel that is easy to miss when looking indoors.",
        "hint_hi": "घर की बाहरी दीवारों और चारदीवारी के किनारे-किनारे चलें। हर पानी निकासी पाइप, बरसात के आउटलेट और बाहरी जल पाइप के पास देखें। बाहर गिरी चीजें अक्सर दीवार के पास या नाली के किनारे मिलती हैं।",
    },
    46: {
        "location": "Where you were or stayed before — go there and search",
        "location_hi": "थोड़ी दूर पर जहाँ आप पहले ठहरे थे — वहाँ जाकर तलाश करें",
        "hint": "Think back to the last place you stayed or visited before you noticed the item was missing — a friend's home, an office, a hotel room, or a relative's house. Go back there in person or call them to search on your behalf. The item is in that earlier location waiting to be reclaimed.",
        "hint_hi": "सोचें कि वस्तु गुम होने से पहले आप आखिरी बार कहाँ रुके या गए थे — किसी मित्र का घर, दफ्तर, होटल का कमरा, या रिश्तेदार का घर। वहाँ खुद जाएं या उन्हें खोजने को कहें। वस्तु उस पुराने स्थान पर आपका इंतजार कर रही है।",
    },
    47: {
        "location": "Check near your bag, pockets, tools, instrument, or walking stick",
        "location_hi": "थैले, जेबों, औजार, यन्त्र या छड़ी रखने के स्थान के पास देखें",
        "hint": "Empty your bag or satchel completely onto a flat surface and check every inner pocket and compartment. Go through the pockets of every garment you have worn recently. Also check wherever you store your tools, instruments, or walking stick — items frequently end up in these practical, everyday spaces.",
        "hint_hi": "अपना बैग या थैला किसी सपाट सतह पर पूरी तरह खाली करें और हर अंदरूनी जेब जाँचें। हाल ही में पहने गए हर कपड़े की जेबें देखें। औजार, यंत्र या छड़ी रखने की जगहें भी जाँचें।",
    },
    48: {
        "location": "Under two people's control — hard to get; may already be used or spent",
        "location_hi": "दो व्यक्तियों के अधिकार में — कठिनाई से मिलेगी; खर्च हो चुकी है या उपयोग में",
        "hint": "Two people share custody of this item — possibly two household members, two business partners, or two relatives. Getting it back will require navigating both parties. If the item is consumable (money, food, material), it may already have been used up. Approach both parties diplomatically and be prepared that full recovery may not be possible.",
        "hint_hi": "दो लोगों के पास इस वस्तु का नियंत्रण है — दो घर के सदस्य, दो व्यापारिक साझेदार, या दो रिश्तेदार। इसे वापस पाने के लिए दोनों से बात करनी होगी। यदि वस्तु उपभोग्य है तो शायद उपयोग हो चुकी है।",
    },
    49: {
        "location": "With an old/elderly servant — may be inside food/flour — or hidden by servant",
        "location_hi": "पुराने या वृद्ध नौकर के पास — रोटी, आटे, केक जैसी वस्तु के अन्दर, या नौकर ने छिपाया",
        "hint": "An elderly domestic helper in your home either accidentally placed the item inside a food container — a flour bin, a bread box, a grain sack — or has hidden it deliberately. Check all dry food storage first. Then approach the oldest, most long-standing helper calmly and ask whether they have seen it or moved it.",
        "hint_hi": "घर का कोई पुराना नौकर इस वस्तु को गलती से किसी खाने के डिब्बे — आटे के बक्से, रोटी के डिब्बे, अनाज की बोरी — में रख सकता है या जानबूझकर छिपाया है। पहले सभी सूखे खाद्य भंडारण की जाँच करें, फिर सबसे पुराने नौकर से शांति से पूछें।",
    },
    50: {
        "location": "No hope of finding",
        "location_hi": "मिलने की कोई आशा नहीं है",
        "hint": "This number is one of the most definitive — the item is gone and will not return. Rather than continue a fruitless search, accept the loss with equanimity and redirect your energy toward replacing or moving on. Sometimes what is lost creates space for something better to arrive.",
        "hint_hi": "यह अंक सबसे निश्चित संकेतों में से एक है — वस्तु चली गई है और वापस नहीं आएगी। व्यर्थ खोज जारी रखने के बजाय, हानि को समता के साथ स्वीकार करें और नई वस्तु लाने पर ध्यान दें।",
    },
    51: {
        "location": "In the lower part of the house — near shoes, slippers, socks, or drain",
        "location_hi": "घर के नीचे के भाग में — जूते, चप्पल, मोजे, पजामा, पानी की नाली के पास",
        "hint": "Focus your search on the ground floor and the entry area of your home — the shoe rack, the mat near the door, the space under low furniture, and near any indoor drain or floor-level pipe. Items that drop to the lower level of a home often end up pushed against skirting boards or hidden beside footwear.",
        "hint_hi": "खोज को भूतल और घर के प्रवेश द्वार पर केंद्रित करें — जूते रखने की रैक, दरवाजे के पास का मैट, नीचे के फर्नीचर के नीचे, और किसी इनडोर नाली के पास। नीचे गिरी वस्तुएं अक्सर सीमा-पट्टी के पास या जूतों के पास मिलती हैं।",
    },
    52: {
        "location": "Gone by hand — will NOT be found",
        "location_hi": "हाथ से गई — नहीं मिलेगी",
        "hint": "The item passed from your hands into someone else's and will not return to you. This is a definitive loss, not a misplacement. Spending further energy on the search will yield nothing; channel that energy into replacing the item or making peace with its absence.",
        "hint_hi": "वस्तु आपके हाथों से किसी और के पास चली गई है और वापस नहीं आएगी। यह एक निश्चित हानि है, कोई भूल नहीं। आगे की खोज में ऊर्जा बर्बाद न करें; नई वस्तु लाने या हानि स्वीकार करने पर ध्यान दें।",
    },
    53: {
        "location": "You have it — in an old dark place or old junk pile",
        "location_hi": "आपके ही पास है — पुरानी अँधेरी जगह में या पुराने कबाड़ में पड़ी है",
        "hint": "The item is still in your possession — buried in an old, dark, or rarely visited part of your home. Search your attic, storeroom, under-stair storage, or wherever old and forgotten items accumulate. Bring a torch and go through the junk methodically; the item has been there for some time and simply needs to be unearthed.",
        "hint_hi": "वस्तु अभी भी आपके पास है — घर के किसी पुराने, अंधेरे या कम जाने वाले हिस्से में दबी हुई है। अटारी, स्टोर रूम, सीढ़ियों के नीचे का भंडारण खोजें। टॉर्च लेकर व्यवस्थित रूप से पुराने सामान की जाँच करें।",
    },
    54: {
        "location": "In your possession — forgotten; check dark corners or high-up places",
        "location_hi": "आपके कब्जे में — इधर-उधर रखकर भूले; अँधेरे कोनों में और ऊँचे स्थानों पर देखें",
        "hint": "You have not lost the item — you placed it somewhere and forgot. Focus on dark, shadowy corners of rooms and on high surfaces where you do not normally look — the top of a wardrobe, a high shelf, or a corner behind a door. Bring light into dark areas and look upward; the item is waiting where you left it.",
        "hint_hi": "आपने वस्तु खोई नहीं — आपने इसे कहीं रखा और भूल गए। कमरों के अंधेरे, छायादार कोनों और ऊंची सतहों पर ध्यान दें — अलमारी के ऊपर, ऊंची शेल्फ, दरवाजे के पीछे कोना। अंधेरे क्षेत्रों में रोशनी लाएं और ऊपर देखें।",
    },
    55: {
        "location": "Has left your possession — if found, through someone else's help",
        "location_hi": "आपके पास से चली गई है — मिले तो किसी दूसरे की मदद से मिलेगी",
        "hint": "The item has moved beyond your reach and your own searching will not recover it. Recovery is possible but only through the intervention of another person — a friend, a contact, or someone who happens to come across it. Spread the word among people you trust and let others help; a solo search at this point is ineffective.",
        "hint_hi": "वस्तु आपकी पहुँच से बाहर चली गई है और अकेले खोजने से नहीं मिलेगी। मिलना संभव है लेकिन किसी और के हस्तक्षेप से — कोई मित्र, संपर्क, या संयोगवश कोई जो इसे पाए। अपने विश्वस्त लोगों को बताएं।",
    },
    56: {
        "location": "Gone due to servants' conspiracy — hard to find; investigate guilty servant",
        "location_hi": "दो नौकरों के षड्यन्त्र से गई — मिलना कठिन; दोषी नौकर की तहकीकात करें",
        "hint": "Two domestic helpers have colluded and the item has been deliberately taken. Recovery is difficult but not impossible. Conduct a careful and quiet investigation — observe their behaviour, check their belongings if appropriate, and question each one separately. Do not tip them off that you suspect collusion; gather evidence first.",
        "hint_hi": "दो घरेलू नौकरों ने मिलकर वस्तु जानबूझकर ली है। मिलना मुश्किल लेकिन असंभव नहीं। सावधानी से और चुपचाप जाँच करें — उनके व्यवहार पर नजर रखें, अलग-अलग से पूछताछ करें। पहले साक्ष्य इकट्ठा करें।",
    },
    57: {
        "location": "With help of a young person or child — they will find it",
        "location_hi": "किसी नवयुवक या बच्चे की सहायता से मिलेगी",
        "hint": "Enlist the help of a young person in your household — a teenager, a young adult, or an energetic child. They either know where the item is or have a natural curiosity and energy that will lead them to it quickly. Describe the item clearly and ask them to search; their fresh eyes and different perspective will succeed where yours has not.",
        "hint_hi": "घर में किसी युवा व्यक्ति की सहायता लें — किशोर, युवा वयस्क, या ऊर्जावान बच्चा। वे या तो जानते हैं कि वस्तु कहाँ है या उनकी स्वाभाविक जिज्ञासा उन्हें जल्दी ढूंढ देगी। वस्तु का स्पष्ट विवरण दें।",
    },
    58: {
        "location": "On the roof or upper part of the house — servant will help retrieve it",
        "location_hi": "घर की छत पर या ऊपर के भाग में — नौकर के द्वारा प्राप्त होगी",
        "hint": "The item has ended up on the roof, terrace, or the upper floor of your home — likely placed there by a domestic helper while doing laundry, airing things, or cleaning. Ask the servant who works on those floors; they will know where it is and will be able to retrieve it for you.",
        "hint_hi": "वस्तु घर की छत, टेरेस या ऊपरी मंजिल पर पहुँच गई है — शायद कोई नौकर कपड़े सुखाते, हवा लगाते या सफाई करते वहाँ रख आया। उस नौकर से पूछें जो उस मंजिल पर काम करता है; वह जानता होगा।",
    },
    59: {
        "location": "Near where you were when you discovered the loss — or near a relative or cup/vessel",
        "location_hi": "जहाँ खोने का पता लगा वहाँ या उसके पास — किसी संबंधी द्वारा या प्याले के पास",
        "hint": "Return physically to the exact spot where you first realised the item was missing — the room, the chair, the table where the absence struck you. Search a small radius around that spot carefully, including any cup, vessel, or container nearby. Also check if a relative who was present at that moment has inadvertently picked it up.",
        "hint_hi": "उस स्थान पर वापस जाएं जहाँ आपको पहले पता चला कि वस्तु गई है — वह कमरा, कुर्सी, टेबल। उस स्थान के आसपास छोटे दायरे में सावधानी से खोजें और पास के किसी प्याले या बर्तन में भी देखें।",
    },
    60: {
        "location": "Where water is stored — look around that area",
        "location_hi": "जहाँ पानी रखा जाता है — वहीं आस-पास देखने से मिल जाएगी",
        "hint": "Go to where water is stored in your home — the matka shelf, the water cooler, the water filter, the refrigerator — and search the surrounding area thoroughly. Look on top of, below, beside, and behind each water storage unit. The item is in this zone and will be found with a patient and thorough search.",
        "hint_hi": "घर में पानी रखने की जगह पर जाएं — मटका की शेल्फ, वाटर कूलर, वाटर फिल्टर, फ्रिज — और आसपास के क्षेत्र में अच्छी तरह खोजें। हर पानी भंडारण इकाई के ऊपर, नीचे, बगल में और पीछे देखें।",
    },
    61: {
        "location": "Stand where item was lost — look around — it is right at your feet",
        "location_hi": "जहाँ खोई है वहीं खड़े होकर आसपास देखो — पैरों के पास ही है",
        "hint": "Go back to the last place you remember having the item and stand still. Look slowly and deliberately in every direction — down at your feet, behind you, to each side. The item has not travelled far; it is on the floor, beneath something, or in a crack nearby. Stop and look rather than moving around.",
        "hint_hi": "जहाँ आखिरी बार वस्तु थी वहाँ जाकर खड़े हो जाएं। धीरे-धीरे और जानबूझकर हर दिशा में देखें — पैरों के नीचे, पीछे, दोनों तरफ। वस्तु दूर नहीं गई; फर्श पर, किसी चीज के नीचे, या पास की दरार में है।",
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
