"""
prashnavali_engine.py — Sacred Oracle Engine
==============================================
Implements four Vedic divination systems:
  1. Ram Shalaka Prashnavali (15x15 grid of Rama names)
  2. Hanuman Prashna (40 Chaupais)
  3. Ramcharitmanas Prashna (Tulsidas verses)
  4. Gita Prashna (50 Gita slokas as oracle)

All use hash(question + current_date) for deterministic daily answers.
"""
import hashlib
from datetime import date

# ============================================================
# 1. RAM SHALAKA — 15x15 grid of Rama name syllables
# ============================================================
# Traditional Ram Shalaka uses syllables from Rama's names.
# The 225 cells contain syllables that form responses when selected.
_RAMA_SYLLABLES = [
    "श्री", "रा", "म", "ज", "य", "श्री", "रा", "म", "ज", "य", "श्री", "रा", "म", "ज", "य",
    "सी", "ता", "रा", "म", "च", "न्द्र", "की", "ज", "य", "श्री", "रा", "म", "ज", "य", "श्री",
    "ह", "नु", "मा", "न", "की", "ज", "य", "श्री", "रा", "म", "ज", "य", "श्री", "रा", "म",
    "रा", "म", "ज", "य", "श्री", "सी", "ता", "रा", "म", "ज", "य", "हा", "रे", "रा", "म",
    "ज", "य", "हा", "रे", "रा", "म", "ज", "य", "रा", "म", "ज", "य", "श्री", "सी", "ता",
    "श्री", "रा", "म", "ज", "य", "सी", "ता", "रा", "म", "ज", "य", "हा", "रे", "रा", "म",
    "रा", "घ", "व", "श्री", "रा", "म", "ज", "य", "दा", "श", "र", "थी", "रा", "म", "ज",
    "य", "सु", "ग्री", "व", "सा", "रथी", "रा", "म", "ज", "य", "भ", "र", "त", "रा", "म",
    "ल", "क्ष्म", "ण", "रा", "म", "ज", "य", "शत्रु", "घ्न", "रा", "म", "ज", "य", "श्री", "हरि",
    "रा", "म", "ना", "म", "सु", "ख", "दा", "ई", "रा", "म", "ज", "य", "सी", "ता", "रा",
    "म", "ज", "य", "रा", "म", "ज", "य", "श्री", "रा", "म", "ज", "य", "सी", "ता", "रा",
    "ओम", "श्री", "रा", "म", "ज", "य", "रा", "म", "ज", "य", "श्री", "सी", "ता", "रा", "म",
    "रा", "म", "ज", "य", "श्री", "रा", "म", "ज", "य", "श्री", "हरि", "ओम", "रा", "म", "ज",
    "य", "श्री", "रा", "म", "रा", "म", "रा", "म", "ज", "य", "रा", "म", "ज", "य", "श्री",
    "श्री", "रा", "म", "ज", "य", "श्री", "रा", "म", "ज", "य", "श्री", "रा", "म", "ज", "य",
]

RAM_SHALAKA_GRID = [_RAMA_SYLLABLES[i * 15:(i + 1) * 15] for i in range(15)]

# Ram Shalaka answers (9 possible outcomes mapped to grid regions)
_RAM_SHALAKA_ANSWERS = [
    {
        "answer": "Highly Auspicious",
        "verse": "श्री राम जय राम जय जय राम",
        "meaning": "Your wish will be fulfilled. Lord Rama's blessings are with you. "
                   "Proceed with confidence and faith.",
    },
    {
        "answer": "Auspicious with Effort",
        "verse": "करम प्रधान विश्व करि राखा। जो जस करहि सो तस फल चाखा।",
        "meaning": "Success is assured but requires dedicated effort. "
                   "Put in the work and Rama will support your endeavors.",
    },
    {
        "answer": "Wait and Watch",
        "verse": "धीरज धरम मित्र अरु नारी। आपद काल परखिए चारी।",
        "meaning": "This is not the right time for action. Exercise patience. "
                   "The situation will become clearer soon.",
    },
    {
        "answer": "Moderate Success",
        "verse": "होइहि सोइ जो राम रचि राखा। को करि तरक बढ़ावै साखा।",
        "meaning": "Partial success is indicated. Accept what comes with grace. "
                   "Not everything will go as planned, but the outcome will be acceptable.",
    },
    {
        "answer": "Obstacle Ahead",
        "verse": "बिपति कसौटी जे कसे सोइ साँचे मीत।",
        "meaning": "An obstacle lies ahead. Seek guidance from a trusted elder. "
                   "This challenge will test your character but strengthen you.",
    },
    {
        "answer": "Very Auspicious",
        "verse": "मंगल भवन अमंगल हारी। द्रवउ सो दशरथ अजिर बिहारी।",
        "meaning": "Extremely favorable outcome. All obstacles will be removed. "
                   "Divine grace is flowing in your direction.",
    },
    {
        "answer": "Seek Guidance",
        "verse": "गुरु बिन भवनिधि तरइ न कोई। जो बिरंचि शंकर सम होई।",
        "meaning": "Consult a guru or wise advisor before proceeding. "
                   "The answer lies in seeking counsel, not acting alone.",
    },
    {
        "answer": "Transform Approach",
        "verse": "परहित सरिस धर्म नहिं भाई। पर पीड़ा सम नहिं अधमाई।",
        "meaning": "Change your approach. Consider the well-being of others in your plan. "
                   "Selfless action will unlock the path forward.",
    },
    {
        "answer": "Divine Timing",
        "verse": "होइ है वही जो राम रचि राखा।",
        "meaning": "Trust in divine timing. What is meant for you will come. "
                   "Release anxiety and surrender to the cosmic plan.",
    },
]


# ============================================================
# 2. HANUMAN CHAUPAI — 40 Chaupais with answer meanings
# ============================================================
HANUMAN_CHAUPAI = [
    {"chaupai": "जय हनुमान ज्ञान गुन सागर। जय कपीस तिहुँ लोक उजागर।",
     "meaning": "Victory is assured. Your knowledge and virtues will illuminate the path ahead."},
    {"chaupai": "राम दूत अतुलित बल धामा। अंजनि पुत्र पवन सुत नामा।",
     "meaning": "Immense strength supports you. Like Hanuman, you have untapped power within."},
    {"chaupai": "महावीर विक्रम बजरंगी। कुमति निवार सुमति के संगी।",
     "meaning": "Bad thoughts and plans will be dispelled. Good wisdom will be your companion."},
    {"chaupai": "कंचन वरन वीराज सुवेसा। कानन कुंडल कुंचित केसा।",
     "meaning": "Prosperity and beauty await. Adorn yourself with confidence."},
    {"chaupai": "हाथ वज्र औ ध्वजा बिराजे। काँधे मूँज जनेऊ साजे।",
     "meaning": "You carry the weapons of determination. Wear your sacred thread of purpose."},
    {"chaupai": "शंकर सुवन केसरी नन्दन। तेज प्रताप महा जग वन्दन।",
     "meaning": "Your brilliance will be honored by the world. Great respect is coming."},
    {"chaupai": "विद्यावान गुणी अति चातुर। राम काज करिबे को आतुर।",
     "meaning": "Your skills and knowledge are sufficient. Be eager to serve the higher purpose."},
    {"chaupai": "प्रभु चरित्र सुनिबे को रसिया। राम लखन सीता मन बसिया।",
     "meaning": "Listen to divine stories. Keep the divine in your heart for guidance."},
    {"chaupai": "सूक्ष्म रूप धरि सियहिं दिखावा। विकट रूप धरि लंक जरावा।",
     "meaning": "Sometimes subtlety wins, sometimes boldness. Choose your form wisely."},
    {"chaupai": "भीम रूप धरि असुर संहारे। रामचंद्र के काज संवारे।",
     "meaning": "Take fierce action against obstacles. Your mighty effort will accomplish the mission."},
    {"chaupai": "लाय सजीवन लखन जियाये। श्री रघुवीर हरषि उर लाये।",
     "meaning": "Healing is coming. What seemed lost will be restored to life."},
    {"chaupai": "रघुपति कीन्ही बहुत बड़ाई। तुम मम प्रिय भरतहि सम भाई।",
     "meaning": "Your efforts will be deeply appreciated by those in authority."},
    {"chaupai": "सहस वदन तुम्हरो जस गावैं। अस कहि श्रीपति कंठ लगावैं।",
     "meaning": "Thousands will sing your praise. Divine embrace awaits."},
    {"chaupai": "सनकादिक ब्रह्मादि मुनीसा। नारद शारद सहित अहीसा।",
     "meaning": "Even the greatest sages support your endeavor. You are on the right path."},
    {"chaupai": "जम कुबेर दिगपाल जहाँ ते। कवि कोविद कहि सके कहाँ ते।",
     "meaning": "Your accomplishments will go beyond what words can describe."},
    {"chaupai": "तुम उपकार सुग्रीवहिं कीन्हा। राम मिलाय राज पद दीन्हा।",
     "meaning": "Your help to others will be returned manifold. A position of honor awaits."},
    {"chaupai": "तुम्हरो मंत्र विभीषण माना। लंकेश्वर भए सब जग जाना।",
     "meaning": "Your counsel will be heeded and lead to great transformation."},
    {"chaupai": "जुग सहस्र जोजन पर भानू। लील्यो ताहि मधुर फल जानू।",
     "meaning": "Even impossible goals are within reach. What seems distant is actually close."},
    {"chaupai": "प्रभु मुद्रिका मेलि मुख माहीं। जलधि लाँघि गये अचरज नाहीं।",
     "meaning": "With divine authority, no ocean is uncrossable. Carry the master's seal."},
    {"chaupai": "दुर्गम काज जगत के जेते। सुगम अनुग्रह तुम्हरे तेते।",
     "meaning": "All difficult tasks become easy with divine grace on your side."},
    {"chaupai": "राम दुआरे तुम रखवारे। होत न आज्ञा बिनु पैसारे।",
     "meaning": "You are protected at the divine gate. Nothing enters without permission."},
    {"chaupai": "सब सुख लहैं तुम्हारी शरना। तुम रक्षक काहू को डर ना।",
     "meaning": "All happiness comes to those who seek your shelter. Fear nothing."},
    {"chaupai": "आपन तेज सम्हारो आपै। तीनों लोक हाँक तें काँपै।",
     "meaning": "Control your own power. The three worlds tremble at your roar."},
    {"chaupai": "भूत पिशाच निकट नहिं आवै। महावीर जब नाम सुनावै।",
     "meaning": "No evil can approach you. Chant the divine name for protection."},
    {"chaupai": "नासै रोग हरै सब पीरा। जपत निरंतर हनुमत वीरा।",
     "meaning": "Diseases and pain will vanish. Continuous devotion brings healing."},
    {"chaupai": "संकट तें हनुमान छुड़ावै। मन क्रम वचन ध्यान जो लावै।",
     "meaning": "Hanuman frees from all troubles. Focus your mind, actions, and words."},
    {"chaupai": "सब पर राम तपस्वी राजा। तिनके काज सकल तुम साजा।",
     "meaning": "Rama is king of all ascetics. Through devotion, all tasks are accomplished."},
    {"chaupai": "और मनोरथ जो कोई लावै। सोइ अमित जीवन फल पावै।",
     "meaning": "Whatever desire you bring to the divine, you will receive infinite blessings."},
    {"chaupai": "चारों जुग परताप तुम्हारा। है परसिद्ध जगत उजियारा।",
     "meaning": "Your glory spans all four ages. You are famous as the light of the world."},
    {"chaupai": "साधु संत के तुम रखवारे। असुर निकन्दन राम दुलारे।",
     "meaning": "You protect the virtuous and destroy evil. You are beloved of the divine."},
    {"chaupai": "अष्ट सिद्धि नौ निधि के दाता। अस वर दीन्ह जानकी माता।",
     "meaning": "Eight mystical powers and nine treasures can be granted. Mother Sita has blessed this."},
    {"chaupai": "राम रसायन तुम्हरे पासा। सदा रहो रघुपति के दासा।",
     "meaning": "The elixir of Rama is with you. Remain in devoted service always."},
    {"chaupai": "तुम्हरे भजन राम को पावै। जनम जनम के दुख बिसरावै।",
     "meaning": "Through devotion, Rama is attained. Lifetimes of sorrow are forgotten."},
    {"chaupai": "अन्त काल रघुबर पुर जाई। जहाँ जन्म हरि भक्त कहाई।",
     "meaning": "In the end, you reach the divine abode. Wherever you are born, you are called a devotee."},
    {"chaupai": "और देवता चित्त न धरई। हनुमत सेई सर्व सुख करई।",
     "meaning": "No need to seek other deities. Hanuman's service brings all happiness."},
    {"chaupai": "संकट कटै मिटै सब पीरा। जो सुमिरै हनुमत बलवीरा।",
     "meaning": "All troubles are cut and pain removed for those who remember mighty Hanuman."},
    {"chaupai": "जय जय जय हनुमान गोसाईं। कृपा करहु गुरुदेव की नाईं।",
     "meaning": "Victory! Victory! Victory! Have mercy like a divine teacher."},
    {"chaupai": "जो सत बार पाठ कर कोई। छूटहि बन्दी महा सुख होई।",
     "meaning": "Reading this a hundred times frees one from all bondage. Great happiness follows."},
    {"chaupai": "जो यह पढ़ै हनुमान चालीसा। होय सिद्धि साखी गौरीसा।",
     "meaning": "Whoever reads the Hanuman Chalisa attains perfection. Lord Shiva is witness."},
    {"chaupai": "तुलसीदास सदा हरि चेरा। कीजै नाथ हृदय मँह डेरा।",
     "meaning": "Tulsidas is forever Hari's servant. May the Lord dwell in your heart always."},
]


# ============================================================
# 3. GITA SLOKAS ORACLE — 50 slokas with oracle interpretations
# ============================================================
GITA_SLOKAS_ORACLE = [
    {"sloka": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन (2.47)",
     "meaning": "Focus on action, not results. Do your duty without attachment to outcomes."},
    {"sloka": "योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय (2.48)",
     "meaning": "Perform work in yoga, abandoning attachment. Stay centered in equanimity."},
    {"sloka": "नैनं छिन्दन्ति शस्त्राणि नैनं दहति पावकः (2.23)",
     "meaning": "The soul cannot be cut or burned. You are eternal — this challenge cannot truly harm you."},
    {"sloka": "वासांसि जीर्णानि यथा विहाय (2.22)",
     "meaning": "As one discards worn-out clothes, the soul takes new ones. Embrace transformation."},
    {"sloka": "क्लैब्यं मा स्म गमः पार्थ नैतत्त्वय्युपपद्यते (2.3)",
     "meaning": "Do not yield to weakness. It does not befit you. Stand up and face the challenge."},
    {"sloka": "उद्धरेदात्मनात्मानं नात्मानमवसादयेत् (6.5)",
     "meaning": "Elevate yourself by your own effort. Do not degrade yourself. You are your own friend and enemy."},
    {"sloka": "श्रद्धावान्लभते ज्ञानम् (4.39)",
     "meaning": "The faithful obtain knowledge. Trust the process and wisdom will come."},
    {"sloka": "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत (4.7)",
     "meaning": "Whenever dharma declines, divine intervention arises. Help is on the way."},
    {"sloka": "सर्वधर्मान्परित्यज्य मामेकं शरणं व्रज (18.66)",
     "meaning": "Surrender all duties to the Divine. You will be freed from all sins. Do not grieve."},
    {"sloka": "मन्मना भव मद्भक्तो मद्याजी मां नमस्कुरु (18.65)",
     "meaning": "Fix your mind on the Divine, be devoted, worship, and bow down. You shall come to Me."},
    {"sloka": "न हि ज्ञानेन सदृशं पवित्रमिह विद्यते (4.38)",
     "meaning": "There is nothing as purifying as knowledge. Seek understanding above all."},
    {"sloka": "ध्यायतो विषयान्पुंसः सङ्गस्तेषूपजायते (2.62)",
     "meaning": "Dwelling on sense objects creates attachment. Guard your thoughts carefully."},
    {"sloka": "यो मां पश्यति सर्वत्र सर्वं च मयि पश्यति (6.30)",
     "meaning": "One who sees the Divine everywhere is never lost. See the sacred in all things."},
    {"sloka": "अनन्याश्चिन्तयन्तो मां ये जनाः पर्युपासते (9.22)",
     "meaning": "Those who worship with undivided devotion — the Divine carries what they lack."},
    {"sloka": "पत्रं पुष्पं फलं तोयं यो मे भक्त्या प्रयच्छति (9.26)",
     "meaning": "A leaf, flower, fruit, or water offered with devotion — the Divine accepts the love behind it."},
    {"sloka": "समोऽहं सर्वभूतेषु न मे द्वेष्योऽस्ति न प्रियः (9.29)",
     "meaning": "The Divine is equal to all beings. None is hated, none is favored. Act with fairness."},
    {"sloka": "अपि चेत्सुदुराचारो भजते मामनन्यभाक् (9.30)",
     "meaning": "Even the worst sinner who turns to the Divine wholeheartedly is transformed. It's never too late."},
    {"sloka": "अश्रद्दधानाः पुरुषा धर्मस्य परन्तप (9.3)",
     "meaning": "Those without faith fail to reach the Divine. Cultivate trust and faith in your journey."},
    {"sloka": "दैवी ह्येषा गुणमयी मम माया दुरत्यया (7.14)",
     "meaning": "Divine illusion is difficult to overcome. But those who surrender to the Divine cross beyond it."},
    {"sloka": "ईश्वरः सर्वभूतानां हृद्देशेऽर्जुन तिष्ठति (18.61)",
     "meaning": "The Divine dwells in the heart of all beings. Look within for your answer."},
    {"sloka": "तमेव शरणं गच्छ सर्वभावेन भारत (18.62)",
     "meaning": "Take refuge in the Divine with your whole being. Supreme peace and eternal abode await."},
    {"sloka": "यत्करोषि यदश्नासि यज्जुहोषि ददासि यत् (9.27)",
     "meaning": "Whatever you do, eat, offer, or give away — do it as an offering to the Divine."},
    {"sloka": "सुखदुःखे समे कृत्वा लाभालाभौ जयाजयौ (2.38)",
     "meaning": "Treat pleasure and pain, gain and loss, victory and defeat alike. Then fight. You shall incur no sin."},
    {"sloka": "प्रकृतेः क्रियमाणानि गुणैः कर्माणि सर्वशः (3.27)",
     "meaning": "All actions are performed by the gunas of nature. The wise see this and do not cling."},
    {"sloka": "यो न हृष्यति न द्वेष्टि न शोचति न काङ्क्षति (12.17)",
     "meaning": "One who neither rejoices nor hates, neither grieves nor desires — such a devotee is dear to the Divine."},
    {"sloka": "तस्माद्योगी भवार्जुन (6.46)",
     "meaning": "Therefore, be a yogi, Arjuna. Of all paths, the yoga of devoted practice is supreme."},
    {"sloka": "विद्याविनयसम्पन्ने ब्राह्मणे गवि हस्तिनि (5.18)",
     "meaning": "The wise see equally a learned Brahmin, a cow, an elephant, a dog, and an outcast. See unity in all."},
    {"sloka": "सर्वभूतस्थमात्मानं सर्वभूतानि चात्मनि (6.29)",
     "meaning": "See yourself in all beings and all beings in yourself. This is the vision of oneness."},
    {"sloka": "बहूनां जन्मनामन्ते ज्ञानवान्मां प्रपद्यते (7.19)",
     "meaning": "After many births, the wise one surrenders to the Divine. Such a great soul is very rare."},
    {"sloka": "अन्तकाले च मामेव स्मरन्मुक्त्वा कलेवरम् (8.5)",
     "meaning": "Whoever remembers the Divine at the time of death attains the supreme state."},
    {"sloka": "ये यथा मां प्रपद्यन्ते तांस्तथैव भजाम्यहम् (4.11)",
     "meaning": "As you approach the Divine, so does the Divine respond. Your path is honored."},
    {"sloka": "ज्ञानं ते ऽहं सविज्ञानम् इदं वक्ष्याम्यशेषतः (7.2)",
     "meaning": "Complete knowledge and wisdom will be revealed to you. Nothing will remain unknown."},
    {"sloka": "मयि सर्वमिदं प्रोतं सूत्रे मणिगणा इव (7.7)",
     "meaning": "All this is strung on the Divine like pearls on a thread. Everything is connected."},
    {"sloka": "न मे विदुः सुरगणाः प्रभवं न महर्षयः (10.2)",
     "meaning": "Even the gods and great sages do not know the Divine origin. Trust that mystery is part of the path."},
    {"sloka": "यत्रयोगेश्वरः कृष्णो यत्र पार्थो धनुर्धरः (18.78)",
     "meaning": "Where there is the Divine and the devoted warrior together, there is victory, prosperity, and justice."},
    {"sloka": "अभ्यासयोगेन ततो मामिच्छाप्तुं धनञ्जय (12.9)",
     "meaning": "If you cannot fix your mind on the Divine, seek through the yoga of practice. Discipline leads to attainment."},
    {"sloka": "श्रेयो हि ज्ञानमभ्यासात् (12.12)",
     "meaning": "Knowledge is better than practice without understanding. But renunciation of results surpasses even knowledge."},
    {"sloka": "अद्वेष्टा सर्वभूतानां मैत्रः करुण एव च (12.13)",
     "meaning": "Be without hatred for any being, be friendly and compassionate. This is the mark of the devoted."},
    {"sloka": "समः शत्रौ च मित्रे च तथा मानापमानयोः (12.18)",
     "meaning": "Be equal toward friend and foe, in honor and dishonor, heat and cold. Free from attachment."},
    {"sloka": "सत्त्वानुरूपा सर्वस्य श्रद्धा भवति भारत (17.3)",
     "meaning": "Everyone's faith is according to their nature. Your faith reflects who you truly are."},
    {"sloka": "त्रिविधा भवति श्रद्धा देहिनां सा स्वभावजा (17.2)",
     "meaning": "Faith is of three kinds — sattvic, rajasic, and tamasic. Cultivate the pure, sattvic faith."},
    {"sloka": "आहारस्त्वपि सर्वस्य त्रिविधो भवति प्रियः (17.7)",
     "meaning": "Food is also of three kinds. Nourish yourself with pure, wholesome sustenance."},
    {"sloka": "दानं तपश्च कर्म च न त्याज्यं कार्यमेव तत् (18.5)",
     "meaning": "Charity, austerity, and action should never be abandoned. They purify the wise."},
    {"sloka": "ब्रह्मण्याधाय कर्माणि सङ्गं त्यक्त्वा करोति यः (5.10)",
     "meaning": "One who acts offering all to the Divine, abandoning attachment — sin does not touch them."},
    {"sloka": "सर्वस्य चाहं हृदि सन्निविष्टो (15.15)",
     "meaning": "The Divine is seated in the heart of all. From the Divine come memory, knowledge, and their absence."},
    {"sloka": "ऊर्ध्वमूलमधःशाखम् अश्वत्थं प्राहुरव्ययम् (15.1)",
     "meaning": "The sacred tree has its roots above and branches below. Cut attachment with the weapon of detachment."},
    {"sloka": "द्वाविमौ पुरुषौ लोके क्षरश्चाक्षर एव च (15.16)",
     "meaning": "Two types of beings exist — the perishable and the imperishable. Beyond both is the Supreme."},
    {"sloka": "मच्चित्तः सर्वदुर्गाणि मत्प्रसादात्तरिष्यसि (18.58)",
     "meaning": "With your consciousness fixed on the Divine, you shall overcome all difficulties by grace."},
    {"sloka": "यत्र प्रकाशं सत्त्वस्थं प्रवृत्तिं च सञ्जय (14.22)",
     "meaning": "When sattva (goodness) increases, there is light, knowledge, and clarity. Seek this state."},
    {"sloka": "इति ते ज्ञानमाख्यातं गुह्याद्गुह्यतरं मया (18.63)",
     "meaning": "The most secret of all secrets has been revealed. Reflect on it fully, then act as you wish."},
]


# ============================================================
# HELPER — deterministic hash selection
# ============================================================
def _hash_select(question: str, max_index: int) -> int:
    """
    Produce a deterministic index from question + current date.
    Same question on the same day always returns the same index.
    """
    today = date.today().isoformat()
    raw = f"{question.strip().lower()}|{today}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return int(h, 16) % max_index


# ============================================================
# PUBLIC API
# ============================================================

def ram_shalaka(row: int, col: int) -> dict:
    """
    Ram Shalaka Prashnavali — select a cell from the 15x15 grid.

    Args:
        row: Row index (0-14)
        col: Column index (0-14)

    Returns:
        dict with syllable, answer, verse, meaning
    """
    if not (0 <= row < 15 and 0 <= col < 15):
        raise ValueError(f"Row and col must be 0-14. Got row={row}, col={col}")

    syllable = RAM_SHALAKA_GRID[row][col]

    # Map grid position to answer using combined position hash
    answer_idx = (row * 15 + col) % len(_RAM_SHALAKA_ANSWERS)
    answer = _RAM_SHALAKA_ANSWERS[answer_idx]

    return {
        "syllable": syllable,
        "answer": answer["answer"],
        "verse": answer["verse"],
        "meaning": answer["meaning"],
    }


def hanuman_prashna(question: str) -> dict:
    """
    Hanuman Prashna — answer a question using Hanuman Chalisa chaupais.

    Args:
        question: The question being asked

    Returns:
        dict with answer, chaupai, meaning
    """
    idx = _hash_select(question, len(HANUMAN_CHAUPAI))
    selected = HANUMAN_CHAUPAI[idx]

    # Determine answer tone based on chaupai index
    if idx < 10:
        answer = "Highly Favorable"
    elif idx < 20:
        answer = "Favorable with Effort"
    elif idx < 30:
        answer = "Proceed with Devotion"
    else:
        answer = "Auspicious and Blessed"

    return {
        "answer": answer,
        "chaupai": selected["chaupai"],
        "meaning": selected["meaning"],
    }


def ramcharitmanas_prashna(question: str) -> dict:
    """
    Ramcharitmanas Prashna — answer using Ram Shalaka answer verses.

    Args:
        question: The question being asked

    Returns:
        dict with answer, verse, meaning
    """
    idx = _hash_select(question, len(_RAM_SHALAKA_ANSWERS))
    selected = _RAM_SHALAKA_ANSWERS[idx]

    return {
        "answer": selected["answer"],
        "verse": selected["verse"],
        "meaning": selected["meaning"],
    }


def gita_prashna(question: str) -> dict:
    """
    Gita Prashna — answer a question using Bhagavad Gita slokas.

    Args:
        question: The question being asked

    Returns:
        dict with answer, sloka, meaning
    """
    idx = _hash_select(question, len(GITA_SLOKAS_ORACLE))
    selected = GITA_SLOKAS_ORACLE[idx]

    # Generate answer summary based on the sloka's meaning
    meaning_lower = selected["meaning"].lower()
    if any(w in meaning_lower for w in ["surrender", "refuge", "divine", "grace"]):
        answer = "Surrender to the Divine Path"
    elif any(w in meaning_lower for w in ["action", "duty", "work", "fight"]):
        answer = "Act with Detached Determination"
    elif any(w in meaning_lower for w in ["knowledge", "wisdom", "understanding"]):
        answer = "Seek Knowledge and Clarity"
    elif any(w in meaning_lower for w in ["faith", "devotion", "worship"]):
        answer = "Cultivate Faith and Devotion"
    elif any(w in meaning_lower for w in ["equal", "unity", "oneness"]):
        answer = "See Unity in All Things"
    else:
        answer = "Trust the Cosmic Order"

    return {
        "answer": answer,
        "sloka": selected["sloka"],
        "meaning": selected["meaning"],
    }
