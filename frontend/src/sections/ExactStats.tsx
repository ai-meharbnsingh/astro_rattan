import { Users, Award, Star, ShieldCheck } from 'lucide-react';

const stats = [
  { icon: Users, value: '500,000+', label: 'Kundli Generated' },
  { icon: Award, value: '120+', label: 'Expert Astrologers' },
  { icon: Star, value: '4.9/5', label: 'Trusted Since 1998' },
  { icon: ShieldCheck, value: '100%', label: 'Certified & Energized' },
];

export default function ExactStats() {
  return (
    <section className="py-5 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Decorative divider above */}
        <div className="flex items-center justify-center mb-5">
          <div className="flex-1 h-px" style={{ background: 'linear-gradient(to right, transparent, #D4A052, transparent)' }} />
        </div>

        <div className="flex flex-wrap justify-center lg:justify-between items-center gap-8 lg:gap-4 py-2">
          {stats.map((stat, idx) => (
            <div key={stat.label} className="flex items-center gap-3">
              {/* Separator dot (not on first) */}
              {idx > 0 && (
                <span className="hidden lg:block w-1.5 h-1.5 rounded-full mr-4" style={{ background: '#D4A052' }} />
              )}
              <div className="w-10 h-10 flex items-center justify-center rounded-full"
                   style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)', border: '1.5px solid #D4A052' }}>
                <stat.icon className="w-5 h-5" style={{ color: '#8B6914' }} strokeWidth={1.5} />
              </div>
              <div>
                <div className="font-serif font-bold text-lg leading-none" style={{ color: '#8B6914' }}>
                  {stat.value}
                </div>
                <div className="text-xs mt-1" style={{ color: '#7A6548' }}>
                  {stat.label}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Decorative divider below */}
        <div className="flex items-center justify-center mt-5">
          <div className="flex-1 h-px" style={{ background: 'linear-gradient(to right, transparent, #D4A052, transparent)' }} />
        </div>
      </div>
    </section>
  );
}
