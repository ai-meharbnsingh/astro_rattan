import React from 'react';
import { Heading } from '@/components/ui/heading';
import { Lightbulb } from 'lucide-react';

interface AnalysisTheorySectionProps {
  language: string;
  tab: string;
}

export default function AnalysisTheorySection({ language, tab }: AnalysisTheorySectionProps) {
  const hi = language === 'hi';

  const contentMap: Record<string, { titleEn: string; titleHi: string; bodyEn: string; bodyHi: string }> = {
    shadbala: {
      titleEn: 'Shadbala (Six-fold Strength) Detailed Theory',
      titleHi: 'षड्बल (छह-गुना बल) विस्तृत सिद्धांत',
      bodyEn:
        'Shadbala is the primary mathematical system in Vedic Astrology to determine the exact potency of a planet. It consists of six distinct strengths: 1. Sthana Bala (Positional strength based on zodiac signs), 2. Dig Bala (Directional strength — planets are strongest in specific compass directions), 3. Kaala Bala (Temporal strength based on day/night, lunar phase, and seasonal cycles), 4. Chestha Bala (Motional strength based on planetary speed and retrograde motion), 5. Naisargika Bala (Natural inherent brightness), and 6. Drik Bala (Aspectual strength — how other planets strengthen or weaken it by sight). A planet with high Shadbala acts as a "strong commander" in your chart, capable of delivering its full promises during its dasha (period). If Shadbala is low, the planet may struggle to fulfill its responsibilities despite being in a good house.',
      bodyHi:
        'षड्बल वैदिक ज्योतिष में किसी ग्रह की सटीक शक्ति निर्धारित करने की मुख्य गणितीय प्रणाली है। इसमें छह अलग-अलग बल शामिल हैं: १. स्थान बल (राशियों के आधार पर), २. दिग बल (दिशात्मक बल — ग्रह विशिष्ट दिशाओं में सबसे मजबूत होते हैं), ३. काल बल (दिन/रात, चंद्रमा की स्थिति और मौसमी चक्रों के आधार पर), ४. चेष्टा बल (ग्रह की गति और वक्री होने के आधार पर), ५. नैसर्गिक बल (ग्रह की स्वाभाविक चमक), और ६. दृक बल (दृष्टि बल — अन्य ग्रह इसे कैसे प्रभावित करते हैं)। उच्च षड्बल वाला ग्रह आपकी कुंडली में एक "मजबूत सेनापति" की तरह कार्य करता है, जो अपनी दशा के दौरान अपने सभी वादे पूरे करने में सक्षम होता है। यदि षड्बल कम है, तो अच्छा घर होने के बावजूद ग्रह अपनी जिम्मेदारियों को पूरा करने में संघर्ष कर सकता है।',
    },
    kp: {
      titleEn: 'KP System (Krishnamurti Paddhati) Detailed Theory',
      titleHi: 'केपी सिस्टम (कृष्णमूर्ति पद्धति) विस्तृत सिद्धांत',
      bodyEn:
        'The Krishnamurti Paddhati (KP) is a modern, scientific approach to astrology that focuses on pinpoint accuracy in timing events. Unlike traditional systems that look at whole signs, KP divides the zodiac into 249 "Subs" (Sub-Lords). The core principle is: "A planet gives the results of its Constellation (Nakshatra) Lord, but the quality of that result is determined by its Sub-Lord." If the Sub-Lord of a planet signifies a house, that event is almost certain to happen. KP uses the Placidus (Cuspal) house system, meaning houses can vary in size. It is widely considered the best system for answering binary "Yes/No" questions and finding the exact minute an event will occur.',
      bodyHi:
        'कृष्णमूर्ति पद्धति (केपी) ज्योतिष का एक आधुनिक और वैज्ञानिक दृष्टिकोण है जो घटनाओं के समय की सटीक भविष्यवाणी पर ध्यान केंद्रित करता है। पारंपरिक प्रणालियों के विपरीत, केपी राशियों को २४९ "उप-भागों" (Sub-Lords) में विभाजित करता है। इसका मुख्य सिद्धांत है: "एक ग्रह अपने नक्षत्र स्वामी के परिणाम देता है, लेकिन उस परिणाम की गुणवत्ता उसके उप-स्वामी (Sub-Lord) द्वारा निर्धारित की जाती है।" यदि किसी ग्रह का उप-स्वामी किसी घर का संकेत देता है, तो वह घटना होना लगभग निश्चित है। केपी प्लेसिडस हाउस सिस्टम का उपयोग करता है। इसे बाइनरी "हाँ/नहीं" प्रश्नों का उत्तर देने और घटना के सटीक समय का पता लगाने के लिए सबसे अच्छी प्रणाली माना जाता है।',
    },
    jaimini: {
      titleEn: 'Jaimini Astrology Detailed Theory',
      titleHi: 'जैमिनी ज्योतिष विस्तृत सिद्धांत',
      bodyEn:
        'Jaimini Astrology is a distinct, ancient branch of Vedic Astrology attributed to Sage Jaimini. Its logic is entirely different from the standard Parashari system. Key features include: 1. Chara Karakas: The planets with the highest degrees (Atmakaraka, Amatyakaraka, etc.) become variable significators of the Soul, Career, etc. 2. Sign Aspects (Rashi Drishti): Here, signs (Aries, Taurus, etc.) look at each other, not just planets. 3. Chara Dashas: Timing is based on Signs rather than Nakshatras. Jaimini is exceptionally powerful for identifying Raja Yogas (Great Fortune) and determining the true spiritual destiny of an individual.',
      bodyHi:
        'जैमिनी ज्योतिष महर्षि जैमिनी द्वारा प्रतिपादित वैदिक ज्योतिष की एक प्राचीन और विशिष्ट शाखा है। इसका तर्क मानक पाराशरी प्रणाली से पूरी तरह अलग है। मुख्य विशेषताएं: १. चर कारक: उच्चतम डिग्री वाले ग्रह (आत्मकारक, अमात्यकारक, आदि) आत्मा, करियर आदि के संकेतक बन जाते हैं। २. राशि दृष्टि: यहाँ ग्रह नहीं, बल्कि राशियाँ (मेष, वृष आदि) एक-दूसरे को देखती हैं। ३. चर दशा: यहाँ समय की गणना नक्षत्रों के बजाय राशियों पर आधारित होती है। जैमिनी ज्योतिष राजयोगों की पहचान करने और किसी व्यक्ति के वास्तविक आध्यात्मिक भाग्य का निर्धारण करने के लिए अत्यधिक शक्तिशाली है।',
    },
    pravrajya: {
      titleEn: 'Pravrajya (Renunciation) Yogas Detailed Theory',
      titleHi: 'प्रव्रज्या (वैराग्य) योग विस्तृत सिद्धांत',
      bodyEn:
        'Pravrajya Yogas are planetary combinations that lead a person toward spirituality, detachment, and a life of renunciation. Usually, when 4 or more planets cluster in a single house (especially the 10th or 12th), it creates a strong psychological pull away from material desires. If Saturn is involved, it brings deep discipline; if Sun, it brings authority in spiritual circles; if Moon, it brings deep emotional devotion. These yogas do not always mean becoming a monk; in modern times, they often manifest as high-level spiritual researchers, philosophers, or people who achieve great worldly success but remain completely detached from it internally.',
      bodyHi:
        'प्रव्रज्या योग वे ग्रहीय संयोजन हैं जो व्यक्ति को आध्यात्मिकता, वैराग्य और सन्यास की ओर ले जाते हैं। आमतौर पर, जब एक ही घर (विशेषकर १०वें या १२वें) में ४ या अधिक ग्रह होते हैं, तो यह भौतिक इच्छाओं से दूर एक मजबूत खिंचाव पैदा करता है। यदि इसमें शनि शामिल है, तो यह गहरा अनुशासन लाता है; सूर्य है, तो आध्यात्मिक हलकों में अधिकार लाता है; चंद्रमा है, तो गहरी भक्ति लाता है। इन योगों का मतलब हमेशा साधु बनना नहीं होता; आधुनिक समय में, ये अक्सर उच्च स्तर के आध्यात्मिक शोधकर्ताओं, दार्शनिकों या उन लोगों के रूप में प्रकट होते हैं जो बड़ी सांसारिक सफलता तो पाते हैं लेकिन आंतरिक रूप से उससे पूरी तरह अलग रहते हैं।',
    },
    apatya: {
      titleEn: 'Progeny (Apatya) Detailed Analysis Theory',
      titleHi: 'संतान (अपत्य) विस्तृत विश्लेषण सिद्धांत',
      bodyEn:
        'Apatya analysis studies the potential for children, their health, and the legacy one leaves behind. We primarily analyze three factors: 1. The 5th House (The core house of children), 2. The 5th Lord (Strength of the controller), and 3. Jupiter (Putrakaraka — the universal significator of children). For deep details, we look at the Saptamsha (D7) divisional chart, which is a "magnified view" of the 5th house. We check for "Beeja Sphuta" (for men) and "Kshetra Sphuta" (for women) to ensure biological fertility. Timing of birth is predicted using Dashas and transits of Jupiter and Saturn over the 5th house or its lord.',
      bodyHi:
        'संतान विश्लेषण बच्चों की संभावना, उनके स्वास्थ्य और व्यक्ति द्वारा छोड़ी गई विरासत का अध्ययन करता है। हम मुख्य रूप से तीन कारकों का विश्लेषण करते हैं: १. ५वां घर (संतान का मुख्य घर), २. ५वें घर का स्वामी, और ३. बृहस्पति (पुत्रकारक — बच्चों का सार्वभौमिक संकेतक)। गहन विवरण के लिए, हम सप्तमांश (D7) चार्ट देखते हैं, जो ५वें घर का "विस्तृत दृश्य" है। हम जैविक उर्वरता सुनिश्चित करने के लिए पुरुषों के लिए "बीज स्फुट" और महिलाओं के लिए "क्षेत्र स्फुट" की जांच करते हैं। जन्म के समय की भविष्यवाणी ५वें घर या उसके स्वामी पर बृहस्पति और शनि के गोचर और दशाओं का उपयोग करके की जाती है।',
    },
    'stri-jataka': {
      titleEn: 'Stri Jataka (Female Horoscopy) Detailed Theory',
      titleHi: 'स्त्री जातक (महिला कुंडली) विस्तृत सिद्धांत',
      bodyEn:
        'Stri Jataka is a specialized branch of astrology focused on the unique physiological and psychological makeup of women. While basic rules are the same, certain houses are emphasized: 1. The 7th house (Marriage & Husband), 2. The 8th house (Saubhagya — longevity of marriage), and 3. The 4th house (Chastity & Home). In a female chart, the Moon represents the mind and hormones, while Venus represents beauty and relationship energy. This analysis helps understand the person’s influence on their family, their health cycles, and the specific timing of significant life transformations like marriage and motherhood.',
      bodyHi:
        'स्त्री जातक ज्योतिष की एक विशेष शाखा है जो महिलाओं के अद्वितीय शारीरिक और मनोवैज्ञानिक बनावट पर केंद्रित है। जबकि बुनियादी नियम समान हैं, कुछ घरों पर जोर दिया जाता है: १. ७वां घर (विवाह और पति), २. ८वां घर (सौभाग्य — वैवाहिक आयु), और ३. ४था घर (चरित्र और घर)। महिला की कुंडली में, चंद्रमा मन और हार्मोन का प्रतिनिधित्व करता है, जबकि शुक्र सौंदर्य और संबंधों की ऊर्जा का। यह विश्लेषण व्यक्ति के परिवार पर प्रभाव, उनके स्वास्थ्य चक्र और विवाह और मातृत्व जैसे महत्वपूर्ण जीवन परिवर्तनों के समय को समझने में मदद करता है।',
    },
    conjunctions: {
      titleEn: 'Planetary Conjunctions (Yuti) Detailed Theory',
      titleHi: 'ग्रह युति (युति) विस्तृत सिद्धांत',
      bodyEn:
        'A conjunction occurs when two or more planets occupy the same house in a chart. This blends their energies into a "combined force." The outcome depends on: 1. Degrees: If they are within 5 degrees, the influence is intense. 2. Natural Friendship: If friends join (like Sun and Jupiter), the result is constructive (Raja Yoga). If enemies join (like Saturn and Mars), it creates friction and explosive energy. 3. House: A conjunction in the 10th (Career) will act differently than in the 8th (Obstacles). Think of conjunctions as different colors mixing; the final shade depends on which planet is stronger (higher Shadbala) and which rules better houses.',
      bodyHi:
        'युति तब होती है जब दो या दो से अधिक ग्रह एक ही घर में होते हैं। यह उनकी ऊर्जाओं को एक "संयुक्त बल" में मिला देता है। परिणाम निर्भर करता है: १. डिग्री: यदि वे ५ डिग्री के भीतर हैं, तो प्रभाव तीव्र होता है। २. नैसर्गिक मित्रता: यदि मित्र ग्रह मिलते हैं (जैसे सूर्य और बृहस्पति), तो परिणाम रचनात्मक (राजयोग) होता है। यदि शत्रु मिलते हैं (जैसे शनि और मंगल), तो यह घर्षण और विस्फोटक ऊर्जा पैदा करता है। ३. घर: १०वें घर (करियर) में युति ८वें घर (बाधाओं) से अलग तरह से कार्य करेगी। युतियों को विभिन्न रंगों के मिश्रण के रूप में सोचें; अंतिम रंग इस बात पर निर्भर करता है कि कौन सा ग्रह मजबूत है और कौन सा बेहतर घरों का स्वामी है।',
    },
    roga: {
      titleEn: 'Roga (Medical Astrology) Detailed Theory',
      titleHi: 'रोग (चिकित्सा ज्योतिष) विस्तृत सिद्धांत',
      bodyEn:
        'Medical astrology uses the birth chart to identify physical vulnerabilities and potential health issues. The key markers are: 1. The 6th House (Diseases and recovery), 2. The 8th House (Chronic illness and longevity), and 3. The 12th House (Hospitalization). Each planet governs specific body parts: Sun (Heart/Bones), Moon (Lungs/Blood/Emotions), Mars (Blood/Infections), Mercury (Skin/Nervous System), Jupiter (Liver/Digestion), Venus (Kidneys/Reproduction), and Saturn (Joints/Teeth/Chronic pain). By analyzing these, we can determine the "root cause" of an illness—whether it is physical, mental, or karmic—and predict when health cycles will change.',
      bodyHi:
        'चिकित्सा ज्योतिष शारीरिक कमजोरियों और संभावित स्वास्थ्य समस्याओं की पहचान करने के लिए जन्म कुंडली का उपयोग करता है। मुख्य संकेतक हैं: १. ६ठा घर (रोग और ठीक होना), २. ८वां घर (पुरानी बीमारी और दीर्घायु), और ३. १२वां घर (अस्पताल में भर्ती)। प्रत्येक ग्रह शरीर के विशिष्ट हिस्सों को नियंत्रित करता है: सूर्य (हृदय/हड्डियां), चंद्रमा (फेफड़े/रक्त/भावनाएं), मंगल (रक्त/संक्रमण), बुध (त्वचा/तंत्रिका तंत्र), बृहस्पति (यकृत/पाचन), शुक्र (गुर्दे/प्रजनन), और शनि (जोड़/दांत/पुरानी पीड़ा)। इनका विश्लेषण करके, हम बीमारी के "मूल कारण" का निर्धारण कर सकते हैं और स्वास्थ्य चक्रों के बदलने की भविष्यवाणी कर सकते हैं।',
    },
    'bhava-phala': {
      titleEn: 'Bhava Phala (House Results) Detailed Theory',
      titleHi: 'भाव फल विस्तृत सिद्धांत',
      bodyEn:
        'Bhava Phala is the specific "output" of each of the 12 houses based on the planets residing in them. Every house represents a stage of life: 1st (Identity), 2nd (Wealth), 4th (Comfort), 7th (Partners), 10th (Status), etc. When a planet enters a house, it "activates" that life area with its own nature. For example, Rahu in the 2nd house may give immense wealth but also family friction. Saturn in the 10th house brings great responsibility and slow but steady rise in career. This section gives you the classic interpretation of how each planet "colors" the room it is sitting in, providing a detailed map of your life’s various departments.',
      bodyHi:
        'भाव फल वहां रहने वाले ग्रहों के आधार पर १२ घरों में से प्रत्येक का विशिष्ट "परिणाम" है। प्रत्येक घर जीवन के एक चरण का प्रतिनिधित्व करता है: १ला (पहचान), २रा (धन), ४था (सुविधा), ७वां (साथी), १०वां (प्रतिष्ठा), आदि। जब कोई ग्रह किसी घर में प्रवेश करता है, तो वह उस जीवन क्षेत्र को अपने स्वभाव से "सक्रिय" कर देता है। उदाहरण के लिए, २रे घर में राहु अत्यधिक धन दे सकता है लेकिन पारिवारिक कलह भी। १०वें घर में शनि बड़ी जिम्मेदारी और करियर में धीमी लेकिन स्थिर वृद्धि लाता है। यह खंड आपको बताता है कि प्रत्येक ग्रह जिस घर में बैठा है, उसे कैसे "रंग" देता है।',
    },
    vritti: {
      titleEn: 'Career (Vritti) & Profession Detailed Theory',
      titleHi: 'आजीविका (वृत्ति) और व्यवसाय विस्तृत सिद्धांत',
      bodyEn:
        'Vritti analysis determines how you will earn your livelihood and achieve social status. The primary house is the 10th (Karma Bhava), but we also look at the 2nd (Wealth) and 6th (Daily Service). To find the exact profession, we use: 1. The Lord of the 10th house and its strength. 2. The strongest planet in the chart. 3. The Navamsha (D9) position of the 10th lord (Navamsha-Career). 4. The Dashamsha (D10) chart for professional milestones. For example, if Mercury rules the 10th, the person may be a writer, accountant, or speaker. If Mars rules, they may be a soldier, engineer, or surgeon. This analysis shows your true talent and the periods of professional growth.',
      bodyHi:
        'वृत्ति विश्लेषण यह निर्धारित करता है कि आप अपनी आजीविका कैसे कमाएंगे और सामाजिक स्थिति कैसे प्राप्त करेंगे। मुख्य घर १०वां (कर्म भाव) है, लेकिन हम २रे (धन) और ६ठे (दैनिक सेवा) को भी देखते हैं। सटीक पेशा खोजने के लिए, हम उपयोग करते हैं: १. १०वें घर का स्वामी और उसकी ताकत। २. कुंडली में सबसे मजबूत ग्रह। ३. १०वें स्वामी की नवांश (D9) स्थिति। ४. पेशेवर मील के पत्थर के लिए दशमांश (D10) चार्ट। उदाहरण के लिए, यदि बुध १०वें घर का स्वामी है, तो व्यक्ति लेखक, लेखाकार या वक्ता हो सकता है। यदि मंगल स्वामी है, तो वे सैनिक, इंजीनियर या सर्जन हो सकते हैं।',
    },
    'janma-predictions': {
      titleEn: 'Janma Predictions (General Life Readings) Theory',
      titleHi: 'जन्म फल (सामान्य जीवन भविष्यवाणियां) सिद्धांत',
      bodyEn:
        'Janma Predictions provide a holistic reading of your entire personality based on your birth coordinates. It looks at three main pillars: 1. Lagna (Ascendant): Your physical appearance, temperament, and how the world sees you. 2. Chandra (Moon): Your mental makeup, emotions, and how you perceive the world. 3. Surya (Sun): Your soul, ego, and inner willpower. These readings describe your general life path, luck (bhagya), and recurring patterns in relationships and health. It is the "User Manual" for your life, explaining why you think, act, and feel the way you do.',
      bodyHi:
        'जन्म फल आपके जन्म विवरण के आधार पर आपके पूरे व्यक्तित्व की एक समग्र व्याख्या प्रदान करते हैं। यह तीन मुख्य स्तंभों को देखता है: १. लग्न: आपका शारीरिक स्वरूप, स्वभाव और दुनिया आपको कैसे देखती है। २. चंद्र: आपका मानसिक ढांचा, भावनाएं और आप दुनिया को कैसे समझते हैं। ३. सूर्य: आपकी आत्मा, अहंकार और आंतरिक इच्छाशक्ति। ये भविष्यवाणियां आपके सामान्य जीवन पथ, भाग्य और स्वास्थ्य में आवर्ती पैटर्न का वर्णन करती हैं। यह आपके जीवन का "उपयोगकर्ता मैनुअल" है, जो बताता है कि आप क्यों सोचते, कार्य करते और महसूस करते हैं।',
    },
    iogita: {
      titleEn: 'Iogita (Aptitude & Talent Strength) Detailed Theory',
      titleHi: 'आयोगिता (योग्यता और कौशल शक्ति) विस्तृत सिद्धांत',
      bodyEn:
        'Iogita analysis evaluates your natural "skill set" and mental aptitude. While Career analysis shows *what* you do, Iogita shows *how* well you do it. It looks at planetary combinations (Yogas) that give specific talents: 1. Saraswati Yoga (Intelligence & Music), 2. Budha-Aditya Yoga (Administrative Intelligence), 3. Malavya Yoga (Artistic beauty), etc. This section measures the "quality" of your success. It helps you understand whether your strengths lie in communication, technical analysis, artistic creation, or leadership. Knowing your Iogita allows you to choose paths where you have a natural "unfair advantage" over others.',
      bodyHi:
        'आयोगिता विश्लेषण आपकी स्वाभाविक "कौशल क्षमता" और मानसिक योग्यता का मूल्यांकन करता है। जबकि करियर विश्लेषण यह दिखाता है कि आप *क्या* करते हैं, आयोगिता यह दिखाती है कि आप उसे *कितनी अच्छी तरह* करते हैं। यह उन ग्रहीय योगों को देखता है जो विशिष्ट प्रतिभा देते हैं: १. सरस्वती योग (बुद्धि और संगीत), २. बुध-आदित्य योग (प्रशासनिक बुद्धि), ३. मालव्य योग (कलात्मक सुंदरता) आदि। यह खंड आपकी सफलता की "गुणवत्ता" को मापता है। यह आपको यह समझने में मदद करता है कि आपकी ताकत संचार, तकनीकी विश्लेषण, कलात्मक निर्माण या नेतृत्व में निहित है या नहीं।',
    },
    'navamsha-career': {
      titleEn: 'Navamsha Career Analysis Detailed Theory',
      titleHi: 'नवांश करियर विश्लेषण विस्तृत सिद्धांत',
      bodyEn:
        'The Navamsha (D9) chart is known as the "Fruit" of the tree. The birth chart (D1) is the "Promise," but D9 shows if that promise will actually bear fruit. For career, we specifically look at the Lord of the 10th house from the birth chart and see its position in the D9 chart. If the 10th lord is strong in D9 (in its own or exalted sign), the career will be highly successful and stable. If it is weak in D9, there may be many struggles despite a good-looking D1. The D9 chart becomes increasingly important after the age of 30-35, showing the actual professional destiny and lasting legacy of the individual.',
      bodyHi:
        'नवांश (D9) चार्ट को पेड़ के "फल" के रूप में जाना जाता है। जन्म कुंडली (D1) "वादा" है, लेकिन D9 दिखाता है कि क्या वह वादा वास्तव में फल देगा। करियर के लिए, हम विशेष रूप से जन्म कुंडली के १०वें घर के स्वामी को देखते हैं और D9 चार्ट में उसकी स्थिति देखते हैं। यदि १०वां स्वामी D9 में मजबूत है, तो करियर अत्यधिक सफल और स्थिर होगा। यदि यह D9 में कमजोर है, तो अच्छे D1 के बावजूद कई संघर्ष हो सकते हैं। ३०-३५ वर्ष की आयु के बाद D9 चार्ट तेजी से महत्वपूर्ण हो जाता है, जो वास्तविक पेशेवर भाग्य को दर्शाता है।',
    },
    'graha-sambandha': {
      titleEn: 'Graha Sambandha (Planetary Relations) Detailed Theory',
      titleHi: 'ग्रह सम्बन्ध विस्तृत सिद्धांत',
      bodyEn:
        'Sambandha is the mechanism by which two planets exchange their energies and work together. There are four types of Sambandha: 1. Mutual Aspect: Two planets looking at each other (e.g., Sun in 1st, Saturn in 7th). 2. Exchange (Parivartana): Two planets sitting in each other\'s signs (e.g., Mars in Taurus, Venus in Aries). This is the strongest bond. 3. Conjunction: Sitting together in one house. 4. One-way Aspect: One planet looking at another without a return look. Sambandha creates a "bridge" between two life areas. For example, a bond between the 2nd (Wealth) and 10th (Career) lords creates a strong "Dhana Yoga" or wealth-generating professional life.',
      bodyHi:
        'सम्बन्ध वह तंत्र है जिसके द्वारा दो ग्रह अपनी ऊर्जाओं का आदान-प्रदान करते हैं और मिलकर कार्य करते हैं। सम्बन्ध चार प्रकार के होते हैं: १. आपसी दृष्टि: दो ग्रह एक-दूसरे को देखते हैं। २. परिवर्तन: दो ग्रह एक-दूसरे की राशियों में बैठे हों (जैसे मंगल वृष में, शुक्र मेष में)। यह सबसे मजबूत बंधन है। ३. युति: एक ही घर में साथ बैठना। ४. एकतरफा दृष्टि। सम्बन्ध दो जीवन क्षेत्रों के बीच एक "पुल" बनाता है। उदाहरण के लिए, २रे (धन) और १०वें (करियर) स्वामियों के बीच का बंधन एक मजबूत "धन योग" या धन पैदा करने वाला पेशेवर जीवन बनाता है।',
    },
    'panchadha-maitri': {
      titleEn: 'Panchadha Maitri (5-fold Friendship) Detailed Theory',
      titleHi: 'पंचधा मैत्री (५-गुना मित्रता) विस्तृत सिद्धांत',
      bodyEn:
        'In Astrology, planets aren\'t just points; they have "social relations." Panchadha Maitri calculates the final relationship between two planets by combining: 1. Natural (Naisargika) Relationship: Permanent friendship based on nature (e.g., Sun and Moon are friends). 2. Temporary (Tatkalika) Relationship: Based on where they are sitting in your specific chart (Planets in the 2nd, 3rd, 4th, 10th, 11th, and 12th from each other are temporary friends). Combining these gives 5 levels: Great Friend, Friend, Neutral, Enemy, and Great Enemy. This determines whether a planet will "cooperate" with another during a period or create obstacles. If a planet is sitting in a Great Friend\'s sign, it feels "at home" and delivers excellent results.',
      bodyHi:
        'ज्योतिष में, ग्रह केवल बिंदु नहीं हैं; उनके "सामाजिक संबंध" होते हैं। पंचधा मैत्री दो ग्रहों के बीच अंतिम संबंध की गणना दो चीजों को जोड़कर करती है: १. नैसर्गिक सम्बन्ध: प्रकृति पर आधारित स्थायी मित्रता (जैसे सूर्य और चंद्र मित्र हैं)। २. तात्कालिक सम्बन्ध: यह इस बात पर आधारित है कि वे आपकी कुंडली में कहाँ बैठे हैं। इन दोनों को मिलाने से ५ स्तर मिलते हैं: परम मित्र, मित्र, सम, शत्रु और परम शत्रु। यह निर्धारित करता है कि कोई ग्रह दूसरे के साथ "सहयोग" करेगा या बाधाएं पैदा करेगा। यदि कोई ग्रह परम मित्र की राशि में बैठा है, तो वह "घर जैसा" महसूस करता है और उत्कृष्ट परिणाम देता है।',
    },
    'nadi-analysis': {
      titleEn: 'Nadi Analysis Detailed Theory',
      titleHi: 'नाड़ी विश्लेषण विस्तृत सिद्धांत',
      bodyEn:
        'Nadi Astrology is a highly advanced predictive system. Unlike Parashari, which uses 12 houses primarily, Nadi focuses on the Nakshatras (Constellations) and their Sub-portions. It uses "Coordinates" or combinations of houses to predict events. For example, the combination 2, 7, 11 signifies Marriage. The combination 1, 6, 10 signifies Career success. Nadi is known for its "logic-based" approach where the result of a planet is given by its Nakshatra Lord. It is exceptionally accurate for predicting the *timing* of events and is the preferred method for those who want clear, unambiguous answers about specific life events like job change, marriage, or litigation.',
      bodyHi:
        'नाड़ी ज्योतिष एक अत्यधिक उन्नत भविष्य कहने वाली प्रणाली है। पाराशरी के विपरीत, नाड़ी नक्षत्रों और उनके उप-भागों पर ध्यान केंद्रित करती है। यह घटनाओं की भविष्यवाणी करने के लिए घरों के "निर्देशांक" या संयोजनों का उपयोग करती है। उदाहरण के लिए, २, ७, ११ का संयोजन विवाह का प्रतीक है। १, ६, १० करियर की सफलता का प्रतीक है। नाड़ी अपने "तर्क-आधारित" दृष्टिकोण के लिए जानी जाती है जहाँ ग्रह का परिणाम उसके नक्षत्र स्वामी द्वारा दिया जाता है। यह घटनाओं के *समय* की भविष्यवाणी करने के लिए अत्यधिक सटीक है।',
    },
    'ashtakvarga-phala': {
      titleEn: 'Ashtakvarga Detailed Effects Theory',
      titleHi: 'अष्टकवर्ग फल विस्तृत सिद्धांत',
      bodyEn:
        'Ashtakvarga is a numerical "Strength Scorecard" for each planet. Each sign in the zodiac gets a score between 0 and 8 Bindus (points) for a specific planet. Total sign strength (Sarvashtakvarga) ranges from 0 to 50+. A score of 28 is neutral. Above 28, the sign is strong; below 28, it is weak. When a planet transits a sign where it has high Bindus, it gives wonderful results even if it is naturally a "malefic" planet like Saturn. This system is the best tool to understand why some transits feel lucky and others feel difficult. It provides a objective, mathematical way to filter the complexity of the chart and find your strongest and weakest life zones.',
      bodyHi:
        'अष्टकवर्ग प्रत्येक ग्रह के लिए एक संख्यात्मक "शक्ति स्कोरकार्ड" है। प्रत्येक राशि को एक विशिष्ट ग्रह के लिए ० से ८ बिंदुओं (Bindus) के बीच स्कोर मिलता है। कुल राशि शक्ति (सर्वाष्टकवर्ग) ० से ५०+ तक होती है। २८ का स्कोर तटस्थ है। २८ से ऊपर राशि मजबूत है; २८ से नीचे कमजोर है। जब कोई ग्रह ऐसी राशि में गोचर करता है जहाँ उसके बिंदु अधिक होते हैं, तो वह शनि जैसे स्वाभाविक रूप से "पाप" ग्रह होने पर भी अद्भुत परिणाम देता है। यह प्रणाली यह समझने का सबसे अच्छा उपकरण है कि कुछ गोचर भाग्यशाली और अन्य कठिन क्यों महसूस होते हैं।',
    },
    'kp-horary': {
      titleEn: 'KP Horary (Prashna) Detailed Theory',
      titleHi: 'केपी प्रश्न (होरेरी) विस्तृत सिद्धांत',
      bodyEn:
        'Horary Astrology (Prashna) is used to answer a question when no birth chart is available or for a specific, urgent query. The user provides a number between 1 and 249, which corresponds to a specific Sub-Lord in the zodiac. A chart is then "frozen" for that exact moment based on that number. The logic follows the KP system: we analyze the "Cuspal Sub-Lord" of the house related to the question. For example, for a question about a job, we check the 6th and 10th house sub-lords. If they signify favorable houses, the answer is "Yes." It is a powerful method for immediate guidance on real estate deals, lost items, job offers, or relationship outcomes.',
      bodyHi:
        'प्रश्न ज्योतिष का उपयोग तब किया जाता है जब कोई जन्म कुंडली उपलब्ध न हो या किसी विशिष्ट, तत्काल प्रश्न के लिए। उपयोगकर्ता १ से २४९ के बीच एक संख्या प्रदान करता है, जो राशि चक्र में एक विशिष्ट उप-स्वामी (Sub-Lord) से मेल खाती है। फिर उस संख्या के आधार पर उस सटीक क्षण के लिए एक चार्ट बनाया जाता है। तर्क केपी प्रणाली का पालन करता है। उदाहरण के लिए, नौकरी के बारे में प्रश्न के लिए, हम ६ठे और १०वें घर के उप-स्वामियों की जांच करते हैं। यदि वे अनुकूल घरों का संकेत देते हैं, तो उत्तर "हाँ" है। यह तत्काल मार्गदर्शन के लिए एक शक्तिशाली तरीका है।',
    },
    'kundli-interpretations': {
      titleEn: 'Chart Interpretations (The Life Map) Theory',
      titleHi: 'कुंडली व्याख्या (जीवन मानचित्र) सिद्धांत',
      bodyEn:
        'This section is the "Final Synthesis." While other tabs give you technical data (scores, degrees, names), Interpretations translate that data into human language. It combines the influence of your Ascendant (Personality), Moon (Mind), Sun (Soul), and the currently active Dasha (Timing). It identifies your "Karmic Blocks" and your "Dharmic Gifts." Think of this as the final report from a senior astrologer who has looked at all 100+ factors in your chart and is now telling you the story of your life—what you are here to learn, where you will find success, and how to navigate your challenges.',
      bodyHi:
        'यह खंड "अंतिम संश्लेषण" है। जबकि अन्य टैब आपको तकनीकी डेटा (स्कोर, डिग्री, नाम) देते हैं, व्याख्याएं उस डेटा को सरल भाषा में अनुवाद करती हैं। यह आपके लग्न (व्यक्तित्व), चंद्रमा (मन), सूर्य (आत्मा) और वर्तमान में सक्रिय दशा (समय) के प्रभाव को जोड़ता है। यह आपके "कर्मिक अवरोधों" और "धार्मिक उपहारों" की पहचान करता है। इसे एक वरिष्ठ ज्योतिषी की अंतिम रिपोर्ट के रूप में सोचें, जिसने आपकी कुंडली के सभी १००+ कारकों को देखा है और अब आपको आपके जीवन की कहानी बता रहा है।',
    },
    'aspects-matrix': {
      titleEn: 'Aspects Matrix (The Interaction Grid) Detailed Theory',
      titleHi: 'दृष्टि मैट्रिक्स (परस्पर क्रिया ग्रिड) विस्तृत सिद्धांत',
      bodyEn:
        'The Aspects Matrix is a full grid showing how every planet "talks" to every other planet. In Astrology, planets don\'t act alone; they are influenced by who is looking at them. We use two layers: 1. Vedic Drishti: Standard aspects where Mars looks at 4/7/8 houses away, Saturn at 3/7/10, etc. This is based on "desire" and "control." 2. Western Aspects: Based on precise degrees (Conjunction 0°, Opposition 180°, Trine 120°, Square 90°). A Square creates tension and action, while a Trine creates ease and flow. This matrix allows you to see the "internal dialogue" of your chart—for example, why your Career planet might be hindered by your Anxiety planet through a difficult square aspect.',
      bodyHi:
        'दृष्टि मैट्रिक्स एक पूर्ण ग्रिड है जो दिखाता है कि प्रत्येक ग्रह दूसरे ग्रह से कैसे "बात" करता है। ज्योतिष में, ग्रह अकेले कार्य नहीं करते हैं; वे इस बात से प्रभावित होते हैं कि उन्हें कौन देख रहा है। हम दो परतों का उपयोग करते हैं: १. वैदिक दृष्टि: मानक दृष्टि जहाँ मंगल ४/७/८ घरों को देखता है, शनि ३/७/१० को, आदि। २. पश्चिमी दृष्टि: सटीक डिग्री पर आधारित (युति, केंद्र, त्रिकोण, आदि)। केंद्र (Square) तनाव और क्रिया पैदा करता है, जबकि त्रिकोण (Trine) सहजता और प्रवाह। यह मैट्रिक्स आपको अपनी कुंडली के "आंतरिक संवाद" को देखने की अनुमति देता है।',
    },
  };

  const content = contentMap[tab];
  if (!content) return null;

  return (
    <div className="mt-8 space-y-4 pb-6 px-1">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Lightbulb className="w-5 h-5" />
          {hi ? content.titleHi : content.titleEn}
        </Heading>
        <p className="text-sm text-foreground/80 leading-relaxed">
          {hi ? content.bodyHi : content.bodyEn}
        </p>
      </div>
    </div>
  );
}
