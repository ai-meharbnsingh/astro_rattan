import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Star, Quote } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const testimonials = [
  { name: 'Priya Sharma', location: 'Mumbai', rating: 5, text: 'The AI astrologer provided incredibly accurate insights about my career. Highly recommended!', service: 'AI Astrology' },
  { name: 'Rahul Patel', location: 'Ahmedabad', rating: 5, text: 'Got my Kundli generated and was amazed by the detailed analysis.', service: 'Kundli Analysis' },
  { name: 'Anita Gupta', location: 'Delhi', rating: 5, text: 'The daily Panchang helps me plan my day. Very accurate and easy to use.', service: 'Daily Panchang' },
  { name: 'Vikram Reddy', location: 'Hyderabad', rating: 5, text: 'The Muhurat finder helped me choose the perfect time for my company launch.', service: 'Muhurat' },
];

export default function Testimonials() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.testimonials-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="relative py-24 bg-cosmic-bg">
      <div className="relative z-10">
        <div className="testimonials-title text-center mb-16 px-4">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-6 border border-sacred-gold/30">
            <Star className="w-4 h-4" />Testimonials
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-4">
            What Our Users<span className="text-gradient-gold"> Say</span>
          </h2>
        </div>
        <div className="relative overflow-hidden">
          <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-cosmic-bg to-transparent z-10" />
          <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-cosmic-bg to-transparent z-10" />
          <div className="flex gap-6 animate-marquee-left">
            {[...testimonials, ...testimonials].map((t, i) => (
              <Card key={i} className="flex-shrink-0 w-[350px] card-sacred border-sacred-gold/15">
                <CardContent className="p-6">
                  <Quote className="w-8 h-8 text-sacred-gold/30 mb-4" />
                  <div className="flex gap-1 mb-3">
                    {[...Array(t.rating)].map((_, j) => <Star key={j} className="w-4 h-4 text-sacred-gold fill-sacred-gold" />)}
                  </div>
                  <p className="text-cosmic-text-secondary text-sm mb-4">&ldquo;{t.text}&rdquo;</p>
                  <span className="inline-block text-xs px-3 py-1 rounded-full bg-sacred-gold/10 text-sacred-gold mb-4 border border-sacred-gold/20">{t.service}</span>
                  <div className="flex items-center gap-3 pt-4 border-t border-sacred-gold/10">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center">
                      <span className="text-cosmic-bg font-bold text-sm">{t.name.charAt(0)}</span>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-cosmic-text">{t.name}</p>
                      <p className="text-xs text-cosmic-text-secondary">{t.location}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
        <div className="testimonials-title mt-16 px-4">
          <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
            {[{ value: '50K+', label: 'Happy Users' }, { value: '4.9', label: 'Average Rating' }, { value: '100K+', label: 'Kundlis' }, { value: '98%', label: 'Satisfaction' }].map((stat, i) => (
              <div key={i} className="text-center">
                <p className="text-3xl font-sacred font-bold text-gradient-gold mb-1">{stat.value}</p>
                <p className="text-sm text-cosmic-text-secondary">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
