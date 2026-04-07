import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { Sparkles, Star, ChevronRight, Users, Award, Globe } from 'lucide-react';
import { Canvas } from '@react-three/fiber';
import { FloatingPlanet } from '@/components/three';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

const stats = [
  { value: '50K+', label: 'Kundlis Generated', icon: Star },
  { value: '100+', label: 'Expert Astrologers', icon: Users },
  { value: '99%', label: 'Accuracy Rate', icon: Award },
  { value: '24/7', label: 'AI Support', icon: Globe },
];

export default function About() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { t } = useTranslation();

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.about-content', { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
      gsap.fromTo('.about-image', { x: 50, opacity: 0 }, { x: 0, opacity: 1, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
      gsap.fromTo('.stat-item', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: '.stats-grid', start: 'top 85%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} id="about" className="relative py-24 bg-cosmic-bg overflow-hidden">
      {/* Observatory theme - pure black with gold accents */}
      <div className="absolute inset-0 z-0 bg-gradient-to-b from-cosmic-bg via-transparent to-cosmic-bg pointer-events-none" />
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          <div className="about-content">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-6 border border-sacred-gold/30">
              <Sparkles className="w-4 h-4" />{t('about.ourStory')}
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-6">
              {t('about.heading')}
            </h2>
            <div className="space-y-4 text-cosmic-text-secondary mb-8">
              <p>{t('about.p1')}</p>
              <p>{t('about.p2')}</p>
            </div>
            <Button className="btn-sacred">
              {t('about.learnMore')}<ChevronRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
          <div className="about-image relative">
            <div className="relative aspect-square max-w-lg mx-auto">
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-sacred-gold-dark/10 to-transparent border border-sacred-gold/20" />
              <div className="absolute inset-8 rounded-2xl card-sacred flex items-center justify-center overflow-hidden">
              </div>
            </div>
          </div>
        </div>
        <div className="stats-grid grid grid-cols-2 lg:grid-cols-4 gap-6 mt-20">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="stat-item card-sacred rounded-2xl p-6 text-center">
                <div className="w-12 h-12 rounded-xl bg-sacred-gold/10 flex items-center justify-center mx-auto mb-4 border border-sacred-gold/20">
                  <Icon className="w-6 h-6 text-sacred-gold" />
                </div>
                <p className="text-3xl font-sacred font-bold text-gradient-gold mb-1">{stat.value}</p>
                <p className="text-sm text-cosmic-text-secondary">{stat.label}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
