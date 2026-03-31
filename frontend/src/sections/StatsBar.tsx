import { statsData } from '../config';
import { TrendingUp, Users, Star, Shield, Zap } from 'lucide-react';

const iconMap: Record<string, React.ReactNode> = {
  '📊': <TrendingUp className="w-5 h-5 text-amber-600" />,
  '👨‍🦳': <Users className="w-5 h-5 text-amber-600" />,
  '⭐': <Star className="w-5 h-5 text-amber-600" />,
  '✓': <Shield className="w-5 h-5 text-amber-600" />,
  '⚡': <Zap className="w-5 h-5 text-amber-600" />,
};

export default function StatsBar() {
  return (
    <section className="py-6 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="vedic-card py-4 px-6">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 md:gap-6">
            {statsData.map((stat, index) => (
              <div
                key={stat.id}
                className={`flex items-center gap-3 ${
                  index < statsData.length - 1 ? 'md:border-r md:border-amber-300/50' : ''
                }`}
              >
                {/* Icon */}
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center border border-amber-300">
                  {iconMap[stat.icon]}
                </div>
                
                {/* Text */}
                <div className="flex flex-col">
                  <span className="stat-number text-lg">{stat.value}</span>
                  <span className="stat-label">{stat.label}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
