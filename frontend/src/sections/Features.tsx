import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Brain, Star, Calendar, BookOpen, Sparkles, ChevronRight, Compass } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const features = [
  { icon: Star, title: 'Kundli', description: 'Detailed Birth Charts', action: 'Generate Kundli', route: '/kundli' },
  { icon: Calendar, title: 'Panchang', description: 'Daily Auspicious Times', action: 'View Panchang', route: '/panchang' },
  { icon: Brain, title: 'AI Astrologer', description: 'Instant Cosmic Guidance', action: 'Ask AI', route: '/ai-chat' },
  { icon: BookOpen, title: 'Shop', description: 'Astrological Products', action: 'Explore', route: '/shop' },
  { icon: Sparkles, title: 'Dosha Analysis', description: 'Personalized Remedies', action: 'Check Dosha', route: '/kundli' },
  { icon: Compass, title: 'Muhurat Finder', description: 'Perfect Timing for Events', action: 'Find Muhurat', route: '/panchang' },
];

export default function Features() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.features-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
      gsap.fromTo('.feature-card', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} id="features" className="relative py-24 bg-cosmic-bg bg-mandala">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="features-title text-center mb-16">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-4">
            Unlock the Secrets of<span className="text-gradient-gold"> Vedic Astrology</span>
          </h2>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card key={index} className="feature-card group relative card-sacred border-sacred-gold/20 hover:border-sacred-gold/50 transition-all duration-300 hover:-translate-y-1 cursor-pointer" onClick={() => navigate(feature.route)}>
                <CardContent className="relative p-6 text-center">
                  <div className="w-16 h-16 rounded-xl flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform bg-sacred-gold/10 border border-sacred-gold/20">
                    <Icon className="w-8 h-8 text-sacred-gold" />
                  </div>
                  <h3 className="text-xl font-sacred font-semibold text-cosmic-text mb-2 uppercase tracking-wide">{feature.title}</h3>
                  <p className="text-sm text-cosmic-text-secondary">{feature.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
        <div className="features-title mt-16 text-center">
          <Button onClick={() => navigate('/ai-chat')} className="btn-sacred">
            <Brain className="w-5 h-5 mr-2" />Chat with AI Astrologer<ChevronRight className="w-5 h-5 ml-2" />
          </Button>
        </div>
      </div>
    </section>
  );
}
