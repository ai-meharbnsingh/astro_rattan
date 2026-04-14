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
  const sunPlanet = planets.find((p) => p.name === 'Sun');
  const moonPlanet = planets.find((p) => p.name === 'Moon');

  const summaryRows = [
    {
      item: language === 'hi' ? 'सूर्य राशि' : 'Sun Sign',
      value: language === 'hi' && panchang.sun_sign ? translateRashiToHindi(panchang.sun_sign) : panchang.sun_sign || '--',
      details: sunPlanet ? `${language === 'hi' ? 'अंश' : 'Degree'}: ${sunPlanet.degree}°` : '--',
      extra: sunPlanet ? `${language === 'hi' ? 'दीर्घांश' : 'Longitude'}: ${sunPlanet.longitude}°` : '--',
    },
    {
      item: language === 'hi' ? 'चंद्र राशि' : 'Moon Sign',
      value: language === 'hi' && panchang.moon_sign ? translateRashiToHindi(panchang.moon_sign) : panchang.moon_sign || '--',
      details: moonPlanet ? `${language === 'hi' ? 'अंश' : 'Degree'}: ${moonPlanet.degree}°` : '--',
      extra: `${language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}: ${language === 'hi' ? panchang.nakshatra?.name_hindi || panchang.nakshatra?.name || '--' : panchang.nakshatra?.name || '--'}`,
    },
  ];

  return (
    <div className="space-y-3">
      <div className="rounded-lg border border-cosmic-border p-2">
        <h3 className="font-bold text-cosmic-text-primary mb-1">
          {language === 'hi' ? 'सूर्य / चंद्र सारांश' : 'Sun / Moon Summary'}
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[680px] text-sm">
            <thead>
              <tr className="bg-sacred-gold/15">
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">{language === 'hi' ? 'विषय' : 'Item'}</th>
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">{language === 'hi' ? 'मान' : 'Value'}</th>
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">{language === 'hi' ? 'विवरण' : 'Details'}</th>
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">{language === 'hi' ? 'अतिरिक्त' : 'Extra'}</th>
              </tr>
            </thead>
            <tbody>
              {summaryRows.map((row) => (
                <tr key={row.item} className="border-b border-cosmic-border/50 last:border-0">
                  <td className="px-2 py-1 font-medium text-cosmic-text-primary">{row.item}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{row.value}</td>
                  <td className="px-2 py-1 text-cosmic-text-secondary">{row.details}</td>
                  <td className="px-2 py-1 text-cosmic-text-secondary">{row.extra}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

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
