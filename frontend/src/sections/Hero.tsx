import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Star, ChevronRight, Calendar, MapPin, Clock } from 'lucide-react';

export default function Hero() {
  const heroRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
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
    <section ref={heroRef} className="relative min-h-screen flex items-center justify-center overflow-hidden hero-sacred bg-mandala">
      <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold-dark text-sm font-medium mb-6 border border-sacred-gold/30">
              <Sparkles className="w-4 h-4" />Vedic Astrology
            </div>
            <div className="overflow-hidden mb-4">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-sacred font-bold text-sacred-brown">
                <span className="hero-word inline-block">Discover</span>{' '}
                <span className="hero-word inline-block">Your</span>
              </h1>
            </div>
            <div className="overflow-hidden mb-4">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-sacred font-bold">
                <span className="hero-word inline-block text-gradient-gold">Cosmic</span>{' '}
                <span className="hero-word inline-block text-sacred-saffron-dark">Path</span>
              </h1>
            </div>
            <p className="hero-subtitle text-lg text-sacred-text-secondary max-w-xl mx-auto lg:mx-0 mb-8">
              Unlock Vedic astrology wisdom with AI-powered insights. Get personalized predictions and spiritual guidance.
            </p>
            <div className="hero-form card-sacred rounded-2xl p-6 max-w-md mx-auto lg:mx-0">
              <h3 className="text-lg font-sacred font-semibold text-sacred-brown mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-sacred-gold-dark" />Generate Free Kundli
              </h3>
              <div className="space-y-4">
                <div className="relative">
                  <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
                  <Input type="date" value={birthDate} onChange={(e) => setBirthDate(e.target.value)} className="pl-10 input-sacred" />
                </div>
                <div className="relative">
                  <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
                  <Input type="time" value={birthTime} onChange={(e) => setBirthTime(e.target.value)} className="pl-10 input-sacred" />
                </div>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
                  <Input type="text" value={birthPlace} onChange={(e) => setBirthPlace(e.target.value)} placeholder="Birth Place" className="pl-10 input-sacred" />
                </div>
                <Button onClick={handleGenerateKundli} className="w-full btn-sacred font-medium">
                  Generate Kundli<ChevronRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            </div>
            <div className="hero-form flex flex-wrap justify-center lg:justify-start gap-4 mt-6">
              <Button variant="outline" onClick={() => navigate('/ai-chat')} className="border-sacred-gold/50 text-sacred-brown hover:bg-sacred-gold/10 hover:border-sacred-gold">
                <Sparkles className="w-4 h-4 mr-2 text-sacred-saffron" />Ask AI Astrologer
              </Button>
            </div>
          </div>
          <div className="hidden lg:flex items-center justify-center">
            <div className="relative w-[400px] h-[400px]">
              <div className="absolute inset-0 rounded-full bg-gradient-to-br from-sacred-gold/10 to-sacred-saffron/10 animate-pulse-gold" />
              <div className="absolute inset-8 rounded-full bg-gradient-to-br from-sacred-gold/20 to-sacred-saffron/20" />
              <div className="absolute inset-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center shadow-lg">
                <Star className="w-24 h-24 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
