import { Card, CardContent } from '@/components/ui/card';
import { Globe } from 'lucide-react';

interface Planet {
  name: string;
  longitude: number;
  degree: number;
  rashi: string;
  rashi_index: number;
}

interface PlanetaryPositionsProps {
  planets: Planet[];
}

const PLANET_COLORS: Record<string, string> = {
  Sun: 'bg-amber-400',
  Moon: 'bg-blue-300',
  Mars: 'bg-red-400',
  Mercury: 'bg-green-400',
  Jupiter: 'bg-yellow-400',
  Venus: 'bg-pink-400',
  Saturn: 'bg-purple-400',
  Rahu: 'bg-gray-400',
  Ketu: 'bg-gray-500',
};

function formatDegree(degree: number): string {
  const deg = Math.floor(degree);
  const min = Math.round((degree - deg) * 60);
  return `${deg}\u00B0${min.toString().padStart(2, '0')}'`;
}

function PlanetaryPositions({ planets }: PlanetaryPositionsProps) {
  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <Globe className="w-5 h-5 text-sacred-gold" />
          <h3 className="text-cosmic-text font-semibold text-lg">
            Planetary Positions (Navgraha)
          </h3>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {planets.map((planet) => (
            <div
              key={planet.name}
              className="p-3 rounded-xl bg-cosmic-card border border-sacred-gold/10 flex items-center gap-3"
            >
              <span
                className={`inline-block w-3 h-3 rounded-full shrink-0 ${PLANET_COLORS[planet.name] ?? 'bg-gray-400'}`}
              />
              <div className="min-w-0">
                <div className="text-sm font-medium text-cosmic-text">
                  {planet.name}
                </div>
                <div className="text-xs text-cosmic-text-secondary">
                  {formatDegree(planet.degree)}
                </div>
                <span className="inline-block mt-1 text-xs font-medium px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold">
                  {planet.rashi}
                </span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export default PlanetaryPositions;
