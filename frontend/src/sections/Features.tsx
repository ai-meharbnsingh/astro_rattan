import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Brain, Star, Calendar, BookOpen, Sparkles, ChevronRight, Compass } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

const features = [
  { icon: Star, titleKey: 'features.kundli.title', descKey: 'features.kundli.description', route: '/kundli' },
  { icon: Calendar, titleKey: 'features.panchang.title', descKey: 'features.panchang.description', route: '/panchang' },
  { icon: Brain, titleKey: 'features.aiAstrologer.title', descKey: 'features.aiAstrologer.description', route: '/ai-chat' },
  { icon: BookOpen, titleKey: 'features.shop.title', descKey: 'features.shop.description', route: '/shop' },
  { icon: Sparkles, titleKey: 'features.dosha.title', descKey: 'features.dosha.description', route: '/kundli' },
  { icon: Compass, titleKey: 'features.muhurat.title', descKey: 'features.muhurat.description', route: '/panchang' },
];

export default function Features() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const { t } = useTranslation();

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
            {t('features.heading')}<span className="text-gradient-gold">{t('features.headingHighlight')}</span>
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
                  <h3 className="text-xl font-sacred font-semibold text-cosmic-text mb-2 uppercase tracking-wide">{t(feature.titleKey)}</h3>
                  <p className="text-sm text-cosmic-text-secondary">{t(feature.descKey)}</p>
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
