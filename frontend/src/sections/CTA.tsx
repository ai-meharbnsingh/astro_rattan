import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { Sparkles, Phone, ChevronRight, Star } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

export default function CTA() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const { t } = useTranslation();

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.cta-content', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="relative min-h-[70vh] flex items-center justify-center overflow-hidden bg-cosmic-bg">
      {/* Gold gradient lines */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-sacred-gold-dark/30 to-transparent" />
      
      {/* Subtle glow effects */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-sacred-gold-dark/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-sacred-gold-dark/5 rounded-full blur-3xl" />
      </div>
      
      <div className="relative z-10 cta-content max-w-4xl mx-auto px-4 text-center">
        <div className="flex justify-center gap-2 mb-6">
          {[...Array(5)].map((_, i) => (
            <Star key={i} className="w-6 h-6 text-sacred-gold-dark" fill="currentColor" />
          ))}
        </div>
        
        <h2 className="text-4xl sm:text-5xl lg:text-6xl font-['Cinzel_Decorative'] text-cosmic-text mb-6">
          {t('cta.heading')}
        </h2>

        <p className="text-lg text-cosmic-text/70 max-w-2xl mx-auto mb-10">
          {t('cta.subtitle2')}
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <Button 
            onClick={() => navigate('/ai-chat')} 
            size="lg" 
            className="bg-transparent border border-[#ffaa33] text-[#ffaa33] hover:bg-[#ffaa33] hover:text-cosmic-bg transition-all text-lg px-8 py-6 font-['Cinzel']"
          >
            <Sparkles className="w-5 h-5 mr-2" />
            {t('cta.chatAI')}
            <ChevronRight className="w-5 h-5 ml-2" />
          </Button>
          
          <Button 
            variant="outline" 
            size="lg" 
            className="border-sacred-gold/50 text-cosmic-text text-lg px-8 py-6 hover:bg-sacred-gold-dark/10 hover:border-sacred-gold bg-transparent font-['Cinzel']"
          >
            <Phone className="w-5 h-5 mr-2" />
            {t('cta.talkExpert')}
          </Button>
        </div>
        
        <div className="flex flex-wrap justify-center gap-6 text-sm text-cosmic-text/60">
          {['Free Kundli', '24/7 Support', '100% Accurate', 'Expert Astrologers'].map((item, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="w-2 h-2 bg-sacred-gold-dark" />
              <span>{item}</span>
            </div>
          ))}
        </div>
      </div>
      
      {/* Bottom gold line */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-sacred-gold-dark/30 to-transparent" />
    </section>
  );
}
