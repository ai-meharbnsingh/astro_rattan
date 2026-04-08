import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { ChevronRight, Star } from 'lucide-react';

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
    <section ref={sectionRef} className="relative min-h-[50vh] flex items-center justify-center overflow-hidden bg-cosmic-bg">
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-sacred-gold-dark/30 to-transparent" />

      <div className="relative z-10 cta-content max-w-3xl mx-auto px-4 text-center py-20">
        <div className="flex justify-center gap-2 mb-6">
          {[...Array(5)].map((_, i) => (
            <Star key={i} className="w-5 h-5 text-sacred-gold-dark" fill="currentColor" />
          ))}
        </div>

        <h2 className="text-3xl sm:text-4xl lg:text-5xl font-['Cinzel_Decorative'] text-cosmic-text mb-6">
          Start Reading Your Chart
        </h2>

        <p className="text-cosmic-text/60 max-w-xl mx-auto mb-10">
          Free account. No credit card. Full access to all 21 engines,
          24 analysis tabs, and PDF export.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            onClick={() => navigate('/login')}
            className="bg-sacred-gold-dark text-cosmic-bg hover:bg-sacred-gold transition-all px-8 py-5 text-xs font-cinzel tracking-[3px] uppercase rounded-none"
            style={{ boxShadow: '0 0 30px rgba(212, 175, 55, 0.3)' }}
          >
            Create Free Account
            <ChevronRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-sacred-gold-dark/30 to-transparent" />
    </section>
  );
}
