import { Card, CardContent } from '@/components/ui/card';
import { Globe } from 'lucide-react';
import InteractiveKundli from '@/components/InteractiveKundli';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign } from '@/lib/backend-translations';

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

function formatDegree(degree: number): string {
  const deg = Math.floor(degree);
  const min = Math.round((degree - deg) * 60);
  return `${deg}\u00B0${min.toString().padStart(2, '0')}'`;
}

function PlanetaryPositions({ planets }: PlanetaryPositionsProps) {
  const { language } = useTranslation();
  // Build chart data for InteractiveKundli
  const chartPlanets = planets.map(p => ({
    planet: p.name,
    sign: p.rashi,
    house: (p.rashi_index || 0) + 1,
    nakshatra: '',
    sign_degree: p.degree,
    status: '',
  }));

  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <Globe className="w-5 h-5 text-sacred-gold" />
          <h3 className="text-cosmic-text font-semibold text-lg">
            {t('auto.planetaryPositionsNa')}
          </h3>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Kundli Chart */}
          <div className="flex justify-center">
            <InteractiveKundli
              chartData={{ planets: chartPlanets }}
              onPlanetClick={() => {}}
              onHouseClick={() => {}}
            />
          </div>

          {/* Table with degrees */}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-sacred-gold/10">
                  <th className="p-2 text-left text-sacred-gold-dark">{t('auto.planet')}</th>
                  <th className="p-2 text-left text-sacred-gold-dark">{t('auto.rashi')}</th>
                  <th className="p-2 text-right text-sacred-gold-dark">{t('auto.degree')}</th>
                  <th className="p-2 text-right text-sacred-gold-dark">{t('auto.longitude')}</th>
                </tr>
              </thead>
              <tbody>
                {planets.map(p => (
                  <tr key={p.name} className="border-t border-sacred-gold/10">
                    <td className="p-2 text-cosmic-text font-medium">{translatePlanet(p.name, language)}</td>
                    <td className="p-2 text-cosmic-text">{translateSign(p.rashi, language)}</td>
                    <td className="p-2 text-right text-gray-600">{formatDegree(p.degree)}</td>
                    <td className="p-2 text-right text-gray-500">{p.longitude?.toFixed(2)}°</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default PlanetaryPositions;
