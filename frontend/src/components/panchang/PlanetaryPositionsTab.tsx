import { Orbit } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

const PLANET_DOT_BG: Record<string, string> = {
  Sun: 'bg-orange-500',
  Moon: 'bg-slate-300',
  Mars: 'bg-red-500',
  Mercury: 'bg-green-500',
  Jupiter: 'bg-yellow-500',
  Venus: 'bg-pink-400',
  Saturn: 'bg-blue-400',
  Rahu: 'bg-purple-500',
  Ketu: 'bg-gray-400',
};

// Hindi names for planets
const PLANET_HINDI: Record<string, string> = {
  Sun: 'सूर्य',
  Moon: 'चंद्र',
  Mars: 'मंगल',
  Mercury: 'बुध',
  Jupiter: 'गुरु',
  Venus: 'शुक्र',
  Saturn: 'शनि',
  Rahu: 'राहु',
  Ketu: 'केतु',
};

export default function PlanetaryPositionsTab({ panchang, language, t }: Props) {
  const planets = panchang.planetary_positions || [];

  return (
    <div className="space-y-3">
      <div className="rounded-lg border border-cosmic-border p-2">
        <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
          <Orbit className="h-4 w-4 text-sacred-gold" />
          {language === 'hi' ? 'नवग्रह स्थिति' : 'Navgraha Positions (Planetary Positions)'}
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[680px] text-sm">
            <thead>
              <tr className="bg-sacred-gold/15">
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'ग्रह' : 'Planet'}
                </th>
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'राशि' : 'Sign'}
                </th>
                <th className="text-right px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'अंश' : 'Degree'}
                </th>
                <th className="text-right px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'दीर्घांश' : 'Longitude'}
                </th>
              </tr>
            </thead>
            <tbody>
              {planets.map((planet) => (
                <tr
                  key={planet.name}
                  className="border-b border-cosmic-border/50 last:border-0"
                >
                  <td className="px-2 py-1 font-medium text-cosmic-text-primary">
                    <span className={`inline-block w-2 h-2 rounded-full mr-1 ${PLANET_DOT_BG[planet.name] || 'bg-gray-400'}`} />
                    {language === 'hi' ? PLANET_HINDI[planet.name] || planet.name : planet.name}
                  </td>
                  <td className="px-2 py-1 text-cosmic-text-secondary">
                    {language === 'hi' && planet.rashi_hindi ? planet.rashi_hindi : planet.rashi}
                  </td>
                  <td className="px-2 py-1 text-right text-cosmic-text-secondary">
                    {planet.degree}°
                  </td>
                  <td className="px-2 py-1 text-right text-cosmic-text-secondary">
                    {planet.longitude}°
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
