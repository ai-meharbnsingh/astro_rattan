import React from 'react';
import { Heading } from '@/components/ui/heading';
import { LayoutGrid } from 'lucide-react';

interface ChartsTheorySectionProps {
  language: string;
  tab: string;
}

export default function ChartsTheorySection({ language, tab }: ChartsTheorySectionProps) {
  const hi = language === 'hi';

  const contentMap: Record<string, { titleEn: string; titleHi: string; bodyEn: string; bodyHi: string }> = {
    'ashtakvarga-phala': {
      titleEn: 'Ashtakvarga Effects Theory',
      titleHi: 'अष्टकवर्ग फल सिद्धांत',
      bodyEn:
        'Ashtakvarga Phala provides interpretations based on the scores (Bindus) each planet receives in different signs. High scores indicate strength and positive results during transits, while low scores suggest challenges and the need for caution.',
      bodyHi:
        'अष्टकवर्ग फल प्रत्येक ग्रह को विभिन्न राशियों में प्राप्त अंकों (बिंदुओं) के आधार पर व्याख्या प्रदान करता है। उच्च अंक गोचर के दौरान ताकत और सकारात्मक परिणामों का संकेत देते हैं, जबकि कम अंक चुनौतियों और सावधानी की आवश्यकता का सुझाव देते हैं।',
    },
    'animation': {
      titleEn: 'Chart Animation Theory',
      titleHi: 'चार्ट एनिमेशन सिद्धांत',
      bodyEn:
        'Chart animation visualizes the movement of planets over time. It helps in understanding how transits evolve and when specific planetary alignments or aspects will occur, providing a dynamic view of astrological timing.',
      bodyHi:
        'चार्ट एनिमेशन समय के साथ ग्रहों की गति की कल्पना करता है। यह समझने में मदद करता है कि गोचर कैसे विकसित होते हैं और विशिष्ट ग्रहीय विन्यास या पहलू कब होंगे, जो ज्योतिषीय समय का एक गतिशील दृश्य प्रदान करता है।',
    },
    'sarvatobhadra': {
      titleEn: 'Sarvatobhadra Chakra Theory',
      titleHi: 'सर्वतोभद्र चक्र सिद्धांत',
      bodyEn:
        'Sarvatobhadra Chakra is a powerful tool for predicting the effects of transits on an individual. It uses a grid of 81 squares and considers "Vedha" (obstruction) to various sensitive points like birth star, tithi, and name initial.',
      bodyHi:
        'सर्वतोभद्र चक्र व्यक्ति पर गोचर के प्रभावों की भविष्यवाणी करने के लिए एक शक्तिशाली उपकरण है। यह ८१ वर्गों के ग्रिड का उपयोग करता है और जन्म नक्षत्र, तिथि और नाम के अक्षर जैसे विभिन्न संवेदनशील बिंदुओं पर "वेध" (बाधा) पर विचार करता है।',
    },
  };

  const content = contentMap[tab];
  if (!content) return null;

  return (
    <div className="mt-8 space-y-4 pb-6 px-1">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <LayoutGrid className="w-5 h-5" />
          {hi ? content.titleHi : content.titleEn}
        </Heading>
        <p className="text-sm text-foreground/80 leading-relaxed">
          {hi ? content.bodyHi : content.bodyEn}
        </p>
      </div>
    </div>
  );
}
