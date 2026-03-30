import { useNavigate } from 'react-router-dom';
import { Hash, CreditCard, Search, BookOpen, Sparkles } from 'lucide-react';

const links = [
  { icon: Hash, label: 'Numerology', path: '/numerology' },
  { icon: CreditCard, label: 'Tarot', path: '/numerology' },
  { icon: Search, label: 'KP Astrology', path: '/kp-lalkitab' },
  { icon: BookOpen, label: 'Lal Kitab', path: '/kp-lalkitab' },
  { icon: Sparkles, label: 'Remedies', path: '/kp-lalkitab' },
];

export default function ExactQuickLinks() {
  const navigate = useNavigate();

  return (
    <section className="py-6 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Decorative divider */}
        <div className="flex items-center justify-center mb-6">
          <div className="flex-1 h-px" style={{ background: 'linear-gradient(to right, transparent, #D4A052, transparent)' }} />
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3">
          {links.map((link) => (
            <button
              key={link.label}
              onClick={() => navigate(link.path)}
              className="flex items-center gap-2.5 px-5 py-2.5 rounded-full text-sm font-serif font-medium
                         border transition-all duration-200 hover:-translate-y-0.5"
              style={{
                background: '#FFF8EE',
                borderColor: '#D4A052',
                color: '#3D2B1F',
                boxShadow: '0 2px 6px rgba(139, 105, 20, 0.08)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'linear-gradient(to right, #D4A052, #B8860B)';
                e.currentTarget.style.color = 'white';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(139, 105, 20, 0.2)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = '#FFF8EE';
                e.currentTarget.style.color = '#3D2B1F';
                e.currentTarget.style.boxShadow = '0 2px 6px rgba(139, 105, 20, 0.08)';
              }}
            >
              <link.icon className="w-4 h-4" />
              {link.label}
            </button>
          ))}
        </div>

        {/* Decorative divider */}
        <div className="flex items-center justify-center mt-6">
          <div className="flex-1 h-px" style={{ background: 'linear-gradient(to right, transparent, #D4A052, transparent)' }} />
        </div>
      </div>
    </section>
  );
}
