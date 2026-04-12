import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { useTranslation } from '@/lib/i18n';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function Hero() {
  const heroRef = useRef<HTMLDivElement>(null);
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.hero-shloka',   { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1,   delay: 0.3, ease: 'power3.out' });
      gsap.fromTo('.hero-badge',    { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.8, delay: 0.4, ease: 'power3.out' });
      gsap.fromTo('.hero-title-main', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1.2, delay: 0.5, ease: 'power3.out' });
      gsap.fromTo('.hero-subtitle', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1,   delay: 0.7, ease: 'power3.out' });
      gsap.fromTo('.hero-cta',      { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, delay: 0.9, ease: 'power3.out' });
      gsap.fromTo('.hero-chart',    { opacity: 0, x: 40, scale: 0.92 }, { opacity: 1, x: 0, scale: 1, duration: 1.3, delay: 0.6, ease: 'power3.out' });
    }, heroRef);
    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={heroRef}
      className="relative min-h-[85vh] flex items-center overflow-hidden pt-24 pb-12"
      style={{
        backgroundImage: 'url(/images/hero-bg.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center top',
      }}
    >
      {/* Dark overlay — keeps text readable over the starry image */}
      <div className="absolute inset-0 z-[1] bg-[#0a0804]/72" />

      {/* Left-side gradient so text column is extra legible */}
      <div className="absolute inset-0 z-[2] pointer-events-none"
        style={{ background: 'linear-gradient(to right, rgba(10,8,4,0.85) 0%, rgba(10,8,4,0.55) 55%, rgba(10,8,4,0.15) 100%)' }}
      />

      {/* Subtle gold top glow */}
      <div className="absolute top-0 left-0 right-0 h-1 z-[3] bg-gradient-to-r from-transparent via-sacred-gold/60 to-transparent" />

      {/* ── Content ── */}
      <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">

          {/* Left column — text */}
          <div className="text-center lg:text-left">

            {/* Shloka */}
            <div className="hero-shloka opacity-0 mb-5">
              <p className="font-sans text-sm tracking-[4px] text-[var(--aged-gold)] uppercase"
                style={{ textShadow: '0 0 18px rgba(255,170,51,0.6)' }}>
                {'\u091C\u094D\u092F\u094B\u0924\u093F\u0937\u092E\u094D \u0905\u092F\u092E\u094D \u092C\u094D\u0930\u0939\u094D\u092E'} {t('hero.shlokaSupreme')}
              </p>
            </div>

            {/* Badge */}
            <div className="hero-badge opacity-0 mb-6 flex justify-center lg:justify-start">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/15 border border-sacred-gold/40">
                <Sparkles className="w-4 h-4 text-sacred-gold-dark" />
                <span className="text-sm font-medium text-sacred-gold-dark">
                  {l('The Only Complete Lal Kitab Platform', 'इकलौता पूर्ण लाल किताब प्लेटफॉर्म')}
                </span>
              </div>
            </div>

            {/* Main Title */}
            <div className="hero-title-main opacity-0">
              <h1
                className="font-sans text-4xl sm:text-5xl lg:text-6xl xl:text-7xl text-cosmic-text leading-[0.95] tracking-wide"
                style={{ textShadow: '0 0 60px rgba(255,153,51,0.25)' }}
              >
                {t('hero.observatory')}
              </h1>
              <p className="font-sans text-base tracking-[12px] text-sacred-gold-dark mt-4 uppercase">
                {t('hero.ofDestiny')}
              </p>
            </div>

            {/* Subtitle */}
            <div className="hero-subtitle opacity-0 mt-8 max-w-xl mx-auto lg:mx-0">
              <p className="text-lg text-cosmic-text/85 leading-relaxed">
                {l(
                  '22 Lal Kitab specializations including Chandra Chalana protocol, Nishaniyan Matcher, and AI-powered insights. Not just another astrology app — a complete karmic operating system.',
                  'चंद्र चालना प्रोटोकॉल, निशानियां मैचर और AI-संचालित अंतर्दृष्टि सहित 22 लाल किताब विशेषज्ञताएं। केवल एक और ज्योतिष ऐप नहीं — एक पूर्ण कर्मिक ऑपरेटिंग सिस्टम।'
                )}
              </p>
            </div>

            {/* CTA Buttons */}
            <div className="hero-cta opacity-0 mt-10 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <a
                href="/login"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-sacred-gold-dark text-white rounded-lg font-semibold hover:bg-sacred-gold transition-all shadow-lg shadow-sacred-gold/25 group"
              >
                {l('Start Your Journey', 'अपनी यात्रा शुरू करें')}
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </a>
              <a
                href="#features"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 border-2 border-sacred-gold/50 text-sacred-gold-dark rounded-lg font-semibold hover:bg-sacred-gold/10 backdrop-blur-sm transition-all"
              >
                {l('Explore Features', 'सुविधाएं देखें')}
              </a>
            </div>

            {/* Trust indicators */}
            <div className="hero-cta opacity-0 mt-10 flex flex-wrap justify-center lg:justify-start gap-6 text-sm text-cosmic-text/65">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-400 shadow-sm shadow-green-400/50" />
                {l('Swiss Ephemeris Accuracy', 'Swiss Ephemeris सटीकता')}
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-400 shadow-sm shadow-green-400/50" />
                {l('Parashari + Jaimini + KP', 'पाराशरी + जैमिनी + केपी')}
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-400 shadow-sm shadow-green-400/50" />
                {l('Hindi + English', 'हिंदी + अंग्रेजी')}
              </div>
            </div>
          </div>

          {/* Right column — Kundli chart image */}
          <div className="hero-chart opacity-0 hidden lg:flex items-center justify-center">
            <div className="relative">
              {/* Outer atmospheric glow */}
              <div className="absolute inset-0 rounded-3xl bg-sacred-gold/20 blur-3xl scale-110" />

              {/* Card frame */}
              <div className="relative rounded-2xl border border-sacred-gold/40 overflow-hidden shadow-2xl shadow-black/60 backdrop-blur-sm bg-black/20">
                <img
                  src="/images/kundli-chart.jpg"
                  alt="Vedic Kundli Chart — 12 Signs of the Zodiac"
                  className="w-[380px] h-auto block"
                  loading="eager"
                />

                {/* Bottom glass label */}
                <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/80 to-transparent px-5 py-4">
                  <p className="text-xs text-center text-sacred-gold-dark/90 font-medium tracking-wider uppercase">
                    {l('12 Zodiac Signs · Swiss Ephemeris · Vedic Astrology', '12 राशियां · Swiss Ephemeris · वैदिक ज्योतिष')}
                  </p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
