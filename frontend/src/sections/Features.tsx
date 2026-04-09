import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { ChevronRight } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const features = [
  {
    title: '21 Kundli Engines',
    desc: 'Parashari + Jaimini + KP System. Divisional charts (D1-D60), Shadbala, Ashtakvarga, Yogini Dasha — depth no app matches.',
    img: 'https://images.unsplash.com/photo-1630694093867-4b947d812bf0?w=600&h=400&fit=crop&q=90',
  },
  {
    title: 'Live Panchang',
    desc: 'Tithi, Nakshatra, Yoga, Karana with exact end times. Rahu Kaal, Choghadiya, Muhurat finder — location-aware.',
    img: 'https://images.unsplash.com/photo-1545156521-77bd85671d30?w=600&h=400&fit=crop&q=90',
  },
  {
    title: 'Lal Kitab Remedies',
    desc: 'Full Lal Kitab system with personalized remedies, house analysis, and annual predictions — rarely found in apps.',
    img: 'https://images.unsplash.com/photo-1604881991720-f91add269bed?w=600&h=400&fit=crop&q=90',
  },
  {
    title: 'Dosha + Yoga Detection',
    desc: 'Mangal, Kaal Sarp, Sade Sati, Pitra, Kemdrum Dosha. Plus Gajakesari, Budhaditya, Panch Mahapurusha Yogas.',
    img: 'https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=600&h=400&fit=crop&q=90',
  },
  {
    title: 'Varshphal + Transits',
    desc: 'Solar Return with Muntha & Mudda Dasha. Live Gochara transit tracking from your natal Moon.',
    img: 'https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=600&h=400&fit=crop&q=90',
  },
  {
    title: 'Numerology + Loshu Grid',
    desc: 'Life Path, Destiny, Soul Urge numbers. Mobile number analysis with Vedic Grid and compatibility.',
    img: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&h=400&fit=crop&q=90',
  },
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
    <section ref={sectionRef} id="features" className="relative pt-4 pb-24 bg-cosmic-bg">

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="features-title text-center mb-16">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-['Cinzel_Decorative'] text-cosmic-text mb-6">
            Bridging Ancient Wisdom with Modern Technology
          </h2>
          <div className="max-w-3xl mx-auto space-y-4 text-cosmic-text">
            <p>
              Most astrology apps use lookup tables and generic predictions. Astro Rattan computes every position from Swiss Ephemeris — the same library used by research astronomers — accurate to arc-seconds.
            </p>
            <p>
              Three complete astrological systems in one app: <strong className="text-sacred-gold-dark">Parashari</strong> (classical Vedic), <strong className="text-sacred-gold-dark">Jaimini</strong> (Chara Karakas, special lagnas), and <strong className="text-sacred-gold-dark">KP System</strong> (Krishnamurti Paddhati with sub-lord analysis). Plus full <strong className="text-sacred-gold-dark">Lal Kitab</strong> remedies and <strong className="text-sacred-gold-dark">Numerology</strong>.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card
              key={index}
              className="feature-card group relative bg-cosmic-bg border border-sacred-gold/20 overflow-hidden"
            >
              <div className="h-40 overflow-hidden">
                <img
                  src={feature.img}
                  alt={feature.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  loading="lazy"
                />
                <div className="absolute inset-0 h-40 bg-gradient-to-t from-cosmic-bg via-cosmic-bg/40 to-transparent" />
              </div>
              <CardContent className="relative p-6 pt-2">
                <h3 className="text-lg font-cinzel font-semibold text-cosmic-text mb-2 uppercase tracking-wide">
                  {feature.title}
                </h3>
                <p className="text-base text-cosmic-text leading-relaxed">{feature.desc}</p>
              </CardContent>
            </Card>
          ))}
        </div>

      </div>

    </section>
  );
}
