import { Sun, Moon, CircleDot, Orbit } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

// Planet colors for styling
const PLANET_COLORS: Record<string, string> = {
  Sun: 'text-orange-500',
  Moon: 'text-slate-300',
  Mars: 'text-red-500',
  Mercury: 'text-green-500',
  Jupiter: 'text-yellow-500',
  Venus: 'text-pink-400',
  Saturn: 'text-blue-400',
  Rahu: 'text-purple-500',
  Ketu: 'text-gray-400',
};

const PLANET_BG_COLORS: Record<string, string> = {
  Sun: 'bg-orange-500/10',
  Moon: 'bg-slate-300/10',
  Mars: 'bg-red-500/10',
  Mercury: 'bg-green-500/10',
  Jupiter: 'bg-yellow-500/10',
  Venus: 'bg-pink-400/10',
  Saturn: 'bg-blue-400/10',
  Rahu: 'bg-purple-500/10',
  Ketu: 'bg-gray-400/10',
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
      {/* Sun and Moon Signs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <div className="rounded-lg border border-orange-500/30 p-2">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-orange-500/10">
              <Sun className="h-5 w-5 text-orange-500" />
            </div>
            <div>
              <p className="text-sm text-cosmic-text-secondary">
                {language === 'hi' ? 'सूर्य राशि' : 'Sun Sign'}
              </p>
              <h3 className="text-xl font-bold text-cosmic-text-primary">
                {language === 'hi' && panchang.sun_sign
                  ? translateRashiToHindi(panchang.sun_sign)
                  : panchang.sun_sign || '--'}
              </h3>
            </div>
            {(() => {
              const sunPlanet = planets.find(p => p.name === 'Sun');
              if (sunPlanet) {
                return (
                  <div className="ml-auto text-xs text-cosmic-text-secondary text-right">
                    <p>{sunPlanet.degree}°</p>
                    <p>{sunPlanet.longitude}°</p>
                  </div>
                );
              }
              return null;
            })()}
          </div>
        </div>

        <div className="rounded-lg border border-slate-400/30 p-2">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-slate-300/10">
              <Moon className="h-5 w-5 text-slate-300" />
            </div>
            <div>
              <p className="text-sm text-cosmic-text-secondary">
                {language === 'hi' ? 'चंद्र राशि' : 'Moon Sign'}
              </p>
              <h3 className="text-xl font-bold text-cosmic-text-primary">
                {language === 'hi' && panchang.moon_sign
                  ? translateRashiToHindi(panchang.moon_sign)
                  : panchang.moon_sign || '--'}
              </h3>
            </div>
            {(() => {
              const moonPlanet = planets.find(p => p.name === 'Moon');
              if (moonPlanet) {
                return (
                  <div className="ml-auto text-xs text-cosmic-text-secondary text-right">
                    <p>{moonPlanet.degree}°</p>
                    <p>{panchang.nakshatra?.name}</p>
                  </div>
                );
              }
              return null;
            })()}
          </div>
        </div>
      </div>

      {/* Navgraha Grid */}
      <div className="rounded-lg border border-cosmic-border p-2">
        <h3 className="font-bold text-cosmic-text-primary mb-2 flex items-center gap-1">
          <Orbit className="h-4 w-4 text-sacred-gold" />
          {language === 'hi' ? 'नवग्रह स्थिति' : 'Navgraha Positions (Planetary Positions)'}
        </h3>

        <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 gap-2">
          {planets.map((planet) => {
            const colorClass = PLANET_COLORS[planet.name] || 'text-gray-400';
            const bgClass = PLANET_BG_COLORS[planet.name] || 'bg-gray-400/10';
            const hindiName = PLANET_HINDI[planet.name] || planet.name;

            return (
              <div
                key={planet.name}
                className={`p-2 rounded-lg ${bgClass} text-center`}
              >
                <div className="flex items-center justify-center gap-1 mb-1">
                  <CircleDot className={`h-3 w-3 ${colorClass}`} />
                  <span className="font-semibold text-cosmic-text-primary text-sm">
                    {language === 'hi' ? hindiName : planet.name}
                  </span>
                </div>
                <p className="font-bold text-cosmic-text-primary">
                  {language === 'hi' && planet.rashi_hindi
                    ? planet.rashi_hindi
                    : planet.rashi}
                </p>
                <p className="text-xs text-cosmic-text-secondary">
                  {planet.degree}°
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Position Table */}
      <div className="rounded-lg border border-cosmic-border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-cosmic-border bg-cosmic-card/30">
                <th className="text-left py-1 px-2 text-cosmic-text-secondary font-medium">
                  {language === 'hi' ? 'ग्रह' : 'Planet'}
                </th>
                <th className="text-left py-1 px-2 text-cosmic-text-secondary font-medium">
                  {language === 'hi' ? 'राशि' : 'Sign'}
                </th>
                <th className="text-right py-1 px-2 text-cosmic-text-secondary font-medium">
                  {language === 'hi' ? 'अंश' : 'Degree'}
                </th>
                <th className="text-right py-1 px-2 text-cosmic-text-secondary font-medium">
                  {language === 'hi' ? 'दीर्घांश' : 'Longitude'}
                </th>
              </tr>
            </thead>
            <tbody>
              {planets.map((planet, index) => (
                <tr
                  key={planet.name}
                  className={`border-b border-cosmic-border/50 last:border-0 ${index % 2 === 0 ? 'bg-cosmic-card/30' : ''}`}
                >
                  <td className="py-1 px-2 font-medium text-cosmic-text-primary">
                    <span className={`inline-block w-2 h-2 rounded-full mr-1 ${PLANET_BG_COLORS[planet.name]?.replace('/10', '')}`} />
                    {language === 'hi' ? PLANET_HINDI[planet.name] || planet.name : planet.name}
                  </td>
                  <td className="py-1 px-2 text-cosmic-text-secondary">
                    {language === 'hi' && planet.rashi_hindi ? planet.rashi_hindi : planet.rashi}
                  </td>
                  <td className="py-1 px-2 text-right text-cosmic-text-secondary">
                    {planet.degree}°
                  </td>
                  <td className="py-1 px-2 text-right text-cosmic-text-secondary">
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

// Helper to translate rashi names
function translateRashiToHindi(rashi: string): string {
  const translations: Record<string, string> = {
    'Aries': 'मेष',
    'Taurus': 'वृषभ',
    'Gemini': 'मिथुन',
    'Cancer': 'कर्क',
    'Leo': 'सिंह',
    'Virgo': 'कन्या',
    'Libra': 'तुला',
    'Scorpio': 'वृश्चिक',
    'Sagittarius': 'धनु',
    'Capricorn': 'मकर',
    'Aquarius': 'कुंभ',
    'Pisces': 'मीन',
  };
  return translations[rashi] || rashi;
}
