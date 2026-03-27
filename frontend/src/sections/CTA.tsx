import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { Sparkles, Phone, ChevronRight, Star } from 'lucide-react';
import { Canvas } from '@react-three/fiber';
import { FloatingPlanet } from '@/components/three';

gsap.registerPlugin(ScrollTrigger);

export default function CTA() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.cta-content', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="relative min-h-[70vh] flex items-center justify-center overflow-hidden bg-cosmic-bg bg-mandala bg-cosmic-stars">
      <div className="absolute inset-0 z-0 opacity-30 pointer-events-none">
        <Canvas camera={{ position: [0, 0, 8], fov: 50 }} gl={{ alpha: true }}>
          <FloatingPlanet color="#ffd700" size={0.4} position={[-4, 2, -2]} hasRing rotationSpeed={0.2} />
          <FloatingPlanet color="#7c3aed" size={0.25} position={[4.5, -1.5, -3]} rotationSpeed={0.35} />
          <FloatingPlanet color="#f97316" size={0.3} position={[3, 3, -4]} hasRing orbitRadius={1.5} rotationSpeed={0.15} />
        </Canvas>
      </div>
      <div className="absolute inset-0 z-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-sacred-purple/20 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-sacred-gold/5 rounded-full blur-3xl" />
      </div>
      <div className="relative z-10 cta-content max-w-4xl mx-auto px-4 text-center">
        <div className="flex justify-center gap-2 mb-6">
          {[...Array(5)].map((_, i) => <Star key={i} className="w-6 h-6 text-sacred-gold" fill="currentColor" />)}
        </div>
        <h2 className="text-4xl sm:text-5xl lg:text-6xl font-sacred font-bold text-cosmic-text mb-6">
          Ready to Meet Your<span className="block text-gradient-gold">Future?</span>
        </h2>
        <p className="text-lg text-cosmic-text-secondary max-w-2xl mx-auto mb-10">
          Unlock the secrets of your destiny with AI-powered Vedic astrology.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <Button onClick={() => navigate('/ai-chat')} size="lg" className="btn-saffron text-lg px-8 py-6">
            <Sparkles className="w-5 h-5 mr-2" />Chat with AI Astrologer<ChevronRight className="w-5 h-5 ml-2" />
          </Button>
          <Button variant="outline" size="lg" className="border-sacred-gold/50 text-cosmic-text text-lg px-8 py-6 hover:bg-sacred-gold/10 hover:border-sacred-gold">
            <Phone className="w-5 h-5 mr-2" />Talk to Expert
          </Button>
        </div>
        <div className="flex flex-wrap justify-center gap-6 text-sm text-cosmic-text-secondary">
          {['Free Kundli', '24/7 Support', '100% Accurate', 'Expert Astrologers'].map((item, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-sacred-gold" />
              <span>{item}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
