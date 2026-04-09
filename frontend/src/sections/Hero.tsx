import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { useTranslation } from '@/lib/i18n';

export default function Hero() {
  const heroRef = useRef<HTMLDivElement>(null);
  const { t } = useTranslation();

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.hero-shloka',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 1, delay: 0.3, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-title-main',
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 1.2, delay: 0.5, ease: 'power3.out' }
      );
    }, heroRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={heroRef} className="relative min-h-[40vh] flex items-center justify-center overflow-hidden pt-24 pb-8">
      <div className="absolute inset-0 z-[1] opacity-[0.03] pointer-events-none"
        style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")` }}
      />
      <div className="absolute inset-0 z-[2] pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at center, transparent 30%, rgba(139,69,19,0.06) 100%)' }}
      />

      <div className="relative z-10 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        <div className="hero-shloka opacity-0 mb-8">
          <p className="font-sans text-base tracking-[6px] text-[var(--aged-gold)] uppercase"
            style={{ textShadow: '0 0 15px rgba(255, 170, 51, 0.4)' }}>
            {'\u091C\u094D\u092F\u094B\u0924\u093F\u0937\u092E\u094D \u0905\u092F\u092E\u094D \u092C\u094D\u0930\u0939\u094D\u092E'} — Astrology is the Supreme
          </p>
        </div>

        <div className="hero-title-main opacity-0">
          <h1 className="font-sans text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-cosmic-text leading-[0.95] tracking-wide"
            style={{ textShadow: '0 0 60px rgba(255, 153, 51, 0.15)' }}>
            {t('hero.observatory')}
          </h1>
          <p className="font-sans text-base tracking-[12px] text-sacred-gold-dark mt-4 uppercase">
            {t('hero.ofDestiny')}
          </p>
        </div>
      </div>

    </section>
  );
}
