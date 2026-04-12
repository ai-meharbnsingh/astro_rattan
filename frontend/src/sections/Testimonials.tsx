import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Star, Quote } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

const testimonials = [
  {
    nameEn: 'Pandit Ravi Sharma',
    nameHi: 'पंडित रवि शर्मा',
    roleEn: 'Professional Astrologer · Delhi',
    roleHi: 'पेशेवर ज्योतिषी · दिल्ली',
    avatarInitials: 'RS',
    stars: 5,
    textEn:
      "The Lal Kitab depth here is unmatched. 22 specialization tabs vs 2–3 on every other platform. The Nishaniyan Matcher alone is worth it — my clients are amazed when I map their physical signs to exact planetary positions in seconds.",
    textHi:
      "यहां लाल किताब की गहराई अतुलनीय है। 22 विशेषज्ञता टैब बनाम अन्य प्लेटफॉर्म के 2-3। निशानियां मैचर अकेले इसके लायक है — जब मैं सेकंडों में उनके भौतिक संकेतों को ग्रह स्थितियों से मैप करता हूं तो मेरे ग्राहक चकित हो जाते हैं।",
    highlight: true,
  },
  {
    nameEn: 'Priya Mehta',
    nameHi: 'प्रिया मेहता',
    roleEn: 'Yoga Teacher · Pune',
    roleHi: 'योग शिक्षक · पुणे',
    avatarInitials: 'PM',
    stars: 5,
    textEn:
      "The 43-day Chandra Chalana protocol completely transformed my spiritual practice. The daily task tracking, streak system, and journal entries keep me accountable in ways no other astrology app has ever attempted.",
    textHi:
      "43-दिवसीय चंद्र चालना प्रोटोकॉल ने मेरी आध्यात्मिक साधना को पूरी तरह बदल दिया। दैनिक कार्य ट्रैकिंग, स्ट्रीक सिस्टम और जर्नल एंट्रीज़ ने मुझे जवाबदेह बनाया जैसा किसी अन्य ज्योतिष ऐप ने कभी नहीं किया।",
    highlight: false,
  },
  {
    nameEn: 'Amit Kumar',
    nameHi: 'अमित कुमार',
    roleEn: 'Business Consultant · Mumbai',
    roleHi: 'बिजनेस कंसल्टेंट · मुंबई',
    avatarInitials: 'AK',
    stars: 5,
    textEn:
      "Finally a platform that takes both Hindi and astrology seriously. The bilingual mode isn't just a translated UI — the Sanskrit shlokas, Hindi terminology, and regional accuracy feel completely authentic.",
    textHi:
      "आखिरकार एक ऐसा प्लेटफॉर्म जो हिंदी और ज्योतिष दोनों को गंभीरता से लेता है। द्विभाषी मोड केवल अनुवादित UI नहीं है — संस्कृत श्लोक, हिंदी शब्दावली और क्षेत्रीय सटीकता बिल्कुल प्रामाणिक लगती है।",
    highlight: false,
  },
];

export default function Testimonials() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.testi-title', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' },
      });
      gsap.fromTo('.testi-card', { y: 50, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, stagger: 0.15, ease: 'power3.out',
        scrollTrigger: { trigger: '.testi-grid', start: 'top 78%' },
      });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="relative py-24 bg-gradient-to-b from-cosmic-bg to-[#1a1510] overflow-hidden">
      {/* Background glow */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -bottom-20 left-1/2 -translate-x-1/2 w-[700px] h-[300px] bg-sacred-gold/6 rounded-full blur-[90px]" />
      </div>

      {/* Sage rishi — decorative, fades in from left */}
      <div className="hidden xl:block absolute left-0 bottom-0 z-[3] w-48 opacity-20 pointer-events-none select-none">
        <img src="/assets/sage-rishi-2.png" alt="" aria-hidden="true" className="w-full h-auto object-contain" loading="lazy" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="testi-title text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 mb-6">
            <Star className="w-4 h-4 text-sacred-gold-dark fill-sacred-gold-dark" />
            <span className="text-sm font-medium text-sacred-gold-dark uppercase tracking-wider">
              {l('What Astrologers Say', 'ज्योतिषियों का क्या कहना है')}
            </span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sans text-cosmic-text mb-4">
            {l('Trusted by Professionals', 'पेशेवरों द्वारा')}{' '}
            <span className="text-sacred-gold-dark">{l('& Enthusiasts', 'विश्वसनीय')}</span>
          </h2>
          <p className="max-w-xl mx-auto text-lg text-cosmic-text/70">
            {l(
              'From professional astrologers to first-time users — see why they chose Astro Rattan.',
              'पेशेवर ज्योतिषियों से लेकर पहली बार उपयोगकर्ताओं तक — देखें उन्होंने Astro Rattan क्यों चुना।'
            )}
          </p>
        </div>

        {/* Cards */}
        <div className="testi-grid grid md:grid-cols-3 gap-6">
          {testimonials.map((t, i) => (
            <div
              key={i}
              className={`testi-card relative p-6 rounded-2xl border transition-all duration-300 hover:scale-[1.02] ${
                t.highlight
                  ? 'bg-gradient-to-br from-sacred-gold/15 to-cosmic-bg border-sacred-gold/50'
                  : 'bg-cosmic-bg/70 border-sacred-gold/20 hover:border-sacred-gold/40'
              }`}
            >
              {/* Quote icon */}
              <Quote className="w-8 h-8 text-sacred-gold/25 mb-4" />

              {/* Stars */}
              <div className="flex gap-1 mb-4">
                {Array.from({ length: t.stars }).map((_, s) => (
                  <Star key={s} className="w-4 h-4 text-sacred-gold-dark fill-sacred-gold-dark" />
                ))}
              </div>

              {/* Text */}
              <p className="text-sm text-cosmic-text/80 leading-relaxed mb-6 italic">
                "{l(t.textEn, t.textHi)}"
              </p>

              {/* Author */}
              <div className="flex items-center gap-3 mt-auto">
                <div className="w-10 h-10 rounded-full bg-sacred-gold/20 border border-sacred-gold/40 flex items-center justify-center text-sacred-gold-dark text-sm font-bold flex-shrink-0">
                  {t.avatarInitials}
                </div>
                <div>
                  <p className="text-sm font-semibold text-cosmic-text">{l(t.nameEn, t.nameHi)}</p>
                  <p className="text-xs text-cosmic-text/50">{l(t.roleEn, t.roleHi)}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
