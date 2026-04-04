import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Calendar, MapPin, Clock } from 'lucide-react';
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
      // Shloka fade in
      gsap.fromTo('.hero-shloka',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 1, delay: 0.3, ease: 'power3.out' }
      );
      
      // Title animation
      gsap.fromTo('.hero-title-main',
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 1.2, delay: 0.5, ease: 'power3.out' }
      );
      
      // Subtitle
      gsap.fromTo('.hero-subtitle-text',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.8, delay: 0.8, ease: 'power3.out' }
      );
      
      // Equation box
      gsap.fromTo('.hero-equation',
        { opacity: 0, scale: 0.9 },
        { opacity: 1, scale: 1, duration: 0.8, delay: 1, ease: 'power3.out' }
      );
      
      // CTA Buttons
      gsap.fromTo('.hero-cta',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.8, delay: 1.2, ease: 'power3.out' }
      );
      
      // Form
      gsap.fromTo('.hero-form',
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 0.8, delay: 1.4, ease: 'power3.out' }
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
    <section ref={heroRef} className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Grain overlay */}
      <div className="absolute inset-0 z-[1] opacity-[0.03] pointer-events-none"
        style={{ 
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")` 
        }} 
      />
      
      {/* Vignette */}
      <div className="absolute inset-0 z-[2] pointer-events-none"
        style={{ 
          background: 'radial-gradient(ellipse at center, transparent 30%, rgba(139,69,19,0.06) 100%)' 
        }} 
      />
      
      <div className="relative z-10 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        {/* Sanskrit Shloka */}
        <div className="hero-shloka opacity-0 mb-8">
          <p className="font-['Cinzel'] text-xs md:text-sm tracking-[6px] text-[#ffaa33] uppercase"
            style={{ textShadow: '0 0 15px rgba(255, 170, 51, 0.4)' }}>
            ज्योतिषम् अयम् ब्रह्म — Astrology is the Supreme
          </p>
        </div>

        {/* Main Title */}
        <div className="hero-title-main opacity-0 mb-6">
          <h1 className="font-['Cinzel_Decorative'] text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-[#1a1a2e] leading-[0.95] tracking-wide"
            style={{ textShadow: '0 0 60px rgba(184, 134, 11, 0.15)' }}>
            {t('hero.observatory')}
          </h1>
          <p className="font-['Cinzel'] text-sm md:text-base tracking-[12px] text-[#9A7B0A] mt-4 uppercase">
            {t('hero.ofDestiny')}
          </p>
        </div>

        {/* Equation */}
        <div className="hero-equation opacity-0 mb-8 inline-block">
          <div className="px-5 py-2 border border-[#9A7B0A]/30 bg-[#22223a]/60 backdrop-blur-sm">
            <code className="font-['Space_Mono'] text-xs md:text-sm text-[#9A7B0A] tracking-wider">
              L = Asc + (S × 30°) + (N × 3°20')
            </code>
          </div>
        </div>

        {/* Subtitle */}
        <div className="hero-subtitle-text opacity-0 mb-10 max-w-xl mx-auto">
          <p className="text-sm md:text-base text-[#1a1a2e]/70 leading-relaxed font-light">
            The universe does not hide its secrets. It writes them in light,<br className="hidden md:block" />
            across twelve houses, waiting for those who know how to read.
          </p>
        </div>

        {/* CTA Buttons - Elegant Style */}
        <div className="hero-cta opacity-0 mb-12 flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button 
            onClick={() => navigate('/kundli')} 
            className="bg-[#9A7B0A] text-[#1a1a2e] hover:bg-[#B8860B] transition-all duration-300 
                       text-xs tracking-[3px] uppercase font-['Cinzel'] font-semibold
                       px-8 py-5 rounded-none border-none"
            style={{ boxShadow: '0 0 30px rgba(212, 175, 55, 0.3)' }}
          >
            {t('hero.getFreeKundli')}
          </Button>
          
          <Button 
            onClick={() => navigate('/consultation')}
            variant="outline"
            className="bg-transparent border border-[#8B7355]/30 text-[#1a1a2e]/80 hover:border-[#9A7B0A] hover:text-[#9A7B0A] 
                       transition-all duration-300 text-xs tracking-[3px] uppercase font-['Cinzel']
                       px-8 py-5 rounded-none"
          >
            {t('hero.consultExpert')}
          </Button>
        </div>

        {/* Quick Kundli Form */}
        <div className="hero-form opacity-0 max-w-md mx-auto">
          <div className="border border-[#9A7B0A]/20 bg-[#22223a]/60 backdrop-blur-sm p-5 relative">
            {/* Corner decorations */}
            <div className="absolute top-0 left-0 w-3 h-3 border-t border-l border-[#9A7B0A]" />
            <div className="absolute top-0 right-0 w-3 h-3 border-t border-r border-[#9A7B0A]" />
            <div className="absolute bottom-0 left-0 w-3 h-3 border-b border-l border-[#9A7B0A]" />
            <div className="absolute bottom-0 right-0 w-3 h-3 border-b border-r border-[#9A7B0A]" />
            
            <p className="text-[#9A7B0A] text-xs tracking-[3px] uppercase mb-4 font-['Cinzel']">
              {t('hero.calculateChart')}
            </p>
            
            <div className="space-y-3">
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#9A7B0A]/70" />
                <Input 
                  type="date" 
                  value={birthDate} 
                  onChange={(e) => setBirthDate(e.target.value)} 
                  className="pl-9 bg-transparent border-[#8B7355]/10 text-[#1a1a2e] text-sm
                             focus:border-[#9A7B0A] rounded-none h-10"
                />
              </div>
              <div className="relative">
                <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#9A7B0A]/70" />
                <Input 
                  type="time" 
                  value={birthTime} 
                  onChange={(e) => setBirthTime(e.target.value)} 
                  className="pl-9 bg-transparent border-[#8B7355]/10 text-[#1a1a2e] text-sm
                             focus:border-[#9A7B0A] rounded-none h-10"
                />
              </div>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#9A7B0A]/70" />
                <Input 
                  type="text" 
                  value={birthPlace} 
                  onChange={(e) => setBirthPlace(e.target.value)} 
                  placeholder={t('hero.birthPlace')} 
                  className="pl-9 bg-transparent border-[#8B7355]/10 text-[#1a1a2e] text-sm placeholder:text-[#1a1a2e]/30
                             focus:border-[#9A7B0A] rounded-none h-10"
                />
              </div>
              <Button 
                onClick={handleGenerateKundli} 
                className="w-full bg-transparent border border-[#9A7B0A] text-[#9A7B0A] 
                           hover:bg-[#9A7B0A] hover:text-[#1a1a2e] transition-all duration-300
                           font-['Cinzel'] text-xs tracking-[2px] uppercase h-10 rounded-none"
              >
                {t('hero.generateKundli')}
              </Button>
            </div>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 opacity-50">
          <div className="w-[1px] h-12 bg-gradient-to-b from-[#9A7B0A] to-transparent" />
        </div>
      </div>
    </section>
  );
}
