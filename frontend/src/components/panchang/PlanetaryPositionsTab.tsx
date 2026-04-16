import { Orbit } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

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

// Hindi names for signs (rashi)
const RASHI_HINDI: Record<string, string> = {
  'Aries': 'मेष', 'Taurus': 'वृषभ', 'Gemini': 'मिथुन', 'Cancer': 'कर्क',
  'Leo': 'सिंह', 'Virgo': 'कन्या', 'Libra': 'तुला', 'Scorpio': 'वृश्चिक',
  'Sagittarius': 'धनु', 'Capricorn': 'मकर', 'Aquarius': 'कुंभ', 'Pisces': 'मीन',
};

export default function PlanetaryPositionsTab({ panchang, language, t }: Props) {
  const planets = panchang.planetary_positions || [];

  return (
    <div className="space-y-3">
      <div className="rounded-lg border p-2">
        <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
          <Orbit className="h-4 w-4 text-sacred-gold" />
          {t('auto.navgrahaPositionsPla')}
        </h3>
        <div className="overflow-x-auto">
          <Table className="w-full min-w-[680px] text-sm">
            <TableHeader>
              <TableRow className="bg-sacred-gold/15">
                <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {t('auto.planet')}
                </TableHead>
                <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {t('auto.sign')}
                </TableHead>
                <TableHead className="text-right px-2 py-1 text-sacred-gold-dark font-semibold">
                  {t('auto.degree')}
                </TableHead>
                <TableHead className="text-right px-2 py-1 text-sacred-gold-dark font-semibold">
                  {t('auto.longitude')}
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {planets.map((planet) => (
                <TableRow
                  key={planet.name}
                  className="border-b border/50 last:border-0"
                >
                  <TableCell className="px-2 py-1 font-medium text-foreground">
                    <span className={`inline-block w-2 h-2 rounded-full mr-1 ${PLANET_DOT_BG[planet.name] || 'bg-gray-400'}`} />
                    {language === 'hi' ? PLANET_HINDI[planet.name] || planet.name : planet.name}
                  </TableCell>
                  <TableCell className="px-2 py-1 text-muted-foreground">
                    {language === 'hi' ? RASHI_HINDI[planet.rashi] || planet.rashi : planet.rashi}
                  </TableCell>
                  <TableCell className="px-2 py-1 text-right text-muted-foreground">
                    {planet.degree}°
                  </TableCell>
                  <TableCell className="px-2 py-1 text-right text-muted-foreground">
                    {planet.longitude}°
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