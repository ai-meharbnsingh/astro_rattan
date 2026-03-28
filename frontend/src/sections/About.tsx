import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { Sparkles, Star, ChevronRight, Users, Award, Globe } from 'lucide-react';
import { Canvas } from '@react-three/fiber';
import { FloatingPlanet } from '@/components/three';

gsap.registerPlugin(ScrollTrigger);

const stats = [
  { value: '50K+', label: 'Kundlis Generated', icon: Star },
  { value: '100+', label: 'Expert Astrologers', icon: Users },
  { value: '99%', label: 'Accuracy Rate', icon: Award },
  { value: '24/7', label: 'AI Support', icon: Globe },
];

export default function About() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.about-content', { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
      gsap.fromTo('.about-image', { x: 50, opacity: 0 }, { x: 0, opacity: 1, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
      gsap.fromTo('.stat-item', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: '.stats-grid', start: 'top 85%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} id="about" className="relative py-24 bg-[#F5F0E8] overflow-hidden">
      {/* Observatory theme - pure black with gold accents */}
      <div className="absolute inset-0 z-0 bg-gradient-to-b from-black via-transparent to-black pointer-events-none" />
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          <div className="about-content">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-6 border border-sacred-gold/30">
              <Sparkles className="w-4 h-4" />Our Story
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-6">
              Bridging Ancient Wisdom with<span className="text-gradient-gold"> Modern Technology</span>
            </h2>
            <div className="space-y-4 text-cosmic-text-secondary mb-8">
              <p>Astro Rattan was born from a profound respect for Vedic astrology and a vision to make this ancient wisdom accessible to everyone.</p>
              <p>We believe that understanding your cosmic blueprint empowers you to make better decisions and navigate life&apos;s challenges.</p>
            </div>
            <Button className="btn-sacred">
              Learn More About Us<ChevronRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
          <div className="about-image relative">
            <div className="relative aspect-square max-w-lg mx-auto">
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-[#9A7B0A]/10 to-transparent border border-[#9A7B0A]/20" />
              <div className="absolute inset-8 rounded-2xl card-sacred flex items-center justify-center overflow-hidden">
                <div className="absolute inset-0 z-0 opacity-30 pointer-events-none">
                  <Canvas camera={{ position: [0, 0, 4], fov: 50 }} gl={{ alpha: true }}>
                    <FloatingPlanet color="#B8860B" size={0.6} position={[0, 0, 0]} hasRing rotationSpeed={0.25} />
                  </Canvas>
                </div>
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
