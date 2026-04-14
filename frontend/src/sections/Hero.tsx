import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { useTranslation } from '@/lib/i18n';
import { ArrowRight, Users, Grid3X3 } from 'lucide-react';
import LiveTransitWheel from '@/components/LiveTransitWheel';

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
      gsap.fromTo('.hero-stats',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.8, delay: 1.1, ease: 'power3.out' }
      );
    }, heroRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={heroRef} className="relative min-h-[60vh] flex items-center overflow-hidden pt-24 pb-16">
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

      <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Two-column layout */}
        <div className="flex flex-col lg:flex-row items-center gap-8 lg:gap-12">

          {/* LEFT — Text content */}
          <div className="flex-1 text-center lg:text-left">
            {/* Shloka */}
            <div className="hero-shloka opacity-0 mb-4">
              <p className="font-sans text-xl sm:text-2xl lg:text-3xl opacity-70 tracking-[4px] text-gray-600"
                style={{ textShadow: '0 0 15px rgba(255, 170, 51, 0.4)' }}>
                {'\u091C\u094D\u092F\u094B\u0924\u093F\u0937\u092E\u094D \u0905\u092F\u092E\u094D \u092C\u094D\u0930\u0939\u094D\u092E'} {t('hero.shlokaSupreme')}
              </p>
            </div>

            {/* Main Title */}
            <div className="hero-title-main opacity-0">
              <h1
                className="text-2xl sm:text-3xl lg:text-4xl text-cosmic-text leading-[1.1]"
                style={{
                  fontWeight: 800,
                  letterSpacing: '-0.02em',
                }}
              >
                {l('Your Complete Astrology Platform', 'आपका पूर्ण ज्योतिष प्लेटफॉर्म')}
              </h1>
              <p
                className="text-base text-sacred-gold-dark mt-4 uppercase"
                style={{
                  fontWeight: 700,
                  letterSpacing: '0.15em',
                }}
              >
                {l('Kundli · Lal Kitab · Vastu · Panchang · Numerology', 'कुंडली · लाल किताब · वास्तु · पंचांग · अंकशास्त्र')}
              </p>
            </div>

            {/* Subtitle */}
            <div className="hero-subtitle opacity-0 mt-6 max-w-xl lg:max-w-none">
              <p className="text-lg text-gray-600 leading-relaxed">
                {l(
                  'Deep Kundli analysis, Lal Kitab remedies & predictions, Vastu floor plan scoring, live Panchang, and Numerology — all in one platform.',
                  'गहरी कुंडली विश्लेषण, लाल किताब उपाय और भविष्यवाणियां, वास्तु फ्लोर प्लान स्कोरिंग, लाइव पंचांग और अंकशास्त्र — एक ही प्लेटफॉर्म।'
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
          </div>

          {/* RIGHT — Zodiac Wheel */}
          <div className="hero-wheel opacity-0 flex-shrink-0 w-full max-w-[360px] lg:max-w-[460px]">
            <LiveTransitWheel />
          </div>

        </div>

        {/* Stats strip — separate section below hero */}
        <div className="hero-stats opacity-0 mt-12">
          <div className="rounded-2xl bg-sacred-gold/5 p-4 sm:p-5">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="rounded-xl border border-sacred-gold/25 bg-cosmic-bg/70 p-3 sm:p-4 flex items-start gap-3">
                <img
                  src="/images/features/feature-kundli.jpg"
                  alt="Kundli"
                  className="w-8 h-8 rounded-lg object-cover shrink-0 border border-sacred-gold/40"
                />
                <div>
                  <p className="text-base font-semibold text-cosmic-text">{l('10,000+ Kundlis Generated', '10,000+ कुंडलियां बनाई गईं')}</p>
                  <p className="text-xs text-gray-600 mt-0.5">{l('Real usage data', 'वास्तविक उपयोग डेटा')}</p>
                </div>
              </div>
              <div className="rounded-xl border border-sacred-gold/25 bg-cosmic-bg/70 p-3 sm:p-4 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark flex items-center justify-center shrink-0">
                  <Users className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-base font-semibold text-cosmic-text">{l('Trusted by Astrologers', 'ज्योतिषियों द्वारा विश्वसनीय')}</p>
                  <p className="text-xs text-gray-600 mt-0.5">{l('Professional daily workflows', 'पेशेवर दैनिक वर्कफ़्लो')}</p>
                </div>
              </div>
              <div className="rounded-xl border border-sacred-gold/25 bg-cosmic-bg/70 p-3 sm:p-4 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark flex items-center justify-center shrink-0">
                  <Grid3X3 className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-base font-semibold text-cosmic-text">{l('5 Modules in One', 'एक में 5 मॉड्यूल')}</p>
                  <p className="text-xs text-gray-600 mt-0.5">{l('Single connected platform', 'एकीकृत सिंगल प्लेटफॉर्म')}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
