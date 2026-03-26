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
    <section ref={sectionRef} className="relative py-24 bg-white">
      <div className="relative z-10">
        <div className="testimonials-title text-center mb-16 px-4">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-minimal-indigo/10 text-minimal-indigo text-sm font-medium mb-6">
            <Star className="w-4 h-4" />Testimonials
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold text-minimal-gray-900 mb-4">
            What Our Users<span className="text-gradient-indigo"> Say</span>
          </h2>
        </div>
        <div className="relative overflow-hidden">
          <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-white to-transparent z-10" />
          <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-white to-transparent z-10" />
          <div className="flex gap-6 animate-marquee-left">
            {[...testimonials, ...testimonials].map((t, i) => (
              <Card key={i} className="flex-shrink-0 w-[350px] bg-minimal-gray-50 border-0 shadow-soft">
                <CardContent className="p-6">
                  <Quote className="w-8 h-8 text-minimal-indigo/30 mb-4" />
                  <div className="flex gap-1 mb-3">
                    {[...Array(t.rating)].map((_, j) => <Star key={j} className="w-4 h-4 text-minimal-indigo fill-minimal-indigo" />)}
                  </div>
                  <p className="text-minimal-gray-600 text-sm mb-4">&ldquo;{t.text}&rdquo;</p>
                  <span className="inline-block text-xs px-3 py-1 rounded-full bg-minimal-indigo/10 text-minimal-indigo mb-4">{t.service}</span>
                  <div className="flex items-center gap-3 pt-4 border-t border-minimal-gray-200">
                    <div className="w-10 h-10 rounded-full bg-minimal-indigo flex items-center justify-center">
                      <span className="text-white font-bold text-sm">{t.name.charAt(0)}</span>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-minimal-gray-900">{t.name}</p>
                      <p className="text-xs text-minimal-gray-500">{t.location}</p>
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
                <p className="text-3xl font-display font-bold text-gradient-indigo mb-1">{stat.value}</p>
                <p className="text-sm text-minimal-gray-500">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
