import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { useTranslation } from '@/lib/i18n';
import { Sparkles, ArrowRight } from 'lucide-react';
import ZodiacWheel from '@/components/ZodiacWheel';

export default function Hero() {
  const heroRef = useRef<HTMLDivElement>(null);
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.hero-shloka',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 1, delay: 0.3, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-badge',
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.8, delay: 0.4, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-title-main',
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 1.2, delay: 0.5, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-subtitle',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 1, delay: 0.7, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-cta',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.8, delay: 0.9, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-wheel',
        { opacity: 0, scale: 0.85 },
        { opacity: 1, scale: 1, duration: 1.4, delay: 0.6, ease: 'power3.out' }
      );
    }, heroRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={heroRef} className="relative min-h-[60vh] flex items-center overflow-hidden pt-24 pb-8">
      {/* Background — noise texture */}
      <div className="absolute inset-0 z-[1] opacity-[0.03] pointer-events-none"
        style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")` }}
      />
      {/* Depth radial gradient behind text side */}
      <div className="absolute inset-0 z-[2] pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at 30% 50%, rgba(196,97,31,0.06) 0%, rgba(245,240,232,0) 60%)' }}
      />

      {/* Floating orbs */}
      <div className="absolute top-1/4 left-10 w-64 h-64 bg-sacred-gold/5 rounded-full blur-3xl opacity-20" />
      <div className="absolute bottom-1/4 right-10 w-80 h-80 bg-[#8B4513]/10 rounded-full blur-3xl opacity-20" />

      {/* Two-column layout */}
      <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col lg:flex-row items-center gap-8 lg:gap-12">

          {/* LEFT — Text content */}
          <div className="flex-1 text-center lg:text-left">
            {/* Badge */}
            <div className="hero-badge opacity-0 mb-6">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 border border-sacred-gold/30">
                <Sparkles className="w-4 h-4 text-sacred-gold-dark" />
                <span className="text-sm font-medium text-sacred-gold-dark">
                  {l('Vedic Astrology + Lal Kitab + Vastu', 'वैदिक ज्योतिष + लाल किताब + वास्तु')}
                </span>
              </div>
            </div>

            {/* Shloka */}
            <div className="hero-shloka opacity-0 mb-4">
              <p className="font-sans text-xs opacity-70 tracking-[4px] text-gray-600 uppercase"
                style={{ textShadow: '0 0 15px rgba(255, 170, 51, 0.4)' }}>
                {'\u091C\u094D\u092F\u094B\u0924\u093F\u0937\u092E\u094D \u0905\u092F\u092E\u094D \u092C\u094D\u0930\u0939\u094D\u092E'} {t('hero.shlokaSupreme')}
              </p>
            </div>

            {/* Main Title — 3D extruded text */}
            <div className="hero-title-main opacity-0">
              <h1
                className="text-4xl sm:text-5xl lg:text-6xl text-[#1a1a2e] leading-[1.0]"
                style={{
                  fontWeight: 800,
                  letterSpacing: '-0.02em',
                  textShadow: '1px 1px 0px #8B4513, 2px 2px 0px #7A3B10, 3px 3px 0px #6B330E, 4px 4px 0px #5C2C0C, 5px 5px 0px #4D240A, 6px 6px 12px rgba(0,0,0,0.3)',
                }}
              >
                {l('Your Complete Vedic Astrology Platform', 'आपका पूर्ण वैदिक ज्योतिष प्लेटफॉर्म')}
              </h1>
              <p
                className="text-base text-[#C4611F] mt-4 uppercase"
                style={{
                  fontWeight: 700,
                  letterSpacing: '0.15em',
                  textShadow: '1px 1px 3px rgba(196, 97, 31, 0.4)',
                }}
              >
                {l('Kundli · Lal Kitab · Vastu · Panchang · Numerology', 'कुंडली · लाल किताब · वास्तु · पंचांग · अंकशास्त्र')}
              </p>
            </div>

            {/* Subtitle */}
            <div className="hero-subtitle opacity-0 mt-6 max-w-xl lg:max-w-none">
              <p className="text-lg text-gray-600 leading-relaxed">
                {l(
                  'Deep Kundli analysis, Lal Kitab remedies & predictions, Vastu floor plan scoring, live Panchang, and Numerology & Tarot — all in one platform powered by AI and authentic Vedic traditions.',
                  'गहरी कुंडली विश्लेषण, लाल किताब उपाय और भविष्यवाणियां, वास्तु फ्लोर प्लान स्कोरिंग, लाइव पंचांग और अंकशास्त्र — AI और प्रामाणिक वैदिक परंपराओं द्वारा संचालित एक ही प्लेटफॉर्म।'
                )}
              </p>
            </div>

            {/* CTA Buttons */}
            <div className="hero-cta opacity-0 mt-8 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <a
                href="/kundli"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-sacred-gold-dark text-white rounded-lg font-semibold hover:bg-sacred-gold transition-all shadow-lg shadow-sacred-gold/20 group"
              >
                {l('Generate Your Kundli Free', 'अपनी कुंडली मुफ्त बनाएं')}
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </a>
              <a
                href="#features"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 border-2 border-sacred-gold/50 text-sacred-gold-dark rounded-lg font-semibold hover:bg-sacred-gold/10 transition-all"
              >
                {l('See How It Works', 'कैसे काम करता है देखें')}
              </a>
            </div>

            {/* Trust indicators */}
            <div className="hero-cta opacity-0 mt-8 flex flex-wrap justify-center lg:justify-start gap-6 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-600"></span>
                {l('10,000+ Kundlis Generated', '10,000+ कुंडलियां बनाई गईं')}
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-600"></span>
                {l('Trusted by Astrologers', 'ज्योतिषियों द्वारा विश्वसनीय')}
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-600"></span>
                {l('5 Modules in One', 'एक में 5 मॉड्यूल')}
              </div>
            </div>
          </div>

          {/* RIGHT — Zodiac Wheel with 3D depth */}
          <div className="hero-wheel opacity-0 flex-shrink-0 w-full max-w-[320px] lg:max-w-[400px]">
            <ZodiacWheel />
          </div>

        </div>
      </div>
    </section>
  );
}
