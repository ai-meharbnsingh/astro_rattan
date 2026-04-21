import React from 'react';
import { Heading } from '@/components/ui/heading';
import { Clock } from 'lucide-react';
import SlokaHover from './SlokaHover';

interface TimingTheorySectionProps {
  language: string;
  tab: string; // identifier of the timing sub-tab
}

export default function TimingTheorySection({ language, tab }: TimingTheorySectionProps) {
  const hi = language === 'hi';

  const contentMap: Record<string, { titleEn: string; titleHi: string; bodyEn: React.ReactNode; bodyHi: React.ReactNode }> = {
    sadesati: {
      titleEn: "Sade Sati (Saturn's 7.5 Year Cycle) Detailed Theory",
      titleHi: 'साढ़े साती (शनि का ७.५ वर्ष का चक्र) विस्तृत सिद्धांत',
      bodyEn: (
        <div className="space-y-3">
          <p>
            Sade Sati is one of the most significant timing cycles in Vedic Astrology. It begins when Saturn (Shani) enters the sign immediately preceding your natal Moon sign, continues while it transits your Moon sign, and concludes when it leaves the sign following your Moon sign.
            Since Saturn stays in each sign for about 2.5 years, the total period lasts approximately 7.5 years.
          </p>
          <p>
            According to <SlokaHover slokaRef="Phaladeepika Adh. 13" language={language}>Phaladeepika Adh. 13</SlokaHover>, this period is often marked by intense introspection and karmic adjustment.
            Key Phases: 1. The First Phase (Rising) often brings financial changes or family responsibilities. 2. The Second Phase (Peak) is when Saturn is directly over your Moon, often bringing emotional pressure and deep transformation. 3. The Third Phase (Setting) marks the resolution of lessons and gradual relief.
          </p>
          <p>
            Sade Sati is not just a period of "hardship"; it is a "Karmic Audit" designed to instill discipline, humility, and long-term stability by removing what is no longer serving your soul.
          </p>
        </div>
      ),
      bodyHi: (
        <div className="space-y-3">
          <p>
            साढ़े साती वैदिक ज्योतिष में सबसे महत्वपूर्ण समय चक्रों में से एक है। यह तब शुरू होता है जब शनि आपके जन्म के चंद्र राशि से ठीक पहले वाली राशि में प्रवेश करता है, चंद्र राशि में रहने के दौरान जारी रहता है, और चंद्र राशि के बाद वाली राशि को छोड़ने पर समाप्त होता है।
            चूंकि शनि प्रत्येक राशि में लगभग २.५ वर्ष तक रहता है, इसलिए कुल अवधि लगभग ७.५ वर्ष तक चलती है।
          </p>
          <p>
            <SlokaHover slokaRef="Phaladeepika Adh. 13" language={language}>फलदीपिका अध्याय 13</SlokaHover> के अनुसार, यह काल अक्सर गहन आत्मनिरीक्षण और कर्मों के मेल-मिलाप का समय होता है।
            मुख्य चरण: १. प्रथम चरण (उदय) अक्सर वित्तीय परिवर्तन या पारिवारिक जिम्मेदारियां लाता है। २. द्वितीय चरण (शिखर) तब होता है जब शनि सीधे आपके चंद्रमा पर होता है। ३. तृतीय चरण (अस्त) सीखे गए पाठों के समाधान और धीरे-धीरे राहत का प्रतीक है।
          </p>
          <p>
            साढ़े साती केवल "कठिनाई" की अवधि नहीं है; यह एक "कर्मिक ऑडिट" है जिसे अनुशासन, विनम्रता और दीर्घकालिक स्थिरता पैदा करने के लिए डिज़ाइन किया गया है।
          </p>
        </div>
      ),
    },
    transits: {
      titleEn: 'Planetary Transits (Gochara) Detailed Theory',
      titleHi: 'ग्रहीय गोचर (गोचर) विस्तृत सिद्धांत',
      bodyEn: (
        <div className="space-y-3">
          <p>
            Transits refer to the current, moving positions of planets in the sky and how they interact with your static birth chart. Think of your birth chart as a "seed" and transits as the "weather" that helps that seed grow.
          </p>
          <p>
            <SlokaHover slokaRef="Phaladeepika Adh. 26" language={language}>Phaladeepika Adhyaya 26 (Gocharadhyaya)</SlokaHover> provides the foundation for evaluating these daily triggers.
            Traditional Vedic Astrology prioritizes transits relative to the natal Moon sign. For example, Jupiter transiting the 2nd, 5th, 7th, 9th, or 11th from the Moon is considered highly auspicious.
          </p>
          <p>
            Slow planets like Saturn (2.5 years), Jupiter (1 year), and Rahu/Ketu (1.5 years) define the major themes of your year. Fast planets like Sun, Mars, and Mercury define the monthly mood.
          </p>
        </div>
      ),
      bodyHi: (
        <div className="space-y-3">
          <p>
            गोचर का तात्पर्य आकाश में ग्रहों की वर्तमान, चलती स्थिति और वे आपकी स्थिर जन्म कुंडली के साथ कैसे परस्पर क्रिया करते हैं, इससे है। अपनी जन्म कुंडली को एक "बीज" के रूप में सोचें और गोचर को "मौसम" के रूप में जो उस बीज को बढ़ने में मदद करता है।
          </p>
          <p>
            <SlokaHover slokaRef="Phaladeepika Adh. 26" language={language}>फलदीपिका अध्याय 26 (गोचाराध्याय)</SlokaHover> इन दैनिक ट्रिगर्स के मूल्यांकन का आधार प्रदान करता है।
            पारंपरिक वैदिक ज्योतिष जन्म कुंडली के चंद्र राशि के सापेक्ष गोचर को प्राथमिकता देता है। उदाहरण के लिए, चंद्रमा से २, ५, ७, ९ या ११वें घर में बृहस्पति का गोचर अत्यधिक शुभ माना जाता है।
          </p>
          <p>
            धीमे ग्रह जैसे शनि, बृहस्पति और राहु/केतु आपके वर्ष के मुख्य विषयों को निर्धारित करते हैं। सूर्य, मंगल और बुध जैसे तेज ग्रह मासिक मूड को निर्धारित करते हैं।
          </p>
        </div>
      ),
    },
    varshphal: {
      titleEn: 'Varshphal (Annual Solar Return) Detailed Theory',
      titleHi: 'वर्षफल (वार्षिक सौर वापसी) विस्तृत सिद्धांत',
      bodyEn: (
        <div className="space-y-3">
          <p>
            Varshphal is a unique predictive system used to forecast the events of a single year. It is based on the moment the Sun returns to the exact longitude it held at your birth.
          </p>
          <p>
            Unique Features: 1. Muntha: A sensitive mathematical point that moves one sign per year. 2. Year Lord: One planet is selected as the "King" of your year. 3. Mudda Dasha: A fast-moving dasha system that covers the 365 days of the year.
          </p>
        </div>
      ),
      bodyHi: (
        <div className="space-y-3">
          <p>
            वर्षफल एक अनूठी भविष्य कहने वाली प्रणाली है जिसका उपयोग एक वर्ष की घटनाओं का पूर्वानुमान लगाने के लिए किया जाता है। यह उस क्षण पर आधारित है जब सूर्य उसी सटीक डिग्री पर लौटता है जो आपके जन्म के समय थी।
          </p>
          <p>
            अनूठी विशेषताएं: १. मुन्था: एक संवेदनशील बिंदु जो प्रति वर्ष एक राशि आगे बढ़ता है। २. वर्षेश: वर्ष का स्वामी। ३. मुद्दा दशा: जो वर्ष के ३६५ दिनों को विस्तार से कवर करती है।
          </p>
        </div>
      ),
    },
    yogini: {
      titleEn: 'Yogini Dasha (36-Year Cycle) Detailed Theory',
      titleHi: 'योगिनी दशा (३६-वर्षीय चक्र) विस्तृत सिद्धांत',
      bodyEn: (
        <div className="space-y-3">
          <p>
            Yogini Dasha is an alternative timing system, a 36-year cycle governed by 8 Yoginis. It is highly praised for precision in short-term events.
          </p>
          <p>
            The 8 Yoginis: 1. Mangala, 2. Pingala, 3. Dhanya, 4. Bhramari, 5. Bhadrika, 6. Ulka, 7. Siddha, and 8. Sankata. Each Yogini has a specific nature and ruling planet.
          </p>
        </div>
      ),
      bodyHi: (
        <div className="space-y-3">
          <p>
            योगिनी दशा एक वैकल्पिक समय प्रणाली है, जो ८ योगिनियों द्वारा शासित ३६ वर्ष का चक्र है। यह अल्पकालिक घटनाओं की भविष्यवाणी करने में अपनी सटीकता के लिए जानी जाती है।
          </p>
          <p>
            ८ योगिनियाँ: १. मंगला, २. पिंगला, ३. धान्या, ४. भ्रामरी, ५. भद्रिका, ६. उल्का, ७. सिद्धा, और ८. संकटा। प्रत्येक योगिनी का एक विशिष्ट स्वभाव होता है।
          </p>
        </div>
      ),
    },
    'gochara-vedha': {
      titleEn: 'Gochara Vedha (Transit Obstruction) Detailed Theory',
      titleHi: 'गोचर वेध (गोचर बाधा) विस्तृत सिद्धांत',
      bodyEn: (
        <div className="space-y-3">
          <p>
            Vedha literally means "obstruction." In transit astrology, even if a planet is transiting a highly favorable house, its good effects can be "cancelled" or blocked if another planet is sitting in its Vedha position.
          </p>
          <p>
            <SlokaHover slokaRef="Phaladeepika Adh. 26" language={language}>Phaladeepika</SlokaHover> explains that every planet has a specific Vedha point for each favorable transit house. For example, if Jupiter is in the 11th house, but any planet (except Saturn) is in the 8th house, it creates Vedha.
          </p>
        </div>
      ),
      bodyHi: (
        <div className="space-y-3">
          <p>
            वेध का शाब्दिक अर्थ है "बाधा"। गोचर ज्योतिष में, भले ही कोई ग्रह अत्यधिक अनुकूल घर में गोचर कर रहा हो, लेकिन यदि कोई अन्य ग्रह उसकी वेध स्थिति में बैठा हो, तो उसके अच्छे प्रभाव अवरुद्ध हो सकते हैं।
          </p>
          <p>
            <SlokaHover slokaRef="Phaladeepika Adh. 26" language={language}>फलदीपिका</SlokaHover> के अनुसार प्रत्येक अनुकूल गोचर घर के लिए प्रत्येक ग्रह का एक विशिष्ट वेध बिंदु होता है। उदाहरण के लिए, यदि बृहस्पति ११वें घर में है, लेकिन कोई अन्य ग्रह ८वें घर में है, तो यह वेध बनाता है।
          </p>
        </div>
      ),
    },
    'transit-interp': {
      titleEn: 'Transit Interpretations Detailed Theory',
      titleHi: 'गोचर व्याख्या विस्तृत सिद्धांत',
      bodyEn: (
        <div className="space-y-3">
          <p>
            Transit Interpretations provide a detailed narrative of how current planetary energies are interacting with your life.
            As noted in <SlokaHover slokaRef="Phaladeepika Adh. 26" language={language}>Phaladeepika's Gocharadhyaya</SlokaHover>, each planet carries themes like Status, Mind, Energy, Wisdom, etc.
          </p>
          <p>
            By analyzing the sign and house a planet is currently visiting, we interpret how its core nature will manifest in areas like career, finance, and health.
          </p>
        </div>
      ),
      bodyHi: (
        <div className="space-y-3">
          <p>
            गोचर व्याख्याएं इस बात का विस्तृत वर्णन प्रदान करती हैं कि वर्तमान ग्रहीय ऊर्जाएं आपके जीवन के साथ कैसे परस्पर क्रिया कर रही हैं।
            <SlokaHover slokaRef="Phaladeepika Adh. 26" language={language}>फलदीपिका के गोचाराध्याय</SlokaHover> के अनुसार, प्रत्येक ग्रह सम्मान, मन, ऊर्जा, ज्ञान आदि के विषय लेकर चलता है।
          </p>
          <p>
            ग्रह वर्तमान में किस राशि और घर में है, इसके विश्लेषण से हम करियर, वित्त और स्वास्थ्य जैसे क्षेत्रों में उसके फल की व्याख्या करते हैं।
          </p>
        </div>
      ),
    },
    'dasha-phala': {
      titleEn: 'Dasha Phala (Timing Effects) Detailed Theory',
      titleHi: 'दशा फल (समय प्रभाव) विस्तृत सिद्धांत',
      bodyEn: (
        <div className="space-y-3">
          <p>
            Dasha Phala is the art of predicting results of a planetary period based on its "Portfolio" (house lordship and placement).
            The synthesis of Mahadasha and Antardasha is crucial.
          </p>
          <p>
            <SlokaHover slokaRef="Phaladeepika Adh. 20" language={language}>Phaladeepika Adh. 20</SlokaHover> and <SlokaHover slokaRef="Phaladeepika Adh. 21" language={language}>Adh. 21</SlokaHover> provide the classical results for Mahadashas and sub-periods respectively.
          </p>
        </div>
      ),
      bodyHi: (
        <div className="space-y-3">
          <p>
            दशा फल एक ग्रहीय अवधि के परिणामों की भविष्यवाणी करने की कला है। महादशा और अंतर्दशा का संश्लेषण अत्यंत महत्वपूर्ण है।
          </p>
          <p>
            <SlokaHover slokaRef="Phaladeepika Adh. 20" language={language}>फलदीपिका अध्याय 20</SlokaHover> और <SlokaHover slokaRef="Phaladeepika Adh. 21" language={language}>अध्याय 21</SlokaHover> क्रमशः महादशा और अंतर्दशा के शास्त्रीय फल प्रदान करते हैं।
          </p>
        </div>
      ),
    },
  };

  const content = contentMap[tab];
  if (!content) return null;

  return (
    <div className="mt-8 space-y-4 pb-6 px-1">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Clock className="w-5 h-5" />
          {hi ? content.titleHi : content.titleEn}
        </Heading>
        <div className="text-sm text-foreground/80 leading-relaxed">
          {hi ? content.bodyHi : content.bodyEn}
        </div>
      </div>
    </div>
  );
}
