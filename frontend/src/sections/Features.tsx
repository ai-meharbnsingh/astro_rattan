import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Star, Calendar, BookOpen, Sparkles, Compass, ChevronRight, Layers } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

const features = [
  {
    icon: Star,
    title: '21 Kundli Engines',
    desc: 'Parashari + Jaimini + KP System. Divisional charts (D1–D60), Shadbala, Ashtakvarga, Yogini Dasha — depth no app matches.',
    route: '/kundli',
  },
  {
    icon: Calendar,
    title: 'Live Panchang',
    desc: 'Tithi, Nakshatra, Yoga, Karana with exact end times. Rahu Kaal, Choghadiya, Muhurat finder — location-aware.',
    route: '/panchang',
  },
  {
    icon: BookOpen,
    title: 'Lal Kitab Remedies',
    desc: 'Full Lal Kitab system with personalized remedies, house analysis, and annual predictions — rarely found in apps.',
    route: '/lal-kitab',
  },
  {
    icon: Sparkles,
    title: 'Dosha + Yoga Detection',
    desc: 'Mangal, Kaal Sarp, Sade Sati, Pitra, Kemdrum Dosha. Plus Gajakesari, Budhaditya, Panch Mahapurusha Yogas.',
    route: '/kundli',
  },
  {
    icon: Layers,
    title: 'Varshphal + Transits',
    desc: 'Solar Return with Muntha & Mudda Dasha. Live Gochara transit tracking from your natal Moon.',
    route: '/kundli',
  },
  {
    icon: Compass,
    title: 'Numerology + Loshu Grid',
    desc: 'Life Path, Destiny, Soul Urge numbers. Mobile number analysis with Vedic Grid and compatibility.',
    route: '/numerology',
  },
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
    <section ref={sectionRef} id="features" className="relative py-24 bg-cosmic-bg">
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-sacred-gold-dark/50 to-transparent" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="features-title text-center mb-16">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-['Cinzel_Decorative'] text-cosmic-text mb-4">
            Built Different
          </h2>
          <p className="text-cosmic-text/60 max-w-2xl mx-auto">
            Bridging Ancient Wisdom with Modern Technology
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card
                key={index}
                className="feature-card group relative bg-cosmic-bg border border-sacred-gold/20 hover:border-sacred-gold/50 transition-all duration-300 hover:-translate-y-1 cursor-pointer"
                onClick={() => navigate(feature.route)}
              >
                <CardContent className="relative p-6">
                  <div className="w-14 h-14 flex items-center justify-center mb-4 bg-sacred-gold-dark/10 border border-sacred-gold/20 group-hover:scale-110 transition-transform">
                    <Icon className="w-7 h-7 text-sacred-gold-dark" />
                  </div>
                  <h3 className="text-lg font-cinzel font-semibold text-cosmic-text mb-2 uppercase tracking-wide">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-cosmic-text/60 leading-relaxed">{feature.desc}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="features-title mt-16 text-center">
          <button
            onClick={() => navigate('/login')}
            className="inline-flex items-center gap-2 bg-transparent border border-sacred-gold text-sacred-gold-dark hover:bg-sacred-gold-dark hover:text-cosmic-bg transition-all px-8 py-4 text-xs font-cinzel tracking-[3px] uppercase"
          >
            Sign In to Explore
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-sacred-gold-dark/30 to-transparent" />
    </section>
  );
}
