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
