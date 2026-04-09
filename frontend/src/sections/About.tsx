import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Sparkles, Star, Layers, BookOpen } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

const stats = [
  { value: '21', label: 'Calculation Engines', icon: Layers },
  { value: '24', label: 'Kundli Analysis Tabs', icon: Star },
  { value: '16', label: 'Divisional Charts', icon: Sparkles },
  { value: '3', label: 'Astrological Systems', icon: BookOpen },
];

export default function About() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { t } = useTranslation();

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.about-content', { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
      gsap.fromTo('.stat-item', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: '.stats-grid', start: 'top 85%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} id="about" className="relative py-24 bg-cosmic-bg overflow-hidden">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="about-content max-w-3xl mx-auto text-center mb-16">
          <p className="text-sacred-gold text-sm tracking-[4px] uppercase mb-4 font-sans">Built Different</p>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sans text-cosmic-text mb-6">
            {t('about.heading')}
          </h2>
          <div className="space-y-4 text-cosmic-text">
            <p>
              Most astrology apps use lookup tables and generic predictions.
              Astro Rattan computes every position from Swiss Ephemeris — the same
              library used by research astronomers — accurate to arc-seconds.
            </p>
            <p>
              Three complete astrological systems in one app: <strong className="text-sacred-gold-dark">Parashari</strong> (classical Vedic),
              <strong className="text-sacred-gold-dark"> Jaimini</strong> (Chara Karakas, special lagnas),
              and <strong className="text-sacred-gold-dark">KP System</strong> (Krishnamurti Paddhati with sub-lord analysis).
              Plus full <strong className="text-sacred-gold-dark">Lal Kitab</strong> remedies and <strong className="text-sacred-gold-dark">Numerology</strong>.
            </p>
          </div>
        </div>

        <div className="stats-grid grid grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="stat-item border border-sacred-gold p-6 text-center bg-cosmic-bg hover:border-sacred-gold transition-colors">
                <div className="w-12 h-12 flex items-center justify-center mx-auto mb-4 bg-sacred-gold-dark border border-sacred-gold">
                  <Icon className="w-6 h-6 text-sacred-gold-dark" />
                </div>
                <p className="text-3xl font-sans font-bold text-sacred-gold-dark mb-1">{stat.value}</p>
                <p className="text-sm text-cosmic-text">{stat.label}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
