import { Card, CardContent } from '@/components/ui/card';
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
    <div className="space-y-6">
      {/* Sun and Moon Signs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card className="card-sacred border-orange-500/30">
          <CardContent className="p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-3 rounded-xl bg-orange-500/10">
                <Sun className="h-6 w-6 text-orange-500" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">
                  {language === 'hi' ? 'सूर्य राशि' : 'Sun Sign'}
                </p>
                <h3 className="text-2xl font-bold text-cosmic-text-primary">
                  {language === 'hi' && panchang.sun_sign 
                    ? translateRashiToHindi(panchang.sun_sign) 
                    : panchang.sun_sign || '--'}
                </h3>
              </div>
            </div>
            {(() => {
              const sunPlanet = planets.find(p => p.name === 'Sun');
              if (sunPlanet) {
                return (
                  <div className="text-sm text-cosmic-text-secondary">
                    <p>{language === 'hi' ? 'अंश' : 'Degree'}: {sunPlanet.degree}°</p>
                    <p>{language === 'hi' ? 'दीर्घांश' : 'Longitude'}: {sunPlanet.longitude}°</p>
                  </div>
                );
              }
              return null;
            })()}
          </CardContent>
        </Card>

        <Card className="card-sacred border-slate-400/30">
          <CardContent className="p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-3 rounded-xl bg-slate-300/10">
                <Moon className="h-6 w-6 text-slate-300" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">
                  {language === 'hi' ? 'चंद्र राशि' : 'Moon Sign'}
                </p>
                <h3 className="text-2xl font-bold text-cosmic-text-primary">
                  {language === 'hi' && panchang.moon_sign 
                    ? translateRashiToHindi(panchang.moon_sign) 
                    : panchang.moon_sign || '--'}
                </h3>
              </div>
            </div>
            {(() => {
              const moonPlanet = planets.find(p => p.name === 'Moon');
              if (moonPlanet) {
                return (
                  <div className="text-sm text-cosmic-text-secondary">
                    <p>{language === 'hi' ? 'अंश' : 'Degree'}: {moonPlanet.degree}°</p>
                    <p>{language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}: {panchang.nakshatra?.name}</p>
                  </div>
                );
              }
              return null;
            })()}
          </CardContent>
        </Card>
      </div>

      {/* Navgraha Grid */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <h3 className="text-lg font-bold text-cosmic-text-primary mb-4 flex items-center gap-2">
            <Orbit className="h-5 w-5 text-sacred-gold" />
            {language === 'hi' ? 'नवग्रह स्थिति' : 'Navgraha Positions (Planetary Positions)'}
          </h3>
          
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            {planets.map((planet) => {
              const colorClass = PLANET_COLORS[planet.name] || 'text-gray-400';
              const bgClass = PLANET_BG_COLORS[planet.name] || 'bg-gray-400/10';
              const hindiName = PLANET_HINDI[planet.name] || planet.name;
              
              return (
                <div 
                  key={planet.name} 
                  className={`p-4 rounded-xl ${bgClass} border border-transparent hover:border-sacred-gold/30 transition-all`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <CircleDot className={`h-4 w-4 ${colorClass}`} />
                    <span className="font-semibold text-cosmic-text-primary">
                      {language === 'hi' ? hindiName : planet.name}
                    </span>
                  </div>
                  <p className="text-lg font-bold text-cosmic-text-primary">
                    {language === 'hi' && planet.rashi_hindi 
                      ? planet.rashi_hindi 
                      : planet.rashi}
                  </p>
                  <p className="text-xs text-cosmic-text-secondary">
                    {planet.degree}° {language === 'hi' ? 'अंश' : 'deg'}
                  </p>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Position Table */}
      <Card className="card-sacred">
        <CardContent className="p-4 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-cosmic-border">
                <th className="text-left py-2 px-3 text-cosmic-text-secondary font-medium">
                  {language === 'hi' ? 'ग्रह' : 'Planet'}
                </th>
                <th className="text-left py-2 px-3 text-cosmic-text-secondary font-medium">
                  {language === 'hi' ? 'राशि' : 'Sign'}
                </th>
                <th className="text-right py-2 px-3 text-cosmic-text-secondary font-medium">
                  {language === 'hi' ? 'अंश' : 'Degree'}
                </th>
                <th className="text-right py-2 px-3 text-cosmic-text-secondary font-medium">
                  {language === 'hi' ? 'दीर्घांश' : 'Longitude'}
                </th>
              </tr>
            </thead>
            <tbody>
              {planets.map((planet, index) => (
                <tr 
                  key={planet.name} 
                  className={index % 2 === 0 ? 'bg-cosmic-card/30' : ''}
                >
                  <td className="py-2 px-3 font-medium text-cosmic-text-primary">
                    <span className={`inline-block w-2 h-2 rounded-full mr-2 ${PLANET_BG_COLORS[planet.name]?.replace('/10', '')}`} />
                    {language === 'hi' ? PLANET_HINDI[planet.name] || planet.name : planet.name}
                  </td>
                  <td className="py-2 px-3 text-cosmic-text-secondary">
                    {language === 'hi' && planet.rashi_hindi ? planet.rashi_hindi : planet.rashi}
                  </td>
                  <td className="py-2 px-3 text-right text-cosmic-text-secondary">
                    {planet.degree}°
                  </td>
                  <td className="py-2 px-3 text-right text-cosmic-text-secondary">
                    {planet.longitude}°
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
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
