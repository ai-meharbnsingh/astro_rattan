import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Star, ChevronRight, Calendar, MapPin, Clock } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export default function Hero() {
  const heroRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [birthDate, setBirthDate] = useState('');
  const [birthTime, setBirthTime] = useState('');
  const [birthPlace, setBirthPlace] = useState('');

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.hero-word',
        { y: 100, opacity: 0 },
        { y: 0, opacity: 1, duration: 1, stagger: 0.1, ease: 'power3.out', delay: 0.5 }
      );
      gsap.fromTo('.hero-subtitle',
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, delay: 1, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-form',
        { y: 50, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, delay: 1.2, ease: 'power3.out' }
      );
    }, heroRef);
    return () => ctx.revert();
  }, []);

  const handleGenerateKundli = () => {
    if (birthDate && birthTime && birthPlace) {
      navigate('/kundli', { state: { birthDate, birthTime, birthPlace } });
    }
  };

  return (
    <section ref={heroRef} className="relative min-h-screen flex items-center justify-center overflow-hidden hero-sacred bg-mandala bg-cosmic-stars">
      <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-6 border border-sacred-gold/30">
              <Sparkles className="w-4 h-4" />{t('hero.badge')}
            </div>
            <div className="overflow-hidden mb-2">
              <h1 className="text-4xl sm:text-5xl lg:text-7xl font-sacred font-bold tracking-wider">
                <span className="hero-word inline-block text-cosmic-text-secondary uppercase">{t('hero.knowYour')}</span>
              </h1>
            </div>
            <div className="overflow-hidden mb-6">
              <h1 className="text-5xl sm:text-6xl lg:text-8xl font-sacred font-bold tracking-wide">
                <span className="hero-word inline-block text-gradient-gold uppercase">{t('hero.destiny')}</span>
              </h1>
            </div>
            <div className="hero-form">
              <Button onClick={() => navigate('/kundli')} size="lg" className="btn-sacred text-lg px-8 py-6 rounded-full tracking-wider uppercase">
                {t('hero.getFreeKundli')}
              </Button>
            </div>
            <div className="hero-form mt-8 card-sacred rounded-2xl p-6 max-w-md mx-auto lg:mx-0">
              <h3 className="text-lg font-sacred font-semibold text-sacred-gold mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-sacred-gold" />{t('hero.quickKundli')}
              </h3>
              <div className="space-y-4">
                <div className="relative">
                  <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type="date" value={birthDate} onChange={(e) => setBirthDate(e.target.value)} className="pl-10 input-sacred" />
                </div>
                <div className="relative">
                  <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type="time" value={birthTime} onChange={(e) => setBirthTime(e.target.value)} className="pl-10 input-sacred" />
                </div>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type="text" value={birthPlace} onChange={(e) => setBirthPlace(e.target.value)} placeholder={t('hero.birthPlace')} className="pl-10 input-sacred" />
                </div>
                <Button onClick={handleGenerateKundli} className="w-full btn-sacred font-medium">
                  {t('hero.generateKundli')}<ChevronRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            </div>
          </div>
          <div className="hidden lg:flex items-center justify-center">
            <div className="relative w-[420px] h-[420px]">
              {/* Outer cosmic glow */}
              <div className="absolute inset-0 rounded-full bg-gradient-to-br from-sacred-purple/40 to-sacred-gold/10 animate-pulse-gold blur-xl" />
              {/* Zodiac ring */}
              <div className="absolute inset-4 rounded-full border-2 border-sacred-gold/30 animate-spin-slow" />
              <div className="absolute inset-12 rounded-full border border-sacred-gold/20" />
              {/* Inner circle with star */}
              <div className="absolute inset-20 rounded-full bg-gradient-to-br from-sacred-purple/60 to-cosmic-bg border border-sacred-gold/40 flex items-center justify-center shadow-glow-gold">
                <div className="relative">
                  <Star className="w-20 h-20 text-sacred-gold" fill="currentColor" />
                  <div className="absolute inset-0 animate-pulse-gold rounded-full" />
                </div>
              </div>
              {/* Zodiac symbols positioned around the ring */}
              {['\u2648','\u2649','\u264A','\u264B','\u264C','\u264D','\u264E','\u264F','\u2650','\u2651','\u2652','\u2653'].map((symbol, i) => {
                const angle = (i * 30 - 90) * (Math.PI / 180);
                const radius = 185;
                const x = Math.cos(angle) * radius;
                const y = Math.sin(angle) * radius;
                return (
                  <span key={i} className="absolute text-sacred-gold/60 text-lg font-bold" style={{ left: `calc(50% + ${x}px - 10px)`, top: `calc(50% + ${y}px - 10px)` }}>
                    {symbol}
                  </span>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
