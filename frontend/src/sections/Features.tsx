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
    <section ref={sectionRef} id="features" className="relative py-24 bg-[#F5F0E8]">
      {/* Gold gradient line at top */}
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#9A7B0A]/50 to-transparent" />
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="features-title text-center mb-16">
          <p className="text-[#ffaa33] text-sm tracking-[4px] uppercase mb-4 font-['Cinzel']">The Celestial Houses</p>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-['Cinzel_Decorative'] text-[#1a1a2e] mb-4">
            Cosmic <span className="text-[#B8860B]">Services</span>
          </h2>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card 
                key={index} 
                className="feature-card group relative bg-[#F5F0E8] border border-[#9A7B0A]/20 hover:border-[#9A7B0A]/50 transition-all duration-300 hover:-translate-y-1 cursor-pointer" 
                onClick={() => navigate(feature.route)}
              >
                <CardContent className="relative p-6 text-center">
                  <div className="w-16 h-16 flex items-center justify-center mb-4 mx-auto bg-[#9A7B0A]/10 border border-[#9A7B0A]/20 group-hover:scale-110 transition-transform">
                    <Icon className="w-8 h-8 text-[#B8860B]" />
                  </div>
                  <h3 className="text-xl font-['Cinzel'] font-semibold text-[#1a1a2e] mb-2 uppercase tracking-wide">
                    {t(feature.titleKey)}
                  </h3>
                  <p className="text-sm text-[#1a1a2e]/60">{t(feature.descKey)}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
        
        <div className="features-title mt-16 text-center">
          <Button 
            onClick={() => navigate('/ai-chat')} 
            className="bg-transparent border border-[#9A7B0A] text-[#9A7B0A] hover:bg-[#9A7B0A] hover:text-[#1a1a2e] transition-all px-8 py-6 text-base font-['Cinzel'] tracking-wider"
          >
            <Brain className="w-5 h-5 mr-2" />
            {t('features.chatWithAI')}
            <ChevronRight className="w-5 h-5 ml-2" />
          </Button>
        </div>
      </div>
      
      {/* Gold gradient line at bottom */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#9A7B0A]/30 to-transparent" />
    </section>
  );
}
