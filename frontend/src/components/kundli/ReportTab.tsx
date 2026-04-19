import { Loader2, CheckCircle, Shield, ChevronDown } from 'lucide-react';
import { formatDate } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { ChartLegend, type PlanetData } from '@/components/InteractiveKundli';
import { DIVISIONAL_CHART_OPTIONS } from '@/components/kundli/kundli-utils';
import { calculateJaiminiKarakas } from '@/components/kundli/jhora-utils';
import LordshipsTab from '@/components/kundli/LordshipsTab';
import { translatePlanet, translateSign, translateLabel, translateName, translateNakshatra, translateBackend, translateSignAbbr, translatePlanetAbbr } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';

interface ReportTabProps {
  result: any;
  planets: any[];
  formData: { name: string; date: string; time: string; place: string };
  language: string;
  t: (key: string) => string;
  doshaData: any;
  loadingDosha: boolean;
  dashaData: any;
  loadingDasha: boolean;
  extendedDashaData: any;
  loadingExtendedDasha: boolean;
  avakhadaData: any;
  loadingAvakhada: boolean;
  yogaDoshaData: any;
  loadingYogaDosha: boolean;
  ashtakvargaData: any;
  loadingAshtakvarga: boolean;
  shadbalaData: any;
  loadingShadbala: boolean;
  divisionalData: any;
  loadingDivisional: boolean;
  transitData: any;
  loadingTransit: boolean;
  d10Data: any;
  loadingD10: boolean;
  selectedDivision: string;
  reportLagnaShift: number;
  setReportLagnaShift: (v: number) => void;
  reportMoonShift: number;
  setReportMoonShift: (v: number) => void;
  reportGocharShift: number;
  setReportGocharShift: (v: number) => void;
  expandedMahadasha: string | null;
  setExpandedMahadasha: (v: string | null) => void;
  expandedAntardasha: string | null;
  setExpandedAntardasha: (v: string | null) => void;
  fetchTransit: () => void;
  fetchD10: () => void;
  fetchDasha: () => void;
  fetchExtendedDasha: () => void;
  changeDivision: (code: string) => void;
  handlePlanetClick: (planet: any) => void;
  handleHouseClick: (house: number, sign: string, planets: any[]) => void;
}

export default function ReportTab({
  result, planets, formData: _formData, language, t,
  doshaData, loadingDosha,
  dashaData, loadingDasha,
  extendedDashaData, loadingExtendedDasha,
  avakhadaData, loadingAvakhada,
  yogaDoshaData, loadingYogaDosha,
  ashtakvargaData, loadingAshtakvarga,
  shadbalaData, loadingShadbala,
  divisionalData, loadingDivisional,
  transitData, loadingTransit,
  d10Data, loadingD10,
  selectedDivision,
  reportLagnaShift, setReportLagnaShift,
  reportMoonShift, setReportMoonShift,
  reportGocharShift, setReportGocharShift,
  expandedMahadasha, setExpandedMahadasha,
  expandedAntardasha, setExpandedAntardasha,
  fetchTransit, fetchD10, fetchDasha, fetchExtendedDasha,
  changeDivision,
  handlePlanetClick, handleHouseClick,
}: ReportTabProps) {
  const SIGNS_ORDER = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
  const shiftedSign = (base: string, shift: number) => {
    const idx = SIGNS_ORDER.indexOf(String(base || '').trim());
    if (idx < 0) return base || '';
    return SIGNS_ORDER[(idx + (shift % 12) + 12) % 12] || base;
  };
  const ascFromHouses = (houses: any): string => {
    const list = Array.isArray(houses) ? houses : [];
    const h1 = list.find((h: any) => Number(h?.number) === 1);
    return String(h1?.sign || '').trim();
  };
  const toPlanetEntry = (p: any): PlanetEntry => ({
    planet: p.planet,
    sign: p.sign || p.current_sign || '',
    sign_degree: Number(p.sign_degree ?? p.degree ?? 0) || 0,
    status: typeof p.status === 'string' ? p.status : '',
    is_retrograde: !!p.is_retrograde,
    is_combust: !!p.is_combust,
    is_vargottama: !!p.is_vargottama,
    is_exalted: !!p.is_exalted,
    is_debilitated: !!p.is_debilitated,
  } as any);

  return (
            <div className="space-y-6">


              {/* Report title */}
              <div className="bg-gradient-to-r from-muted to-muted rounded-xl p-5 border border-border text-center">
                <Heading as={3} variant={3}>{t('section.consolidatedReport')}</Heading>
                <p className="text-sm text-foreground mt-1">{result.person_name} | {formatDate(result.birth_date)} | {result.birth_time} | {result.birth_place}</p>
              </div>

              {/* Charts row — Lagna, Moon, Gochar side by side */}
              <p className="text-xs text-muted-foreground text-center -mb-2">{t('kundli.clickHouseToRotate')}</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 print:grid-cols-3">
                {/* 1. Lagna Chart (D1) — click house to rotate lagan */}
                <div className="bg-transparent border-0 p-0">
                  <Heading as={4} variant={4} className="mb-2 text-center">
                    {t('section.lagna')}
                  </Heading>
                  <div className="flex justify-center">
                    {(() => {
                      const shift = reportLagnaShift;
                      const baseAsc = result.chart_data?.ascendant?.sign
                        || planets.find((p: any) => p.planet === 'Lagna' || p.planet === 'Ascendant')?.sign
                        || '';
                      const asc = shiftedSign(baseAsc, shift);
                      return (
                        <div className="w-full max-w-[340px] aspect-square">
  	                          <KundliChartSVG
  	                            planets={planets.map(toPlanetEntry)}
  	                            ascendantSign={asc}
  	                            language={language}
  	                            showHouseNumbers={false}
                            showRashiNumbers
                            rashiNumberPlacement="corner"
                            showAscendantMarker={false}
                            onPlanetClick={(pl) => handlePlanetClick(pl as any)}
                            onHouseClick={(house) => {
                              // Rotate view so the clicked house becomes Lagna (house 1).
                              // shift is the current sign-rotation offset applied to the base ascendant.
                              setReportLagnaShift((prev) => (prev + (house - 1)) % 12);
                            }}
                          />
                        </div>
                      );
                    })()}
                  </div>
                  {reportLagnaShift > 0 && (
                    <button onClick={() => setReportLagnaShift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
                  )}
                </div>

                {/* 2. Moon Chart — click house to rotate lagan */}
                <div className="bg-transparent border-0 p-0">
                  <Heading as={4} variant={4} className="mb-2 text-center">
                    {t('section.moon')}
                  </Heading>
                  <div className="flex justify-center">
                    {(() => {
                      const moonPlanet = planets.find((p: PlanetData) => p.planet === 'Moon');
                      const moonHouse = moonPlanet?.house || 1;
                      const baseShift = moonHouse - 1;
                      const totalShift = baseShift + reportMoonShift;
                      const baseAsc = result.chart_data?.ascendant?.sign
                        || planets.find((p: any) => p.planet === 'Lagna' || p.planet === 'Ascendant')?.sign
                        || '';
                      const asc = shiftedSign(baseAsc, totalShift);
                      return (
                        <div className="w-full max-w-[340px] aspect-square">
  	                          <KundliChartSVG
  	                            planets={planets.map(toPlanetEntry)}
  	                            ascendantSign={asc}
  	                            language={language}
  	                            showHouseNumbers={false}
                            showRashiNumbers
                            rashiNumberPlacement="corner"
                            showAscendantMarker={false}
                            onPlanetClick={(pl) => handlePlanetClick(pl as any)}
                            onHouseClick={(house) => {
                              // Same rule: clicked house becomes Lagna, but Moon chart has a fixed baseShift.
                              // reportMoonShift is the additional rotation on top of baseShift.
                              setReportMoonShift((prev) => (prev + (house - 1)) % 12);
                            }}
                          />
                        </div>
                      );
                    })()}
                  </div>
                  {reportMoonShift > 0 && (
                    <button onClick={() => setReportMoonShift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
                  )}
                </div>

                {/* 3. Gochar (Transit) Chart — click house to rotate lagan */}
                <div className="bg-transparent border-0 p-0">
                  <Heading as={4} variant={4} className="mb-2 text-center">
                    {t('section.gochar')} {transitData?.transit_date ? `(${transitData.transit_date})` : ''}
                  </Heading>
                  <div className="flex justify-center">
                    {loadingTransit ? (
                      <div className="flex items-center justify-center py-12"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
                    ) : transitData?.transits ? (() => {
                      const shift = reportGocharShift;
                      const transitPlanets = transitData.transits.map((tr: any) => ({
                        planet: tr.planet,
                        sign: tr.current_sign || tr.sign || '',
                        nakshatra: tr.nakshatra || '',
                        sign_degree: tr.sign_degree || tr.degree || 0,
                        status: tr.is_retrograde ? 'Retrograde' : '',
                        is_retrograde: tr.is_retrograde,
                      }));
                      const baseAsc = transitData.chart_data?.ascendant?.sign || result.chart_data?.ascendant?.sign || '';
                      const asc = shiftedSign(baseAsc, shift);
                      return (
                        <div className="w-full max-w-[340px] aspect-square">
  	                          <KundliChartSVG
  	                            planets={transitPlanets.map(toPlanetEntry)}
  	                            ascendantSign={asc}
  	                            language={language}
  	                            showHouseNumbers={false}
                            showRashiNumbers
                            rashiNumberPlacement="corner"
                            showAscendantMarker={false}
                            onPlanetClick={(pl) => handlePlanetClick(pl as any)}
                            onHouseClick={(house) => {
                              // Rotate view so the clicked house becomes Lagna (house 1).
                              setReportGocharShift((prev) => (prev + (house - 1)) % 12);
                            }}
                          />
                        </div>
                      );
                    })() : (
                      <p className="text-center text-foreground py-12 text-sm">{t('common.loading')}</p>
                    )}
                  </div>
                  {reportGocharShift > 0 && (
                    <button onClick={() => setReportGocharShift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
                  )}
                </div>
              </div>

              {/* Chart Legend */}
              <ChartLegend />

              {/* Row 1: Planet Details (2/3) and Divisional Chart (1/3) */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6 print:grid-cols-3">
                {/* 2. Planet Details Table */}
                <div className="lg:col-span-2 rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden flex flex-col">
                  <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
                    <span>{t('section.detailedPlanetPositions')}</span>
                    <span className="text-xs font-normal opacity-80">
                      {t('kundli.lagna')}: {translateSign(result.chart_data?.ascendant?.sign || '', language) || '\u2014'}
                    </span>
                  </div>
                  <div className="overflow-x-auto flex-1">
                    <Table className="w-full text-xs">
                      <TableHeader>
                        <TableRow>
                          <TableHead className="text-left">{t('table.planet')}</TableHead>
                          <TableHead className="text-left">{t('table.sign')}</TableHead>
                          <TableHead className="text-center">{t('table.house')}</TableHead>
                          <TableHead className="text-left">{t('table.nakshatra')}</TableHead>
                          <TableHead className="text-center whitespace-nowrap">{t('table.degree')}</TableHead>
                          <TableHead className="text-center">{t('table.status')}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {planets.map((planet: any, index: number) => (
                          <TableRow key={index}>
                            <TableCell className="text-foreground font-medium">{translatePlanet(planet.planet, language)}</TableCell>
                            <TableCell className="text-foreground">{translateSign(planet.sign, language)}</TableCell>
                            <TableCell className="text-center text-foreground">{planet.house}</TableCell>
                            <TableCell className="text-foreground">{translateNakshatra(planet.nakshatra, language) || '\u2014'}</TableCell>
                            <TableCell className="text-center text-foreground whitespace-nowrap">{(Number(planet.sign_degree) || 0).toFixed(1)}°</TableCell>
                            <TableCell className="text-center">
                              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-100 text-green-800' : 'text-foreground'}`}>
                                {translateLabel(planet.status, language) || '\u2014'}
                              </span>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </div>

	                {/* 3. Divisional Chart */}
	                <div className="lg:col-span-1 bg-transparent rounded-xl border border-sacred-gold/20 overflow-hidden flex flex-col">
	                  <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
	                    {t('kundli.divisionalCharts')}
	                  </div>
	                  <div className="p-3 flex flex-col gap-3 flex-1">
	                    <div className="flex justify-end">
	                      <div className="relative w-full max-w-[220px]">
	                        <select
	                          value={selectedDivision}
	                          onChange={(e) => changeDivision(e.target.value)}
	                          className="input-sacred text-xs py-1.5 pr-8 w-full"
	                        >
	                          {DIVISIONAL_CHART_OPTIONS.map((c) => (
	                            <option key={c.code} value={c.code}>{c.name}</option>
	                          ))}
	                        </select>
	                        <ChevronDown
	                          className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 w-4 h-4"
	                          style={{ color: '#C4611F', opacity: 0.75 }}
	                        />
	                      </div>
	                    </div>
	                    {loadingDivisional ? (
	                      <div className="flex items-center justify-center py-8 flex-1"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
	                    ) : divisionalData?.planet_positions ? (
	                      <div className="flex justify-center flex-1 items-center">
	                        <div className="w-full max-w-[340px] aspect-square">
	                          <KundliChartSVG
	                            planets={(divisionalData.planet_positions || []).map(toPlanetEntry)}
	                            ascendantSign={
	                              ascFromHouses(divisionalData.houses)
	                              || divisionalData.chart_data?.ascendant?.sign
	                              || divisionalData.ascendant?.sign
	                              || (divisionalData.planet_positions || []).find((p: any) => p.planet === 'Lagna' || p.planet === 'Ascendant')?.sign
	                              || result.chart_data?.ascendant?.sign
	                              || ''
	                            }
	                            language={language}
	                            className="w-full h-full"
	                            showHouseNumbers={false}
	                            showRashiNumbers
	                            rashiNumberPlacement="corner"
	                            showAscendantMarker={false}
	                            onPlanetClick={(pl) => handlePlanetClick(pl as any)}
	                          />
	                        </div>
	                      </div>
	                    ) : (
	                      <p className="text-center text-foreground py-8 text-sm flex-1 flex items-center justify-center">{t('kundli.selectChart')}</p>
	                    )}
	                  </div>
	                </div>
              </div>

              {/* Grid layout for remaining items — 2 columns on desktop, 1 on mobile */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 print:grid-cols-2">

	                {/* 4. Lordships */}
	                <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
	                  <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
	                    {t('section.houseLordships')}
	                  </div>
	                  <div className="pb-3">
	                    <LordshipsTab planets={planets} houses={result.chart_data?.houses || {}} />
	                  </div>
	                </div>

	                {/* 5. Avakhada Chakra */}
	                <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
	                  <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
	                    {t('section.avakhadaChakra')}
	                  </div>
	                  {loadingAvakhada ? (
	                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
	                  ) : avakhadaData ? (
	                    <div className="pb-3 overflow-x-auto">
	                      <Table className="w-full text-xs">
	                        <TableHeader>
	                          <TableRow>
	                            <TableHead className="text-left">{t('table.parameter')}</TableHead>
	                            <TableHead className="text-left">{t('table.value')}</TableHead>
	                          </TableRow>
	                        </TableHeader>
	                        <TableBody>
	                          {[
	                            { label: t('avakhada.ascendant'), value: translateSign(avakhadaData.ascendant, language) },
	                            { label: t('avakhada.ascendantLord'), value: translatePlanet(avakhadaData.ascendant_lord, language) },
	                            { label: t('avakhada.rashi'), value: translateSign(avakhadaData.rashi, language) },
	                            { label: t('avakhada.rashiLord'), value: translatePlanet(avakhadaData.rashi_lord, language) },
	                            { label: t('avakhada.nakshatra'), value: `${translateNakshatra(avakhadaData.nakshatra, language)} (P${avakhadaData.nakshatra_pada})` },
	                            { label: t('avakhada.yoga'), value: translateBackend(avakhadaData.yoga, language) },
	                            { label: t('avakhada.karana'), value: translateBackend(avakhadaData.karana, language) },
	                            { label: t('avakhada.yoni'), value: translateBackend(avakhadaData.yoni, language) },
	                            { label: t('avakhada.gana'), value: translateBackend(avakhadaData.gana, language) },
	                            { label: t('avakhada.nadi'), value: translateBackend(avakhadaData.nadi, language) },
	                            { label: t('avakhada.varna'), value: translateBackend(avakhadaData.varna, language) },
	                            { label: t('avakhada.naamakshar'), value: avakhadaData.naamakshar },
	                            { label: t('avakhada.sunSign'), value: translateSign(avakhadaData.sun_sign, language) },
	                          ].map((item) => (
	                            <TableRow key={item.label}>
	                              <TableCell className="font-medium text-foreground whitespace-nowrap">{item.label}</TableCell>
	                              <TableCell className="text-foreground">{item.value || '\u2014'}</TableCell>
	                            </TableRow>
	                          ))}
	                        </TableBody>
	                      </Table>
	                    </div>
	                  ) : (
	                    <p className="text-center text-foreground py-4 text-sm">{t('common.loading')}</p>
	                  )}
	                </div>

	                {/* 6. Vimshottari Dasha — compact 120-yr list */}
	                {(() => {
	                  const BENEFIC = new Set(['Jupiter', 'Venus', 'Mercury', 'Moon']);
	                  const MALEFIC = new Set(['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']);
	                  const getNature = (p: any): 'benefic' | 'malefic' | null => {
	                    const raw = String(p?.nature || p?.type || '').toLowerCase().trim();
	                    if (raw.includes('benefic')) return 'benefic';
	                    if (raw.includes('malefic')) return 'malefic';
	                    const planet = String(p?.planet || '').trim();
	                    if (BENEFIC.has(planet)) return 'benefic';
	                    if (MALEFIC.has(planet)) return 'malefic';
	                    return null;
	                  };
	                  const toIso = (s: any): string => (typeof s === 'string' ? s.slice(0, 10) : '');
	                  const dateToTime = (iso: string): number => {
	                    const t = Date.parse(iso);
	                    return Number.isFinite(t) ? t : NaN;
	                  };
	                  const yearsBetween = (startIso: string, endIso: string): number | null => {
	                    const a = dateToTime(startIso);
	                    const b = dateToTime(endIso);
	                    if (!Number.isFinite(a) || !Number.isFinite(b)) return null;
	                    return Math.max(0, (b - a) / (1000 * 60 * 60 * 24 * 365.25));
	                  };
	                  const normalizeSub = (p: any, idx: number, arr: any[], fallbackStart: string) => {
	                    const end = toIso(p?.end || p?.end_date);
	                    const prevEnd = idx > 0 ? toIso(arr[idx - 1]?.end || arr[idx - 1]?.end_date) : '';
	                    const start = toIso(p?.start || p?.start_date) || prevEnd || fallbackStart;
	                    const y = p?.years != null ? Number(p.years) : (start && end ? yearsBetween(start, end) : null);
	                    return {
	                      planet: p?.planet,
	                      start_date: start || '',
	                      end_date: end || '',
	                      years: y,
	                      nature: getNature(p),
	                      is_current: !!p?.is_current,
	                      pratyantar: p?.pratyantar || p?.pratyantars || [],
	                    };
	                  };
	                  const normalizeMd = (p: any, idx: number, arr: any[]) => {
	                    const end = toIso(p?.end || p?.end_date);
	                    const prevEnd = idx > 0 ? toIso(arr[idx - 1]?.end || arr[idx - 1]?.end_date) : '';
	                    const start = toIso(p?.start || p?.start_date) || prevEnd || String(result.birth_date || '').slice(0, 10);
	                    const y = p?.years != null ? Number(p.years) : (start && end ? yearsBetween(start, end) : null);
	                    const rawAds = p?.antardasha || p?.antardashas || [];
	                    const ads = Array.isArray(rawAds) ? rawAds.map((ad: any, ai: number, aarr: any[]) => normalizeSub(ad, ai, aarr, start)) : [];
	                    return {
	                      planet: p?.planet,
	                      start_date: start || '',
	                      end_date: end || '',
	                      years: y,
	                      nature: getNature(p),
	                      is_current: !!p?.is_current || (p?.planet && p.planet === dashaData?.current_dasha),
	                      antardasha: ads,
	                    };
	                  };
	                  const rawPeriods: any[] = extendedDashaData?.mahadasha || dashaData?.mahadasha_periods || [];
	                  const periods: any[] = rawPeriods.map((p: any, i: number, arr: any[]) => normalizeMd(p, i, arr));
	                  const currentMD = (extendedDashaData || dashaData)?.current_dasha;
	                  return (
	                    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
	                      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold text-center">
	                        {t('section.vimshottariDasha')}
	                      </div>
	                      <div className="pb-3">
	                      {(loadingDasha || loadingExtendedDasha) ? (
	                        <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
	                      ) : periods.length > 0 ? (
	                        <>
	                          <div className="overflow-x-auto">
	                            <Table className="w-full text-xs">
	                              <TableHeader>
	                                <TableRow>
	                                  <TableHead className="text-left whitespace-nowrap">{t('table.dashaLord')}</TableHead>
	                                  <TableHead className="text-left whitespace-nowrap">{t('table.start')}</TableHead>
	                                  <TableHead className="text-left whitespace-nowrap">{t('table.end')}</TableHead>
	                                  <TableHead className="text-center whitespace-nowrap">{t('table.years')}</TableHead>
	                                  <TableHead className="text-center whitespace-nowrap">{t('table.nature')}</TableHead>
	                                </TableRow>
	                              </TableHeader>
	                              <TableBody>
	                                {periods.map((md: any) => {
	                                  const isCurrent = md.is_current || md.planet === currentMD;
	                                  const isOpen = expandedMahadasha === md.planet;
	                                  const nature = md.nature;
	                                  const hasAds = Array.isArray(md.antardasha) && md.antardasha.length > 0;
	                                  return (
	                                    <>
	                                      <TableRow
	                                        key={md.planet}
	                                        className={isCurrent ? 'bg-sacred-gold/10' : undefined}
	                                      >
	                                        <TableCell className="font-medium text-foreground">
	                                          <button
	                                            type="button"
	                                            onClick={() => hasAds && setExpandedMahadasha(isOpen ? null : md.planet)}
	                                            className={`inline-flex items-center gap-2 transition-colors ${
	                                              hasAds ? 'hover:text-sacred-gold-dark' : 'cursor-default opacity-80'
	                                            }`}
	                                          >
	                                            <ChevronDown className={`w-3 h-3 transition-transform ${hasAds ? '' : 'opacity-0'} ${isOpen ? 'rotate-180' : ''}`} />
	                                            <span className="whitespace-nowrap">{translatePlanet(md.planet, language)}</span>
	                                            {isCurrent && (
	                                              <span className="ml-1 text-[9px] px-1.5 py-0.5 rounded bg-sacred-gold-dark text-white uppercase">
	                                                {t('common.current')}
	                                              </span>
	                                            )}
	                                          </button>
	                                        </TableCell>
	                                        <TableCell className="text-foreground whitespace-nowrap">{md.start_date || '—'}</TableCell>
	                                        <TableCell className="text-foreground whitespace-nowrap">{md.end_date || '—'}</TableCell>
	                                        <TableCell className="text-center text-foreground font-semibold whitespace-nowrap">
	                                          {md.years == null ? '—' : (Number.isInteger(md.years) ? md.years : Number(md.years).toFixed(4))}
	                                        </TableCell>
	                                        <TableCell className="text-center whitespace-nowrap">
	                                          {nature ? (
	                                            <span className={`text-[9px] px-2 py-0.5 rounded-full font-black uppercase border ${
	                                              nature === 'benefic'
	                                                ? 'bg-emerald-100 text-emerald-700 border-emerald-200'
	                                                : 'bg-red-100 text-red-700 border-red-200'
	                                            }`}>
	                                              {nature === 'benefic' ? t('kundli.benefic') : t('kundli.malefic')}
	                                            </span>
	                                          ) : (
	                                            '—'
	                                          )}
	                                        </TableCell>
	                                      </TableRow>

	                                      {hasAds && isOpen && (
	                                        <TableRow key={`${md.planet}-ads`}>
	                                          <TableCell colSpan={5} className="bg-sacred-gold/[0.03]">
	                                            <div className="pl-4 border-l border-sacred-gold/20">
	                                              <div className="text-[11px] font-semibold text-sacred-gold-dark mb-2">
	                                                {t('kundli.antardasha')}
	                                              </div>
	                                              <div className="overflow-x-auto">
	                                                <Table className="w-full text-xs">
	                                                  <TableHeader>
	                                                    <TableRow>
	                                                      <TableHead className="text-left whitespace-nowrap">{t('table.dashaLord')}</TableHead>
	                                                      <TableHead className="text-left whitespace-nowrap">{t('table.start')}</TableHead>
	                                                      <TableHead className="text-left whitespace-nowrap">{t('table.end')}</TableHead>
	                                                      <TableHead className="text-center whitespace-nowrap">{t('table.years')}</TableHead>
	                                                      <TableHead className="text-center whitespace-nowrap">{t('table.nature')}</TableHead>
	                                                    </TableRow>
	                                                  </TableHeader>
	                                                  <TableBody>
	                                                    {(md.antardasha || []).map((ad: any) => {
	                                                      const adKey = `${md.planet}-${ad.planet}`;
	                                                      const adOpen = expandedAntardasha === adKey;
	                                                      const adHasPts = Array.isArray(ad.pratyantar) && ad.pratyantar.length > 0;
	                                                      const adNature = ad.nature;
	                                                      return (
	                                                        <>
	                                                          <TableRow key={adKey}>
	                                                            <TableCell className="font-medium text-foreground">
	                                                              <button
	                                                                type="button"
	                                                                onClick={() => adHasPts && setExpandedAntardasha(adOpen ? null : adKey)}
	                                                                className={`inline-flex items-center gap-2 transition-colors ${
	                                                                  adHasPts ? 'hover:text-sacred-gold-dark' : 'cursor-default opacity-80'
	                                                                }`}
	                                                              >
	                                                                <ChevronDown className={`w-3 h-3 transition-transform ${adHasPts ? '' : 'opacity-0'} ${adOpen ? 'rotate-180' : ''}`} />
	                                                                <span className="whitespace-nowrap">{translatePlanet(ad.planet, language)}</span>
	                                                              </button>
	                                                            </TableCell>
	                                                            <TableCell className="text-foreground whitespace-nowrap">{ad.start_date || '—'}</TableCell>
	                                                            <TableCell className="text-foreground whitespace-nowrap">{ad.end_date || '—'}</TableCell>
	                                                            <TableCell className="text-center text-foreground font-semibold whitespace-nowrap">
	                                                              {ad.years == null ? '—' : (Number.isInteger(ad.years) ? ad.years : Number(ad.years).toFixed(4))}
	                                                            </TableCell>
	                                                            <TableCell className="text-center whitespace-nowrap">
	                                                              {adNature ? (
	                                                                <span className={`text-[9px] px-2 py-0.5 rounded-full font-black uppercase border ${
	                                                                  adNature === 'benefic'
	                                                                    ? 'bg-emerald-100 text-emerald-700 border-emerald-200'
	                                                                    : 'bg-red-100 text-red-700 border-red-200'
	                                                                }`}>
	                                                                  {adNature === 'benefic' ? t('kundli.benefic') : t('kundli.malefic')}
	                                                                </span>
	                                                              ) : (
	                                                                '—'
	                                                              )}
	                                                            </TableCell>
	                                                          </TableRow>

	                                                          {adHasPts && adOpen && (
	                                                            <TableRow key={`${adKey}-pts`}>
	                                                              <TableCell colSpan={5} className="bg-sacred-gold/[0.02]">
	                                                                <div className="pl-4 border-l border-sacred-gold/15">
	                                                                  <div className="text-[11px] font-semibold text-sacred-gold-dark mb-2">
	                                                                    {t('kundli.pratyantar')}
	                                                                  </div>
	                                                                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1">
	                                                                    {(ad.pratyantar || []).map((pt: any, pti: number) => {
	                                                                      const ptEnd = toIso(pt?.end || pt?.end_date);
	                                                                      const ptPrevEnd = pti > 0 ? toIso(ad.pratyantar[pti - 1]?.end || ad.pratyantar[pti - 1]?.end_date) : ad.start_date;
	                                                                      const ptStart = toIso(pt?.start || pt?.start_date) || ptPrevEnd || '';
	                                                                      return (
	                                                                        <div key={`${adKey}-pt-${pti}`} className="flex items-center justify-between text-[11px]">
	                                                                          <span className="text-foreground whitespace-nowrap">
	                                                                            {translatePlanet(pt.planet, language)}
	                                                                          </span>
	                                                                          <span className="text-muted-foreground whitespace-nowrap">
	                                                                            {ptStart || '—'} → {ptEnd || '—'}
	                                                                          </span>
	                                                                        </div>
	                                                                      );
	                                                                    })}
	                                                                  </div>
	                                                                </div>
	                                                              </TableCell>
	                                                            </TableRow>
	                                                          )}
	                                                        </>
	                                                      );
	                                                    })}
	                                                  </TableBody>
	                                                </Table>
	                                              </div>
	                                            </div>
	                                          </TableCell>
	                                        </TableRow>
	                                      )}
	                                    </>
	                                  );
	                                })}
	                              </TableBody>
	                            </Table>
	                          </div>
	                          <p className="text-xs text-muted-foreground mt-3">
	                            {language === 'hi'
	                              ? 'नोट :- उप-काल के लिए ऊपर पंक्ति पर क्लिक करें। ऊपर दिनांक समाप्ति तिथियाँ हैं।'
	                              : 'Note :- Click on row above for sub-period. Date mentioned above are ending dates.'}
	                          </p>
	                        </>
	                      ) : (
	                        <p className="text-center py-4 text-sm text-muted-foreground">{t('common.noData')}</p>
	                      )}
	                      </div>
	                    </div>
	                  );
	                })()}

                {/* 6b. Jaimini Karakas — separate card */}
                <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
                  <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                    {t('section.jaiminiKarakas')}
                  </div>
                  {(() => {
                    const karakas = calculateJaiminiKarakas(planets);
                    const karakaOrder = [
                      { key: 'AK', name: t('auto.atmakaraka') },
                      { key: 'AmK', name: t('auto.amatyakaraka') },
                      { key: 'BK', name: t('auto.bhratrikaraka') },
                      { key: 'MK', name: t('auto.matrikaraka') },
                      { key: 'PiK', name: t('auto.pitrikaraka') },
                      { key: 'GnK', name: t('auto.gnatikaraka') },
                      { key: 'DK', name: t('auto.darakaraka') },
                    ];
                    return (
                      <Table className="w-full text-sm">
                        <TableHeader>
                          <TableRow>
                            <TableHead className="text-left">{t('table.karaka')}</TableHead>
                            <TableHead className="text-left">{t('table.planet')}</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {karakaOrder.map(({ key, name }) => {
                            const planet = Object.entries(karakas).find(([, v]) => v === key)?.[0] || '-';
                            return (
                              <TableRow key={key}>
                                <TableCell className="text-foreground">
                                  <span className="font-semibold">{key}</span> <span className="text-sm text-foreground">({name})</span>
                                </TableCell>
                                <TableCell className="font-semibold text-foreground">{translatePlanet(planet, language)}</TableCell>
                              </TableRow>
                            );
                          })}
                        </TableBody>
                      </Table>
                    );
                  })()}
                </div>

	                {/* 7. Yoga & Dosha */}
	                <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden lg:col-span-2">
	                  <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
	                    {t('section.yogasAndDoshas')}
	                  </div>
	                  <div className="p-3">
	                    {loadingYogaDosha ? (
	                      <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
	                    ) : yogaDoshaData ? (
	                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
	                        <div>
	                          <div className="flex items-center gap-2 mb-2">
	                            <CheckCircle className="w-4 h-4 text-green-500" />
	                            <Heading as={5} variant={5}>{t('section.yogas')}</Heading>
	                          </div>
	                          <div className="space-y-1">
	                            {(yogaDoshaData.yogas || []).filter((y: any) => y.present).slice(0, 8).map((yoga: any, idx: number) => (
	                              <div key={idx} className="rounded-lg p-2 text-sm border border-green-300 bg-green-500">
	                                <div className="flex items-center justify-between">
	                                  <span className="font-medium text-foreground">{translateName(yoga.name, language)}</span>
	                                  <span className="text-sm px-1.5 py-0.5 rounded-full bg-green-100 text-green-800">
	                                    {t('common.present')}
	                                  </span>
	                                </div>
	                              </div>
	                            ))}
	                            {(yogaDoshaData.yogas || []).filter((y: any) => y.present).length === 0 && (
	                              <p className="text-sm text-foreground py-2">{t('kundli.noYogasDetected')}</p>
	                            )}
	                          </div>
	                        </div>
	                        <div>
	                          <div className="flex items-center gap-2 mb-2">
	                            <Shield className="w-4 h-4 text-red-500" />
	                            <Heading as={5} variant={5}>{t('section.doshas')}</Heading>
	                          </div>
	                          <div className="space-y-1">
	                            {(yogaDoshaData.doshas || []).filter((d: any) => d.present).slice(0, 8).map((dosha: any, idx: number) => (
	                              <div key={idx} className="rounded-lg p-2 text-sm border border-red-300 bg-red-500">
	                                <div className="flex items-center justify-between">
	                                  <span className="font-medium text-foreground">{translateName(dosha.name, language)}</span>
	                                  <span className="text-sm px-1.5 py-0.5 rounded-full bg-red-100 text-red-800">
	                                    {t('common.present')}
	                                  </span>
	                                </div>
	                              </div>
	                            ))}
	                            {(yogaDoshaData.doshas || []).filter((d: any) => d.present).length === 0 && (
	                              <p className="text-sm text-green-400 py-2">{t('kundli.noDoshasDetected')}</p>
	                            )}
	                          </div>
	                        </div>
	                      </div>
	                    ) : (
	                      <p className="text-center text-foreground py-4 text-sm">{t('common.loading')}</p>
	                    )}
	                  </div>
	                </div>

                {/* 7b. Mangal / Kaal Sarp / Sade Sati Dosha */}
                <div className="bg-muted rounded-xl border border-border p-4 lg:col-span-2">
                  <Heading as={4} variant={4} className="mb-3">{t('section.doshaAnalysis')}</Heading>
                  {loadingDosha ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
                  ) : doshaData ? (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {/* Mangal Dosha */}
                      <div className={`rounded-lg p-3 border ${doshaData.mangal_dosha?.has_dosha ? 'border-red-300 bg-red-500' : 'border-green-300 bg-green-500'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <Heading as={5} variant={5}>{translateName('Mangal Dosha', language)}</Heading>
                          <span className={`text-sm px-2 py-0.5 rounded-full font-medium ${doshaData.mangal_dosha?.has_dosha ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaData.mangal_dosha?.has_dosha ? translateLabel(doshaData.mangal_dosha.severity, language) || t('common.present') : t('common.absent')}
                          </span>
                        </div>
                        <p className="text-sm text-foreground">{translateBackend(doshaData.mangal_dosha?.description, language) || t('kundli.noMangalDosha')}</p>
                      </div>
                      {/* Kaal Sarp Dosha */}
                      <div className={`rounded-lg p-3 border ${doshaData.kaal_sarp_dosha?.has_dosha ? 'border-red-300 bg-red-500' : 'border-green-300 bg-green-500'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <Heading as={5} variant={5}>{translateName('Kaal Sarp Dosha', language)}</Heading>
                          <span className={`text-sm px-2 py-0.5 rounded-full font-medium ${doshaData.kaal_sarp_dosha?.has_dosha ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaData.kaal_sarp_dosha?.has_dosha ? translateLabel(doshaData.kaal_sarp_dosha.severity, language) || t('common.present') : t('common.absent')}
                          </span>
                        </div>
                        <p className="text-sm text-foreground">{translateBackend(doshaData.kaal_sarp_dosha?.description, language) || t('kundli.noKaalSarpDosha')}</p>
                      </div>
                      {/* Sade Sati */}
                      <div className={`rounded-lg p-3 border ${doshaData.sade_sati?.has_sade_sati ? 'border-orange-500 bg-orange-500' : 'border-green-300 bg-green-500'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <Heading as={5} variant={5}>{translateName('Sade Sati', language)}</Heading>
                          <span className={`text-sm px-2 py-0.5 rounded-full font-medium ${doshaData.sade_sati?.has_sade_sati ? 'bg-orange-100 text-orange-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaData.sade_sati?.has_sade_sati ? `${t('common.active')} - ${translateLabel(doshaData.sade_sati.phase, language)}` : t('common.inactive')}
                          </span>
                        </div>
                        <p className="text-sm text-foreground">{translateBackend(doshaData.sade_sati?.description, language) || t('kundli.sadeSatiNotActive')}</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-foreground py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 8. Ashtakvarga SAV bar chart */}
                <div className="bg-muted rounded-xl border border-border p-4">
                  <Heading as={4} variant={4} className="mb-3">{t('section.sarvashtakvarga')}</Heading>
                  {loadingAshtakvarga ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
                  ) : ashtakvargaData ? (
                    <div>
                      <div className="flex items-end gap-1 h-36">
                        {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map((sign) => {
                          const points = ashtakvargaData.sarvashtakvarga?.[sign] || 0;
                          const maxPoints = 56;
                          const heightPct = Math.round((points / maxPoints) * 100);
                          const isStrong = points >= 28;
                          return (
                            <div key={sign} className="flex-1 flex flex-col items-center gap-0.5">
                              <span className="text-sm font-medium text-foreground">{points}</span>
                              <div className="w-full bg-muted rounded-t-sm relative h-[100px]">
                                <div
                                  className="absolute bottom-0 w-full rounded-t-sm"
                                  style={{ height: `${heightPct}%`, backgroundColor: isStrong ? 'var(--aged-gold-dim)' : 'var(--ink-light)' }}
                                />
                              </div>
                              <span className="text-sm text-foreground">{translateSignAbbr(sign, language)}</span>
                            </div>
                          );
                        })}
                      </div>
                      <div className="flex items-center gap-3 mt-2 text-sm text-foreground">
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />{t('kundli.strong')}</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--ink-light)' }} />{t('kundli.weak')}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-foreground py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 9. Shadbala + Bhav Bala bar charts */}
                <div className="bg-muted rounded-xl border border-border p-4 space-y-4">
                  {/* Shadbala */}
                  <div>
                    <Heading as={4} variant={4} className="mb-3">{t('section.shadbalaStrength')}</Heading>
                    {loadingShadbala ? (
                      <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
                    ) : shadbalaData?.planets ? (
                      <div>
                        <div className="flex items-end justify-around gap-1 h-[180px]">
                          {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                            const data = shadbalaData.planets[planet];
                            if (!data) return null;
                            const ratio = (data.total || 0) / (data.required || 1);
                            const barHeight = Math.min((ratio / 1.5) * 100, 100);
                            const isStrong = ratio >= 1.0;
                            const barColor = isStrong ? '#16a34a' : '#dc2626';
                            const requiredPct = (1 / 1.5) * 100;
                            return (
                              <div key={planet} className="flex flex-col items-center gap-1 flex-1 min-w-[36px]">
                                <span className={`text-xs font-bold ${isStrong ? 'text-green-700' : 'text-red-600'}`}>
                                  {data.total.toFixed(1)}
                                </span>
                                <div className="relative w-full flex justify-center bg-muted/20 rounded-t-lg h-[130px]">
                                  <div className="absolute w-full border-t-2 border-dashed border-red-400 z-10" style={{ bottom: `${requiredPct}%` }} title={`${t('kundli.required')}: ${data.required}`} />
                                  <div className="w-5 rounded-t-lg transition-all duration-500" style={{ height: `${barHeight}%`, backgroundColor: barColor, alignSelf: 'flex-end' }} />
                                </div>
                                <span className="text-xs font-medium text-foreground text-center leading-tight mt-1">
                                  {translatePlanetAbbr(planet, language)}
                                </span>
                              </div>
                            );
                          })}
                        </div>
                        <div className="flex items-center gap-3 mt-2 text-xs text-foreground">
                          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#16a34a' }} />{t('kundli.strong')}</span>
                          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#dc2626' }} />{t('kundli.weak')}</span>
                          <span className="flex items-center gap-1"><span className="w-4 border-t-2 border-dashed border-red-400" />{t('kundli.required')}</span>
                        </div>
                      </div>
                    ) : (
                      <p className="text-center text-foreground py-4 text-sm">{t('common.loading')}</p>
                    )}
                  </div>

                  {/* Bhav Bala */}
                  {shadbalaData?.bhav_bala && (
                    <div>
                      <div className="border-t border-border/30 pt-4">
                        <Heading as={4} variant={4} className="mb-3">{t('section.bhavBala')}</Heading>
                        <div className="overflow-x-auto -mx-1 px-1">
                          <div className="flex items-end gap-1" style={{ height: '160px', minWidth: '360px' }}>
                            {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
                              const data = shadbalaData.bhav_bala[house];
                              if (!data) return null;
                              const maxVal = Math.max(...Object.values(shadbalaData.bhav_bala as Record<string, {total: number}>).map((d) => d.total), 1);
                              const barHeight = Math.min((data.total / maxVal) * 100, 100);
                              const barColor = data.total >= maxVal * 0.5 ? '#16a34a' : '#dc2626';
                              return (
                                <div key={house} className="flex flex-col items-center gap-1 flex-1">
                                  <span className="text-xs font-bold" style={{ color: barColor, fontSize: '9px' }}>
                                    {data.total.toFixed(1)}
                                  </span>
                                  <div className="relative w-full flex justify-center bg-muted/20 rounded-t-lg h-[110px]">
                                    <div className="w-3 rounded-t-lg transition-all duration-500" style={{ height: `${barHeight}%`, backgroundColor: barColor, alignSelf: 'flex-end' }} />
                                  </div>
                                  <span className="text-xs font-medium text-foreground text-center leading-tight mt-1" style={{ fontSize: '9px' }}>{house}</span>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                        <p className="text-xs text-foreground mt-1 text-center">{t('report.houseNumberRange')}</p>
                      </div>
                    </div>
                  )}
                </div>

              </div>
            </div>
  );
}
