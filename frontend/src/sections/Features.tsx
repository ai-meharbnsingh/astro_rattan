import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Brain, Star, Calendar, BookOpen, Sparkles, ChevronRight, Compass } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const features = [
  { icon: Star, title: 'Kundli Analysis', description: 'Generate detailed birth charts with planetary positions and insights.', action: 'Generate Kundli', route: '/kundli', color: 'gold' },
  { icon: Calendar, title: 'Daily Panchang', description: 'Stay aligned with cosmic rhythms. Get daily Tithi, Nakshatra, and more.', action: 'View Panchang', route: '/panchang', color: 'saffron' },
  { icon: Brain, title: 'AI Astrologer', description: 'Ask anything about your future, relationships, or spiritual growth.', action: 'Ask AI', route: '/ai-chat', color: 'gold' },
  { icon: BookOpen, title: 'Spiritual Library', description: 'Access ancient wisdom from Bhagavad Gita, mantras, and pooja guides.', action: 'Explore', route: '/library', color: 'saffron' },
  { icon: Sparkles, title: 'Dosha Analysis', description: 'Identify Mangal Dosha, Kaal Sarp, and get personalized remedies.', action: 'Check Dosha', route: '/kundli', color: 'gold' },
  { icon: Compass, title: 'Muhurat Finder', description: 'Find auspicious times for marriage, business, and life events.', action: 'Find Muhurat', route: '/panchang', color: 'saffron' },
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
    <section ref={sectionRef} id="features" className="relative py-24 bg-sacred-cream bg-mandala">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="features-title text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold-dark text-sm font-medium mb-6 border border-sacred-gold/30">
            <Sparkles className="w-4 h-4" />Our Services
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-sacred-brown mb-4">
            Unlock the Secrets of<span className="text-gradient-gold"> Vedic Astrology</span>
          </h2>
          <p className="text-lg text-sacred-text-secondary max-w-2xl mx-auto">
            Discover ancient Vedic wisdom combined with modern AI technology
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            const isGold = feature.color === 'gold';
            return (
              <Card key={index} className="feature-card group relative card-sacred border-0 transition-all duration-300 hover:-translate-y-1">
                <CardContent className="relative p-6">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform ${isGold ? 'bg-sacred-gold/10' : 'bg-sacred-saffron/10'}`}>
                    <Icon className={`w-6 h-6 ${isGold ? 'text-sacred-gold-dark' : 'text-sacred-saffron-dark'}`} />
                  </div>
                  <h3 className="text-xl font-sacred font-semibold text-sacred-brown mb-2">{feature.title}</h3>
                  <p className="text-sm text-sacred-text-secondary mb-4">{feature.description}</p>
                  <Button variant="ghost" size="sm" onClick={() => navigate(feature.route)} className={`p-0 h-auto hover:bg-transparent ${isGold ? 'text-sacred-gold-dark' : 'text-sacred-saffron-dark'}`}>
                    {feature.action}<ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>
        <div className="features-title mt-16 text-center">
          <p className="text-sacred-text-secondary mb-4">Not sure where to start? Try our AI Astrologer</p>
          <Button onClick={() => navigate('/ai-chat')} className="btn-sacred">
            <Brain className="w-5 h-5 mr-2" />Chat with AI Astrologer<ChevronRight className="w-5 h-5 ml-2" />
          </Button>
        </div>
      </div>
    </section>
  );
}
