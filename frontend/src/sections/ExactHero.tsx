import { useNavigate } from 'react-router-dom';
import { Sparkles, Calendar, Heart, Clock, BookOpen, ChevronRight } from 'lucide-react';

const services = [
  {
    icon: Sparkles,
    emoji: '\u2728',
    title: 'Kundli\nGeneration',
    subtitle: 'Generate your\nVedic Birth Chart',
    cta: 'Start Kundli',
    path: '/kundli',
  },
  {
    icon: Calendar,
    emoji: '\uD83D\uDCC5',
    title: 'Horoscope',
    subtitle: 'Daily Monthly\nYearly',
    cta: 'Read Now',
    path: '/horoscope',
  },
  {
    icon: Heart,
    emoji: '\u2764\uFE0F',
    title: 'Kundli\nMatching',
    subtitle: 'Marriage\nCompatibility Check',
    cta: 'Check Match',
    path: '/kundli',
  },
  {
    icon: Clock,
    emoji: '\uD83D\uDD52',
    title: 'Muhurat\nFinder',
    subtitle: 'Find Auspicious\nDates & Timings',
    cta: 'Search',
    path: '/panchang',
  },
  {
    icon: BookOpen,
    emoji: '\uD83D\uDCDA',
    title: 'Spiritual\nLibrary',
    subtitle: 'Bhagavad Gita,\nMantras, Aarti, Chalisa...',
    cta: 'Explore',
    path: '/library',
  },
];

export default function ExactHero() {
  const navigate = useNavigate();

  return (
    <section className="pt-20 pb-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Decorative top ornament */}
        <div className="flex items-center justify-center mb-6">
          <div className="h-px w-16 bg-gradient-to-r from-transparent to-[#D4A052]" />
          <span className="mx-3 text-[#8B6914] text-sm font-serif tracking-widest uppercase">Our Services</span>
          <div className="h-px w-16 bg-gradient-to-l from-transparent to-[#D4A052]" />
        </div>

        {/* 5 Service Cards */}
        <div className="flex flex-col sm:flex-row flex-wrap lg:flex-nowrap justify-center gap-4">
          {services.map((service) => (
            <div
              key={service.title}
              onClick={() => navigate(service.path)}
              className="group w-full sm:w-[calc(50%-8px)] lg:w-[200px] xl:w-[210px] rounded-xl p-5
                         border cursor-pointer flex flex-col items-center text-center
                         transition-all duration-300 hover:-translate-y-1"
              style={{
                background: '#FFF8EE',
                borderColor: '#D4A052',
                boxShadow: '0 2px 8px rgba(139, 105, 20, 0.08)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = '0 8px 24px rgba(139, 105, 20, 0.18)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = '0 2px 8px rgba(139, 105, 20, 0.08)';
              }}
            >
              {/* Icon */}
              <div className="w-14 h-14 rounded-full flex items-center justify-center mb-3"
                   style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)', border: '2px solid #D4A052' }}>
                <service.icon className="w-6 h-6" style={{ color: '#8B6914' }} />
              </div>

              {/* Title */}
              <h3 className="font-serif font-bold text-base mb-1 whitespace-pre-line leading-tight"
                  style={{ color: '#3D2B1F' }}>
                {service.title}
              </h3>

              {/* Subtitle */}
              <p className="text-xs mb-4 whitespace-pre-line leading-relaxed flex-grow"
                 style={{ color: '#7A6548' }}>
                {service.subtitle}
              </p>

              {/* CTA Button */}
              <button className="w-full py-2 px-4 rounded-full text-white text-sm font-medium
                               flex items-center justify-center gap-1.5 transition-all duration-200"
                      style={{ background: 'linear-gradient(to right, #D4A052, #B8860B)' }}>
                {service.cta}
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
