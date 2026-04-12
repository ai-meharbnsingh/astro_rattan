import { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ChevronDown, HelpCircle } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

const faqs = [
  {
    qEn: 'Is Astro Rattan free to use?',
    qHi: 'क्या Astro Rattan उपयोग करना मुफ्त है?',
    aEn: 'Yes. Create an account and generate your complete Kundli chart for free. Core features including Lal Kitab analysis, Panchang, and Nishaniyan Matcher are all included at no charge.',
    aHi: 'हां। खाता बनाएं और अपनी पूरी कुंडली मुफ्त में बनाएं। लाल किताब विश्लेषण, पंचांग और निशानियां मैचर सहित मुख्य सुविधाएं बिना शुल्क के शामिल हैं।',
  },
  {
    qEn: 'What makes the Lal Kitab system here unique?',
    qHi: 'यहां की लाल किताब प्रणाली क्या अद्वितीय बनाती है?',
    aEn: 'Most apps offer 2–3 basic Lal Kitab tabs. We built 22 specialized tabs covering Nishaniyan (physical sign matching), Teva classification, Chandra Chalana 43-day protocol, D60 past-life karma, advanced remedies with a streak-based tracker, and full AI interpretation. Nothing like this exists elsewhere.',
    aHi: 'अधिकांश ऐप 2-3 बुनियादी लाल किताब टैब देते हैं। हमने 22 विशेष टैब बनाए हैं जिनमें निशानियां (भौतिक संकेत मिलान), तेवा वर्गीकरण, चंद्र चालना 43-दिन प्रोटोकॉल, D60 पिछले जन्म का कर्म, स्ट्रीक-आधारित ट्रैकर के साथ उन्नत उपाय और पूर्ण AI व्याख्या शामिल हैं।',
  },
  {
    qEn: 'How accurate are the planetary calculations?',
    qHi: 'ग्रह गणना कितनी सटीक है?',
    aEn: 'Extremely accurate. We use Swiss Ephemeris — the same astronomical library used by professional research observatories — accurate to arc-seconds. Unlike apps that use lookup tables or simplified algorithms, every position is computed from first principles for your exact birth coordinates and time.',
    aHi: 'अत्यंत सटीक। हम Swiss Ephemeris का उपयोग करते हैं — वही खगोलीय लाइब्रेरी जो पेशेवर शोध वेधशालाएं उपयोग करती हैं — आर्क-सेकंड तक सटीक। लुकअप टेबल या सरलीकृत एल्गोरिदम का उपयोग करने वाले ऐप के विपरीत, हर स्थिति आपके सटीक जन्म निर्देशांक और समय से गणना की जाती है।',
  },
  {
    qEn: 'Can I use the platform in Hindi?',
    qHi: 'क्या मैं प्लेटफॉर्म को हिंदी में उपयोग कर सकता हूं?',
    aEn: 'Yes, fully. The bilingual mode is not machine-translated — it uses authentic Hindi astrological terminology, proper Sanskrit shlokas, and regionally accurate phrasing. Switch between Hindi and English at any time with a single click.',
    aHi: 'हां, पूरी तरह। द्विभाषी मोड मशीन-अनुवादित नहीं है — यह प्रामाणिक हिंदी ज्योतिषीय शब्दावली, उचित संस्कृत श्लोक और क्षेत्रीय रूप से सटीक वाक्यांश का उपयोग करता है। एक क्लिक से किसी भी समय हिंदी और अंग्रेजी के बीच स्विच करें।',
  },
  {
    qEn: 'What is the Chandra Chalana Protocol?',
    qHi: 'चंद्र चालना प्रोटोकॉल क्या है?',
    aEn: 'A 43-day Moon discipline practice rooted in Lal Kitab tradition. Each day has specific tasks aligned to the Moon\'s transit. Astro Rattan is the only platform with a complete tracker: daily check-ins, a personal journal, streak counters, and progress that syncs across all your devices.',
    aHi: 'लाल किताब परंपरा में निहित 43-दिवसीय चंद्र अनुशासन साधना। प्रत्येक दिन में चंद्रमा के गोचर के अनुरूप विशिष्ट कार्य होते हैं। Astro Rattan एकमात्र प्लेटफॉर्म है जिसमें पूरा ट्रैकर है: दैनिक चेक-इन, व्यक्तिगत जर्नल, स्ट्रीक काउंटर और आपके सभी उपकरणों पर सिंक होने वाली प्रगति।',
  },
];

export default function FAQ() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.faq-title', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: sectionRef.current, start: 'top 82%' },
      });
      gsap.fromTo('.faq-item', { y: 30, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: 'power2.out',
        scrollTrigger: { trigger: '.faq-list', start: 'top 80%' },
      });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="relative py-24 bg-gradient-to-b from-[#1a1510] to-cosmic-bg overflow-hidden">
      <div className="relative z-10 max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="faq-title text-center mb-14">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 mb-6">
            <HelpCircle className="w-4 h-4 text-sacred-gold-dark" />
            <span className="text-sm font-medium text-sacred-gold-dark uppercase tracking-wider">
              {l('Frequently Asked', 'अक्सर पूछे जाने वाले प्रश्न')}
            </span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-sans text-cosmic-text mb-4">
            {l('Got Questions?', 'प्रश्न हैं?')}{' '}
            <span className="text-sacred-gold-dark">{l("We've Got Answers", 'हमारे पास उत्तर हैं')}</span>
          </h2>
        </div>

        {/* Accordion */}
        <div className="faq-list space-y-3">
          {faqs.map((faq, i) => {
            const isOpen = openIndex === i;
            return (
              <div
                key={i}
                className={`faq-item rounded-xl border transition-all duration-300 overflow-hidden ${
                  isOpen
                    ? 'border-sacred-gold/50 bg-sacred-gold/8'
                    : 'border-sacred-gold/20 bg-cosmic-bg/60 hover:border-sacred-gold/35'
                }`}
              >
                <button
                  className="w-full text-left px-6 py-5 flex items-center justify-between gap-4"
                  onClick={() => setOpenIndex(isOpen ? null : i)}
                  aria-expanded={isOpen}
                >
                  <span className={`font-sans font-semibold text-base leading-snug transition-colors ${isOpen ? 'text-sacred-gold-dark' : 'text-cosmic-text'}`}>
                    {l(faq.qEn, faq.qHi)}
                  </span>
                  <ChevronDown
                    className={`w-5 h-5 flex-shrink-0 text-sacred-gold-dark transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}
                  />
                </button>
                <div
                  className={`overflow-hidden transition-all duration-300 ease-in-out ${isOpen ? 'max-h-[400px] opacity-100' : 'max-h-0 opacity-0'}`}
                >
                  <p className="px-6 pb-5 text-sm text-cosmic-text/75 leading-relaxed">
                    {l(faq.aEn, faq.aHi)}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-12">
          <p className="text-cosmic-text/60 text-sm mb-4">
            {l('Still have questions? We\'re here to help.', 'अभी भी प्रश्न हैं? हम मदद के लिए यहां हैं।')}
          </p>
          <a
            href="mailto:info@astrorattan.com"
            className="inline-flex items-center gap-2 px-6 py-3 border border-sacred-gold/40 text-sacred-gold-dark rounded-lg text-sm font-medium hover:bg-sacred-gold/10 transition-colors"
          >
            {l('Contact Us', 'संपर्क करें')}
          </a>
        </div>
      </div>
    </section>
  );
}
