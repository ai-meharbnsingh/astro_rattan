import { Orbit } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";
import PanchangTabHeader from './PanchangTabHeader';

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

// Hindi names for planets (fallback when backend field missing)
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

// Hindi names for signs (fallback when backend field missing)
const RASHI_HINDI: Record<string, string> = {
  'Aries': 'मेष', 'Taurus': 'वृषभ', 'Gemini': 'मिथुन', 'Cancer': 'कर्क',
  'Leo': 'सिंह', 'Virgo': 'कन्या', 'Libra': 'तुला', 'Scorpio': 'वृश्चिक',
  'Sagittarius': 'धनु', 'Capricorn': 'मकर', 'Aquarius': 'कुंभ', 'Pisces': 'मीन',
};

/** Row background: retrograde = red tint, combusted = orange tint, both = red wins */
function rowBg(planet: { retrograde?: boolean; combusted?: boolean }): string {
  if (planet.retrograde) return 'bg-red-50';
  if (planet.combusted) return 'bg-orange-50';
  return '';
}

export default function PlanetaryPositionsTab({ panchang, language, t }: Props) {
  const planets = panchang.planetary_positions || [];

  return (
    <div className="space-y-4">
      <PanchangTabHeader
        icon={Orbit}
        title={language === 'hi' ? 'ग्रह स्थिति' : 'Planetary Positions'}
        description={language === 'hi'
          ? 'नवग्रह की राशि, नक्षत्र, अंश और वक्री/अस्त स्थिति — दैनिक पंचांग के अनुसार।'
          : 'Daily positions of the Navagraha with sign, nakshatra, degrees, and retrograde/combust status.'}
      />

      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
          <Orbit className="w-4 h-4" />
          <span>{t('auto.navgrahaPositionsPla')}</span>
        </div>
        <div className="overflow-x-auto">
          <Table className="w-full min-w-[640px] text-xs table-fixed">
            <TableHeader>
              <TableRow>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('auto.planet')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[16%]">{t('auto.sign')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[22%]">{language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}</TableHead>
                <TableHead className="text-right p-2 text-primary font-semibold uppercase tracking-wide w-[12%]">{t('auto.degree')}</TableHead>
                <TableHead className="text-right p-2 text-primary font-semibold uppercase tracking-wide w-[14%]">{t('auto.longitude')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[9%]">{language === 'hi' ? 'वक्री' : 'Retro'}</TableHead>
                <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[9%]">{language === 'hi' ? 'अस्त' : 'Combust'}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {planets.map((planet) => (
                <TableRow key={planet.name} className={`border-t border-border hover:bg-muted/5 ${rowBg(planet)}`}>
                  <TableCell className="p-2 font-medium text-foreground">
                    <span className={`inline-block w-2 h-2 rounded-full mr-2 align-middle ${PLANET_DOT_BG[planet.name] || 'bg-gray-400'}`} />
                    {language === 'hi'
                      ? (planet.name_hindi || PLANET_HINDI[planet.name] || planet.name)
                      : planet.name}
                  </TableCell>
                  <TableCell className="p-2 text-muted-foreground">
                    {language === 'hi'
                      ? (planet.rashi_hindi || RASHI_HINDI[planet.rashi] || planet.rashi)
                      : planet.rashi}
                  </TableCell>
                  <TableCell className="p-2 text-muted-foreground whitespace-normal break-words">
                    {planet.nakshatra
                      ? `${language === 'hi' && planet.nakshatra_hindi ? planet.nakshatra_hindi : planet.nakshatra}${planet.nakshatra_pada ? ` (${planet.nakshatra_pada})` : ''}`
                      : '—'}
                  </TableCell>
                  <TableCell className="p-2 text-right text-muted-foreground">{planet.degree}°</TableCell>
                  <TableCell className="p-2 text-right text-muted-foreground">{planet.longitude}°</TableCell>
                  <TableCell className="p-2 text-center">
                    {planet.retrograde
                      ? <span className="text-red-600 font-bold" title={language === 'hi' ? 'वक्री' : 'Retrograde'}>&#8478;</span>
                      : <span className="text-muted-foreground/40">—</span>}
                  </TableCell>
                  <TableCell className="p-2 text-center">
                    {planet.combusted
                      ? <span title={language === 'hi' ? 'अस्त' : 'Combust'}>🔥</span>
                      : <span className="text-muted-foreground/40">—</span>}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
