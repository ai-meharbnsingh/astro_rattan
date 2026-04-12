import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { MapPin, Zap, Compass } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

const steps = [
  {
    number: '01',
    icon: MapPin,
    titleEn: 'Enter Your Birth Details',
    titleHi: 'जन्म विवरण दर्ज करें',
    descEn: 'Enter your date, time, and place of birth. Our system geocodes your exact coordinates and feeds them into Swiss Ephemeris — the same engine used by research astronomers.',
    descHi: 'अपनी जन्म तिथि, समय और स्थान दर्ज करें। हमारा सिस्टम आपके सटीक निर्देशांक Swiss Ephemeris में फीड करता है — वही इंजन जो शोध खगोलविद उपयोग करते हैं।',
  },
  {
    number: '02',
    icon: Zap,
    titleEn: 'Instant Kundli Generation',
    titleHi: 'तुरंत कुंडली निर्माण',
    descEn: 'In seconds, get your complete North/South Indian chart, 21 divisional charts (D1–D60), Shadbala strength analysis, Ashtakvarga, Dasha periods, and planetary yogas.',
    descHi: 'सेकंडों में पूरी कुंडली पाएं — North/South Indian चार्ट, 21 विभाजन चार्ट (D1–D60), शडबल विश्लेषण, अष्टकवर्ग, दशा काल और ग्रह योग।',
  },
  {
    number: '03',
    icon: Compass,
    titleEn: 'Explore Deep Insights',
    titleHi: 'गहरी अंतर्दृष्टि खोजें',
    descEn: '22 Lal Kitab tabs, Nishaniyan Matcher, 43-day Chandra Chalana Protocol, AI-powered interpretations, Remedy Tracker with streaks — a complete karmic operating system.',
    descHi: '22 लाल किताब टैब, निशानियां मैचर, 43-दिवसीय चंद्र चालना प्रोटोकॉल, AI-संचालित व्याख्याएं, स्ट्रीक्स के साथ उपाय ट्रैकर — एक पूर्ण कर्मिक ऑपरेटिंग सिस्टम।',
  },
];

export default function HowItWorks() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.hiw-title', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' },
      });
      gsap.fromTo('.hiw-step', { y: 60, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, stagger: 0.18, ease: 'power3.out',
        scrollTrigger: { trigger: '.hiw-grid', start: 'top 78%' },
      });
      gsap.fromTo('.hiw-connector', { scaleX: 0, opacity: 0 }, {
        scaleX: 1, opacity: 1, duration: 0.6, stagger: 0.18, ease: 'power2.out',
        scrollTrigger: { trigger: '.hiw-grid', start: 'top 75%' },
      });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="relative py-24 bg-gradient-to-b from-[#1a1510] to-cosmic-bg overflow-hidden">
      {/* Subtle background glow */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-sacred-gold/8 rounded-full blur-[80px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="hiw-title text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 mb-6">
            <span className="text-sm font-medium text-sacred-gold-dark uppercase tracking-wider">
              {l('How It Works', 'यह कैसे काम करता है')}
            </span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sans text-cosmic-text mb-4">
            {l('From Birth Details to', 'जन्म विवरण से')}{' '}
            <span className="text-sacred-gold-dark">{l('Cosmic Clarity', 'ब्रह्मांडीय स्पष्टता तक')}</span>
          </h2>
          <p className="max-w-2xl mx-auto text-lg text-cosmic-text/70">
            {l(
              'Three steps. Seconds to complete. A lifetime of insights.',
              'तीन चरण। सेकंडों में पूरा। जीवन भर की अंतर्दृष्टि।'
            )}
          </p>
        </div>

        {/* Steps */}
        <div className="hiw-grid grid lg:grid-cols-3 gap-8 lg:gap-6 relative">
          {/* Connecting lines (desktop only) */}
          <div className="hidden lg:block absolute top-[3.5rem] left-[calc(33.33%-1rem)] right-[calc(33.33%-1rem)] h-px z-0">
            <div className="hiw-connector h-full bg-gradient-to-r from-sacred-gold/40 via-sacred-gold/20 to-sacred-gold/40 origin-left" />
          </div>

          {steps.map((step, i) => {
            const Icon = step.icon;
            return (
              <div key={i} className="hiw-step relative z-10">
                {/* Step number + icon */}
                <div className="flex items-start gap-4 mb-6">
                  <div className="relative flex-shrink-0">
                    <div className="w-14 h-14 rounded-full bg-sacred-gold/15 border-2 border-sacred-gold/50 flex items-center justify-center text-sacred-gold-dark">
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-sacred-gold-dark text-white text-[10px] font-bold flex items-center justify-center">
                      {step.number}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-xl font-sans font-semibold text-cosmic-text leading-snug">
                      {l(step.titleEn, step.titleHi)}
                    </h3>
                  </div>
                </div>

                {/* Card body */}
                <div className="pl-0 lg:pl-0 p-5 rounded-xl bg-cosmic-bg/60 border border-sacred-gold/20 hover:border-sacred-gold/40 transition-colors">
                  <p className="text-sm text-cosmic-text/70 leading-relaxed">
                    {l(step.descEn, step.descHi)}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* App Preview — phone mockup */}
        <div className="mt-20 flex flex-col lg:flex-row items-center gap-10 lg:gap-16 p-8 rounded-2xl border border-sacred-gold/20 bg-cosmic-bg/50">
          <div className="relative flex-shrink-0">
            {/* Glow behind phone */}
            <div className="absolute inset-0 bg-sacred-gold/15 rounded-3xl blur-2xl scale-110" />
            <img
              src="/assets/phone-mockup.png"
              alt="Astro Rattan App — AI Astrologer in action"
              className="relative w-[200px] sm:w-[240px] h-auto drop-shadow-2xl"
              loading="lazy"
            />
          </div>
          <div className="text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 mb-4">
              <span className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wider">
                {l('AI Astrologer', 'AI ज्योतिषी')}
              </span>
            </div>
            <h3 className="text-2xl font-sans font-semibold text-cosmic-text mb-3">
              {l('Ask Anything About Your Chart', 'अपनी कुंडली के बारे में कुछ भी पूछें')}
            </h3>
            <p className="text-sm text-cosmic-text/70 leading-relaxed max-w-md">
              {l(
                'Our built-in AI Astrologer reads your exact planetary positions and answers questions in plain language — career timing, relationship compatibility, remedy suggestions, and more.',
                'हमारा अंतर्निहित AI ज्योतिषी आपकी सटीक ग्रह स्थितियां पढ़कर सरल भाषा में उत्तर देता है — करियर टाइमिंग, रिश्ते की अनुकूलता, उपाय सुझाव और बहुत कुछ।'
              )}
            </p>
            <a
              href="/login"
              className="inline-flex items-center gap-2 mt-6 px-7 py-3.5 bg-sacred-gold-dark text-white rounded-lg font-semibold hover:bg-sacred-gold transition-all shadow-lg shadow-sacred-gold/20"
            >
              {l('Try It Free', 'मुफ्त में आज़माएं')}
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
