import React from 'react';
import { Heading } from '@/components/ui/heading';

interface TimingTheorySectionProps {
  language: string;
  tab: string; // identifier of the timing sub-tab, e.g., 'sadesati', 'transits', etc.
}

export default function TimingTheorySection({ language, tab }: TimingTheorySectionProps) {
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);

  const contentMap: Record<string, { titleEn: string; titleHi: string; bodyEn: string; bodyHi: string }> = {
    sadesati: {
      titleEn: 'Sade Sati Theory',
      titleHi: 'साढ़े साती सिद्धांत',
      bodyEn:
        'Sade Sati is the 7½‑year period when Saturn transits the natal Moon sign, the preceding sign, and the following sign. It is a time of karmic lessons, discipline, and potential challenges, but also of deep personal growth.',
      bodyHi:
        'साढ़े साती वह ७.५‑साल की अवधि है जब शनि जन्म चंद्र राशि, उससे पहले की राशि और उसके बाद की राशि से गुजरता है। यह कर्मिक सीख, अनुशासन और संभावित चुनौतियों का समय है, लेकिन साथ ही गहरी व्यक्तिगत विकास का भी अवसर।',
    },
    transits: {
      titleEn: 'Transit Theory',
      titleHi: 'गोचर सिद्धांत',
      bodyEn:
        'Transits show the current positions of planets in the sky relative to your natal chart. They indicate timing for events, opportunities, and challenges based on the aspects formed with natal planets.',
      bodyHi:
        'गोचर वर्तमान में ग्रहों की स्थिति को आपके जन्म कुंडली के सापेक्ष दर्शाते हैं। वे पहलुओं के आधार पर घटनाओं, अवसरों और चुनौतियों के समय को संकेत देते हैं।',
    },
    yogini: {
      titleEn: 'Yogini Dasha Theory',
      titleHi: 'योगिनी दशा सिद्धांत',
      bodyEn:
        'Yogini Dasha is a 36‑year cycle of 8 goddesses, each ruling a 4‑year sub‑period. It reflects subtle karmic patterns and spiritual lessons.',
      bodyHi:
        'योगिनी दशा ८ देवियों का ३६‑साल का चक्र है, प्रत्येक ४‑साल के उप‑अवधि को शासित करती है। यह सूक्ष्म कर्मिक पैटर्न और आध्यात्मिक सीख को दर्शाता है।',
    },
    varshphal: {
      titleEn: 'Varshphal Theory',
      titleHi: 'वर्षफल सिद्धांत',
      bodyEn:
        'Varshphal (Solar Return) is the chart for the exact moment the Sun returns to its natal longitude each year, indicating themes for that year.',
      bodyHi:
        'वर्षफल (सौर वापसी) वह चार्ट है जब सूर्य प्रत्येक वर्ष अपने जन्मांश पर वापस आता है, जो उस वर्ष के विषयों को दर्शाता है।',
    },
    kalachakra: {
      titleEn: 'Kalachakra Dasha Theory',
      titleHi: 'कालचक्र दशा सिद्धांत',
      bodyEn:
        'Kalachakra Dasha groups the 27 nakshatras into 9 sets, each governing a 12‑year period, providing a different timing framework from Vimshottari.',
      bodyHi:
        'कालचक्र दशा २७ नक्षत्रों को ९ समूहों में बाँटती है, प्रत्येक १२‑साल की अवधि को शासित करता है, जो विंशोत्तरी से अलग समय फ्रेमवर्क प्रदान करता है।',
    },
    'gochara-vedha': {
      titleEn: 'Gochara Vedha Theory',
      titleHi: 'गोचर वेध सिद्धांत',
      bodyEn:
        'Gochara Vedha points are specific planetary positions that neutralise the benefic effects of a transit, acting as a protective filter.',
      bodyHi:
        'गोचर वेध बिंदु विशिष्ट ग्रह स्थितियां हैं जो एक गोचर के शुभ प्रभाव को निरस्त करती हैं, एक सुरक्षा फ़िल्टर के रूप में कार्य करती हैं।',
    },
    'transit-interp': {
      titleEn: 'Transit Interpretations Theory',
      titleHi: 'गोचर व्याख्या सिद्धांत',
      bodyEn:
        'Interpretations provide detailed explanations for each active transit planet, linking its aspect to life areas and potential outcomes.',
      bodyHi:
        'व्याख्याएं प्रत्येक सक्रिय गोचर ग्रह के लिए विस्तृत विवरण देती हैं, उसके पहलू को जीवन क्षेत्रों और संभावित परिणामों से जोड़ती हैं।',
    },
    'transit-lucky': {
      titleEn: 'Lucky Indicators Theory',
      titleHi: 'शुभ संकेतक सिद्धांत',
      bodyEn:
        'Lucky indicators highlight auspicious timing windows derived from favorable transit configurations, helping to plan important actions.',
      bodyHi:
        'शुभ संकेतक अनुकूल गोचर विन्यासों से प्राप्त शुभ समय विंडो को उजागर करते हैं, जिससे महत्वपूर्ण कार्यों की योजना बनाना आसान होता है।',
    },
  };

  const content = contentMap[tab];
  if (!content) return null;

  return (
    <div className="mt-8 space-y-4 pb-6">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          {content.titleEn}
        </Heading>
        <p className="text-sm text-foreground/80 leading-relaxed">{hi ? content.bodyHi : content.bodyEn}</p>
      </div>
    </div>
  );
}
