import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { useTranslation } from '@/lib/i18n';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function Hero() {
  const heroRef = useRef<HTMLDivElement>(null);
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return; // reduced motion
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
    }, heroRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={heroRef} className="relative min-h-[60vh] flex items-center justify-center overflow-hidden pt-24 pb-8">
      {/* Background decorative elements */}
      <div className="absolute inset-0 z-[1] opacity-[0.03] pointer-events-none"
        style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")` }}
      />
      <div className="absolute inset-0 z-[2] pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at center, transparent 30%, rgba(139,69,19,0.06) 100%)' }}
      />
      
      {/* Floating orbs */}
      <div className="absolute top-1/4 left-10 w-64 h-64 bg-sacred-gold/5 rounded-full blur-3xl opacity-20" />
      <div className="absolute bottom-1/4 right-10 w-80 h-80 bg-[#8B4513]/10 rounded-full blur-3xl opacity-20" />

      <div className="relative z-10 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        {/* Badge */}
        <div className="hero-badge opacity-0 mb-6">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 border border-sacred-gold/30">
            <Sparkles className="w-4 h-4 text-sacred-gold-dark" />
            <span className="text-sm font-medium text-sacred-gold-dark">
              {l('Vedic Astrology + Lal Kitab + Vastu', 'वैदिक ज्योतिष + लाल किताब + वास्तु')}
            </span>
          </div>
        </div>

        {/* Main Title */}
        <div className="hero-title-main opacity-0">
          <h1 className="font-sans text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-cosmic-text leading-[0.95] tracking-wide"
            style={{ textShadow: '0 0 60px rgba(255, 153, 51, 0.15)' }}>
            {l('The Only Complete Lal Kitab Platform', 'इकलौता पूर्ण लाल किताब प्लेटफॉर्म')}
          </h1>
          <p className="font-sans text-base tracking-[4px] text-sacred-gold-dark mt-4 uppercase">
            {t('hero.ofDestiny')}
          </p>
        </div>

        {/* Shloka */}
        <div className="hero-shloka opacity-0 mb-6 mt-4">
          <p className="font-sans text-xs opacity-60 tracking-[4px] text-[var(--aged-gold)] uppercase"
            style={{ textShadow: '0 0 15px rgba(255, 170, 51, 0.4)' }}>
            {'\u091C\u094D\u092F\u094B\u0924\u093F\u0937\u092E\u094D \u0905\u092F\u092E\u094D \u092C\u094D\u0930\u0939\u094D\u092E'} {t('hero.shlokaSupreme')}
          </p>
        </div>

        {/* Subtitle */}
        <div className="hero-subtitle opacity-0 mt-8 max-w-2xl mx-auto">
          <p className="text-lg text-cosmic-text/80 leading-relaxed">
            {l(
              '22 Lal Kitab specializations including Chandra Chalana protocol, Nishaniyan Matcher, and AI-powered insights. Not just another astrology app — a complete karmic operating system.',
              'चंद्र चालना प्रोटोकॉल, निशानियां मैचर और AI-संचालित अंतर्दृष्टि सहित 22 लाल किताब विशेषज्ञताएं। केवल एक और ज्योतिष ऐप नहीं — एक पूर्ण कर्मिक ऑपरेटिंग सिस्टम।'
            )}
          </p>
        </div>

        {/* CTA Buttons */}
        <div className="hero-cta opacity-0 mt-10 flex flex-col sm:flex-row gap-4 justify-center">
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
        <div className="hero-cta opacity-0 mt-12 flex flex-wrap justify-center gap-8 text-sm text-cosmic-text/60">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500"></span>
            {l('10,000+ Kundlis Generated', '10,000+ कुंडलियां बनाई गईं')}
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500"></span>
            {l('Trusted by Astrologers Across India', 'पूरे भारत के ज्योतिषियों द्वारा विश्वसनीय')}
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500"></span>
            {l('22 Lal Kitab Specializations', '22 लाल किताब विशेषज्ञताएं')}
          </div>
        </div>
      </div>

    </section>
  );
}
