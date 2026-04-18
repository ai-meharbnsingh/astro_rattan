import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { translatePlanet, translateSign, translateNakshatra, translateBackend } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface KPTabProps {
  kpData: any;
  loadingKp: boolean;
  result: any;
  language: string;
  t: (key: string) => string;
}

export default function KPTab(props: KPTabProps) {
  const { kpData, loadingKp, result, language, t } = props;
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const planetShort = (name: string) => (translatePlanet(name || '', language) || name || '-').slice(0, 2);
  const planetList = (items: any[]) =>
    (items || []).map((x) => translatePlanet(String(x || ''), language)).join(', ');

  return (
    <div className="space-y-6">
      {loadingKp ? (
        <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-primary" /><span className="ml-2 text-foreground">{t('kundli.loadingKP')}</span></div>
      ) : kpData ? (
        <div className="space-y-6">
          {/* 1. KP Planet Table — full reference chart style */}
          <div className="bg-muted rounded-xl border border-border p-4">
            <Heading as={4} variant={4} className="mb-3">{t('auto.krishnamurtiPaddhati')}</Heading>
            <div className="overflow-x-auto">
              <Table className="w-full text-sm">
                <TableHeader><TableRow className="bg-muted">
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.planet')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">R/C</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.sign')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.degree')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">{t('kundli.pada')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.rashiLord')}>RL</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.nakshatraLord')}>NL</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.subLord')}>SL</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.subSubLord')}>SS</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.starLordOfSubLord')}>SSSL</TableHead>
                </TableRow></TableHeader>
                <TableBody>
                  {(kpData.planets || []).map((p: any) => (
                    <TableRow key={p.planet} className="border-t border-border">
                      <TableCell className="p-1.5 font-semibold text-foreground">{translatePlanet(p.planet, language)}</TableCell>
                      <TableCell className="p-1.5 text-center">{p.retrograde ? <span className="text-red-400 font-bold">{l('R', 'व')}</span> : ''}</TableCell>
                      <TableCell className="p-1.5 text-foreground">{translateSign(p.sign, language)}</TableCell>
                      <TableCell className="p-1.5 text-foreground font-mono">{p.degree_dms || (typeof p.degree === 'number' ? p.degree.toFixed(2) : p.degree)}</TableCell>
                      <TableCell className="p-1.5 text-foreground">{translateNakshatra(p.nakshatra, language) || '-'}</TableCell>
                      <TableCell className="p-1.5 text-center text-foreground">{p.pada || '-'}</TableCell>
                      <TableCell className="p-1.5 text-center text-primary font-medium">{p.sign_lord ? planetShort(p.sign_lord) : '-'}</TableCell>
                      <TableCell className="p-1.5 text-center text-primary font-medium">{p.star_lord || p.nakshatra_lord ? planetShort(p.star_lord || p.nakshatra_lord) : '-'}</TableCell>
                      <TableCell className="p-1.5 text-center text-primary font-medium">{p.sub_lord ? planetShort(p.sub_lord) : '-'}</TableCell>
                      <TableCell className="p-1.5 text-center text-primary font-medium">{p.sub_sub_lord ? planetShort(p.sub_sub_lord) : '-'}</TableCell>
                      <TableCell className="p-1.5 text-center text-primary font-medium">{p.star_lord_of_sub_lord ? planetShort(p.star_lord_of_sub_lord) : '-'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* Birth Chart + Cuspal Chart — North Indian Diamond */}
          {(() => {
            // Build chart data from KP planets for Birth Chart (Rashi-based houses)
            const SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
            const kpPlanets = kpData.planets || [];
            // Birth chart: house derived from sign relative to ascendant sign
            const ascSign = result?.chart_data?.ascendant?.sign || (kpData.cusps?.[0]?.sign) || 'Aries';
            const ascIdx = SIGNS.indexOf(ascSign);
            const birthPlanets: PlanetData[] = kpPlanets.map((p: any) => {
              const signIdx = SIGNS.indexOf(p.sign);
              const house = signIdx >= 0 && ascIdx >= 0 ? ((signIdx - ascIdx + 12) % 12) + 1 : 1;
              return { planet: p.planet, sign: p.sign, house, nakshatra: p.nakshatra || '', sign_degree: typeof p.degree === 'number' ? p.degree % 30 : 0, status: '', is_retrograde: p.retrograde };
            });
            const birthHouses = SIGNS.map((_, i) => ({ number: i + 1, sign: SIGNS[(ascIdx + i) % 12] }));

            // Cuspal chart: house based on which cusp range the planet falls in
            const cusps = kpData.cusps || [];
            const cuspDegrees = cusps.map((c: any) => typeof c.degree === 'number' ? c.degree : 0);
            const cuspalPlanets: PlanetData[] = kpPlanets.map((p: any) => {
              const lon = typeof p.degree === 'number' ? p.degree : 0;
              let house = 1;
              for (let h = 0; h < 12; h++) {
                const start = cuspDegrees[h] || 0;
                const end = cuspDegrees[(h + 1) % 12] || 0;
                if (end > start ? (lon >= start && lon < end) : (lon >= start || lon < end)) { house = h + 1; break; }
              }
              return { planet: p.planet, sign: p.sign, house, nakshatra: p.nakshatra || '', sign_degree: typeof p.degree === 'number' ? p.degree % 30 : 0, status: '', is_retrograde: p.retrograde };
            });
            const cuspalHouses = cusps.map((c: any, i: number) => ({ number: i + 1, sign: c.sign || SIGNS[(ascIdx + i) % 12] }));

            return (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-muted rounded-xl border border-border p-4">
                  <Heading as={4} variant={4} className="mb-2 text-center">{t('section.vedicBirthChart')}</Heading>
                  <InteractiveKundli chartData={{ planets: birthPlanets, houses: birthHouses, ascendant: result?.chart_data?.ascendant } as ChartData} compact />
                </div>
                <div className="bg-muted rounded-xl border border-border p-4">
                  <Heading as={4} variant={4} className="mb-2 text-center">{t('auto.cuspalChart')}</Heading>
                  <InteractiveKundli chartData={{ planets: cuspalPlanets, houses: cuspalHouses, ascendant: result?.chart_data?.ascendant } as ChartData} compact />
                </div>
              </div>
            );
          })()}

          {/* 2. Bhava Details (Placidus) — House Cusps */}
          <div className="bg-muted rounded-xl border border-border p-4">
            <Heading as={4} variant={4} className="mb-3">{t('auto.bhavaDetailsPlacidus')}</Heading>
            <div className="overflow-x-auto">
              <Table className="w-full text-sm">
                <TableHeader><TableRow className="bg-muted">
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.house')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.sign')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.degree')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">{t('kundli.pada')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.rashiLord')}>RL</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.nakshatraLord')}>NL</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.subLord')}>SL</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.subSubLord')}>SS</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.starLordOfSubLord')}>SSSL</TableHead>
                </TableRow></TableHeader>
                <TableBody>
                  {(() => {
                    const houseNames = language === 'hi'
                      ? ['प्रथम','द्वितीय','तृतीय','चतुर्थ','पंचम','षष्ठ','सप्तम','अष्टम','नवम','दशम','एकादश','द्वादश']
                      : ['First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eighth','Ninth','Tenth','Eleventh','Twelfth'];
                    return (kpData.cusps || []).map((c: any, i: number) => {
                    return (
                      <TableRow key={i} className="border-t border-border">
                        <TableCell className="p-1.5 font-semibold text-foreground">{(c.house || i + 1)}.{houseNames[i] || ''}</TableCell>
                        <TableCell className="p-1.5 text-foreground">{translateSign(c.sign || '', language)}</TableCell>
                        <TableCell className="p-1.5 text-foreground font-mono">{c.degree_dms || (typeof c.degree === 'number' ? c.degree.toFixed(2) : c.degree || '-')}</TableCell>
                        <TableCell className="p-1.5 text-foreground">{translateNakshatra(c.nakshatra, language) || '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-foreground">{c.pada || '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{c.sign_lord ? c.sign_lord.slice(0, 2) : '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{(c.star_lord || '-').slice(0, 2)}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{(c.sub_lord || '-').slice(0, 2)}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{(c.sub_sub_lord || '-').slice(0, 2)}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{(c.star_lord_of_sub_lord || '-').slice(0, 2)}</TableCell>
                      </TableRow>
                    );
                  });
                  })()}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* 3. Significations of Houses */}
          {kpData.house_significations && Object.keys(kpData.house_significations).length > 0 && (
            <div className="bg-muted rounded-xl border border-border p-4">
              <Heading as={4} variant={4} className="mb-3">{t('auto.significationsOfHous')}</Heading>
              <div className="overflow-x-auto">
                <Table className="w-full text-sm">
                  <TableHeader><TableRow className="bg-muted">
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.house')}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('auto.planetsInNakOfOccupa')}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('auto.occupants')}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('auto.planetsInNakOfCuspLo')}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('auto.cuspSignLord')}</TableHead>
                  </TableRow></TableHeader>
                  <TableBody>
                    {[1,2,3,4,5,6,7,8,9,10,11,12].map(h => {
                      const sig = kpData.house_significations[h] || kpData.house_significations[String(h)] || {};
                      return (
                        <TableRow key={h} className="border-t border-border">
                          <TableCell className="p-1.5 font-semibold text-foreground">{h}</TableCell>
                          <TableCell className="p-1.5 text-foreground">{planetList(sig.planets_in_nak_of_occupants || []) || '-'}</TableCell>
                          <TableCell className="p-1.5 text-foreground font-medium">{planetList(sig.occupants || []) || '-'}</TableCell>
                          <TableCell className="p-1.5 text-foreground">{planetList(sig.planets_in_nak_of_cusp_sign_lord || []) || '-'}</TableCell>
                          <TableCell className="p-1.5 text-primary font-medium">{sig.cusp_sign_lord ? translatePlanet(sig.cusp_sign_lord, language) : '-'}</TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>
            </div>
          )}

          {/* 4. Houses Signified by Planets */}
          {kpData.planet_significator_strengths && Object.keys(kpData.planet_significator_strengths).length > 0 && (
            <div className="bg-muted rounded-xl border border-border p-4">
              <Heading as={4} variant={4} className="mb-3">{t('auto.housesSignifiedByPla')}</Heading>
              <div className="overflow-x-auto">
                <Table className="w-full text-sm">
                  <TableHeader><TableRow className="bg-muted">
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.planet')}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('auto.veryStrong')}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('auto.strong')}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('auto.normal')}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{t('auto.weak')}</TableHead>
                  </TableRow></TableHeader>
                  <TableBody>
                    {Object.entries(kpData.planet_significator_strengths).map(([planet, levels]: [string, any]) => (
                      <TableRow key={planet} className="border-t border-border">
                        <TableCell className="p-1.5 font-semibold text-foreground">{translatePlanet(planet, language)}</TableCell>
                        <TableCell className="p-1.5 text-green-500 font-medium">{planetList(levels.very_strong || [])}</TableCell>
                        <TableCell className="p-1.5 text-blue-400 font-medium">{planetList(levels.strong || [])}</TableCell>
                        <TableCell className="p-1.5 text-foreground">{planetList(levels.normal || [])}</TableCell>
                        <TableCell className="p-1.5 text-orange-400">{planetList(levels.weak || [])}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>
          )}

          {/* 5. Ruling Planets */}
          {kpData.ruling_planets && Object.keys(kpData.ruling_planets).length > 0 && (
            <div className="bg-muted rounded-xl border border-border p-4">
              <Heading as={4} variant={4} className="mb-3">{t('auto.rulingPlanets')}</Heading>
              <div className="grid grid-cols-2 gap-3 text-sm">
                {[
                  ['day_lord', t('auto.dayLord')],
                  ['lagna_lord', t('auto.lagnaLord')],
                  ['lagna_nak_lord', t('auto.lagnaNakLord')],
                  ['lagna_sub_lord', t('auto.lagnaSubLord')],
                  ['moon_rashi_lord', t('auto.moonRashiLord')],
                  ['moon_nak_lord', t('auto.moonNakLord')],
                  ['moon_sub_lord', t('auto.moonSubLord')],
                ].map(([key, label]) => (
                  <div key={key} className="flex items-center justify-between bg-white rounded-lg p-2">
                    <span className="text-foreground">{translateBackend(label, language)}</span>
                    <span className="font-semibold text-primary">{kpData.ruling_planets[key] ? translatePlanet(kpData.ruling_planets[key], language) : '-'}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <p className="text-center text-foreground py-8">{t('kundli.clickKPTab')}</p>
      )}
    </div>
  );
}
