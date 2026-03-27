import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { Canvas } from '@react-three/fiber';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, ChevronRight, Calendar, MapPin, Clock } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import ArmillarySphere from '@/components/three/ArmillarySphere';

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
    <section ref={heroRef} className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#0a0a1a]">
      {/* Subtle star-field dots */}
      <div className="absolute inset-0 z-0 opacity-30" style={{ backgroundImage: 'radial-gradient(1px 1px at 20% 30%, #d4af37 0.5px, transparent 0), radial-gradient(1px 1px at 60% 15%, #fff 0.5px, transparent 0), radial-gradient(1px 1px at 80% 70%, #d4af37 0.5px, transparent 0), radial-gradient(1px 1px at 10% 80%, #fff 0.5px, transparent 0), radial-gradient(1px 1px at 45% 55%, #d4af37 0.5px, transparent 0), radial-gradient(1px 1px at 90% 40%, #fff 0.5px, transparent 0)' }} />
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
            <div className="relative w-[500px] h-[500px]" style={{ background: 'none' }}>
              <Canvas
                camera={{ position: [0, 0, 5], fov: 50 }}
                gl={{ alpha: true, premultipliedAlpha: false }}
                scene={{ background: null } as any}
                style={{ background: 'transparent', mixBlendMode: 'screen' }}
                onCreated={({ gl, scene }) => { gl.setClearColor(0x000000, 0); scene.background = null; }}
              >
                <ambientLight intensity={0.5} />
                <pointLight position={[5, 5, 5]} intensity={0.8} color="#d4af37" />
                <pointLight position={[-3, -3, 3]} intensity={0.3} color="#f0e6d3" />
                <ArmillarySphere interactive scale={1} />
              </Canvas>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
