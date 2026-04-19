import { Loader2, CheckCircle, Shield, ChevronDown } from 'lucide-react';
import { formatDate } from '@/lib/api';
import { Button } from '@/components/ui/button';
import InteractiveKundli, { ChartLegend, type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { DIVISIONAL_CHART_OPTIONS } from '@/components/kundli/kundli-utils';
import { calculateJaiminiKarakas } from '@/components/kundli/jhora-utils';
import LordshipsTab from '@/components/kundli/LordshipsTab';
import { translatePlanet, translateSign, translateLabel, translateName, translateNakshatra, translateBackend, translateSignAbbr, translatePlanetAbbr } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

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
                <div className="bg-muted rounded-xl border border-border p-3">
                  <Heading as={4} variant={4} className="mb-2 text-center">
                    {t('section.lagna')}
                  </Heading>
                  <div className="flex justify-center">
                    {(() => {
                      const shift = reportLagnaShift;
                      const basePlanets = planets;
                      const baseHouses = result.chart_data?.houses;
                      const shiftedPlanets = shift
                        ? basePlanets.map((p: PlanetData) => ({
                            ...p,
                            house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                          }))
                        : basePlanets;
                      const shiftedHouses = shift && baseHouses
                        ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                        : baseHouses;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: shiftedPlanets, houses: shiftedHouses, ascendant: result.chart_data?.ascendant } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                            setReportLagnaShift(orig - 1 === 0 ? 0 : orig - 1);
                          }}
                          compact
                        />
                      );
                    })()}
                  </div>
                  {reportLagnaShift > 0 && (
                    <button onClick={() => setReportLagnaShift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
                  )}
                </div>

                {/* 2. Moon Chart — click house to rotate lagan */}
                <div className="bg-muted rounded-xl border border-border p-3">
                  <Heading as={4} variant={4} className="mb-2 text-center">
                    {t('section.moon')}
                  </Heading>
                  <div className="flex justify-center">
                    {(() => {
                      const moonPlanet = planets.find((p: PlanetData) => p.planet === 'Moon');
                      const moonHouse = moonPlanet?.house || 1;
                      const baseShift = moonHouse - 1;
                      const totalShift = baseShift + reportMoonShift;
                      const moonPlanets = planets.map((p: PlanetData) => ({
                        ...p,
                        house: ((((p.house || 1) - 1 - totalShift + 24) % 12) + 1),
                      }));
                      const moonHouses = result.chart_data?.houses
                        ? result.chart_data.houses.map((h: { number: number; sign: string }) => ({
                            number: ((h.number - 1 - totalShift + 24) % 12) + 1,
                            sign: h.sign,
                          }))
                        : undefined;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: moonPlanets, houses: moonHouses } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = totalShift ? ((house - 1 + totalShift) % 12) + 1 : house;
                            const newShift = ((orig - 1) - baseShift + 12) % 12;
                            setReportMoonShift(newShift);
                          }}
                          compact
                        />
                      );
                    })()}
                  </div>
                  {reportMoonShift > 0 && (
                    <button onClick={() => setReportMoonShift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
                  )}
                </div>

                {/* 3. Gochar (Transit) Chart — click house to rotate lagan */}
                <div className="bg-muted rounded-xl border border-border p-3">
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
                        house: tr.house || 1,
                        nakshatra: tr.nakshatra || '',
                        sign_degree: tr.sign_degree || tr.degree || 0,
                        status: tr.is_retrograde ? 'Retrograde' : '',
                        is_retrograde: tr.is_retrograde,
                      }));
                      const baseHouses = transitData.chart_data?.houses || result.chart_data?.houses;
                      const shiftedPlanets = shift
                        ? transitPlanets.map((p: any) => ({
                            ...p,
                            house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                          }))
                        : transitPlanets;
                      const shiftedHouses = shift && baseHouses
                        ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                        : baseHouses;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: shiftedPlanets, houses: shiftedHouses } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                            setReportGocharShift(orig - 1 === 0 ? 0 : orig - 1);
                          }}
                          compact
                        />
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
                <div className="lg:col-span-2 bg-muted rounded-xl border border-border p-4 flex flex-col">
                  <Heading as={4} variant={4} className="mb-3">{t('section.detailedPlanetPositions')}</Heading>
                  <div className="overflow-x-auto flex-1">
                    <Table className="w-full text-xs">
                      <TableHeader className="bg-muted">
                        <TableRow>
                          <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.planet')}</TableHead>
                          <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.sign')}</TableHead>
                          <TableHead className="text-center p-1.5 text-primary font-medium">{t('table.house')}</TableHead>
                          <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                          <TableHead className="text-center p-1.5 text-primary font-medium whitespace-nowrap">{t('table.degree')}</TableHead>
                          <TableHead className="text-center p-1.5 text-primary font-medium">{t('table.status')}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {planets.map((planet: any, index: number) => (
                          <TableRow key={index} className="border-t border-border hover:bg-muted/5">
                            <TableCell className="p-1.5 text-foreground font-medium">{translatePlanet(planet.planet, language)}</TableCell>
                            <TableCell className="p-1.5 text-foreground">{translateSign(planet.sign, language)}</TableCell>
                            <TableCell className="p-1.5 text-center text-foreground">{planet.house}</TableCell>
                            <TableCell className="p-1.5 text-foreground">{translateNakshatra(planet.nakshatra, language) || '\u2014'}</TableCell>
                            <TableCell className="p-1.5 text-center text-foreground whitespace-nowrap">{(Number(planet.sign_degree) || 0).toFixed(1)}°</TableCell>
                            <TableCell className="p-1.5 text-center">
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
                <div className="lg:col-span-1 bg-muted rounded-xl border border-border p-4 flex flex-col">
                  <div className="flex items-center justify-between mb-3">
                    <Heading as={4} variant={4}>{t('kundli.divisionalCharts')}</Heading>
                    <select
                      value={selectedDivision}
                      onChange={(e) => changeDivision(e.target.value)}
                      className="bg-card border border-border rounded-lg px-2 py-1 text-foreground text-xs focus:border-border focus:outline-none"
                    >
                      {DIVISIONAL_CHART_OPTIONS.map((c) => (
                        <option key={c.code} value={c.code}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                  {loadingDivisional ? (
                    <div className="flex items-center justify-center py-8 flex-1"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
                  ) : divisionalData?.planet_positions ? (
                    <div className="flex justify-center flex-1 items-center">
                      <InteractiveKundli
                        chartData={{
                          planets: divisionalData.planet_positions.map((p: any) => ({
                            planet: p.planet,
                            sign: p.sign,
                            house: p.house,
                            nakshatra: p.nakshatra || '',
                            sign_degree: p.sign_degree || 0,
                            status: '',
                          })),
                          houses: divisionalData.houses || Array.from({ length: 12 }, (_, i) => ({
                            number: i + 1,
                            sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
                          })),
                        } as ChartData}
                        onPlanetClick={handlePlanetClick}
                        onHouseClick={handleHouseClick}
                        compact
                      />
                    </div>
                  ) : (
                    <p className="text-center text-foreground py-8 text-sm flex-1 flex items-center justify-center">{t('kundli.selectChart')}</p>
                  )}
                </div>
              </div>

              {/* Grid layout for remaining items — 2 columns on desktop, 1 on mobile */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 print:grid-cols-2">

                {/* 4. Lordships */}
                <div className="bg-muted rounded-xl border border-border p-4">
                  <Heading as={4} variant={4} className="mb-3">{t('section.houseLordships')}</Heading>
                  <LordshipsTab planets={planets} houses={result.chart_data?.houses || {}} />
                </div>

                {/* 5. Avakhada Chakra */}
                <div className="bg-muted rounded-xl border border-border p-4">
                  <Heading as={4} variant={4} className="mb-3">{t('section.avakhadaChakra')}</Heading>
                  {loadingAvakhada ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
                  ) : avakhadaData ? (
                    <div className="grid grid-cols-2 gap-2">
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
                        <div key={item.label} className="rounded-lg p-2 bg-card">
                          <p className="text-sm text-foreground">{item.label}</p>
                          <p className="text-sm font-semibold text-foreground">{item.value}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-center text-foreground py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 6. Vimshottari Dasha — with expandable AD/PD */}
                <div className="bg-muted rounded-xl border border-border p-4">
                  <Heading as={4} variant={4} className="mb-3">{t('section.vimshottariDasha')}</Heading>
                  {(loadingDasha || loadingExtendedDasha) ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
                  ) : (extendedDashaData || dashaData) ? (
                    <div className="space-y-2">
                      {/* Current dasha info */}
                      <div className="rounded-lg p-3 bg-gold-10">
                        <p className="text-sm text-muted-foreground">{t('section.currentMahadasha')}</p>
                        <p className="text-sm font-bold text-primary">
                          {translatePlanet((extendedDashaData || dashaData).current_dasha, language)}
                        </p>
                        {(extendedDashaData || dashaData).current_antardasha && (extendedDashaData || dashaData).current_antardasha !== 'Unknown' && (
                          <p className="text-sm text-primary">
                            {t('report.adLabel')} {translatePlanet((extendedDashaData || dashaData).current_antardasha, language)}
                            {extendedDashaData?.current_pratyantar && extendedDashaData.current_pratyantar !== 'Unknown' && ` / ${t('report.pdLabel')} ${translatePlanet(extendedDashaData.current_pratyantar, language)}`}
                          </p>
                        )}
                      </div>

                      {/* Expandable Mahadasha list */}
                      {extendedDashaData?.mahadasha ? (
                        <div className="space-y-1">
                          {extendedDashaData.mahadasha.map((md: any) => (
                            <div key={md.planet} className="border border-border rounded-lg overflow-hidden">
                              <button
                                onClick={() => setExpandedMahadasha(expandedMahadasha === md.planet ? null : md.planet)}
                                className="w-full flex items-center justify-between p-2 text-sm transition-colors"
                                style={{ background: md.is_current ? 'rgba(184,134,11,0.12)' : 'transparent' }}
                              >
                                <span className="flex items-center gap-1.5">
                                  <ChevronDown className={`w-3 h-3 transition-transform text-primary ${expandedMahadasha === md.planet ? 'rotate-180' : ''}`} />
                                  <span className="font-semibold" style={{ color: md.is_current ? 'var(--aged-gold)' : 'var(--ink)' }}>
                                    {translatePlanet(md.planet, language)} {md.is_current ? '←' : ''}
                                  </span>
                                </span>
                                <span className="text-muted-foreground">{md.start?.slice(0,10)} — {md.end?.slice(0,10)} ({md.years} {t('table.years')})</span>
                              </button>

                              {expandedMahadasha === md.planet && (md.antardasha || []).length > 0 && (
                                <div className="border-t border-border">
                                  {md.antardasha.map((ad: any) => (
                                    <div key={`${md.planet}-${ad.planet}`}>
                                      <button
                                        onClick={() => setExpandedAntardasha(expandedAntardasha === `${md.planet}-${ad.planet}` ? null : `${md.planet}-${ad.planet}`)}
                                        className="w-full flex items-center justify-between px-4 py-1.5 text-sm"
                                        style={{ background: ad.is_current ? 'rgba(184,134,11,0.06)' : 'transparent' }}
                                      >
                                        <span className="flex items-center gap-1">
                                          {ad.pratyantar?.length > 0 && <ChevronDown className={`w-2.5 h-2.5 transition-transform text-muted-foreground ${expandedAntardasha === `${md.planet}-${ad.planet}` ? 'rotate-180' : ''}`} />}
                                          <span style={{ color: ad.is_current ? 'var(--aged-gold)' : 'var(--ink)' }}>{translatePlanet(ad.planet, language)} {t('report.adLabel')} {ad.is_current ? '*' : ''}</span>
                                        </span>
                                        <span style={{ color: 'var(--ink-light)', fontSize: 'var(--text-label, 0.875rem)' }}>{ad.start?.slice(0,10)} — {ad.end?.slice(0,10)}</span>
                                      </button>

                                      {expandedAntardasha === `${md.planet}-${ad.planet}` && (ad.pratyantar || []).length > 0 && (
                                        <div className="border-t border-border">
                                          {ad.pratyantar.map((pt: any, idx: number) => (
                                            <div key={idx} className="flex items-center justify-between px-8 py-1 text-sm"
                                              style={{ background: pt.is_current ? 'rgba(184,134,11,0.04)' : 'transparent' }}>
                                              <span style={{ color: pt.is_current ? 'var(--aged-gold)' : 'var(--ink-light)' }}>
                                                {translatePlanet(pt.planet, language)} {t('report.pdLabel')} {pt.is_current ? '*' : ''}
                                              </span>
                                              <span style={{ color: 'var(--ink-light)', fontSize: 'var(--text-label, 0.875rem)' }}>{pt.start?.slice(0,10)} — {pt.end?.slice(0,10)}</span>
                                            </div>
                                          ))}
                                        </div>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      ) : (
                        /* Fallback: simple table when extendedDashaData unavailable */
                        <div className="overflow-x-auto">
                          <Table className="w-full text-sm">
                            <TableHeader><TableRow className="bg-gold-10">
                              <TableHead className="text-left p-2 font-medium text-primary">{t('table.planet')}</TableHead>
                              <TableHead className="text-left p-2 font-medium text-primary">{t('table.start')}</TableHead>
                              <TableHead className="text-left p-2 font-medium text-primary">{t('table.end')}</TableHead>
                              <TableHead className="text-center p-2 font-medium text-primary">{t('table.years')}</TableHead>
                            </TableRow></TableHeader>
                            <TableBody>
                              {(dashaData.mahadasha_periods || []).map((p: any) => (
                                <TableRow key={p.planet} className="border-t border-border" style={{ background: p.planet === dashaData.current_dasha ? 'rgba(184,134,11,0.1)' : 'transparent' }}>
                                  <TableCell className="p-2 text-foreground">{translatePlanet(p.planet, language)}{p.planet === dashaData.current_dasha ? ' ←' : ''}</TableCell>
                                  <TableCell className="p-2 text-muted-foreground">{p.start_date}</TableCell>
                                  <TableCell className="p-2 text-muted-foreground">{p.end_date}</TableCell>
                                  <TableCell className="p-2 text-center text-muted-foreground">{p.years}</TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-center py-4 text-sm text-muted-foreground">{t('common.loading')}</p>
                  )}
                </div>

                {/* 6b. Jaimini Karakas — separate card */}
                <div className="bg-muted rounded-xl border border-border p-4">
                  <Heading as={4} variant={4} className="mb-3">{t('section.jaiminiKarakas')}</Heading>
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
                        <TableHeader><TableRow className="bg-muted">
                          <TableHead className="text-left p-2 text-primary font-medium">{t('table.karaka')}</TableHead>
                          <TableHead className="text-left p-2 text-primary font-medium">{t('table.planet')}</TableHead>
                        </TableRow></TableHeader>
                        <TableBody>
                          {karakaOrder.map(({ key, name }) => {
                            const planet = Object.entries(karakas).find(([, v]) => v === key)?.[0] || '-';
                            return (
                              <TableRow key={key} className="border-t border-border">
                                <TableCell className="p-2 text-foreground"><span className="font-semibold">{key}</span> <span className="text-sm text-foreground">({name})</span></TableCell>
                                <TableCell className="p-2 font-semibold text-primary">{translatePlanet(planet, language)}</TableCell>
                              </TableRow>
                            );
                          })}
                        </TableBody>
                      </Table>
                    );
                  })()}
                </div>

                {/* 7. Yoga & Dosha */}
                <div className="bg-muted rounded-xl border border-border p-4 lg:col-span-2">
                  <Heading as={4} variant={4} className="mb-3">{t('section.yogasAndDoshas')}</Heading>
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
