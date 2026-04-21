import React from 'react';
import { Heading } from '@/components/ui/heading';
import { Info } from 'lucide-react';

interface AdvancedTheorySectionProps {
  language: string;
  tab: string;
}

export default function AdvancedTheorySection({ language, tab }: AdvancedTheorySectionProps) {
  const hi = language === 'hi';

  const contentMap: Record<string, { titleEn: string; titleHi: string; bodyEn: string; bodyHi: string }> = {
    'bhava-vichara': {
      titleEn: 'Bhava Analysis (House Study) Theory',
      titleHi: 'भाव विचार (घरों का अध्ययन) सिद्धांत',
      bodyEn:
        'Bhava Vichara involves a deep analysis of each of the 12 houses. It considers the house lord (Bhavesha), the occupants of the house, and the aspects (Drishti) it receives. Each house represents specific areas of life like career, health, wealth, and relationships.',
      bodyHi:
        'भाव विचार में १२ घरों में से प्रत्येक का गहरा विश्लेषण शामिल है। यह घर के स्वामी (भावेश), घर में स्थित ग्रहों और उस पर पड़ने वाली दृष्टियों पर विचार करता है। प्रत्येक घर जीवन के विशिष्ट क्षेत्रों जैसे करियर, स्वास्थ्य, धन और संबंधों का प्रतिनिधित्व करता है।',
    },
    'longevity': {
      titleEn: 'Longevity Indicators Theory',
      titleHi: 'आयु संकेतक सिद्धांत',
      bodyEn:
        'Ayurdaya (Longevity) calculation uses various classical methods like Amsayu, Pindayu, and Nisargayu to estimate lifespan. It also considers Maraka (killer) planets and the strength of the 8th house and its lord.',
      bodyHi:
        'आयुर्दाय (दीर्घायु) गणना जीवनकाल का अनुमान लगाने के लिए अंशायु, पिण्डायु और निसर्गयु जैसी विभिन्न शास्त्रीय विधियों का उपयोग करती है। यह मारक ग्रहों और ८वें घर और उसके स्वामी की ताकत पर भी विचार करता है।',
    },
    'mundane': {
      titleEn: 'Mundane Astrology Theory',
      titleHi: 'मुंडन ज्योतिष सिद्धांत',
      bodyEn:
        'Mundane astrology deals with nations, world events, weather, and collective karma. It uses charts of nations (Lagna of independence), planetary transits over sensitive points, and solar ingresses (Sankranti) to predict global trends.',
      bodyHi:
        'मुंडन ज्योतिष राष्ट्रों, विश्व घटनाओं, मौसम और सामूहिक कर्म से संबंधित है। यह वैश्विक रुझानों की भविष्यवाणी करने के लिए राष्ट्रों के चार्ट, संवेदनशील बिंदुओं पर ग्रहों के गोचर और सौर संक्रांति का उपयोग करता है।',
    },
    'rectification': {
      titleEn: 'Birth Time Rectification Theory',
      titleHi: 'जन्म समय शोधन सिद्धांत',
      bodyEn:
        'Birth rectification is the process of fine-tuning the birth time when it is uncertain. It uses major life events (marriage, birth of children, career changes) and matches them with the dasha and transits in the rectified chart to ensure accuracy.',
      bodyHi:
        'जन्म समय शोधन अनिश्चित होने पर जन्म के समय को ठीक करने की प्रक्रिया है। यह प्रमुख जीवन घटनाओं (विवाह, बच्चों का जन्म, करियर परिवर्तन) का उपयोग करता है और सटीकता सुनिश्चित करने के लिए उन्हें संशोधित चार्ट में दशा और गोचर के साथ मिलाता है।',
    },
    'upagrahas': {
      titleEn: 'Upagrahas (Sub-planets) Theory',
      titleHi: 'उपग्रह सिद्धांत',
      bodyEn:
        'Upagrahas are mathematical points or non-luminous sub-planets like Gulika, Mandi, and Dhuma. Despite not being physical bodies, they exert significant influence on health, character, and karmic results based on their placement.',
      bodyHi:
        'उपग्रह गणितीय बिंदु या गैर-चमकदार उप-ग्रह हैं जैसे गुलिका, मांदी और धूम। भौतिक पिंड न होने के बावजूद, वे अपनी स्थिति के आधार पर स्वास्थ्य, चरित्र और कर्म परिणामों पर महत्वपूर्ण प्रभाव डालते हैं।',
    },
    'lordships': {
      titleEn: 'House Lordships Theory',
      titleHi: 'भाव स्वामित्व सिद्धांत',
      bodyEn:
        'Lordship refers to which planet rules each of the 12 houses based on the sign rising at birth. The placement of a house lord in another house creates a link between those life areas, showing how different aspects of life influence each other.',
      bodyHi:
        'स्वामित्व यह संदर्भित करता है कि जन्म के समय उदय होने वाली राशि के आधार पर १२ घरों में से प्रत्येक पर कौन सा ग्रह शासन करता है। दूसरे घर में घर के स्वामी की स्थिति उन जीवन क्षेत्रों के बीच एक कड़ी बनाती है, जिससे पता चलता है कि जीवन के विभिन्न पहलू एक-दूसरे को कैसे प्रभावित करते हैं।',
    },
    'details': {
      titleEn: 'Panchanga Details Theory',
      titleHi: 'पंचांग विवरण सिद्धांत',
      bodyEn:
        'The five limbs (Panch-Anga) of time — Tithi, Vara, Nakshatra, Yoga, and Karana — represent the quality of the moment of birth. Each limb governs a specific energy: Tithi (emotions), Vara (vitality), Nakshatra (mind), Yoga (health), and Karana (actions).',
      bodyHi:
        'समय के पांच अंग (पंचांग) — तिथि, वार, नक्षत्र, योग और करण — जन्म के क्षण की गुणवत्ता का प्रतिनिधित्व करते हैं। प्रत्येक अंग एक विशिष्ट ऊर्जा को नियंत्रित करता है: तिथि (भावनाएं), वार (प्राण शक्ति), नक्षत्र (मन), योग (स्वास्थ्य), और करण (कार्य)।',
    },
    'avakhada': {
      titleEn: 'Avakhada Chakra Theory',
      titleHi: 'अवखड़ा चक्र सिद्धांत',
      bodyEn:
        'Avakhada Chakra provides essential birth data for traditional rituals and naming. It includes Varna (caste/inclination), Vashya (amenability), Tara (compatibility), Yoni (nature), Gana (temperament), and Nadi (health/constitution).',
      bodyHi:
        'अवखड़ा चक्र पारंपरिक अनुष्ठानों और नामकरण के लिए आवश्यक जन्म डेटा प्रदान करता है। इसमें वर्ण (झुकाव), वश्य (वश में होना), तारा (संगतता), योनि (प्रकृति), गण (स्वभाव) और नाड़ी (स्वास्थ्य/संविधान) शामिल हैं।',
    },
    'milan': {
      titleEn: 'Kundli Milan (Compatibility) Theory',
      titleHi: 'कुंडली मिलान सिद्धांत',
      bodyEn:
        'Matchmaking analysis evaluates the compatibility between two individuals using the 8-fold Ashtakoota system (36 points) and checking for Mangal Dosha. It aims to ensure emotional, physical, and spiritual harmony in a long-term union.',
      bodyHi:
        'मिलान विश्लेषण अष्टकूट प्रणाली (३६ अंक) का उपयोग करके दो व्यक्तियों के बीच संगतता का मूल्यांकन करता है और मंगल दोष की जांच करता है। इसका उद्देश्य दीर्घकालिक मिलन में भावनात्मक, शारीरिक और आध्यात्मिक सद्भाव सुनिश्चित करना है।',
    },
    'family-demise': {
      titleEn: 'Family Longevity Theory',
      titleHi: 'परिवार आयु विचार सिद्धांत',
      bodyEn:
        'This analysis looks at the indicators for the health and longevity of family members (parents, siblings, spouse) from your own chart. It uses specific houses (e.g., 4th for mother, 9th for father) and their respective karakas.',
      bodyHi:
        'यह विश्लेषण आपके अपने चार्ट से परिवार के सदस्यों (माता-पिता, भाई-बहन, जीवनसाथी) के स्वास्थ्य और दीर्घायु के संकेतकों को देखता है। यह विशिष्ट घरों (जैसे माता के लिए ४था, पिता के लिए ९वां) और उनके संबंधित कारकों का उपयोग करता है।',
    },
    'astro-map': {
      titleEn: 'Astrocartography Theory',
      titleHi: 'ज्योतिष मानचित्र सिद्धांत',
      bodyEn:
        'Astrocartography maps your planetary lines across the globe. It shows how moving to or visiting different locations can activate specific planetary energies in your life, affecting career success, relationships, and well-being.',
      bodyHi:
        'ज्योतिष मानचित्र दुनिया भर में आपके ग्रहीय रेखाओं का मानचित्रण करता है। यह दिखाता है कि विभिन्न स्थानों पर जाने या रहने से आपके जीवन में विशिष्ट ग्रहीय ऊर्जाएं कैसे सक्रिय हो सकती हैं, जो करियर की सफलता, रिश्तों और कल्याण को प्रभावित करती हैं।',
    },
  };

  const content = contentMap[tab];
  if (!content) return null;

  return (
    <div className="mt-8 space-y-4 pb-6 px-1">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Info className="w-5 h-5" />
          {hi ? content.titleHi : content.titleEn}
        </Heading>
        <p className="text-sm text-foreground/80 leading-relaxed">
          {hi ? content.bodyHi : content.bodyEn}
        </p>
      </div>
    </div>
  );
}
